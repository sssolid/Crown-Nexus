from __future__ import annotations

"""
Cache decorators for function-level caching.

This module provides decorators for implementing caching at the function level,
including automatic cache key generation and invalidation.
"""

import asyncio
import functools
import time
from typing import Any, Callable, List, Optional, TypeVar, cast, Dict

from app.core.cache.keys import generate_cache_key
from app.core.cache.manager import cache_manager
from app.logging import get_logger

F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")
logger = get_logger("app.core.cache.decorators")

# Try to import metrics, but don't fail if not available
try:
    from app.core.dependency_manager import get_dependency

    HAS_METRICS = True
except ImportError:
    HAS_METRICS = False


def cached(
    ttl: Optional[int] = 300,
    prefix: str = "cache",
    backend: Optional[str] = None,
    skip_args: Optional[List[int]] = None,
    skip_kwargs: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> Callable[[F], F]:
    """Cache the result of a function.

    Args:
        ttl: Time-to-live in seconds (default: 300).
        prefix: Cache key prefix (default: 'cache').
        backend: Cache backend to use (default: None, uses default backend).
        skip_args: Argument indexes to skip when generating the cache key.
        skip_kwargs: Keyword argument names to skip when generating the cache key.
        tags: Optional tags for cache invalidation.

    Returns:
        Decorated function.
    """

    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)

        if is_coroutine:

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                cache_hit = False
                error = None
                backend_type = backend or "default"

                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency("metrics_service")
                        except Exception as e:
                            logger.debug(f"Could not get metrics service: {str(e)}")

                    key = generate_cache_key(
                        prefix, func, args, kwargs, skip_args, skip_kwargs
                    )
                    cached_value = await cache_manager.get(key, backend=backend)

                    if cached_value is not None:
                        cache_hit = True
                        logger.debug(f"Cache hit for key: {key}")
                        return cached_value

                    logger.debug(f"Cache miss for key: {key}")
                    result = await func(*args, **kwargs)

                    if result is not None:
                        await cache_manager.set(key, result, ttl, backend)

                        if tags and "redis" in cache_manager.backends:
                            for tag in tags:
                                tag_key = f"cache:tag:{tag}"
                                redis_backend = cache_manager.backends["redis"]
                                if hasattr(redis_backend, "add_to_set"):
                                    await redis_backend.add_to_set(tag_key, key)

                    return result

                except Exception as e:
                    error = str(e)
                    logger.error(
                        f"Error in cached decorator for {func.__name__}: {error}",
                        exc_info=True,
                    )
                    # Continue with function execution without caching
                    return await func(*args, **kwargs)

                finally:
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.track_cache_operation(
                                operation="cached_decorator",
                                backend=backend_type,
                                hit=cache_hit,
                                duration=duration,
                                component=func.__module__,
                            )
                        except Exception as metrics_err:
                            logger.warning(
                                f"Failed to record cache metrics: {str(metrics_err)}"
                            )

            return cast(F, async_wrapper)

        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                cache_hit = False
                error = None
                backend_type = backend or "default"

                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency("metrics_service")
                        except Exception as e:
                            logger.debug(f"Could not get metrics service: {str(e)}")

                    # Generate cache key
                    key = generate_cache_key(
                        prefix, func, args, kwargs, skip_args, skip_kwargs
                    )

                    # Try to get event loop
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        # No running loop, create a new one
                        loop = asyncio.new_event_loop()

                    # Try to get from cache
                    try:
                        cached_value = loop.run_until_complete(
                            cache_manager.get(key, backend=backend)
                        )
                        if cached_value is not None:
                            cache_hit = True
                            logger.debug(f"Cache hit for key: {key}")
                            return cached_value
                    except Exception as cache_err:
                        logger.warning(f"Error getting from cache: {str(cache_err)}")
                        # Continue without using cache

                    logger.debug(f"Cache miss for key: {key}")

                    # Execute function
                    result = func(*args, **kwargs)

                    # Cache result
                    if result is not None:
                        try:
                            loop.run_until_complete(
                                cache_manager.set(key, result, ttl, backend)
                            )

                            # Handle tags
                            if tags and "redis" in cache_manager.backends:
                                redis_backend = cache_manager.backends["redis"]
                                if hasattr(redis_backend, "add_to_set"):
                                    for tag in tags:
                                        tag_key = f"cache:tag:{tag}"
                                        loop.run_until_complete(
                                            redis_backend.add_to_set(tag_key, key)
                                        )
                        except Exception as cache_err:
                            logger.warning(f"Error setting cache: {str(cache_err)}")

                    return result

                except Exception as e:
                    error = str(e)
                    logger.error(
                        f"Error in cached decorator for {func.__name__}: {error}",
                        exc_info=True,
                    )
                    # Continue with function execution without caching
                    return func(*args, **kwargs)

                finally:
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.track_cache_operation(
                                operation="cached_decorator",
                                backend=backend_type,
                                hit=cache_hit,
                                duration=duration,
                                component=func.__module__,
                            )
                        except Exception as metrics_err:
                            logger.warning(
                                f"Failed to record cache metrics: {str(metrics_err)}"
                            )

            return cast(F, sync_wrapper)

    return decorator


