# /app/middleware/metrics.py
from __future__ import annotations

import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route, Match

from app.core.logging import get_logger
from app.core.metrics import (
    track_request,
    set_gauge,
    MetricName,
    MetricTag,
)

logger = get_logger("app.middleware.metrics")


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting request metrics.

    Automatically tracks HTTP request metrics such as request count,
    duration, and errors.
    """

    def __init__(self, app: FastAPI) -> None:
        """Initialize the metrics middleware.

        Args:
            app: FastAPI application
        """
        super().__init__(app)
        # Store a reference to the actual FastAPI app
        self._fastapi_app = app
        logger.info("MetricsMiddleware initialized")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timing the request
        start_time = time.monotonic()

        # Get endpoint name safely
        endpoint = self._get_endpoint_name(request)

        # Create labels for metrics
        labels = {
            MetricTag.METHOD: request.method,
            MetricTag.ENDPOINT: endpoint,
        }

        # Increment in-progress counter
        try:
            set_gauge(MetricName.HTTP_IN_PROGRESS, 1, labels)
        except Exception as e:
            logger.error(f"Error tracking in-progress request: {str(e)}")

        # Default error code
        error_code = None
        status_code = 500  # Default in case of exception

        try:
            # Execute request
            response = await call_next(request)
            status_code = response.status_code

            # Extract error code if available (from custom headers or response)
            error_code = response.headers.get("X-Error-Code")

            return response
        except Exception as e:
            # Handle uncaught exceptions
            logger.error(f"Uncaught exception in request: {str(e)}")
            status_code = 500
            error_code = type(e).__name__

            # Re-raise the exception to be handled by FastAPI
            raise
        finally:
            # Calculate request duration
            duration = time.monotonic() - start_time

            # Track request metrics
            try:
                # Track the complete request
                track_request(
                    method=request.method,
                    endpoint=endpoint,
                    status_code=status_code,
                    duration=duration,
                    error_code=error_code,
                )

                # Decrement in-progress counter
                set_gauge(MetricName.HTTP_IN_PROGRESS, 0, labels)
            except Exception as e:
                logger.error(f"Error tracking request metrics: {str(e)}")

    def _get_endpoint_name(self, request: Request) -> str:
        """Extract the endpoint name from the request.

        Args:
            request: FastAPI request

        Returns:
            Endpoint name
        """
        # First try using the stored FastAPI app
        if hasattr(self, "_fastapi_app") and hasattr(self._fastapi_app, "routes"):
            try:
                # Try to match the request to a route
                for route in self._fastapi_app.routes:
                    match, scope = route.matches(request.scope)
                    if match == Match.FULL:
                        if isinstance(route, Route):
                            return route.name or route.path
                        return route.path
            except Exception as e:
                logger.warning(f"Error getting endpoint from routes: {str(e)}")

        # Fallback to extracting from the path
        path = request.url.path

        # Try to clean up the path to make it more usable as a metric
        # Remove trailing slash
        if path.endswith("/") and len(path) > 1:
            path = path[:-1]

        # Get the relevant part of the path (exclude API version prefix)
        parts = path.split("/")
        if len(parts) > 3 and parts[1] == "api" and parts[2].startswith("v"):
            # This is an API path with version, make a cleaner name
            return "/".join(parts[3:])

        return path
