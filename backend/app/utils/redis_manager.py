"""
Core Redis utility functions with proper error handling and structured logging.

This module provides functions for interacting with Redis, including connection management,
caching operations, and utility functions to simplify common Redis operations.
"""

from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, TypeVar, cast

import redis.asyncio as redis
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from app.core.config import settings
from app.core.exceptions import ServiceException, ErrorCode
from app.core.logging import get_logger

logger = get_logger("app.utils.redis_manager")

T = TypeVar("T")
_redis_pool: Optional[ConnectionPool] = None


async def get_redis_pool() -> ConnectionPool:
    """Get or create a Redis connection pool.

    Returns:
        ConnectionPool: A Redis connection pool instance.

    Raises:
        ServiceException: If unable to connect to Redis.
    """
    global _redis_pool
    if _redis_pool is None:
        try:
            _redis_pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
            )
            logger.info(
                "Created Redis connection pool",
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
            )
        except Exception as e:
            logger.error(
                "Failed to create Redis connection pool",
                error=str(e),
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                exc_info=True,
            )
            raise ServiceException(
                message="Failed to connect to Redis",
                code=ErrorCode.EXTERNAL_SERVICE_ERROR,
                details={
                    "service": "redis",
                    "host": settings.REDIS_HOST,
                    "port": settings.REDIS_PORT,
                },
                original_exception=e,
            ) from e
    return _redis_pool


async def get_redis_client() -> Redis:
    """Get a Redis client from the connection pool.

    Returns:
        Redis: A Redis client instance.

    Raises:
        ServiceException: If unable to connect to Redis.
    """
    try:
        pool = await get_redis_pool()
        return redis.Redis(connection_pool=pool)
    except ServiceException:
        raise
    except Exception as e:
        logger.error("Failed to get Redis client", error=str(e), exc_info=True)
        raise ServiceException(
            message="Failed to get Redis client",
            code=ErrorCode.EXTERNAL_SERVICE_ERROR,
            details={"service": "redis"},
            original_exception=e,
        ) from e


async def set_key(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """Set a key in Redis with optional TTL.

    Args:
        key: The Redis key.
        value: The value to store (will be JSON serialized).
        ttl: Optional TTL in seconds.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        client = await get_redis_client()
        serialized = json.dumps(value)
        if ttl:
            await client.setex(key, ttl, serialized)
        else:
            await client.set(key, serialized)
        logger.debug("Redis key set", key=key, ttl=ttl)
        return True
    except Exception as e:
        logger.error("Redis set error", key=key, error=str(e), exc_info=True)
        return False


async def get_key(key: str, default: Optional[T] = None) -> Optional[T]:
    """Get a key from Redis.

    Args:
        key: The Redis key.
        default: Default value if key doesn't exist.

    Returns:
        The stored value or default.
    """
    try:
        client = await get_redis_client()
        value = await client.get(key)
        if value is None:
            logger.debug("Redis key not found", key=key)
            return default

        logger.debug("Redis key retrieved", key=key)
        return cast(T, json.loads(value))
    except Exception as e:
        logger.error("Redis get error", key=key, error=str(e), exc_info=True)
        return default


async def delete_key(key: str) -> bool:
    """Delete a key from Redis.

    Args:
        key: The Redis key.

    Returns:
        bool: True if key was deleted, False otherwise.
    """
    try:
        client = await get_redis_client()
        result = await client.delete(key)
        success = result > 0
        if success:
            logger.debug("Redis key deleted", key=key)
        else:
            logger.debug("Redis key not found for deletion", key=key)
        return success
    except Exception as e:
        logger.error("Redis delete error", key=key, error=str(e), exc_info=True)
        return False


async def increment_counter(
    key: str, amount: int = 1, ttl: Optional[int] = None
) -> Optional[int]:
    """Increment a counter in Redis.

    Args:
        key: The Redis key.
        amount: Amount to increment by.
        ttl: Optional TTL in seconds.

    Returns:
        int: New counter value, or None if operation failed.
    """
    try:
        client = await get_redis_client()
        value = await client.incrby(key, amount)
        if ttl:
            await client.expire(key, ttl)
        logger.debug(
            "Redis counter incremented", key=key, amount=amount, new_value=value
        )
        return value
    except Exception as e:
        logger.error("Redis increment error", key=key, error=str(e), exc_info=True)
        return None


async def rate_limit_check(key: str, limit: int, window: int) -> tuple[bool, int]:
    """Check if a rate limit has been exceeded.

    Args:
        key: The rate limit key.
        limit: Maximum number of operations in the window.
        window: Time window in seconds.

    Returns:
        tuple: (is_limited, current_count)
    """
    try:
        client = await get_redis_client()
        current = await client.get(key)
        if current is None:
            await client.setex(key, window, 1)
            logger.debug("Rate limit initialized", key=key)
            return (False, 1)

        count = await client.incr(key)
        if count > limit:
            logger.warning("Rate limit exceeded", key=key, limit=limit, count=count)
            return (True, count)

        logger.debug("Rate limit check passed", key=key, count=count, limit=limit)
        return (False, count)
    except Exception as e:
        logger.error("Redis rate limit error", key=key, error=str(e), exc_info=True)
        return (False, 0)


async def publish_message(channel: str, message: Dict[str, Any]) -> bool:
    """Publish a message to a Redis channel.

    Args:
        channel: Redis channel name.
        message: Message to publish (will be JSON serialized).

    Returns:
        bool: True if message was published to at least one subscriber.
    """
    try:
        client = await get_redis_client()
        receivers = await client.publish(channel, json.dumps(message))
        if receivers > 0:
            logger.debug(
                "Redis message published", channel=channel, receivers=receivers
            )
        else:
            logger.warning("Redis message published but no receivers", channel=channel)
        return receivers > 0
    except Exception as e:
        logger.error(
            "Redis publish error", channel=channel, error=str(e), exc_info=True
        )
        return False


async def cache_get_or_set(
    key: str, callback: callable, ttl: int = 3600, force_refresh: bool = False
) -> Any:
    """Get a value from Redis or set it using the callback.

    Args:
        key: Redis key.
        callback: Async function to call if key doesn't exist.
        ttl: TTL in seconds.
        force_refresh: Force refresh the cache.

    Returns:
        The cached or newly computed value.
    """
    if not force_refresh:
        cached = await get_key(key)
        if cached is not None:
            logger.debug("Cache hit", key=key)
            return cached

    logger.debug("Cache miss, calling callback", key=key)
    value = await callback()
    await set_key(key, value, ttl)
    return value
