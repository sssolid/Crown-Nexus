# app/services/validation_service.py
from __future__ import annotations

import asyncio
import ipaddress
import re
import uuid
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Pattern, Set, Tuple, Type, Union, cast

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, ValidationError, validator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.exceptions import (
    BusinessLogicException,
    ErrorCode,
    ValidationException,
)
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.validation_service")


class ValidationService:
    """Service for data validation throughout the application.

    This service provides methods for validating different types of data,
    including integration with Pydantic models for schema validation.
    It centralizes validation logic to ensure consistency across the application.
    """

    def __init__(self) -> None:
        """Initialize the validation service."""
        self.logger = logger

        # Register common validators
        self.validators: Dict[str, Callable] = {
            "email": self.validate_email,
            "phone": self.validate_phone,
            "date": self.validate_date,
            "length": self.validate_length,
            "range": self.validate_range,
            "regex": self.validate_regex,
            "required": self.validate_required,
            "unique": self.validate_unique,
            "url": self.validate_url,
            "uuid": self.validate_uuid,
            "credit_card": self.validate_credit_card,
            "ip_address": self.validate_ip_address,
            "password": self.validate_password_strength,
            "enum": self.validate_enum,
        }

        # Common regex patterns
        self.patterns = {
            "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
            "url": re.compile(
                r"^(https?:\/\/)?"  # protocol
                r"(([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|"  # domain name
                r"((\d{1,3}\.){3}\d{1,3}))"  # OR ip (v4) address
                r"(\:\d+)?(\/[-a-z\d%_.~+]*)*"  # port and path
                r"(\?[;&a-z\d%_.~+=-]*)?"  # query string
                r"(\#[-a-z\d_]*)?$",  # fragment locator
                re.IGNORECASE,
            ),
            "phone": re.compile(r"^\+?[0-9]{10,15}$"),
            "username": re.compile(r"^[a-zA-Z0-9_-]{3,32}$"),
            "password": re.compile(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
            ),
            "credit_card": re.compile(r"^[0-9]{13,19}$"),
        }

    async def initialize(self) -> None:
        """Initialize the validation service."""
        self.logger.debug("Initializing validation service")

    async def shutdown(self) -> None:
        """Shutdown the validation service."""
        self.logger.debug("Shutting down validation service")

    def validate_data(self, data: Dict[str, Any], schema_class: Type[BaseModel]) -> BaseModel:
        """Validate data against a Pydantic schema.

        Args:
            data: The data to validate
            schema_class: The Pydantic model class to validate against

        Returns:
            A validated Pydantic model instance

        Raises:
            ValidationException: If validation fails
        """
        try:
            # Parse and validate the data using the Pydantic model
            schema = schema_class(**data)
            return schema
        except ValidationError as e:
            self.logger.warning(f"Validation error: {str(e)}")
            errors = []
            for error in e.errors():
                errors.append(
                    {"loc": list(error["loc"]), "msg": error["msg"], "type": error["type"]}
                )
            raise ValidationException(
                "Validation error",
                code=ErrorCode.VALIDATION_ERROR,
                details={"errors": errors},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

    def validate_model(
        self, model: BaseModel, include: Optional[Set[str]] = None, exclude: Optional[Set[str]] = None
    ) -> None:
        """Validate a Pydantic model instance.

        Args:
            model: The Pydantic model instance to validate
            include: Set of fields to include in validation
            exclude: Set of fields to exclude from validation

        Raises:
            ValidationException: If validation fails
        """
        try:
            # Use Pydantic's validate method with potential field filtering
            model_dict = model.dict(include=include, exclude=exclude)
            model.__class__(**model_dict)
        except ValidationError as e:
            self.logger.warning(f"Model validation error: {str(e)}")
            errors = []
            for error in e.errors():
                errors.append(
                    {"loc": list(error["loc"]), "msg": error["msg"], "type": error["type"]}
                )
            raise ValidationException(
                "Model validation error",
                code=ErrorCode.VALIDATION_ERROR,
                details={"errors": errors},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

    def validate_email(self, email: str) -> bool:
        """Validate an email address format.

        Args:
            email: The email address to validate

        Returns:
            True if the email is valid, False otherwise
        """
        if not email or len(email) > 255:
            return False
        return bool(self.patterns["email"].match(email))

    def validate_phone(self, phone: str) -> bool:
        """Validate a phone number format.

        Args:
            phone: The phone number to validate

        Returns:
            True if the phone number is valid, False otherwise
        """
        cleaned = re.sub(r"[\s\-\(\).]", "", phone)
        return bool(self.patterns["phone"].match(cleaned))

    def validate_date(
        self,
        value: Union[str, date, datetime],
        min_date: Optional[Union[str, date, datetime]] = None,
        max_date: Optional[Union[str, date, datetime]] = None,
        format_str: Optional[str] = None,
    ) -> bool:
        """Validate a date value.

        Args:
            value: The date to validate
            min_date: Optional minimum date
            max_date: Optional maximum date
            format_str: Optional date format string for parsing string dates

        Returns:
            True if the date is valid and meets constraints, False otherwise
        """
        if isinstance(value, str):
            if not format_str:
                format_str = "%Y-%m-%d"
            try:
                value = datetime.strptime(value, format_str).date()
            except ValueError:
                return False

        if isinstance(value, datetime):
            value = value.date()

        # Process min_date if provided
        if min_date and isinstance(min_date, str):
            if not format_str:
                format_str = "%Y-%m-%d"
            try:
                min_date = datetime.strptime(min_date, format_str).date()
            except ValueError:
                return False

        # Process max_date if provided
        if max_date and isinstance(max_date, str):
            if not format_str:
                format_str = "%Y-%m-%d"
            try:
                max_date = datetime.strptime(max_date, format_str).date()
            except ValueError:
                return False

        if isinstance(min_date, datetime):
            min_date = min_date.date()
        if isinstance(max_date, datetime):
            max_date = max_date.date()

        # Check constraints
        if min_date and value < min_date:
            return False
        if max_date and value > max_date:
            return False

        return True

    def validate_length(
        self, value: str, min_length: Optional[int] = None, max_length: Optional[int] = None
    ) -> bool:
        """Validate the length of a string.

        Args:
            value: The string to validate
            min_length: Optional minimum length
            max_length: Optional maximum length

        Returns:
            True if the string length meets constraints, False otherwise
        """
        if min_length is not None and len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        return True

    def validate_range(
        self,
        value: Union[int, float],
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
    ) -> bool:
        """Validate a numeric value against a range.

        Args:
            value: The number to validate
            min_value: Optional minimum value
            max_value: Optional maximum value

        Returns:
            True if the value meets range constraints, False otherwise
        """
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True

    def validate_regex(self, value: str, pattern: str) -> bool:
        """Validate a string against a regex pattern.

        Args:
            value: The string to validate
            pattern: The regex pattern to validate against

        Returns:
            True if the string matches the pattern, False otherwise
        """
        try:
            compiled_pattern = re.compile(pattern)
            return bool(compiled_pattern.match(value))
        except re.error:
            self.logger.error(f"Invalid regex pattern: {pattern}")
            return False

    def validate_required(self, value: Any) -> bool:
        """Validate that a value is not empty.

        Args:
            value: The value to validate

        Returns:
            True if the value is not empty, False otherwise
        """
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, (list, dict, set)) and not value:
            return False
        return True

    async def validate_unique(
        self, field: str, value: Any, model: Any, db: AsyncSession, exclude_id: Optional[str] = None
    ) -> bool:
        """Validate that a value is unique in the database.

        Args:
            field: The field name to check
            value: The value to check for uniqueness
            model: The SQLAlchemy model class
            db: The database session
            exclude_id: Optional ID to exclude from the check

        Returns:
            True if the value is unique, False otherwise
        """
        query = select(model).filter(getattr(model, field) == value)
        if exclude_id:
            query = query.filter(model.id != exclude_id)
        result = await db.execute(query)
        return result.first() is None

    def validate_url(self, url: str) -> bool:
        """Validate a URL format.

        Args:
            url: The URL to validate

        Returns:
            True if the URL is valid, False otherwise
        """
        if not url:
            return False
        return bool(self.patterns["url"].match(url))

    def validate_uuid(self, value: str) -> bool:
        """Validate a UUID format.

        Args:
            value: The UUID string to validate

        Returns:
            True if the UUID is valid, False otherwise
        """
        try:
            uuid_obj = uuid.UUID(value)
            return str(uuid_obj) == value
        except (ValueError, AttributeError, TypeError):
            return False

    def validate_credit_card(self, card_number: str) -> bool:
        """Validate a credit card number using the Luhn algorithm.

        Args:
            card_number: The credit card number to validate

        Returns:
            True if the credit card number is valid, False otherwise
        """
        # Remove spaces and hyphens
        card_number = card_number.replace(" ", "").replace("-", "")

        # Check if it only contains digits and has appropriate length
        if not self.patterns["credit_card"].match(card_number):
            return False

        # Luhn algorithm
        digits = [int(d) for d in card_number]
        checksum = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit

        return checksum % 10 == 0

    def validate_ip_address(self, ip: str, version: Optional[int] = None) -> bool:
        """Validate an IP address.

        Args:
            ip: The IP address to validate
            version: Optional IP version (4 or 6)

        Returns:
            True if the IP address is valid, False otherwise
        """
        try:
            ip_obj = ipaddress.ip_address(ip)
            if version == 4:
                return isinstance(ip_obj, ipaddress.IPv4Address)
            elif version == 6:
                return isinstance(ip_obj, ipaddress.IPv6Address)
            return True
        except ValueError:
            return False

    def validate_password_strength(
        self,
        password: str,
        min_length: int = 8,
        require_lowercase: bool = True,
        require_uppercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True
    ) -> bool:
        """Validate password strength.

        Args:
            password: The password to validate
            min_length: Minimum password length
            require_lowercase: Whether to require at least one lowercase letter
            require_uppercase: Whether to require at least one uppercase letter
            require_digit: Whether to require at least one digit
            require_special: Whether to require at least one special character

        Returns:
            True if the password meets strength requirements, False otherwise
        """
        if len(password) < min_length:
            return False

        if require_lowercase and not any(c.islower() for c in password):
            return False

        if require_uppercase and not any(c.isupper() for c in password):
            return False

        if require_digit and not any(c.isdigit() for c in password):
            return False

        if require_special and not any(not c.isalnum() for c in password):
            return False

        return True

    def validate_enum(self, value: Any, enum_class: Type[Enum]) -> bool:
        """Validate that a value is a valid enum member.

        Args:
            value: The value to validate
            enum_class: The Enum class to validate against

        Returns:
            True if the value is a valid enum member, False otherwise
        """
        try:
            enum_class(value)
            return True
        except (ValueError, TypeError):
            return False

    def validate_composite(self, data: Dict[str, Any], rules: Dict[str, Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
        """Validate multiple fields with different validation rules.

        Args:
            data: The data dictionary containing fields to validate
            rules: Dictionary mapping field names to validation rules

        Returns:
            Tuple of (success, errors) where success is a boolean and errors is a list of error details
        """
        errors = []

        for field, field_rules in rules.items():
            # Skip validation if field is not in data and not required
            if field not in data:
                if field_rules.get("required", False):
                    errors.append({
                        "loc": [field],
                        "msg": "Field is required",
                        "type": "value_error.missing"
                    })
                continue

            value = data[field]

            # Apply each rule
            for rule_name, rule_params in field_rules.items():
                if rule_name == "required":
                    # Already handled above
                    continue

                if rule_name in self.validators:
                    validator_func = self.validators[rule_name]

                    # Handle validator parameters
                    if isinstance(rule_params, dict):
                        # Pass parameters as kwargs
                        is_valid = validator_func(value, **rule_params)
                    else:
                        # Pass single parameter
                        is_valid = validator_func(value, rule_params)

                    if not is_valid:
                        errors.append({
                            "loc": [field],
                            "msg": f"Validation error for rule {rule_name}",
                            "type": f"value_error.{rule_name}"
                        })

        return len(errors) == 0, errors

    def create_validator(
        self,
        rule_type: str,
        **params: Any
    ) -> Callable[[Any], bool]:
        """Create a validator function based on a rule type and parameters.

        Args:
            rule_type: The type of validation rule
            **params: Parameters for the validation rule

        Returns:
            A validator function that takes a value and returns a boolean
        """
        if rule_type not in self.validators:
            raise ValueError(f"Unknown validator type: {rule_type}")

        validator_func = self.validators[rule_type]

        def validator(value: Any) -> bool:
            return validator_func(value, **params)

        return validator

    def register_validator(self, name: str, validator_func: Callable) -> None:
        """Register a custom validator function.

        Args:
            name: The name of the validator
            validator_func: The validator function
        """
        self.validators[name] = validator_func
        self.logger.debug(f"Registered custom validator: {name}")