def invalidate_cache(
    pattern: str,
    prefix: str = "cache",
    backend: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Callable[[F], F]:
    """Invalidate cache entries matching a pattern after function execution.

    Args:
        pattern: The pattern to match for invalidation.
        prefix: Cache key prefix (default: 'cache').
        backend: Cache backend to use (default: None, uses default backend).
        tags: Optional tags for cache invalidation.

    Returns:
        Decorated function.
    """

    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)

        if is_coroutine:

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Execute function first
                result = await func(*args, **kwargs)

                # Then invalidate cache
                try:
                    pattern_key = f"{prefix}:{pattern}"
                    count = await cache_manager.invalidate_pattern(pattern_key, backend)
                    logger.debug(
                        f"Invalidated {count} cache entries matching pattern: {pattern_key}"
                    )

                    # Handle tag-based invalidation if Redis is available
                    if tags and "redis" in cache_manager.backends:
                        redis_backend = cache_manager.backends["redis"]
                        if hasattr(redis_backend, "get_set_members"):
                            for tag in tags:
                                try:
                                    tag_key = f"cache:tag:{tag}"
                                    keys = await redis_backend.get_set_members(tag_key)
                                    if keys:
                                        await cache_manager.delete_many(keys)
                                        await redis_backend.delete(tag_key)
                                        logger.debug(
                                            f"Invalidated tag: {tag} with {len(keys)} keys"
                                        )
                                except Exception as tag_err:
                                    logger.warning(
                                        f"Error invalidating tag {tag}: {str(tag_err)}"
                                    )
                except Exception as e:
                    logger.warning(f"Error invalidating cache: {str(e)}", exc_info=True)

                return result

            return cast(F, async_wrapper)

        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Execute function first
                result = func(*args, **kwargs)

                # Then invalidate cache
                try:
                    # Try to get event loop
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        # No running loop, create a new one
                        loop = asyncio.new_event_loop()

                    # Invalidate by pattern
                    pattern_key = f"{prefix}:{pattern}"
                    count = loop.run_until_complete(
                        cache_manager.invalidate_pattern(pattern_key, backend)
                    )
                    logger.debug(
                        f"Invalidated {count} cache entries matching pattern: {pattern_key}"
                    )

                    # Handle tag-based invalidation if Redis is available
                    if tags and "redis" in cache_manager.backends:
                        redis_backend = cache_manager.backends["redis"]
                        if hasattr(redis_backend, "get_set_members"):
                            for tag in tags:
                                try:
                                    tag_key = f"cache:tag:{tag}"
                                    keys = loop.run_until_complete(
                                        redis_backend.get_set_members(tag_key)
                                    )
                                    if keys:
                                        loop.run_until_complete(
                                            cache_manager.delete_many(keys)
                                        )
                                        loop.run_until_complete(
                                            redis_backend.delete(tag_key)
                                        )
                                        logger.debug(
                                            f"Invalidated tag: {tag} with {len(keys)} keys"
                                        )
                                except Exception as tag_err:
                                    logger.warning(
                                        f"Error invalidating tag {tag}: {str(tag_err)}"
                                    )
                except Exception as e:
                    logger.warning(f"Error invalidating cache: {str(e)}", exc_info=True)

                return result

            return cast(F, sync_wrapper)

    return decorator


