# backend/app/core/cache/base.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol, TypeVar, Generic

T = TypeVar("T")


class CacheBackend(Protocol, Generic[T]):
    """Protocol defining cache backend interface."""

    async def initialize(self) -> None:
        """Initialize the cache backend."""
        ...

    async def shutdown(self) -> None:
        """Shut down the cache backend."""
        ...

    async def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        """Get value from cache by key."""
        ...

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        ...

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        ...

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        ...

    async def clear(self) -> bool:
        """Clear all cache entries."""
        ...

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching a pattern."""
        ...

    async def get_many(self, keys: List[str]) -> Dict[str, Optional[T]]:
        """Get multiple values from the cache."""
        ...

    async def set_many(self, mapping: Dict[str, T], ttl: Optional[int] = None) -> bool:
        """Set multiple values in the cache."""
        ...

    async def delete_many(self, keys: List[str]) -> int:
        """Delete multiple values from the cache."""
        ...

    async def incr(
        self, key: str, amount: int = 1, default: int = 0, ttl: Optional[int] = None
    ) -> int:
        """Increment a counter in the cache."""
        ...

    async def decr(
        self, key: str, amount: int = 1, default: int = 0, ttl: Optional[int] = None
    ) -> int:
        """Decrement a counter in the cache."""
        ...
