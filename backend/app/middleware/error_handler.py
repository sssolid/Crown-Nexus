from __future__ import annotations
import traceback
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
    app_exception_handler,
    generic_exception_handler,
)
from app.core.logging import get_logger

logger = get_logger("app.middleware.error_handler")


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling exceptions across the application."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process the request and handle any exceptions."""
        # Get error service
        error_service = get_dependency("error_service")

        try:
            # Process the request
            return await call_next(request)
        except AppException as exc:
            # Application exceptions are already structured
            error_service.handle_exception(exc, request.headers.get("X-Request-ID"))
            return await app_exception_handler(request, exc)
        except Exception as exc:
            # Unexpected exceptions
            error_service.handle_exception(exc, request.headers.get("X-Request-ID"))
            return await generic_exception_handler(request, exc)
