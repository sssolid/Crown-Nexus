from __future__ import annotations
import base64
import json
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union, cast
from fastapi import HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import Column, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import ClauseElement
from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.db.base_class import Base
from app.db.utils import count_query, execute_query
from app.schemas.pagination import CursorPaginationParams, OffsetPaginationParams, PaginationResult, SortDirection, SortField
logger = get_logger('app.services.pagination')
T = TypeVar('T', bound=Base)
R = TypeVar('R', bound=BaseModel)
class PaginationService(Generic[T, R]):
    def __init__(self, db: AsyncSession, model: Type[T], response_model: Type[R]) -> None:
        self.db = db
        self.model = model
        self.response_model = response_model
    async def paginate_with_offset(self, query: Select, params: OffsetPaginationParams, transform_func: Optional[Callable[[T], R]]=None) -> PaginationResult[R]:
        total = await count_query(self.db, query)
        page = params.page
        page_size = params.page_size
        pages = (total + page_size - 1) // page_size if total > 0 else 0
        if page > pages and pages > 0:
            page = pages
        if params.sort:
            query = self._apply_sorting(query, params.sort)
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await execute_query(self.db, query)
        items = list(result.scalars().all())
        transformed_items = items
        if transform_func:
            transformed_items = [transform_func(item) for item in items]
        elif hasattr(self.response_model, 'from_orm'):
            transformed_items = [self.response_model.from_orm(item) for item in items]
        return PaginationResult[R](items=transformed_items, total=total, page=page, page_size=page_size, pages=pages, has_next=page < pages, has_prev=page > 1)
    async def paginate_with_cursor(self, query: Select, params: CursorPaginationParams, transform_func: Optional[Callable[[T], R]]=None) -> PaginationResult[R]:
        sort_fields = params.sort or [SortField(field='id', direction=SortDirection.ASC)]
        cursor_values = None
        if params.cursor:
            try:
                cursor_values = self._decode_cursor(params.cursor)
            except Exception as e:
                logger.warning(f'Invalid cursor: {str(e)}')
                raise ValidationException(message='Invalid cursor format')
        original_query = query
        if cursor_values:
            query = self._apply_cursor_filter(query, sort_fields, cursor_values)
        query = self._apply_sorting(query, sort_fields)
        query = query.limit(params.limit + 1)
        result = await execute_query(self.db, query)
        items = list(result.scalars().all())
        total = 0
        if not params.cursor:
            total = await count_query(self.db, original_query)
        has_next = len(items) > params.limit
        if has_next:
            items = items[:params.limit]
        next_cursor = None
        if has_next and items:
            next_cursor = self._encode_cursor(items[-1], sort_fields)
        transformed_items = items
        if transform_func:
            transformed_items = [transform_func(item) for item in items]
        elif hasattr(self.response_model, 'from_orm'):
            transformed_items = [self.response_model.from_orm(item) for item in items]
        return PaginationResult[R](items=transformed_items, total=total, next_cursor=next_cursor, has_next=has_next, has_prev=bool(params.cursor))
    def _apply_sorting(self, query: Select, sort_fields: List[SortField]) -> Select:
        for sort_field in sort_fields:
            field_name = sort_field.field
            if not hasattr(self.model, field_name):
                raise ValidationException(message=f'Invalid sort field: {field_name}')
            column = getattr(self.model, field_name)
            if sort_field.direction == SortDirection.DESC:
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))
        return query
    def _apply_cursor_filter(self, query: Select, sort_fields: List[SortField], cursor_values: Dict[str, Any]) -> Select:
        conditions = []
        for i, sort_field in enumerate(sort_fields):
            field_name = sort_field.field
            if field_name not in cursor_values:
                continue
            if not hasattr(self.model, field_name):
                raise ValidationException(message=f'Invalid cursor field: {field_name}')
            column = getattr(self.model, field_name)
            value = cursor_values[field_name]
            if i == 0:
                if sort_field.direction == SortDirection.ASC:
                    conditions.append(column > value)
                else:
                    conditions.append(column < value)
            else:
                previous_field = sort_fields[i - 1].field
                previous_column = getattr(self.model, previous_field)
                previous_value = cursor_values[previous_field]
                conditions.append(previous_column == previous_value)
                if sort_field.direction == SortDirection.ASC:
                    conditions.append(column > value)
                else:
                    conditions.append(column < value)
        if conditions:
            query = query.where(*conditions)
        return query
    def _encode_cursor(self, item: T, sort_fields: List[SortField]) -> str:
        cursor_data = {}
        for sort_field in sort_fields:
            field_name = sort_field.field
            if not hasattr(item, field_name):
                continue
            value = getattr(item, field_name)
            if isinstance(value, (datetime, uuid.UUID)):
                value = str(value)
            cursor_data[field_name] = value
        cursor_json = json.dumps(cursor_data)
        return base64.b64encode(cursor_json.encode('utf-8')).decode('utf-8')
    def _decode_cursor(self, cursor: str) -> Dict[str, Any]:
        try:
            cursor_json = base64.b64decode(cursor.encode('utf-8')).decode('utf-8')
            return json.loads(cursor_json)
        except Exception as e:
            raise ValueError(f'Invalid cursor format: {str(e)}')