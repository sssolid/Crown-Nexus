# /app/core/pagination/__init__.py
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
from app.core.pagination.manager import (
    initialize,
    shutdown,
    paginate_with_offset,
    paginate_with_cursor,
)

__all__ = [
    # Base types
    "PaginationResult",
    "OffsetPaginationParams",
    "CursorPaginationParams",
    "SortDirection",
    "SortField",
    # Core functions
    "initialize",
    "shutdown",
    "paginate_with_offset",
    "paginate_with_cursor",
]
