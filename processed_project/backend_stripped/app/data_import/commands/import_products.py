from __future__ import annotations
'\nCommand for importing products.\n\nThis module provides a CLI command for importing product data from\nFileMaker or files.\n'
import asyncio
import json
import sys
from typing import Dict, Optional
import typer
from app.logging import get_logger
from app.data_import.connectors.file_connector import FileConnector, FileConnectionConfig
from app.data_import.connectors.filemaker_connector import FileMakerConnector, FileMakerConnectionConfig
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.pipeline.product_pipeline import ProductPipeline
from app.data_import.processors.product_processor import ProductMappingConfig, ProductProcessor
from app.db.session import get_db_context
logger = get_logger('app.data_import.commands.import_products')
app = typer.Typer()
@app.command()
def import_products(source_type: str=typer.Option('filemaker', '--source', '-s', help='Source type (filemaker or file)'), config_file: str=typer.Option(None, '--config', '-c', help='Path to configuration JSON file'), query: str=typer.Option(None, '--query', '-q', help='Query or table name to extract data from'), dry_run: bool=typer.Option(False, '--dry-run', '-d', help="Dry run (extract, process, validate, but don't import)"), output_file: Optional[str]=typer.Option(None, '--output', '-o', help='Output file for processed data (dry run only)'), dsn: Optional[str]=typer.Option(None, '--dsn', help='FileMaker ODBC DSN'), username: Optional[str]=typer.Option(None, '--username', '-u', help='FileMaker username'), password: Optional[str]=typer.Option(None, '--password', '-p', help='FileMaker password'), database: Optional[str]=typer.Option(None, '--database', '-db', help='FileMaker database name (optional, may be included in DSN)'), file_path: Optional[str]=typer.Option(None, '--file', '-f', help='Path to input file (CSV or JSON)'), mapping_file: Optional[str]=typer.Option(None, '--mapping', '-m', help='Path to field mapping JSON file'), file_type: Optional[str]=typer.Option(None, '--file-type', '-ft', help='File type (csv or json)'), disable_ssl: bool=typer.Option(False, '--disable-ssl-verification', help='Disable SSL certificate verification'), limit: Optional[int]=typer.Option(None, '--limit', '-l', help='Limit the number of records to import')) -> None:
    try:
        connector_config = _load_connector_config(source_type=source_type, config_file=config_file, dsn=dsn, username=username, password=password, database=database, file_path=file_path, file_type=file_type, disable_ssl=disable_ssl)
        mapping_config = _load_mapping_config(mapping_file)
        if not query:
            if source_type == 'filemaker':
                query = 'Products'
            else:
                query = ''
        result = asyncio.run(_run_import(source_type=source_type, connector_config=connector_config, mapping_config=mapping_config, query=query, limit=limit, dry_run=dry_run, output_file=output_file))
        _print_result(result)
        if result.get('success', False):
            typer.echo('Import completed successfully')
            sys.exit(0)
        else:
            typer.echo('Import failed', err=True)
            sys.exit(1)
    except Exception as e:
        typer.echo(f'Error: {str(e)}', err=True)
        sys.exit(1)
def _load_connector_config(source_type: str, config_file: Optional[str], dsn: Optional[str], username: Optional[str], password: Optional[str], database: Optional[str], file_path: Optional[str], file_type: Optional[str], disable_ssl: bool=False) -> Dict:
    if config_file:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config
        except Exception as e:
            raise ValueError(f'Failed to load configuration file: {str(e)}') from e
    if source_type == 'filemaker':
        if not all([dsn, username, password]):
            raise ValueError('FileMaker source requires dsn, username, and password. Provide them as command line options or in a config file.')
        config = {'dsn': dsn, 'username': username, 'password': password, 'disable_ssl_verification': disable_ssl}
        if database:
            config['database'] = database
        return config
    elif source_type == 'file':
        if not file_path:
            raise ValueError('File source requires file_path. Provide it as a command line option or in a config file.')
        if not file_type:
            if file_path.endswith('.csv'):
                file_type = 'csv'
            elif file_path.endswith('.json'):
                file_type = 'json'
            else:
                raise ValueError('Could not determine file type from file extension. Provide file_type as a command line option or in a config file.')
        return {'file_path': file_path, 'file_type': file_type, 'encoding': 'utf-8', 'csv_delimiter': ',', 'csv_quotechar': '"'}
    else:
        raise ValueError(f'Unsupported source type: {source_type}')
