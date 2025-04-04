from __future__ import annotations
'Database-specific validators.\n\nThis module provides validators that require database access,\nsuch as unique field validation.\n'
from typing import Any, Dict, List, Optional, Type, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
logger = get_logger('app.core.validation.db')
class UniqueValidator(Validator):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    async def validate_async(self, value: Any, field: str, model: Any, exclude_id: Optional[str]=None, **kwargs: Any) -> ValidationResult:
        logger.debug(f"Checking uniqueness of '{field}' in {model.__name__}", field=field, value=value, model=model.__name__, exclude_id=exclude_id)
        query = select(model).filter(getattr(model, field) == value)
        if exclude_id:
            query = query.filter(model.id != exclude_id)
        result = await self.db.execute(query)
        existing = result.first()
        if existing:
            logger.debug(f"Value '{value}' already exists for field '{field}' in {model.__name__}", field=field, value=value, model=model.__name__)
            return ValidationResult(is_valid=False, errors=[{'msg': f"Value '{value}' already exists for field '{field}'", 'type': 'unique_error', 'field': field, 'value': value}])
        logger.debug(f"Value '{value}' is unique for field '{field}' in {model.__name__}", field=field, value=value, model=model.__name__)
        return ValidationResult(is_valid=True)
    def validate(self, value: Any, field: str='', model: Any=None, exclude_id: Optional[str]=None, **kwargs: Any) -> ValidationResult:
        error_msg = 'UniqueValidator requires async operations. Use validate_async instead.'
        logger.error(error_msg)
        raise ValidationException('Validation method error', errors=[{'loc': ['method', 'validate'], 'msg': error_msg, 'type': 'method_error.async_required', 'hint': "Use 'await validator.validate_async()' instead of 'validator.validate()'"}])