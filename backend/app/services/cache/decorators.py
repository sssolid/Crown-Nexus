# backend/app/services/cache/decorators.py
"""Cache decorators for function memoization.

This module provides decorators for caching function results,
supporting both synchronous and asynchronous functions.
"""
from __future__ import annotations

import asyncio
import functools
import inspect
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union, cast

from app.core.logging import get_logger
from app.services.cache.base import F
from app.services.cache.keys import generate_cache_key

logger = get_logger(__name__)


def cached(
    prefix: Optional[str] = None,
    ttl: int = 300,
    backend: str = "memory",
    skip_args: Optional[List[str]] = None,
    force_refresh: bool = False,
    cache_none: bool = False,
) -> Callable[[F], F]:
    """
    Decorator for caching function results.

    Args:
        prefix: Namespace prefix for cache keys
        ttl: Time-to-live in seconds
        backend: Cache backend to use
        skip_args: List of argument names to exclude from key generation
        force_refresh: Force refresh of cache
        cache_none: Whether to cache None results

    Returns:
        Decorator function
    """

    def decorator(func: F) -> F:
        """Decorator that caches function results."""
        is_async = asyncio.iscoroutinefunction(func)

        if is_async:

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Only import here to avoid circular imports
                from app.services.cache.service import CacheService

                # Get cache service instance
                cache_service = CacheService()
                await cache_service.ensure_initialized()

                # Generate cache key
                key = generate_cache_key(
                    prefix or func.__name__, func, args, kwargs, skip_args
                )

                if force_refresh:
                    # Bypass cache
                    result = await func(*args, **kwargs)
                    if result is not None or cache_none:
                        await cache_service.set(key, result, ttl, backend=backend)
                    return result

                # Try to get from cache
                cached_result = await cache_service.get(key, backend=backend)
                if cached_result is not None:
                    return cached_result

                # Cache miss, call function
                result = await func(*args, **kwargs)

                # Store result in cache if it's not None or cache_none is True
                if result is not None or cache_none:
                    await cache_service.set(key, result, ttl, backend=backend)

                return result

            return cast(F, async_wrapper)
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                # For sync functions, we still need to run this in an event loop
                async def _get_cached() -> Any:
                    # Only import here to avoid circular imports
                    from app.services.cache.service import CacheService

                    # Get cache service instance
                    cache_service = CacheService()
                    await cache_service.ensure_initialized()

                    # Generate cache key
                    key = generate_cache_key(
                        prefix or func.__name__, func, args, kwargs, skip_args
                    )

                    if force_refresh:
                        # Bypass cache
                        result = func(*args, **kwargs)
                        if result is not None or cache_none:
                            await cache_service.set(key, result, ttl, backend=backend)
                        return result

                    # Try to get from cache
                    cached_result = await cache_service.get(key, backend=backend)
                    if cached_result is not None:
                        return cached_result

                    # Cache miss, call function
                    result = func(*args, **kwargs)

                    # Store result in cache if it's not None or cache_none is True
                    if result is not None or cache_none:
                        await cache_service.set(key, result, ttl, backend=backend)

                    return result

                # Run in event loop
                loop = asyncio.get_event_loop()
                return loop.run_until_complete(_get_cached())

            return cast(F, sync_wrapper)

    return decorator


def cache_invalidate(
    prefix: Optional[str] = None,
    backends: Optional[List[str]] = None,
    key_func: Optional[Callable[..., str]] = None,
) -> Callable[[F], F]:
    """
    Decorator for invalidating cache entries.

    Args:
        prefix: Namespace prefix for cache keys
        backends: List of cache backends to invalidate
        key_func: Function to generate cache key from function arguments

    Returns:
        Decorator function
    """

    def decorator(func: F) -> F:
        """Decorator that invalidates cache entries."""
        is_async = asyncio.iscoroutinefunction(func)

        if is_async:

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Call the wrapped function first
                result = await func(*args, **kwargs)

                # Then invalidate cache
                await _invalidate_cache(prefix, backends, key_func, args, kwargs)

                return result

            return cast(F, async_wrapper)
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Call the wrapped function first
                result = func(*args, **kwargs)

                # Then invalidate cache
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    _invalidate_cache(prefix, backends, key_func, args, kwargs)
                )

                return result

            return cast(F, sync_wrapper)

    return decorator


async def _invalidate_cache(
    prefix: Optional[str],
    backends: Optional[List[str]],
    key_func: Optional[Callable[..., str]],
    args: Any,
    kwargs: Any,
) -> None:
    """
    Helper function to invalidate cache entries.

    Args:
        prefix: Namespace prefix for cache keys
        backends: List of cache backends to invalidate
        key_func: Function to generate cache key
        args: Function arguments
        kwargs: Function keyword arguments
    """
    # Only import here to avoid circular imports
    from app.services.cache.service import CacheService

    # Get cache service instance
    cache_service = CacheService()
    await cache_service.ensure_initialized()

    # Determine backends to invalidate
    cache_backends = backends or ["memory", "redis"]

    # Generate key if key_func is provided
    if key_func:
        key = key_func(*args, **kwargs)

        # Delete from each backend
        for backend in cache_backends:
            await cache_service.delete(key, backend=backend)
    elif prefix:
        # If only prefix is provided, clear all keys with that prefix
        # This is more of a wildcard invalidation
        for backend in cache_backends:
            # Using the backend-specific clear_prefix method
            # This isn't part of the base CacheBackend protocol but is a useful extension
            await cache_service.clear_prefix(prefix, backend=backend)
