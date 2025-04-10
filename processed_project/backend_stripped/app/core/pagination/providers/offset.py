from __future__ import annotations
'Offset-based pagination provider implementation.\n\nThis module provides a pagination provider that uses offset-based pagination,\nwhich is suitable for most use cases where the total count is needed.\n'
from typing import Any, Callable, Generic, List, Optional, TypeVar, cast
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.logging import get_logger
from app.db.utils import count_query, execute_query
from app.core.pagination.base import OffsetPaginationParams, PaginationProvider, PaginationResult, SortDirection, SortField
from app.core.pagination.exceptions import InvalidSortFieldException
logger = get_logger('app.core.pagination.providers.offset')
T = TypeVar('T')
R = TypeVar('R')
class OffsetPaginationProvider(Generic[T, R], PaginationProvider[T, R]):
    def __init__(self, db: AsyncSession, model_class: type[DeclarativeMeta]) -> None:
        self.db = db
        self.model_class = model_class
        self.logger = logger
    async def paginate_with_offset(self, query: Select, params: OffsetPaginationParams, transform_func: Optional[Callable[[T], R]]=None) -> PaginationResult[R]:
        total = await count_query(self.db, query)
        page = params.page
        page_size = params.page_size
        pages = (total + page_size - 1) // page_size if total > 0 else 0
        if page > pages > 0:
            page = pages
        if params.sort:
            query = self._apply_sorting(query, params.sort)
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await execute_query(self.db, query)
        items = list(result.scalars().all())
        transformed_items: List[Any] = items
        if transform_func:
            transformed_items = [transform_func(item) for item in items]
        return PaginationResult[R](items=cast(List[R], transformed_items), total=total, page=page, page_size=page_size, pages=pages, has_next=page < pages, has_prev=page > 1)
    async def paginate_with_cursor(self, query: Select, params: Any, transform_func: Optional[Callable[[T], R]]=None) -> PaginationResult[R]:
        raise NotImplementedError('Cursor-based pagination is not supported by OffsetPaginationProvider. Use CursorPaginationProvider instead.')
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