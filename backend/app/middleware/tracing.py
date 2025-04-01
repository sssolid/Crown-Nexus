# backend/app/middleware/tracing.py
from __future__ import annotations

from app.core.metrics import MetricName

"""
Tracing middleware for the application.

This middleware handles distributed tracing for request processing, allowing
for request tracking across services and components.
"""

import time
import uuid
from typing import Callable, Optional, Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging import get_logger, request_context
from app.core.dependency_manager import get_service

logger = get_logger("app.middleware.tracing")


class TracingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling distributed tracing.

    This middleware sets up tracing spans and propagates tracing headers
    to enable request tracking across services and components.
    """

    def __init__(
        self,
        app: Any,
        service_name: str = "api",
        exclude_paths: Optional[list[str]] = None,
    ) -> None:
        """
        Initialize the middleware.

        Args:
            app: The FastAPI application
            service_name: Name of this service for tracing
            exclude_paths: List of paths to exclude from tracing
        """
        super().__init__(app)
        self.service_name = service_name
        self.exclude_paths = exclude_paths or []
        logger.info("TracingMiddleware initialized", service_name=service_name)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """
        Process the request with tracing.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            The response from downstream middleware
        """
        # Get the path
        path = request.url.path

        # Skip tracing for excluded paths
        if any(path.startswith(exc) for exc in self.exclude_paths):
            return await call_next(request)

        # Extract existing trace context from headers or create new ones
        trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        parent_span_id = request.headers.get("X-Span-ID")

        # Store tracing info in request state
        request.state.trace_id = trace_id
        request.state.span_id = span_id
        request.state.parent_span_id = parent_span_id

        # Try to get metrics service for tracking
        metrics_service = None
        try:
            metrics_service = get_service("metrics_service")
        except Exception:
            pass  # Continue without metrics if not available

        start_time = time.monotonic()
        status_code = 500  # Default in case of exception
        error = None

        # Create a trace context for this request
        with request_context(request_id=trace_id):
            # Add tracing info to logging context
            logger.info(
                "Starting request trace",
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=parent_span_id,
                path=path,
                method=request.method,
                service=self.service_name,
            )

            try:
                # Process the request
                response = await call_next(request)
                status_code = response.status_code

                # Add tracing headers to response
                response.headers["X-Trace-ID"] = trace_id
                response.headers["X-Span-ID"] = span_id
                if parent_span_id:
                    response.headers["X-Parent-Span-ID"] = parent_span_id

                return response
            except Exception as e:
                error = str(e)
                # Let the exception propagate to the error handler middleware
                raise
            finally:
                # Calculate duration
                duration = time.monotonic() - start_time

                # Log the end of the span
                logger.info(
                    "Completed request trace",
                    trace_id=trace_id,
                    span_id=span_id,
                    duration=duration,
                    status_code=status_code,
                    path=path,
                    method=request.method,
                    service=self.service_name,
                    error=error,
                )

                # Track span metrics if metrics service is available
                if metrics_service:
                    try:
                        metrics_service.observe_histogram(
                            MetricName.REQUEST_TRACE_DURATION_SECONDS.value,
                            duration,
                            {
                                "path": path,
                                "method": request.method,
                                "status_code": str(status_code // 100) + "xx",
                                "error_code": "true" if error else "false",
                            },
                        )
                    except Exception as e:
                        logger.debug(f"Failed to track tracing metrics: {str(e)}")
