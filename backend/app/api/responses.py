# app/api/responses.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, TypeVar

from app.schemas.responses import Response, PaginatedResponse
from fastapi import status
from fastapi.responses import JSONResponse

T = TypeVar("T")


def success_response(
    data: Optional[Any] = None,
    message: str = "Request successful",
    code: int = status.HTTP_200_OK,
    meta: Optional[Dict[str, Any]] = None,
    pagination: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None,
) -> JSONResponse:
    """Create a success response.

    Args:
        data: Response data
        message: Success message
        code: HTTP status code
        meta: Additional metadata
        pagination: Pagination metadata
        request_id: Request ID for tracking

    Returns:
        JSONResponse: Success response
    """
    response = Response.success(
        data=data,
        message=message,
        code=code,
        meta=meta,
        pagination=pagination,
        request_id=request_id,
    )

    json_response = JSONResponse(
        content=response.dict(),
        status_code=code,
    )
    setattr(json_response, "is_formatted", True)

    return json_response


def error_response(
    message: str,
    code: int = status.HTTP_400_BAD_REQUEST,
    data: Optional[Any] = None,
    meta: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None,
) -> JSONResponse:
    """Create an error response.

    Args:
        message: Error message
        code: HTTP status code
        data: Error data
        meta: Additional metadata
        request_id: Request ID for tracking

    Returns:
        JSONResponse: Error response
    """
    response = Response.error(
        message=message,
        code=code,
        data=data,
        meta=meta,
        request_id=request_id,
    )

    json_response = JSONResponse(
        content=response.dict(),
        status_code=code,
    )
    setattr(json_response, "is_formatted", True)

    return json_response


def paginated_response(
    items: List[Any],
    pagination: Dict[str, Any],
    message: str = "Request successful",
    code: int = status.HTTP_200_OK,
    meta: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None,
) -> JSONResponse:
    """Create a paginated response.

    Args:
        items: List of items
        pagination: Pagination metadata
        message: Success message
        code: HTTP status code
        meta: Additional metadata
        request_id: Request ID for tracking

    Returns:
        JSONResponse: Paginated response
    """
    response = PaginatedResponse.from_pagination_result(
        items=items,
        pagination=pagination,
        message=message,
        code=code,
        meta=meta,
        request_id=request_id,
    )

    json_response = JSONResponse(
        content=response.dict(),
        status_code=code,
    )
    setattr(json_response, "is_formatted", True)

    return json_response


def created_response(
    data: Optional[Any] = None,
    message: str = "Resource created successfully",
    meta: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None,
) -> JSONResponse:
    """Create a 201 Created response.

    Args:
        data: Response data
        message: Success message
        meta: Additional metadata
        request_id: Request ID for tracking

    Returns:
        JSONResponse: Created response
    """
    return success_response(
        data=data,
        message=message,
        code=status.HTTP_201_CREATED,
        meta=meta,
        request_id=request_id,
    )


def no_content_response() -> JSONResponse:
    """Create a 204 No Content response.

    Returns:
        JSONResponse: No content response
    """
    return success_response(
        message="No content",
        code=status.HTTP_204_NO_CONTENT,
    )
