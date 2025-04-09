# processed_project/backend_stripped/app/schemas/responses.py
from __future__ import annotations

"""API response schemas.

This module defines standardized response formats for API endpoints.
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class ResponseBase(BaseModel):
    """Base response model with standard fields."""

    success: bool = True
    message: str
    code: int
    meta: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None


class Response(ResponseBase, Generic[T]):
    """Standard API response with optional data."""

    data: Optional[T] = None
    pagination: Optional[Dict[str, Any]] = None

    @classmethod
    def success(
        cls,
        data: Optional[Any] = None,
        message: str = "Request successful",
        code: int = 200,
        meta: Optional[Dict[str, Any]] = None,
        pagination: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> Response:
        """Create a success response.

        Args:
            data: Response data
            message: Response message
            code: HTTP status code
            meta: Additional metadata
            pagination: Pagination information
            request_id: Request identifier

        Returns:
            Response: Success response instance
        """
        return cls(
            success=True,
            message=message,
            code=code,
            data=data,
            meta=meta,
            pagination=pagination,
            request_id=request_id,
        )

    @classmethod
    def error(
        cls,
        message: str,
        code: int = 400,
        data: Optional[Any] = None,
        meta: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> Response:
        """Create an error response.

        Args:
            message: Error message
            code: HTTP status code
            data: Optional error data
            meta: Additional metadata
            request_id: Request identifier

        Returns:
            Response: Error response instance
        """
        return cls(
            success=False,
            message=message,
            code=code,
            data=data,
            meta=meta,
            request_id=request_id,
        )


class PaginatedResponse(ResponseBase, Generic[T]):
    """Paginated API response."""

    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def from_pagination_result(
        cls,
        items: List[Any],
        pagination: Dict[str, Any],
        message: str = "Request successful",
        code: int = 200,
        meta: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> PaginatedResponse:
        """Create a paginated response from pagination result.

        Args:
            items: List of items
            pagination: Pagination information
            message: Response message
            code: HTTP status code
            meta: Additional metadata
            request_id: Request identifier

        Returns:
            PaginatedResponse: Paginated response instance
        """
        return cls(
            success=True,
            message=message,
            code=code,
            items=items,
            total=pagination.get("total", 0),
            page=pagination.get("page", 1),
            page_size=pagination.get("page_size", len(items)),
            pages=pagination.get("pages", 1),
            meta=meta,
            request_id=request_id,
        )
