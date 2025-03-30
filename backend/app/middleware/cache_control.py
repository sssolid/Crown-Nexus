# backend/app/middleware/cache_control.py
from __future__ import annotations

"""
Cache control middleware for the application.

This middleware adds appropriate cache control headers to responses
based on the request path and method.
"""

from typing import Callable, Dict, Optional, Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging import get_logger

logger = get_logger("app.middleware.cache_control")


class CacheControlMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding cache control headers to responses.

    This middleware adds appropriate cache control headers to responses
    based on the request path and method to control client and CDN caching.
    """

    def __init__(
        self,
        app: Any,
        cache_rules: Optional[Dict[str, str]] = None,
        default_rule: str = "no-store, no-cache, must-revalidate, max-age=0",
        cacheable_methods: Optional[list[str]] = None,
        exclude_paths: Optional[list[str]] = None,
    ) -> None:
        """
        Initialize the middleware.

        Args:
            app: The FastAPI application
            cache_rules: Dictionary mapping path prefixes to cache control directives
            default_rule: Default cache control directive for paths not in cache_rules
            cacheable_methods: HTTP methods that can be cached (default: GET, HEAD)
            exclude_paths: List of paths to exclude from cache control
        """
        super().__init__(app)
        self.cache_rules = cache_rules or {
            "/static/": "public, max-age=86400, stale-while-revalidate=3600",
            "/media/": "public, max-age=86400, stale-while-revalidate=3600",
            "/api/v1/docs": "public, max-age=3600",
            "/api/v1/redoc": "public, max-age=3600",
            "/api/v1/openapi.json": "public, max-age=3600",
            "/api/v1/health": "public, max-age=60",
        }
        self.default_rule = default_rule
        self.cacheable_methods = cacheable_methods or ["GET", "HEAD"]
        self.exclude_paths = exclude_paths or []
        logger.info("CacheControlMiddleware initialized")

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """
        Process the request and add cache control headers to the response.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            The response with added cache control headers
        """
        # Get the path and method
        path = request.url.path
        method = request.method

        # Skip if the path should be excluded
        if any(path.startswith(exc) for exc in self.exclude_paths):
            return await call_next(request)

        # Process the request first
        response = await call_next(request)

        # Skip if the response already has Cache-Control header
        if "Cache-Control" in response.headers:
            return response

        # Only apply cache control to cacheable methods
        if method not in self.cacheable_methods:
            response.headers["Cache-Control"] = "no-store"
            return response

        # Find the matching cache rule for the path
        cache_control = self.default_rule
        for path_prefix, rule in self.cache_rules.items():
            if path.startswith(path_prefix):
                cache_control = rule
                break

        # Add the Cache-Control header
        response.headers["Cache-Control"] = cache_control

        # Add Vary header to prevent incorrect caching
        response.headers["Vary"] = "Accept-Encoding, Cookie, Authorization"

        return response
