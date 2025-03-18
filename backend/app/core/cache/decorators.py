# app/core/cache/decorators.py
from __future__ import annotations

import asyncio
import functools
import inspect
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

from app.core.cache.keys import generate_cache_key
from app.core.cache.manager import cache_manager
from app.core.logging import get_logger

F = TypeVar("F", bound=Callable[..., Any])
logger = get_logger("app.core.cache.decorators")


def cached(
    ttl: Optional[int] = 300,
    prefix: str = "cache",
    backend: Optional[str] = None,
    skip_args: Optional[List[int, str]] = None,
    skip_kwargs: Optional[List[str]] = None,
    tags: Optional[List[str]] = None
) -> Callable[[F], F]:
    """Decorator for caching function results.

    Args:
        ttl: Time-to-live in seconds
        prefix: Cache key prefix
        backend: Optional cache backend name
        skip_args: Optional list of argument indices to skip in key generation
        skip_kwargs: Optional list of keyword argument names to skip in key generation
        tags: Optional list of tags for cache invalidation

    Returns:
        Decorator function
    """
    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)

        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                key = generate_cache_key(prefix, func, args, kwargs, skip_args, skip_kwargs)
                cached_value = await cache_manager.get(key, backend)

                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {key}")
                    return cached_value

                logger.debug(f"Cache miss for key: {key}")
                result = await func(*args, **kwargs)

                if result is not None:
                    await cache_manager.set(key, result, ttl, backend)

                    # Add tags if Redis backend is available
                    if tags and "redis" in cache_manager.backends:
                        for tag in tags:
                            tag_key = f"cache:tag:{tag}"
                            redis_backend = cache_manager.backends["redis"]
                            if hasattr(redis_backend, "add_to_set"):
                                await redis_backend.add_to_set(tag_key, key)

                return result

            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                loop = asyncio.get_event_loop() if asyncio.get_event_loop_policy().get_event_loop().is_running() else asyncio.new_event_loop()

                key = generate_cache_key(prefix, func, args, kwargs, skip_args, skip_kwargs)

                # Check cache
                cached_value = loop.run_until_complete(cache_manager.get(key, backend))
                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {key}")
                    return cached_value

                logger.debug(f"Cache miss for key: {key}")
                result = func(*args, **kwargs)

                if result is not None:
                    loop.run_until_complete(cache_manager.set(key, result, ttl, backend))

                    # Add tags if Redis backend is available
                    if tags and "redis" in cache_manager.backends:
                        for tag in tags:
                            tag_key = f"cache:tag:{tag}"
                            redis_backend = cache_manager.backends["redis"]
                            if hasattr(redis_backend, "add_to_set"):
                                loop.run_until_complete(redis_backend.add_to_set(tag_key, key))

                return result

            return cast(F, sync_wrapper)

    return decorator


def invalidate_cache(
    pattern: str,
    prefix: str = "cache",
    backend: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Callable[[F], F]:
    """Decorator to invalidate cache after function execution.

    Args:
        pattern: Cache key pattern to invalidate
        prefix: Cache key prefix
        backend: Optional cache backend name
        tags: Optional list of tags to invalidate

    Returns:
        Decorator function
    """
    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)

        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                result = await func(*args, **kwargs)

                # Invalidate by pattern
                pattern_key = f"{prefix}:{pattern}"
                count = await cache_manager.invalidate_pattern(pattern_key, backend)
                logger.debug(f"Invalidated {count} cache entries matching pattern: {pattern_key}")

                # Invalidate by tags if Redis backend is available
                if tags and "redis" in cache_manager.backends:
                    for tag in tags:
                        tag_key = f"cache:tag:{tag}"
                        redis_backend = cache_manager.backends["redis"]
                        if hasattr(redis_backend, "get_set_members"):
                            keys = await redis_backend.get_set_members(tag_key)
                            if keys:
                                await cache_manager.delete_many(keys)
                                await redis_backend.delete(tag_key)
                                logger.debug(f"Invalidated tag: {tag} with {len(keys)} keys")

                return result

            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                loop = asyncio.get_event_loop() if asyncio.get_event_loop_policy().get_event_loop().is_running() else asyncio.new_event_loop()

                result = func(*args, **kwargs)

                # Invalidate by pattern
                pattern_key = f"{prefix}:{pattern}"
                count = loop.run_until_complete(cache_manager.invalidate_pattern(pattern_key, backend))
                logger.debug(f"Invalidated {count} cache entries matching pattern: {pattern_key}")

                # Invalidate by tags if Redis backend is available
                if tags and "redis" in cache_manager.backends:
                    for tag in tags:
                        tag_key = f"cache:tag:{tag}"
                        redis_backend = cache_manager.backends["redis"]
                        if hasattr(redis_backend, "get_set_members"):
                            keys = loop.run_until_complete(redis_backend.get_set_members(tag_key))
                            if keys:
                                loop.run_until_complete(cache_manager.delete_many(keys))
                                loop.run_until_complete(redis_backend.delete(tag_key))
                                logger.debug(f"Invalidated tag: {tag} with {len(keys)} keys")

                return result

            return cast(F, sync_wrapper)

    return decorator


def cache_aside(
    key_func: Callable[..., str],
    ttl: Optional[int] = 300,
    backend: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Callable[[F], F]:
    """Decorator for implementing the cache-aside pattern.

    Args:
        key_func: Function to generate cache key
        ttl: Time-to-live in seconds
        backend: Optional cache backend name
        tags: Optional list of tags for cache invalidation

    Returns:
        Decorator function
    """
    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)

        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                key = key_func(*args, **kwargs)
                cached_value = await cache_manager.get(key, backend)

                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {key}")
                    return cached_value

                logger.debug(f"Cache miss for key: {key}")
                result = await func(*args, **kwargs)

                if result is not None:
                    await cache_manager.set(key, result, ttl, backend)

                    # Add tags if Redis backend is available
                    if tags and "redis" in cache_manager.backends:
                        for tag in tags:
                            tag_key = f"cache:tag:{tag}"
                            redis_backend = cache_manager.backends["redis"]
                            if hasattr(redis_backend, "add_to_set"):
                                await redis_backend.add_to_set(tag_key, key)

                return result

            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                loop = asyncio.get_event_loop() if asyncio.get_event_loop_policy().get_event_loop().is_running() else asyncio.new_event_loop()

                key = key_func(*args, **kwargs)
                cached_value = loop.run_until_complete(cache_manager.get(key, backend))

                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {key}")
                    return cached_value

                logger.debug(f"Cache miss for key: {key}")
                result = func(*args, **kwargs)

                if result is not None:
                    loop.run_until_complete(cache_manager.set(key, result, ttl, backend))

                    # Add tags if Redis backend is available
                    if tags and "redis" in cache_manager.backends:
                        for tag in tags:
                            tag_key = f"cache:tag:{tag}"
                            redis_backend = cache_manager.backends["redis"]
                            if hasattr(redis_backend, "add_to_set"):
                                loop.run_until_complete(redis_backend.add_to_set(tag_key, key))

                return result

            return cast(F, sync_wrapper)

    return decorator


def memoize(ttl: Optional[int] = None, max_size: int = 128) -> Callable[[F], F]:
    """In-memory memoization decorator.

    Args:
        ttl: Optional time-to-live in seconds
        max_size: Maximum cache size

    Returns:
        Decorator function
    """
    return cached(
        ttl=ttl,
        prefix=f"memoize",
        backend="memory"
    )
