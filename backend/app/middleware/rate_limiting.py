# backend/app/middleware/rate_limiting.py
from __future__ import annotations

from app.core.metrics import MetricName

"""
Rate limiting middleware for FastAPI applications.

This middleware applies rate limiting to incoming requests based on configurable
rules and strategies. It supports both Redis-backed and in-memory rate limiting.
"""

import time
from typing import Any, Callable, Dict, List, Optional, Tuple

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.exceptions import RateLimitException
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.rate_limiting.exceptions import RateLimitExceededException
from app.core.dependency_manager import get_service

logger = get_logger("app.middleware.rate_limiting")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware that applies rate limiting to incoming requests.

    This middleware checks requests against configured rate limit rules
    and rejects requests that exceed the limits.
    """

    def __init__(
        self,
        app: Any,
        rules: Optional[List[RateLimitRule]] = None,
        use_redis: bool = True,
        enable_headers: bool = True,
        block_exceeding_requests: bool = True,
        fallback_to_memory: bool = True,
        limit_by_path: bool = False,
    ) -> None:
        """Initialize the rate limit middleware.

        Args:
            app: The FastAPI application.
            rules: List of rate limit rules to apply. If None, a default
                rule will be used.
            use_redis: Whether to use Redis for rate limiting.
            enable_headers: Whether to include rate limit headers in responses.
            block_exceeding_requests: Whether to block requests that exceed
                the rate limit.
            fallback_to_memory: Whether to fallback to memory if Redis fails
            limit_by_path: Whether to apply rate limits by path in addition to rules
        """
        super().__init__(app)
        self.rules: List[RateLimitRule] = rules or [
            RateLimitRule(
                requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
                window_seconds=60,
            )
        ]
        self.use_redis: bool = use_redis
        self.enable_headers: bool = enable_headers
        self.block_exceeding_requests: bool = block_exceeding_requests
        self.fallback_to_memory: bool = fallback_to_memory
        self.limit_by_path: bool = limit_by_path

        try:
            self.rate_limiter: RateLimiter = RateLimiter(use_redis=use_redis)
            self.using_fallback: bool = False
        except Exception as e:
            if fallback_to_memory:
                logger.warning(
                    "Failed to initialize Redis rate limiter, falling back to memory",
                    error=str(e),
                )
                self.rate_limiter = RateLimiter(use_redis=False)
                self.using_fallback = True
            else:
                logger.error(
                    "Failed to initialize rate limiter and fallback disabled",
                    error=str(e),
                )
                raise

        logger.info(
            "RateLimitMiddleware initialized",
            rules_count=len(self.rules),
            use_redis=use_redis,
            using_fallback=getattr(self, "using_fallback", False),
            enable_headers=enable_headers,
            block_exceeding_requests=block_exceeding_requests,
            limit_by_path=limit_by_path,
        )

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        """Process the request and apply rate limiting.

        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.

        Returns:
            The response from the next middleware or route handler,
            or a 429 response if the rate limit is exceeded.

        Raises:
            RateLimitException: If the rate limit is exceeded and
                block_exceeding_requests is True.
        """
        # Get metrics service
        metrics_service = None
        try:
            metrics_service = get_service("metrics_service")
        except Exception as e:
            logger.debug(f"Could not get metrics service: {str(e)}")

        start_time = time.time()
        is_limited = False
        path: str = request.url.path
        client_host = getattr(request.client, "host", "unknown") if request.client else "unknown"

        try:
            # Skip excluded paths
            if any(
                path.startswith(excluded)
                for rule in self.rules
                for excluded in rule.exclude_paths
            ):
                if metrics_service:
                    try:
                        metrics_service.increment_counter(
                            "rate_limit_skipped_total",
                            1,
                            {"endpoint": path, "reason": "excluded_path"},
                        )
                    except Exception as e:
                        logger.debug(f"Failed to record rate limit metrics: {str(e)}")

                return await call_next(request)

            # Find applicable rules
            applicable_rules, rule_match_reason = self._get_applicable_rules(request)

            if not applicable_rules:
                if metrics_service:
                    try:
                        metrics_service.increment_counter(
                            "rate_limit_skipped_total",
                            1,
                            {"endpoint": path, "reason": "no_applicable_rules"},
                        )
                    except Exception as e:
                        logger.debug(f"Failed to record rate limit metrics: {str(e)}")

                return await call_next(request)

            headers: Dict[str, str] = {}

            # Check against each rule
            limited_rule = None
            for rule in applicable_rules:
                key: str = self.rate_limiter.get_key_for_request(request, rule)
                limited, count, limit = await self.rate_limiter.is_rate_limited(
                    key, rule
                )

                if limited:
                    is_limited = True
                    limited_rule = rule
                    logger.warning(
                        "Rate limit exceeded",
                        client_host=client_host,
                        path=path,
                        key=key,
                        count=count,
                        limit=limit,
                        rule_type=rule.strategy.value,
                    )

                    # Track detailed metrics
                    if metrics_service:
                        try:
                            metrics_service.increment_counter(
                                "rate_limit_exceeded_total",
                                1,
                                {
                                    "endpoint": path,
                                    "client_host": client_host[:15],  # Truncate long IPs
                                    "strategy": rule.strategy.value,
                                    "match_reason": rule_match_reason,
                                },
                            )
                        except Exception as e:
                            logger.debug(f"Failed to record rate limit metrics: {str(e)}")

                    break

                if self.enable_headers:
                    # Update headers with the most restrictive remaining value
                    if "X-RateLimit-Remaining" not in headers or int(headers["X-RateLimit-Remaining"]) > (
                        limit - count):
                        headers["X-RateLimit-Limit"] = str(limit)
                        headers["X-RateLimit-Remaining"] = str(max(0, limit - count))
                        headers["X-RateLimit-Reset"] = str(rule.window_seconds)

            # Handle rate limit exceeded
            if is_limited and self.block_exceeding_requests:
                assert limited_rule is not None, "Limited rule should not be None when is_limited is True"
                headers["Retry-After"] = str(limited_rule.window_seconds)

                raise RateLimitExceededException(
                    message="Rate limit exceeded",
                    details={
                        "ip": client_host,
                        "endpoint": path,
                        "strategy": limited_rule.strategy.value,
                    },
                    headers=headers,
                    reset_seconds=limited_rule.window_seconds,
                )

            # Process the request
            response: Response = await call_next(request)

            # Add rate limit headers to the response
            if self.enable_headers and headers:
                for header, value in headers.items():
                    response.headers[header] = value

            return response
        finally:
            # Record metrics
            if metrics_service:
                duration = time.time() - start_time
                try:
                    metrics_service.observe_histogram(
                        MetricName.RATE_LIMITING_MIDDLEWARE_DURATION_SECONDS.value,
                        duration,
                        {"limited": str(is_limited), "path": path},
                    )
                    metrics_service.increment_counter(
                        MetricName.RATE_LIMITING_REQUESTS_TOTAL.value,
                        1,
                        {"limited": str(is_limited), "path": path},
                    )
                except Exception as e:
                    logger.debug(f"Failed to record rate limiting metrics: {str(e)}")

    def _get_applicable_rules(self, request: Request) -> Tuple[List[RateLimitRule], str]:
        """Get applicable rate limit rules for a request.

        Args:
            request: The incoming request

        Returns:
            Tuple of (list of applicable rules, match reason)
        """
        path: str = request.url.path

        # Check for path-specific rules first
        path_rules = [
            rule for rule in self.rules
            if rule.path_pattern is not None and path.startswith(rule.path_pattern)
        ]

        if path_rules:
            return path_rules, "path_pattern"

        # If path-specific rules not found, check for default rules
        default_rules = [
            rule for rule in self.rules
            if rule.path_pattern is None
        ]

        if default_rules:
            return default_rules, "default"

        # If no matching rules, return the first rule as fallback
        if self.rules:
            return [self.rules[0]], "fallback"

        # If no rules at all, return empty list
        return [], "no_rules"
