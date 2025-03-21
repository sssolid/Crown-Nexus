from __future__ import annotations
'Factory for creating validators.\n\nThis module provides a factory for creating different validator instances\nbased on validation type and configuration options.\n'
from typing import Any, Dict, Type
from app.core.logging import get_logger
from app.core.validation.base import Validator
from app.core.validation.validators import CreditCardValidator, DateValidator, EmailValidator, EnumValidator, IPAddressValidator, LengthValidator, PasswordValidator, PhoneValidator, RangeValidator, RegexValidator, RequiredValidator, URLValidator, UUIDValidator
logger = get_logger('app.core.validation.factory')
class ValidatorFactory:
    _validators: Dict[str, Type[Validator]] = {'email': EmailValidator, 'phone': PhoneValidator, 'date': DateValidator, 'length': LengthValidator, 'range': RangeValidator, 'regex': RegexValidator, 'required': RequiredValidator, 'url': URLValidator, 'uuid': UUIDValidator, 'credit_card': CreditCardValidator, 'ip_address': IPAddressValidator, 'password': PasswordValidator, 'enum': EnumValidator}
    @classmethod
    def register_validator(cls, name: str, validator_class: Type[Validator]) -> None:
        if name in cls._validators:
            raise ValueError(f"Validator '{name}' is already registered")
        cls._validators[name] = validator_class
        logger.debug(f'Registered validator type: {name}')
    @classmethod
    def create_validator(cls, validator_type: str, **options: Any) -> Validator:
        if validator_type not in cls._validators:
            raise ValueError(f"Unsupported validator type: {validator_type}. Supported types: {', '.join(cls._validators.keys())}")
        validator_class = cls._validators[validator_type]
        validator = validator_class()
        logger.debug(f'Created validator of type: {validator_type}')
        return validator