from __future__ import annotations
'Core validation functionality.\n\nThis module provides the main validation functions for data validation\nthroughout the application.\n'
from datetime import date, datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union, cast
from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.error import resource_not_found, validation_error
from app.core.exceptions import BusinessException, ErrorCode, ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.db import UniqueValidator
from app.core.validation.factory import ValidatorFactory
logger = get_logger('app.core.validation.manager')
def validate_data(data: Dict[str, Any], schema_class: Type[BaseModel]) -> BaseModel:
    try:
        schema = schema_class(**data)
        logger.debug(f'Validated data against schema {schema_class.__name__}', schema=schema_class.__name__)
        return schema
    except ValidationError as e:
        logger.warning(f'Validation error: {str(e)}', schema=schema_class.__name__, error_count=len(e.errors()))
        errors = []
        for error in e.errors():
            errors.append({'loc': list(error['loc']), 'msg': error['msg'], 'type': error['type']})
        raise ValidationException('Validation error', errors=errors) from e
def validate_model(model: BaseModel, include: Optional[Set[str]]=None, exclude: Optional[Set[str]]=None) -> None:
    try:
        model_dict = model.model_dump(include=include, exclude=exclude)
        model.__class__(**model_dict)
        logger.debug(f'Validated model instance of {model.__class__.__name__}', model_class=model.__class__.__name__, included_fields=include, excluded_fields=exclude)
    except ValidationError as e:
        logger.warning(f'Model validation error: {str(e)}', model_class=model.__class__.__name__, error_count=len(e.errors()))
        errors = []
        for error in e.errors():
            errors.append({'loc': list(error['loc']), 'msg': error['msg'], 'type': error['type']})
        raise ValidationException('Model validation error', errors=errors) from e
def validate_email(email: str) -> bool:
    validator = ValidatorFactory.create_validator('email')
    result = validator.validate(email)
    logger.debug(f'Email validation result: {result.is_valid}', email=email)
    return result.is_valid
def validate_phone(phone: str) -> bool:
    validator = ValidatorFactory.create_validator('phone')
    result = validator.validate(phone)
    logger.debug(f'Phone validation result: {result.is_valid}', phone=phone)
    return result.is_valid
def validate_date(value: Union[str, date, datetime], min_date: Optional[Union[str, date, datetime]]=None, max_date: Optional[Union[str, date, datetime]]=None, format_str: Optional[str]=None) -> bool:
    validator = ValidatorFactory.create_validator('date')
    result = validator.validate(value, min_date=min_date, max_date=max_date, format_str=format_str)
    logger.debug(f'Date validation result: {result.is_valid}', value=value, min_date=min_date, max_date=max_date)
    return result.is_valid
def validate_length(value: str, min_length: Optional[int]=None, max_length: Optional[int]=None) -> bool:
    validator = ValidatorFactory.create_validator('length')
    result = validator.validate(value, min_length=min_length, max_length=max_length)
    logger.debug(f'Length validation result: {result.is_valid}', value_length=len(value), min_length=min_length, max_length=max_length)
    return result.is_valid
def validate_range(value: Union[int, float], min_value: Optional[Union[int, float]]=None, max_value: Optional[Union[int, float]]=None) -> bool:
    validator = ValidatorFactory.create_validator('range')
    result = validator.validate(value, min_value=min_value, max_value=max_value)
    logger.debug(f'Range validation result: {result.is_valid}', value=value, min_value=min_value, max_value=max_value)
    return result.is_valid
def validate_regex(value: str, pattern: str) -> bool:
    validator = ValidatorFactory.create_validator('regex')
    result = validator.validate(value, pattern=pattern)
    logger.debug(f'Regex validation result: {result.is_valid}', pattern=pattern)
    return result.is_valid
def validate_required(value: Any) -> bool:
    validator = ValidatorFactory.create_validator('required')
    result = validator.validate(value)
    logger.debug(f'Required validation result: {result.is_valid}')
    return result.is_valid
async def validate_unique(field: str, value: Any, model: Any, db: AsyncSession, exclude_id: Optional[str]=None) -> bool:
    validator = UniqueValidator(db)
    result = await validator.validate_async(value, field=field, model=model, exclude_id=exclude_id)
    logger.debug(f'Uniqueness validation result: {result.is_valid}', field=field, model=model.__name__, exclude_id=exclude_id)
    return result.is_valid
def validate_url(url: str) -> bool:
    validator = ValidatorFactory.create_validator('url')
    result = validator.validate(url)
    logger.debug(f'URL validation result: {result.is_valid}', url=url)
    return result.is_valid
