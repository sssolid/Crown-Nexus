# app/middleware/metrics.py
from __future__ import annotations

import time
from typing import Callable, Dict, Optional

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route, Match

from app.core.dependency_manager import get_dependency
from app.core.logging import get_logger
from app.services.metrics import MetricsService
from app.services.metrics.base import MetricName, MetricTag

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
        self.app = app
        logger.info("MetricsMiddleware initialized")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timing the request
        start_time = time.monotonic()

        # Get metrics service
        metrics_service: Optional[MetricsService] = None
        try:
            metrics_service = get_dependency("metrics_service")

            # Track in-progress request
            if (
                metrics_service
                and MetricName.HTTP_IN_PROGRESS in metrics_service.gauges
            ):
                endpoint = self._get_endpoint_name(request)
                labels = {
                    MetricTag.METHOD: request.method,
                    MetricTag.ENDPOINT: endpoint,
                }
                metrics_service.track_in_progress(
                    MetricName.HTTP_IN_PROGRESS, labels, 1
                )
        except Exception as e:
            logger.error(f"Error getting metrics service: {str(e)}")
            metrics_service = None

        # Default error code
        error_code = None

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

            # Track metrics if service is available
            if metrics_service:
                endpoint = self._get_endpoint_name(request)

                # Track request metrics
                metrics_service.track_request(
                    method=request.method,
                    endpoint=endpoint,
                    status_code=status_code,
                    duration=duration,
                    error_code=error_code,
                )

                # Update in-progress count
                if MetricName.HTTP_IN_PROGRESS in metrics_service.gauges:
                    labels = {
                        MetricTag.METHOD: request.method,
                        MetricTag.ENDPOINT: endpoint,
                    }
                    metrics_service.track_in_progress(
                        MetricName.HTTP_IN_PROGRESS, labels, -1
                    )

    def _get_endpoint_name(self, request: Request) -> str:
        """Extract the endpoint name from the request.

        Args:
            request: FastAPI request

        Returns:
            Endpoint name
        """
        # Try to match the request to a route
        for route in self.app.routes:
            match, scope = route.matches(request.scope)
            if match == Match.FULL:
                if isinstance(route, Route):
                    return route.name or route.path
                return route.path

        # Fallback to the path if no route is matched
        return request.url.path
