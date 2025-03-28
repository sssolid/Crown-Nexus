# app/core/rate_limiting/__init__.py
from __future__ import annotations

"""
Rate limiting package for application-wide rate limiting.

This package provides core functionality for limiting request rates
using both in-memory and Redis-based implementations.
"""

from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.rate_limiting.utils import check_rate_limit, get_ttl
from app.core.rate_limiting.exceptions import (
    RateLimitingException,
    RateLimitExceededException,
    RateLimitingServiceException,
    RateLimitingConfigurationException,
)
from app.core.rate_limiting.service import (
    RateLimitingService,
    get_rate_limiting_service,
)

logger = get_logger("app.core.rate_limiting.__init__")


async def initialize() -> None:
    """Initialize the rate limiting system.

    This function is called during application startup.
    """
    logger.info("Initializing rate limiting system")

    # Initialize rate limiting service
    rate_limiting_service = get_rate_limiting_service()
    await rate_limiting_service.initialize()

    # Register with metrics system if available
    try:
        from app.core.dependency_manager import get_dependency

        metrics_service = get_dependency("metrics_service")

        # Create rate limiting metrics
        metrics_service.create_counter(
            "rate_limit_exceeded_total",
            "Total number of requests that exceeded rate limits",
            ["path", "client_host"],
        )
        metrics_service.create_counter(
            "rate_limiting_requests_total",
            "Total number of requests processed by rate limiting",
            ["limited"],
        )
        metrics_service.create_histogram(
            "rate_limiting_middleware_duration_seconds",
            "Time spent in rate limiting middleware",
            ["limited"],
        )
        metrics_service.create_histogram(
            "rate_limiting_check_duration_seconds",
            "Time spent checking rate limits",
            ["storage", "error"],
        )
        metrics_service.create_counter(
            "rate_limiting_checks_total",
            "Total number of rate limit checks performed",
            ["storage", "error"],
        )

        logger.info("Rate limiting metrics registered")
    except Exception as e:
        logger.debug(f"Could not register rate limiting metrics: {str(e)}")

    logger.info("Rate limiting system initialized")


async def shutdown() -> None:
    """Shut down the rate limiting system.

    This function is called during application shutdown.
    """
    logger.info("Shutting down rate limiting system")

    # Shut down rate limiting service
    rate_limiting_service = get_rate_limiting_service()
    await rate_limiting_service.shutdown()

    logger.info("Rate limiting system shut down")


__all__ = [
    "RateLimitRule",
    "RateLimitStrategy",
    "RateLimiter",
    "initialize",
    "shutdown",
    "check_rate_limit",
    "get_ttl",
    "RateLimitingException",
    "RateLimitExceededException",
    "RateLimitingServiceException",
    "RateLimitingConfigurationException",
    "RateLimitingService",
    "get_rate_limiting_service",
]
