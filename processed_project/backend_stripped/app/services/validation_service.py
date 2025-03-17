from __future__ import annotations
import re
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Type, Union, cast
from pydantic import BaseModel, Field, ValidationError, root_validator, validator
from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
logger = get_logger('app.services.validation_service')
class ValidationService:
    def __init__(self) -> None:
        self.logger = logger
        self.validators: Dict[str, callable] = {'email': self.validate_email, 'phone': self.validate_phone, 'date': self.validate_date, 'length': self.validate_length, 'range': self.validate_range, 'regex': self.validate_regex, 'required': self.validate_required, 'unique': self.validate_unique}
    async def initialize(self) -> None:
        self.logger.debug('Initializing validation service')
    async def shutdown(self) -> None:
        self.logger.debug('Shutting down validation service')
    def validate_data(self, data: Dict[str, Any], schema_class: Type[BaseModel]) -> BaseModel:
        try:
            schema = schema_class(**data)
            return schema
        except ValidationError as e:
            self.logger.warning(f'Validation error: {str(e)}')
            errors = []
            for error in e.errors():
                errors.append({'loc': list(error['loc']), 'msg': error['msg'], 'type': error['type']})
            raise ValidationException('Validation error', code='validation_error', details={'errors': errors}, status_code=400)
    def validate_email(self, email: str) -> bool:
        pattern = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    def validate_phone(self, phone: str) -> bool:
        cleaned = re.sub('[\\s\\-\\(\\).]', '', phone)
        return bool(re.match('^\\+?[0-9]{10,15}$', cleaned))
    def validate_date(self, value: Union[str, date, datetime], min_date: Optional[Union[str, date, datetime]]=None, max_date: Optional[Union[str, date, datetime]]=None, format_str: Optional[str]=None) -> bool:
        if isinstance(value, str):
            if not format_str:
                format_str = '%Y-%m-%d'
            try:
                value = datetime.strptime(value, format_str).date()
            except ValueError:
                return False
        if isinstance(value, datetime):
            value = value.date()
        if min_date and isinstance(min_date, str):
            if not format_str:
                format_str = '%Y-%m-%d'
            try:
                min_date = datetime.strptime(min_date, format_str).date()
            except ValueError:
                return False
        if max_date and isinstance(max_date, str):
            if not format_str:
                format_str = '%Y-%m-%d'
            try:
                max_date = datetime.strptime(max_date, format_str).date()
            except ValueError:
                return False
        if min_date and isinstance(min_date, datetime):
            min_date = min_date.date()
        if max_date and isinstance(max_date, datetime):
            max_date = max_date.date()
        if min_date and value < min_date:
            return False
        if max_date and value > max_date:
            return False
        return True
    def validate_length(self, value: str, min_length: Optional[int]=None, max_length: Optional[int]=None) -> bool:
        if min_length is not None and len(value) < min_length:
            return False
        if max_length is not None and len(value) > max_length:
            return False
        return True
    def validate_range(self, value: Union[int, float], min_value: Optional[Union[int, float]]=None, max_value: Optional[Union[int, float]]=None) -> bool:
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
    def validate_regex(self, value: str, pattern: str) -> bool:
        return bool(re.match(pattern, value))
    def validate_required(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str) and (not value.strip()):
            return False
        if isinstance(value, (list, dict, set)) and (not value):
            return False
        return True
    async def validate_unique(self, field: str, value: Any, model: Any, db: Any, exclude_id: Optional[str]=None) -> bool:
        from sqlalchemy import select
        query = select(model).filter(getattr(model, field) == value)
        if exclude_id:
            query = query.filter(model.id != exclude_id)
        result = await db.execute(query)
        return result.first() is None