# backend/app/core/cache/manager.py
from __future__ import annotations
from typing import Any, Dict, Optional, Type, Union

from app.core.cache.backends import get_backend
from app.core.cache.base import CacheBackend
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("app.core.cache.manager")


class CacheManager:
    """Manager for cache backends."""

    def __init__(self):
        self._initialized = False
        self._backends: Dict[str, CacheBackend] = {}

    def get_backend(self, name: str = None) -> CacheBackend:
        """Get cache backend by name.

        Args:
            name: Backend name (defaults to the configured default backend)

        Returns:
            CacheBackend: The requested cache backend

        Raises:
            ValueError: If the backend name is unknown
        """
        if not self._initialized:
            # Auto-initialize if needed
            import asyncio

            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.initialize())
            except RuntimeError:
                # No running event loop
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.initialize())

        name = name or settings.CACHE_DEFAULT_BACKEND
        if name not in self._backends:
            logger.warning(f"Unknown cache backend: {name}, falling back to memory")
            return self._backends.get("memory")

        return self._backends[name]

    async def initialize(self) -> None:
        """Initialize cache backends.

        This method sets up all configured cache backends during application startup.
        """
        if self._initialized:
            return

        # Initialize memory cache
        memory_backend = get_backend("memory")()
        self._backends["memory"] = memory_backend

        # Initialize Redis cache if configured
        if settings.REDIS_HOST:
            try:
                redis_backend = get_backend("redis")()
                await redis_backend.initialize()
                self._backends["redis"] = redis_backend
                logger.info("Redis cache backend initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Redis cache: {e}")
                # Fall back to memory cache
                self._backends["redis"] = memory_backend
        else:
            logger.info("Redis host not configured, using memory cache as fallback")
            # Fall back to memory cache
            self._backends["redis"] = memory_backend

        # Set null cache
        self._backends["null"] = get_backend("null")()

        self._initialized = True
        logger.info("Cache manager initialization complete")

    async def shutdown(self) -> None:
        """Shutdown cache backends.

        This method properly closes all cache backend connections during application shutdown.
        """
        for name, backend in self._backends.items():
            try:
                if hasattr(backend, "shutdown"):
                    await backend.shutdown()
                    logger.debug(f"Shut down {name} cache backend")
            except Exception as e:
                logger.error(f"Error shutting down {name} cache backend: {str(e)}")

        self._backends = {}
        self._initialized = False
        logger.info("Cache manager shutdown complete")


# Singleton instance
cache_manager = CacheManager()


async def initialize_cache() -> None:
    """Initialize cache manager.

    This function is called during application startup to initialize all cache backends.
    """
    await cache_manager.initialize()
    logger.info("Cache system initialized")
