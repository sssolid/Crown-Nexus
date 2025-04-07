from __future__ import annotations

"""
Command for running a complete data import process.

This module provides a CLI command for importing all types of data (products, pricing, stock, etc.)
in a single operation, with options for controlling logging verbosity, audit tracking,
and sync history.
"""
import asyncio
import json
import sys
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import typer
from sqlalchemy import select

from app.core.config.integrations.as400 import get_as400_connector_config
from app.core.config.integrations.filemaker import get_filemaker_connector_config
from app.data_import import create_processor, EntityType, SourceType
from app.data_import.connectors.as400_connector import (
    AS400ConnectionConfig,
    AS400Connector,
)
from app.data_import.connectors.file_connector import (
    FileConnectionConfig,
    FileConnector,
)
from app.data_import.connectors.filemaker_connector import (
    FileMakerConnectionConfig,
    FileMakerConnector,
)
from app.data_import.field_definitions import generate_query_for_entity
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.pipeline.product_pipeline import ProductPipeline
from app.db.session import get_db_context
from app.domains.sync_history.models import SyncEntityType, SyncSource, SyncStatus
from app.domains.sync_history.repository import SyncHistoryRepository
from app.logging import get_logger

logger = get_logger("app.data_import.commands.import_all")

app = typer.Typer()


class LoggingVerbosity:
    QUIET = "quiet"
    NORMAL = "normal"
    VERBOSE = "verbose"
    DEBUG = "debug"


@app.command()
def import_all(
    source_type: str = typer.Option(
        "filemaker",
        "--source",
        "-s",
        help="Source type (filemaker, as400, or file/csv)",
    ),
    config_file: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Optional path to configuration JSON file (overrides settings)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Dry run (extract, process, validate, but don't import)",
    ),
    output_dir: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for processed data (dry run only)",
    ),
    file_path: Optional[str] = typer.Option(
        None, "--file", "-f", help="Path to input file (CSV or JSON)"
    ),
    file_type: Optional[str] = typer.Option(
        None, "--file-type", "-ft", help="File type (csv or json)"
    ),
    limit: Optional[int] = typer.Option(
        None, "--limit", "-l", help="Limit the number of records to import"
    ),
    verbosity: str = typer.Option(
        LoggingVerbosity.NORMAL,
        "--verbosity",
        "-v",
        help=f"Logging verbosity: {LoggingVerbosity.QUIET}, {LoggingVerbosity.NORMAL}, {LoggingVerbosity.VERBOSE}, or {LoggingVerbosity.DEBUG}",
    ),
    system_user: Optional[str] = typer.Option(
        None,
        "--system-user",
        "-u",
        help="System user ID for audit logging",
    ),
    notify_users: bool = typer.Option(
        False,
        "--notify",
        "-n",
        help="Send notifications for updated products",
    ),
    entity_types: List[str] = typer.Option(
        ["product", "pricing", "stock"],
        "--entity-types",
        "-e",
        help="Entity types to import",
    ),
) -> None:
    """
    Import all specified entity types in a single operation.

    This command handles importing products, pricing, stock, and other entity types
    from the specified source, with options for controlling logging verbosity and
    audit tracking.
    """
    # Configure logging based on verbosity
    configure_logging(verbosity)

    try:
        # Normalize source type
        normalized_source_type = source_type.lower()
        if normalized_source_type == "file":
            normalized_source_type = "csv"

        # Load connector config
        connector_config = _load_connector_config(
            source_type=normalized_source_type,
            config_file=config_file,
            file_path=file_path,
            file_type=file_type,
        )

        # Get or create system user for audit logging
        system_user_id = resolve_system_user_id(system_user)

        # Run import for all entity types
        results = asyncio.run(
            _run_import_all(
                source_type=normalized_source_type,
                entity_types=entity_types,
                connector_config=connector_config,
                limit=limit,
                dry_run=dry_run,
                output_dir=output_dir,
                system_user_id=system_user_id,
                notify_users=notify_users,
            )
        )

        # Print results
        _print_results(results)

        # Check for overall success
        success = all(result.get("success", False) for result in results.values())
        if success:
            typer.echo("Import completed successfully for all entity types")
            sys.exit(0)
        else:
            typer.echo("Import failed for some entity types", err=True)
            sys.exit(1)
    except Exception as e:
        logger.exception(f"Error in import_all: {str(e)}")
        typer.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def configure_logging(verbosity: str) -> None:
    """
    Configure logging based on the specified verbosity level.

    Args:
        verbosity: The verbosity level (quiet, normal, verbose, debug)
    """
    import logging

    # Set root logger level
    root_logger = logging.getLogger()

    # Set specific loggers for our application
    app_logger = logging.getLogger("app")
    sqlalchemy_logger = logging.getLogger("sqlalchemy")

    # Configure based on verbosity
    if verbosity == LoggingVerbosity.QUIET:
        root_logger.setLevel(logging.ERROR)
        app_logger.setLevel(logging.WARNING)
        sqlalchemy_logger.setLevel(logging.ERROR)
    elif verbosity == LoggingVerbosity.NORMAL:
        root_logger.setLevel(logging.WARNING)
        app_logger.setLevel(logging.INFO)
        sqlalchemy_logger.setLevel(logging.WARNING)
    elif verbosity == LoggingVerbosity.VERBOSE:
        root_logger.setLevel(logging.INFO)
        app_logger.setLevel(logging.DEBUG)
        sqlalchemy_logger.setLevel(logging.INFO)
    elif verbosity == LoggingVerbosity.DEBUG:
        root_logger.setLevel(logging.DEBUG)
        app_logger.setLevel(logging.DEBUG)
        sqlalchemy_logger.setLevel(logging.DEBUG)
    else:
        # Default to normal if invalid verbosity level
        root_logger.setLevel(logging.WARNING)
        app_logger.setLevel(logging.INFO)
        sqlalchemy_logger.setLevel(logging.WARNING)

    logger.info(f"Logging level set to {verbosity}")


