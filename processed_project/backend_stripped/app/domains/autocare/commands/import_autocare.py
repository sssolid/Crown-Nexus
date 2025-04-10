from __future__ import annotations
import logging
'\nCommand for importing AutoCare data into the application database.\n\nThis module provides a CLI command for importing VCdb, PCdb, PAdb, and Qdb data\nfrom various data formats into the application database.\n'
import asyncio
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, cast
import typer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_context
from app.domains.autocare.importers.flexible_importer import SourceFormat, detect_source_format
from app.domains.autocare.importers.vcdb_importer import VCdbImporter
from app.domains.autocare.importers.pcdb_importer import PCdbImporter
from app.domains.autocare.importers.padb_importer import PAdbImporter
from app.domains.autocare.importers.qdb_importer import QdbImporter
from app.domains.sync_history.models import SyncEntityType, SyncSource, SyncStatus
from app.domains.sync_history.repository import SyncHistoryRepository
from app.logging import get_logger
logger = get_logger('app.domains.autocare.commands.import_autocare')
app = typer.Typer(help='Import AutoCare standard data into the application database.')
class AutoCareDatabase(str, Enum):
    VCDB = 'vcdb'
    PCDB = 'pcdb'
    PADB = 'padb'
    QDB = 'qdb'
    ALL = 'all'
@app.command(name='import')
def import_autocare(database: AutoCareDatabase=typer.Argument(AutoCareDatabase.ALL, help='AutoCare database to import (vcdb, pcdb, padb, qdb, or all)'), source_dir: Path=typer.Option(..., '--source-dir', '-s', help='Directory containing the AutoCare data files', exists=True, file_okay=False, dir_okay=True), format: Optional[SourceFormat]=typer.Option(None, '--format', '-f', help='Format of the source data (pipe, json, etc.). Auto-detected if not specified.'), batch_size: int=typer.Option(1000, '--batch-size', '-b', help='Number of records to process in each batch'), dry_run: bool=typer.Option(False, '--dry-run', '-d', help="Validate the source data but don't import it"), track_in_history: bool=typer.Option(True, '--track-history/--no-track-history', help='Track the import in the sync history'), verbose: bool=typer.Option(False, '--verbose', '-v', help='Enable verbose output')) -> None:
    print('\n' + '=' * 80)
    print(f' AUTOCARE DATA IMPORT: {database.value.upper()} ')
    print('=' * 80)
    print(f'Source directory: {source_dir}')
    print(f'Batch size: {batch_size}')
    print(f'Dry run: {dry_run}')
    print(f'Track in history: {track_in_history}')
    print(f'Verbose: {verbose}')
    if format is None:
        source_format = detect_source_format(source_dir)
        print(f'Auto-detected source format: {source_format.value}')
    else:
        source_format = format
        print(f'Using specified source format: {source_format.value}')
    print('-' * 80)
    if not source_dir.exists():
        print(f'ERROR: Source directory does not exist: {source_dir}')
        raise typer.Exit(code=1)
    try:
        print('Starting import process...')
        db_dir = get_database_source_dir(source_dir, database)
        print(f'Using database directory: {db_dir}')
        version_file = db_dir / ('Version.json' if source_format == SourceFormat.JSON else 'Version.txt')
        if not version_file.exists():
            print(f'ERROR: Version file not found in {db_dir}')
            raise typer.Exit(code=1)
        else:
            print(f'Found version file: {version_file.name}')
        result = asyncio.run(run_import(database=database, source_dir=source_dir, source_format=source_format, batch_size=batch_size, dry_run=dry_run, track_in_history=track_in_history, verbose=verbose))
        print('Import process completed.')
    except Exception as e:
        print(f'ERROR: {str(e)}')
        import traceback
        traceback.print_exc()
        raise typer.Exit(code=1)
