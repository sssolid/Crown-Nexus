from __future__ import annotations

"""Rate limiting functionality.

This module provides functions for implementing rate limiting to protect
against abuse and DoS attacks.
"""

import time
from typing import Tuple

from app.core.logging import get_logger
from app.core.exceptions import RateLimitException
from app.utils.redis_manager import get_key, set_key

logger = get_logger(__name__)


async def check_rate_limit(
    key: str, max_requests: int, window_seconds: int
) -> Tuple[bool, int, int]:
    """Check if a rate limit has been exceeded.

    Args:
        key: The rate limit key.
        max_requests: The maximum number of requests allowed in the time window.
        window_seconds: The time window in seconds.

    Returns:
        Tuple[bool, int, int]: A tuple containing a boolean indicating if the rate limit has been
            exceeded, the current request count, and the reset time in seconds.
    """
    rate_limit_prefix = "rate_limit:"
    window_start = int(time.time() / window_seconds) * window_seconds
    cache_key = f"{rate_limit_prefix}{key}:{window_start}"

    current = await get_key(cache_key)

    if current is None:
        count = 1
        await set_key(cache_key, count, window_seconds)
        reset_seconds = window_seconds
        return (False, count, reset_seconds)

    count = int(current) + 1
    remaining_ttl = await _get_ttl(cache_key)

    if remaining_ttl > 0:
        await set_key(cache_key, count, remaining_ttl)
        reset_seconds = remaining_ttl
    else:
        count = 1
        await set_key(cache_key, count, window_seconds)
        reset_seconds = window_seconds

    is_limited = count > max_requests

    if is_limited:
        logger.warning(
            "Rate limit exceeded",
            extra={
                "key": key,
                "count": count,
                "max_requests": max_requests,
                "reset_seconds": reset_seconds,
            },
        )

    return (is_limited, count, reset_seconds)


async def _get_ttl(key: str) -> int:
    """Get the TTL of a key in Redis.

    Args:
        key: The key to get the TTL for.

    Returns:
        int: The TTL in seconds, or 0 if the key doesn't exist or an error occurs.
    """
    try:
        import redis.asyncio as redis
        from app.core.cache.manager import get_redis_pool

        redis_conn = redis.Redis(connection_pool=get_redis_pool())
        ttl = await redis_conn.ttl(key)

        if ttl < 0:
            return 0

        return ttl

    except Exception as e:
        logger.error(f"Error getting TTL: {str(e)}")
        return 0


class RateLimitManager:
    """Manager for rate limiting functionality."""

    def __init__(self) -> None:
        """Initialize the rate limit manager."""
        self.rate_limit_prefix = "rate_limit:"

    async def check_rate_limit(
        self, key: str, max_requests: int, window_seconds: int
    ) -> Tuple[bool, int, int]:
        """Check if a rate limit has been exceeded.

        Args:
            key: The rate limit key.
            max_requests: The maximum number of requests allowed in the time window.
            window_seconds: The time window in seconds.

        Returns:
            Tuple[bool, int, int]: A tuple containing a boolean indicating if the rate limit has been
                exceeded, the current request count, and the reset time in seconds.
        """
        return await check_rate_limit(key, max_requests, window_seconds)

    async def _get_ttl(self, key: str) -> int:
        """Get the TTL of a key in Redis.

        Args:
            key: The key to get the TTL for.

        Returns:
            int: The TTL in seconds, or 0 if the key doesn't exist or an error occurs.
        """
        return await _get_ttl(key)
