# /app/middleware/request_context.py
from __future__ import annotations

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger, request_context

logger = get_logger("app.middleware.request_context")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware that sets up logging request context.

    This middleware ensures each request has a unique ID and tracks execution time,
    both stored in the logging context.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request and set up logging context.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            Response: The processed response
        """
        # Generate request ID
        request_id = str(uuid.uuid4())

        # Store request start time
        start_time = time.time()

        # Add request ID to request state
        request.state.request_id = request_id

        # Use logging context manager
        with request_context(request_id):
            # Log request
            logger.info(
                f"Request: {request.method} {request.url.path}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "client": request.client.host if request.client else None,
                },
            )

            # Process request
            response = await call_next(request)

            # Calculate execution time
            execution_time = time.time() - start_time

            # Log response
            logger.info(
                f"Response: {response.status_code}",
                extra={
                    "status_code": response.status_code,
                    "execution_time": f"{execution_time:.4f}s",
                },
            )

            # Add request ID and timing headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Execution-Time"] = f"{execution_time:.4f}s"

            return response
