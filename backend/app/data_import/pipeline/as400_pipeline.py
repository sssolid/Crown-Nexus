from __future__ import annotations

"""
AS400 data synchronization pipeline.

This module provides a pipeline for orchestrating the data synchronization
process between AS400 and the application database.
"""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel

from app.core.exceptions import AppException
from app.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector
from app.data_import.importers.base import Importer
from app.data_import.processors.as400_processor import AS400BaseProcessor

logger = get_logger("app.data_import.pipeline.as400_pipeline")

# Type variable for schema models
T = TypeVar("T", bound=BaseModel)


class AS400Pipeline(Generic[T]):
    """
    Pipeline for synchronizing data from AS400 to the application database.

    Orchestrates the extract, transform, load (ETL) process for AS400 data.
    """

    def __init__(
        self,
        connector: AS400Connector,
        processor: AS400BaseProcessor[T],
        importer: Importer[T],
        dry_run: bool = False,
        chunk_size: int = 1000,
    ) -> None:
        """
        Initialize the AS400 pipeline.

        Args:
            connector: AS400 connector for data extraction
            processor: Processor for data transformation
            importer: Importer for loading data
            dry_run: If True, don't actually import data
            chunk_size: Number of records to process at once
        """
        self.connector = connector
        self.processor = processor
        self.importer = importer
        self.dry_run = dry_run
        self.chunk_size = chunk_size

        logger.debug(
            f"Initialized AS400Pipeline with {processor.__class__.__name__}, "
            f"dry_run={dry_run}, chunk_size={chunk_size}"
        )

    async def run(
        self, query: str, limit: Optional[int] = None, **params: Any
    ) -> Dict[str, Any]:
        """
        Run the sync pipeline.

        Args:
            query: SQL query or table name
            limit: Maximum number of records to process
            **params: Additional parameters for query

        Returns:
            Dictionary with sync results
        """
        start_time = time.time()

        try:
            # Step 1: Extract data from AS400
            logger.info(
                f"Starting data extraction with query: {query} "
                f"{f'(limited to {limit} records)' if limit else ''}"
            )

            extract_start = time.time()
            await self.connector.connect()
            raw_data = await self.connector.extract(query, limit=limit, **params)
            extract_time = time.time() - extract_start

            if not raw_data:
                logger.warning("No data extracted from AS400")
                await self.connector.close()
                return {
                    "success": True,
                    "message": "No data extracted from AS400",
                    "records_extracted": 0,
                    "records_processed": 0,
                    "records_validated": 0,
                    "records_imported": 0,
                    "extract_time": extract_time,
                    "process_time": 0,
                    "validate_time": 0,
                    "import_time": 0,
                    "total_time": time.time() - start_time,
                }

            logger.info(
                f"Extracted {len(raw_data)} records in {extract_time:.2f} seconds"
            )

            # Process data in chunks if necessary
            total_processed = 0
            total_validated = 0
            total_created = 0
            total_updated = 0
            total_errors = 0
            error_details = []

            process_start = time.time()
            validate_time = 0
            import_time = 0

            # Calculate number of chunks
            num_chunks = (len(raw_data) + self.chunk_size - 1) // self.chunk_size

            for chunk_index in range(num_chunks):
                # Get chunk of data
                start_idx = chunk_index * self.chunk_size
                end_idx = min(start_idx + self.chunk_size, len(raw_data))
                chunk = raw_data[start_idx:end_idx]

                logger.debug(
                    f"Processing chunk {chunk_index + 1}/{num_chunks} "
                    f"({len(chunk)} records)"
                )

                # Step 2: Process chunk data
                try:
                    processed_data = await self.processor.process(chunk)
                    total_processed += len(processed_data)

                    # Step 3: Validate processed data
                    validate_start = time.time()
                    validated_data = await self.processor.validate(processed_data)
                    validate_time += time.time() - validate_start
                    total_validated += len(validated_data)

                    # Step 4: Import validated data
                    if not self.dry_run and validated_data:
                        import_start = time.time()
                        import_result = await self.importer.import_data(validated_data)
                        import_time += time.time() - import_start

                        total_created += import_result.get("created", 0)
                        total_updated += import_result.get("updated", 0)
                        total_errors += import_result.get("errors", 0)

                        if (
                            "error_details" in import_result
                            and import_result["error_details"]
                        ):
                            # Adjust indices for chunk position
                            for error in import_result["error_details"]:
                                if "index" in error:
                                    error["index"] += start_idx
                            error_details.extend(import_result["error_details"])

                except Exception as e:
                    logger.error(f"Error processing chunk {chunk_index + 1}: {str(e)}")
                    error_details.append(
                        {
                            "chunk": chunk_index + 1,
                            "error": str(e),
                        }
                    )
                    total_errors += 1

            process_time = time.time() - process_start - validate_time - import_time

            # Close connection
            await self.connector.close()

            # Calculate total time
            total_time = time.time() - start_time

            # Prepare result
            if self.dry_run:
                # Dry run result
                import_result = {
                    "success": True,
                    "created": 0,
                    "updated": 0,
                    "errors": 0,
                    "total": total_validated,
                    "message": "Dry run, no data imported",
                }
            else:
                # Actual import result
                import_result = {
                    "success": total_errors == 0,
                    "created": total_created,
                    "updated": total_updated,
                    "errors": total_errors,
                    "total": total_validated,
                    "message": "Import completed",
                }

            logger.info(
                f"AS400 sync completed: "
                f"extracted={len(raw_data)}, "
                f"processed={total_processed}, "
                f"validated={total_validated}, "
                f"created={total_created}, "
                f"updated={total_updated}, "
                f"errors={total_errors}, "
                f"time={total_time:.2f}s"
            )

            return {
                "success": import_result.get("success", False),
                "message": import_result.get("message", "Import completed"),
                "records_extracted": len(raw_data),
                "records_processed": total_processed,
                "records_validated": total_validated,
                "records_imported": total_created + total_updated,
                "records_created": total_created,
                "records_updated": total_updated,
                "records_with_errors": total_errors,
                "error_details": error_details,
                "extract_time": extract_time,
                "process_time": process_time,
                "validate_time": validate_time,
                "import_time": import_time,
                "total_time": total_time,
                "dry_run": self.dry_run,
                "sync_timestamp": datetime.now().isoformat(),
            }

        except AppException as e:
            logger.error(f"Pipeline error: {str(e)}")
            try:
                await self.connector.close()
            except Exception as close_error:
                logger.error(f"Error closing connector: {str(close_error)}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error in pipeline: {str(e)}", exc_info=True)
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
                "error": str(e),
                "sync_timestamp": datetime.now().isoformat(),
            }


