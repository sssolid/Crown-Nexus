from __future__ import annotations

"""Product data processor with field alias handling.

This module provides a processor for product data that can handle
field aliases in the query results.
"""

from typing import Any, Dict, List, Optional, cast
from app.logging import get_logger
from app.domains.products.schemas import (
    ProductCreate,
    ProductDescriptionCreate,
    ProductMarketingCreate,
)
from app.data_import.field_definitions import (
    ENTITY_FIELD_DEFINITIONS,
    COMPLEX_FIELD_MAPPINGS,
    ExternalFieldInfo,
)
from app.data_import.processors.generic_processor import GenericProcessor

logger = get_logger("app.data_import.processors.product_processor")


class ProductProcessor(GenericProcessor[ProductCreate]):
    """Enhanced processor for product data with special handling for field aliases.

    This processor can handle cases where the database returns field aliases
    instead of the original field names.
    """

    def __init__(self, source_type: str) -> None:
        """Initialize the product processor.

        Args:
            source_type: The type of data source (as400, filemaker, csv)
        """
        super().__init__(
            field_definitions=ENTITY_FIELD_DEFINITIONS["product"],
            model_type=ProductCreate,
            source_type=source_type,
        )

        # Create field alias maps for complex fields
        self.description_field_map = self._create_field_alias_map("descriptions")
        self.marketing_field_map = self._create_field_alias_map("marketing")

        logger.debug(f"ProductProcessor initialized for {source_type} source")
        logger.debug(f"Description field map: {self.description_field_map}")
        logger.debug(f"Marketing field map: {self.marketing_field_map}")

    def _create_field_alias_map(self, complex_field: str) -> Dict[str, str]:
        """Create a mapping from field type to possible field names.

        This handles cases where SQL aliases might be used instead of original field names.

        Args:
            complex_field: The complex field name ('descriptions' or 'marketing')

        Returns:
            Dictionary mapping field type to possible field names
        """
        field_map = {}

        if (
            "product" in COMPLEX_FIELD_MAPPINGS
            and complex_field in COMPLEX_FIELD_MAPPINGS["product"]
        ):
            if self.source_type in COMPLEX_FIELD_MAPPINGS["product"][complex_field]:
                mappings = COMPLEX_FIELD_MAPPINGS["product"][complex_field][
                    self.source_type
                ]

                for field_type, field_info in mappings.items():
                    if isinstance(field_info, ExternalFieldInfo):
                        original_field = field_info.field_name

                        # Map both the original field name and the field type (which might be used as alias)
                        field_map[original_field] = field_type
                        field_map[field_type] = field_type

                        # Also map lowercase versions
                        field_map[original_field.lower()] = field_type
                        field_map[field_type.lower()] = field_type

        return field_map

    def _process_complex_field(
        self,
        processed_record: Dict[str, Any],
        original_record: Dict[str, Any],
        complex_field: str,
        mappings: Dict[str, Any],
    ) -> None:
        """Process a complex field type (descriptions or marketing).

        This enhanced version handles both original field names and aliases.

        Args:
            processed_record: The processed record to update
            original_record: The original source record
            complex_field: The name of the complex field ('descriptions' or 'marketing')
            mappings: Field mappings for the complex field
        """
        logger.debug(
            f"Processing complex field '{complex_field}' with {len(mappings)} mappings"
        )

        # Debug the original record fields
        field_names = list(original_record.keys())
        logger.debug(
            f"Original record has {len(field_names)} fields: {field_names[:10]}"
        )

        items = []
        field_map = (
            self.description_field_map
            if complex_field == "descriptions"
            else self.marketing_field_map
        )

        # Try to find both the original fields and aliases in the record
        for field_name in field_names:
            # Skip basic fields that aren't part of complex data
            if field_name in [
                "part_number",
                "application",
                "is_active",
                "vintage",
                "late_model",
                "soft",
                "universal",
                "last_updated",
            ]:
                continue

            # Check if this field matches any of our expected fields
            if field_name in field_map:
                field_type = field_map[field_name]
                value = original_record[field_name]

                if value and (not isinstance(value, str) or value.strip()):
                    if complex_field == "descriptions":
                        items.append(
                            ProductDescriptionCreate(
                                description_type=field_type,
                                description=str(value).strip(),
                            )
                        )
                        logger.debug(
                            f"Added description '{field_type}' from field '{field_name}'"
                        )
                    elif complex_field == "marketing":
                        items.append(
                            ProductMarketingCreate(
                                marketing_type=field_type,
                                content=str(value).strip(),
                                position=len(items) + 1,
                            )
                        )
                        logger.debug(
                            f"Added marketing '{field_type}' from field '{field_name}'"
                        )

        # Add the items to the processed record
        if items:
            processed_record[complex_field] = items
            logger.info(f"Added {len(items)} items to '{complex_field}'")
        else:
            logger.info(f"No items found for complex field '{complex_field}'")
