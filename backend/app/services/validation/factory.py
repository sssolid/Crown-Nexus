# /app/services/validation/factory.py
from __future__ import annotations

"""Factory for creating validators.

This module provides a factory for creating different validator instances
based on validation type and configuration options.
"""

from typing import Any, Dict, Type

from app.core.logging import get_logger
from app.services.validation.base import Validator
from app.services.validation.validators import (
    CreditCardValidator,
    DateValidator,
    EmailValidator,
    EnumValidator,
    IPAddressValidator,
    LengthValidator,
    PasswordValidator,
    PhoneValidator,
    RangeValidator,
    RegexValidator,
    RequiredValidator,
    URLValidator,
    UUIDValidator,
)

logger = get_logger("app.services.validation.factory")


class ValidatorFactory:
    """Factory for creating validator instances."""

    # Registry of validator types to their classes
    _validators: Dict[str, Type[Validator]] = {
        "email": EmailValidator,
        "phone": PhoneValidator,
        "date": DateValidator,
        "length": LengthValidator,
        "range": RangeValidator,
        "regex": RegexValidator,
        "required": RequiredValidator,
        "url": URLValidator,
        "uuid": UUIDValidator,
        "credit_card": CreditCardValidator,
        "ip_address": IPAddressValidator,
        "password": PasswordValidator,
        "enum": EnumValidator,
    }

    @classmethod
    def register_validator(cls, name: str, validator_class: Type[Validator]) -> None:
        """Register a new validator type.

        Args:
            name: Validator type name
            validator_class: Validator class

        Raises:
            ValueError: If a validator with the same name is already registered
        """
        if name in cls._validators:
            raise ValueError(f"Validator '{name}' is already registered")

        cls._validators[name] = validator_class
        logger.debug(f"Registered validator type: {name}")

    @classmethod
    def create_validator(cls, validator_type: str, **options: Any) -> Validator:
        """Create a validator of the specified type.

        Args:
            validator_type: The type of validator to create
            **options: Configuration options for the validator

        Returns:
            Validator: An instance of the specified validator

        Raises:
            ValueError: If the validator type is not supported
        """
        if validator_type not in cls._validators:
            raise ValueError(
                f"Unsupported validator type: {validator_type}. "
                f"Supported types: {', '.join(cls._validators.keys())}"
            )

        validator_class = cls._validators[validator_type]
        validator = validator_class()

        logger.debug(f"Created validator of type: {validator_type}")
        return validator
