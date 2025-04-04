from __future__ import annotations
'\nAS400 sync CLI commands.\n\nThis module provides CLI commands for manually running, scheduling, and monitoring\nAS400 data synchronization operations.\n'
import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, Optional
import typer
from app.core.config.integrations.as400 import get_as400_connector_config
from app.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
from app.services.as400_sync_service import as400_sync_service, SyncEntityType
logger = get_logger('app.commands.sync_as400')
app = typer.Typer()
@app.command()
def sync(entity_type: str=typer.Option('product', '--entity', '-e', help='Entity type to sync (product, measurement, stock, pricing)'), force: bool=typer.Option(False, '--force', '-f', help='Force sync regardless of schedule'), dry_run: bool=typer.Option(False, '--dry-run', '-d', help="Extract and process data but don't import"), output_file: Optional[str]=typer.Option(None, '--output', '-o', help='Output file for processed data (dry run only)')) -> None:
    try:
        try:
            entity = SyncEntityType(entity_type.lower())
        except ValueError:
            valid_types = ', '.join([e.value for e in SyncEntityType])
            typer.echo(f"Error: Invalid entity type '{entity_type}'. Valid types are: {valid_types}", err=True)
            sys.exit(1)
        typer.echo(f'Starting {entity.value} synchronization...')
        result = asyncio.run(_run_sync(entity, force, dry_run, output_file))
        _print_sync_result(result)
        if result.get('success', False):
            typer.echo('Synchronization completed successfully')
            sys.exit(0)
        else:
            typer.echo('Synchronization failed', err=True)
            sys.exit(1)
    except Exception as e:
        typer.echo(f'Error: {str(e)}', err=True)
        sys.exit(1)
@app.command()
def schedule(entity_type: str=typer.Option('product', '--entity', '-e', help='Entity type to schedule (product, measurement, stock, pricing)'), delay: int=typer.Option(300, '--delay', '-d', help='Delay in seconds before running sync')) -> None:
    try:
        try:
            entity = SyncEntityType(entity_type.lower())
        except ValueError:
            valid_types = ', '.join([e.value for e in SyncEntityType])
            typer.echo(f"Error: Invalid entity type '{entity_type}'. Valid types are: {valid_types}", err=True)
            sys.exit(1)
        asyncio.run(_schedule_sync(entity, delay))
        typer.echo(f'Scheduled {entity.value} synchronization to run in {delay} seconds')
        sys.exit(0)
    except Exception as e:
        typer.echo(f'Error: {str(e)}', err=True)
        sys.exit(1)
@app.command()
def status(entity_type: Optional[str]=typer.Option(None, '--entity', '-e', help='Entity type to check (product, measurement, stock, pricing)'), json_output: bool=typer.Option(False, '--json', '-j', help='Output in JSON format')) -> None:
    try:
        entity = None
        if entity_type:
            try:
                entity = SyncEntityType(entity_type.lower())
            except ValueError:
                valid_types = ', '.join([e.value for e in SyncEntityType])
                typer.echo(f"Error: Invalid entity type '{entity_type}'. Valid types are: {valid_types}", err=True)
                sys.exit(1)
        result = asyncio.run(_get_sync_status(entity))
        if json_output:
            typer.echo(json.dumps(result, indent=2))
        else:
            _print_sync_status(result, entity)
        sys.exit(0)
    except Exception as e:
        typer.echo(f'Error: {str(e)}', err=True)
        sys.exit(1)
@app.command()
def test_connection() -> None:
    try:
        typer.echo('Testing AS400 connection...')
        result = asyncio.run(_test_as400_connection())
        if result.get('success', False):
            typer.echo('Connection successful!')
            typer.echo(f"Connected to: {result.get('database', 'Unknown')}")
            typer.echo(f"Available tables: {', '.join(result.get('tables', []))}")
            sys.exit(0)
        else:
            typer.echo(f"Connection failed: {result.get('error', 'Unknown error')}", err=True)
            sys.exit(1)
    except Exception as e:
        typer.echo(f'Error: {str(e)}', err=True)
        sys.exit(1)
