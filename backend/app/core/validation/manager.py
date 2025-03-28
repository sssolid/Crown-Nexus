from __future__ import annotations

"""Core validation functionality.

This module provides the main validation functions for data validation
throughout the application.
"""

from datetime import date, datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union, cast

from pydantic import BaseModel, ValidationError

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error import resource_not_found, validation_error
from app.core.exceptions import (
    BusinessException,
    ErrorCode,
    ValidationException,
)
from app.core.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.db import UniqueValidator
from app.core.validation.factory import ValidatorFactory

logger = get_logger("app.core.validation.manager")


def validate_data(data: Dict[str, Any], schema_class: Type[BaseModel]) -> BaseModel:
    """Validate data against a Pydantic schema.

    Args:
        data: The data to validate
        schema_class: The Pydantic model class to validate against

    Returns:
        BaseModel: The validated model instance

    Raises:
        ValidationException: If validation fails
    """
    try:
        schema = schema_class(**data)
        logger.debug(
            f"Validated data against schema {schema_class.__name__}",
            schema=schema_class.__name__,
        )
        return schema
    except ValidationError as e:
        logger.warning(
            f"Validation error: {str(e)}",
            schema=schema_class.__name__,
            error_count=len(e.errors()),
        )
        errors = []
        for error in e.errors():
            errors.append({"loc": list(error["loc"]), "msg": error["msg"], "type": error["type"]})
        raise ValidationException("Validation error", errors=errors) from e


def validate_model(
    model: BaseModel, include: Optional[Set[str]] = None, exclude: Optional[Set[str]] = None
) -> None:
    """Validate an existing Pydantic model instance.

    Args:
        model: The model instance to validate
        include: Optional set of fields to include in validation
        exclude: Optional set of fields to exclude from validation

    Raises:
        ValidationException: If validation fails
    """
    try:
        model_dict = model.model_dump(include=include, exclude=exclude)
        model.__class__(**model_dict)
        logger.debug(
            f"Validated model instance of {model.__class__.__name__}",
            model_class=model.__class__.__name__,
            included_fields=include,
            excluded_fields=exclude,
        )
    except ValidationError as e:
        logger.warning(
            f"Model validation error: {str(e)}",
            model_class=model.__class__.__name__,
            error_count=len(e.errors()),
        )
        errors = []
        for error in e.errors():
            errors.append({"loc": list(error["loc"]), "msg": error["msg"], "type": error["type"]})
        raise ValidationException("Model validation error", errors=errors) from e


def validate_email(email: str) -> bool:
    """Validate an email address.

    Args:
        email: The email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("email")
    result = validator.validate(email)
    logger.debug(f"Email validation result: {result.is_valid}", email=email)
    return result.is_valid


def validate_phone(phone: str) -> bool:
    """Validate a phone number.

    Args:
        phone: The phone number to validate

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("phone")
    result = validator.validate(phone)
    logger.debug(f"Phone validation result: {result.is_valid}", phone=phone)
    return result.is_valid


