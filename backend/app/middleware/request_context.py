# backend/app/middleware/request_context.py
from __future__ import annotations

from app.core.metrics import MetricName
from app.utils.circuit_breaker_utils import (
    safe_increment_counter,
    safe_observe_histogram,
)

"""
Request context middleware for the application.

This middleware sets up the request context for each incoming request,
including request ID generation and logging of request/response information.
"""

import time
import uuid
from typing import Callable, Any, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging.context import get_logger, request_context, set_user_id, clear_user_id
from app.core.dependency_manager import get_service

logger = get_logger("app.middleware.request_context")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware for setting up request context and logging request information.

    This middleware generates a request ID for each incoming request, logs
    request and response information, and sets up the thread-local request
    context for use by other components.
    """

    def __init__(self, app: Any) -> None:
        """
        Initialize the middleware.

        Args:
            app: The FastAPI application
        """
        super().__init__(app)
        logger.info("RequestContextMiddleware initialized")

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """
        Process the request, setting up context and logging information.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            The response from downstream middleware
        """
        # Get metrics service if available
        metrics_service: Optional[Any] = None
        try:
            metrics_service = get_service("metrics_service")
        except Exception:
            pass  # Continue without metrics service

        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        start_time = time.time()

        # Extract user ID from headers if available
        user_id = request.headers.get("X-User-ID")

        # Store request_id in request state for other middleware
        request.state.request_id = request_id
        if user_id:
            request.state.user_id = user_id

        # Set up logging context for this request
        with request_context(request_id, user_id=user_id):
            # Log request information with structured data
            logger.info(
                f"Request: {request.method} {request.url.path}",
                method=request.method,
                path=request.url.path,
                query=str(request.query_params),
                client=request.client.host if request.client else None,
                user_agent=request.headers.get("User-Agent"),
                referrer=request.headers.get("Referer"),
                content_type=request.headers.get("Content-Type"),
                accept=request.headers.get("Accept"),
            )

            try:
                # Process the request
                response = await call_next(request)

                # Calculate execution time
                execution_time = time.time() - start_time

                # Log response information
                logger.info(
                    f"Response: {response.status_code}",
                    status_code=response.status_code,
                    execution_time=f"{execution_time:.4f}s",
                    content_type=response.headers.get("Content-Type"),
                    content_length=response.headers.get("Content-Length"),
                )

                # Record metrics if service is available
                if metrics_service:
                    try:
                        safe_observe_histogram(
                            MetricName.HTTP_REQUEST_DURATION_SECONDS.value,
                            execution_time,
                            {
                                "method": request.method,
                                "endpoint": request.url.path,
                                "status_code": str(response.status_code // 100) + "xx",
                            },
                        )
                    except Exception as e:
                        logger.debug(f"Failed to record metrics: {e}")

                # Add headers to response
                response.headers["X-Request-ID"] = request_id
                response.headers["X-Execution-Time"] = f"{execution_time:.4f}s"

                return response

            except Exception as e:
                # Record execution time
                execution_time = time.time() - start_time

                # Log exception with context
                logger.exception(
                    f"Error processing request: {str(e)}",
                    exc_info=e,
                    method=request.method,
                    path=request.url.path,
                    execution_time=f"{execution_time:.4f}s",
                )

                # Record error metrics if service is available
                if metrics_service:
                    try:
                        safe_increment_counter(
                            MetricName.HTTP_REQUEST_ERRORS_TOTAL.value,
                            1,
                            {
                                "method": request.method,
                                "endpoint": request.url.path,
                                "error_type": type(e).__name__,
                            },
                        )
                    except Exception as metrics_err:
                        logger.debug(f"Failed to record error metrics: {metrics_err}")

                # Re-raise the exception
                raise
            finally:
                # Clear user ID from context if it was set
                if user_id:
                    clear_user_id()
