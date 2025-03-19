# backend/app/services/security/rate_limiting.py
"""Rate limiting utilities.

This module provides rate limiting services to protect against abuse,
DoS attacks, and to ensure fair API usage.
"""
from __future__ import annotations

import time
from typing import Tuple

from app.core.logging import get_logger
from app.utils.redis_manager import get_key, set_key

logger = get_logger(__name__)


class RateLimitService:
    """Service for rate limiting."""

    def __init__(self) -> None:
        """Initialize the rate limiting service."""
        # Prefix for rate limit keys in the cache
        self.rate_limit_prefix = "rate_limit:"

    async def check_rate_limit(
        self, key: str, max_requests: int, window_seconds: int
    ) -> Tuple[bool, int, int]:
        """
        Check if a request should be rate limited.

        Args:
            key: The key to rate limit on (e.g., user ID, IP address)
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds

        Returns:
            Tuple of (is_limited, current_count, reset_seconds)
        """
        # Generate window-based key
        window_start = int(time.time() / window_seconds) * window_seconds
        cache_key = f"{self.rate_limit_prefix}{key}:{window_start}"

        # Get current count
        current = await get_key(cache_key)

        if current is None:
            # First request in this window
            count = 1
            await set_key(cache_key, count, window_seconds)
            reset_seconds = window_seconds
            return False, count, reset_seconds

        # Increment count
        count = int(current) + 1

        # Update in cache
        remaining_ttl = await self._get_ttl(cache_key)
        if remaining_ttl > 0:
            await set_key(cache_key, count, remaining_ttl)
            reset_seconds = remaining_ttl
        else:
            # Window expired during operation, start new window
            count = 1
            await set_key(cache_key, count, window_seconds)
            reset_seconds = window_seconds

        # Check if limit exceeded
        is_limited = count > max_requests

        if is_limited:
            logger.warning(
                "Rate limit exceeded",
                key=key,
                count=count,
                max_requests=max_requests,
                reset_seconds=reset_seconds,
            )

        return is_limited, count, reset_seconds

    async def _get_ttl(self, key: str) -> int:
        """
        Get the remaining TTL for a cache key.

        Args:
            key: The cache key

        Returns:
            Remaining TTL in seconds, 0 if expired or not found
        """
        try:
            import redis.asyncio as redis
            from app.core.cache.manager import get_redis_pool

            # Get Redis connection from pool
            redis_conn = redis.Redis(connection_pool=get_redis_pool())
            ttl = await redis_conn.ttl(key)

            # TTL returns -2 if key doesn't exist, -1 if no expiry
            if ttl < 0:
                return 0

            return ttl
        except Exception as e:
            logger.error(f"Error getting TTL: {str(e)}")
            return 0