def _load_mapping_config(mapping_file: Optional[str]) -> Dict:
    if mapping_file:
        try:
            with open(mapping_file, 'r') as f:
                config = json.load(f)
                return config
        except Exception as e:
            raise ValueError(f'Failed to load mapping file: {str(e)}') from e
    return {'part_number_field': 'PartNumber', 'application_field': 'Application', 'vintage_field': 'Vintage', 'late_model_field': 'LateModel', 'soft_field': 'Soft', 'universal_field': 'Universal', 'active_field': 'Active', 'boolean_true_values': ['yes', 'y', 'true', 't', '1', 'on'], 'boolean_false_values': ['no', 'n', 'false', 'f', '0', 'off'], 'description_fields': {'Short': 'ShortDescription', 'Long': 'Description', 'Keywords': 'Keywords'}, 'marketing_fields': {'Bullet Point': 'BulletPoints'}}
async def _run_import(source_type: str, connector_config: Dict, mapping_config: Dict, query: str, limit: Optional[int], dry_run: bool, output_file: Optional[str]) -> Dict:
    async with get_db_context() as db:
        if source_type == 'filemaker':
            connector = FileMakerConnector(FileMakerConnectionConfig(**connector_config))
        else:
            connector = FileConnector(FileConnectionConfig(**connector_config))
        processor = ProductProcessor(ProductMappingConfig(**mapping_config))
        importer = ProductImporter(db)
        pipeline = ProductPipeline(connector=connector, processor=processor, importer=importer, dry_run=dry_run)
        result = await pipeline.run(query, limit=limit)
        if dry_run and output_file and ('processed_data' in result):
            try:
                with open(output_file, 'w') as f:
                    json.dump(result['processed_data'], f, indent=2)
                typer.echo(f'Processed data written to {output_file}')
            except Exception as e:
                typer.echo(f'Failed to write output file: {str(e)}', err=True)
        return result
def _print_result(result: Dict) -> None:
    typer.echo('\nImport Result:')
    typer.echo(f"  Status: {('Success' if result.get('success', False) else 'Failed')}")
    typer.echo(f"  Message: {result.get('message', 'No message')}")
    typer.echo(f"  Extracted: {result.get('records_extracted', 0)} records")
    typer.echo(f"  Processed: {result.get('records_processed', 0)} records")
    typer.echo(f"  Validated: {result.get('records_validated', 0)} records")
    typer.echo(f"  Imported: {result.get('records_imported', 0)} records")
    typer.echo(f"    - Created: {result.get('records_created', 0)} records")
    typer.echo(f"    - Updated: {result.get('records_updated', 0)} records")
    typer.echo(f"    - Errors: {result.get('records_with_errors', 0)} records")
    typer.echo(f'  Timing:')
    typer.echo(f"    - Extract: {result.get('extract_time', 0):.2f} seconds")
    typer.echo(f"    - Process: {result.get('process_time', 0):.2f} seconds")
    typer.echo(f"    - Validate: {result.get('validate_time', 0):.2f} seconds")
    typer.echo(f"    - Import: {result.get('import_time', 0):.2f} seconds")
    typer.echo(f"    - Total: {result.get('total_time', 0):.2f} seconds")
    if result.get('dry_run', False):
        typer.echo('\nDRY RUN: No data was imported')
if __name__ == '__main__':
    app()