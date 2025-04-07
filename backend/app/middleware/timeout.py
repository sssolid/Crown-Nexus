# backend/app/middleware/timeout.py
from __future__ import annotations

from app.utils.circuit_breaker_utils import (
    safe_observe_histogram,
    safe_increment_counter,
)

"""
Timeout middleware for the application.

This middleware sets a maximum execution time for requests to prevent
long-running requests from consuming resources.
"""

import asyncio
import time
from typing import Callable, Optional, Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette import status

from app.core.exceptions import AppException, ErrorCode
from app.logging import get_logger
from app.core.dependency_manager import get_service

logger = get_logger("app.middleware.timeout")


class TimeoutException(AppException):
    """Exception raised when a request exceeds the configured timeout."""

    def __init__(
        self,
        message: str,
        details: Optional[dict[str, Any]] = None,
        status_code: int = status.HTTP_504_GATEWAY_TIMEOUT,
        code: ErrorCode = ErrorCode.SERVER_ERROR,
    ) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message
            details: Additional error details
            status_code: HTTP status code
            code: Application-specific error code
        """
        super().__init__(message, details, status_code, code)


class TimeoutMiddleware(BaseHTTPMiddleware):
    """
    Middleware for setting request timeouts.

    This middleware sets a maximum execution time for requests to prevent
    long-running requests from consuming resources.
    """

    def __init__(
        self,
        app: Any,
        timeout_seconds: float = 30.0,
        exclude_paths: Optional[list[str]] = None,
    ) -> None:
        """
        Initialize the middleware.

        Args:
            app: The FastAPI application
            timeout_seconds: Maximum request execution time in seconds
            exclude_paths: List of paths to exclude from timeout enforcement
        """
        super().__init__(app)
        self.timeout_seconds = timeout_seconds
        self.exclude_paths = exclude_paths or ["/docs", "/redoc", "/openapi.json"]
        logger.info("TimeoutMiddleware initialized", timeout_seconds=timeout_seconds)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """
        Process the request with a timeout.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            The response from downstream middleware

        Raises:
            TimeoutException: If the request exceeds the timeout
        """
        # Get the path
        path = request.url.path

        # Skip timeout for excluded paths
        if any(path.startswith(exc) for exc in self.exclude_paths):
            return await call_next(request)

        # Track metrics if available
        metrics_service = None
        try:
            metrics_service = get_service("metrics_service")
        except Exception:
            pass  # Continue without metrics if not available

        start_time = time.monotonic()
        timed_out = False

        try:
            # Execute the request with a timeout
            return await asyncio.wait_for(
                call_next(request), timeout=self.timeout_seconds
            )
        except asyncio.TimeoutError:
            timed_out = True
            # Get client IP safely
            client_ip = (
                getattr(request.client, "host", "unknown")
                if request.client
                else "unknown"
            )

            logger.warning(
                "Request timed out",
                path=path,
                method=request.method,
                client=client_ip,
                timeout_seconds=self.timeout_seconds,
            )

            # Track timeout in metrics if available
            if metrics_service:
                try:
                    safe_increment_counter(
                        "request_timeouts_total",
                        1,
                        {"endpoint": path, "method": request.method},
                    )
                except Exception as e:
                    logger.debug(f"Failed to track timeout metrics: {str(e)}")

            raise TimeoutException(
                message=f"Request timed out after {self.timeout_seconds} seconds",
                details={
                    "endpoint": path,
                    "method": request.method,
                    "timeout_seconds": self.timeout_seconds,
                },
            )
        finally:
            # Track request duration in metrics if available
            if metrics_service and not timed_out:
                try:
                    duration = time.monotonic() - start_time
                    safe_observe_histogram(
                        "request_duration_seconds",
                        duration,
                        {"endpoint": path, "method": request.method},
                    )
                except Exception as e:
                    logger.debug(f"Failed to track duration metrics: {str(e)}")
