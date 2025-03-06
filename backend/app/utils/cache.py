# backend/app/utils/cache.py
"""
Caching utility functions.

This module provides a caching layer for expensive operations:
- Redis-based caching for database queries
- In-memory caching for frequently accessed data
- Cache key generation and management
- Cache invalidation utilities

These utilities improve application performance by reducing
database load and computation time.
"""

from __future__ import annotations

import functools
import hashlib
import inspect
import json
import pickle
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, cast

import redis.asyncio as redis
from fastapi import Depends, Request

from app.core.config import settings

# Type variable for the cached function
F = TypeVar('F', bound=Callable[..., Any])
RT = TypeVar('RT')  # Return type


# Redis client instance
redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """
    Get Redis client instance.

    Creates a new connection if one doesn't exist.

    Returns:
        redis.Redis: Redis client
    """
    global redis_client

    if redis_client is None:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=False,  # Need binary data for pickle
        )

    return redis_client


def generate_cache_key(
    prefix: str, func: Callable[..., Any], args: Tuple[Any, ...], kwargs: Dict[str, Any]
) -> str:
    """
    Generate a cache key for a function call.

    Args:
        prefix: Key prefix
        func: Function
        args: Function arguments
        kwargs: Function keyword arguments

    Returns:
        str: Cache key
    """
    # Get function name
    func_name = f"{func.__module__}.{func.__qualname__}"

    # Create a string representation of arguments
    arg_str = str(args) + str(sorted(kwargs.items()))

    # Create a hash of the arguments
    arg_hash = hashlib.md5(arg_str.encode()).hexdigest()

    # Combine prefix, function name, and argument hash
    return f"{prefix}:{func_name}:{arg_hash}"


def redis_cache(
    prefix: str = "cache", ttl: int = 300, skip_args: List[str] = None
) -> Callable[[F], F]:
    """
    Decorator for Redis caching.

    Args:
        prefix: Cache key prefix
        ttl: Time-to-live in seconds
        skip_args: List of argument names to skip when generating cache key

    Returns:
        Callable: Decorator function
    """
    skip_args = skip_args or ["self", "cls", "db", "request"]

    def decorator(func: F) -> F:
        """
        Decorator function.

        Args:
            func: Function to decorate

        Returns:
            F: Decorated function
        """
        signature = inspect.signature(func)

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function.

            Args:
                *args: Function arguments
                **kwargs: Function keyword arguments

            Returns:
                Any: Function result
            """
            # Skip caching for certain arguments
            cache_kwargs = {k: v for k, v in kwargs.items() if k not in skip_args}

            # Convert positional arguments to keyword arguments based on function signature
            bound_args = signature.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()
            arg_dict = bound_args.arguments

            # Filter out skipped arguments
            filtered_args = {k: v for k, v in arg_dict.items() if k not in skip_args}

            # Generate cache key
            key = generate_cache_key(prefix, func, (), filtered_args)

            # Get Redis client
            redis_conn = await get_redis()

            # Try to get from cache
            cached_data = await redis_conn.get(key)
            if cached_data:
                return pickle.loads(cached_data)

            # Execute function
            result = await func(*args, **kwargs)

            # Cache result
            await redis_conn.set(key, pickle.dumps(result), ex=ttl)

            return result

        return cast(F, wrapper)

    return decorator


def memory_cache(maxsize: int = 128, ttl: int = 300) -> Callable[[F], F]:
    """
    Decorator for in-memory caching with TTL.

    Args:
        maxsize: Maximum cache size
        ttl: Time-to-live in seconds

    Returns:
        Callable: Decorator function
    """
    cache: Dict[str, Tuple[float, Any]] = {}

    def decorator(func: F) -> F:
        """
        Decorator function.

        Args:
            func: Function to decorate

        Returns:
            F: Decorated function
        """
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function.

            Args:
                *args: Function arguments
                **kwargs: Function keyword arguments

            Returns:
                Any: Function result
            """
            # Generate cache key
            key = generate_cache_key("memory", func, args, kwargs)

            import time
            current_time = time.time()

            # Check cache
            if key in cache:
                timestamp, value = cache[key]
                if current_time - timestamp < ttl:
                    return value

            # Execute function
            result = await func(*args, **kwargs)

            # Update cache
            cache[key] = (current_time, result)

            # Prune cache if needed
            if len(cache) > maxsize:
                # Remove oldest entries
                items = sorted(cache.items(), key=lambda x: x[1][0])
                for old_key, _ in items[:len(cache) - maxsize]:
                    del cache[old_key]

            return result

        return cast(F, wrapper)

    return decorator


async def invalidate_cache(
    prefix: str, pattern: str = "*", redis_conn: Optional[redis.Redis] = None
) -> int:
    """
    Invalidate cache keys matching a pattern.

    Args:
        prefix: Cache key prefix
        pattern: Key pattern
        redis_conn: Redis client

    Returns:
        int: Number of keys deleted
    """
    if redis_conn is None:
        redis_conn = await get_redis()

    # Find keys matching pattern
    keys = await redis_conn.keys(f"{prefix}:{pattern}")

    # Delete keys
    if keys:
        return await redis_conn.delete(*keys)

    return 0


# Request-specific cache (useful for caching during a single request lifecycle)
class RequestCache:
    """
    Cache for the current request lifecycle.

    This class provides a way to cache data during a single request,
    which can be useful for repeated database queries or expensive
    computations within the same request.
    """
    def __init__(self) -> None:
        """Initialize an empty cache."""
        self.cache: Dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Optional[Any]: Cached value or None
        """
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = value

    def delete(self, key: str) -> None:
        """
        Delete value from cache.

        Args:
            key: Cache key
        """
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        """Clear all cached values."""
        self.cache.clear()


def get_request_cache(request: Request) -> RequestCache:
    """
    Get or create a RequestCache instance for the current request.

    Args:
        request: FastAPI request

    Returns:
        RequestCache: Request cache
    """
    if not hasattr(request.state, "cache"):
        request.state.cache = RequestCache()
    return request.state.cache
