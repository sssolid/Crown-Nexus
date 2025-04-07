from __future__ import annotations

"""Product pricing data processor.

This module provides a specialized processor for transforming AS400 product pricing data
into separate records for different pricing types (Jobber and Export).
"""

from typing import Any, Dict, List
from app.logging import get_logger
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS
from app.data_import.processors.generic_processor import GenericProcessor
from app.data_import.schemas.pricing import ProductPricingImport  # Updated import

logger = get_logger("app.data_import.processors.pricing_processor")


class PricingProcessor(GenericProcessor[ProductPricingImport]):
    """Specialized processor for product pricing data.

    This processor handles the transformation of AS400 product pricing data,
    where multiple price types (Jobber and Export) exist in a single record,
    into separate records for each price type.

    Attributes:
        source_type: The type of data source (as400, filemaker, csv)
    """

    def __init__(self, source_type: str) -> None:
        """Initialize the pricing processor.

        Args:
            source_type: The type of data source (as400, filemaker, csv)
        """
        super().__init__(
            field_definitions=ENTITY_FIELD_DEFINITIONS["product_pricing"],
            model_type=ProductPricingImport,
            source_type=source_type,
        )
        logger.debug(f"PricingProcessor initialized for {source_type} source")

    async def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process pricing data from AS400, transforming each row into multiple pricing records.

        For AS400 sources, each input row with part number, jobber price, and export price
        is transformed into two separate records - one for each price type.

        Args:
            data: List of raw data records from the source

        Returns:
            List of processed records ready for validation
        """
        # For sources other than AS400, use the standard processing
        if self.source_type != "as400":
            return await super().process(data)

        # Debug: Log the first record to see its structure
        if data and len(data) > 0:
            logger.debug(f"First record field names: {list(data[0].keys())}")
            logger.debug(f"First record content: {data[0]}")

        processed_data = []
        skipped_records = 0
        invalid_price_records = 0

        for i, record in enumerate(data):
            try:
                # Extract SPART field directly - AS400 typically returns uppercase field names
                if "SPART" in record:
                    part_number = str(record["SPART"]).strip()
                elif "part_number" in record:
                    part_number = str(record["part_number"]).strip()
                else:
                    # Log field names for debugging if part number is missing
                    if i == 0:
                        logger.warning(
                            f"Available fields in record: {list(record.keys())}"
                        )

                    skipped_records += 1
                    if i % 1000 == 0:  # Log only periodically to avoid log spam
                        logger.warning(
                            f"Record at index {i} is missing part number. Available fields: {list(record.keys())}"
                        )
                    continue

                # Skip record if part number is empty
                if not part_number:
                    skipped_records += 1
                    continue

                # Process Jobber price if available (SRET1)
                jobber_price = None
                if "SRET1" in record and record["SRET1"] is not None:
                    try:
                        # Handle string, int, float or any other type that could be converted to float
                        jobber_value = record["SRET1"]
                        if jobber_value == "" or jobber_value is None:
                            jobber_price = None
                        else:
                            jobber_price = float(jobber_value)
                            if jobber_price <= 0:  # Skip non-positive prices
                                jobber_price = None
                    except (ValueError, TypeError):
                        invalid_price_records += 1
                        if i % 1000 == 0:  # Log only periodically
                            logger.warning(
                                f'Invalid Jobber price for {part_number}: {record["SRET1"]}'
                            )

                # Process Export price if available (SRET2)
                export_price = None
                if "SRET2" in record and record["SRET2"] is not None:
                    try:
                        export_value = record["SRET2"]
                        if export_value == "" or export_value is None:
                            export_price = None
                        else:
                            export_price = float(export_value)
                            if export_price <= 0:  # Skip non-positive prices
                                export_price = None
                    except (ValueError, TypeError):
                        invalid_price_records += 1
                        if i % 1000 == 0:  # Log only periodically
                            logger.warning(
                                f'Invalid Export price for {part_number}: {record["SRET2"]}'
                            )

                # Create records for each price type if we have values
                if jobber_price is not None:
                    jobber_record = {
                        "part_number": part_number,
                        "pricing_type": "Jobber",
                        "price": jobber_price,
                        "currency": "USD",
                    }
                    processed_data.append(jobber_record)

                if export_price is not None:
                    export_record = {
                        "part_number": part_number,
                        "pricing_type": "Export",
                        "price": export_price,
                        "currency": "USD",
                    }
                    processed_data.append(export_record)

            except Exception as e:
                logger.warning(
                    f"Error processing pricing record at index {i}: {str(e)}"
                )

        logger.info(
            f"Processed {len(processed_data)} pricing records from {len(data)} input records. "
            f"Skipped {skipped_records} records with missing part numbers. "
            f"Found {invalid_price_records} records with invalid prices."
        )
        return processed_data
