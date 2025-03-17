# /backend/app/core/cache/base.py
from __future__ import annotations

import abc
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Pattern, Set, TypeVar, Union

T = TypeVar('T')

class CacheBackend(ABC, Generic[T]):
    """Abstract base class for cache backends.
    
    This class defines the interface that all cache backends must implement.
    """
    
    @abstractmethod
    async def get(self, key: str) -> Optional[T]:
        """Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Optional[T]: Cached value or None if not found
        """
        pass
    
    @abstractmethod
    async def set(
        self,
        key: str,
        value: T,
        ttl: Optional[int] = None
    ) -> bool:
        """Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists in the cache.
        
        Args:
            key: Cache key
            
        Returns:
            bool: True if key exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching a pattern.
        
        Args:
            pattern: Key pattern to match
            
        Returns:
            int: Number of keys invalidated
        """
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        """Clear all cached values.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def get_many(self, keys: List[str]) -> Dict[str, Optional[T]]:
        """Get multiple values from the cache.
        
        Args:
            keys: List of cache keys
            
        Returns:
            Dict[str, Optional[T]]: Dictionary of key-value pairs
        """
        pass
    
    @abstractmethod
    async def set_many(
        self,
        mapping: Dict[str, T],
        ttl: Optional[int] = None
    ) -> bool:
        """Set multiple values in the cache.
        
        Args:
            mapping: Dictionary of key-value pairs to cache
            ttl: Time-to-live in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def delete_many(self, keys: List[str]) -> int:
        """Delete multiple values from the cache.
        
        Args:
            keys: List of cache keys
            
        Returns:
            int: Number of keys deleted
        """
        pass
    
    @abstractmethod
    async def incr(
        self,
        key: str,
        amount: int = 1,
        default: int = 0,
        ttl: Optional[int] = None
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
        pass
    
    @abstractmethod
    async def decr(
        self,
        key: str,
        amount: int = 1,
        default: int = 0,
        ttl: Optional[int] = None
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
        pass
