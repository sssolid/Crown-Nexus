# /app/core/pagination/base.py
from __future__ import annotations

"""
Base interfaces and types for the pagination system.

This module defines common types, protocols, and interfaces
used throughout the pagination components.
"""

from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar

from pydantic import BaseModel, Field
from sqlalchemy.sql import Select

# Type variables
T = TypeVar("T")  # Entity type
R = TypeVar("R")  # Result type


class SortDirection(str, Enum):
    """Sort direction options."""

    ASC = "asc"
    DESC = "desc"


class SortField(BaseModel):
    """Model for sort field configuration."""

    field: str
    direction: SortDirection = SortDirection.ASC


class OffsetPaginationParams(BaseModel):
    """Parameters for offset-based pagination."""

    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(20, ge=1, le=100, description="Number of items per page")
    sort: Optional[List[SortField]] = Field(None, description="Fields to sort by")


class CursorPaginationParams(BaseModel):
    """Parameters for cursor-based pagination."""

    cursor: Optional[str] = Field(None, description="Pagination cursor")
    limit: int = Field(
        20, ge=1, le=100, description="Maximum number of items to return"
    )
    sort: Optional[List[SortField]] = Field(None, description="Fields to sort by")


class PaginationResult(Generic[R]):
    """Result of a pagination operation."""

    def __init__(
        self,
        items: List[R],
        total: int = 0,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        pages: Optional[int] = None,
        next_cursor: Optional[str] = None,
        has_next: bool = False,
        has_prev: bool = False,
    ) -> None:
        """Initialize the pagination result.

        Args:
            items: List of items for the current page
            total: Total number of items (across all pages)
            page: Current page number (for offset pagination)
            page_size: Number of items per page (for offset pagination)
            pages: Total number of pages (for offset pagination)
            next_cursor: Cursor for fetching the next page (for cursor pagination)
            has_next: Whether there are more items after this page
            has_prev: Whether there are more items before this page
        """
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.pages = pages
        self.next_cursor = next_cursor
        self.has_next = has_next
        self.has_prev = has_prev

    def to_dict(self) -> Dict[str, Any]:
        """Convert the pagination result to a dictionary.

        Returns:
            Dictionary representation of the pagination result
        """
        result = {
            "items": self.items,
            "total": self.total,
            "has_next": self.has_next,
            "has_prev": self.has_prev,
        }

        # Add offset pagination fields
        if self.page is not None:
            result["page"] = self.page
        if self.page_size is not None:
            result["page_size"] = self.page_size
        if self.pages is not None:
            result["pages"] = self.pages

        # Add cursor pagination fields
        if self.next_cursor is not None:
            result["next_cursor"] = self.next_cursor

        return result


class PaginationProvider(Protocol, Generic[T, R]):
    """Protocol for pagination providers."""

    async def paginate_with_offset(
        self,
        query: Select,
        params: OffsetPaginationParams,
        transform_func: Optional[callable] = None,
    ) -> PaginationResult[R]:
        """Paginate query results using offset-based pagination.

        Args:
            query: SQLAlchemy select query
            params: Pagination parameters
            transform_func: Optional function to transform each result item

        Returns:
            Paginated results
        """
        ...

    async def paginate_with_cursor(
        self,
        query: Select,
        params: CursorPaginationParams,
        transform_func: Optional[callable] = None,
    ) -> PaginationResult[R]:
        """Paginate query results using cursor-based pagination.

        Args:
            query: SQLAlchemy select query
            params: Pagination parameters
            transform_func: Optional function to transform each result item

        Returns:
            Paginated results
        """
        ...
