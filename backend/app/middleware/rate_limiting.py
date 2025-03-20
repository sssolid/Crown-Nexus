# /app/core/middleware/rate_limiting.py
"""FastAPI middleware for rate limiting.

This module provides a middleware for applying rate limiting to
FastAPI applications.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.exceptions import RateLimitException
from app.core.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for applying rate limiting to requests.

    This middleware applies rate limiting to incoming requests based on
    configurable rules and can block requests that exceed limits.

    Attributes:
        rules: List of rate limit rules
        rate_limiter: Rate limiter instance
        enable_headers: Whether to add rate limit headers to responses
        block_exceeding_requests: Whether to block requests that exceed limits
    """

    def __init__(
        self,
        app: Any,
        rules: Optional[List[RateLimitRule]] = None,
        use_redis: bool = True,
        enable_headers: bool = True,
        block_exceeding_requests: bool = True,
    ) -> None:
        """Initialize rate limit middleware.

        Args:
            app: FastAPI application
            rules: List of rate limit rules
            use_redis: Whether to use Redis for distributed rate limiting
            enable_headers: Add rate limit headers to responses
            block_exceeding_requests: Block requests that exceed limits
        """
        super().__init__(app)
        self.rules: List[RateLimitRule] = rules or [
            RateLimitRule(
                requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
                window_seconds=60,
            )
        ]
        self.rate_limiter: RateLimiter = RateLimiter(use_redis=use_redis)
        self.enable_headers: bool = enable_headers
        self.block_exceeding_requests: bool = block_exceeding_requests

        logger.info("RateLimitMiddleware initialized")

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        """Process the request and apply rate limiting.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            Response: The processed response

        Raises:
            RateLimitException: If the request exceeds rate limits
        """
        # Skip rate limiting for excluded paths
        path: str = request.url.path
        if any(
            path.startswith(excluded)
            for rule in self.rules
            for excluded in rule.exclude_paths
        ):
            return await call_next(request)

        # Find applicable rules
        applicable_rules: List[RateLimitRule] = [
            rule
            for rule in self.rules
            if rule.path_pattern is None or path.startswith(rule.path_pattern)
        ]

        if not applicable_rules:
            applicable_rules = [self.rules[0]]  # Default to first rule

        # Check rate limits
        is_limited: bool = False
        headers: Dict[str, str] = {}

        for rule in applicable_rules:
            key: str = self.rate_limiter.get_key_for_request(request, rule)
            limited, count, limit = await self.rate_limiter.is_rate_limited(key, rule)

            if limited:
                is_limited = True

            if self.enable_headers:
                headers["X-RateLimit-Limit"] = str(limit)
                headers["X-RateLimit-Remaining"] = str(max(0, limit - count))
                headers["X-RateLimit-Reset"] = str(rule.window_seconds)

        # Block the request if it exceeds rate limits
        if is_limited and self.block_exceeding_requests:
            headers["Retry-After"] = str(applicable_rules[0].window_seconds)

            logger.warning(f"Rate limit exceeded for {request.client.host}")

            # Use custom exception from the project's hierarchy
            raise RateLimitException(
                message="Rate limit exceeded",
                details={"ip": request.client.host},
                headers=headers,
            )

        # Process the request
        response: Response = await call_next(request)

        # Add rate limit headers to the response
        if self.enable_headers:
            for header, value in headers.items():
                response.headers[header] = value

        return response
