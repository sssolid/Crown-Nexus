# backend/app/services/cache/service.py
"""Main cache service implementation.

This module provides the primary CacheService that coordinates caching
operations across different backends, handling serialization, key management,
and failure recovery.
"""
from __future__ import annotations

import functools
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union, cast

from app.core.logging import get_logger
from app.services.cache.base import CacheBackend, F, RT
from app.services.cache.decorators import cache_invalidate, cached
from app.services.cache.factory import CacheBackendFactory
from app.services.cache.keys import generate_cache_key, make_prefixed_key
from app.services.interfaces import ServiceInterface

logger = get_logger(__name__)


class CacheService(ServiceInterface):
    """Service for caching operations across multiple backends."""

    def __init__(self, default_backend: str = "memory"):
        """
        Initialize the cache service.

        Args:
            default_backend: The default cache backend to use
        """
        self.default_backend = default_backend
        self.initialized = False
        logger.debug(f"CacheService initialized with default backend: {default_backend}")

    async def initialize(self) -> None:
        """Initialize the cache service."""
        if self.initialized:
            return

        logger.debug("Initializing cache service")
        self.initialized = True

    async def ensure_initialized(self) -> None:
        """Ensure the service is initialized."""
        if not self.initialized:
            await self.initialize()

    async def shutdown(self) -> None:
        """Shutdown the cache service."""
        logger.debug("Shutting down cache service")
        await CacheBackendFactory.close_all()

    async def get(self, key: str, default: Any = None, backend: Optional[str] = None) -> Any:
        """
        Get a value from the cache.

        Args:
            key: Cache key
            default: Default value if not found
            backend: Backend to use (defaults to service default)

        Returns:
            Cached value or default
        """
        await self.ensure_initialized()

        try:
            cache_backend = CacheBackendFactory.get_backend(backend or self.default_backend)
            return await cache_backend.get(key, default)
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {str(e)}")
            return default

    async def set(self, key: str, value: Any, ttl: int = 300, backend: Optional[str] = None) -> bool:
        """
        Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
            backend: Backend to use (defaults to service default)

        Returns:
            True if successful, False otherwise
        """
        await self.ensure_initialized()

        try:
            cache_backend = CacheBackendFactory.get_backend(backend or self.default_backend)
            return await cache_backend.set(key, value, ttl)
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {str(e)}")
            return False

    async def delete(self, key: str, backend: Optional[str] = None) -> bool:
        """
        Delete a value from the cache.

        Args:
            key: Cache key
            backend: Backend to use (defaults to service default)

        Returns:
            True if successful, False otherwise
        """
        await self.ensure_initialized()

        try:
            cache_backend = CacheBackendFactory.get_backend(backend or self.default_backend)
            return await cache_backend.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {str(e)}")
            return False

    async def exists(self, key: str, backend: Optional[str] = None) -> bool:
        """
        Check if a key exists in the cache.

        Args:
            key: Cache key
            backend: Backend to use (defaults to service default)

        Returns:
            True if key exists, False otherwise
        """
        await self.ensure_initialized()

        try:
            cache_backend = CacheBackendFactory.get_backend(backend or self.default_backend)
            return await cache_backend.exists(key)
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {str(e)}")
            return False

    async def clear(self, backend: Optional[str] = None) -> bool:
        """
        Clear all values from the cache.

        Args:
            backend: Backend to use (defaults to service default)

        Returns:
            True if successful, False otherwise
        """
        await self.ensure_initialized()

        try:
            cache_backend = CacheBackendFactory.get_backend(backend or self.default_backend)
            return await cache_backend.clear()
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")
            return False

    async def get_or_set(
        self,
        key: str,
        value_func: Callable[[], Any],
        ttl: int = 300,
        backend: Optional[str] = None,
        force_refresh: bool = False
    ) -> Any:
        """
        Get a value from cache or compute and store it.

        Args:
            key: Cache key
            value_func: Function to call if cache miss
            ttl: Time-to-live in seconds
            backend: Backend to use (defaults to service default)
            force_refresh: Force refresh of cache

        Returns:
            Cached or computed value
        """
        await self.ensure_initialized()

        if not force_refresh:
            # Try to get from cache first
            cached_value = await self.get(key, backend=backend)
            if cached_value is not None:
                return cached_value

        # Compute value
        computed_value = value_func()

        # Store in cache
        await self.set(key, computed_value, ttl, backend=backend)

        return computed_value

    async def get_or_set_async(
        self,
        key: str,
        value_func: Callable[[], Any],
        ttl: int = 300,
        backend: Optional[str] = None,
        force_refresh: bool = False
    ) -> Any:
        """
        Get a value from cache or compute and store it asynchronously.

        Args:
            key: Cache key
            value_func: Async function to call if cache miss
            ttl: Time-to-live in seconds
            backend: Backend to use (defaults to service default)
            force_refresh: Force refresh of cache

        Returns:
            Cached or computed value
        """
        await self.ensure_initialized()

        if not force_refresh:
            # Try to get from cache first
            cached_value = await self.get(key, backend=backend)
            if cached_value is not None:
                return cached_value

        # Compute value asynchronously
        computed_value = await value_func()

        # Store in cache
        await self.set(key, computed_value, ttl, backend=backend)

        return computed_value

    async def get_many(self, keys: List[str], backend: Optional[str] = None) -> Dict[str, Any]:
        """
        Get multiple values from cache.

        Args:
            keys: List of cache keys
            backend: Backend to use (defaults to service default)

        Returns:
            Dictionary of cached values
        """
        await self.ensure_initialized()

        try:
            cache_backend = CacheBackendFactory.get_backend(backend or self.default_backend)
            return await cache_backend.get_many(keys)
        except Exception as e:
            logger.error(f"Cache get_many error: {str(e)}")
            return {}

    async def set_many(
        self,
        mapping: Dict[str, Any],
        ttl: int = 300,
        backend: Optional[str] = None
    ) -> bool:
        """
        Set multiple values in cache.

        Args:
            mapping: Dictionary of key-value pairs
            ttl: Time-to-live in seconds
            backend: Backend to use (defaults to service default)

        Returns:
            True if successful, False otherwise
        """
        await self.ensure_initialized()

        try:
            cache_backend = CacheBackendFactory.get_backend(backend or self.default_backend)
            return await cache_backend.set_many(mapping, ttl)
        except Exception as e:
            logger.error(f"Cache set_many error: {str(e)}")
            return False

    async def delete_many(self, keys: List[str], backend: Optional[str] = None) -> int:
        """
        Delete multiple values from cache.

        Args:
            keys: List of cache keys
            backend: Backend to use (defaults to service default)

        Returns:
            Number of keys deleted
        """
        await self.ensure_initialized()

        try:
            cache_backend = CacheBackendFactory.get_backend(backend or self.default_backend)
            return await cache_backend.delete_many(keys)
        except Exception as e:
            logger.error(f"Cache delete_many error: {str(e)}")
            return 0

    async def clear_prefix(self, prefix: str, backend: Optional[str] = None) -> bool:
        """
        Clear all keys with a given prefix.

        Args:
            prefix: Key prefix to match
            backend: Backend to use (defaults to service default)

        Returns:
            True if successful, False otherwise
        """
        await self.ensure_initialized()

        # This is a higher-level operation that depends on the backend implementation
        # For Redis, we can use the SCAN command with a pattern
        # For memory backend, we need to iterate through all keys

        if backend == "redis" or (backend is None and self.default_backend == "redis"):
            # Redis-specific implementation using SCAN
            try:
                from redis.asyncio import Redis
                from app.core.cache.manager import get_redis_pool

                redis_conn = Redis(connection_pool=get_redis_pool())
                pattern = f"{prefix}*"

                # Use SCAN to find matching keys
                cursor = b"0"
                deleted_keys = []

                while True:
                    cursor, keys = await redis_conn.scan(cursor=cursor, match=pattern, count=100)
                    if keys:
                        deleted_keys.extend(keys)
                        await redis_conn.delete(*keys)

                    if cursor == b"0":
                        break

                logger.debug(f"Cleared {len(deleted_keys)} keys with prefix '{prefix}' from Redis")
                return True
            except Exception as e:
                logger.error(f"Redis clear_prefix error: {str(e)}")
                return False
        else:
            # Generic implementation for other backends
            # This is less efficient but works for any backend
            try:
                cache_backend = CacheBackendFactory.get_backend(backend or self.default_backend)

                # For memory backend, we'd need a method to get all keys
                # Since this is not part of the CacheBackend protocol, we'll use a simplified approach
                if isinstance(cache_backend, "MemoryCacheBackend"):
                    # Direct access to cache dictionary
                    keys_to_delete = [k for k in cache_backend.cache.keys() if k.startswith(prefix)]
                    for key in keys_to_delete:
                        await cache_backend.delete(key)
                    logger.debug(f"Cleared {len(keys_to_delete)} keys with prefix '{prefix}' from memory cache")
                    return True
                else:
                    # Fallback for other backends: we can't efficiently clear by prefix
                    logger.warning(f"clear_prefix not efficiently supported for backend: {backend or self.default_backend}")
                    return False
            except Exception as e:
                logger.error(f"Cache clear_prefix error: {str(e)}")
                return False

    # Decorator factory methods
    def cache(
        self,
        prefix: Optional[str] = None,
        ttl: int = 300,
        backend: Optional[str] = None,
        skip_args: Optional[List[str]] = None,
        force_refresh: bool = False,
        cache_none: bool = False,
    ) -> Callable[[F], F]:
        """
        Decorator for caching function results.

        Args:
            prefix: Namespace prefix for cache keys
            ttl: Time-to-live in seconds
            backend: Backend to use (defaults to service default)
            skip_args: List of argument names to exclude from key generation
            force_refresh: Force refresh of cache
            cache_none: Whether to cache None results

        Returns:
            Decorator function
        """
        return cached(
            prefix=prefix,
            ttl=ttl,
            backend=backend or self.default_backend,
            skip_args=skip_args,
            force_refresh=force_refresh,
            cache_none=cache_none,
        )

    def invalidate(
        self,
        prefix: Optional[str] = None,
        backends: Optional[List[str]] = None,
        key_func: Optional[Callable[..., str]] = None,
    ) -> Callable[[F], F]:
        """
        Decorator for invalidating cache entries.

        Args:
            prefix: Namespace prefix for cache keys
            backends: List of cache backends to invalidate
            key_func: Function to generate cache key

        Returns:
            Decorator function
        """
        return cache_invalidate(
            prefix=prefix,
            backends=backends,
            key_func=key_func,
        )