def resolve_system_user_id(user_id: Optional[str] = None) -> Optional[uuid.UUID]:
    """
    Resolve or create a system user ID for audit logging.

    Args:
        user_id: Optional user ID string

    Returns:
        UUID of the system user to use for audit logging
    """
    if user_id:
        try:
            return uuid.UUID(user_id)
        except ValueError:
            logger.warning(f"Invalid UUID format for system user: {user_id}")

    # Create or get default system user
    async def get_or_create_system_user():
        async with get_db_context() as db:
            # Check if system user exists
            from app.domains.users.models import User

            system_user_query = select(User).where(User.username == "system.import")
            result = await db.execute(system_user_query)
            system_user = result.scalars().first()

            if not system_user:
                # Create system user
                logger.info("Creating system user for import")
                system_user = User(
                    username="system.import",
                    email="system.import@system",
                    is_active=True,
                    is_system=True,
                    first_name="System",
                    last_name="Import",
                )
                db.add(system_user)
                await db.commit()
                await db.refresh(system_user)

            return system_user.id

    try:
        return asyncio.run(get_or_create_system_user())
    except Exception as e:
        logger.warning(f"Failed to create system user: {str(e)}")
        return None


def _load_connector_config(
    source_type: str,
    config_file: Optional[str],
    file_path: Optional[str],
    file_type: Optional[str],
) -> Dict[str, Any]:
    """
    Load connector configuration from file or environment.

    Args:
        source_type: The data source type
        config_file: Optional path to config file
        file_path: Optional path to input file
        file_type: Optional file type

    Returns:
        Dictionary of connector configuration
    """
    if config_file:
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                return config
        except Exception as e:
            raise ValueError(f"Failed to load configuration file: {str(e)}") from e

    if source_type == "filemaker":
        return get_filemaker_connector_config()
    elif source_type == "as400":
        return get_as400_connector_config()
    elif source_type == "csv":
        if not file_path:
            raise ValueError(
                "File source requires file_path. Provide it as a command line option or in a config file."
            )

        if not file_type:
            if file_path.endswith(".csv"):
                file_type = "csv"
            elif file_path.endswith(".json"):
                file_type = "json"
            else:
                raise ValueError(
                    "Could not determine file type from file extension. Provide file_type as a command line option or in a config file."
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


async def _run_import_all(
    source_type: str,
    entity_types: List[str],
    connector_config: Dict[str, Any],
    limit: Optional[int],
    dry_run: bool,
    output_dir: Optional[str],
    system_user_id: Optional[uuid.UUID],
    notify_users: bool,
) -> Dict[str, Dict[str, Any]]:
    """
    Run import for all specified entity types.

    Args:
        source_type: The data source type
        entity_types: List of entity types to import
        connector_config: Connector configuration
        limit: Optional limit on records
        dry_run: Whether to perform a dry run
        output_dir: Optional output directory for dry run
        system_user_id: System user ID for audit logging
        notify_users: Whether to send notifications

    Returns:
        Dictionary of results for each entity type
    """
    async with get_db_context() as db:
        # Create sync history entry for the overall import
        sync_repo = SyncHistoryRepository(db)
        main_sync = await sync_repo.create_sync(
            entity_type=SyncEntityType.PRODUCT,  # Main entity type
            source=SyncSource(source_type),
            triggered_by_id=system_user_id,
            details={
                "entity_types": entity_types,
                "dry_run": dry_run,
                "notify_users": notify_users,
                "start_time": datetime.now().isoformat(),
            },
        )

        # Create connector
        connector = _create_connector(source_type, connector_config)

        # Run import for each entity type
        results = {}
        overall_success = True
        total_start_time = time.time()

        for entity_type in entity_types:
            entity_start_time = time.time()
            try:
                # Map entity type to SyncEntityType
                sync_entity_type = _map_to_sync_entity_type(entity_type)

                # Create entity-specific sync history entry
                entity_sync = await sync_repo.create_sync(
                    entity_type=sync_entity_type,
                    source=SyncSource(source_type),
                    triggered_by_id=system_user_id,
                    details={
                        "parent_sync_id": str(main_sync.id),
                        "dry_run": dry_run,
                        "start_time": datetime.now().isoformat(),
                    },
                )

                # Update sync status to running
                await sync_repo.update_sync_status(
                    sync_id=entity_sync.id, status=SyncStatus.RUNNING
                )

                # Log start of entity import
                await sync_repo.add_sync_event(
                    sync_id=entity_sync.id,
                    event_type="start",
                    message=f"Starting import for {entity_type}",
                )

                # Generate query
                try:
                    query = generate_query_for_entity(entity_type, source_type)
                    logger.info(f"Generated query for {entity_type}: {query}")
                    if limit is not None:
                        if source_type in ["as400", "filemaker"]:
                            query = f"{query} FETCH FIRST {limit} ROWS ONLY"
                        else:
                            query = f"{query} LIMIT {limit}"
                except Exception as e:
                    logger.error(
                        f"Failed to generate query for {entity_type}: {str(e)}"
                    )
                    await sync_repo.update_sync_status(
                        sync_id=entity_sync.id,
                        status=SyncStatus.FAILED,
                        error_message=f"Failed to generate query: {str(e)}",
                    )
                    results[entity_type] = {
                        "success": False,
                        "message": f"Failed to generate query: {str(e)}",
                        "records_extracted": 0,
                        "records_processed": 0,
                        "records_validated": 0,
                        "records_imported": 0,
                        "total_time": time.time() - entity_start_time,
                    }
                    overall_success = False
                    continue

                # Create processor
                processor = create_processor(
                    entity_type=entity_type, source_type=source_type
                )

                # Create importer
                importer = ProductImporter(db)

                # Create pipeline
                pipeline = ProductPipeline(
                    connector=connector,
                    processor=processor,
                    importer=importer,
                    dry_run=dry_run,
                )

                # Run pipeline
                result = await pipeline.run(query, limit=limit)

                # Update sync history
                if result.get("success", False):
                    await sync_repo.update_sync_status(
                        sync_id=entity_sync.id,
                        status=SyncStatus.COMPLETED,
                        records_processed=result.get("records_processed", 0),
                        records_created=result.get("records_created", 0),
                        records_updated=result.get("records_updated", 0),
                        records_failed=result.get("records_with_errors", 0),
                        details={
                            "end_time": datetime.now().isoformat(),
                            "extract_time": result.get("extract_time", 0),
                            "process_time": result.get("process_time", 0),
                            "validate_time": result.get("validate_time", 0),
                            "import_time": result.get("import_time", 0),
                            "total_time": result.get("total_time", 0),
                        },
                    )

                    # Send notifications if requested
                    if (
                        not dry_run
                        and notify_users
                        and result.get("records_updated", 0) > 0
                    ):
                        await _send_notifications(
                            db=db,
                            entity_type=entity_type,
                            updated_count=result.get("records_updated", 0),
                            created_count=result.get("records_created", 0),
                            system_user_id=system_user_id,
                        )
                else:
                    await sync_repo.update_sync_status(
                        sync_id=entity_sync.id,
                        status=SyncStatus.FAILED,
                        records_processed=result.get("records_processed", 0),
                        records_created=result.get("records_created", 0),
                        records_updated=result.get("records_updated", 0),
                        records_failed=result.get("records_with_errors", 0),
                        error_message=result.get("message", "Unknown error"),
                        details={
                            "end_time": datetime.now().isoformat(),
                            "extract_time": result.get("extract_time", 0),
                            "process_time": result.get("process_time", 0),
                            "validate_time": result.get("validate_time", 0),
                            "import_time": result.get("import_time", 0),
                            "total_time": result.get("total_time", 0),
                        },
                    )
                    overall_success = False

                # Write processed data to output file if dry run
                if dry_run and output_dir and ("processed_data" in result):
                    import os

                    output_file = os.path.join(output_dir, f"{entity_type}_data.json")
                    try:
                        os.makedirs(output_dir, exist_ok=True)
                        with open(output_file, "w") as f:
                            json.dump(result["processed_data"], f, indent=2)
                        logger.info(f"Processed data written to {output_file}")
                    except Exception as e:
                        logger.error(f"Failed to write output file: {str(e)}")

                # Store result
                results[entity_type] = result

            except Exception as e:
                logger.exception(f"Error importing {entity_type}: {str(e)}")
                await sync_repo.update_sync_status(
                    sync_id=entity_sync.id,
                    status=SyncStatus.FAILED,
                    error_message=str(e),
                    details={
                        "end_time": datetime.now().isoformat(),
                        "total_time": time.time() - entity_start_time,
                    },
                )
                results[entity_type] = {
                    "success": False,
                    "message": f"Import failed: {str(e)}",
                    "records_extracted": 0,
                    "records_processed": 0,
                    "records_validated": 0,
                    "records_imported": 0,
                    "total_time": time.time() - entity_start_time,
                }
                overall_success = False

        # Update main sync history
        total_time = time.time() - total_start_time

        # Calculate aggregated stats
        total_extracted = sum(r.get("records_extracted", 0) for r in results.values())
        total_processed = sum(r.get("records_processed", 0) for r in results.values())
        total_validated = sum(r.get("records_validated", 0) for r in results.values())
        total_created = sum(r.get("records_created", 0) for r in results.values())
        total_updated = sum(r.get("records_updated", 0) for r in results.values())
        total_failed = sum(r.get("records_with_errors", 0) for r in results.values())

        if overall_success:
            await sync_repo.update_sync_status(
                sync_id=main_sync.id,
                status=SyncStatus.COMPLETED,
                records_processed=total_processed,
                records_created=total_created,
                records_updated=total_updated,
                records_failed=total_failed,
                details={
                    "results": {
                        k: {
                            "success": v.get("success", False),
                            "records_extracted": v.get("records_extracted", 0),
                            "records_processed": v.get("records_processed", 0),
                            "records_validated": v.get("records_validated", 0),
                            "records_created": v.get("records_created", 0),
                            "records_updated": v.get("records_updated", 0),
                            "records_failed": v.get("records_with_errors", 0),
                        }
                        for k, v in results.items()
                    },
                    "end_time": datetime.now().isoformat(),
                    "total_time": total_time,
                },
            )
        else:
            await sync_repo.update_sync_status(
                sync_id=main_sync.id,
                status=SyncStatus.FAILED,
                records_processed=total_processed,
                records_created=total_created,
                records_updated=total_updated,
                records_failed=total_failed,
                details={
                    "results": {
                        k: {
                            "success": v.get("success", False),
                            "records_extracted": v.get("records_extracted", 0),
                            "records_processed": v.get("records_processed", 0),
                            "records_validated": v.get("records_validated", 0),
                            "records_created": v.get("records_created", 0),
                            "records_updated": v.get("records_updated", 0),
                            "records_failed": v.get("records_with_errors", 0),
                        }
                        for k, v in results.items()
                    },
                    "end_time": datetime.now().isoformat(),
                    "total_time": total_time,
                },
            )

        # Add a final event
        await sync_repo.add_sync_event(
            sync_id=main_sync.id,
            event_type="complete",
            message=f"Import {'completed successfully' if overall_success else 'failed'} for {len(entity_types)} entity types",
            details={
                "total_time": total_time,
                "total_extracted": total_extracted,
                "total_processed": total_processed,
                "total_validated": total_validated,
                "total_created": total_created,
                "total_updated": total_updated,
                "total_failed": total_failed,
            },
        )

        return results


def _create_connector(
    source_type: str, config: Dict[str, Any]
) -> Union[FileConnector, FileMakerConnector, AS400Connector]:
    """
    Create a connector instance based on source type.

    Args:
        source_type: The data source type
        config: Connector configuration

    Returns:
        Connector instance
    """
    if source_type == "filemaker":
        if "password" in config and hasattr(config["password"], "get_secret_value"):
            config_copy = config.copy()
            config_copy["password"] = config["password"].get_secret_value()
            return FileMakerConnector(FileMakerConnectionConfig(**config_copy))
        return FileMakerConnector(FileMakerConnectionConfig(**config))
    elif source_type == "as400":
        if "password" in config and hasattr(config["password"], "get_secret_value"):
            config_copy = config.copy()
            config_copy["password"] = config["password"].get_secret_value()
            return AS400Connector(AS400ConnectionConfig(**config_copy))
        return AS400Connector(AS400ConnectionConfig(**config))
    elif source_type == "csv":
        return FileConnector(FileConnectionConfig(**config))
    else:
        raise ValueError(f"Unsupported source type: {source_type}")


def _map_to_sync_entity_type(entity_type: str) -> SyncEntityType:
    """
    Map entity type string to SyncEntityType enum.

    Args:
        entity_type: Entity type string

    Returns:
        SyncEntityType enum value
    """
    if entity_type == "product":
        return SyncEntityType.PRODUCT
    elif entity_type == "pricing" or entity_type == "product_pricing":
        return SyncEntityType.PRICING
    elif entity_type == "stock" or entity_type == "product_stock":
        return SyncEntityType.STOCK
    elif entity_type == "measurement" or entity_type == "product_measurement":
        return SyncEntityType.MEASUREMENT
    elif entity_type == "manufacturer":
        return SyncEntityType.MANUFACTURER
    elif entity_type == "customer":
        return SyncEntityType.CUSTOMER
    elif entity_type == "order":
        return SyncEntityType.ORDER
    else:
        # Default to product if unknown
        logger.warning(f"Unknown entity type: {entity_type}, defaulting to PRODUCT")
        return SyncEntityType.PRODUCT


async def _send_notifications(
    db: Any,
    entity_type: str,
    updated_count: int,
    created_count: int,
    system_user_id: Optional[uuid.UUID],
) -> None:
    """
    Send notifications for updated products.

    Args:
        db: Database session
        entity_type: Entity type
        updated_count: Number of updated records
        created_count: Number of created records
        system_user_id: System user ID
    """
    try:
        # TODO: Get notification service
        # # Import notification service
        # from app.core.notification.service import get_notification_service
        #
        # # Create notification
        # notification_service = get_notification_service(db)

        # Build message
        message = f"Data import complete: {entity_type} - "
        if updated_count > 0:
            message += f"{updated_count} records updated"
        if created_count > 0:
            message += (
                f"{', ' if updated_count > 0 else ''}{created_count} records created"
            )

        # TODO: Send notification to users with proper permissions
        # await notification_service.send_admin_notification(
        #     title=f"Data Import: {entity_type.capitalize()}",
        #     message=message,
        #     category="data_import",
        #     sender_id=system_user_id,
        #     data={
        #         "entity_type": entity_type,
        #         "updated_count": updated_count,
        #         "created_count": created_count,
        #         "timestamp": datetime.now().isoformat()
        #     }
        # )

        logger.info(f"Sent notification for {entity_type} import")
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")


def _print_results(results: Dict[str, Dict[str, Any]]) -> None:
    """
    Print import results to console.

    Args:
        results: Dictionary of results for each entity type
    """
    typer.echo("\nImport Results:")

    for entity_type, result in results.items():
        typer.echo(f"\n  Entity Type: {entity_type}")
        typer.echo(
            f"    Status: {('Success' if result.get('success', False) else 'Failed')}"
        )
        typer.echo(f"    Message: {result.get('message', 'No message')}")
        typer.echo(f"    Extracted: {result.get('records_extracted', 0)} records")
        typer.echo(f"    Processed: {result.get('records_processed', 0)} records")
        typer.echo(f"    Validated: {result.get('records_validated', 0)} records")
        typer.echo(f"    Imported: {result.get('records_imported', 0)} records")
        typer.echo(f"      - Created: {result.get('records_created', 0)} records")
        typer.echo(f"      - Updated: {result.get('records_updated', 0)} records")
        typer.echo(f"      - Errors: {result.get('records_with_errors', 0)} records")
        typer.echo(f"    Timing:")
        typer.echo(f"      - Extract: {result.get('extract_time', 0):.2f} seconds")
        typer.echo(f"      - Process: {result.get('process_time', 0):.2f} seconds")
        typer.echo(f"      - Validate: {result.get('validate_time', 0):.2f} seconds")
        typer.echo(f"      - Import: {result.get('import_time', 0):.2f} seconds")
        typer.echo(f"      - Total: {result.get('total_time', 0):.2f} seconds")

        if result.get("error"):
            typer.echo(f"\n    Error: {result['error']}", err=True)

    # Print overall summary
    total_extracted = sum(r.get("records_extracted", 0) for r in results.values())
    total_processed = sum(r.get("records_processed", 0) for r in results.values())
    total_validated = sum(r.get("records_validated", 0) for r in results.values())
    total_created = sum(r.get("records_created", 0) for r in results.values())
    total_updated = sum(r.get("records_updated", 0) for r in results.values())
    total_errors = sum(r.get("records_with_errors", 0) for r in results.values())

    typer.echo("\nOverall Summary:")
    typer.echo(f"  Total Extracted: {total_extracted} records")
    typer.echo(f"  Total Processed: {total_processed} records")
    typer.echo(f"  Total Validated: {total_validated} records")
    typer.echo(f"  Total Created: {total_created} records")
    typer.echo(f"  Total Updated: {total_updated} records")
    typer.echo(f"  Total Errors: {total_errors} records")

    if all(result.get("success", False) for result in results.values()):
        typer.echo("\nAll imports completed successfully!")
    else:
        typer.echo("\nSome imports failed!", err=True)


if __name__ == "__main__":
    app()
