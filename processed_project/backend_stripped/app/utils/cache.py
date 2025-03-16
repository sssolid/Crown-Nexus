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
F = TypeVar('F', bound=Callable[..., Any])
RT = TypeVar('RT')
redis_client: Optional[redis.Redis] = None
async def get_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=False)
    return redis_client
def generate_cache_key(prefix: str, func: Callable[..., Any], args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> str:
    func_name = f'{func.__module__}.{func.__qualname__}'
    arg_str = str(args) + str(sorted(kwargs.items()))
    arg_hash = hashlib.md5(arg_str.encode()).hexdigest()
    return f'{prefix}:{func_name}:{arg_hash}'
def redis_cache(prefix: str='cache', ttl: int=300, skip_args: List[str]=None) -> Callable[[F], F]:
    skip_args = skip_args or ['self', 'cls', 'db', 'request']
    def decorator(func: F) -> F:
        signature = inspect.signature(func)
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_kwargs = {k: v for k, v in kwargs.items() if k not in skip_args}
            bound_args = signature.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()
            arg_dict = bound_args.arguments
            filtered_args = {k: v for k, v in arg_dict.items() if k not in skip_args}
            key = generate_cache_key(prefix, func, (), filtered_args)
            redis_conn = await get_redis()
            cached_data = await redis_conn.get(key)
            if cached_data:
                return pickle.loads(cached_data)
            result = await func(*args, **kwargs)
            await redis_conn.set(key, pickle.dumps(result), ex=ttl)
            return result
        return cast(F, wrapper)
    return decorator
def memory_cache(maxsize: int=128, ttl: int=300) -> Callable[[F], F]:
    cache: Dict[str, Tuple[float, Any]] = {}
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = generate_cache_key('memory', func, args, kwargs)
            import time
            current_time = time.time()
            if key in cache:
                timestamp, value = cache[key]
                if current_time - timestamp < ttl:
                    return value
            result = await func(*args, **kwargs)
            cache[key] = (current_time, result)
            if len(cache) > maxsize:
                items = sorted(cache.items(), key=lambda x: x[1][0])
                for old_key, _ in items[:len(cache) - maxsize]:
                    del cache[old_key]
            return result
        return cast(F, wrapper)
    return decorator
async def invalidate_cache(prefix: str, pattern: str='*', redis_conn: Optional[redis.Redis]=None) -> int:
    if redis_conn is None:
        redis_conn = await get_redis()
    keys = await redis_conn.keys(f'{prefix}:{pattern}')
    if keys:
        return await redis_conn.delete(*keys)
    return 0
class RequestCache:
    def __init__(self) -> None:
        self.cache: Dict[str, Any] = {}
    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key)
    def set(self, key: str, value: Any) -> None:
        self.cache[key] = value
    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]
    def clear(self) -> None:
        self.cache.clear()
def get_request_cache(request: Request) -> RequestCache:
    if not hasattr(request.state, 'cache'):
        request.state.cache = RequestCache()
    return request.state.cache