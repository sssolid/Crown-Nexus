# /backend/app/middleware/error_handler.py
from __future__ import annotations

import logging
import time
import traceback
from datetime import datetime
from typing import Callable, Dict, Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import (
    AppException,
    ErrorCode,
    ErrorResponse,
    ErrorSeverity,
    ErrorCategory
)
from app.core.logging import get_logger

logger = get_logger("app.middleware.error_handler")

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling errors.
    
    This middleware catches all exceptions raised during request processing
    and converts them to standardized error responses. It also logs errors
    with appropriate severity and context.
    """
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """Process the request and handle any errors.
        
        Args:
            request: FastAPI request
            call_next: Next middleware or route handler
            
        Returns:
            Response: Response with standardized error format if an error occurred
        """
        try:
            # Process request
            return await call_next(request)
        except Exception as exc:
            # Don't handle exceptions here, they'll be handled by exception handlers
            # This is just a fallback in case exception handlers fail
            logger.error(
                f"Unhandled exception in error handler middleware: {str(exc)}",
                exc_info=exc,
                request_id=getattr(request.state, "request_id", None),
                path=request.url.path,
                method=request.method,
            )
            
            # Create error response
            error_response = ErrorResponse(
                success=False,
                message="An unexpected server error occurred",
                code=ErrorCode.UNKNOWN_ERROR,
                data=None,
                details=[{
                    "loc": ["server"],
                    "msg": "An unexpected server error occurred",
                    "type": "unknown_error",
                }],
                meta={
                    "request_id": getattr(request.state, "request_id", None),
                    "severity": ErrorSeverity.CRITICAL,
                    "category": ErrorCategory.UNKNOWN,
                },
                timestamp=datetime.utcnow().isoformat(),
            )
            
            # Return error response
            return JSONResponse(
                status_code=500,
                content=error_response.dict(),
            )