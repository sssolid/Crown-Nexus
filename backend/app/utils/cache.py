# app/utils/cache.py
"""
Cache utility functions for improving application performance.

This module provides various caching decorators and utilities for:
- In-memory caching with TTL
- Redis-based distributed caching
- Request-scoped caching
- Smart key generation

All functions include proper error handling, logging, and consistent cache key
generation to ensure cache operations are reliable and effective.
"""

from __future__ import annotations

import functools
import hashlib
import inspect
import json
import time
from typing import Any, Callable, Dict, List, Optional, Protocol, Set, Tuple, TypeVar, Union, cast

import redis.asyncio as redis
from fastapi import Depends, HTTPException, Request

from app.core.config import settings
from app.core.exceptions import ExternalServiceException, ErrorCode
from app.core.logging import get_logger

# Initialize structured logger
logger = get_logger("app.utils.cache")

# Type variables for functions
F = TypeVar("F", bound=Callable[..., Any])
RT = TypeVar("RT")  # Return type

# Global redis client
redis_client: Optional[redis.Redis] = None


class CacheBackend(Protocol):
    """Protocol for cache backends to standardize interface."""

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache by key."""
        ...

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        ...

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        ...

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        ...


class RedisError(ExternalServiceException):
    """Exception raised for Redis-related errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.EXTERNAL_SERVICE_ERROR,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ) -> None:
        """Initialize RedisError.

        Args:
            message: Human-readable error description
            code: Error code from ErrorCode enum
            details: Additional error context
            original_exception: Original exception that caused this error
        """
        super().__init__(
            message=message,
            code=code,
            details=details or {"service_name": "redis"},
            status_code=503,
            original_exception=original_exception,
        )


async def get_redis() -> redis.Redis:
    """Get Redis client instance (singleton).

    Returns:
        redis.Redis: Configured Redis client

    Raises:
        RedisError: If connection to Redis fails
    """
    global redis_client

    if redis_client is None:
        try:
            logger.debug(
                f"Initializing Redis connection to {settings.REDIS_HOST}:{settings.REDIS_PORT}"
            )
            redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=False,
            )
            # Test connection
            await redis_client.ping()
            logger.info("Redis connection established")
        except (redis.ConnectionError, redis.RedisError) as e:
            logger.error(f"Redis connection error: {str(e)}", exc_info=True)
            raise RedisError(
                message=f"Failed to connect to Redis: {str(e)}",
                details={"host": settings.REDIS_HOST, "port": settings.REDIS_PORT},
                original_exception=e,
            ) from e

    return redis_client


