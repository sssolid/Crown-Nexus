from __future__ import annotations
'Core validation functionality.\n\nThis module provides the main validation functions for data validation\nthroughout the application.\n'
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union, cast
from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.db import UniqueValidator
from app.core.validation.factory import ValidatorFactory
logger = get_logger('app.core.validation.manager')
def validate_data(data: Dict[str, Any], schema_class: Type[BaseModel]) -> BaseModel:
    try:
        schema = schema_class(**data)
        return schema
    except ValidationError as e:
        logger.warning(f'Validation error: {str(e)}')
        errors = []
        for error in e.errors():
            errors.append({'loc': list(error['loc']), 'msg': error['msg'], 'type': error['type']})
        raise ValidationException('Validation error', errors=errors)
def validate_model(model: BaseModel, include: Optional[Set[str]]=None, exclude: Optional[Set[str]]=None) -> None:
    try:
        model_dict = model.model_dump(include=include, exclude=exclude)
        model.__class__(**model_dict)
    except ValidationError as e:
        logger.warning(f'Model validation error: {str(e)}')
        errors = []
        for error in e.errors():
            errors.append({'loc': list(error['loc']), 'msg': error['msg'], 'type': error['type']})
        raise ValidationException('Model validation error', errors=errors)
def validate_email(email: str) -> bool:
    validator = ValidatorFactory.create_validator('email')
    result = validator.validate(email)
    return result.is_valid
def validate_phone(phone: str) -> bool:
    validator = ValidatorFactory.create_validator('phone')
    result = validator.validate(phone)
    return result.is_valid
def validate_date(value: Union[str, date, datetime], min_date: Optional[Union[str, date, datetime]]=None, max_date: Optional[Union[str, date, datetime]]=None, format_str: Optional[str]=None) -> bool:
    validator = ValidatorFactory.create_validator('date')
    result = validator.validate(value, min_date=min_date, max_date=max_date, format_str=format_str)
    return result.is_valid
def validate_length(value: str, min_length: Optional[int]=None, max_length: Optional[int]=None) -> bool:
    validator = ValidatorFactory.create_validator('length')
    result = validator.validate(value, min_length=min_length, max_length=max_length)
    return result.is_valid
def validate_range(value: Union[int, float], min_value: Optional[Union[int, float]]=None, max_value: Optional[Union[int, float]]=None) -> bool:
    validator = ValidatorFactory.create_validator('range')
    result = validator.validate(value, min_value=min_value, max_value=max_value)
    return result.is_valid
def validate_regex(value: str, pattern: str) -> bool:
    validator = ValidatorFactory.create_validator('regex')
    result = validator.validate(value, pattern=pattern)
    return result.is_valid
def validate_required(value: Any) -> bool:
    validator = ValidatorFactory.create_validator('required')
    result = validator.validate(value)
    return result.is_valid
async def validate_unique(field: str, value: Any, model: Any, db: AsyncSession, exclude_id: Optional[str]=None) -> bool:
    validator = UniqueValidator(db)
    result = await validator.validate_async(value, field=field, model=model, exclude_id=exclude_id)
    return result.is_valid
def validate_url(url: str) -> bool:
    validator = ValidatorFactory.create_validator('url')
    result = validator.validate(url)
    return result.is_valid
def validate_uuid(value: str) -> bool:
    validator = ValidatorFactory.create_validator('uuid')
    result = validator.validate(value)
    return result.is_valid
def validate_credit_card(card_number: str) -> bool:
    validator = ValidatorFactory.create_validator('credit_card')
    result = validator.validate(card_number)
    return result.is_valid
def validate_ip_address(ip: str, version: Optional[int]=None) -> bool:
    validator = ValidatorFactory.create_validator('ip_address')
    result = validator.validate(ip, version=version)
    return result.is_valid
def validate_password_strength(password: str, min_length: int=8, require_lowercase: bool=True, require_uppercase: bool=True, require_digit: bool=True, require_special: bool=True) -> bool:
    validator = ValidatorFactory.create_validator('password')
    result = validator.validate(password, min_length=min_length, require_lowercase=require_lowercase, require_uppercase=require_uppercase, require_digit=require_digit, require_special=require_special)
    return result.is_valid
def validate_enum(value: Any, enum_class: Type[Enum]) -> bool:
    validator = ValidatorFactory.create_validator('enum')
    result = validator.validate(value, enum_class=enum_class)
    return result.is_valid
def validate_composite(data: Dict[str, Any], rules: Dict[str, Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
    all_errors: List[Dict[str, Any]] = []
    for field, field_rules in rules.items():
        if field not in data:
            if field_rules.get('required', False):
                all_errors.append({'loc': [field], 'msg': 'Field is required', 'type': 'value_error.missing'})
            continue
        value = data[field]
        for rule_name, rule_params in field_rules.items():
            if rule_name == 'required':
                continue
            validator = ValidatorFactory.create_validator(rule_name)
            if isinstance(rule_params, dict):
                result = validator.validate(value, **rule_params)
            else:
                result = validator.validate(value, rule_params)
            if not result.is_valid:
                for error in result.errors:
                    error['loc'] = [field]
                    all_errors.append(error)
    return (len(all_errors) == 0, all_errors)
def create_validator(rule_type: str, **params: Any) -> Callable[[Any], bool]:
    validator = ValidatorFactory.create_validator(rule_type)
    def validator_func(value: Any) -> bool:
        result = validator.validate(value, **params)
        return result.is_valid
    return validator_func
def register_validator(name: str, validator_class: Type[Validator]) -> None:
    ValidatorFactory.register_validator(name, validator_class)
    logger.debug(f'Registered custom validator: {name}')
async def initialize() -> None:
    logger.info('Initializing validation system')
async def shutdown() -> None:
    logger.info('Shutting down validation system')
from datetime import date, datetime