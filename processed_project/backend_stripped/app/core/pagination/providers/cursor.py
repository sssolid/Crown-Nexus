from __future__ import annotations
'Cursor-based pagination provider implementation.\n\nThis module provides a pagination provider that uses cursor-based pagination,\nwhich is suitable for large datasets and continuous scrolling interfaces.\n'
import base64
import json
from datetime import datetime
import uuid
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, cast
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.logging import get_logger
from app.db.utils import count_query, execute_query
from app.core.pagination.base import CursorPaginationParams, PaginationProvider, PaginationResult, SortDirection, SortField
from app.core.pagination.exceptions import InvalidCursorException, InvalidSortFieldException
logger = get_logger('app.core.pagination.providers.cursor')
T = TypeVar('T')
R = TypeVar('R')
class CursorPaginationProvider(Generic[T, R], PaginationProvider[T, R]):
    def __init__(self, db: AsyncSession, model_class: type[DeclarativeMeta]) -> None:
        self.db = db
        self.model_class = model_class
        self.logger = logger
    async def paginate_with_offset(self, query: Select, params: Any, transform_func: Optional[Callable[[T], R]]=None) -> PaginationResult[R]:
        raise NotImplementedError('Offset-based pagination is not supported by CursorPaginationProvider. Use OffsetPaginationProvider instead.')
    async def paginate_with_cursor(self, query: Select, params: CursorPaginationParams, transform_func: Optional[Callable[[T], R]]=None) -> PaginationResult[R]:
        sort_fields = params.sort or [SortField(field='id', direction=SortDirection.ASC)]
        cursor_values = None
        if params.cursor:
            try:
                cursor_values = self._decode_cursor(params.cursor)
            except Exception as e:
                self.logger.warning(f'Invalid cursor: {str(e)}', extra={'cursor': params.cursor})
                raise InvalidCursorException(message=f'Invalid cursor format: {str(e)}', cursor=params.cursor, original_exception=e) from e
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
        transformed_items: List[Any] = items
        if transform_func:
            transformed_items = [transform_func(item) for item in items]
        return PaginationResult[R](items=cast(List[R], transformed_items), total=total, next_cursor=next_cursor, has_next=has_next, has_prev=bool(params.cursor))
    def _apply_sorting(self, query: Select, sort_fields: List[SortField]) -> Select:
        for sort_field in sort_fields:
            field_name = sort_field.field
            if not hasattr(self.model_class, field_name):
                self.logger.warning(f'Invalid sort field: {field_name}', extra={'model': self.model_class.__name__, 'field': field_name})
                raise InvalidSortFieldException(field=field_name, model=self.model_class.__name__)
            column = getattr(self.model_class, field_name)
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
            if not hasattr(self.model_class, field_name):
                self.logger.warning(f'Invalid cursor field: {field_name}', extra={'model': self.model_class.__name__, 'field': field_name})
                raise InvalidSortFieldException(field=field_name, model=self.model_class.__name__, message=f'Invalid cursor field: {field_name}')
            column = getattr(self.model_class, field_name)
            value = cursor_values[field_name]
            if i == 0:
                if sort_field.direction == SortDirection.ASC:
                    conditions.append(column > value)
                else:
                    conditions.append(column < value)
            else:
                previous_field = sort_fields[i - 1].field
                previous_column = getattr(self.model_class, previous_field)
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
            raise ValueError(f'Invalid cursor format: {str(e)}') from e