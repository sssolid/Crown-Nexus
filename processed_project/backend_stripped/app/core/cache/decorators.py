from __future__ import annotations
'\nCache decorators for function-level caching.\n\nThis module provides decorators for implementing caching at the function level,\nincluding automatic cache key generation and invalidation.\n'
import asyncio
import functools
import time
from typing import Any, Callable, List, Optional, TypeVar, cast, Dict
from app.core.cache.keys import generate_cache_key
from app.core.cache.manager import cache_manager
from app.logging import get_logger
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')
logger = get_logger('app.core.cache.decorators')
try:
    from app.core.dependency_manager import get_dependency
    HAS_METRICS = True
except ImportError:
    HAS_METRICS = False
def cached(ttl: Optional[int]=300, prefix: str='cache', backend: Optional[str]=None, skip_args: Optional[List[int]]=None, skip_kwargs: Optional[List[str]]=None, tags: Optional[List[str]]=None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)
        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                cache_hit = False
                error = None
                backend_type = backend or 'default'
                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency('metrics_service')
                        except Exception as e:
                            logger.debug(f'Could not get metrics service: {str(e)}')
                    key = generate_cache_key(prefix, func, args, kwargs, skip_args, skip_kwargs)
                    cached_value = await cache_manager.get(key, backend=backend)
                    if cached_value is not None:
                        cache_hit = True
                        logger.debug(f'Cache hit for key: {key}')
                        return cached_value
                    logger.debug(f'Cache miss for key: {key}')
                    result = await func(*args, **kwargs)
                    if result is not None:
                        await cache_manager.set(key, result, ttl, backend)
                        if tags and 'redis' in cache_manager.backends:
                            for tag in tags:
                                tag_key = f'cache:tag:{tag}'
                                redis_backend = cache_manager.backends['redis']
                                if hasattr(redis_backend, 'add_to_set'):
                                    await redis_backend.add_to_set(tag_key, key)
                    return result
                except Exception as e:
                    error = str(e)
                    logger.error(f'Error in cached decorator for {func.__name__}: {error}', exc_info=True)
                    return await func(*args, **kwargs)
                finally:
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.track_cache_operation(operation='cached_decorator', backend=backend_type, hit=cache_hit, duration=duration, component=func.__module__)
                        except Exception as metrics_err:
                            logger.warning(f'Failed to record cache metrics: {str(metrics_err)}')
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                cache_hit = False
                error = None
                backend_type = backend or 'default'
                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency('metrics_service')
                        except Exception as e:
                            logger.debug(f'Could not get metrics service: {str(e)}')
                    key = generate_cache_key(prefix, func, args, kwargs, skip_args, skip_kwargs)
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                    try:
                        cached_value = loop.run_until_complete(cache_manager.get(key, backend=backend))
                        if cached_value is not None:
                            cache_hit = True
                            logger.debug(f'Cache hit for key: {key}')
                            return cached_value
                    except Exception as cache_err:
                        logger.warning(f'Error getting from cache: {str(cache_err)}')
                    logger.debug(f'Cache miss for key: {key}')
                    result = func(*args, **kwargs)
                    if result is not None:
                        try:
                            loop.run_until_complete(cache_manager.set(key, result, ttl, backend))
                            if tags and 'redis' in cache_manager.backends:
                                redis_backend = cache_manager.backends['redis']
                                if hasattr(redis_backend, 'add_to_set'):
                                    for tag in tags:
                                        tag_key = f'cache:tag:{tag}'
                                        loop.run_until_complete(redis_backend.add_to_set(tag_key, key))
                        except Exception as cache_err:
                            logger.warning(f'Error setting cache: {str(cache_err)}')
                    return result
                except Exception as e:
                    error = str(e)
                    logger.error(f'Error in cached decorator for {func.__name__}: {error}', exc_info=True)
                    return func(*args, **kwargs)
                finally:
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.track_cache_operation(operation='cached_decorator', backend=backend_type, hit=cache_hit, duration=duration, component=func.__module__)
                        except Exception as metrics_err:
                            logger.warning(f'Failed to record cache metrics: {str(metrics_err)}')
            return cast(F, sync_wrapper)
    return decorator