async def _run_sync(entity: SyncEntityType, force: bool, dry_run: bool, output_file: Optional[str]) -> Dict:
    await as400_sync_service.initialize()
    result = await as400_sync_service.run_sync(entity, force)
    if dry_run and output_file and ('processed_data' in result):
        try:
            with open(output_file, 'w') as f:
                json.dump(result['processed_data'], f, indent=2)
            typer.echo(f'Processed data written to {output_file}')
        except Exception as e:
            typer.echo(f'Failed to write output file: {str(e)}', err=True)
    return result
async def _schedule_sync(entity: SyncEntityType, delay: int) -> None:
    await as400_sync_service.initialize()
    await as400_sync_service.schedule_sync(entity, delay)
async def _get_sync_status(entity: Optional[SyncEntityType]) -> Dict:
    await as400_sync_service.initialize()
    return await as400_sync_service.get_sync_status(entity)
async def _test_as400_connection() -> Dict:
    try:
        connector_config_dict = get_as400_connector_config()
        connector_config = AS400ConnectionConfig(**connector_config_dict)
        connector = AS400Connector(connector_config)
        await connector.connect()
        tables = []
        try:
            result = await connector.extract('SELECT TABLE_NAME FROM QSYS2.SYSTABLES FETCH FIRST 10 ROWS ONLY')
            tables = [row.get('TABLE_NAME', '') for row in result]
        except Exception:
            try:
                result = await connector.extract('SELECT * FROM SYSTABLES FETCH FIRST 10 ROWS ONLY')
                tables = [row.get('TABLE_NAME', '') for row in result]
            except Exception:
                pass
        await connector.close()
        return {'success': True, 'database': connector_config.database, 'tables': tables[:10], 'message': 'Connection successful', 'timestamp': datetime.now().isoformat()}
    except Exception as e:
        return {'success': False, 'error': str(e), 'timestamp': datetime.now().isoformat()}
def _print_sync_result(result: Dict) -> None:
    typer.echo('\nSync Result:')
    typer.echo(f"  Status: {('Success' if result.get('success', False) else 'Failed')}")
    typer.echo(f"  Message: {result.get('message', 'No message')}")
    typer.echo(f"  Entity type: {result.get('entity_type', 'Unknown')}")
    typer.echo(f"  Records processed: {result.get('records_processed', 0)}")
    typer.echo(f"  Records created: {result.get('records_created', 0)}")
    typer.echo(f"  Records updated: {result.get('records_updated', 0)}")
    typer.echo(f"  Records failed: {result.get('records_failed', 0)}")
    typer.echo(f"  Sync time: {result.get('sync_time', 0):.2f} seconds")
    typer.echo(f"  Timestamp: {result.get('sync_timestamp', 'N/A')}")
    if result.get('error'):
        typer.echo(f"\nError: {result['error']}", err=True)
def _print_sync_status(result: Dict, entity: Optional[SyncEntityType]) -> None:
    typer.echo('\nAS400 Sync Status:')
    typer.echo(f"  Service initialized: {result.get('is_initialized', False)}")
    typer.echo(f"  Active syncs: {', '.join(result.get('active_syncs', ['None']))}")
    typer.echo('\nLast Sync Times:')
    for entity_type, time in result.get('last_sync_times', {}).items():
        typer.echo(f'  {entity_type}: {time}')
    if entity and 'entity_history' in result:
        typer.echo(f'\nHistory for {entity.value}:')
        for idx, history in enumerate(result['entity_history'][:5]):
            typer.echo(f"  {idx + 1}. {history['status']} at {history['started_at']}")
            typer.echo(f"     Processed: {history['records_processed']}, Created: {history['records_created']}, Updated: {history['records_updated']}, Failed: {history['records_failed']}")
            if history.get('error_message'):
                typer.echo(f"     Error: {history['error_message']}")
        if len(result['entity_history']) > 5:
            typer.echo(f"  ... and {len(result['entity_history']) - 5} more")
        typer.echo(f"\n  Current status: {result.get('current_status', 'unknown')}")
if __name__ == '__main__':
    app()