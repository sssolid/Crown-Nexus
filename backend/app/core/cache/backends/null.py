# backend/app/core/cache/backends/null.py
from __future__ import annotations
from typing import Any, Dict, List, Optional, TypeVar, Union

from app.core.cache.base import CacheBackend
from app.core.logging import get_logger

T = TypeVar("T")
logger = get_logger("app.core.cache.null")


class NullCacheBackend(CacheBackend[T]):
    """No-op cache backend for testing or disabling cache.

    This backend doesn't actually store or retrieve any data. It simply provides
    the interface required by the CacheBackend protocol but performs no operations.
    Useful for testing or when caching needs to be disabled.
    """

    async def initialize(self) -> None:
        """Initialize the null cache backend.

        This is a no-op method that exists for interface consistency.
        """
        logger.info("Null cache backend initialized")
        return None

    async def shutdown(self) -> None:
        """Shut down the null cache backend.

        This is a no-op method that exists for interface consistency.
        """
        logger.info("Null cache backend shut down")
        return None

    async def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        """Always return default value.

        Args:
            key: Cache key
            default: Default value to return

        Returns:
            Default value (always)
        """
        return default

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """No-op, always return success.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds

        Returns:
            bool: Always True
        """
        return True

    async def delete(self, key: str) -> bool:
        """No-op, always return success.

        Args:
            key: Cache key

        Returns:
            bool: Always True
        """
        return True

    async def exists(self, key: str) -> bool:
        """Always return False.

        Args:
            key: Cache key

        Returns:
            bool: Always False
        """
        return False

    async def clear(self) -> bool:
        """No-op, always return success.

        Returns:
            bool: Always True
        """
        return True

    async def invalidate_pattern(self, pattern: str) -> int:
        """No-op invalidate method.

        Args:
            pattern: Pattern to match

        Returns:
            int: Always 0
        """
        return 0

    async def get_many(self, keys: List[str]) -> Dict[str, Optional[T]]:
        """No-op get many method.

        Args:
            keys: List of cache keys

        Returns:
            Dict[str, Optional[T]]: Dictionary with None values for all keys
        """
        return {key: None for key in keys}

    async def set_many(self, mapping: Dict[str, T], ttl: Optional[int] = None) -> bool:
        """No-op set many method.

        Args:
            mapping: Dictionary of key-value pairs
            ttl: Time-to-live in seconds

        Returns:
            bool: Always True
        """
        return True

    async def delete_many(self, keys: List[str]) -> int:
        """No-op delete many method.

        Args:
            keys: List of cache keys

        Returns:
            int: Always 0
        """
        return 0

    async def incr(
        self, key: str, amount: int = 1, default: int = 0, ttl: Optional[int] = None
    ) -> int:
        """No-op increment method.

        Args:
            key: Cache key
            amount: Amount to increment by
            default: Default value if key doesn't exist
            ttl: Time-to-live in seconds

        Returns:
            int: Always the default value
        """
        return default

    async def decr(
        self, key: str, amount: int = 1, default: int = 0, ttl: Optional[int] = None
    ) -> int:
        """No-op decrement method.

        Args:
            key: Cache key
            amount: Amount to decrement by
            default: Default value if key doesn't exist
            ttl: Time-to-live in seconds

        Returns:
            int: Always the default value
        """
        return default
