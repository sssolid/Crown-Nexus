# backend/app/data_import/commands/import_products.py
from __future__ import annotations

"""
Command for importing products using field definitions.

This module provides a CLI command for importing product data from
various sources using centralized field definitions and settings.
"""

import asyncio
import json
import sys
import time
from typing import Dict, List, Optional, Any

import typer

from app.logging import get_logger
from app.core.config.integrations.filemaker import get_filemaker_connector_config
from app.core.config.integrations.as400 import get_as400_connector_config
from app.data_import.connectors.file_connector import (
    FileConnector,
    FileConnectionConfig,
)
from app.data_import.connectors.filemaker_connector import (
    FileMakerConnector,
    FileMakerConnectionConfig,
)
from app.data_import.connectors.as400_connector import (
    AS400Connector,
    AS400ConnectionConfig,
)
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.pipeline.product_pipeline import ProductPipeline
from app.data_import import create_processor, EntityType, SourceType
from app.data_import.field_definitions import generate_query_for_entity
from app.db.session import get_db_context

logger = get_logger("app.data_import.commands.import_products")

app = typer.Typer()


@app.command()
def import_products(
    source_type: str = typer.Option(
        "filemaker", "--source", "-s", help="Source type (filemaker, as400, or file/csv)"
    ),
    entity_type: str = typer.Option(
        "product", "--entity", "-e", help="Entity type (product, product_pricing, product_stock)"
    ),
    config_file: Optional[str] = typer.Option(
        None, "--config", "-c", help="Optional path to configuration JSON file (overrides settings)"
    ),
    custom_query: Optional[str] = typer.Option(
        None, "--query", "-q", help="Custom query (overrides generated query)"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Dry run (extract, process, validate, but don't import)",
    ),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output file for processed data (dry run only)"
    ),
    # File specific options (only needed for CSV/file source)
    file_path: Optional[str] = typer.Option(
        None, "--file", "-f", help="Path to input file (CSV or JSON)"
    ),
    file_type: Optional[str] = typer.Option(
        None, "--file-type", "-ft", help="File type (csv or json)"
    ),
    limit: Optional[int] = typer.Option(
        None, "--limit", "-l", help="Limit the number of records to import"
    ),
    # Field selection options
    fields: Optional[str] = typer.Option(
        None, "--fields", help="Comma-separated list of fields to import"
    ),
) -> None:
    """
    Import entity data from FileMaker, AS400, or file.

    This command extracts entity data from a source using field definitions,
    processes and validates it, and imports it into the database.
    """
    try:
        # Normalize source type
        normalized_source_type = source_type.lower()
        if normalized_source_type == "file":
            normalized_source_type = "csv"

        # Normalize entity type
        normalized_entity_type = entity_type.lower()

        # Load configuration
        connector_config = _load_connector_config(
            source_type=normalized_source_type,
            config_file=config_file,
            file_path=file_path,
            file_type=file_type,
        )

        # Parse field list if provided
        field_list = None
        if fields:
            field_list = [f.strip() for f in fields.split(",")]

        # Run the import
        result = asyncio.run(
            _run_import(
                source_type=normalized_source_type,
                entity_type=normalized_entity_type,
                connector_config=connector_config,
                custom_query=custom_query,
                fields=field_list,
                limit=limit,
                dry_run=dry_run,
                output_file=output_file,
            )
        )

        # Print result
        _print_result(result)

        # Exit with success code if successful
        if result.get("success", False):
            typer.echo("Import completed successfully")
            sys.exit(0)
        else:
            typer.echo("Import failed", err=True)
            sys.exit(1)

    except Exception as e:
        logger.exception(f"Error in import_products: {str(e)}")
        typer.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def _load_connector_config(
    source_type: str,
    config_file: Optional[str],
    file_path: Optional[str],
    file_type: Optional[str],
) -> Dict[str, Any]:
    """
    Load connector configuration from settings or config file.

    Args:
        source_type: Source type (filemaker, as400, or csv)
        config_file: Optional path to configuration file
        file_path: Path to input file (for file source)
        file_type: File type (for file source)

    Returns:
        Connector configuration dictionary

    Raises:
        ValueError: If required configuration is missing
    """
    # If a config file is provided, it takes precedence
    if config_file:
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                return config
        except Exception as e:
            raise ValueError(f"Failed to load configuration file: {str(e)}") from e

    # Load configuration from settings
    if source_type == "filemaker":
        return get_filemaker_connector_config()

    elif source_type == "as400":
        return get_as400_connector_config()

    elif source_type == "csv":
        if not file_path:
            raise ValueError(
                "File source requires file_path. "
                "Provide it as a command line option or in a config file."
            )

        if not file_type:
            if file_path.endswith(".csv"):
                file_type = "csv"
            elif file_path.endswith(".json"):
                file_type = "json"
            else:
                raise ValueError(
                    "Could not determine file type from file extension. "
                    "Provide file_type as a command line option or in a config file."
                )

        return {
            "file_path": file_path,
            "file_type": file_type,
            "encoding": "utf-8",
            "csv_delimiter": ",",
            "csv_quotechar": '"',
        }

    else:
        raise ValueError(f"Unsupported source type: {source_type}")


