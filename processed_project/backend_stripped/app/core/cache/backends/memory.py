from __future__ import annotations
import fnmatch
import time
from collections import OrderedDict
from threading import RLock
from typing import Any, Dict, List, Optional, TypeVar
from app.core.cache.base import CacheBackend
from app.logging import get_logger
T = TypeVar('T')
logger = get_logger('app.core.cache.memory')
class MemoryCacheBackend(CacheBackend[T]):
    def __init__(self, max_size: int=1000, clean_interval: int=60) -> None:
        self.cache: Dict[str, Any] = OrderedDict()
        self.expiry: Dict[str, float] = {}
        self.max_size = max_size
        self.clean_interval = clean_interval
        self.lock = RLock()
        self.last_cleanup = time.time()
    async def initialize(self) -> None:
        logger.info('Memory cache backend initialized')
        return None
    async def shutdown(self) -> None:
        with self.lock:
            self.cache.clear()
            self.expiry.clear()
        logger.info('Memory cache backend shut down')
        return None
    async def get(self, key: str) -> Optional[T]:
        with self.lock:
            if key not in self.cache:
                return None
            if key in self.expiry and self.expiry[key] < time.time():
                del self.cache[key]
                del self.expiry[key]
                return None
            value = self.cache.pop(key)
            self.cache[key] = value
            await self._clean_if_needed()
            return value
    async def set(self, key: str, value: T, ttl: Optional[int]=None) -> bool:
        with self.lock:
            if len(self.cache) >= self.max_size and key not in self.cache:
                oldest_key, _ = next(iter(self.cache.items()))
                del self.cache[oldest_key]
                if oldest_key in self.expiry:
                    del self.expiry[oldest_key]
            self.cache[key] = value
            if ttl is not None:
                self.expiry[key] = time.time() + ttl
            elif key in self.expiry:
                del self.expiry[key]
            await self._clean_if_needed()
            return True
    async def delete(self, key: str) -> bool:
        with self.lock:
            if key not in self.cache:
                return False
            del self.cache[key]
            if key in self.expiry:
                del self.expiry[key]
            return True
    async def exists(self, key: str) -> bool:
        with self.lock:
            if key not in self.cache:
                return False
            if key in self.expiry and self.expiry[key] < time.time():
                del self.cache[key]
                del self.expiry[key]
                return False
            return True
    async def invalidate_pattern(self, pattern: str) -> int:
        count = 0
        with self.lock:
            keys_to_delete = [key for key in self.cache.keys() if fnmatch.fnmatch(key, pattern)]
            for key in keys_to_delete:
                del self.cache[key]
                if key in self.expiry:
                    del self.expiry[key]
                count += 1
        return count
    async def clear(self) -> bool:
        with self.lock:
            self.cache.clear()
            self.expiry.clear()
            return True
    async def get_many(self, keys: List[str]) -> Dict[str, Optional[T]]:
        result = {}
        with self.lock:
            for key in keys:
                result[key] = await self.get(key)
        return result
    async def set_many(self, mapping: Dict[str, T], ttl: Optional[int]=None) -> bool:
        with self.lock:
            for key, value in mapping.items():
                await self.set(key, value, ttl)
        return True
    async def delete_many(self, keys: List[str]) -> int:
        count = 0
        with self.lock:
            for key in keys:
                if await self.delete(key):
                    count += 1
        return count
    async def incr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None) -> int:
        with self.lock:
            value = await self.get(key)
            if value is None:
                value = default
            elif not isinstance(value, int):
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    value = default
            value += amount
            await self.set(key, value, ttl)
            return value
    async def decr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None) -> int:
        return await self.incr(key, -amount, default, ttl)
    async def _clean_if_needed(self) -> None:
        current_time = time.time()
        if current_time - self.last_cleanup < self.clean_interval:
            return
        self.last_cleanup = current_time
        expired_keys = [key for key, expiry in self.expiry.items() if expiry < current_time]
        for key in expired_keys:
            if key in self.cache:
                del self.cache[key]
            del self.expiry[key]
        logger.debug(f'Cleaned {len(expired_keys)} expired keys from memory cache')