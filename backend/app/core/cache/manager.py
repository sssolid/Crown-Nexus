from __future__ import annotations

"""
Cache manager for the application.

This module provides a central manager for cache backends,
handling initialization, configuration, and access to backends.
"""

import time
from typing import Dict, Optional, Any, TypeVar, List, Union, cast

from app.core.cache.backends import get_backend
from app.core.cache.base import CacheBackend
from app.core.config import settings
from app.logging import get_logger

logger = get_logger("app.core.cache.manager")

T = TypeVar("T")

# Try to import metrics, but don't fail if not available
try:
    from app.core.dependency_manager import get_dependency

    HAS_METRICS = True
except ImportError:
    HAS_METRICS = False


class CacheManager:
    def __init__(self):
        self._initialized = False
        self.backends: Dict[str, CacheBackend] = {}

    def get_backend(self, name: Optional[str] = None) -> CacheBackend:
        """Get a cache backend by name.

        Args:
            name: The backend name. If None, uses the default backend.

        Returns:
            The cache backend instance.

        Raises:
            ValueError: If the backend is not configured.
        """
        if not self._initialized:
            import asyncio

            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.initialize())
            except RuntimeError:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.initialize())

        name = name or settings.CACHE_DEFAULT_BACKEND
        if name not in self.backends:
            logger.warning(f"Unknown cache backend: {name}, falling back to memory")
            if "memory" not in self.backends:
                raise ValueError(
                    f"Unknown cache backend: {name} and no memory fallback available"
                )
            return self.backends["memory"]
        return self.backends[name]

    async def initialize(self) -> None:
        """Initialize the cache manager and backends."""
        if self._initialized:
            return

        memory_backend = get_backend("memory")()
        self.backends["memory"] = memory_backend
        await memory_backend.initialize()

        if settings.REDIS_HOST:
            try:
                redis_backend = get_backend("redis")()
                await redis_backend.initialize()
                self.backends["redis"] = redis_backend
                logger.info("Redis cache backend initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Redis cache: {e}", exc_info=True)
                self.backends["redis"] = memory_backend
        else:
            logger.info("Redis host not configured, using memory cache as fallback")
            self.backends["redis"] = memory_backend

        self.backends["null"] = get_backend("null")()

        # Register metrics
        if HAS_METRICS:
            try:
                metrics_service = get_dependency("metrics_service")

                # Register metrics for cache operations
                metrics_service.create_counter(
                    "cache_hit_total",
                    "Total number of cache hits",
                    ["backend", "component"],
                )

                metrics_service.create_counter(
                    "cache_miss_total",
                    "Total number of cache misses",
                    ["backend", "component"],
                )

                metrics_service.create_counter(
                    "cache_operations_total",
                    "Total number of cache operations",
                    ["operation", "backend", "component"],
                )

                metrics_service.create_histogram(
                    "cache_operation_duration_seconds",
                    "Duration of cache operations in seconds",
                    ["operation", "backend", "component"],
                )

                logger.info("Cache metrics registered")
            except Exception as e:
                logger.debug(f"Could not register cache metrics: {str(e)}")

        self._initialized = True
        logger.info("Cache manager initialization complete")

    async def shutdown(self) -> None:
        """Shutdown all cache backends."""
        for name, backend in self.backends.items():
            try:
                if hasattr(backend, "shutdown"):
                    await backend.shutdown()
                    logger.debug(f"Shut down {name} cache backend")
            except Exception as e:
                logger.error(
                    f"Error shutting down {name} cache backend: {str(e)}", exc_info=True
                )

        self.backends = {}
        self._initialized = False
        logger.info("Cache manager shutdown complete")

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
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)
        hit = False

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            value = await cache_backend.get(key)
            hit = value is not None
            return value if hit else default

        except Exception as e:
            error = str(e)
            logger.error(f"Error getting cache key {key}: {error}", exc_info=True)
            return default

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="get",
                        backend=backend_name,
                        hit=hit,
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

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
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            result = await cache_backend.set(key, value, ttl)
            return result

        except Exception as e:
            error = str(e)
            logger.error(f"Error setting cache key {key}: {error}", exc_info=True)
            return False

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="set",
                        backend=backend_name,
                        hit=True,  # For set operations, we consider them "hits"
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

    async def delete(self, key: str, backend: Optional[str] = None) -> bool:
        """Delete a value from the cache.

        Args:
            key: The cache key.
            backend: Optional backend name.

        Returns:
            True if successful, False otherwise.
        """
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            result = await cache_backend.delete(key)
            return result

        except Exception as e:
            error = str(e)
            logger.error(f"Error deleting cache key {key}: {error}", exc_info=True)
            return False

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="delete",
                        backend=backend_name,
                        hit=True,  # For delete operations, we consider them "hits"
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

    async def exists(self, key: str, backend: Optional[str] = None) -> bool:
        """Check if a key exists in the cache.

        Args:
            key: The cache key.
            backend: Optional backend name.

        Returns:
            True if key exists, False otherwise.
        """
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            result = await cache_backend.exists(key)
            return result

        except Exception as e:
            error = str(e)
            logger.error(
                f"Error checking if cache key {key} exists: {error}", exc_info=True
            )
            return False

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="exists",
                        backend=backend_name,
                        hit=True,  # For exists operations, we consider them "hits"
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

    async def clear(self, backend: Optional[str] = None) -> bool:
        """Clear the cache.

        Args:
            backend: Optional backend name.

        Returns:
            True if successful, False otherwise.
        """
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            result = await cache_backend.clear()
            return result

        except Exception as e:
            error = str(e)
            logger.error(f"Error clearing cache: {error}", exc_info=True)
            return False

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="clear",
                        backend=backend_name,
                        hit=True,  # For clear operations, we consider them "hits"
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

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
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            count = await cache_backend.invalidate_pattern(pattern)
            logger.debug(
                f"Invalidated {count} cache entries matching pattern: {pattern}"
            )
            return count

        except Exception as e:
            error = str(e)
            logger.error(
                f"Error invalidating cache pattern {pattern}: {error}", exc_info=True
            )
            return 0

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="invalidate_pattern",
                        backend=backend_name,
                        hit=True,  # For invalidate operations, we consider them "hits"
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

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
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)
        hit_count = 0

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            result = await cache_backend.get_many(keys)

            # Count hits for metrics
            if result:
                hit_count = sum(1 for v in result.values() if v is not None)

            return result

        except Exception as e:
            error = str(e)
            logger.error(f"Error getting multiple cache keys: {error}", exc_info=True)
            return {key: None for key in keys}

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time

                    # Track individual get operations for metrics
                    if keys:
                        hit_rate = hit_count / len(keys)
                        metrics_service.track_cache_operation(
                            operation="get_many",
                            backend=backend_name,
                            hit=(
                                hit_rate > 0.5
                            ),  # Consider it a hit if more than half were hits
                            duration=duration,
                            component="cache_manager",
                        )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

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
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            result = await cache_backend.set_many(mapping, ttl)
            return result

        except Exception as e:
            error = str(e)
            logger.error(f"Error setting multiple cache keys: {error}", exc_info=True)
            return False

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="set_many",
                        backend=backend_name,
                        hit=True,  # For set operations, we consider them "hits"
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

    async def delete_many(self, keys: List[str], backend: Optional[str] = None) -> int:
        """Delete multiple values from the cache.

        Args:
            keys: List of cache keys.
            backend: Optional backend name.

        Returns:
            Number of deleted keys.
        """
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            count = await cache_backend.delete_many(keys)
            return count

        except Exception as e:
            error = str(e)
            logger.error(f"Error deleting multiple cache keys: {error}", exc_info=True)
            return 0

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="delete_many",
                        backend=backend_name,
                        hit=True,  # For delete operations, we consider them "hits"
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

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
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            value = await cache_backend.incr(key, amount, default, ttl)
            return value

        except Exception as e:
            error = str(e)
            logger.error(f"Error incrementing cache key {key}: {error}", exc_info=True)
            return default

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="incr",
                        backend=backend_name,
                        hit=True,  # For incr operations, we consider them "hits"
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )

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
        metrics_service = None
        start_time = time.monotonic()
        error = None
        backend_name = backend or settings.CACHE_DEFAULT_BACKEND
        cache_backend = self.get_backend(backend_name)

        try:
            if HAS_METRICS:
                try:
                    metrics_service = get_dependency("metrics_service")
                except Exception as e:
                    logger.debug(f"Could not get metrics service: {str(e)}")

            value = await cache_backend.decr(key, amount, default, ttl)
            return value

        except Exception as e:
            error = str(e)
            logger.error(f"Error decrementing cache key {key}: {error}", exc_info=True)
            return default

        finally:
            if metrics_service and HAS_METRICS:
                try:
                    duration = time.monotonic() - start_time
                    metrics_service.track_cache_operation(
                        operation="decr",
                        backend=backend_name,
                        hit=True,  # For decr operations, we consider them "hits"
                        duration=duration,
                        component="cache_manager",
                    )
                except Exception as metrics_err:
                    logger.warning(
                        f"Failed to record cache metrics: {str(metrics_err)}"
                    )


cache_manager = CacheManager()


async def initialize_cache() -> None:
    """Initialize the cache system."""
    await cache_manager.initialize()
    logger.info("Cache system initialized")
