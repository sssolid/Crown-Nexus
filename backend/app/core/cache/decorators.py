# /backend/app/core/cache/decorators.py
from __future__ import annotations

import asyncio
import functools
import inspect
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

from app.core.cache.keys import generate_cache_key
from app.core.cache.manager import cache_manager
from app.core.logging import get_logger

F = TypeVar('F', bound=Callable[..., Any])

logger = get_logger("app.core.cache.decorators")

def cached(
    ttl: Optional[int] = 300,
    prefix: str = "cache",
    backend: Optional[str] = None,
    skip_args: Optional[List[int]] = None,
    skip_kwargs: Optional[List[str]] = None
) -> Callable[[F], F]:
    """Decorator for caching function results.
    
    This decorator can be used on both synchronous and asynchronous functions.
    
    Args:
        ttl: Time-to-live in seconds (None for no expiration)
        prefix: Cache key prefix
        backend: Cache backend to use
        skip_args: Indices of positional arguments to skip
        skip_kwargs: Names of keyword arguments to skip
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func: F) -> F:
        # Check if function is coroutine
        is_coroutine = asyncio.iscoroutinefunction(func)
        
        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Generate cache key
                key = generate_cache_key(
                    prefix,
                    func,
                    args,
                    kwargs,
                    skip_args,
                    skip_kwargs
                )
                
                # Try to get cached value
                cached_value = await cache_manager.get(key, backend)
                
                # If found, return cached value
                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {key}")
                    return cached_value
                    
                # If not found, call function and cache result
                logger.debug(f"Cache miss for key: {key}")
                result = await func(*args, **kwargs)
                
                # Cache result
                await cache_manager.set(key, result, ttl, backend)
                
                return result
                
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Generate cache key
                key = generate_cache_key(
                    prefix,
                    func,
                    args,
                    kwargs,
                    skip_args,
                    skip_kwargs
                )
                
                # Try to get cached value
                cached_value = asyncio.run(cache_manager.get(key, backend))
                
                # If found, return cached value
                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {key}")
                    return cached_value
                    
                # If not found, call function and cache result
                logger.debug(f"Cache miss for key: {key}")
                result = func(*args, **kwargs)
                
                # Cache result
                asyncio.run(cache_manager.set(key, result, ttl, backend))
                
                return result
                
            return cast(F, sync_wrapper)
            
    return decorator

def invalidate_cache(
    pattern: str,
    prefix: str = "cache",
    backend: Optional[str] = None
) -> Callable[[F], F]:
    """Decorator for invalidating cache entries matching a pattern.
    
    This decorator can be used on both synchronous and asynchronous functions.
    
    Args:
        pattern: Cache key pattern to invalidate
        prefix: Cache key prefix
        backend: Cache backend to use
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func: F) -> F:
        # Check if function is coroutine
        is_coroutine = asyncio.iscoroutinefunction(func)
        
        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Call function
                result = await func(*args, **kwargs)
                
                # Invalidate cache
                pattern_key = f"{prefix}:{pattern}"
                count = await cache_manager.invalidate_pattern(pattern_key, backend)
                
                logger.debug(f"Invalidated {count} cache entries matching pattern: {pattern_key}")
                
                return result
                
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Call function
                result = func(*args, **kwargs)
                
                # Invalidate cache
                pattern_key = f"{prefix}:{pattern}"
                count = asyncio.run(cache_manager.invalidate_pattern(pattern_key, backend))
                
                logger.debug(f"Invalidated {count} cache entries matching pattern: {pattern_key}")
                
                return result
                
            return cast(F, sync_wrapper)
            
    return decorator

def cache_aside(
    key_func: Callable[..., str],
    ttl: Optional[int] = 300,
    backend: Optional[str] = None
) -> Callable[[F], F]:
    """Decorator for implementing the cache-aside pattern.
    
    This decorator is used for functions that fetch data from a slow data source.
    It tries to get data from the cache first, and if not found, fetches from
    the data source and caches the result.
    
    Args:
        key_func: Function to generate cache key from arguments
        ttl: Time-to-live in seconds (None for no expiration)
        backend: Cache backend to use
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func: F) -> F:
        # Check if function is coroutine
        is_coroutine = asyncio.iscoroutinefunction(func)
        
        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Generate cache key
                key = key_func(*args, **kwargs)
                
                # Try to get cached value
                cached_value = await cache_manager.get(key, backend)
                
                # If found, return cached value
                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {key}")
                    return cached_value
                    
                # If not found, call function and cache result
                logger.debug(f"Cache miss for key: {key}")
                result = await func(*args, **kwargs)
                
                # Cache result if not None
                if result is not None:
                    await cache_manager.set(key, result, ttl, backend)
                
                return result
                
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                # Generate cache key
                key = key_func(*args, **kwargs)
                
                # Try to get cached value
                cached_value = asyncio.run(cache_manager.get(key, backend))
                
                # If found, return cached value
                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {key}")
                    return cached_value
                    
                # If not found, call function and cache result
                logger.debug(f"Cache miss for key: {key}")
                result = func(*args, **kwargs)
                
                # Cache result if not None
                if result is not None:
                    asyncio.run(cache_manager.set(key, result, ttl, backend))
                
                return result
                
            return cast(F, sync_wrapper)
            
    return decorator

def memoize(
    ttl: Optional[int] = None,
    max_size: int = 128
) -> Callable[[F], F]:
    """Decorator for memoizing function results in memory.
    
    This decorator is used for caching function results in memory,
    similar to functools.lru_cache but with TTL support.
    
    Args:
        ttl: Time-to-live in seconds (None for no expiration)
        max_size: Maximum number of items to store in the cache
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func: F) -> F:
        # Use memory cache backend
        return cached(
            ttl=ttl,
            prefix=f"memoize:{func.__module__}.{func.__qualname__}",
            backend="memory"
        )(func)
        
    return decorator
