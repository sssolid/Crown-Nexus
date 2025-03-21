# app/data_import/commands/import_products.py
from __future__ import annotations

"""
Command for importing products.

This module provides a CLI command for importing product data from
FileMaker or files.
"""

import asyncio
import json
import sys
from typing import Dict, List, Optional

import typer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.core.logging import get_logger
from app.data_import.connectors.file_connector import (
    FileConnector,
    FileConnectionConfig,
)
from app.data_import.connectors.filemaker_connector import (
    FileMakerConnector,
    FileMakerConnectionConfig,
)
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.pipeline.product_pipeline import ProductPipeline
from app.data_import.processors.product_processor import (
    ProductMappingConfig,
    ProductProcessor,
)
from app.db.session import get_db_context

logger = get_logger("app.data_import.commands.import_products")

app = typer.Typer()


@app.command()
def import_products(
    source_type: str = typer.Option(
        "filemaker", "--source", "-s", help="Source type (filemaker or file)"
    ),
    config_file: str = typer.Option(
        None, "--config", "-c", help="Path to configuration JSON file"
    ),
    query: str = typer.Option(
        None, "--query", "-q", help="Query or table name to extract data from"
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
    dsn: Optional[str] = typer.Option(None, "--dsn", help="FileMaker ODBC DSN"),
    # FileMaker specific options
    username: Optional[str] = typer.Option(
        None, "--username", "-u", help="FileMaker username"
    ),
    password: Optional[str] = typer.Option(
        None, "--password", "-p", help="FileMaker password"
    ),
    database: Optional[str] = typer.Option(
        None,
        "--database",
        "-db",
        help="FileMaker database name (optional, may be included in DSN)",
    ),
    file_path: Optional[str] = typer.Option(
        None, "--file", "-f", help="Path to input file (CSV or JSON)"
    ),
    # Mapping options
    mapping_file: Optional[str] = typer.Option(
        None, "--mapping", "-m", help="Path to field mapping JSON file"
    ),
    # File specific options
    file_type: Optional[str] = typer.Option(
        None, "--file-type", "-ft", help="File type (csv or json)"
    ),
    disable_ssl: bool = typer.Option(
        False, "--disable-ssl-verification", help="Disable SSL certificate verification"
    ),
    limit: Optional[int] = typer.Option(
        None, "--limit", "-l", help="Limit the number of records to import"
    ),
) -> None:
    """
    Import products from FileMaker or file.

    This command extracts product data from FileMaker or a file,
    processes and validates it, and imports it into the database.
    """
    try:
        # Load configuration
        connector_config = _load_connector_config(
            source_type=source_type,
            config_file=config_file,
            dsn=dsn,
            username=username,
            password=password,
            database=database,
            file_path=file_path,
            file_type=file_type,
            disable_ssl=disable_ssl,
        )

        mapping_config = _load_mapping_config(mapping_file)

        if not query:
            if source_type == "filemaker":
                query = "Products"
            else:
                query = ""

        # Run the import
        result = asyncio.run(
            _run_import(
                source_type=source_type,
                connector_config=connector_config,
                mapping_config=mapping_config,
                query=query,
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
        typer.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def _load_connector_config(
    source_type: str,
    config_file: Optional[str],
    dsn: Optional[str],
    username: Optional[str],
    password: Optional[str],
    database: Optional[str],
    file_path: Optional[str],
    file_type: Optional[str],
    disable_ssl: bool = False,
) -> Dict:
    """
    Load connector configuration from file or command line options.

    Args:
        source_type: Source type (filemaker or file)
        config_file: Path to configuration file
        dsn: FileMaker DSN
        username: FileMaker username
        password: FileMaker password
        database: FileMaker database
        file_path: Path to input file
        file_type: File type

    Returns:
        Connector configuration dictionary

    Raises:
        ValueError: If required configuration is missing
    """
    if config_file:
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                return config
        except Exception as e:
            raise ValueError(f"Failed to load configuration file: {str(e)}") from e

    if source_type == "filemaker":
        if not all([dsn, username, password]):
            raise ValueError(
                "FileMaker source requires dsn, username, and password. "
                "Provide them as command line options or in a config file."
            )
        config = {
            "dsn": dsn,
            "username": username,
            "password": password,
            "disable_ssl_verification": disable_ssl,
        }

        # Only add database if specified
        if database:
            config["database"] = database

        return config

    elif source_type == "file":
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


def _load_mapping_config(mapping_file: Optional[str]) -> Dict:
    """
    Load field mapping configuration from file.

    Args:
        mapping_file: Path to mapping file

    Returns:
        Mapping configuration dictionary

    Raises:
        ValueError: If mapping file cannot be loaded
    """
    if mapping_file:
        try:
            with open(mapping_file, "r") as f:
                config = json.load(f)
                return config
        except Exception as e:
            raise ValueError(f"Failed to load mapping file: {str(e)}") from e

    # Default mapping configuration
    return {
        "part_number_field": "PartNumber",
        "application_field": "Application",
        "vintage_field": "Vintage",
        "late_model_field": "LateModel",
        "soft_field": "Soft",
        "universal_field": "Universal",
        "active_field": "Active",
        "boolean_true_values": ["yes", "y", "true", "t", "1", "on"],
        "boolean_false_values": ["no", "n", "false", "f", "0", "off"],
        "description_fields": {
            "Short": "ShortDescription",
            "Long": "Description",
            "Keywords": "Keywords",
        },
        "marketing_fields": {"Bullet Point": "BulletPoints"},
    }


async def _run_import(
    source_type: str,
    connector_config: Dict,
    mapping_config: Dict,
    query: str,
    limit: Optional[int],
    dry_run: bool,
    output_file: Optional[str],
) -> Dict:
    """
    Run the import pipeline.

    Args:
        source_type: Source type (filemaker or file)
        connector_config: Connector configuration
        mapping_config: Mapping configuration
        query: Query string
        dry_run: Dry run flag
        output_file: Output file path

    Returns:
        Import result statistics

    Raises:
        AppException: If import fails
    """
    async with get_db_context() as db:
        # Create connector
        if source_type == "filemaker":
            connector = FileMakerConnector(
                FileMakerConnectionConfig(**connector_config)
            )
        else:
            connector = FileConnector(FileConnectionConfig(**connector_config))

        # Create processor
        processor = ProductProcessor(ProductMappingConfig(**mapping_config))

        # Create importer
        importer = ProductImporter(db)

        # Create pipeline
        pipeline = ProductPipeline(
            connector=connector, processor=processor, importer=importer, dry_run=dry_run
        )

        # Run pipeline
        result = await pipeline.run(query, limit=limit)

        # If dry run and output file, write processed data
        if dry_run and output_file and "processed_data" in result:
            try:
                with open(output_file, "w") as f:
                    json.dump(result["processed_data"], f, indent=2)
                typer.echo(f"Processed data written to {output_file}")
            except Exception as e:
                typer.echo(f"Failed to write output file: {str(e)}", err=True)

        return result


def _print_result(result: Dict) -> None:
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
