from __future__ import annotations
from typing import Any, Dict, Optional, Protocol, TypeVar, Union

T = TypeVar("T")

class CacheBackend(Protocol):
    """Protocol defining cache backend interface."""

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
