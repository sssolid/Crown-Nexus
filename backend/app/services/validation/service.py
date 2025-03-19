# /app/services/validation/service.py
from __future__ import annotations

"""Main validation service implementation.

This module provides the primary ValidationService that coordinates validation
operations throughout the application.
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union, cast

from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ErrorCode, ValidationException
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
from app.services.validation.base import ValidationResult, Validator
from app.services.validation.db import UniqueValidator
from app.services.validation.factory import ValidatorFactory

logger = get_logger("app.services.validation.service")


class ValidationService(ServiceInterface):
    """Service for data validation throughout the application.

    This service provides methods for validating different types of data,
    including integration with Pydantic models for schema validation.
    It centralizes validation logic to ensure consistency across the application.
    """

    def __init__(self) -> None:
        """Initialize the validation service."""
        self.validator_factory = ValidatorFactory()
        self.logger = logger

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
                details={"errors": errors}
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
                details={"errors": errors}
            )

    def validate_email(self, email: str) -> bool:
        """Validate an email address format.

        Args:
            email: The email address to validate

        Returns:
            True if the email is valid, False otherwise
        """
        validator = self.validator_factory.create_validator("email")
        result = validator.validate(email)
        return result.is_valid

    def validate_phone(self, phone: str) -> bool:
        """Validate a phone number format.

        Args:
            phone: The phone number to validate

        Returns:
            True if the phone number is valid, False otherwise
        """
        validator = self.validator_factory.create_validator("phone")
        result = validator.validate(phone)
        return result.is_valid

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
        validator = self.validator_factory.create_validator("date")
        result = validator.validate(
            value, min_date=min_date, max_date=max_date, format_str=format_str
        )
        return result.is_valid

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
        validator = self.validator_factory.create_validator("length")
        result = validator.validate(value, min_length=min_length, max_length=max_length)
        return result.is_valid

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
        validator = self.validator_factory.create_validator("range")
        result = validator.validate(value, min_value=min_value, max_value=max_value)
        return result.is_valid

    def validate_regex(self, value: str, pattern: str) -> bool:
        """Validate a string against a regex pattern.

        Args:
            value: The string to validate
            pattern: The regex pattern to validate against

        Returns:
            True if the string matches the pattern, False otherwise
        """
        validator = self.validator_factory.create_validator("regex")
        result = validator.validate(value, pattern=pattern)
        return result.is_valid

    def validate_required(self, value: Any) -> bool:
        """Validate that a value is not empty.

        Args:
            value: The value to validate

        Returns:
            True if the value is not empty, False otherwise
        """
        validator = self.validator_factory.create_validator("required")
        result = validator.validate(value)
        return result.is_valid

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
        validator = UniqueValidator(db)
        result = await validator.validate_async(
            value, field=field, model=model, exclude_id=exclude_id
        )
        return result.is_valid

    def validate_url(self, url: str) -> bool:
        """Validate a URL format.

        Args:
            url: The URL to validate

        Returns:
            True if the URL is valid, False otherwise
        """
        validator = self.validator_factory.create_validator("url")
        result = validator.validate(url)
        return result.is_valid

    def validate_uuid(self, value: str) -> bool:
        """Validate a UUID format.

        Args:
            value: The UUID string to validate

        Returns:
            True if the UUID is valid, False otherwise
        """
        validator = self.validator_factory.create_validator("uuid")
        result = validator.validate(value)
        return result.is_valid

    def validate_credit_card(self, card_number: str) -> bool:
        """Validate a credit card number using the Luhn algorithm.

        Args:
            card_number: The credit card number to validate

        Returns:
            True if the credit card number is valid, False otherwise
        """
        validator = self.validator_factory.create_validator("credit_card")
        result = validator.validate(card_number)
        return result.is_valid

    def validate_ip_address(self, ip: str, version: Optional[int] = None) -> bool:
        """Validate an IP address.

        Args:
            ip: The IP address to validate
            version: Optional IP version (4 or 6)

        Returns:
            True if the IP address is valid, False otherwise
        """
        validator = self.validator_factory.create_validator("ip_address")
        result = validator.validate(ip, version=version)
        return result.is_valid

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
        validator = self.validator_factory.create_validator("password")
        result = validator.validate(
            password,
            min_length=min_length,
            require_lowercase=require_lowercase,
            require_uppercase=require_uppercase,
            require_digit=require_digit,
            require_special=require_special
        )
        return result.is_valid

    def validate_enum(self, value: Any, enum_class: Type[Enum]) -> bool:
        """Validate that a value is a valid enum member.

        Args:
            value: The value to validate
            enum_class: The Enum class to validate against

        Returns:
            True if the value is a valid enum member, False otherwise
        """
        validator = self.validator_factory.create_validator("enum")
        result = validator.validate(value, enum_class=enum_class)
        return result.is_valid

    def validate_composite(
        self, data: Dict[str, Any], rules: Dict[str, Dict[str, Any]]
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Validate multiple fields with different validation rules.

        Args:
            data: The data dictionary containing fields to validate
            rules: Dictionary mapping field names to validation rules

        Returns:
            Tuple of (success, errors) where success is a boolean and errors is a list of error details
        """
        all_errors: List[Dict[str, Any]] = []

        for field, field_rules in rules.items():
            # Skip validation if field is not in data and not required
            if field not in data:
                if field_rules.get("required", False):
                    all_errors.append({
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

                validator = self.validator_factory.create_validator(rule_name)

                # Handle validator parameters
                if isinstance(rule_params, dict):
                    # Pass parameters as kwargs
                    result = validator.validate(value, **rule_params)
                else:
                    # Pass single parameter (assuming it's the primary parameter for the validator)
                    result = validator.validate(value, rule_params)

                if not result.is_valid:
                    for error in result.errors:
                        error["loc"] = [field]
                        all_errors.append(error)

        return len(all_errors) == 0, all_errors

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
        validator = self.validator_factory.create_validator(rule_type)

        def validator_func(value: Any) -> bool:
            result = validator.validate(value, **params)
            return result.is_valid

        return validator_func

    def register_validator(self, name: str, validator_class: Type[Validator]) -> None:
        """Register a custom validator.

        Args:
            name: The name of the validator
            validator_class: The validator class
        """
        ValidatorFactory.register_validator(name, validator_class)
        self.logger.debug(f"Registered custom validator: {name}")

# Fix imports for methods in the class
from datetime import date, datetime