def validate_date(
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
    validator = ValidatorFactory.create_validator("date")
    result = validator.validate(
        value, min_date=min_date, max_date=max_date, format_str=format_str
    )
    logger.debug(
        f"Date validation result: {result.is_valid}",
        value=value,
        min_date=min_date,
        max_date=max_date,
    )
    return result.is_valid


def validate_length(
    value: str, min_length: Optional[int] = None, max_length: Optional[int] = None
) -> bool:
    """Validate string length.

    Args:
        value: The string to validate
        min_length: Optional minimum length
        max_length: Optional maximum length

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("length")
    result = validator.validate(value, min_length=min_length, max_length=max_length)
    logger.debug(
        f"Length validation result: {result.is_valid}",
        value_length=len(value),
        min_length=min_length,
        max_length=max_length,
    )
    return result.is_valid


def validate_range(
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
    validator = ValidatorFactory.create_validator("range")
    result = validator.validate(value, min_value=min_value, max_value=max_value)
    logger.debug(
        f"Range validation result: {result.is_valid}",
        value=value,
        min_value=min_value,
        max_value=max_value,
    )
    return result.is_valid


def validate_regex(value: str, pattern: str) -> bool:
    """Validate string against a regex pattern.

    Args:
        value: The string to validate
        pattern: The regex pattern to validate against

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("regex")
    result = validator.validate(value, pattern=pattern)
    logger.debug(f"Regex validation result: {result.is_valid}", pattern=pattern)
    return result.is_valid


def validate_required(value: Any) -> bool:
    """Validate that a value is not None or empty.

    Args:
        value: The value to validate

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("required")
    result = validator.validate(value)
    logger.debug(f"Required validation result: {result.is_valid}")
    return result.is_valid


async def validate_unique(
    field: str, value: Any, model: Any, db: AsyncSession, exclude_id: Optional[str] = None
) -> bool:
    """Validate that a field value is unique in the database.

    Args:
        field: The field name to check
        value: The field value to check
        model: The SQLAlchemy model class
        db: The database session
        exclude_id: Optional ID to exclude from the uniqueness check

    Returns:
        bool: True if unique, False otherwise
    """
    validator = UniqueValidator(db)
    result = await validator.validate_async(
        value, field=field, model=model, exclude_id=exclude_id
    )
    logger.debug(
        f"Uniqueness validation result: {result.is_valid}",
        field=field,
        model=model.__name__,
        exclude_id=exclude_id,
    )
    return result.is_valid


def validate_url(url: str) -> bool:
    """Validate a URL.

    Args:
        url: The URL to validate

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("url")
    result = validator.validate(url)
    logger.debug(f"URL validation result: {result.is_valid}", url=url)
    return result.is_valid


def validate_uuid(value: str) -> bool:
    """Validate a UUID string.

    Args:
        value: The UUID string to validate

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("uuid")
    result = validator.validate(value)
    logger.debug(f"UUID validation result: {result.is_valid}", uuid=value)
    return result.is_valid


def validate_credit_card(card_number: str) -> bool:
    """Validate a credit card number.

    Args:
        card_number: The credit card number to validate

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("credit_card")
    result = validator.validate(card_number)
    # Don't log the full card number for security reasons
    masked_number = (
        "".join(["*" for _ in range(len(card_number) - 4)]) + card_number[-4:]
        if len(card_number) > 4
        else card_number
    )
    logger.debug(f"Credit card validation result: {result.is_valid}", card=masked_number)
    return result.is_valid


def validate_ip_address(ip: str, version: Optional[int] = None) -> bool:
    """Validate an IP address.

    Args:
        ip: The IP address to validate
        version: Optional IP version (4 or 6)

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("ip_address")
    result = validator.validate(ip, version=version)
    logger.debug(f"IP address validation result: {result.is_valid}", ip=ip, version=version)
    return result.is_valid


def validate_password_strength(
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
    validator = ValidatorFactory.create_validator("password")
    result = validator.validate(
        password,
        min_length=min_length,
        require_lowercase=require_lowercase,
        require_uppercase=require_uppercase,
        require_digit=require_digit,
        require_special=require_special,
    )
    # Don't log the password for security reasons
    logger.debug(
        f"Password strength validation result: {result.is_valid}",
        min_length=min_length,
        requirements={
            "lowercase": require_lowercase,
            "uppercase": require_uppercase,
            "digit": require_digit,
            "special": require_special,
        },
        password_length=len(password) if password else 0,
    )
    return result.is_valid


def validate_enum(value: Any, enum_class: Type[Enum]) -> bool:
    """Validate that a value is a valid enum value.

    Args:
        value: The value to validate
        enum_class: The enum class to validate against

    Returns:
        bool: True if valid, False otherwise
    """
    validator = ValidatorFactory.create_validator("enum")
    result = validator.validate(value, enum_class=enum_class)
    logger.debug(
        f"Enum validation result: {result.is_valid}",
        value=value,
        enum_class=enum_class.__name__,
        valid_values=[e.value for e in enum_class],
    )
    return result.is_valid


def validate_composite(
    data: Dict[str, Any], rules: Dict[str, Dict[str, Any]]
) -> Tuple[bool, List[Dict[str, Any]]]:
    """Validate data against multiple validation rules.

    Args:
        data: The data to validate
        rules: Dictionary mapping field names to validation rules

    Returns:
        Tuple[bool, List[Dict[str, Any]]]: A tuple containing a boolean indicating
            validation success and a list of validation errors
    """
    all_errors: List[Dict[str, Any]] = []
    fields_validated = 0

    for field, field_rules in rules.items():
        if field not in data:
            if field_rules.get("required", False):
                all_errors.append(
                    {"loc": [field], "msg": "Field is required", "type": "value_error.missing"}
                )
            continue

        value = data[field]
        fields_validated += 1

        for rule_name, rule_params in field_rules.items():
            if rule_name == "required":
                continue

            try:
                validator = ValidatorFactory.create_validator(rule_name)
            except ValueError as e:
                logger.error(f"Invalid validator type: {rule_name}", error=str(e))
                all_errors.append(
                    {
                        "loc": [field],
                        "msg": f"Invalid validator type: {rule_name}",
                        "type": "validator_error",
                    }
                )
                continue

            if isinstance(rule_params, dict):
                result = validator.validate(value, **rule_params)
            else:
                result = validator.validate(value, rule_params)

            if not result.is_valid:
                for error in result.errors:
                    error["loc"] = [field]
                    all_errors.append(error)

    is_valid = len(all_errors) == 0
    logger.debug(
        f"Composite validation result: {is_valid}",
        fields_validated=fields_validated,
        error_count=len(all_errors),
    )
    return (is_valid, all_errors)


def create_validator(rule_type: str, **params: Any) -> Callable[[Any], bool]:
    """Create a validator function for a specific rule type.

    Args:
        rule_type: The type of validator to create
        **params: Additional parameters for the validator

    Returns:
        Callable[[Any], bool]: A function that takes a value and returns a boolean

    Raises:
        ValidationException: If the validator type is not supported
    """
    try:
        validator = ValidatorFactory.create_validator(rule_type)
        logger.debug(f"Created validator function for rule type: {rule_type}", params=params)
    except ValueError as e:
        logger.error(f"Failed to create validator: {str(e)}")
        raise ValidationException(
            f"Failed to create validator",
            errors=[{"loc": ["validator"], "msg": str(e), "type": "validator_error"}]
        ) from e

    def validator_func(value: Any) -> bool:
        result = validator.validate(value, **params)
        return result.is_valid

    return validator_func


def register_validator(name: str, validator_class: Type[Validator]) -> None:
    """Register a custom validator.

    Args:
        name: The name to register the validator under
        validator_class: The validator class to register

    Raises:
        ValidationException: If a validator with the same name is already registered
    """
    try:
        ValidatorFactory.register_validator(name, validator_class)
        logger.info(f"Registered custom validator: {name}")
    except ValueError as e:
        logger.error(f"Failed to register validator: {str(e)}")
        raise ValidationException(
            f"Failed to register validator",
            errors=[{"loc": ["validator"], "msg": str(e), "type": "validator_error"}]
        ) from e


async def initialize() -> None:
    """Initialize the validation system."""
    logger.info("Initializing validation system")


async def shutdown() -> None:
    """Shutdown the validation system."""
    logger.info("Shutting down validation system")
