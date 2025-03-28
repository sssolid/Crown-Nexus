from __future__ import annotations

"""Validation service implementation.

This module provides a service wrapper around the validation system,
making it available through the dependency manager.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union
from datetime import date, datetime

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.factory import ValidatorFactory
from app.core.validation.manager import (
    validate_composite,
    validate_credit_card,
    validate_data,
    validate_date,
    validate_email,
    validate_enum,
    validate_ip_address,
    validate_length,
    validate_model,
    validate_password_strength,
    validate_phone,
    validate_range,
    validate_regex,
    validate_required,
    validate_unique,
    validate_url,
    validate_uuid,
)

logger = get_logger("app.core.validation.service")


class ValidationService:
    """Service for performing validations throughout the application.

    This service provides a high-level interface to the validation system,
    with methods for validating different types of data.
    """

    def __init__(self, db: Optional[AsyncSession] = None) -> None:
        """Initialize the validation service.

        Args:
            db: Optional database session for validations requiring database access
        """
        self.db = db
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the validation service."""
        if self._initialized:
            logger.debug("Validation service already initialized")
            return

        logger.info("Initializing validation service")
        self._initialized = True

    async def shutdown(self) -> None:
        """Shutdown the validation service."""
        if not self._initialized:
            return

        logger.info("Shutting down validation service")
        self._initialized = False

    def validate_data(
        self, data: Dict[str, Any], schema_class: Type[BaseModel]
    ) -> BaseModel:
        """Validate data against a Pydantic schema.

        Args:
            data: The data to validate
            schema_class: The Pydantic model class to validate against

        Returns:
            BaseModel: The validated model instance

        Raises:
            ValidationException: If validation fails
        """
        return validate_data(data, schema_class)

    def validate_model(
        self,
        model: BaseModel,
        include: Optional[Set[str]] = None,
        exclude: Optional[Set[str]] = None,
    ) -> None:
        """Validate an existing Pydantic model instance.

        Args:
            model: The model instance to validate
            include: Optional set of fields to include in validation
            exclude: Optional set of fields to exclude from validation

        Raises:
            ValidationException: If validation fails
        """
        validate_model(model, include, exclude)

    def validate_email(self, email: str) -> bool:
        """Validate an email address.

        Args:
            email: The email address to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_email(email)

    def validate_phone(self, phone: str) -> bool:
        """Validate a phone number.

        Args:
            phone: The phone number to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_phone(phone)

    def validate_date(
        self,
        value: Union[str, date, datetime],
        min_date: Optional[Union[str, date, datetime]] = None,
        max_date: Optional[Union[str, date, datetime]] = None,
        format_str: Optional[str] = None,
    ) -> bool:
        """Validate a date value.

        Args:
            value: The date to validate (string, date, or datetime)
            min_date: Optional minimum allowed date
            max_date: Optional maximum allowed date
            format_str: Optional date format string for parsing string dates

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_date(value, min_date, max_date, format_str)

    def validate_length(
        self,
        value: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ) -> bool:
        """Validate string length.

        Args:
            value: The string to validate
            min_length: Optional minimum length
            max_length: Optional maximum length

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_length(value, min_length, max_length)

    def validate_range(
        self,
        value: Union[int, float],
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
    ) -> bool:
        """Validate numeric range.

        Args:
            value: The number to validate
            min_value: Optional minimum value
            max_value: Optional maximum value

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_range(value, min_value, max_value)

    def validate_regex(self, value: str, pattern: str) -> bool:
        """Validate string against a regex pattern.

        Args:
            value: The string to validate
            pattern: The regex pattern to validate against

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_regex(value, pattern)

    def validate_required(self, value: Any) -> bool:
        """Validate that a value is not None or empty.

        Args:
            value: The value to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_required(value)

    async def validate_unique(
        self, field: str, value: Any, model: Any, exclude_id: Optional[str] = None
    ) -> bool:
        """Validate that a field value is unique in the database.

        Args:
            field: The field name to check
            value: The field value to check
            model: The SQLAlchemy model class
            exclude_id: Optional ID to exclude from the uniqueness check

        Returns:
            bool: True if unique, False otherwise

        Raises:
            ValidationException: If no database session is available
        """
        if not self.db:
            logger.error("Database session not available for unique validation")
            raise ValidationException(
                "Validation error",
                errors=[
                    {
                        "loc": ["validator", "unique"],
                        "msg": "Database session not available for unique validation",
                        "type": "validator_error.no_db_session",
                    }
                ],
            )

        return await validate_unique(field, value, model, self.db, exclude_id)

    def validate_url(self, url: str) -> bool:
        """Validate a URL.

        Args:
            url: The URL to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_url(url)

    def validate_uuid(self, value: str) -> bool:
        """Validate a UUID string.

        Args:
            value: The UUID string to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_uuid(value)

    def validate_credit_card(self, card_number: str) -> bool:
        """Validate a credit card number.

        Args:
            card_number: The credit card number to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_credit_card(card_number)

    def validate_ip_address(self, ip: str, version: Optional[int] = None) -> bool:
        """Validate an IP address.

        Args:
            ip: The IP address to validate
            version: Optional IP version (4 or 6)

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_ip_address(ip, version)

    def validate_password_strength(
        self,
        password: str,
        min_length: int = 8,
        require_lowercase: bool = True,
        require_uppercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
    ) -> bool:
        """Validate password strength.

        Args:
            password: The password to validate
            min_length: Minimum password length
            require_lowercase: Whether to require lowercase letters
            require_uppercase: Whether to require uppercase letters
            require_digit: Whether to require digits
            require_special: Whether to require special characters

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_password_strength(
            password,
            min_length,
            require_lowercase,
            require_uppercase,
            require_digit,
            require_special,
        )

    def validate_enum(self, value: Any, enum_class: Type[Enum]) -> bool:
        """Validate that a value is a valid enum value.

        Args:
            value: The value to validate
            enum_class: The enum class to validate against

        Returns:
            bool: True if valid, False otherwise
        """
        return validate_enum(value, enum_class)

    def validate_composite(
        self, data: Dict[str, Any], rules: Dict[str, Dict[str, Any]]
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """Validate data against multiple validation rules.

        Args:
            data: The data to validate
            rules: Dictionary mapping field names to validation rules

        Returns:
            Tuple[bool, List[Dict[str, Any]]]: A tuple containing a boolean indicating
                validation success and a list of validation errors
        """
        return validate_composite(data, rules)

    def create_validator(self, validator_type: str, **options: Any) -> Validator:
        """Create a validator instance.

        Args:
            validator_type: The type of validator to create
            **options: Additional options for the validator

        Returns:
            Validator: The validator instance

        Raises:
            ValidationException: If the validator type is not supported
        """
        return ValidatorFactory.create_validator(validator_type, **options)

    def get_available_validators(self) -> List[str]:
        """Get a list of all available validator types.

        Returns:
            List[str]: List of registered validator type names
        """
        return ValidatorFactory.get_available_validators()


# Singleton instance for use in dependency injection
_validation_service: Optional[ValidationService] = None


def get_validation_service(db: Optional[AsyncSession] = None) -> ValidationService:
    """Get the validation service instance.

    This function is intended to be used with the dependency injection system.

    Args:
        db: Optional database session

    Returns:
        ValidationService: The validation service instance
    """
    global _validation_service

    if _validation_service is None:
        _validation_service = ValidationService(db)

    # Update the database session if provided
    if db is not None:
        _validation_service.db = db

    return _validation_service
