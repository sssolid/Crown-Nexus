# /app/core/pagination/providers/cursor.py
from __future__ import annotations

"""Cursor-based pagination provider implementation.

This module provides a pagination provider that uses cursor-based pagination,
which is suitable for large datasets and continuous scrolling interfaces.
"""

import base64
import json
from datetime import datetime
import uuid
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, cast

from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select

from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.db.utils import count_query, execute_query
from app.core.pagination.base import (
    CursorPaginationParams,
    PaginationProvider,
    PaginationResult,
    SortDirection,
    SortField,
)

logger = get_logger("app.core.pagination.providers.cursor")

T = TypeVar("T")  # Entity type
R = TypeVar("R")  # Result type


class CursorPaginationProvider(Generic[T, R], PaginationProvider[T, R]):
    """Provider for cursor-based pagination."""

    def __init__(self, db: AsyncSession, model_class: type[DeclarativeMeta]) -> None:
        """Initialize the cursor pagination provider.

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
        params: Any,
        transform_func: Optional[Callable[[T], R]] = None,
    ) -> PaginationResult[R]:
        """Not supported by this provider - use OffsetPaginationProvider instead.

        Raises:
            NotImplementedError: Always
        """
        raise NotImplementedError(
            "Offset-based pagination is not supported by CursorPaginationProvider. "
            "Use OffsetPaginationProvider instead."
        )

    async def paginate_with_cursor(
        self,
        query: Select,
        params: CursorPaginationParams,
        transform_func: Optional[Callable[[T], R]] = None,
    ) -> PaginationResult[R]:
        """Paginate query results using cursor-based pagination.

        Args:
            query: SQLAlchemy select query
            params: Pagination parameters
            transform_func: Optional function to transform each result item

        Returns:
            Paginated results

        Raises:
            ValidationException: If pagination parameters are invalid
        """
        # Ensure we have at least one sort field
        sort_fields = params.sort or [
            SortField(field="id", direction=SortDirection.ASC)
        ]

        # Decode cursor if provided
        cursor_values = None
        if params.cursor:
            try:
                cursor_values = self._decode_cursor(params.cursor)
            except Exception as e:
                logger.warning(f"Invalid cursor: {str(e)}")
                raise ValidationException(
                    message="Invalid cursor format",
                    details=[
                        {
                            "loc": ["cursor"],
                            "msg": "Invalid cursor format",
                            "type": "value_error.cursor_format",
                        }
                    ],
                )

        # Store original query for counting if needed
        original_query = query

        # Apply filter based on cursor
        if cursor_values:
            query = self._apply_cursor_filter(query, sort_fields, cursor_values)

        # Apply sorting
        query = self._apply_sorting(query, sort_fields)

        # Apply limit
        query = query.limit(params.limit + 1)  # +1 to check if there are more items

        # Execute query
        result = await execute_query(self.db, query)
        items = list(result.scalars().all())

        # Count total (only for the first page)
        total = 0
        if not params.cursor:
            total = await count_query(self.db, original_query)

        # Check if there are more items
        has_next = len(items) > params.limit
        if has_next:
            items = items[: params.limit]  # Remove the extra item

        # Generate next cursor
        next_cursor = None
        if has_next and items:
            next_cursor = self._encode_cursor(items[-1], sort_fields)

        # Transform items if needed
        transformed_items: List[Any] = items
        if transform_func:
            transformed_items = [transform_func(item) for item in items]

        # Create pagination result
        return PaginationResult[R](
            items=cast(List[R], transformed_items),
            total=total,
            next_cursor=next_cursor,
            has_next=has_next,
            has_prev=bool(params.cursor),
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

    def _apply_cursor_filter(
        self,
        query: Select,
        sort_fields: List[SortField],
        cursor_values: Dict[str, Any],
    ) -> Select:
        """Apply cursor-based filtering to a query.

        Args:
            query: SQLAlchemy query
            sort_fields: Fields used for sorting
            cursor_values: Values from cursor

        Returns:
            Query with cursor filter applied

        Raises:
            ValidationException: If cursor field is invalid
        """
        # Build a filter condition based on sort fields and cursor values
        conditions = []
        for i, sort_field in enumerate(sort_fields):
            field_name = sort_field.field

            # Ensure field exists in cursor values
            if field_name not in cursor_values:
                continue

            # Get column and value
            if not hasattr(self.model_class, field_name):
                raise ValidationException(
                    message=f"Invalid cursor field: {field_name}",
                    details=[
                        {
                            "loc": ["cursor", "field"],
                            "msg": f"Invalid cursor field: {field_name}",
                            "type": "value_error.cursor_field",
                        }
                    ],
                )

            column = getattr(self.model_class, field_name)
            value = cursor_values[field_name]

            # Create condition based on sort direction
            if i == 0:
                # First field uses > or < depending on sort direction
                if sort_field.direction == SortDirection.ASC:
                    conditions.append(column > value)
                else:
                    conditions.append(column < value)
            else:
                # Subsequent fields use equality for previous fields
                previous_field = sort_fields[i - 1].field
                previous_column = getattr(self.model_class, previous_field)
                previous_value = cursor_values[previous_field]

                # Add condition for equality on previous field
                conditions.append(previous_column == previous_value)

                # Add condition for current field
                if sort_field.direction == SortDirection.ASC:
                    conditions.append(column > value)
                else:
                    conditions.append(column < value)

        # Apply conditions to query
        if conditions:
            query = query.where(*conditions)

        return query

    def _encode_cursor(self, item: T, sort_fields: List[SortField]) -> str:
        """Encode a cursor from an item.

        Args:
            item: Item to encode
            sort_fields: Fields used for sorting

        Returns:
            str: Encoded cursor
        """
        cursor_data = {}

        for sort_field in sort_fields:
            field_name = sort_field.field

            if not hasattr(item, field_name):
                continue

            value = getattr(item, field_name)

            # Handle special types
            if isinstance(value, (datetime, uuid.UUID)):
                value = str(value)

            cursor_data[field_name] = value

        # Encode cursor as base64
        cursor_json = json.dumps(cursor_data)
        return base64.b64encode(cursor_json.encode("utf-8")).decode("utf-8")

    def _decode_cursor(self, cursor: str) -> Dict[str, Any]:
        """Decode a cursor into values.

        Args:
            cursor: Encoded cursor

        Returns:
            Dict[str, Any]: Decoded cursor values

        Raises:
            ValueError: If cursor format is invalid
        """
        try:
            cursor_json = base64.b64decode(cursor.encode("utf-8")).decode("utf-8")
            return json.loads(cursor_json)
        except Exception as e:
            raise ValueError(f"Invalid cursor format: {str(e)}")
