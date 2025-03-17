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
logger = get_logger('app.core.cache.decorators')
def cached(ttl: Optional[int]=300, prefix: str='cache', backend: Optional[str]=None, skip_args: Optional[List[int]]=None, skip_kwargs: Optional[List[str]]=None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)
        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                key = generate_cache_key(prefix, func, args, kwargs, skip_args, skip_kwargs)
                cached_value = await cache_manager.get(key, backend)
                if cached_value is not None:
                    logger.debug(f'Cache hit for key: {key}')
                    return cached_value
                logger.debug(f'Cache miss for key: {key}')
                result = await func(*args, **kwargs)
                await cache_manager.set(key, result, ttl, backend)
                return result
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                key = generate_cache_key(prefix, func, args, kwargs, skip_args, skip_kwargs)
                cached_value = asyncio.run(cache_manager.get(key, backend))
                if cached_value is not None:
                    logger.debug(f'Cache hit for key: {key}')
                    return cached_value
                logger.debug(f'Cache miss for key: {key}')
                result = func(*args, **kwargs)
                asyncio.run(cache_manager.set(key, result, ttl, backend))
                return result
            return cast(F, sync_wrapper)
    return decorator
def invalidate_cache(pattern: str, prefix: str='cache', backend: Optional[str]=None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)
        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                result = await func(*args, **kwargs)
                pattern_key = f'{prefix}:{pattern}'
                count = await cache_manager.invalidate_pattern(pattern_key, backend)
                logger.debug(f'Invalidated {count} cache entries matching pattern: {pattern_key}')
                return result
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)
                pattern_key = f'{prefix}:{pattern}'
                count = asyncio.run(cache_manager.invalidate_pattern(pattern_key, backend))
                logger.debug(f'Invalidated {count} cache entries matching pattern: {pattern_key}')
                return result
            return cast(F, sync_wrapper)
    return decorator
def cache_aside(key_func: Callable[..., str], ttl: Optional[int]=300, backend: Optional[str]=None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)
        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                key = key_func(*args, **kwargs)
                cached_value = await cache_manager.get(key, backend)
                if cached_value is not None:
                    logger.debug(f'Cache hit for key: {key}')
                    return cached_value
                logger.debug(f'Cache miss for key: {key}')
                result = await func(*args, **kwargs)
                if result is not None:
                    await cache_manager.set(key, result, ttl, backend)
                return result
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                key = key_func(*args, **kwargs)
                cached_value = asyncio.run(cache_manager.get(key, backend))
                if cached_value is not None:
                    logger.debug(f'Cache hit for key: {key}')
                    return cached_value
                logger.debug(f'Cache miss for key: {key}')
                result = func(*args, **kwargs)
                if result is not None:
                    asyncio.run(cache_manager.set(key, result, ttl, backend))
                return result
            return cast(F, sync_wrapper)
    return decorator
def memoize(ttl: Optional[int]=None, max_size: int=128) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        return cached(ttl=ttl, prefix=f'memoize:{func.__module__}.{func.__qualname__}', backend='memory')(func)
    return decorator