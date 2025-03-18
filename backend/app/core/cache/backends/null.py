from __future__ import annotations
from typing import Any, Dict, Optional, Protocol, TypeVar, Union

from app.core.cache.base import CacheBackend

T = TypeVar("T")

class NullCacheBackend(CacheBackend):
    """No-op cache backend for testing or disabling cache."""

    async def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        """Always return default value."""
        return default

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """No-op, always return success."""
        return True

    async def delete(self, key: str) -> bool:
        """No-op, always return success."""
        return True

    async def exists(self, key: str) -> bool:
        """Always return False."""
        return False

    async def clear(self) -> bool:
        """No-op, always return success."""
        return True
