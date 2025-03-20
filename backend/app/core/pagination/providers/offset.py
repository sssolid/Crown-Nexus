# /app/core/pagination/providers/offset.py
from __future__ import annotations

"""Offset-based pagination provider implementation.

This module provides a pagination provider that uses offset-based pagination,
which is suitable for most use cases where the total count is needed.
"""

from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union, cast

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select

from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.db.utils import count_query, execute_query
from app.core.pagination.base import (
    OffsetPaginationParams,
    PaginationProvider,
    PaginationResult,
    SortDirection,
    SortField,
)

logger = get_logger(__name__)

T = TypeVar("T")  # Entity type
R = TypeVar("R")  # Result type


class OffsetPaginationProvider(Generic[T, R], PaginationProvider[T, R]):
    """Provider for offset-based pagination."""

    def __init__(self, db: AsyncSession, model_class: type[DeclarativeMeta]) -> None:
        """Initialize the offset pagination provider.

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
        """Paginate query results using offset-based pagination.

        Args:
            query: SQLAlchemy select query
            params: Pagination parameters
            transform_func: Optional function to transform each result item

        Returns:
            Paginated results

        Raises:
            ValidationException: If pagination parameters are invalid
        """
        # Count total items
        total = await count_query(self.db, query)

        # Calculate pagination metadata
        page = params.page
        page_size = params.page_size
        pages = (total + page_size - 1) // page_size if total > 0 else 0

        if page > pages > 0:
            page = pages

        # Apply sorting
        if params.sort:
            query = self._apply_sorting(query, params.sort)

        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # Execute query
        result = await execute_query(self.db, query)
        items = list(result.scalars().all())

        # Transform items if needed
        transformed_items: List[Any] = items
        if transform_func:
            transformed_items = [transform_func(item) for item in items]

        # Create pagination result
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
        """Not supported by this provider - use CursorPaginationProvider instead.

        Raises:
            NotImplementedError: Always
        """
        raise NotImplementedError(
            "Cursor-based pagination is not supported by OffsetPaginationProvider. "
            "Use CursorPaginationProvider instead."
        )

    def _apply_sorting(self, query: Select, sort_fields: List[SortField]) -> Select:
        """Apply sorting to a query.

        Args:
            query: SQLAlchemy query
            sort_fields: Fields to sort by

        Returns:
            Query with sorting applied

        Raises:
            ValidationException: If sort field is invalid
        """
        for sort_field in sort_fields:
            field_name = sort_field.field

            # Get column to sort by
            if not hasattr(self.model_class, field_name):
                raise ValidationException(
                    message=f"Invalid sort field: {field_name}",
                    details=[
                        {
                            "loc": ["sort", "field"],
                            "msg": f"Invalid sort field: {field_name}",
                            "type": "value_error.sort_field",
                        }
                    ],
                )

            column = getattr(self.model_class, field_name)

            # Apply sort direction
            if sort_field.direction == SortDirection.DESC:
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))

        return query