def display_import_result(db_name: str, result: Dict) -> None:
    import textwrap
    typer.echo(f'\n{db_name.upper()}:')
    typer.echo(f"  Status: {('Success' if result.get('success', False) else 'Failed')}")
    if 'message' in result:
        wrapped_message = textwrap.fill(result['message'], initial_indent='  Message: ', subsequent_indent='           ', width=80)
        typer.echo(wrapped_message)
    if 'version' in result:
        typer.echo(f"  Version: {result['version']}")
    if 'processed_files' in result:
        typer.echo(f"  Files processed: {result['processed_files']} of {result.get('total_files', '?')}")
    if 'items_imported' in result:
        typer.echo('\n  Items imported:')
        for file_name, count in result['items_imported'].items():
            typer.echo(f'    {file_name}: {count} records')
    if 'start_time' in result and 'end_time' in result:
        start = datetime.fromisoformat(result['start_time'])
        end = datetime.fromisoformat(result['end_time'])
        duration = (end - start).total_seconds()
        typer.echo(f'\n  Timing:')
        typer.echo(f"    Start: {start.strftime('%Y-%m-%d %H:%M:%S')}")
        typer.echo(f"    End:   {end.strftime('%Y-%m-%d %H:%M:%S')}")
        typer.echo(f'    Duration: {duration:.2f} seconds')
    if 'errors' in result and result['errors']:
        typer.echo('\n  Errors:')
        for error in result['errors']:
            wrapped_error = textwrap.fill(error, initial_indent='    - ', subsequent_indent='      ', width=80)
            typer.echo(wrapped_error)
async def run_import(database: AutoCareDatabase, source_dir: Path, source_format: SourceFormat=SourceFormat.PIPE, batch_size: int=1000, dry_run: bool=False, track_in_history: bool=True, verbose: bool=False) -> Union[Dict, Dict[str, Dict]]:
    print(f'\nPreparing to import {database.value} database(s)')
    databases_to_import = []
    if database == AutoCareDatabase.ALL:
        databases_to_import = [AutoCareDatabase.VCDB, AutoCareDatabase.PCDB, AutoCareDatabase.PADB, AutoCareDatabase.QDB]
        print(f"Will import all databases: {', '.join((db.value for db in databases_to_import))}")
    else:
        databases_to_import = [database]
        print(f'Will import single database: {database.value}')
    if len(databases_to_import) == 1:
        print(f'\nStarting import of {databases_to_import[0].value}...')
        async with get_db_context() as db:
            print(f'Database session established')
            db_type = databases_to_import[0]
            result = await import_database(db=db, database=db_type, source_dir=source_dir, source_format=source_format, batch_size=batch_size, dry_run=dry_run, track_in_history=track_in_history, verbose=verbose)
            return result
    else:
        results = {}
        for db_type in databases_to_import:
            try:
                print(f'\nStarting import of {db_type.value}...')
                async with get_db_context() as db:
                    print(f'Database session established for {db_type.value}')
                    result = await import_database(db=db, database=db_type, source_dir=source_dir, source_format=source_format, batch_size=batch_size, dry_run=dry_run, track_in_history=track_in_history, verbose=verbose)
                    results[db_type.value] = result
                    print(f"Import of {db_type.value} completed with status: {('SUCCESS' if result.get('success', False) else 'FAILED')}")
            except Exception as e:
                print(f'ERROR during import of {db_type.value}: {str(e)}')
                logger.error(f'Error importing {db_type.value}: {str(e)}')
                results[db_type.value] = {'success': False, 'message': f'Import failed: {str(e)}', 'errors': [str(e)]}
        return results
