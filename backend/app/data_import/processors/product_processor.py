# backend/app/data_import/processors/product_processor.py
from __future__ import annotations

"""
Product data processor using field definitions.

This module provides a processor for transforming and validating product data
using centralized field definitions.
"""

from typing import Any, Dict, List, Optional

from app.logging import get_logger
from app.domains.products.schemas import ProductCreate
from app.data_import.field_definitions import (
    ENTITY_FIELD_DEFINITIONS,
    COMPLEX_FIELD_MAPPINGS, ExternalFieldInfo,
)
from app.data_import.processors.generic_processor import GenericProcessor

logger = get_logger("app.data_import.processors.product_processor_v2")


class ProductProcessor(GenericProcessor[ProductCreate]):
    """
    Processor for product data using field definitions.

    Uses the central source of truth for field mappings and transformations.
    """

    def __init__(self, source_type: str) -> None:
        """
        Initialize the product processor.

        Args:
            source_type: Source type identifier (e.g., 'filemaker', 'as400', 'csv')
        """
        super().__init__(
            field_definitions=ENTITY_FIELD_DEFINITIONS["product"],
            model_type=ProductCreate,
            source_type=source_type,
        )

        logger.debug(f"ProductProcessorV2 initialized for {source_type} source")

    def _process_complex_field(
        self,
        processed_record: Dict[str, Any],
        original_record: Dict[str, Any],
        complex_field: str,
        mappings: Dict[str, ExternalFieldInfo],
    ) -> None:
        """
        Process a specific complex field using its mappings.

        Customized for product entity to handle descriptions and marketing content.

        Args:
            processed_record: Record being processed
            original_record: Original record
            complex_field: Name of the complex field
            mappings: Mappings for the complex field
        """
        items = []

        # Normalize field names
        resolved_mappings: Dict[str, str] = {}
        for key, val in mappings.items():
            if isinstance(val, str):
                resolved_mappings[key] = val
            elif isinstance(val, ExternalFieldInfo):
                resolved_mappings[key] = val.field_name
            else:
                logger.warning(f"Invalid field mapping for complex field '{complex_field}': {val}")

        if complex_field == "descriptions":
            for desc_type, field_name in resolved_mappings.items():  # ✅ use resolved mappings
                if field_name in original_record and original_record[field_name]:
                    items.append({
                        "description_type": desc_type,
                        "description": str(original_record[field_name]),
                    })

        elif complex_field == "marketing":
            for marketing_type, field_name in resolved_mappings.items():  # ✅ use resolved mappings
                if field_name in original_record and original_record[field_name]:
                    items.append({
                        "marketing_type": marketing_type,
                        "content": str(original_record[field_name]),
                        "position": None,
                    })

        if items:
            processed_record[complex_field] = items
