# Module: app.core.validation

**Path:** `app/core/validation/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.validation.base import ValidationResult, Validator, ValidatorFactory
from app.core.validation.db import UniqueValidator
from app.core.validation.factory import ValidatorFactory as FactoryImpl
from app.core.validation.manager import validate_data, validate_model, validate_email, validate_phone, validate_date, validate_length, validate_range, validate_regex, validate_required, validate_unique, validate_url, validate_uuid, validate_credit_card, validate_ip_address, validate_password_strength, validate_enum, validate_composite, create_validator, register_validator, initialize, shutdown
from app.core.validation.validators import CreditCardValidator, DateValidator, EmailValidator, EnumValidator, IPAddressValidator, LengthValidator, PasswordValidator, PhoneValidator, RangeValidator, RegexValidator, RequiredValidator, URLValidator, UUIDValidator
```

## Global Variables
```python
__all__ = __all__ = [
    # Base types
    "ValidationResult",
    "Validator",
    "ValidatorFactory",
    # Core validation functions
    "validate_data",
    "validate_model",
    "validate_email",
    "validate_phone",
    "validate_date",
    "validate_length",
    "validate_range",
    "validate_regex",
    "validate_required",
    "validate_unique",
    "validate_url",
    "validate_uuid",
    "validate_credit_card",
    "validate_ip_address",
    "validate_password_strength",
    "validate_enum",
    "validate_composite",
    "create_validator",
    "register_validator",
    "initialize",
    "shutdown",
    # Validator implementations
    "CreditCardValidator",
    "DateValidator",
    "EmailValidator",
    "EnumValidator",
    "IPAddressValidator",
    "LengthValidator",
    "PasswordValidator",
    "PhoneValidator",
    "RangeValidator",
    "RegexValidator",
    "RequiredValidator",
    "URLValidator",
    "UUIDValidator",
    "UniqueValidator",
]
```
