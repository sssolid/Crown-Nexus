# app/core/exceptions/handlers.py
from __future__ import annotations

"""
Exception handlers for the application.

This module defines handlers for different types of exceptions that can occur
in the application, mapping them to appropriate HTTP responses.
"""

import datetime
import traceback
from typing import Dict, Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.core.exceptions.base import (
    AppException,
    ErrorCode,
    ErrorDetail,
    ErrorResponse,
    ErrorSeverity,
)
from app.logging.context import get_logger

logger = get_logger("app.core.exceptions.handlers")


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle application exceptions.

    Args:
        request: The request that caused the exception
        exc: The application exception

    Returns:
        A formatted JSON response with error details
    """
    request_id = getattr(request.state, "request_id", None)

    # Log the exception
    exc.log(request_id=request_id)

    # Create response
    error_response = exc.to_response(request_id=request_id)
    error_response.timestamp = datetime.datetime.now(datetime.UTC).isoformat()

    # Extract any custom headers from details
    headers: Dict[str, str] = {}
    if isinstance(exc.details, dict) and "headers" in exc.details:
        headers = exc.details["headers"]

    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(error_response),
        headers=headers,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle validation exceptions.

    Args:
        request: The request that caused the exception
        exc: The validation exception

    Returns:
        A formatted JSON response with validation error details
    """
    request_id = getattr(request.state, "request_id", None)

    # Format validation errors
    errors = []
    for error in exc.errors():
        errors.append(
            ErrorDetail(
                loc=list(map(str, error["loc"])), msg=error["msg"], type=error["type"]
            )
        )

    # Create response
    error_response = ErrorResponse(
        success=False,
        message="Validation error",
        code=ErrorCode.VALIDATION_ERROR,
        details=errors,
        meta={"request_id": request_id, "severity": ErrorSeverity.WARNING},
        timestamp=datetime.datetime.now(datetime.UTC).isoformat(),
    )

    # Log validation errors
    logger.warning(
        f"Validation error: {len(errors)} validation errors",
        request_id=request_id,
        path=request.url.path,
        validation_errors=[
            {"loc": e.loc, "msg": e.msg, "type": e.type} for e in errors
        ],
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(error_response),
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle generic exceptions.

    Args:
        request: The request that caused the exception
        exc: The unhandled exception

    Returns:
        A formatted JSON response with error details
    """
    request_id = getattr(request.state, "request_id", None)

    # Log the unhandled exception
    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=exc,
        request_id=request_id,
        path=request.url.path,
    )

    # Configure error details based on environment
    from app.core.config import settings, Environment

    error_message = "An unexpected error occurred"
    error_details: Any = None

    if settings.ENVIRONMENT != Environment.PRODUCTION:
        error_message = f"Unhandled error: {str(exc)}"
        error_details = [
            {"loc": ["server"], "msg": str(exc), "type": "unhandled_error"}
        ]

        # Include traceback in development
        if settings.ENVIRONMENT == Environment.DEVELOPMENT:
            trace = traceback.format_exception(type(exc), exc, exc.__traceback__)
            error_details[0]["traceback"] = trace

    # Create response
    error_response = ErrorResponse(
        success=False,
        message=error_message,
        code=ErrorCode.UNKNOWN_ERROR,
        details=error_details or [],
        meta={"request_id": request_id, "severity": ErrorSeverity.ERROR},
        timestamp=datetime.datetime.now(datetime.UTC).isoformat(),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(error_response),
    )
