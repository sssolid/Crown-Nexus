# /app/core/rate_limiting/__init__.py
"""Rate limiting package for preventing API abuse.

This package provides rate limiting functionality to protect the API from
abuse and ensure fair usage. It supports both in-memory and Redis-based
rate limiting with configurable rules and strategies.
"""

from __future__ import annotations

from app.core.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.rate_limiting.utils import check_rate_limit, get_ttl

logger = get_logger("app.core.rate_limiting")


async def initialize() -> None:
    """Initialize the rate limiting system."""
    logger.info("Initializing rate limiting system")


async def shutdown() -> None:
    """Shutdown the rate limiting system."""
    logger.info("Shutting down rate limiting system")
    # Any Redis connection cleanup could go here


__all__ = [
    # Models
    "RateLimitRule",
    "RateLimitStrategy",
    # Core functions
    "initialize",
    "shutdown",
    # Core classes
    "RateLimiter",
    # Utility functions
    "check_rate_limit",
    "get_ttl",
]