def generate_cache_key(
    prefix: str,
    func: Callable[..., Any],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    """Generate consistent cache key for function calls.

    Creates a cache key based on function name, arguments, and prefix.

    Args:
        prefix: Namespace prefix for the key
        func: Function being cached
        args: Function positional arguments
        kwargs: Function keyword arguments

    Returns:
        str: Cache key string
    """
    # Get fully qualified function name
    func_name = f"{func.__module__}.{func.__qualname__}"

    # Convert args and kwargs to strings and sort for consistency
    arg_str = str(args)
    kwarg_str = str(sorted(kwargs.items()))

    # Create a hash of the arguments
    arg_hash = hashlib.md5((arg_str + kwarg_str).encode()).hexdigest()

    # Combine components to form the key
    key = f"{prefix}:{func_name}:{arg_hash}"

    logger.debug(f"Generated cache key: {key}")
    return key


def redis_cache(
    prefix: str = "cache",
    ttl: int = 300,
    skip_args: List[str] = None
) -> Callable[[F], F]:
    """Decorator for Redis-backed function caching.

    Args:
        prefix: Namespace prefix for cache keys
        ttl: Time-to-live in seconds (default: 300)
        skip_args: List of argument names to exclude from key generation

    Returns:
        Callable: Decorated function
    """
    # Default arguments to skip (typically self, cls, db, request objects)
    skip_args = skip_args or ["self", "cls", "db", "request"]

    def decorator(func: F) -> F:
        # Get function signature for parameter analysis
        signature = inspect.signature(func)

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Filter out skipped arguments
            cache_kwargs = {k: v for k, v in kwargs.items() if k not in skip_args}

            # Bind arguments to signature and extract values
            bound_args = signature.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()
            arg_dict = bound_args.arguments
            filtered_args = {k: v for k, v in arg_dict.items() if k not in skip_args}

            # Generate key
            key = generate_cache_key(prefix, func, (), filtered_args)

            try:
                # Try to get from cache
                redis_conn = await get_redis()
                cached_data = await redis_conn.get(key)

                if cached_data:
                    # Cache hit
                    import pickle
                    value = pickle.loads(cached_data)
                    logger.debug(f"Cache hit for key: {key}")
                    return value

                # Cache miss, execute function
                logger.debug(f"Cache miss for key: {key}")
                result = await func(*args, **kwargs)

                # Cache result
                import pickle
                await redis_conn.set(key, pickle.dumps(result), ex=ttl)

                return result
            except RedisError as e:
                # Log error but don't fail - fallback to execution without caching
                logger.warning(
                    f"Redis caching failed, executing without cache: {str(e)}"
                )
                return await func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator


def memory_cache(
    maxsize: int = 128,
    ttl: int = 300
) -> Callable[[F], F]:
    """Decorator for in-memory function caching.

    Args:
        maxsize: Maximum size of cache (items)
        ttl: Time-to-live in seconds (default: 300)

    Returns:
        Callable: Decorated function
    """
    # Cache storage: key -> (timestamp, value)
    cache: Dict[str, Tuple[float, Any]] = {}

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate key
            key = generate_cache_key("memory", func, args, kwargs)
            current_time = time.time()

            # Check cache
            if key in cache:
                timestamp, value = cache[key]
                # Check if entry is still valid
                if current_time - timestamp < ttl:
                    logger.debug(f"Memory cache hit for key: {key}")
                    return value

            # Cache miss, execute function
            logger.debug(f"Memory cache miss for key: {key}")
            result = await func(*args, **kwargs)

            # Update cache
            cache[key] = (current_time, result)

            # Evict oldest entries if cache is full
            if len(cache) > maxsize:
                # Sort by timestamp (oldest first)
                items = sorted(cache.items(), key=lambda x: x[1][0])
                # Remove oldest entries
                for old_key, _ in items[:len(cache) - maxsize]:
                    del cache[old_key]

            return result

        return cast(F, wrapper)

    return decorator


async def invalidate_cache(
    prefix: str,
    pattern: str = "*",
    redis_conn: Optional[redis.Redis] = None
) -> int:
    """Invalidate cache entries matching a pattern.

    Args:
        prefix: Namespace prefix for cache keys
        pattern: Pattern to match (glob style)
        redis_conn: Redis connection (optional)

    Returns:
        int: Number of keys invalidated

    Raises:
        RedisError: If Redis operation fails
    """
    try:
        # Get Redis connection if not provided
        if redis_conn is None:
            redis_conn = await get_redis()

        # Find matching keys
        pattern_key = f"{prefix}:{pattern}"
        keys = await redis_conn.keys(pattern_key)

        if not keys:
            logger.debug(f"No keys found matching pattern: {pattern_key}")
            return 0

        # Delete keys
        count = await redis_conn.delete(*keys)
        logger.info(f"Invalidated {count} cache keys matching pattern: {pattern_key}")

        return count
    except (redis.ConnectionError, redis.RedisError) as e:
        logger.error(f"Error invalidating cache: {str(e)}", exc_info=True)
        raise RedisError(
            message=f"Failed to invalidate cache: {str(e)}",
            details={"pattern": pattern},
            original_exception=e,
        ) from e


class RequestCache:
    """Request-scoped cache for storing data during a single request."""

    def __init__(self) -> None:
        """Initialize empty cache dictionary."""
        self.cache: Dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache by key.

        Args:
            key: Cache key

        Returns:
            Optional[Any]: Cached value or None if not found
        """
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = value

    def delete(self, key: str) -> None:
        """Delete key from cache.

        Args:
            key: Cache key to delete
        """
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()


def get_request_cache(request: Request) -> RequestCache:
    """Get or create RequestCache for a request.

    Args:
        request: FastAPI request object

    Returns:
        RequestCache: Cache instance for this request
    """
    if not hasattr(request.state, "cache"):
        request.state.cache = RequestCache()

    return request.state.cache


async def cache_get_or_set(
    key: str,
    callback: Callable[[], Any],
    ttl: int = 3600,
    force_refresh: bool = False
) -> Any:
    """Get value from cache or compute and store it.

    Args:
        key: Cache key
        callback: Function to call if cache miss
        ttl: Time-to-live in seconds
        force_refresh: Force refresh of cache

    Returns:
        Any: Cached or computed value
    """
    # Skip cache lookup if force refresh
    if not force_refresh:
        cached = await get_key(key)
        if cached is not None:
            logger.debug(f"Cache hit for key: {key}")
            return cached

    # Cache miss or force refresh
    logger.debug(f"Calling callback for key: {key}")
    value = await callback()

    # Cache result
    await set_key(key, value, ttl)

    return value


async def set_key(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """Set value in Redis cache.

    Args:
        key: Cache key
        value: Value to cache
        ttl: Time-to-live in seconds

    Returns:
        bool: True if successful
    """
    try:
        client = await get_redis()
        serialized = json.dumps(value)

        if ttl:
            await client.setex(key, ttl, serialized)
        else:
            await client.set(key, serialized)

        logger.debug(f"Set cache key: {key}")
        return True
    except Exception as e:
        logger.error(f"Redis set error: {str(e)}", exc_info=True)
        return False


async def get_key(key: str, default: Optional[RT] = None) -> Optional[RT]:
    """Get value from Redis cache.

    Args:
        key: Cache key
        default: Default value if key not found

    Returns:
        Optional[RT]: Cached value or default
    """
    try:
        client = await get_redis()
        value = await client.get(key)

        if value is None:
            logger.debug(f"Cache miss for key: {key}")
            return default

        logger.debug(f"Cache hit for key: {key}")
        return cast(RT, json.loads(value.decode("utf-8")))
    except Exception as e:
        logger.error(f"Redis get error: {str(e)}", exc_info=True)
        return default


async def delete_key(key: str) -> bool:
    """Delete key from Redis cache.

    Args:
        key: Cache key

    Returns:
        bool: True if key was deleted
    """
    try:
        client = await get_redis()
        result = await client.delete(key)
        deleted = result > 0

        if deleted:
            logger.debug(f"Deleted cache key: {key}")
        else:
            logger.debug(f"Key not found for deletion: {key}")

        return deleted
    except Exception as e:
        logger.error(f"Redis delete error: {str(e)}", exc_info=True)
        return False


async def increment_counter(
    key: str,
    amount: int = 1,
    ttl: Optional[int] = None
) -> Optional[int]:
    """Increment counter in Redis.

    Args:
        key: Counter key
        amount: Amount to increment by
        ttl: Time-to-live in seconds

    Returns:
        Optional[int]: New counter value or None if failed
    """
    try:
        client = await get_redis()
        value = await client.incrby(key, amount)

        if ttl:
            await client.expire(key, ttl)

        logger.debug(f"Incremented counter {key} by {amount} to {value}")
        return value
    except Exception as e:
        logger.error(f"Redis increment error: {str(e)}", exc_info=True)
        return None


async def rate_limit_check(
    key: str,
    limit: int,
    window: int
) -> Tuple[bool, int]:
    """Check if rate limit is exceeded.

    Args:
        key: Rate limit key
        limit: Maximum number of operations
        window: Time window in seconds

    Returns:
        Tuple[bool, int]: (is_limited, current_count)
    """
    try:
        client = await get_redis()

        # Check if key exists
        current = await client.get(key)
        if current is None:
            # First request, initialize counter
            await client.setex(key, window, 1)
            logger.debug(f"Rate limit counter initialized: {key}")
            return (False, 1)

        # Increment counter
        count = await client.incr(key)

        # Check if limit exceeded
        if count > limit:
            logger.warning(f"Rate limit exceeded for {key}: {count}/{limit}")
            return (True, count)

        logger.debug(f"Rate limit check passed for {key}: {count}/{limit}")
        return (False, count)
    except Exception as e:
        logger.error(f"Redis rate limit error: {str(e)}", exc_info=True)
        # Fail open (don't block) if Redis is down
        return (False, 0)


async def publish_message(channel: str, message: Dict[str, Any]) -> bool:
    """Publish message to Redis channel.

    Args:
        channel: Channel name
        message: Message to publish

    Returns:
        bool: True if message was published
    """
    try:
        client = await get_redis()
        receivers = await client.publish(channel, json.dumps(message))

        if receivers > 0:
            logger.debug(f"Published message to {channel} with {receivers} receivers")
        else:
            logger.warning(f"No receivers for message on channel {channel}")

        return receivers > 0
    except Exception as e:
        logger.error(f"Redis publish error: {str(e)}", exc_info=True)
        return False
