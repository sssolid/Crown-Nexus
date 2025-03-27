# app/middleware/request_context.py
from __future__ import annotations

"""
Request context middleware for the application.

This middleware sets up the request context for each incoming request,
including request ID generation and logging of request/response information.
"""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging.context import get_logger, request_context

logger = get_logger("app.middleware.request_context")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware for setting up request context and logging request information.

    This middleware generates a request ID for each incoming request, logs
    request and response information, and sets up the thread-local request
    context for use by other components.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request, setting up context and logging information.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            The response from downstream middleware
        """
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        start_time = time.time()

        # Store request_id in request state for other middleware
        request.state.request_id = request_id

        # Set up logging context for this request
        with request_context(request_id):
            # Log request information
            logger.info(
                f"Request: {request.method} {request.url.path}",
                method=request.method,
                path=request.url.path,
                query=str(request.query_params),
                client=request.client.host if request.client else None,
            )

            # Process the request
            response = await call_next(request)

            # Log response information
            execution_time = time.time() - start_time
            logger.info(
                f"Response: {response.status_code}",
                status_code=response.status_code,
                execution_time=f"{execution_time:.4f}s",
            )

            # Add headers to response
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Execution-Time"] = f"{execution_time:.4f}s"

            return response
