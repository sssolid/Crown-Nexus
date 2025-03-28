from __future__ import annotations

"""Validation package for application-wide data validation.

This package provides core functionality for validating different types of data,
ensuring data integrity and consistency throughout the application.
"""

from app.core.validation.base import ValidationResult, Validator
from app.core.validation.db import UniqueValidator
from app.core.validation.factory import ValidatorFactory
from app.core.validation.manager import (
    # High-level validation functions
    validate_data,
    validate_model,

    # Type-specific validation functions
    validate_email,
    validate_phone,
    validate_date,
    validate_length,
    validate_range,
    validate_regex,
    validate_required,
    validate_unique,
    validate_url,
    validate_uuid,
    validate_credit_card,
    validate_ip_address,
    validate_password_strength,
    validate_enum,
    validate_composite,

    # Factory and registration functions
    create_validator,
    register_validator,

    # Lifecycle functions
    initialize,
    shutdown,
)
from app.core.validation.service import ValidationService, get_validation_service
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

__all__ = [
    # Base types
    'ValidationResult',
    'Validator',
    'ValidatorFactory',

    # High-level validation functions
    'validate_data',
    'validate_model',

    # Type-specific validation functions
    'validate_email',
    'validate_phone',
    'validate_date',
    'validate_length',
    'validate_range',
    'validate_regex',
    'validate_required',
    'validate_unique',
    'validate_url',
    'validate_uuid',
    'validate_credit_card',
    'validate_ip_address',
    'validate_password_strength',
    'validate_enum',
    'validate_composite',

    # Factory and registration functions
    'create_validator',
    'register_validator',

    # Lifecycle functions
    'initialize',
    'shutdown',

    # Service
    'ValidationService',
    'get_validation_service',

    # Validator implementations
    'CreditCardValidator',
    'DateValidator',
    'EmailValidator',
    'EnumValidator',
    'IPAddressValidator',
    'LengthValidator',
    'PasswordValidator',
    'PhoneValidator',
    'RangeValidator',
    'RegexValidator',
    'RequiredValidator',
    'URLValidator',
    'UUIDValidator',
    'UniqueValidator',
]
