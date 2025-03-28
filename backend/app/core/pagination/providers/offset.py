# app/core/pagination/providers/offset.py
from __future__ import annotations

"""Offset-based pagination provider implementation.

This module provides a pagination provider that uses offset-based pagination,
which is suitable for most use cases where the total count is needed.
"""

from typing import Any, Callable, Generic, List, Optional, TypeVar, cast

from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select

from app.logging import get_logger
from app.db.utils import count_query, execute_query
from app.core.pagination.base import (
    OffsetPaginationParams,
    PaginationProvider,
    PaginationResult,
    SortDirection,
    SortField,
)
from app.core.pagination.exceptions import InvalidSortFieldException

logger = get_logger("app.core.pagination.providers.offset")

T = TypeVar("T")
R = TypeVar("R")


class OffsetPaginationProvider(Generic[T, R], PaginationProvider[T, R]):
    """
    Offset-based pagination provider implementation.

    This provider implements pagination using the offset-based approach,
    which is suitable for most use cases where the total count is needed.
    """

    def __init__(self, db: AsyncSession, model_class: type[DeclarativeMeta]) -> None:
        """
        Initialize the offset pagination provider.

        Args:
            db: Database session
            model_class: SQLAlchemy model class
        """
        self.db = db
        self.model_class = model_class
        self.logger = logger

    async def paginate_with_offset(
        self,
        query: Select,
        params: OffsetPaginationParams,
        transform_func: Optional[Callable[[T], R]] = None,
    ) -> PaginationResult[R]:
        """
        Paginate query results using offset-based pagination.

        Args:
            query: SQLAlchemy select query
            params: Offset pagination parameters
            transform_func: Optional function to transform each result item

        Returns:
            PaginationResult with paginated items and metadata

        Raises:
            InvalidSortFieldException: If a sort field is invalid
        """
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

        return PaginationResult[R](
            items=cast(List[R], transformed_items),
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )

    async def paginate_with_cursor(
        self,
        query: Select,
        params: Any,
        transform_func: Optional[Callable[[T], R]] = None,
    ) -> PaginationResult[R]:
        """
        Cursor-based pagination is not supported by this provider.

        Args:
            query: SQLAlchemy select query
            params: Cursor pagination parameters
            transform_func: Optional function to transform each result item

        Raises:
            NotImplementedError: Always raised because this method is not supported
        """
        raise NotImplementedError(
            "Cursor-based pagination is not supported by OffsetPaginationProvider. "
            "Use CursorPaginationProvider instead."
        )

    def _apply_sorting(self, query: Select, sort_fields: List[SortField]) -> Select:
        """
        Apply sorting to the query based on sort fields.

        Args:
            query: SQLAlchemy select query
            sort_fields: List of fields to sort by

        Returns:
            Query with sorting applied

        Raises:
            InvalidSortFieldException: If a sort field is invalid
        """
        for sort_field in sort_fields:
            field_name = sort_field.field
            if not hasattr(self.model_class, field_name):
                self.logger.warning(
                    f"Invalid sort field: {field_name}",
                    extra={"model": self.model_class.__name__, "field": field_name},
                )
                raise InvalidSortFieldException(
                    field=field_name, model=self.model_class.__name__
                )

            column = getattr(self.model_class, field_name)
            if sort_field.direction == SortDirection.DESC:
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))

        return query