def invalidate_cache(pattern: str, prefix: str='cache', backend: Optional[str]=None, tags: Optional[List[str]]=None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)
        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                result = await func(*args, **kwargs)
                try:
                    pattern_key = f'{prefix}:{pattern}'
                    count = await cache_manager.invalidate_pattern(pattern_key, backend)
                    logger.debug(f'Invalidated {count} cache entries matching pattern: {pattern_key}')
                    if tags and 'redis' in cache_manager.backends:
                        redis_backend = cache_manager.backends['redis']
                        if hasattr(redis_backend, 'get_set_members'):
                            for tag in tags:
                                try:
                                    tag_key = f'cache:tag:{tag}'
                                    keys = await redis_backend.get_set_members(tag_key)
                                    if keys:
                                        await cache_manager.delete_many(keys)
                                        await redis_backend.delete(tag_key)
                                        logger.debug(f'Invalidated tag: {tag} with {len(keys)} keys')
                                except Exception as tag_err:
                                    logger.warning(f'Error invalidating tag {tag}: {str(tag_err)}')
                except Exception as e:
                    logger.warning(f'Error invalidating cache: {str(e)}', exc_info=True)
                return result
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)
                try:
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                    pattern_key = f'{prefix}:{pattern}'
                    count = loop.run_until_complete(cache_manager.invalidate_pattern(pattern_key, backend))
                    logger.debug(f'Invalidated {count} cache entries matching pattern: {pattern_key}')
                    if tags and 'redis' in cache_manager.backends:
                        redis_backend = cache_manager.backends['redis']
                        if hasattr(redis_backend, 'get_set_members'):
                            for tag in tags:
                                try:
                                    tag_key = f'cache:tag:{tag}'
                                    keys = loop.run_until_complete(redis_backend.get_set_members(tag_key))
                                    if keys:
                                        loop.run_until_complete(cache_manager.delete_many(keys))
                                        loop.run_until_complete(redis_backend.delete(tag_key))
                                        logger.debug(f'Invalidated tag: {tag} with {len(keys)} keys')
                                except Exception as tag_err:
                                    logger.warning(f'Error invalidating tag {tag}: {str(tag_err)}')
                except Exception as e:
                    logger.warning(f'Error invalidating cache: {str(e)}', exc_info=True)
                return result
            return cast(F, sync_wrapper)
    return decorator
def cache_aside(key_func: Callable[..., str], ttl: Optional[int]=300, backend: Optional[str]=None, tags: Optional[List[str]]=None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        is_coroutine = asyncio.iscoroutinefunction(func)
        if is_coroutine:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                cache_hit = False
                error = None
                backend_type = backend or 'default'
                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency('metrics_service')
                        except Exception as e:
                            logger.debug(f'Could not get metrics service: {str(e)}')
                    key = key_func(*args, **kwargs)
                    cached_value = await cache_manager.get(key, backend=backend)
                    if cached_value is not None:
                        cache_hit = True
                        logger.debug(f'Cache hit for key: {key}')
                        return cached_value
                    logger.debug(f'Cache miss for key: {key}')
                    result = await func(*args, **kwargs)
                    if result is not None:
                        await cache_manager.set(key, result, ttl, backend)
                        if tags and 'redis' in cache_manager.backends:
                            redis_backend = cache_manager.backends['redis']
                            if hasattr(redis_backend, 'add_to_set'):
                                for tag in tags:
                                    tag_key = f'cache:tag:{tag}'
                                    await redis_backend.add_to_set(tag_key, key)
                    return result
                except Exception as e:
                    error = str(e)
                    logger.error(f'Error in cache_aside decorator for {func.__name__}: {error}', exc_info=True)
                    return await func(*args, **kwargs)
                finally:
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.track_cache_operation(operation='cache_aside_decorator', backend=backend_type, hit=cache_hit, duration=duration, component=func.__module__)
                        except Exception as metrics_err:
                            logger.warning(f'Failed to record cache metrics: {str(metrics_err)}')
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service = None
                start_time = time.monotonic()
                cache_hit = False
                error = None
                backend_type = backend or 'default'
                try:
                    if HAS_METRICS:
                        try:
                            metrics_service = get_dependency('metrics_service')
                        except Exception as e:
                            logger.debug(f'Could not get metrics service: {str(e)}')
                    key = key_func(*args, **kwargs)
                    try:
                        loop = asyncio.get_running_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                    try:
                        cached_value = loop.run_until_complete(cache_manager.get(key, backend=backend))
                        if cached_value is not None:
                            cache_hit = True
                            logger.debug(f'Cache hit for key: {key}')
                            return cached_value
                    except Exception as cache_err:
                        logger.warning(f'Error getting from cache: {str(cache_err)}')
                    logger.debug(f'Cache miss for key: {key}')
                    result = func(*args, **kwargs)
                    if result is not None:
                        try:
                            loop.run_until_complete(cache_manager.set(key, result, ttl, backend))
                            if tags and 'redis' in cache_manager.backends:
                                redis_backend = cache_manager.backends['redis']
                                if hasattr(redis_backend, 'add_to_set'):
                                    for tag in tags:
                                        tag_key = f'cache:tag:{tag}'
                                        loop.run_until_complete(redis_backend.add_to_set(tag_key, key))
                        except Exception as cache_err:
                            logger.warning(f'Error setting cache: {str(cache_err)}')
                    return result
                except Exception as e:
                    error = str(e)
                    logger.error(f'Error in cache_aside decorator for {func.__name__}: {error}', exc_info=True)
                    return func(*args, **kwargs)
                finally:
                    if metrics_service and HAS_METRICS:
                        try:
                            duration = time.monotonic() - start_time
                            metrics_service.track_cache_operation(operation='cache_aside_decorator', backend=backend_type, hit=cache_hit, duration=duration, component=func.__module__)
                        except Exception as metrics_err:
                            logger.warning(f'Failed to record cache metrics: {str(metrics_err)}')
            return cast(F, sync_wrapper)
    return decorator
def memoize(ttl: Optional[int]=None, max_size: int=128) -> Callable[[F], F]:
    return cached(ttl=ttl, prefix='memoize', backend='memory')