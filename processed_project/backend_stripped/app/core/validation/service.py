from __future__ import annotations
'Validation service implementation.\n\nThis module provides a service wrapper around the validation system,\nmaking it available through the dependency manager.\n'
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union
from datetime import date, datetime
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.factory import ValidatorFactory
from app.core.validation.manager import validate_composite, validate_credit_card, validate_data, validate_date, validate_email, validate_enum, validate_ip_address, validate_length, validate_model, validate_password_strength, validate_phone, validate_range, validate_regex, validate_required, validate_unique, validate_url, validate_uuid
logger = get_logger('app.core.validation.service')
class ValidationService:
    def __init__(self, db: Optional[AsyncSession]=None) -> None:
        self.db = db
        self._initialized = False
    async def initialize(self) -> None:
        if self._initialized:
            logger.debug('Validation service already initialized')
            return
        logger.info('Initializing validation service')
        self._initialized = True
    async def shutdown(self) -> None:
        if not self._initialized:
            return
        logger.info('Shutting down validation service')
        self._initialized = False
    def validate_data(self, data: Dict[str, Any], schema_class: Type[BaseModel]) -> BaseModel:
        return validate_data(data, schema_class)
    def validate_model(self, model: BaseModel, include: Optional[Set[str]]=None, exclude: Optional[Set[str]]=None) -> None:
        validate_model(model, include, exclude)
    def validate_email(self, email: str) -> bool:
        return validate_email(email)
    def validate_phone(self, phone: str) -> bool:
        return validate_phone(phone)
    def validate_date(self, value: Union[str, date, datetime], min_date: Optional[Union[str, date, datetime]]=None, max_date: Optional[Union[str, date, datetime]]=None, format_str: Optional[str]=None) -> bool:
        return validate_date(value, min_date, max_date, format_str)
    def validate_length(self, value: str, min_length: Optional[int]=None, max_length: Optional[int]=None) -> bool:
        return validate_length(value, min_length, max_length)
    def validate_range(self, value: Union[int, float], min_value: Optional[Union[int, float]]=None, max_value: Optional[Union[int, float]]=None) -> bool:
        return validate_range(value, min_value, max_value)
    def validate_regex(self, value: str, pattern: str) -> bool:
        return validate_regex(value, pattern)
    def validate_required(self, value: Any) -> bool:
        return validate_required(value)
    async def validate_unique(self, field: str, value: Any, model: Any, exclude_id: Optional[str]=None) -> bool:
        if not self.db:
            logger.error('Database session not available for unique validation')
            raise ValidationException('Validation error', errors=[{'loc': ['validator', 'unique'], 'msg': 'Database session not available for unique validation', 'type': 'validator_error.no_db_session'}])
        return await validate_unique(field, value, model, self.db, exclude_id)
    def validate_url(self, url: str) -> bool:
        return validate_url(url)
    def validate_uuid(self, value: str) -> bool:
        return validate_uuid(value)
    def validate_credit_card(self, card_number: str) -> bool:
        return validate_credit_card(card_number)
    def validate_ip_address(self, ip: str, version: Optional[int]=None) -> bool:
        return validate_ip_address(ip, version)
    def validate_password_strength(self, password: str, min_length: int=8, require_lowercase: bool=True, require_uppercase: bool=True, require_digit: bool=True, require_special: bool=True) -> bool:
        return validate_password_strength(password, min_length, require_lowercase, require_uppercase, require_digit, require_special)
    def validate_enum(self, value: Any, enum_class: Type[Enum]) -> bool:
        return validate_enum(value, enum_class)
    def validate_composite(self, data: Dict[str, Any], rules: Dict[str, Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
        return validate_composite(data, rules)
    def create_validator(self, validator_type: str, **options: Any) -> Validator:
        return ValidatorFactory.create_validator(validator_type, **options)
    def get_available_validators(self) -> List[str]:
        return ValidatorFactory.get_available_validators()
_validation_service: Optional[ValidationService] = None
def get_validation_service(db: Optional[AsyncSession]=None) -> ValidationService:
    global _validation_service
    if _validation_service is None:
        _validation_service = ValidationService(db)
    if db is not None:
        _validation_service.db = db
    return _validation_service