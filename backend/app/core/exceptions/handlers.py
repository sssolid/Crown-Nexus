# /backend/app/core/exceptions/handlers.py
from __future__ import annotations

"""Exception handlers for the application.

This module defines handlers for different types of exceptions that can occur
in the application, mapping them to appropriate HTTP responses.
"""

import traceback
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from app.core.exceptions.base import (
    AppException,
    ErrorCode,
    ErrorDetail,
    ErrorResponse,
    ErrorSeverity,
)
from app.core.logging import get_logger

logger = get_logger("app.core.exceptions.handlers")


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application-specific exceptions.

    Converts AppException instances to standardized error responses with
    appropriate status codes.

    Args:
        request: FastAPI request object
        exc: Application exception

    Returns:
        JSONResponse with standardized error format
    """
    # Get request ID from state if available
    request_id = getattr(request.state, "request_id", None)

    # Log the exception
    exc.log(request_id=request_id)

    # Convert to error response model
    error_response = exc.to_response(request_id=request_id)

    # Add timestamp
    error_response.timestamp = datetime.utcnow().isoformat()

    # Return JSON response with appropriate status code
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(error_response),
        headers=exc.details.get("headers", {}) if isinstance(exc.details, dict) else {},
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors from FastAPI and Pydantic.

    Converts validation errors to a standardized format with details
    about each validation error.

    Args:
        request: FastAPI request object
        exc: Validation exception

    Returns:
        JSONResponse with standardized error format
    """
    # Get request ID from state if available
    request_id = getattr(request.state, "request_id", None)

    # Extract error details
    errors = []
    for error in exc.errors():
        errors.append(
            ErrorDetail(
                loc=list(map(str, error["loc"])),
                msg=error["msg"],
                type=error["type"],
            )
        )

    # Create error response
    error_response = ErrorResponse(
        success=False,
        message="Validation error",
        code=ErrorCode.VALIDATION_ERROR,
        details=errors,
        meta={"request_id": request_id, "severity": ErrorSeverity.WARNING},
        timestamp=datetime.utcnow().isoformat(),
    )

    # Log the error
    logger.warning(
        f"Validation error: {len(errors)} validation errors",
        extra={
            "request_id": request_id,
            "path": request.url.path,
            "validation_errors": [
                {"loc": e.loc, "msg": e.msg, "type": e.type}
                for e in errors
            ],
        },
    )

    # Return JSON response
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(error_response),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions.

    Converts any unhandled exception to a standardized error response
    with a 500 status code.

    Args:
        request: FastAPI request object
        exc: Unhandled exception

    Returns:
        JSONResponse with standardized error format
    """
    # Get request ID from state if available
    request_id = getattr(request.state, "request_id", None)

    # Log the error
    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=exc,
        extra={"request_id": request_id, "path": request.url.path},
    )

    # In production, hide the actual error details for security
    from app.core.config import settings, Environment

    error_message = "An unexpected error occurred"
    error_details = None

    if settings.ENVIRONMENT != Environment.PRODUCTION:
        # In non-production environments, include more error details
        error_message = f"Unhandled error: {str(exc)}"
        error_details = [{
            "loc": ["server"],
            "msg": str(exc),
            "type": "unhandled_error",
        }]

        # Add traceback in development environment
        if settings.ENVIRONMENT == Environment.DEVELOPMENT:
            trace = traceback.format_exception(
                type(exc), exc, exc.__traceback__
            )
            error_details[0]["traceback"] = trace

    # Create error response
    error_response = ErrorResponse(
        success=False,
        message=error_message,
        code=ErrorCode.UNKNOWN_ERROR,
        details=error_details or [],
        meta={
            "request_id": request_id,
            "severity": ErrorSeverity.ERROR,
        },
        timestamp=datetime.utcnow().isoformat(),
    )

    # Return JSON response
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(error_response),
    )
