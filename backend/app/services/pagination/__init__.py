# /app/services/pagination/__init__.py
from __future__ import annotations

"""Pagination service package for application-wide pagination functionality.

This package provides services for paginating query results using both
offset-based and cursor-based pagination strategies.
"""

from app.services.pagination.base import (
    CursorPaginationParams,
    OffsetPaginationParams,
    PaginationResult,
    SortDirection,
    SortField
)
from app.services.pagination.service import PaginationService

# Factory function for dependency injection
def get_pagination_service(db, model_class, response_model=None):
    """Factory function to get PaginationService

    Args:
        db: Database session
        model_class: SQLAlchemy model class
        response_model: Optional Pydantic response model

    Returns:
        PaginationService instance
    """
    return PaginationService(db, model_class, response_model)


__all__ = [
    "get_pagination_service",
    "PaginationService",
    "PaginationResult",
    "OffsetPaginationParams",
    "CursorPaginationParams",
    "SortDirection",
    "SortField"
]
