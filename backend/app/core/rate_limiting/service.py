# app/core/rate_limiting/service.py
from __future__ import annotations

"""
Rate limiting service implementation.

This module provides a service wrapper around the rate limiting system,
making it available through the dependency manager.
"""

from typing import Dict, Optional, Tuple
from fastapi import Request

from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.config import settings

logger = get_logger("app.core.rate_limiting.service")


class RateLimitingService:
    def __init__(self) -> None:
        """Initialize the rate limiting service."""
        self._initialized = False
        self._limiter: Optional[RateLimiter] = None

    async def initialize(self) -> None:
        """Initialize the rate limiting service.

        If already initialized, this method does nothing.
        """
        if self._initialized:
            logger.debug("Rate limiting service already initialized, skipping")
            return

        logger.info("Initializing rate limiting service")
        self._limiter = RateLimiter(
            use_redis=settings.RATE_LIMIT_STORAGE == "redis",
            prefix="ratelimit",
            default_rule=RateLimitRule(
                requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
                window_seconds=60,
            ),
        )
        self._initialized = True
        logger.info("Rate limiting service initialized")

    async def shutdown(self) -> None:
        """Shut down the rate limiting service.

        If not initialized, this method does nothing.
        """
        if not self._initialized:
            return

        logger.info("Shutting down rate limiting service")
        self._limiter = None
        self._initialized = False
        logger.info("Rate limiting service shut down")

    async def is_rate_limited(
        self, key: str, rule: Optional[RateLimitRule] = None
    ) -> Tuple[bool, int, int]:
        """Check if a key is rate limited.

        Args:
            key: The key to check.
            rule: Optional rate limit rule to apply. If not provided,
                the default rule will be used.

        Returns:
            A tuple containing:
                - Whether the key is rate limited (True if limited)
                - The current count for the key
                - The maximum allowed count (limit)

        Raises:
            RateLimitingServiceException: If the service is not initialized.
        """
        self._ensure_initialized()
        return await self._limiter.is_rate_limited(key, rule)

    def get_key_for_request(self, request: Request, rule: RateLimitRule) -> str:
        """Generate a rate limit key for a request.

        Args:
            request: The request to generate a key for.
            rule: The rate limit rule that defines the key strategy.

        Returns:
            A string key for rate limiting.

        Raises:
            RateLimitingServiceException: If the service is not initialized.
        """
        self._ensure_initialized()
        return self._limiter.get_key_for_request(request, rule)

    def _ensure_initialized(self) -> None:
        """Ensure the service is initialized.

        Raises:
            RateLimitingServiceException: If the service is not initialized.
        """
        if not self._initialized or self._limiter is None:
            from app.core.rate_limiting.exceptions import RateLimitingServiceException

            logger.error("Rate limiting service accessed before initialization")
            raise RateLimitingServiceException("Rate limiting service not initialized")


_rate_limiting_service: Optional[RateLimitingService] = None


def get_rate_limiting_service() -> RateLimitingService:
    """Get or create the rate limiting service singleton.

    Returns:
        The rate limiting service instance.
    """
    global _rate_limiting_service
    if _rate_limiting_service is None:
        _rate_limiting_service = RateLimitingService()
    return _rate_limiting_service
