from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, Type
from app.core.cache.base import CacheBackend
from app.core.cache.memory import MemoryCacheBackend
from app.core.cache.redis import RedisCacheBackend
from app.core.config import settings
from app.core.logging import get_logger
logger = get_logger('app.core.cache.manager')
class CacheManager:
    def __init__(self) -> None:
        self.backends: Dict[str, CacheBackend] = {}
        self.default_backend: Optional[str] = None
    def register_backend(self, name: str, backend: CacheBackend, set_as_default: bool=False) -> None:
        self.backends[name] = backend
        if set_as_default or self.default_backend is None:
            self.default_backend = name
        logger.debug(f'Registered cache backend: {name}')
    def _get_backend(self, backend_name: Optional[str]=None) -> CacheBackend:
        name = backend_name or self.default_backend
        if name is None:
            raise ValueError('No default cache backend registered')
        if name not in self.backends:
            raise ValueError(f'Cache backend not found: {name}')
        return self.backends[name]
    async def get(self, key: str, backend_name: Optional[str]=None) -> Optional[Any]:
        backend = self._get_backend(backend_name)
        return await backend.get(key)
    async def set(self, key: str, value: Any, ttl: Optional[int]=None, backend_name: Optional[str]=None) -> bool:
        backend = self._get_backend(backend_name)
        return await backend.set(key, value, ttl)
    async def delete(self, key: str, backend_name: Optional[str]=None) -> bool:
        backend = self._get_backend(backend_name)
        return await backend.delete(key)
    async def exists(self, key: str, backend_name: Optional[str]=None) -> bool:
        backend = self._get_backend(backend_name)
        return await backend.exists(key)
    async def invalidate_pattern(self, pattern: str, backend_name: Optional[str]=None) -> int:
        backend = self._get_backend(backend_name)
        return await backend.invalidate_pattern(pattern)
    async def clear(self, backend_name: Optional[str]=None) -> bool:
        if backend_name is not None:
            backend = self._get_backend(backend_name)
            return await backend.clear()
        else:
            results = []
            for name, backend in self.backends.items():
                results.append(await backend.clear())
            return all(results)
    async def get_many(self, keys: List[str], backend_name: Optional[str]=None) -> Dict[str, Optional[Any]]:
        backend = self._get_backend(backend_name)
        return await backend.get_many(keys)
    async def set_many(self, mapping: Dict[str, Any], ttl: Optional[int]=None, backend_name: Optional[str]=None) -> bool:
        backend = self._get_backend(backend_name)
        return await backend.set_many(mapping, ttl)
    async def delete_many(self, keys: List[str], backend_name: Optional[str]=None) -> int:
        backend = self._get_backend(backend_name)
        return await backend.delete_many(keys)
    async def incr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None, backend_name: Optional[str]=None) -> int:
        backend = self._get_backend(backend_name)
        return await backend.incr(key, amount, default, ttl)
    async def decr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None, backend_name: Optional[str]=None) -> int:
        backend = self._get_backend(backend_name)
        return await backend.decr(key, amount, default, ttl)
    async def get_or_set(self, key: str, default_factory: callable, ttl: Optional[int]=None, backend_name: Optional[str]=None) -> Any:
        value = await self.get(key, backend_name)
        if value is not None:
            return value
        value = default_factory()
        await self.set(key, value, ttl, backend_name)
        return value
    async def get_or_set_async(self, key: str, default_factory: callable, ttl: Optional[int]=None, backend_name: Optional[str]=None) -> Any:
        value = await self.get(key, backend_name)
        if value is not None:
            return value
        value = await default_factory()
        await self.set(key, value, ttl, backend_name)
        return value
cache_manager = CacheManager()
def initialize_cache() -> None:
    memory_cache = MemoryCacheBackend(max_size=1000, clean_interval=60)
    cache_manager.register_backend('memory', memory_cache, True)
    if hasattr(settings, 'redis') and hasattr(settings.redis, 'uri'):
        redis_cache = RedisCacheBackend(redis_url=settings.redis.uri, serializer='pickle', prefix='crown_nexus:')
        cache_manager.register_backend('redis', redis_cache)
    logger.info('Cache backends initialized')