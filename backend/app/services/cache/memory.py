# backend/app/services/cache/memory.py
"""In-memory cache backend implementation.

This module provides an in-memory implementation of the CacheBackend protocol,
suitable for development and testing environments.
"""
from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List, Optional

from app.core.logging import get_logger

logger = get_logger(__name__)


class MemoryCacheBackend:
    """In-memory cache backend implementation."""

    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        """
        Initialize the memory cache backend.

        Args:
            max_size: Maximum number of items in the cache
            default_ttl: Default time-to-live in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, tuple[Any, float]] = {}  # (value, expiry)
        self.cleanup_task: Optional[asyncio.Task] = None
        logger.debug("MemoryCacheBackend initialized")

    async def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the cache.

        Args:
            key: Cache key
            default: Default value if key doesn't exist

        Returns:
            Cached value or default
        """
        if key not in self.cache:
            return default

        value, expiry = self.cache[key]

        # Check if expired
        if expiry < time.time():
            await self.delete(key)
            return default

        logger.debug(f"Cache hit: {key}")
        return value

    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """
        Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds

        Returns:
            True if successful, False otherwise
        """
        # Check if we need to evict entries due to max_size
        if len(self.cache) >= self.max_size and key not in self.cache:
            # Simple LRU: remove oldest item (not ideal but simple)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            logger.debug(f"Cache eviction (max size): {oldest_key}")

        # Calculate expiry time
        expiry = time.time() + (ttl or self.default_ttl)

        # Store value with expiry
        self.cache[key] = (value, expiry)
        logger.debug(f"Cache set: {key} (TTL: {ttl}s)")

        # Ensure cleanup task is running
        if self.cleanup_task is None or self.cleanup_task.done():
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())

        return True

    async def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.

        Args:
            key: Cache key

        Returns:
            True if key was deleted, False otherwise
        """
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache delete: {key}")
            return True
        return False

    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in the cache.

        Args:
            key: Cache key

        Returns:
            True if key exists and is not expired, False otherwise
        """
        if key not in self.cache:
            return False

        _, expiry = self.cache[key]

        # Check if expired
        if expiry < time.time():
            await self.delete(key)
            return False

        return True

    async def clear(self) -> bool:
        """
        Clear all cached values.

        Returns:
            True if successful, False otherwise
        """
        self.cache.clear()
        logger.debug("Cache cleared")
        return True

    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """
        Get multiple values from the cache.

        Args:
            keys: List of cache keys

        Returns:
            Dictionary of key-value pairs for found keys
        """
        result = {}
        for key in keys:
            value = await self.get(key)
            if value is not None:
                result[key] = value
        return result

    async def set_many(self, mapping: Dict[str, Any], ttl: int = 300) -> bool:
        """
        Set multiple values in the cache.

        Args:
            mapping: Dictionary of key-value pairs
            ttl: Time-to-live in seconds

        Returns:
            True if successful, False otherwise
        """
        for key, value in mapping.items():
            await self.set(key, value, ttl)
        return True

    async def delete_many(self, keys: List[str]) -> int:
        """
        Delete multiple values from the cache.

        Args:
            keys: List of cache keys

        Returns:
            Number of keys deleted
        """
        count = 0
        for key in keys:
            if await self.delete(key):
                count += 1
        return count

    async def incr(self, key: str, amount: int = 1) -> int:
        """
        Increment a value in the cache.

        Args:
            key: Cache key
            amount: Amount to increment by

        Returns:
            New value
        """
        value = await self.get(key, 0)
        if not isinstance(value, (int, float)):
            value = 0

        new_value = value + amount
        await self.set(key, new_value)
        return new_value

    async def decr(self, key: str, amount: int = 1) -> int:
        """
        Decrement a value in the cache.

        Args:
            key: Cache key
            amount: Amount to decrement by

        Returns:
            New value
        """
        return await self.incr(key, -amount)

    async def ttl(self, key: str) -> Optional[int]:
        """
        Get the remaining time-to-live for a key.

        Args:
            key: Cache key

        Returns:
            Remaining TTL in seconds, or None if key doesn't exist
        """
        if key not in self.cache:
            return None

        _, expiry = self.cache[key]
        remaining = int(expiry - time.time())

        if remaining <= 0:
            await self.delete(key)
            return None

        return remaining

    async def expire(self, key: str, ttl: int) -> bool:
        """
        Set a new expiration time for a key.

        Args:
            key: Cache key
            ttl: New time-to-live in seconds

        Returns:
            True if successful, False otherwise
        """
        if key not in self.cache:
            return False

        value, _ = self.cache[key]
        expiry = time.time() + ttl
        self.cache[key] = (value, expiry)
        return True

    async def ping(self) -> bool:
        """
        Check if the cache backend is available.

        Returns:
            Always True for memory cache
        """
        return True

    async def close(self) -> None:
        """Close the cache backend and release resources."""
        # Cancel cleanup task if running
        if self.cleanup_task and not self.cleanup_task.done():
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
        logger.debug("MemoryCacheBackend closed")

    async def _cleanup_loop(self) -> None:
        """Background task to clean up expired entries."""
        try:
            while True:
                await self._cleanup_expired()
                await asyncio.sleep(60)  # Run cleanup every minute
        except asyncio.CancelledError:
            # Final cleanup when task is cancelled
            await self._cleanup_expired()
            raise

    async def _cleanup_expired(self) -> None:
        """Remove expired entries from the cache."""
        now = time.time()
        expired_keys = [k for k, (_, exp) in self.cache.items() if exp <= now]

        if expired_keys:
            for key in expired_keys:
                del self.cache[key]
            logger.debug(f"Expired {len(expired_keys)} cache entries")
