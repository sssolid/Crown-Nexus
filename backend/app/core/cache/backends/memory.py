# /backend/app/core/cache/backends/memory.py
from __future__ import annotations

import fnmatch
import time
from collections import OrderedDict
from threading import RLock
from typing import Any, Dict, List, Optional, TypeVar

from app.core.cache.base import CacheBackend
from app.logging import get_logger

T = TypeVar("T")

logger = get_logger("app.core.cache.memory")


class MemoryCacheBackend(CacheBackend[T]):
    """In-memory cache backend implementation.

    This backend stores cached values in memory, with optional TTL expiration.
    It's suitable for development and testing environments, or for small-scale
    production use where persistence is not required.
    """

    def __init__(self, max_size: int = 1000, clean_interval: int = 60) -> None:
        """Initialize the memory cache backend.

        Args:
            max_size: Maximum number of items to store in the cache
            clean_interval: Interval between cleanup runs in seconds
        """
        self.cache: Dict[str, Any] = OrderedDict()
        self.expiry: Dict[str, float] = {}
        self.max_size = max_size
        self.clean_interval = clean_interval
        self.lock = RLock()
        self.last_cleanup = time.time()

    async def initialize(self) -> None:
        """Initialize the memory cache backend.

        This is a no-op for the memory backend since it doesn't require
        external connections, but implemented for interface consistency.
        """
        logger.info("Memory cache backend initialized")
        return None

    async def shutdown(self) -> None:
        """Shut down the memory cache backend.

        Clears all cached data and performs cleanup.
        """
        with self.lock:
            self.cache.clear()
            self.expiry.clear()
        logger.info("Memory cache backend shut down")
        return None

    async def get(self, key: str) -> Optional[T]:
        """Get a value from the cache.

        Args:
            key: Cache key

        Returns:
            Optional[T]: Cached value or None if not found or expired
        """
        with self.lock:
            # Check if key exists
            if key not in self.cache:
                return None

            # Check if key has expired
            if key in self.expiry and self.expiry[key] < time.time():
                # Remove expired key
                del self.cache[key]
                del self.expiry[key]
                return None

            # Move key to end of OrderedDict to mark as recently used
            value = self.cache.pop(key)
            self.cache[key] = value

            # Clean cache if needed
            await self._clean_if_needed()

            return value

    async def set(self, key: str, value: T, ttl: Optional[int] = None) -> bool:
        """Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds

        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            # Check cache size and evict oldest item if necessary
            if len(self.cache) >= self.max_size and key not in self.cache:
                # Remove oldest item (first item in OrderedDict)
                oldest_key, _ = next(iter(self.cache.items()))
                del self.cache[oldest_key]
                if oldest_key in self.expiry:
                    del self.expiry[oldest_key]

            # Store value
            self.cache[key] = value

            # Set expiry if TTL provided
            if ttl is not None:
                self.expiry[key] = time.time() + ttl
            elif key in self.expiry:
                # Remove expiry if TTL is None but key previously had expiry
                del self.expiry[key]

            # Clean cache if needed
            await self._clean_if_needed()

            return True

    async def delete(self, key: str) -> bool:
        """Delete a value from the cache.

        Args:
            key: Cache key

        Returns:
            bool: True if key was deleted, False if key wasn't found
        """
        with self.lock:
            if key not in self.cache:
                return False

            # Remove key
            del self.cache[key]
            if key in self.expiry:
                del self.expiry[key]

            return True

    async def exists(self, key: str) -> bool:
        """Check if a key exists in the cache.

        Args:
            key: Cache key

        Returns:
            bool: True if key exists and hasn't expired, False otherwise
        """
        with self.lock:
            # Check if key exists
            if key not in self.cache:
                return False

            # Check if key has expired
            if key in self.expiry and self.expiry[key] < time.time():
                # Remove expired key
                del self.cache[key]
                del self.expiry[key]
                return False

            return True

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching a pattern.

        Args:
            pattern: Key pattern to match (glob pattern)

        Returns:
            int: Number of keys invalidated
        """
        count = 0
        with self.lock:
            # Find keys matching pattern
            keys_to_delete = [
                key for key in self.cache.keys() if fnmatch.fnmatch(key, pattern)
            ]

            # Delete matching keys
            for key in keys_to_delete:
                del self.cache[key]
                if key in self.expiry:
                    del self.expiry[key]
                count += 1

        return count

    async def clear(self) -> bool:
        """Clear all cached values.

        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            self.cache.clear()
            self.expiry.clear()
            return True

    async def get_many(self, keys: List[str]) -> Dict[str, Optional[T]]:
        """Get multiple values from the cache.

        Args:
            keys: List of cache keys

        Returns:
            Dict[str, Optional[T]]: Dictionary of key-value pairs
        """
        result = {}
        with self.lock:
            for key in keys:
                result[key] = await self.get(key)

        return result

    async def set_many(self, mapping: Dict[str, T], ttl: Optional[int] = None) -> bool:
        """Set multiple values in the cache.

        Args:
            mapping: Dictionary of key-value pairs to cache
            ttl: Time-to-live in seconds

        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            for key, value in mapping.items():
                await self.set(key, value, ttl)

        return True

    async def delete_many(self, keys: List[str]) -> int:
        """Delete multiple values from the cache.

        Args:
            keys: List of cache keys

        Returns:
            int: Number of keys deleted
        """
        count = 0
        with self.lock:
            for key in keys:
                if await self.delete(key):
                    count += 1

        return count

    async def incr(
        self, key: str, amount: int = 1, default: int = 0, ttl: Optional[int] = None
    ) -> int:
        """Increment a counter in the cache.

        Args:
            key: Cache key
            amount: Amount to increment by
            default: Default value if key doesn't exist
            ttl: Time-to-live in seconds

        Returns:
            int: New counter value
        """
        with self.lock:
            # Get current value
            value = await self.get(key)

            # Initialize with default if not found
            if value is None:
                value = default
            elif not isinstance(value, int):
                # If value is not an integer, convert it
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    # If conversion fails, use default
                    value = default

            # Increment value
            value += amount

            # Store updated value
            await self.set(key, value, ttl)

            return value

    async def decr(
        self, key: str, amount: int = 1, default: int = 0, ttl: Optional[int] = None
    ) -> int:
        """Decrement a counter in the cache.

        Args:
            key: Cache key
            amount: Amount to decrement by
            default: Default value if key doesn't exist
            ttl: Time-to-live in seconds

        Returns:
            int: New counter value
        """
        return await self.incr(key, -amount, default, ttl)

    async def _clean_if_needed(self) -> None:
        """Clean expired keys if cleanup interval has passed."""
        current_time = time.time()
        if current_time - self.last_cleanup < self.clean_interval:
            return

        # Set last cleanup time
        self.last_cleanup = current_time

        # Find expired keys
        expired_keys = [
            key for key, expiry in self.expiry.items() if expiry < current_time
        ]

        # Remove expired keys
        for key in expired_keys:
            if key in self.cache:
                del self.cache[key]
            del self.expiry[key]

        logger.debug(f"Cleaned {len(expired_keys)} expired keys from memory cache")
