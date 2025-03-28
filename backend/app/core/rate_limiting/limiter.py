# /app/core/rate_limiting/limiter.py
"""Rate limiter implementation.

This module provides the core rate limiting functionality with support for
both in-memory and Redis-based rate limiting.
"""

from __future__ import annotations

import time
from typing import Dict, Optional, Tuple

from fastapi import Request

from app.core.config import settings
from app.logging import get_logger
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.utils.redis_manager import get_redis_client, increment_counter

logger = get_logger("app.core.rate_limiting.limiter")


class RateLimiter:
    """Rate limiter implementation for API request throttling.

    This class provides rate limiting functionality with support for different
    strategies and storage backends (in-memory or Redis).

    Attributes:
        use_redis: Whether to use Redis for distributed rate limiting
        prefix: Key prefix for Redis storage
        default_rule: Default rate limit rule
        _counters: In-memory storage for rate limiting counters
    """

    def __init__(
        self,
        use_redis: Optional[bool] = None,
        prefix: str = "ratelimit",
        default_rule: Optional[RateLimitRule] = None,
    ) -> None:
        """Initialize the rate limiter.

        Args:
            use_redis: Whether to use Redis for distributed rate limiting
            prefix: Key prefix for Redis storage
            default_rule: Default rate limit rule
        """
        self.use_redis: bool = (
            use_redis
            if use_redis is not None
            else (
                settings.RATE_LIMIT_STORAGE == "redis"
                and settings.REDIS_HOST is not None
            )
        )
        self.prefix: str = prefix
        self.default_rule: RateLimitRule = default_rule or RateLimitRule(
            requests_per_window=settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
            window_seconds=60,
        )

        # In-memory storage for rate limiting when Redis is not available
        self._counters: Dict[str, Dict[float, int]] = {}

        logger.info(
            f"RateLimiter initialized with strategy={self.default_rule.strategy}, "
            f"limit={self.default_rule.requests_per_window} requests per "
            f"{self.default_rule.window_seconds}s"
        )

    async def is_rate_limited(
        self, key: str, rule: Optional[RateLimitRule] = None
    ) -> Tuple[bool, int, int]:
        """Check if a key is rate limited.

        Args:
            key: The rate limiting key
            rule: Rate limit rule to apply

        Returns:
            Tuple[bool, int, int]: (is_limited, current_count, limit)
        """
        rule = rule or self.default_rule
        window_key: str = self._get_window_key(key, rule)

        # Use Redis if available
        if self.use_redis:
            try:
                redis_client = await get_redis_client()
                current_count = await increment_counter(
                    window_key, 1, rule.window_seconds
                )

                if current_count is None:
                    # Redis operation failed, fallback to in-memory
                    logger.warning(
                        "Redis rate limiting failed, using in-memory fallback"
                    )
                    return await self._check_in_memory(key, rule)

                is_limited = current_count > rule.requests_per_window
                return is_limited, current_count, rule.requests_per_window

            except Exception as e:
                logger.error(f"Redis rate limiting error: {str(e)}")
                return await self._check_in_memory(key, rule)

        # Use in-memory rate limiting
        return await self._check_in_memory(key, rule)

    async def _check_in_memory(
        self, key: str, rule: RateLimitRule
    ) -> Tuple[bool, int, int]:
        """Check rate limits using in-memory storage.

        Args:
            key: The rate limiting key
            rule: Rate limit rule to apply

        Returns:
            Tuple[bool, int, int]: (is_limited, current_count, limit)
        """
        now: float = time.time()
        window_start: float = now - rule.window_seconds

        # Initialize counter if needed
        if key not in self._counters:
            self._counters[key] = {}

        # Clean up old timestamps
        self._counters[key] = {
            ts: count for ts, count in self._counters[key].items() if ts > window_start
        }

        # Add current request
        timestamp: float = now
        if timestamp in self._counters[key]:
            self._counters[key][timestamp] += 1
        else:
            self._counters[key][timestamp] = 1

        # Count requests in current window
        current_count: int = sum(self._counters[key].values())
        is_limited: bool = current_count > rule.requests_per_window

        return is_limited, current_count, rule.requests_per_window

    def get_key_for_request(self, request: Request, rule: RateLimitRule) -> str:
        """Generate a rate limiting key for a request.

        Args:
            request: The incoming request
            rule: Rate limit rule to apply

        Returns:
            str: Rate limiting key
        """
        if rule.strategy == RateLimitStrategy.IP:
            return f"{self.prefix}:ip:{request.client.host}"

        if rule.strategy == RateLimitStrategy.USER:
            # Get user ID from request state if available
            user_id: str = getattr(request.state, "user_id", "anonymous")
            return f"{self.prefix}:user:{user_id}"

        if rule.strategy == RateLimitStrategy.COMBINED:
            user_id: str = getattr(request.state, "user_id", "anonymous")
            return f"{self.prefix}:combined:{request.client.host}:{user_id}"

        # Default to IP-based rate limiting
        return f"{self.prefix}:ip:{request.client.host}"

    def _get_window_key(self, key: str, rule: RateLimitRule) -> str:
        """Get a key for the current time window.

        Args:
            key: The base rate limiting key
            rule: Rate limit rule to apply

        Returns:
            str: Window-specific key
        """
        window: int = int(time.time() / rule.window_seconds)
        return f"{key}:{window}"