async def import_database(db: AsyncSession, database: AutoCareDatabase, source_dir: Path, source_format: SourceFormat=SourceFormat.PIPE, batch_size: int=1000, dry_run: bool=False, track_in_history: bool=True, verbose: bool=False) -> Dict:
    print(f'\nImporting {database.value} from {source_dir}')
    print(f'Format: {source_format.value}')
    print(f'Options: batch_size={batch_size}, dry_run={dry_run}, track_in_history={track_in_history}')
    if not verbose:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    else:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    sync_record = None
    sync_repo = None
    if track_in_history:
        try:
            print('Creating sync history record...')
            sync_repo = SyncHistoryRepository(db)
            sync_record = await sync_repo.create_sync(entity_type=SyncEntityType.AUTOCARE, source=SyncSource.FILE, details={'database': database.value, 'source_dir': str(source_dir), 'source_format': source_format.value, 'batch_size': batch_size, 'dry_run': dry_run, 'start_time': datetime.now().isoformat()})
            await sync_repo.update_sync_status(sync_id=sync_record.id, status=SyncStatus.RUNNING)
            print(f'Sync history record created with ID: {sync_record.id}')
        except Exception as e:
            print(f'WARNING: Failed to create sync history record: {str(e)}')
    try:
        db_source_dir = get_database_source_dir(source_dir, database)
        print(f'Using database directory: {db_source_dir}')
        if database == AutoCareDatabase.VCDB:
            print('Creating VCdb importer...')
            importer = VCdbImporter(db=db, source_path=db_source_dir, source_format=source_format, batch_size=batch_size)
        elif database == AutoCareDatabase.PCDB:
            print('Creating PCdb importer...')
            importer = PCdbImporter(db=db, source_path=db_source_dir, source_format=source_format, batch_size=batch_size)
        elif database == AutoCareDatabase.PADB:
            print('Creating PAdb importer...')
            importer = PAdbImporter(db=db, source_path=db_source_dir, source_format=source_format, batch_size=batch_size)
        elif database == AutoCareDatabase.QDB:
            print('Creating Qdb importer...')
            importer = QdbImporter(db=db, source_path=db_source_dir, source_format=source_format, batch_size=batch_size)
        else:
            raise ValueError(f'Unsupported database type: {database}')
        print(f'\nValidating source data for {database.value}...')
        is_valid = await importer.validate_source()
        if not is_valid:
            error_msg = f'Source validation failed for {database.value}'
            print(f'\nERROR: {error_msg}')
            logger.error(error_msg)
            if track_in_history and sync_repo and sync_record:
                print('Updating sync history record with failure status...')
                await sync_repo.update_sync_status(sync_id=sync_record.id, status=SyncStatus.FAILED, error_message=error_msg)
            return {'success': False, 'message': error_msg, 'errors': ['Source validation failed. See logs for details.']}
        print(f'\nSource validation successful for {database.value}')
        if dry_run:
            print(f'DRY RUN: {database.value} validation passed, skipping actual import')
            if track_in_history and sync_repo and sync_record:
                print('Updating sync history record with success status...')
                await sync_repo.update_sync_status(sync_id=sync_record.id, status=SyncStatus.COMPLETED, details={'dry_run': True, 'end_time': datetime.now().isoformat()})
            return {'success': True, 'message': f'Dry run: {database.value} source validation passed', 'dry_run': True}
        print(f'\nStarting actual import for {database.value}...')
        start_time = time.time()
        result = await importer.import_data()
        end_time = time.time()
        total_records = sum(result.get('items_imported', {}).values())
        duration = end_time - start_time
        print(f'\nImport completed in {duration:.2f} seconds')
        print(f'Total records imported: {total_records}')
        print(f"Success: {result.get('success', False)}")
        if track_in_history and sync_repo and sync_record:
            print('Updating sync history record with final status...')
            if result.get('success', False):
                await sync_repo.update_sync_status(sync_id=sync_record.id, status=SyncStatus.COMPLETED, records_processed=total_records, details={'end_time': datetime.now().isoformat(), 'duration': duration, 'version': result.get('version')})
            else:
                await sync_repo.update_sync_status(sync_id=sync_record.id, status=SyncStatus.FAILED, records_processed=total_records, error_message=result.get('message', 'Unknown error'), details={'end_time': datetime.now().isoformat(), 'duration': duration, 'errors': result.get('errors', [])})
        return result
    except Exception as e:
        print(f'\nERROR importing {database.value}: {str(e)}')
        import traceback
        traceback.print_exc()
        logger.exception(f'Error importing {database.value}: {str(e)}')
        if track_in_history and sync_repo and sync_record:
            print('Updating sync history record with error status...')
            await sync_repo.update_sync_status(sync_id=sync_record.id, status=SyncStatus.FAILED, error_message=str(e), details={'end_time': datetime.now().isoformat()})
        return {'success': False, 'message': f'Import failed: {str(e)}', 'errors': [str(e)]}
def get_database_source_dir(source_dir: Path, database: AutoCareDatabase) -> Path:
    if (source_dir / 'Version.txt').exists() or (source_dir / 'Version.json').exists():
        return source_dir
    patterns = {AutoCareDatabase.VCDB: ['*VCdb*', '*VCDB*', 'vcdb'], AutoCareDatabase.PCDB: ['*PCdb*', '*PCDB*', 'pcdb'], AutoCareDatabase.PADB: ['*PAdb*', '*PADB*', 'padb'], AutoCareDatabase.QDB: ['*Qdb*', '*QDB*', 'qdb']}
    for pattern in patterns[database]:
        matches = list(source_dir.glob(pattern))
        if matches:
            for match in matches:
                if match.is_dir() and ((match / 'Version.txt').exists() or (match / 'Version.json').exists()):
                    return match
    return source_dir
if __name__ == '__main__':
    app()