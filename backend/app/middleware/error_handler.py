from __future__ import annotations

"""
Enhanced error handler middleware for the application.

This middleware catches exceptions and routes them to the appropriate handlers,
ensuring consistent error responses across the application and preventing
infinite middleware loops.
"""

import time
import sys
import traceback
from typing import Callable, Any, Optional, Dict, Type
from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.error import handle_exception
from app.core.exceptions import (
    AppException,
    ErrorCode,
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.logging.context import get_logger
from app.core.dependency_manager import get_service
from app.utils.circuit_breaker_utils import safe_increment_counter

logger = get_logger("app.middleware.error_handler")

ERROR_TYPE_MAPPING: Dict[Type[Exception], ErrorCode] = {
    RequestValidationError: ErrorCode.VALIDATION_ERROR,
    ValueError: ErrorCode.VALIDATION_ERROR,
    TypeError: ErrorCode.VALIDATION_ERROR,
}


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions and provide consistent error responses."""

    def __init__(self, app: Any) -> None:
        """
        Initialize the error handler middleware.

        Args:
            app: The ASGI application
        """
        super().__init__(app)
        logger.info("ErrorHandlerMiddleware initialized")

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """
        Process the request and handle any exceptions.

        Args:
            request: The incoming request
            call_next: Function to call the next middleware

        Returns:
            Response: The response, or an error response if an exception occurred
        """
        metrics_service: Optional[Any] = None
        try:
            metrics_service = get_service("metrics_service")
        except Exception:
            pass

        start_time = time.time()
        error_type = None
        status_code = None

        # Set up a flag to prevent infinite recursion in case of errors
        # in the error handling process itself
        if hasattr(request.state, "_error_handler_active"):
            logger.error("Detected recursive error handling - bypassing error handler")
            try:
                # Last resort attempt to return something rather than crash
                return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "message": "Internal Server Error",
                        "error": {
                            "code": "RECURSIVE_ERROR",
                            "details": "Error occurred during error handling",
                        },
                    },
                )
            except Exception:
                # If even creating the JSONResponse fails, return a plain 500
                return Response(
                    content="Internal Server Error",
                    status_code=500,
                    media_type="text/plain",
                )

        # Mark that we're inside the error handler
        setattr(request.state, "_error_handler_active", True)

        try:
            try:
                # Process the request
                return await call_next(request)
            except AppException as exc:
                # Handle application-specific exceptions
                execution_time = time.time() - start_time
                request_id = getattr(request.state, "request_id", None)
                user_id = getattr(request.state, "user_id", None)
                path = request.url.path
                method = request.method
                error_type = type(exc).__name__
                status_code = exc.status_code

                logger.warning(
                    f"Application exception: {str(exc)}",
                    exc_info=exc,
                    request_id=request_id,
                    path=path,
                    method=method,
                    error_code=exc.code.value if hasattr(exc, "code") else None,
                    status_code=exc.status_code,
                    details=exc.details,
                    execution_time=f"{execution_time:.4f}s",
                )

                handle_exception(
                    exc, request_id=request_id, user_id=user_id, function_name=method
                )
                self._track_error_metrics(
                    metrics_service,
                    error_type,
                    status_code,
                    request.method,
                    request.url.path,
                )

                return await app_exception_handler(request, exc)

            except RequestValidationError as exc:
                # Handle validation errors
                execution_time = time.time() - start_time
                request_id = getattr(request.state, "request_id", None)
                user_id = getattr(request.state, "user_id", None)
                path = request.url.path
                method = request.method
                error_type = type(exc).__name__
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

                logger.warning(
                    f"Validation error: {str(exc)}",
                    exc_info=exc,
                    request_id=request_id,
                    path=path,
                    method=method,
                    error_code=ErrorCode.VALIDATION_ERROR.value,
                    status_code=status_code,
                    errors=str(exc.errors()) if hasattr(exc, "errors") else None,
                    execution_time=f"{execution_time:.4f}s",
                )

                handle_exception(
                    exc, request_id=request_id, user_id=user_id, function_name=method
                )
                self._track_error_metrics(
                    metrics_service,
                    error_type,
                    status_code,
                    request.method,
                    request.url.path,
                )

                return await validation_exception_handler(request, exc)

            except Exception as exc:
                # Handle all other exceptions
                execution_time = time.time() - start_time
                request_id = getattr(request.state, "request_id", None)
                user_id = getattr(request.state, "user_id", None)
                path = request.url.path
                method = request.method
                error_type = type(exc).__name__
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_code = ERROR_TYPE_MAPPING.get(type(exc), ErrorCode.SERVER_ERROR)

                # Get full traceback for better debugging
                exc_info = sys.exc_info()
                tb_str = "".join(traceback.format_exception(*exc_info))

                logger.exception(
                    f"Unhandled exception: {str(exc)}",
                    exc_info=exc,
                    traceback=tb_str,
                    request_id=request_id,
                    path=path,
                    method=method,
                    error_code=error_code.value,
                    status_code=status_code,
                    execution_time=f"{execution_time:.4f}s",
                )

                handle_exception(
                    exc, request_id=request_id, user_id=user_id, function_name=method
                )
                self._track_error_metrics(
                    metrics_service,
                    error_type,
                    status_code,
                    request.method,
                    request.url.path,
                )

                return await generic_exception_handler(request, exc)

        except Exception as nested_exc:
            # Handle exceptions that occur during error handling
            logger.critical(
                f"Exception occurred during error handling: {str(nested_exc)}",
                exc_info=nested_exc,
            )

            # Return a simple error response as a last resort
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Internal Server Error",
                    "error": {
                        "code": "ERROR_HANDLER_FAILURE",
                        "details": "An error occurred during error handling",
                    },
                },
            )
        finally:
            # Clean up the error handler flag to prevent state leakage
            if hasattr(request.state, "_error_handler_active"):
                delattr(request.state, "_error_handler_active")

    def _track_error_metrics(
        self,
        metrics_service: Optional[Any],
        error_type: str,
        status_code: int,
        method: str,
        path: str,
    ) -> None:
        """
        Track error metrics.

        Args:
            metrics_service: The metrics service
            error_type: The type of error
            status_code: The HTTP status code
            method: The HTTP method
            path: The request path
        """
        if not metrics_service:
            return

        try:
            safe_increment_counter(
                "http_errors_total",
                1,
                {
                    "error_type": error_type,
                    "status_code": str(status_code),
                    "method": method,
                    "endpoint": path,
                },
            )
        except Exception as e:
            logger.debug(f"Failed to track error metrics: {e}")
