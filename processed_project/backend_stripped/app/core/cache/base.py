from __future__ import annotations
import abc
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Pattern, Set, TypeVar, Union
T = TypeVar('T')
class CacheBackend(ABC, Generic[T]):
    @abstractmethod
    async def get(self, key: str) -> Optional[T]:
        pass
    @abstractmethod
    async def set(self, key: str, value: T, ttl: Optional[int]=None) -> bool:
        pass
    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass
    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass
    @abstractmethod
    async def invalidate_pattern(self, pattern: str) -> int:
        pass
    @abstractmethod
    async def clear(self) -> bool:
        pass
    @abstractmethod
    async def get_many(self, keys: List[str]) -> Dict[str, Optional[T]]:
        pass
    @abstractmethod
    async def set_many(self, mapping: Dict[str, T], ttl: Optional[int]=None) -> bool:
        pass
    @abstractmethod
    async def delete_many(self, keys: List[str]) -> int:
        pass
    @abstractmethod
    async def incr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None) -> int:
        pass
    @abstractmethod
    async def decr(self, key: str, amount: int=1, default: int=0, ttl: Optional[int]=None) -> int:
        pass