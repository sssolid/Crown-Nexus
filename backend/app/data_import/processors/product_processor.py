# app/data_import/processors/product_processor.py
from __future__ import annotations

"""
Product data processor.

This module provides a processor for transforming and validating product data
from external sources into the application's product schema.
"""

from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Field, validator

from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.domains.products.schemas import ProductCreate

logger = get_logger("app.data_import.processors.product_processor")


class ProductMappingConfig(BaseModel):
    """Configuration for mapping source data to product schema."""

    part_number_field: str = Field(..., description="Field name for part number")
    application_field: Optional[str] = Field(
        None, description="Field name for application"
    )
    vintage_field: Optional[str] = Field(
        None, description="Field name for vintage flag"
    )
    late_model_field: Optional[str] = Field(
        None, description="Field name for late model flag"
    )
    soft_field: Optional[str] = Field(None, description="Field name for soft flag")
    universal_field: Optional[str] = Field(
        None, description="Field name for universal flag"
    )
    active_field: Optional[str] = Field(None, description="Field name for active flag")

    # Field value transformations
    boolean_true_values: List[str] = Field(
        ["yes", "y", "true", "t", "1", "on"],
        description="Values that map to True for boolean fields",
    )
    boolean_false_values: List[str] = Field(
        ["no", "n", "false", "f", "0", "off"],
        description="Values that map to False for boolean fields",
    )

    # Additional mappings for related entities
    description_fields: Optional[Dict[str, str]] = Field(
        None, description="Mapping of description type to field name"
    )
    marketing_fields: Optional[Dict[str, str]] = Field(
        None, description="Mapping of marketing type to field name"
    )

    @validator("boolean_true_values", "boolean_false_values")
    def validate_boolean_values(cls, v: List[str]) -> List[str]:
        return [str(val).lower() for val in v]


class ProductProcessor:
    """Processor for transforming raw product data into product schema."""

    def __init__(self, config: ProductMappingConfig) -> None:
        """
        Initialize the product processor.

        Args:
            config: Product mapping configuration
        """
        self.config = config
        self.processed_part_numbers: Set[str] = set()
        logger.debug("ProductProcessor initialized")

    def _transform_boolean(self, value: Any) -> bool:
        """
        Transform a value to a boolean.

        Args:
            value: Input value

        Returns:
            Boolean value
        """
        if isinstance(value, bool):
            return value

        if value is None:
            return False

        str_value = str(value).lower()

        if str_value in self.config.boolean_true_values:
            return True
        if str_value in self.config.boolean_false_values:
            return False

        # Default to False for ambiguous values
        return False

    def _clean_part_number(self, part_number: str) -> str:
        """
        Clean and standardize a part number.

        Args:
            part_number: Raw part number

        Returns:
            Cleaned part number
        """
        if not part_number:
            return ""

        # Remove extra spaces
        cleaned = part_number.strip()

        # Optionally apply other cleaning rules
        # For example, standardize format, remove invalid characters, etc.

        return cleaned

    def _generate_part_number_stripped(self, part_number: str) -> str:
        """
        Generate a stripped version of the part number (alphanumeric only).

        Args:
            part_number: Part number

        Returns:
            Stripped part number
        """
        return "".join(c for c in part_number if c.isalnum()).upper()

    def _process_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single record.

        Args:
            record: Raw record data

        Returns:
            Processed record data in product schema format

        Raises:
            ValueError: If required fields are missing
        """
        # Check for required fields
        if self.config.part_number_field not in record:
            raise ValueError(f"Missing required field: {self.config.part_number_field}")

        part_number = self._clean_part_number(
            str(record[self.config.part_number_field])
        )
        if not part_number:
            raise ValueError(f"Empty part number in record: {record}")

        # Basic product fields
        product_data = {
            "part_number": part_number,
            "part_number_stripped": self._generate_part_number_stripped(part_number),
            "application": (
                record.get(self.config.application_field, "")
                if self.config.application_field
                else ""
            ),
            "vintage": (
                self._transform_boolean(record.get(self.config.vintage_field, False))
                if self.config.vintage_field
                else False
            ),
            "late_model": (
                self._transform_boolean(record.get(self.config.late_model_field, False))
                if self.config.late_model_field
                else False
            ),
            "soft": (
                self._transform_boolean(record.get(self.config.soft_field, False))
                if self.config.soft_field
                else False
            ),
            "universal": (
                self._transform_boolean(record.get(self.config.universal_field, False))
                if self.config.universal_field
                else False
            ),
            "is_active": (
                self._transform_boolean(record.get(self.config.active_field, True))
                if self.config.active_field
                else True
            ),
        }

        # Process descriptions
        descriptions = []
        if self.config.description_fields:
            for desc_type, field_name in self.config.description_fields.items():
                if field_name in record and record[field_name]:
                    descriptions.append(
                        {
                            "description_type": desc_type,
                            "description": str(record[field_name]),
                        }
                    )

        if descriptions:
            product_data["descriptions"] = descriptions

        # Process marketing content
        marketing = []
        if self.config.marketing_fields:
            for marketing_type, field_name in self.config.marketing_fields.items():
                if field_name in record and record[field_name]:
                    marketing.append(
                        {
                            "marketing_type": marketing_type,
                            "content": str(record[field_name]),
                            "position": None,
                        }
                    )

        if marketing:
            product_data["marketing"] = marketing

        return product_data

    async def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process raw data into product schema.

        Args:
            data: List of raw data records

        Returns:
            List of processed product records

        Raises:
            ValueError: If data cannot be processed
        """
        processed_data = []
        errors = []
        self.processed_part_numbers.clear()

        for i, record in enumerate(data):
            try:
                processed_record = self._process_record(record)
                part_number = processed_record["part_number"]

                # Check for duplicates within this import
                if part_number in self.processed_part_numbers:
                    logger.warning(f"Duplicate part number: {part_number}")
                    errors.append(
                        {
                            "index": i,
                            "part_number": part_number,
                            "error": "Duplicate part number",
                        }
                    )
                    continue

                self.processed_part_numbers.add(part_number)
                processed_data.append(processed_record)

            except ValueError as e:
                logger.warning(f"Error processing record at index {i}: {str(e)}")
                errors.append({"index": i, "error": str(e), "record": record})

        if errors:
            logger.warning(
                f"Processed {len(processed_data)} records with {len(errors)} errors"
            )
        else:
            logger.info(f"Processed {len(processed_data)} records successfully")

        return processed_data

    async def validate(self, data: List[Dict[str, Any]]) -> List[ProductCreate]:
        """
        Validate processed data against the product schema.

        Args:
            data: List of processed product records

        Returns:
            List of validated product create models

        Raises:
            ValidationException: If validation fails
        """
        validated_data = []
        validation_errors = []

        for i, product_data in enumerate(data):
            try:
                # Validate with Pydantic model
                product_create = ProductCreate(**product_data)
                validated_data.append(product_create)
            except Exception as e:
                logger.warning(f"Validation error at index {i}: {str(e)}")
                validation_errors.append(
                    {
                        "index": i,
                        "part_number": product_data.get("part_number", "unknown"),
                        "error": str(e),
                    }
                )

        if validation_errors:
            logger.warning(
                f"Validated {len(validated_data)} records with {len(validation_errors)} validation errors"
            )
            if len(validation_errors) >= len(data):
                raise ValidationException(
                    message="All records failed validation", errors=validation_errors
                )
        else:
            logger.info(f"Validated {len(validated_data)} records successfully")

        return validated_data
