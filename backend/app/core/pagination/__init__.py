# app/core/pagination/__init__.py
from __future__ import annotations

"""Pagination package for application-wide pagination functionality.

This package provides core functionality for paginating query results using both
offset-based and cursor-based pagination strategies.
"""

from app.core.pagination.base import (
    CursorPaginationParams,
    OffsetPaginationParams,
    PaginationResult,
    SortDirection,
    SortField,
)
from app.core.pagination.exceptions import (
    InvalidCursorException,
    InvalidPaginationParamsException,
    InvalidSortFieldException,
    PaginationException,
)
from app.core.pagination.manager import (
    initialize,
    paginate_with_cursor,
    paginate_with_offset,
    shutdown,
)
from app.core.pagination.service import PaginationService, get_pagination_service

__all__ = [
    "PaginationResult",
    "OffsetPaginationParams",
    "CursorPaginationParams",
    "SortDirection",
    "SortField",
    "initialize",
    "shutdown",
    "paginate_with_offset",
    "paginate_with_cursor",
    "PaginationService",
    "get_pagination_service",
    "PaginationException",
    "InvalidPaginationParamsException",
    "InvalidCursorException",
    "InvalidSortFieldException",
]
