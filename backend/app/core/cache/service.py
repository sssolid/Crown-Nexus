from __future__ import annotations

"""
Cache service implementation.

This module provides a service wrapper around the cache system,
making it available through the dependency manager.
"""

from typing import Any, Dict, List, Optional, TypeVar

from app.core.cache.manager import cache_manager
from app.logging import get_logger

logger = get_logger("app.core.cache.service")

T = TypeVar("T")


class CacheService:
    def __init__(self) -> None:
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the cache service."""
        if self._initialized:
            logger.debug("Cache service already initialized, skipping")
            return
        logger.info("Initializing cache service")
        await cache_manager.initialize()
        self._initialized = True
        logger.info("Cache service initialized")

    async def shutdown(self) -> None:
        """Shutdown the cache service."""
        if not self._initialized:
            return
        logger.info("Shutting down cache service")
        await cache_manager.shutdown()
        self._initialized = False
        logger.info("Cache service shut down")

    async def get(
        self, key: str, default: Optional[T] = None, backend: Optional[str] = None
    ) -> Optional[T]:
        """Get a value from the cache.

        Args:
            key: The cache key.
            default: Default value if key doesn't exist.
            backend: Optional backend name.

        Returns:
            The cached value or default.
        """
        return await cache_manager.get(key, default, backend)

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        backend: Optional[str] = None,
    ) -> bool:
        """Set a value in the cache.

        Args:
            key: The cache key.
            value: The value to cache.
            ttl: Optional time-to-live in seconds.
            backend: Optional backend name.

        Returns:
            True if successful, False otherwise.
        """
        return await cache_manager.set(key, value, ttl, backend)

    async def delete(self, key: str, backend: Optional[str] = None) -> bool:
        """Delete a value from the cache.

        Args:
            key: The cache key.
            backend: Optional backend name.

        Returns:
            True if successful, False otherwise.
        """
        return await cache_manager.delete(key, backend)

    async def exists(self, key: str, backend: Optional[str] = None) -> bool:
        """Check if a key exists in the cache.

        Args:
            key: The cache key.
            backend: Optional backend name.

        Returns:
            True if key exists, False otherwise.
        """
        return await cache_manager.exists(key, backend)

    async def clear(self, backend: Optional[str] = None) -> bool:
        """Clear the cache.

        Args:
            backend: Optional backend name.

        Returns:
            True if successful, False otherwise.
        """
        return await cache_manager.clear(backend)

    async def invalidate_pattern(
        self, pattern: str, backend: Optional[str] = None
    ) -> int:
        """Invalidate cache keys matching a pattern.

        Args:
            pattern: The pattern to match.
            backend: Optional backend name.

        Returns:
            Number of invalidated keys.
        """
        return await cache_manager.invalidate_pattern(pattern, backend)

    async def get_many(
        self, keys: List[str], backend: Optional[str] = None
    ) -> Dict[str, Optional[T]]:
        """Get multiple values from the cache.

        Args:
            keys: List of cache keys.
            backend: Optional backend name.

        Returns:
            Dictionary of key-value pairs.
        """
        return await cache_manager.get_many(keys, backend)

    async def set_many(
        self,
        mapping: Dict[str, T],
        ttl: Optional[int] = None,
        backend: Optional[str] = None,
    ) -> bool:
        """Set multiple values in the cache.

        Args:
            mapping: Dictionary of key-value pairs.
            ttl: Optional time-to-live in seconds.
            backend: Optional backend name.

        Returns:
            True if successful, False otherwise.
        """
        return await cache_manager.set_many(mapping, ttl, backend)

    async def delete_many(self, keys: List[str], backend: Optional[str] = None) -> int:
        """Delete multiple values from the cache.

        Args:
            keys: List of cache keys.
            backend: Optional backend name.

        Returns:
            Number of deleted keys.
        """
        return await cache_manager.delete_many(keys, backend)

    async def incr(
        self,
        key: str,
        amount: int = 1,
        default: int = 0,
        ttl: Optional[int] = None,
        backend: Optional[str] = None,
    ) -> int:
        """Increment a counter.

        Args:
            key: The cache key.
            amount: Amount to increment by.
            default: Default value if key doesn't exist.
            ttl: Optional time-to-live in seconds.
            backend: Optional backend name.

        Returns:
            New counter value.
        """
        return await cache_manager.incr(key, amount, default, ttl, backend)

    async def decr(
        self,
        key: str,
        amount: int = 1,
        default: int = 0,
        ttl: Optional[int] = None,
        backend: Optional[str] = None,
    ) -> int:
        """Decrement a counter.

        Args:
            key: The cache key.
            amount: Amount to decrement by.
            default: Default value if key doesn't exist.
            ttl: Optional time-to-live in seconds.
            backend: Optional backend name.

        Returns:
            New counter value.
        """
        return await cache_manager.decr(key, amount, default, ttl, backend)


_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """Get the cache service singleton instance.

    Returns:
        The cache service instance.
    """
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