def validate_uuid(value: str) -> bool:
    validator = ValidatorFactory.create_validator('uuid')
    result = validator.validate(value)
    logger.debug(f'UUID validation result: {result.is_valid}', uuid=value)
    return result.is_valid
def validate_credit_card(card_number: str) -> bool:
    validator = ValidatorFactory.create_validator('credit_card')
    result = validator.validate(card_number)
    masked_number = ''.join(['*' for _ in range(len(card_number) - 4)]) + card_number[-4:] if len(card_number) > 4 else card_number
    logger.debug(f'Credit card validation result: {result.is_valid}', card=masked_number)
    return result.is_valid
def validate_ip_address(ip: str, version: Optional[int]=None) -> bool:
    validator = ValidatorFactory.create_validator('ip_address')
    result = validator.validate(ip, version=version)
    logger.debug(f'IP address validation result: {result.is_valid}', ip=ip, version=version)
    return result.is_valid
def validate_password_strength(password: str, min_length: int=8, require_lowercase: bool=True, require_uppercase: bool=True, require_digit: bool=True, require_special: bool=True) -> bool:
    validator = ValidatorFactory.create_validator('password')
    result = validator.validate(password, min_length=min_length, require_lowercase=require_lowercase, require_uppercase=require_uppercase, require_digit=require_digit, require_special=require_special)
    logger.debug(f'Password strength validation result: {result.is_valid}', min_length=min_length, requirements={'lowercase': require_lowercase, 'uppercase': require_uppercase, 'digit': require_digit, 'special': require_special}, password_length=len(password) if password else 0)
    return result.is_valid
def validate_enum(value: Any, enum_class: Type[Enum]) -> bool:
    validator = ValidatorFactory.create_validator('enum')
    result = validator.validate(value, enum_class=enum_class)
    logger.debug(f'Enum validation result: {result.is_valid}', value=value, enum_class=enum_class.__name__, valid_values=[e.value for e in enum_class])
    return result.is_valid
def validate_composite(data: Dict[str, Any], rules: Dict[str, Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
    all_errors: List[Dict[str, Any]] = []
    fields_validated = 0
    for field, field_rules in rules.items():
        if field not in data:
            if field_rules.get('required', False):
                all_errors.append({'loc': [field], 'msg': 'Field is required', 'type': 'value_error.missing'})
            continue
        value = data[field]
        fields_validated += 1
        for rule_name, rule_params in field_rules.items():
            if rule_name == 'required':
                continue
            try:
                validator = ValidatorFactory.create_validator(rule_name)
            except ValueError as e:
                logger.error(f'Invalid validator type: {rule_name}', error=str(e))
                all_errors.append({'loc': [field], 'msg': f'Invalid validator type: {rule_name}', 'type': 'validator_error'})
                continue
            if isinstance(rule_params, dict):
                result = validator.validate(value, **rule_params)
            else:
                result = validator.validate(value, rule_params)
            if not result.is_valid:
                for error in result.errors:
                    error['loc'] = [field]
                    all_errors.append(error)
    is_valid = len(all_errors) == 0
    logger.debug(f'Composite validation result: {is_valid}', fields_validated=fields_validated, error_count=len(all_errors))
    return (is_valid, all_errors)
def create_validator(rule_type: str, **params: Any) -> Callable[[Any], bool]:
    try:
        validator = ValidatorFactory.create_validator(rule_type)
        logger.debug(f'Created validator function for rule type: {rule_type}', params=params)
    except ValueError as e:
        logger.error(f'Failed to create validator: {str(e)}')
        raise ValidationException(f'Failed to create validator', errors=[{'loc': ['validator'], 'msg': str(e), 'type': 'validator_error'}]) from e
    def validator_func(value: Any) -> bool:
        result = validator.validate(value, **params)
        return result.is_valid
    return validator_func
def register_validator(name: str, validator_class: Type[Validator]) -> None:
    try:
        ValidatorFactory.register_validator(name, validator_class)
        logger.info(f'Registered custom validator: {name}')
    except ValueError as e:
        logger.error(f'Failed to register validator: {str(e)}')
        raise ValidationException(f'Failed to register validator', errors=[{'loc': ['validator'], 'msg': str(e), 'type': 'validator_error'}]) from e
async def initialize() -> None:
    logger.info('Initializing validation system')
async def shutdown() -> None:
    logger.info('Shutting down validation system')