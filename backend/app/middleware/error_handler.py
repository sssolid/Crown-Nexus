# app/middleware/error_handler.py
from __future__ import annotations

"""
Error handler middleware for the application.

This middleware catches exceptions and routes them to the appropriate handlers,
ensuring consistent error responses across the application.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.error import handle_exception
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    generic_exception_handler,
)
from app.logging.context import get_logger

logger = get_logger("app.middleware.error_handler")


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling exceptions and converting them to standardized responses.

    This middleware catches all exceptions, logs them, and passes them to the
    appropriate exception handler for creating consistent error responses.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and handle any exceptions.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            Either the response from downstream middleware or an error response
        """
        try:
            return await call_next(request)
        except AppException as exc:
            # For AppExceptions, use their built-in logging and handling
            request_id = getattr(request.state, "request_id", None)
            handle_exception(exc, request_id)
            return await app_exception_handler(request, exc)
        except Exception as exc:
            # For unexpected exceptions, log and use the generic handler
            request_id = getattr(request.state, "request_id", None)
            logger.exception(
                f"Unhandled exception: {str(exc)}",
                exc_info=exc,
                request_id=request_id,
                path=request.url.path,
            )
            handle_exception(exc, request_id)
            return await generic_exception_handler(request, exc)
