from __future__ import annotations

"""
AS400 sync CLI commands.

This module provides CLI commands for manually running, scheduling, and monitoring
AS400 data synchronization operations.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, List, Optional
import typer

from app.core.config.integrations.as400 import as400_settings, get_as400_connector_config
from app.core.exceptions import AppException
from app.core.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
from app.services.as400_sync_service import (
    as400_sync_service, SyncEntityType, SyncStatus
)
from app.db.session import get_db_context

logger = get_logger("app.commands.sync_as400")
app = typer.Typer()


@app.command()
def sync(
    entity_type: str = typer.Option(
        "product", "--entity", "-e",
        help="Entity type to sync (product, measurement, stock, pricing)"
    ),
    force: bool = typer.Option(
        False, "--force", "-f",
        help="Force sync regardless of schedule"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-d",
        help="Extract and process data but don't import"
    ),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o",
        help="Output file for processed data (dry run only)"
    ),
) -> None:
    """
    Run AS400 data synchronization for a specific entity type.

    This command triggers the synchronization of data from AS400 to the
    application database for the specified entity type.
    """
    try:
        # Validate entity type
        try:
            entity = SyncEntityType(entity_type.lower())
        except ValueError:
            valid_types = ", ".join([e.value for e in SyncEntityType])
            typer.echo(
                f"Error: Invalid entity type '{entity_type}'. "
                f"Valid types are: {valid_types}",
                err=True
            )
            sys.exit(1)

        # Run sync
        typer.echo(f"Starting {entity.value} synchronization...")
        result = asyncio.run(_run_sync(entity, force, dry_run, output_file))

        # Display result
        _print_sync_result(result)

        # Exit with appropriate code
        if result.get("success", False):
            typer.echo("Synchronization completed successfully")
            sys.exit(0)
        else:
            typer.echo("Synchronization failed", err=True)
            sys.exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@app.command()
def schedule(
    entity_type: str = typer.Option(
        "product", "--entity", "-e",
        help="Entity type to schedule (product, measurement, stock, pricing)"
    ),
    delay: int = typer.Option(
        300, "--delay", "-d",
        help="Delay in seconds before running sync"
    ),
) -> None:
    """
    Schedule AS400 data synchronization for a specific entity type.

    This command schedules the synchronization of data from AS400 to run
    after the specified delay.
    """
    try:
        # Validate entity type
        try:
            entity = SyncEntityType(entity_type.lower())
        except ValueError:
            valid_types = ", ".join([e.value for e in SyncEntityType])
            typer.echo(
                f"Error: Invalid entity type '{entity_type}'. "
                f"Valid types are: {valid_types}",
                err=True
            )
            sys.exit(1)

        # Schedule sync
        asyncio.run(_schedule_sync(entity, delay))

        typer.echo(
            f"Scheduled {entity.value} synchronization to run in {delay} seconds"
        )
        sys.exit(0)
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@app.command()
def status(
    entity_type: Optional[str] = typer.Option(
        None, "--entity", "-e",
        help="Entity type to check (product, measurement, stock, pricing)"
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j",
        help="Output in JSON format"
    ),
) -> None:
    """
    Get the status of AS400 data synchronization.

    This command retrieves the status of all or a specific entity type's
    synchronization operations.
    """
    try:
        # Validate entity type if provided
        entity = None
        if entity_type:
            try:
                entity = SyncEntityType(entity_type.lower())
            except ValueError:
                valid_types = ", ".join([e.value for e in SyncEntityType])
                typer.echo(
                    f"Error: Invalid entity type '{entity_type}'. "
                    f"Valid types are: {valid_types}",
                    err=True
                )
                sys.exit(1)

        # Get status
        result = asyncio.run(_get_sync_status(entity))

        # Display result
        if json_output:
            typer.echo(json.dumps(result, indent=2))
        else:
            _print_sync_status(result, entity)

        sys.exit(0)
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@app.command()
def test_connection() -> None:
    """
    Test the AS400 connection.

    This command verifies that the application can connect to the AS400
    database using the configured settings.
    """
    try:
        typer.echo("Testing AS400 connection...")
        result = asyncio.run(_test_as400_connection())

        if result.get("success", False):
            typer.echo("Connection successful!")
            typer.echo(f"Connected to: {result.get('database', 'Unknown')}")
            typer.echo(f"Available tables: {', '.join(result.get('tables', []))}")
            sys.exit(0)
        else:
            typer.echo(f"Connection failed: {result.get('error', 'Unknown error')}", err=True)
            sys.exit(1)
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


async def _run_sync(
    entity: SyncEntityType,
    force: bool,
    dry_run: bool,
    output_file: Optional[str]
) -> Dict:
    """
    Run a sync operation asynchronously.

    Args:
        entity: Entity type to sync
        force: Whether to force sync
        dry_run: Whether to perform a dry run
        output_file: Output file for processed data

    Returns:
        Dictionary with sync results
    """
    # Initialize sync service
    await as400_sync_service.initialize()

    # Run sync
    result = await as400_sync_service.run_sync(entity, force)

    # Save output if dry run
    if dry_run and output_file and "processed_data" in result:
        try:
            with open(output_file, "w") as f:
                json.dump(result["processed_data"], f, indent=2)
            typer.echo(f"Processed data written to {output_file}")
        except Exception as e:
            typer.echo(f"Failed to write output file: {str(e)}", err=True)

    return result


async def _schedule_sync(entity: SyncEntityType, delay: int) -> None:
    """
    Schedule a sync operation asynchronously.

    Args:
        entity: Entity type to sync
        delay: Delay in seconds
    """
    # Initialize sync service
    await as400_sync_service.initialize()

    # Schedule sync
    await as400_sync_service.schedule_sync(entity, delay)


async def _get_sync_status(entity: Optional[SyncEntityType]) -> Dict:
    """
    Get sync status asynchronously.

    Args:
        entity: Optional entity type to get status for

    Returns:
        Dictionary with sync status
    """
    # Initialize sync service
    await as400_sync_service.initialize()

    # Get status
    return await as400_sync_service.get_sync_status(entity)


async def _test_as400_connection() -> Dict:
    """
    Test AS400 connection asynchronously.

    Returns:
        Dictionary with connection test results
    """
    try:
        # Get connector configuration
        connector_config_dict = get_as400_connector_config()
        connector_config = AS400ConnectionConfig(**connector_config_dict)
        connector = AS400Connector(connector_config)

        # Try to connect
        await connector.connect()

        # Try to list tables
        tables = []
        try:
            # This query might need adjustment for AS400
            result = await connector.extract("SELECT TABLE_NAME FROM QSYS2.SYSTABLES FETCH FIRST 10 ROWS ONLY")
            tables = [row.get("TABLE_NAME", "") for row in result]
        except Exception:
            # Try alternative approach if first fails
            try:
                result = await connector.extract("SELECT * FROM SYSTABLES FETCH FIRST 10 ROWS ONLY")
                tables = [row.get("TABLE_NAME", "") for row in result]
            except Exception:
                pass

        # Close connection
        await connector.close()

        return {
            "success": True,
            "database": connector_config.database,
            "tables": tables[:10],  # Limit to 10 tables
            "message": "Connection successful",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def _print_sync_result(result: Dict) -> None:
    """
    Print sync result in a formatted way.

    Args:
        result: Sync result dictionary
    """
    typer.echo("\nSync Result:")
    typer.echo(f"  Status: {('Success' if result.get('success', False) else 'Failed')}")
    typer.echo(f"  Message: {result.get('message', 'No message')}")
    typer.echo(f"  Entity type: {result.get('entity_type', 'Unknown')}")
    typer.echo(f"  Records processed: {result.get('records_processed', 0)}")
    typer.echo(f"  Records created: {result.get('records_created', 0)}")
    typer.echo(f"  Records updated: {result.get('records_updated', 0)}")
    typer.echo(f"  Records failed: {result.get('records_failed', 0)}")
    typer.echo(f"  Sync time: {result.get('sync_time', 0):.2f} seconds")
    typer.echo(f"  Timestamp: {result.get('sync_timestamp', 'N/A')}")

    if result.get("error"):
        typer.echo(f"\nError: {result['error']}", err=True)


def _print_sync_status(result: Dict, entity: Optional[SyncEntityType]) -> None:
    """
    Print sync status in a formatted way.

    Args:
        result: Sync status dictionary
        entity: Entity type if specific
    """
    typer.echo("\nAS400 Sync Status:")
    typer.echo(f"  Service initialized: {result.get('is_initialized', False)}")
    typer.echo(f"  Active syncs: {', '.join(result.get('active_syncs', ['None']))}")

    typer.echo("\nLast Sync Times:")
    for entity_type, time in result.get("last_sync_times", {}).items():
        typer.echo(f"  {entity_type}: {time}")

    if entity and "entity_history" in result:
        typer.echo(f"\nHistory for {entity.value}:")
        for idx, history in enumerate(result["entity_history"][:5]):  # Show only last 5
            typer.echo(f"  {idx+1}. {history['status']} at {history['started_at']}")
            typer.echo(f"     Processed: {history['records_processed']}, "
                       f"Created: {history['records_created']}, "
                       f"Updated: {history['records_updated']}, "
                       f"Failed: {history['records_failed']}")
            if history.get("error_message"):
                typer.echo(f"     Error: {history['error_message']}")

        if len(result["entity_history"]) > 5:
            typer.echo(f"  ... and {len(result['entity_history']) - 5} more")

        typer.echo(f"\n  Current status: {result.get('current_status', 'unknown')}")


if __name__ == "__main__":
    app()
