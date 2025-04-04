# backend/app/middleware/cors.py
from __future__ import annotations

from app.utils.circuit_breaker_utils import safe_increment_counter

"""
Enhanced CORS middleware for the application.

This middleware provides more detailed logging and metrics for CORS requests
while extending the functionality of FastAPI's built-in CORSMiddleware.
"""

from typing import Callable, Optional, Any, List, Dict, Union

from fastapi import Request, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp

from app.logging import get_logger
from app.core.dependency_manager import get_service

logger = get_logger("app.middleware.cors")


class EnhancedCORSMiddleware(CORSMiddleware):
    """
    Enhanced CORS middleware with additional logging and metrics.

    This middleware extends FastAPI's built-in CORSMiddleware to provide
    more detailed logging and metrics for CORS requests.
    """

    def __init__(
        self,
        app: ASGIApp,
        allow_origins: Union[List[str], str] = (),
        allow_methods: Union[List[str], str] = ("GET",),
        allow_headers: Union[List[str], str] = (),
        allow_credentials: bool = False,
        allow_origin_regex: Optional[str] = None,
        expose_headers: Union[List[str], str] = (),
        max_age: int = 600,
    ) -> None:
        """
        Initialize the middleware.

        Args:
            app: The ASGI application
            allow_origins: List of allowed origins or "*" for wildcard
            allow_methods: List of allowed HTTP methods or "*" for wildcard
            allow_headers: List of allowed HTTP headers or "*" for wildcard
            allow_credentials: Whether to allow credentials (cookies)
            allow_origin_regex: Regex pattern for allowed origins
            expose_headers: Headers to expose to the browser
            max_age: Max age for CORS preflight requests in seconds
        """
        super().__init__(
            app=app,
            allow_origins=allow_origins,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
            allow_credentials=allow_credentials,
            allow_origin_regex=allow_origin_regex,
            expose_headers=expose_headers,
            max_age=max_age,
        )
        # Convert lists to strings for better logging
        if isinstance(allow_origins, list):
            allow_origins_str = ", ".join(allow_origins)
        else:
            allow_origins_str = allow_origins

        if isinstance(allow_methods, list):
            allow_methods_str = ", ".join(allow_methods)
        else:
            allow_methods_str = allow_methods

        if isinstance(allow_headers, list):
            allow_headers_str = ", ".join(allow_headers)
        else:
            allow_headers_str = allow_headers

        logger.info(
            "EnhancedCORSMiddleware initialized",
            allow_origins=allow_origins_str,
            allow_methods=allow_methods_str,
            allow_headers=allow_headers_str,
            allow_credentials=allow_credentials,
            allow_origin_regex=allow_origin_regex,
            max_age=max_age,
        )

    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable) -> None:
        """
        Process the ASGI request.

        Args:
            scope: The ASGI connection scope
            receive: The ASGI receive function
            send: The ASGI send function
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Extract request information
        request = Request(scope)
        origin = request.headers.get("origin")
        is_cors_request = origin is not None
        is_preflight_request = is_cors_request and request.method == "OPTIONS"

        # Try to get metrics service
        metrics_service = None
        try:
            metrics_service = get_service("metrics_service")
        except Exception:
            pass  # Continue without metrics if not available

        # Log CORS request
        if is_cors_request:
            logger.debug(
                "CORS request received",
                path=request.url.path,
                origin=origin,
                method=request.method,
                is_preflight=is_preflight_request,
            )

            # Track CORS request metrics if available
            if metrics_service:
                try:
                    safe_increment_counter(
                        "cors_requests_total",
                        1,
                        {
                            "path": request.url.path,
                            "method": request.method,
                            "is_preflight": str(is_preflight_request),
                        },
                    )
                except Exception as e:
                    logger.debug(f"Failed to track CORS metrics: {str(e)}")

        # Create a special wrapper for send to inspect CORS response headers
        async def wrapped_send(message: Dict[str, Any]) -> None:
            if message["type"] == "http.response.start" and is_cors_request:
                headers = dict(message.get("headers", []))
                headers_dict = {k.decode(): v.decode() for k, v in headers.items()}

                # Check if the origin is allowed
                is_allowed = "access-control-allow-origin" in headers_dict

                if is_allowed:
                    logger.debug(
                        "CORS request allowed",
                        path=request.url.path,
                        origin=origin,
                        method=request.method,
                        is_preflight=is_preflight_request,
                    )
                else:
                    logger.warning(
                        "CORS request denied",
                        path=request.url.path,
                        origin=origin,
                        method=request.method,
                        is_preflight=is_preflight_request,
                    )

                # Track CORS response metrics if available
                if metrics_service:
                    try:
                        safe_increment_counter(
                            "cors_responses_total",
                            1,
                            {
                                "path": request.url.path,
                                "method": request.method,
                                "is_preflight": str(is_preflight_request),
                                "is_allowed": str(is_allowed),
                            },
                        )
                    except Exception as e:
                        logger.debug(f"Failed to track CORS metrics: {str(e)}")

            await send(message)

        # Call the parent middleware with our wrapped send function
        await super().__call__(scope, receive, wrapped_send)