async def _run_import(
    source_type: str,
    entity_type: str,
    connector_config: Dict[str, Any],
    custom_query: Optional[str] = None,
    fields: Optional[List[str]] = None,
    limit: Optional[int] = None,
    dry_run: bool = False,
    output_file: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run the import pipeline.

    Args:
        source_type: Source type (filemaker, as400, or csv)
        entity_type: Entity type (product, product_pricing, etc.)
        connector_config: Connector configuration
        custom_query: Optional custom query
        fields: Optional list of specific fields to include
        limit: Record limit
        dry_run: Dry run flag
        output_file: Output file path

    Returns:
        Import result statistics

    Raises:
        Exception: If import fails
    """
    async with get_db_context() as db:
        start_time = time.time()

        # Create connector
        connector = _create_connector(source_type, connector_config)

        # Create processor using the factory
        processor = create_processor(
            entity_type=entity_type,
            source_type=source_type,
        )

        # Create importer
        importer = ProductImporter(db)

        # Create pipeline
        pipeline = ProductPipeline(
            connector=connector, processor=processor, importer=importer, dry_run=dry_run
        )

        # Generate query if not provided
        query = custom_query
        if not query:
            try:
                query = generate_query_for_entity(entity_type, source_type, fields)
                logger.info(f"Generated query: {query}")

                # Add LIMIT clause if specified
                if limit is not None:
                    if source_type == "as400":
                        query = f"{query} FETCH FIRST {limit} ROWS ONLY"
                    else:
                        query = f"{query} LIMIT {limit}"
            except Exception as e:
                logger.error(f"Failed to generate query: {str(e)}")
                raise ValueError(f"Failed to generate query: {str(e)}") from e

        # Run pipeline
        result = await pipeline.run(query, limit=limit)

        # Add timing information
        end_time = time.time()
        result["total_time"] = end_time - start_time

        # If dry run and output file, write processed data
        if dry_run and output_file and "processed_data" in result:
            try:
                with open(output_file, "w") as f:
                    json.dump(result["processed_data"], f, indent=2)
                logger.info(f"Processed data written to {output_file}")
            except Exception as e:
                logger.error(f"Failed to write output file: {str(e)}")

        return result


def _create_connector(source_type: str, config: Dict[str, Any]) -> Any:
    """
    Create an appropriate connector based on the source type.

    Args:
        source_type: Source type
        config: Connector configuration

    Returns:
        Connector instance

    Raises:
        ValueError: If source type is unsupported
    """
    if source_type == "filemaker":
        # Convert the SecretStr to a plain string for the connector
        if "password" in config and hasattr(config["password"], "get_secret_value"):
            config_copy = config.copy()
            config_copy["password"] = config["password"].get_secret_value()
            return FileMakerConnector(FileMakerConnectionConfig(**config_copy))
        return FileMakerConnector(FileMakerConnectionConfig(**config))

    elif source_type == "as400":
        # Convert the SecretStr to a plain string for the connector
        if "password" in config and hasattr(config["password"], "get_secret_value"):
            config_copy = config.copy()
            config_copy["password"] = config["password"].get_secret_value()
            return AS400Connector(AS400ConnectionConfig(**config_copy))
        return AS400Connector(AS400ConnectionConfig(**config))

    elif source_type == "csv":
        return FileConnector(FileConnectionConfig(**config))

    else:
        raise ValueError(f"Unsupported source type: {source_type}")


def _print_result(result: Dict[str, Any]) -> None:
    """
    Print import result.

    Args:
        result: Import result statistics
    """
    typer.echo("\nImport Result:")
    typer.echo(f"  Status: {'Success' if result.get('success', False) else 'Failed'}")
    typer.echo(f"  Message: {result.get('message', 'No message')}")
    typer.echo(f"  Extracted: {result.get('records_extracted', 0)} records")
    typer.echo(f"  Processed: {result.get('records_processed', 0)} records")
    typer.echo(f"  Validated: {result.get('records_validated', 0)} records")
    typer.echo(f"  Imported: {result.get('records_imported', 0)} records")
    typer.echo(f"    - Created: {result.get('records_created', 0)} records")
    typer.echo(f"    - Updated: {result.get('records_updated', 0)} records")
    typer.echo(f"    - Errors: {result.get('records_with_errors', 0)} records")
    typer.echo(f"  Timing:")
    typer.echo(f"    - Extract: {result.get('extract_time', 0):.2f} seconds")
    typer.echo(f"    - Process: {result.get('process_time', 0):.2f} seconds")
    typer.echo(f"    - Validate: {result.get('validate_time', 0):.2f} seconds")
    typer.echo(f"    - Import: {result.get('import_time', 0):.2f} seconds")
    typer.echo(f"    - Total: {result.get('total_time', 0):.2f} seconds")

    if result.get("dry_run", False):
        typer.echo("\nDRY RUN: No data was imported")


if __name__ == "__main__":
    app()
