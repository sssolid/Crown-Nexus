from __future__ import annotations

"""Product import pipeline.

This module provides a pipeline for orchestrating the product data import process,
from data extraction to transformation and loading.
"""

import time
from typing import Any, Dict, Optional, Union, Type

from app.core.exceptions import AppException
from app.logging import get_logger
from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector
from app.data_import.connectors.filemaker_connector import FileMakerConnector
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.processors.product_processor import ProductProcessor
from app.data_import.schemas.pricing import ProductPricingImport

logger = get_logger('app.data_import.pipeline.product_pipeline')


class ProductPipeline:
    """Pipeline for orchestrating the product data import process.

    This pipeline handles the extract, transform, and load process for product data,
    supporting different data sources and product-related entity types.

    Attributes:
        connector: Data source connector
        processor: Data processor
        importer: Data importer
        dry_run: Whether to skip the import phase
    """

    def __init__(
        self,
        connector: Union[Connector, FileMakerConnector, FileConnector],
        processor: ProductProcessor,
        importer: ProductImporter,
        dry_run: bool = False
    ) -> None:
        """Initialize the product pipeline.

        Args:
            connector: Data source connector
            processor: Data processor
            importer: Data importer
            dry_run: Whether to skip the import phase
        """
        self.connector = connector
        self.processor = processor
        self.importer = importer
        self.dry_run = dry_run
        logger.debug(f'ProductPipeline initialized (dry_run={dry_run})')

    async def run(self, query: str, limit: Optional[int] = None, **params: Any) -> Dict[str, Any]:
        """Run the import pipeline.

        This method orchestrates the extract, transform, and load process for product data.

        Args:
            query: Query to extract data
            limit: Optional limit on the number of records to extract
            **params: Additional parameters for the query

        Returns:
            Dictionary with import statistics
        """
        start_time = time.time()
        try:
            logger.info(
                f"Starting data extraction with query: {query} {(f'(limited to {limit} records)' if limit else '')}")
            extract_start = time.time()
            await self.connector.connect()
            raw_data = await self.connector.extract(query, limit=limit, **params)
            extract_time = time.time() - extract_start

            if not raw_data:
                logger.warning('No data extracted from source')
                return {
                    'success': True,
                    'message': 'No data extracted from source',
                    'records_extracted': 0,
                    'records_processed': 0,
                    'records_validated': 0,
                    'records_imported': 0,
                    'extract_time': extract_time,
                    'process_time': 0,
                    'validate_time': 0,
                    'import_time': 0,
                    'total_time': time.time() - start_time
                }

            logger.info(f'Extracted {len(raw_data)} records in {extract_time:.2f} seconds')
            logger.info('Starting data processing')
            process_start = time.time()
            processed_data = await self.processor.process(raw_data)
            process_time = time.time() - process_start

            if not processed_data:
                logger.warning('No records processed')
                await self.connector.close()
                return {
                    'success': False,
                    'message': 'No records processed',
                    'records_extracted': len(raw_data),
                    'records_processed': 0,
                    'records_validated': 0,
                    'records_imported': 0,
                    'extract_time': extract_time,
                    'process_time': process_time,
                    'validate_time': 0,
                    'import_time': 0,
                    'total_time': time.time() - start_time
                }

            logger.info(f'Processed {len(processed_data)} records in {process_time:.2f} seconds')
            logger.info('Starting data validation')
            validate_start = time.time()
            validated_data = await self.processor.validate(processed_data)
            validate_time = time.time() - validate_start

            if not validated_data:
                logger.warning('No records validated')
                await self.connector.close()
                return {
                    'success': False,
                    'message': 'No records validated',
                    'records_extracted': len(raw_data),
                    'records_processed': len(processed_data),
                    'records_validated': 0,
                    'records_imported': 0,
                    'extract_time': extract_time,
                    'process_time': process_time,
                    'validate_time': validate_time,
                    'import_time': 0,
                    'total_time': time.time() - start_time
                }

            logger.info(f'Validated {len(validated_data)} records in {validate_time:.2f} seconds')

            if self.dry_run:
                logger.info('Skipping import (dry run)')
                import_result = {
                    'success': True,
                    'created': 0,
                    'updated': 0,
                    'errors': 0,
                    'total': len(validated_data),
                    'message': 'Dry run, no data imported'
                }
                import_time = 0
            else:
                logger.info('Starting data import')
                import_start = time.time()

                # Check if we're dealing with pricing data
                is_pricing_data = False
                if validated_data and len(validated_data) > 0:
                    is_pricing_data = isinstance(validated_data[0], ProductPricingImport)

                if is_pricing_data:
                    # Import pricing data using the specialized importer
                    logger.info('Using specialized pricing importer')
                    from app.data_import.importers.product_pricing_importer import ProductPricingImporter
                    pricing_importer = ProductPricingImporter(self.importer.db)
                    import_result = await pricing_importer.import_data(validated_data)
                else:
                    # Use the standard product importer
                    import_result = await self.importer.import_data(validated_data)

                import_time = time.time() - import_start
                logger.info(f'Imported data in {import_time:.2f} seconds: {import_result}')

            await self.connector.close()
            total_time = time.time() - start_time

            return {
                'success': import_result.get('success', False),
                'message': import_result.get('message', 'Import completed'),
                'records_extracted': len(raw_data),
                'records_processed': len(processed_data),
                'records_validated': len(validated_data),
                'records_imported': import_result.get('created', 0) + import_result.get('updated', 0),
                'records_created': import_result.get('created', 0),
                'records_updated': import_result.get('updated', 0),
                'records_with_errors': import_result.get('errors', 0),
                'error_details': import_result.get('error_details', []),
                'extract_time': extract_time,
                'process_time': process_time,
                'validate_time': validate_time,
                'import_time': import_time,
                'total_time': total_time,
                'dry_run': self.dry_run,
                'processed_data': processed_data if self.dry_run else None
            }

        except AppException as e:
            logger.error(f'Pipeline error: {str(e)}')
            try:
                await self.connector.close()
            except Exception as close_error:
                logger.error(f'Error closing connector: {str(close_error)}')
            raise

        except Exception as e:
            logger.error(f'Unexpected error in pipeline: {str(e)}', exc_info=True)
            try:
                await self.connector.close()
            except Exception as close_error:
                logger.error(f'Error closing connector: {str(close_error)}')

            total_time = time.time() - start_time
            return {
                'success': False,
                'message': f'Pipeline failed: {str(e)}',
                'records_extracted': 0,
                'records_processed': 0,
                'records_validated': 0,
                'records_imported': 0,
                'total_time': total_time,
                'error': str(e)
            }
