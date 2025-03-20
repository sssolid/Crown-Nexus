# app/data_import/pipeline/product_pipeline.py
from __future__ import annotations

"""
Product import pipeline.

This module provides a pipeline for orchestrating the product data import process,
from data extraction to transformation and loading.
"""

import time
from typing import Any, Dict, List, Optional, Union

from app.core.exceptions import AppException
from app.core.logging import get_logger
from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector
from app.data_import.connectors.filemaker_connector import FileMakerConnector
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.processors.product_processor import ProductProcessor
from app.schemas.product import ProductCreate

logger = get_logger("app.data_import.pipeline.product_pipeline")

class ProductPipeline:
    """Pipeline for product data import."""

    def __init__(
        self,
        connector: Union[Connector, FileMakerConnector, FileConnector],
        processor: ProductProcessor,
        importer: ProductImporter,
        dry_run: bool = False
    ) -> None:
        """
        Initialize the product import pipeline.

        Args:
            connector: Data source connector
            processor: Product data processor
            importer: Product data importer
            dry_run: If True, do not import data
        """
        self.connector = connector
        self.processor = processor
        self.importer = importer
        self.dry_run = dry_run
        logger.debug(f"ProductPipeline initialized (dry_run={dry_run})")

    async def run(self, query: str, limit: Optional[int] = None, **params: Any) -> Dict[str, Any]:
        """
        Run the complete product import pipeline.

        Args:
            query: Query string or identifier for the data to extract
            limit: Maximum number of records to retrieve
            params: Additional parameters for the query

        Returns:
            Dictionary with pipeline execution statistics

        Raises:
            AppException: If any stage of the pipeline fails
        """
        start_time = time.time()

        try:
            # Extract phase
            logger.info(f"Starting data extraction with query: {query} {f'(limited to {limit} records)' if limit else ''}")
            extract_start = time.time()
            await self.connector.connect()
            raw_data = await self.connector.extract(query, limit=limit, **params)
            extract_time = time.time() - extract_start

            if not raw_data:
                logger.warning("No data extracted from source")
                return {
                    "success": True,
                    "message": "No data extracted from source",
                    "records_extracted": 0,
                    "records_processed": 0,
                    "records_validated": 0,
                    "records_imported": 0,
                    "extract_time": extract_time,
                    "process_time": 0,
                    "validate_time": 0,
                    "import_time": 0,
                    "total_time": time.time() - start_time
                }

            logger.info(f"Extracted {len(raw_data)} records in {extract_time:.2f} seconds")

            # Process phase
            logger.info("Starting data processing")
            process_start = time.time()
            processed_data = await self.processor.process(raw_data)
            process_time = time.time() - process_start

            if not processed_data:
                logger.warning("No records processed")
                await self.connector.close()
                return {
                    "success": False,
                    "message": "No records processed",
                    "records_extracted": len(raw_data),
                    "records_processed": 0,
                    "records_validated": 0,
                    "records_imported": 0,
                    "extract_time": extract_time,
                    "process_time": process_time,
                    "validate_time": 0,
                    "import_time": 0,
                    "total_time": time.time() - start_time
                }

            logger.info(f"Processed {len(processed_data)} records in {process_time:.2f} seconds")

            # Validate phase
            logger.info("Starting data validation")
            validate_start = time.time()
            validated_data = await self.processor.validate(processed_data)
            validate_time = time.time() - validate_start

            if not validated_data:
                logger.warning("No records validated")
                await self.connector.close()
                return {
                    "success": False,
                    "message": "No records validated",
                    "records_extracted": len(raw_data),
                    "records_processed": len(processed_data),
                    "records_validated": 0,
                    "records_imported": 0,
                    "extract_time": extract_time,
                    "process_time": process_time,
                    "validate_time": validate_time,
                    "import_time": 0,
                    "total_time": time.time() - start_time
                }

            logger.info(f"Validated {len(validated_data)} records in {validate_time:.2f} seconds")

            # Import phase
            if self.dry_run:
                logger.info("Skipping import (dry run)")
                import_result = {
                    "success": True,
                    "created": 0,
                    "updated": 0,
                    "errors": 0,
                    "total": len(validated_data),
                    "message": "Dry run, no data imported"
                }
                import_time = 0
            else:
                logger.info("Starting data import")
                import_start = time.time()
                import_result = await self.importer.import_data(validated_data)
                import_time = time.time() - import_start
                logger.info(f"Imported data in {import_time:.2f} seconds: {import_result}")

            # Clean up
            await self.connector.close()

            # Return statistics
            total_time = time.time() - start_time

            return {
                "success": import_result.get("success", False),
                "message": import_result.get("message", "Import completed"),
                "records_extracted": len(raw_data),
                "records_processed": len(processed_data),
                "records_validated": len(validated_data),
                "records_imported": import_result.get("created", 0) + import_result.get("updated", 0),
                "records_created": import_result.get("created", 0),
                "records_updated": import_result.get("updated", 0),
                "records_with_errors": import_result.get("errors", 0),
                "error_details": import_result.get("error_details", []),
                "extract_time": extract_time,
                "process_time": process_time,
                "validate_time": validate_time,
                "import_time": import_time,
                "total_time": total_time,
                "dry_run": self.dry_run
            }

        except AppException as e:
            logger.error(f"Pipeline error: {str(e)}")
            # Clean up
            try:
                await self.connector.close()
            except Exception as close_error:
                logger.error(f"Error closing connector: {str(close_error)}")

            raise

        except Exception as e:
            logger.error(f"Unexpected error in pipeline: {str(e)}", exc_info=True)
            # Clean up
            try:
                await self.connector.close()
            except Exception as close_error:
                logger.error(f"Error closing connector: {str(close_error)}")

            total_time = time.time() - start_time

            return {
                "success": False,
                "message": f"Pipeline failed: {str(e)}",
                "records_extracted": 0,
                "records_processed": 0,
                "records_validated": 0,
                "records_imported": 0,
                "total_time": total_time,
                "error": str(e)
            }
