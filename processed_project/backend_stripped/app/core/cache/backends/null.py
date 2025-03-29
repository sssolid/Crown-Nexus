from __future__ import annotations
from typing import Any, Dict, List, Optional, TypeVar
from app.core.cache.base import CacheBackend
from app.logging import get_logger
T = TypeVar('T')
logger = get_logger('app.core.cache.null')
class NullCacheBackend(CacheBackend[T]):
    async def initialize(self) -> None:
        logger.info('Null cache backend initialized')
        return None
    async def shutdown(self) -> None:
        logger.info('Null cache backend shut down')
        return None
    async def get(self, key: str, default: Optional[T]=None) -> Optional[T]:
        return default
    async def set(self, key: str, value: Any, ttl: Optional[int]=None) -> bool:
        return True
    async def delete(self, key: str) -> bool:
        return True
    async def exists(self, key: str) -> bool:
        return False
    async def clear(self) -> bool:
        return True
    async def invalidate_pattern(self, pattern: str) -> int:
        return 0
    async def get_many(self, keys: List[str]) -> Dict[str, Optional[T]]:
        return {key: None for key in keys}
    async def set_many(self, mapping: Dict[str, T], ttl: Optional[int]=None) -> bool:
        return True
    async def delete_many(self, keys: List[str]) -> int:
        return 0
    async def incr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None) -> int:
        return default
    async def decr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None) -> int:
        return default