# backend/app/services/cache/factory.py
"""Factory for creating cache backends.

This module provides a factory for creating different cache backends
based on configuration settings.
"""
from __future__ import annotations

from typing import Dict, Optional

from app.core.config import settings
from app.core.logging import get_logger
from app.services.cache.base import CacheBackend
from app.services.cache.memory import MemoryCacheBackend
from app.services.cache.redis import RedisCacheBackend

logger = get_logger(__name__)


class CacheBackendFactory:
    """Factory for creating and managing cache backends."""

    # Cache of backend instances
    _backends: Dict[str, CacheBackend] = {}

    @classmethod
    def get_backend(cls, backend_type: str) -> CacheBackend:
        """
        Get a cache backend instance.

        Args:
            backend_type: The type of backend to create ('memory', 'redis')

        Returns:
            Cache backend instance

        Raises:
            ValueError: If backend type is not supported
        """
        # Check if backend already exists
        if backend_type in cls._backends:
            return cls._backends[backend_type]

        # Create new backend
        backend = cls._create_backend(backend_type)
        cls._backends[backend_type] = backend
        return backend

    @classmethod
    def _create_backend(cls, backend_type: str) -> CacheBackend:
        """
        Create a new cache backend instance.

        Args:
            backend_type: The type of backend to create

        Returns:
            Cache backend instance

        Raises:
            ValueError: If backend type is not supported
        """
        if backend_type == "memory":
            return cls._create_memory_backend()
        elif backend_type == "redis":
            return cls._create_redis_backend()
        else:
            logger.error(f"Unsupported cache backend type: {backend_type}")
            raise ValueError(f"Unsupported cache backend type: {backend_type}")

    @classmethod
    def _create_memory_backend(cls) -> MemoryCacheBackend:
        """
        Create a memory cache backend.

        Returns:
            Memory cache backend instance
        """
        logger.debug("Creating memory cache backend")
        return MemoryCacheBackend(
            max_size=settings.CACHE_MEMORY_MAX_SIZE,
            default_ttl=settings.CACHE_DEFAULT_TTL,
        )

    @classmethod
    def _create_redis_backend(cls) -> RedisCacheBackend:
        """
        Create a Redis cache backend.

        Returns:
            Redis cache backend instance
        """
        logger.debug("Creating Redis cache backend")
        return RedisCacheBackend(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            username=settings.REDIS_USERNAME,
            password=settings.REDIS_PASSWORD,
            prefix=settings.CACHE_KEY_PREFIX,
            default_ttl=settings.CACHE_DEFAULT_TTL,
        )

    @classmethod
    async def close_all(cls) -> None:
        """Close all backend instances."""
        for backend_name, backend in cls._backends.items():
            try:
                await backend.close()
                logger.debug(f"Closed cache backend: {backend_name}")
            except Exception as e:
                logger.error(f"Error closing cache backend {backend_name}: {str(e)}")

        cls._backends.clear()
