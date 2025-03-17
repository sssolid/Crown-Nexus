# app/middleware/error_handler.py
from __future__ import annotations

import traceback
from datetime import datetime
from typing import Callable, Dict, Optional

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.dependency_manager import get_dependency
from app.core.exceptions import (
    AppException,
    ErrorCategory,
    ErrorCode,
    ErrorResponse,
    ErrorSeverity,
)
from app.core.logging import get_logger
from app.services.error_handling_service import ErrorContext, ErrorHandlingService

logger = get_logger("app.middleware.error_handler")


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling exceptions across the application.

    Provides consistent error handling and reporting for all exceptions
    that occur during request processing.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and handle any exceptions.

        Args:
            request: The request to process
            call_next: The next middleware or route handler

        Returns:
            Response object
        """
        try:
            # Get error handling service
            error_service: Optional[ErrorHandlingService] = None
            try:
                error_service = get_dependency("error_handling_service")
            except Exception:
                # If dependency manager is not available, continue without error service
                pass

            # Process the request
            return await call_next(request)

        except AppException as exc:
            # Handle application exceptions
            request_id = getattr(request.state, "request_id", None)

            # Report the exception if error service is available
            if error_service:
                context = ErrorContext(
                    request_id=request_id,
                    path=request.url.path,
                    method=request.method
                )
                await error_service.report_error(exc, context)

            # Convert to response
            error_response = exc.to_response(request_id)

            return JSONResponse(
                status_code=exc.status_code,
                content=error_response.dict()
            )

        except RequestValidationError as exc:
            # Handle request validation errors
            request_id = getattr(request.state, "request_id", None)

            # Report the exception if error service is available
            if error_service:
                context = ErrorContext(
                    request_id=request_id,
                    path=request.url.path,
                    method=request.method
                )
                await error_service.report_error(exc, context)

            # Convert validation errors to a standard format
            error_details = []
            for error in exc.errors():
                error_details.append({
                    "loc": list(error["loc"]),
                    "msg": error["msg"],
                    "type": error["type"]
                })

            error_response = ErrorResponse(
                success=False,
                message="Validation error",
                code=ErrorCode.VALIDATION_ERROR,
                data=None,
                details=error_details,
                meta={"request_id": request_id, "severity": ErrorSeverity.WARNING, "category": ErrorCategory.VALIDATION},
                timestamp=datetime.utcnow().isoformat()
            )

            return JSONResponse(
                status_code=422,
                content=error_response.dict()
            )

        except Exception as exc:
            # Handle all other exceptions
            request_id = getattr(request.state, "request_id", None)

            # Report the exception if error service is available
            if error_service:
                context = ErrorContext(
                    request_id=request_id,
                    path=request.url.path,
                    method=request.method
                )
                await error_service.report_error(exc, context)

            # Get the error response
            if error_service:
                error_response = error_service.handle_exception(exc, request_id)
            else:
                # Fallback if error service is not available
                error_response = ErrorResponse(
                    success=False,
                    message="An unexpected error occurred",
                    code=ErrorCode.UNKNOWN_ERROR,
                    data=None,
                    details=[{
                        "loc": ["server"],
                        "msg": str(exc),
                        "type": "server_error"
                    }],
                    meta={"request_id": request_id, "error_type": exc.__class__.__name__},
                    timestamp=datetime.utcnow().isoformat()
                )

            # Log the error
            logger.error(
                f"Unhandled exception: {str(exc)}",
                exc_info=exc,
                request_id=request_id,
                path=request.url.path,
                method=request.method
            )

            return JSONResponse(
                status_code=500,
                content=error_response.dict()
            )
