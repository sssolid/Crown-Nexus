# backend/app/services/cache/base.py
"""Base interfaces and types for the caching system.

This module defines common types, protocols, and interfaces
used throughout the cache service components.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar

# Type variables
F = TypeVar("F", bound=Callable[..., Any])
RT = TypeVar("RT")  # Return type


class CacheBackend(Protocol):
    """Protocol defining the interface for cache backends."""

    async def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the cache.

        Args:
            key: Cache key
            default: Default value if key doesn't exist

        Returns:
            Cached value or default
        """
        ...

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
        ...

    async def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.

        Args:
            key: Cache key

        Returns:
            True if key was deleted, False otherwise
        """
        ...

    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in the cache.

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        ...

    async def clear(self) -> bool:
        """
        Clear all cached values.

        Returns:
            True if successful, False otherwise
        """
        ...

    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """
        Get multiple values from the cache.

        Args:
            keys: List of cache keys

        Returns:
            Dictionary of key-value pairs for found keys
        """
        ...

    async def set_many(self, mapping: Dict[str, Any], ttl: int = 300) -> bool:
        """
        Set multiple values in the cache.

        Args:
            mapping: Dictionary of key-value pairs
            ttl: Time-to-live in seconds

        Returns:
            True if successful, False otherwise
        """
        ...

    async def delete_many(self, keys: List[str]) -> int:
        """
        Delete multiple values from the cache.

        Args:
            keys: List of cache keys

        Returns:
            Number of keys deleted
        """
        ...

    async def incr(self, key: str, amount: int = 1) -> int:
        """
        Increment a value in the cache.

        Args:
            key: Cache key
            amount: Amount to increment by

        Returns:
            New value
        """
        ...

    async def decr(self, key: str, amount: int = 1) -> int:
        """
        Decrement a value in the cache.

        Args:
            key: Cache key
            amount: Amount to decrement by

        Returns:
            New value
        """
        ...

    async def ttl(self, key: str) -> Optional[int]:
        """
        Get the remaining time-to-live for a key.

        Args:
            key: Cache key

        Returns:
            Remaining TTL in seconds, or None if key doesn't exist
        """
        ...

    async def expire(self, key: str, ttl: int) -> bool:
        """
        Set a new expiration time for a key.

        Args:
            key: Cache key
            ttl: New time-to-live in seconds

        Returns:
            True if successful, False otherwise
        """
        ...

    async def ping(self) -> bool:
        """
        Check if the cache backend is available.

        Returns:
            True if available, False otherwise
        """
        ...

    async def close(self) -> None:
        """Close the cache backend and release resources."""
        ...
