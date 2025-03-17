# /backend/app/core/cache/manager.py
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Type

from app.core.cache.base import CacheBackend
from app.core.cache.memory import MemoryCacheBackend
from app.core.cache.redis import RedisCacheBackend
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("app.core.cache.manager")

class CacheManager:
    """Manager for multiple cache backends.
    
    This class provides a centralized interface for all caching operations,
    with support for multiple cache backends.
    """
    
    def __init__(self) -> None:
        """Initialize the cache manager."""
        self.backends: Dict[str, CacheBackend] = {}
        self.default_backend: Optional[str] = None
        
    def register_backend(
        self,
        name: str,
        backend: CacheBackend,
        set_as_default: bool = False
    ) -> None:
        """Register a cache backend.
        
        Args:
            name: Backend name
            backend: Cache backend instance
            set_as_default: Whether to set as default backend
        """
        self.backends[name] = backend
        
        if set_as_default or self.default_backend is None:
            self.default_backend = name
            
        logger.debug(f"Registered cache backend: {name}")
        
    def _get_backend(self, backend_name: Optional[str] = None) -> CacheBackend:
        """Get a cache backend by name.
        
        Args:
            backend_name: Backend name
            
        Returns:
            CacheBackend: Cache backend
            
        Raises:
            ValueError: If backend not found
        """
        name = backend_name or self.default_backend
        
        if name is None:
            raise ValueError("No default cache backend registered")
            
        if name not in self.backends:
            raise ValueError(f"Cache backend not found: {name}")
            
        return self.backends[name]
        
    async def get(
        self,
        key: str,
        backend_name: Optional[str] = None
    ) -> Optional[Any]:
        """Get a value from the cache.
        
        Args:
            key: Cache key
            backend_name: Backend name
            
        Returns:
            Optional[Any]: Cached value or None if not found
        """
        backend = self._get_backend(backend_name)
        return await backend.get(key)
        
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        backend_name: Optional[str] = None
    ) -> bool:
        """Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
            backend_name: Backend name
            
        Returns:
            bool: True if successful, False otherwise
        """
        backend = self._get_backend(backend_name)
        return await backend.set(key, value, ttl)
        
    async def delete(
        self,
        key: str,
        backend_name: Optional[str] = None
    ) -> bool:
        """Delete a value from the cache.
        
        Args:
            key: Cache key
            backend_name: Backend name
            
        Returns:
            bool: True if key was deleted, False if key wasn't found
        """
        backend = self._get_backend(backend_name)
        return await backend.delete(key)
        
    async def exists(
        self,
        key: str,
        backend_name: Optional[str] = None
    ) -> bool:
        """Check if a key exists in the cache.
        
        Args:
            key: Cache key
            backend_name: Backend name
            
        Returns:
            bool: True if key exists, False otherwise
        """
        backend = self._get_backend(backend_name)
        return await backend.exists(key)
        
    async def invalidate_pattern(
        self,
        pattern: str,
        backend_name: Optional[str] = None
    ) -> int:
        """Invalidate all keys matching a pattern.
        
        Args:
            pattern: Key pattern to match
            backend_name: Backend name
            
        Returns:
            int: Number of keys invalidated
        """
        backend = self._get_backend(backend_name)
        return await backend.invalidate_pattern(pattern)
        
    async def clear(
        self,
        backend_name: Optional[str] = None
    ) -> bool:
        """Clear all cached values.
        
        Args:
            backend_name: Backend name
            
        Returns:
            bool: True if successful, False otherwise
        """
        if backend_name is not None:
            # Clear specific backend
            backend = self._get_backend(backend_name)
            return await backend.clear()
        else:
            # Clear all backends
            results = []
            for name, backend in self.backends.items():
                results.append(await backend.clear())
            return all(results)
        
    async def get_many(
        self,
        keys: List[str],
        backend_name: Optional[str] = None
    ) -> Dict[str, Optional[Any]]:
        """Get multiple values from the cache.
        
        Args:
            keys: List of cache keys
            backend_name: Backend name
            
        Returns:
            Dict[str, Optional[Any]]: Dictionary of key-value pairs
        """
        backend = self._get_backend(backend_name)
        return await backend.get_many(keys)
        
    async def set_many(
        self,
        mapping: Dict[str, Any],
        ttl: Optional[int] = None,
        backend_name: Optional[str] = None
    ) -> bool:
        """Set multiple values in the cache.
        
        Args:
            mapping: Dictionary of key-value pairs to cache
            ttl: Time-to-live in seconds
            backend_name: Backend name
            
        Returns:
            bool: True if successful, False otherwise
        """
        backend = self._get_backend(backend_name)
        return await backend.set_many(mapping, ttl)
        
    async def delete_many(
        self,
        keys: List[str],
        backend_name: Optional[str] = None
    ) -> int:
        """Delete multiple values from the cache.
        
        Args:
            keys: List of cache keys
            backend_name: Backend name
            
        Returns:
            int: Number of keys deleted
        """
        backend = self._get_backend(backend_name)
        return await backend.delete_many(keys)
        
    async def incr(
        self,
        key: str,
        amount: int = 1,
        default: int = 0,
        ttl: Optional[int] = None,
        backend_name: Optional[str] = None
    ) -> int:
        """Increment a counter in the cache.
        
        Args:
            key: Cache key
            amount: Amount to increment by
            default: Default value if key doesn't exist
            ttl: Time-to-live in seconds
            backend_name: Backend name
            
        Returns:
            int: New counter value
        """
        backend = self._get_backend(backend_name)
        return await backend.incr(key, amount, default, ttl)
        
    async def decr(
        self,
        key: str,
        amount: int = 1,
        default: int = 0,
        ttl: Optional[int] = None,
        backend_name: Optional[str] = None
    ) -> int:
        """Decrement a counter in the cache.
        
        Args:
            key: Cache key
            amount: Amount to decrement by
            default: Default value if key doesn't exist
            ttl: Time-to-live in seconds
            backend_name: Backend name
            
        Returns:
            int: New counter value
        """
        backend = self._get_backend(backend_name)
        return await backend.decr(key, amount, default, ttl)
        
    async def get_or_set(
        self,
        key: str,
        default_factory: callable,
        ttl: Optional[int] = None,
        backend_name: Optional[str] = None
    ) -> Any:
        """Get a value from the cache or set it if not found.
        
        Args:
            key: Cache key
            default_factory: Function to call to get default value
            ttl: Time-to-live in seconds
            backend_name: Backend name
            
        Returns:
            Any: Cached value or default value
        """
        # Try to get cached value
        value = await self.get(key, backend_name)
        
        if value is not None:
            return value
            
        # If not found, call default_factory
        value = default_factory()
        
        # Cache value
        await self.set(key, value, ttl, backend_name)
        
        return value
        
    async def get_or_set_async(
        self,
        key: str,
        default_factory: callable,
        ttl: Optional[int] = None,
        backend_name: Optional[str] = None
    ) -> Any:
        """Get a value from the cache or set it if not found (async version).
        
        Args:
            key: Cache key
            default_factory: Async function to call to get default value
            ttl: Time-to-live in seconds
            backend_name: Backend name
            
        Returns:
            Any: Cached value or default value
        """
        # Try to get cached value
        value = await self.get(key, backend_name)
        
        if value is not None:
            return value
            
        # If not found, call default_factory
        value = await default_factory()
        
        # Cache value
        await self.set(key, value, ttl, backend_name)
        
        return value

# Create singleton instance
cache_manager = CacheManager()

# Initialize cache backends
def initialize_cache() -> None:
    """Initialize cache backends.
    
    This function should be called during application startup to initialize
    all cache backends.
    """
    # Register memory cache backend
    memory_cache = MemoryCacheBackend(
        max_size=1000,
        clean_interval=60
    )
    cache_manager.register_backend("memory", memory_cache, True)
    
    # Register Redis cache backend if configured
    if hasattr(settings, "redis") and hasattr(settings.redis, "uri"):
        redis_cache = RedisCacheBackend(
            redis_url=settings.redis.uri,
            serializer="pickle",
            prefix="crown_nexus:"
        )
        cache_manager.register_backend("redis", redis_cache)
        
    logger.info("Cache backends initialized")