class ParallelAS400Pipeline(Generic[T]):
    """
    Parallel pipeline for AS400 data synchronization.

    Runs multiple pipelines concurrently for faster processing.
    """

    def __init__(
        self,
        pipelines: List[AS400Pipeline[Any]],
        max_workers: int = 4,
    ) -> None:
        """
        Initialize the parallel pipeline.

        Args:
            pipelines: List of pipelines to run
            max_workers: Maximum number of concurrent workers
        """
        self.pipelines = pipelines
        self.max_workers = max_workers
        logger.debug(
            f"Initialized ParallelAS400Pipeline with {len(pipelines)} pipelines, "
            f"max_workers={max_workers}"
        )

    async def run(self) -> Dict[str, Any]:
        """
        Run all pipelines concurrently.

        Returns:
            Dictionary with combined results
        """
        start_time = time.time()

        # Create a semaphore to limit concurrency
        semaphore = asyncio.Semaphore(self.max_workers)

        async def run_pipeline_with_semaphore(
            pipeline: AS400Pipeline[Any], query: str, **params: Any
        ) -> Dict[str, Any]:
            async with semaphore:
                return await pipeline.run(query, **params)

        # Prepare pipeline tasks
        tasks = []
        for i, pipeline in enumerate(self.pipelines):
            # Extract run parameters
            pipeline_params = getattr(pipeline, "params", {})
            query = pipeline_params.get("query", f"Pipeline{i+1}")

            # Create task
            task = asyncio.create_task(
                run_pipeline_with_semaphore(pipeline, query, **pipeline_params)
            )
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        successful_pipelines = 0
        failed_pipelines = 0
        records_extracted = 0
        records_processed = 0
        records_validated = 0
        records_created = 0
        records_updated = 0
        records_with_errors = 0
        pipeline_results = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_pipelines += 1
                logger.error(f"Pipeline {i+1} failed with exception: {str(result)}")
                pipeline_results.append(
                    {
                        "pipeline": i + 1,
                        "name": getattr(self.pipelines[i], "name", f"Pipeline{i+1}"),
                        "success": False,
                        "error": str(result),
                    }
                )
            else:
                if result.get("success", False):
                    successful_pipelines += 1
                else:
                    failed_pipelines += 1

                # Accumulate metrics
                records_extracted += result.get("records_extracted", 0)
                records_processed += result.get("records_processed", 0)
                records_validated += result.get("records_validated", 0)
                records_created += result.get("records_created", 0)
                records_updated += result.get("records_updated", 0)
                records_with_errors += result.get("records_with_errors", 0)

                pipeline_results.append(
                    {
                        "pipeline": i + 1,
                        "name": getattr(self.pipelines[i], "name", f"Pipeline{i+1}"),
                        "success": result.get("success", False),
                        "records_extracted": result.get("records_extracted", 0),
                        "records_processed": result.get("records_processed", 0),
                        "records_validated": result.get("records_validated", 0),
                        "records_created": result.get("records_created", 0),
                        "records_updated": result.get("records_updated", 0),
                        "records_with_errors": result.get("records_with_errors", 0),
                        "message": result.get("message", ""),
                    }
                )

        total_time = time.time() - start_time

        logger.info(
            f"Parallel AS400 sync completed: "
            f"{successful_pipelines} successful, "
            f"{failed_pipelines} failed, "
            f"created={records_created}, "
            f"updated={records_updated}, "
            f"errors={records_with_errors}, "
            f"time={total_time:.2f}s"
        )

        return {
            "success": failed_pipelines == 0,
            "pipelines_total": len(self.pipelines),
            "pipelines_successful": successful_pipelines,
            "pipelines_failed": failed_pipelines,
            "records_extracted": records_extracted,
            "records_processed": records_processed,
            "records_validated": records_validated,
            "records_created": records_created,
            "records_updated": records_updated,
            "records_with_errors": records_with_errors,
            "pipeline_results": pipeline_results,
            "total_time": total_time,
            "sync_timestamp": datetime.now().isoformat(),
        }
