# app/middleware/error_handler.py
from __future__ import annotations

import traceback
from typing import Callable, Optional

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import AppException, ErrorCode, ErrorResponse
from app.core.logging import get_logger


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling unhandled exceptions.
    
    This middleware catches any unhandled exceptions and returns a standardized
    error response.
    """

    def __init__(self, app: FastAPI) -> None:
        """Initialize the middleware.
        
        Args:
            app: FastAPI application
        """
        super().__init__(app)
        self.logger = get_logger("app.middleware.error_handler")

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """Process the request and catch any unhandled exceptions.
        
        Args:
            request: FastAPI request
            call_next: Next middleware in the chain
            
        Returns:
            Response: HTTP response
        """
        try:
            return await call_next(request)
        except Exception as exc:
            # Skip if it's already an AppException (will be handled by its handler)
            if isinstance(exc, AppException):
                raise
            
            # Get request ID from context if available
            request_id = getattr(request.state, "request_id", None)
            
            # Log the exception with traceback
            self.logger.error(
                f"Unhandled exception in request: {str(exc)}",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "method": request.method,
                    "exception_type": exc.__class__.__name__,
                    "exception_message": str(exc),
                },
            )
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
            
            # Create a generic error response
            error_response = ErrorResponse(
                code=ErrorCode.UNKNOWN_ERROR,
                message="An unexpected error occurred",
                request_id=request_id,
            )
            
            # Return a JSON response with 500 status code
            return JSONResponse(
                status_code=500,
                content=error_response.dict(),
            )
