from __future__ import annotations

"""Factory for creating validators.

This module provides a factory for creating different validator instances
based on validation type and configuration options.
"""

from typing import Any, Dict, List, Type

from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.core.validation.base import Validator
from app.core.validation.validators import (
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

logger = get_logger("app.core.validation.factory")


class ValidatorFactory:
    """Factory for creating validator instances.

    This class provides methods to register and create different types of validators.
    """

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
            name: The name to register the validator under
            validator_class: The validator class to register

        Raises:
            ValidationException: If a validator with the same name is already registered
        """
        if name in cls._validators:
            logger.warning(f"Attempted to register duplicate validator: {name}")
            raise ValidationException(
                "Validator registration failed",
                errors=[
                    {
                        "loc": ["validator", name],
                        "msg": f"Validator '{name}' is already registered",
                        "type": "validator_error.duplicate",
                    }
                ],
            )

        cls._validators[name] = validator_class
        logger.debug(f"Registered validator type: {name}")

    @classmethod
    def create_validator(cls, validator_type: str, **options: Any) -> Validator:
        """Create a validator instance of the specified type.

        Args:
            validator_type: The type of validator to create
            **options: Additional options for the validator

        Returns:
            Validator: An instance of the requested validator

        Raises:
            ValidationException: If the validator type is not supported
        """
        if validator_type not in cls._validators:
            supported_types = ", ".join(cls._validators.keys())
            logger.warning(
                f"Requested unsupported validator type: {validator_type}",
                supported_types=supported_types,
            )
            raise ValidationException(
                "Invalid validator type",
                errors=[
                    {
                        "loc": ["validator_type"],
                        "msg": f"Unsupported validator type: {validator_type}. Supported types: {supported_types}",
                        "type": "validator_error.unsupported_type",
                    }
                ],
            )

        validator_class = cls._validators[validator_type]
        validator = validator_class()
        logger.debug(f"Created validator of type: {validator_type}", options=options)
        return validator

    @classmethod
    def get_available_validators(cls) -> List[str]:
        """Get a list of all available validator types.

        Returns:
            List[str]: List of registered validator type names
        """
        return list(cls._validators.keys())