def cache_aside(
    key_func: Callable[..., str],
    ttl: Optional[int] = 300,
    backend: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> Callable[[F], F]:
    """Implement the cache-aside pattern with a custom key function.

    Args:
        key_func: Function that generates a cache key from function arguments.
        ttl: Time-to-live in seconds (default: 300).
        backend: Cache backend to use (default: None, uses default backend).
        tags: Optional tags for cache invalidation.

    Returns:
        Decorated function.
    """

    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)

        if is_coroutine:

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                cache_hit = False
                error = None
                backend_type = backend or "default"

                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency("metrics_service")
                        except Exception as e:
                            logger.debug(f"Could not get metrics service: {str(e)}")

                    # Generate key using the provided function
                    key = key_func(*args, **kwargs)

                    # Try to get from cache
                    cached_value = await cache_manager.get(key, backend=backend)
                    if cached_value is not None:
                        cache_hit = True
                        logger.debug(f"Cache hit for key: {key}")
                        return cached_value

                    logger.debug(f"Cache miss for key: {key}")

                    # Execute function
                    result = await func(*args, **kwargs)

                    # Cache result
                    if result is not None:
                        await cache_manager.set(key, result, ttl, backend)

                        # Handle tags
                        if tags and "redis" in cache_manager.backends:
                            redis_backend = cache_manager.backends["redis"]
                            if hasattr(redis_backend, "add_to_set"):
                                for tag in tags:
                                    tag_key = f"cache:tag:{tag}"
                                    await redis_backend.add_to_set(tag_key, key)

                    return result

                except Exception as e:
                    error = str(e)
                    logger.error(
                        f"Error in cache_aside decorator for {func.__name__}: {error}",
                        exc_info=True,
                    )
                    # Continue with function execution without caching
                    return await func(*args, **kwargs)

                finally:
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.track_cache_operation(
                                operation="cache_aside_decorator",
                                backend=backend_type,
                                hit=cache_hit,
                                duration=duration,
                                component=func.__module__,
                            )
                        except Exception as metrics_err:
                            logger.warning(
                                f"Failed to record cache metrics: {str(metrics_err)}"
                            )

            return cast(F, async_wrapper)

        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                cache_hit = False
                error = None
                backend_type = backend or "default"

                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency("metrics_service")
                        except Exception as e:
                            logger.debug(f"Could not get metrics service: {str(e)}")

                    # Generate key using the provided function
                    key = key_func(*args, **kwargs)

                    # Try to get event loop
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        # No running loop, create a new one
                        loop = asyncio.new_event_loop()

                    # Try to get from cache
                    try:
                        cached_value = loop.run_until_complete(
                            cache_manager.get(key, backend=backend)
                        )
                        if cached_value is not None:
                            cache_hit = True
                            logger.debug(f"Cache hit for key: {key}")
                            return cached_value
                    except Exception as cache_err:
                        logger.warning(f"Error getting from cache: {str(cache_err)}")

                    logger.debug(f"Cache miss for key: {key}")

                    # Execute function
                    result = func(*args, **kwargs)

                    # Cache result
                    if result is not None:
                        try:
                            loop.run_until_complete(
                                cache_manager.set(key, result, ttl, backend)
                            )

                            # Handle tags
                            if tags and "redis" in cache_manager.backends:
                                redis_backend = cache_manager.backends["redis"]
                                if hasattr(redis_backend, "add_to_set"):
                                    for tag in tags:
                                        tag_key = f"cache:tag:{tag}"
                                        loop.run_until_complete(
                                            redis_backend.add_to_set(tag_key, key)
                                        )
                        except Exception as cache_err:
                            logger.warning(f"Error setting cache: {str(cache_err)}")

                    return result

                except Exception as e:
                    error = str(e)
                    logger.error(
                        f"Error in cache_aside decorator for {func.__name__}: {error}",
                        exc_info=True,
                    )
                    # Continue with function execution without caching
                    return func(*args, **kwargs)

                finally:
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.track_cache_operation(
                                operation="cache_aside_decorator",
                                backend=backend_type,
                                hit=cache_hit,
                                duration=duration,
                                component=func.__module__,
                            )
                        except Exception as metrics_err:
                            logger.warning(
                                f"Failed to record cache metrics: {str(metrics_err)}"
                            )

            return cast(F, sync_wrapper)

    return decorator


def memoize(ttl: Optional[int] = None, max_size: int = 128) -> Callable[[F], F]:
    """Memoize a function using in-memory caching.

    Args:
        ttl: Time-to-live in seconds (default: None, meaning no expiration).
        max_size: Maximum number of items to keep in cache (default: 128).

    Returns:
        Decorated function.
    """
    return cached(ttl=ttl, prefix="memoize", backend="memory")
