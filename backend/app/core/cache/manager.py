from __future__ import annotations
import logging
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
        """Get cache backend by name."""
        if not self._initialized:
            # Auto-initialize if needed
            import asyncio
            asyncio.create_task(self.initialize())
            return self._backends.get(name, self._backends.get('memory'))

        name = name or settings.CACHE_DEFAULT_BACKEND
        if name not in self._backends:
            raise ValueError(f"Unknown cache backend: {name}")

        return self._backends[name]

    async def initialize(self) -> None:
        """Initialize cache backends."""
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
            except Exception as e:
                logger.warning(f"Failed to initialize Redis cache: {e}")
                # Fall back to memory cache
                self._backends["redis"] = memory_backend
        else:
            # Fall back to memory cache
            self._backends["redis"] = memory_backend

        # Set null cache
        self._backends["null"] = get_backend("null")()

        self._initialized = True

    async def shutdown(self) -> None:
        """Shutdown cache backends."""
        for backend in self._backends.values():
            if hasattr(backend, "shutdown"):
                await backend.shutdown()
        self._backends = {}
        self._initialized = False

# Singleton instance
cache_manager = CacheManager()

async def initialize_cache() -> None:
    """Initialize cache manager."""
    await cache_manager.initialize()
