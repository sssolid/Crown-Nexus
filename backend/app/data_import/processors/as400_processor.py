from __future__ import annotations

"""
AS400 data processor.

This module provides base and specific processors for transforming data from
AS400 databases into the format required by the application.
"""

import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Set, Type, TypeVar, Union

from pydantic import BaseModel

from app.core.exceptions import ValidationException
from app.core.logging import get_logger

logger = get_logger("app.data_import.processors.as400_processor")

# Type variable for the schema model
T = TypeVar("T", bound=BaseModel)


class AS400ProcessorConfig(BaseModel):
    """Configuration for AS400 data processors."""

    field_mapping: Dict[str, str] = {}
    boolean_true_values: List[str] = ["1", "Y", "YES", "TRUE", "T"]
    boolean_false_values: List[str] = ["0", "N", "NO", "FALSE", "F"]
    default_values: Dict[str, Any] = {}
    skip_fields: List[str] = []
    required_fields: List[str] = []
    date_format: str = "%Y-%m-%d"
    time_format: str = "%H:%M:%S"
    timestamp_format: str = "%Y-%m-%d %H:%M:%S"
    unique_key_field: Optional[str] = None


class AS400BaseProcessor(Generic[T], ABC):
    """
    Base class for AS400 data processors.

    Generic base processor that transforms data from AS400 format
    to the application's data model format.
    """

    def __init__(
        self, config: AS400ProcessorConfig, destination_model: Type[T]
    ) -> None:
        """
        Initialize the processor with configuration and model.

        Args:
            config: Processing configuration
            destination_model: The Pydantic model to convert data to
        """
        self.config = config
        self.destination_model = destination_model
        self.processed_keys: Set[str] = set()

        # Create a mapping from AS400 fields to model fields
        self.field_mapping = {
            as400_field: model_field
            for model_field, as400_field in config.field_mapping.items()
        }

        logger.debug(
            f"Initialized {self.__class__.__name__} for model "
            f"{destination_model.__name__}"
        )

    async def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process raw AS400 data into application format.

        Args:
            data: List of dictionary records from AS400

        Returns:
            List of processed dictionaries ready for validation
        """
        processed_data = []
        errors = []
        self.processed_keys.clear()

        # Process each record
        for i, record in enumerate(data):
            try:
                processed_record = self._process_record(record)

                # Track processed keys for duplicate detection if needed
                if self.config.unique_key_field and processed_record.get(
                    self.config.unique_key_field
                ):
                    key = processed_record[self.config.unique_key_field]
                    if key in self.processed_keys:
                        logger.warning(f"Duplicate key: {key}")
                        errors.append(
                            {"index": i, "key": key, "error": "Duplicate key"}
                        )
                        continue
                    self.processed_keys.add(key)

                processed_data.append(processed_record)

            except Exception as e:
                logger.warning(f"Error processing record at index {i}: {str(e)}")
                errors.append({"index": i, "error": str(e), "record": record})

        # Log processing results
        if errors:
            logger.warning(
                f"Processed {len(processed_data)} records with {len(errors)} errors"
            )
        else:
            logger.info(f"Processed {len(processed_data)} records successfully")

        return processed_data

    async def validate(self, data: List[Dict[str, Any]]) -> List[T]:
        """
        Validate processed data against destination model.

        Args:
            data: List of processed dictionaries

        Returns:
            List of validated model instances

        Raises:
            ValidationException: If validation fails
        """
        validated_data = []
        validation_errors = []

        # Validate each record against the model
        for i, item in enumerate(data):
            try:
                validated_item = self.destination_model(**item)
                validated_data.append(validated_item)
            except Exception as e:
                logger.warning(f"Validation error at index {i}: {str(e)}")
                key_value = item.get(self.config.unique_key_field, f"index_{i}")
                validation_errors.append(
                    {"index": i, "key": key_value, "error": str(e)}
                )

        # Log validation results
        if validation_errors:
            logger.warning(
                f"Validated {len(validated_data)} records with "
                f"{len(validation_errors)} validation errors"
            )

            # Raise exception if all records failed validation
            if len(validation_errors) >= len(data):
                raise ValidationException(
                    message="All records failed validation", errors=validation_errors
                )
        else:
            logger.info(f"Validated {len(validated_data)} records successfully")

        return validated_data

    def _process_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single record from AS400 format.

        Args:
            record: Dictionary record from AS400

        Returns:
            Processed dictionary ready for validation

        Raises:
            ValueError: If processing fails
        """
        # Start with default values
        processed_record = self.config.default_values.copy()

        # Map fields from AS400 to the application model
        for as400_field, value in record.items():
            # Skip excluded fields
            if as400_field in self.config.skip_fields:
                continue

            # Map field name
            model_field = self.field_mapping.get(as400_field, as400_field)

            # Apply custom field processing
            processed_value = self._process_field_value(as400_field, value)
            processed_record[model_field] = processed_value

        # Apply custom record processing
        processed_record = self._process_record_custom(processed_record, record)

        # Ensure required fields are present
        for field in self.config.required_fields:
            if field not in processed_record or processed_record[field] is None:
                raise ValueError(f"Missing required field: {field}")

        return processed_record

    def _process_field_value(self, field_name: str, value: Any) -> Any:
        """
        Process a field value for specific data types.

        Args:
            field_name: Field name in the AS400 database
            value: Raw value from AS400

        Returns:
            Processed value
        """
        if value is None:
            return None

        # Handle various types based on field names or content patterns

        # Boolean fields
        if field_name.startswith(("IS_", "HAS_")) or field_name.endswith(
            ("_FLAG", "_YN", "_INDICATOR")
        ):
            return self._convert_to_boolean(value)

        # Date fields
        if field_name.endswith(("_DATE", "_DT")):
            return self._convert_to_date(value)

        # Time fields
        if field_name.endswith(("_TIME", "_TM")):
            return self._convert_to_time(value)

        # Timestamp fields
        if field_name.endswith(("_TIMESTAMP", "_TS")):
            return self._convert_to_timestamp(value)

        # Numeric fields
        if field_name.endswith(
            ("_QTY", "_AMOUNT", "_AMT", "_NUM", "_PRICE")
        ) and isinstance(value, (str, int, float)):
            return self._convert_to_numeric(value)

        # Default processing: strip strings, pass other types through
        if isinstance(value, str):
            return value.strip()

        return value

    def _convert_to_boolean(self, value: Any) -> bool:
        """
        Convert a value to a boolean.

        Args:
            value: Value to convert

        Returns:
            Boolean representation
        """
        if isinstance(value, bool):
            return value

        if value is None:
            return False

        if isinstance(value, (int, float)):
            return value != 0

        str_value = str(value).strip().upper()
        if str_value in self.config.boolean_true_values:
            return True

        if str_value in self.config.boolean_false_values:
            return False

        # Default to False for unrecognized values
        return False

    def _convert_to_date(self, value: Any) -> Optional[datetime]:
        """
        Convert a value to a date.

        Args:
            value: Value to convert

        Returns:
            Datetime object or None
        """
        if not value or value in ["0000-00-00", "00/00/0000"]:
            return None

        if isinstance(value, datetime):
            return value

        # Handle common AS400 date formats
        if isinstance(value, str):
            value = value.strip()
            try:
                return datetime.strptime(value, self.config.date_format)
            except ValueError:
                # Try alternative formats
                for fmt in ["%Y%m%d", "%m/%d/%Y", "%d/%m/%Y"]:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue

        # Could not parse
        logger.warning(f"Could not parse date value: {value}")
        return None

    def _convert_to_time(self, value: Any) -> Optional[datetime]:
        """
        Convert a value to a time.

        Args:
            value: Value to convert

        Returns:
            Datetime object or None
        """
        if not value:
            return None

        if isinstance(value, datetime):
            return value

        # Handle common AS400 time formats
        if isinstance(value, str):
            value = value.strip()
            try:
                # Parse as time only, use today's date
                time_obj = datetime.strptime(value, self.config.time_format)
                today = datetime.today()
                return datetime(
                    today.year,
                    today.month,
                    today.day,
                    time_obj.hour,
                    time_obj.minute,
                    time_obj.second,
                )
            except ValueError:
                # Try alternative formats
                for fmt in ["%H%M%S", "%I:%M:%S %p", "%H:%M"]:
                    try:
                        time_obj = datetime.strptime(value, fmt)
                        today = datetime.today()
                        return datetime(
                            today.year,
                            today.month,
                            today.day,
                            time_obj.hour,
                            time_obj.minute,
                            time_obj.second,
                        )
                    except ValueError:
                        continue

        # Could not parse
        logger.warning(f"Could not parse time value: {value}")
        return None

    def _convert_to_timestamp(self, value: Any) -> Optional[datetime]:
        """
        Convert a value to a timestamp.

        Args:
            value: Value to convert

        Returns:
            Datetime object or None
        """
        if not value:
            return None

        if isinstance(value, datetime):
            return value

        # Handle common AS400 timestamp formats
        if isinstance(value, str):
            value = value.strip()
            try:
                return datetime.strptime(value, self.config.timestamp_format)
            except ValueError:
                # Try alternative formats
                for fmt in [
                    "%Y%m%d%H%M%S",
                    "%Y-%m-%dT%H:%M:%S",
                    "%m/%d/%Y %I:%M:%S %p",
                ]:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue

        # Could not parse
        logger.warning(f"Could not parse timestamp value: {value}")
        return None

    def _convert_to_numeric(self, value: Any) -> Optional[Union[int, float]]:
        """
        Convert a value to a numeric type.

        Args:
            value: Value to convert

        Returns:
            int, float, or None
        """
        if value is None or value == "":
            return None

        if isinstance(value, (int, float)):
            return value

        # Handle string representations
        if isinstance(value, str):
            # Remove non-numeric characters except decimal point
            cleaned_value = re.sub(r"[^\d.-]", "", value)
            if not cleaned_value or cleaned_value in [".", "-", ".-", "-."]:
                return None

            try:
                # Try to convert to int first, then float
                numeric_value = float(cleaned_value)
                if numeric_value.is_integer():
                    return int(numeric_value)
                return numeric_value
            except ValueError:
                logger.warning(f"Could not convert to numeric: {value}")
                return None

        # Unhandled type
        return None

    @abstractmethod
    def _process_record_custom(
        self, processed_record: Dict[str, Any], original_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply custom processing to a record.

        This method should be implemented by subclasses to provide
        entity-specific processing logic.

        Args:
            processed_record: Already processed record
            original_record: Original record from AS400

        Returns:
            Further processed record
        """
        pass


class ProductAS400Processor(AS400BaseProcessor[T]):
    """Processor for product data from AS400."""

    def _process_record_custom(
        self, processed_record: Dict[str, Any], original_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply product-specific processing.

        Args:
            processed_record: Already processed record
            original_record: Original record from AS400

        Returns:
            Further processed record
        """
        # Generate normalized part number if not present
        if (
            "part_number" in processed_record
            and "part_number_stripped" not in processed_record
        ):
            part_number = processed_record["part_number"]
            if part_number:
                processed_record["part_number_stripped"] = self._normalize_part_number(
                    part_number
                )

        return processed_record

    def _normalize_part_number(self, part_number: str) -> str:
        """
        Normalize a part number by removing non-alphanumeric characters and converting to uppercase.

        Args:
            part_number: Part number string

        Returns:
            Normalized part number
        """
        return "".join(c for c in part_number if c.isalnum()).upper()


class PricingAS400Processor(AS400BaseProcessor[T]):
    """Processor for pricing data from AS400."""

    def _process_record_custom(
        self, processed_record: Dict[str, Any], original_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply pricing-specific processing.

        Args:
            processed_record: Already processed record
            original_record: Original record from AS400

        Returns:
            Further processed record
        """
        # Ensure price is a proper decimal
        if "price" in processed_record and processed_record["price"] is not None:
            try:
                processed_record["price"] = float(processed_record["price"])
            except (ValueError, TypeError):
                processed_record["price"] = 0.0

        # Default currency to USD if not specified
        if "currency" not in processed_record or not processed_record["currency"]:
            processed_record["currency"] = "USD"

        return processed_record


class InventoryAS400Processor(AS400BaseProcessor[T]):
    """Processor for inventory/stock data from AS400."""

    def _process_record_custom(
        self, processed_record: Dict[str, Any], original_record: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply inventory-specific processing.

        Args:
            processed_record: Already processed record
            original_record: Original record from AS400

        Returns:
            Further processed record
        """
        # Ensure quantity is an integer
        if "quantity" in processed_record:
            try:
                processed_record["quantity"] = int(float(processed_record["quantity"]))
            except (ValueError, TypeError):
                processed_record["quantity"] = 0

        # Ensure quantity is not negative
        if "quantity" in processed_record and processed_record["quantity"] < 0:
            processed_record["quantity"] = 0

        # Add last_updated timestamp if not present
        if "last_updated" not in processed_record:
            processed_record["last_updated"] = datetime.now()

        return processed_record
