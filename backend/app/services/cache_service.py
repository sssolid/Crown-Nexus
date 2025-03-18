from __future__ import annotations
import asyncio
import functools
from typing import Any, Callable, List, TypeVar, cast

from app.core.cache.keys import generate_cache_key
from app.core.cache.manager import cache_manager
from app.core.dependency_manager import dependency_manager
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.cache_service")
F = TypeVar("F", bound=Callable[..., Any])
RT = TypeVar("RT")  # Return type

class CacheService(ServiceInterface):
    """Unified service for all caching operations."""

    def __init__(self, default_backend: str = "redis"):
        """Initialize cache service.

        Args:
            default_backend: Default cache backend to use
        """
        self.default_backend = default_backend
        dependency_manager.register_dependency("cache_service", self)

    async def get(self, key: str, default: Any = None, backend: str = None) -> Any:
        """Get value from cache.

        Args:
            key: Cache key
            default: Default value if key doesn't exist
            backend: Cache backend to use (defaults to service default)

        Returns:
            Cached value or default
        """
        backend_instance = cache_manager.get_backend(backend or self.default_backend)
        return await backend_instance.get(key, default)

    async def set(self, key: str, value: Any, ttl: int = 300, backend: str = None) -> bool:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
            backend: Cache backend to use (defaults to service default)

        Returns:
            True if successful, False otherwise
        """
        backend_instance = cache_manager.get_backend(backend or self.default_backend)
        return await backend_instance.set(key, value, ttl)

    async def delete(self, key: str, backend: str = None) -> bool:
        """Delete value from cache.

        Args:
            key: Cache key
            backend: Cache backend to use (defaults to service default)

        Returns:
            True if key was deleted, False otherwise
        """
        backend_instance = cache_manager.get_backend(backend or self.default_backend)
        return await backend_instance.delete(key)

    async def exists(self, key: str, backend: str = None) -> bool:
        """Check if key exists in cache.

        Args:
            key: Cache key
            backend: Cache backend to use (defaults to service default)

        Returns:
            True if key exists, False otherwise
        """
        backend_instance = cache_manager.get_backend(backend or self.default_backend)
        return await backend_instance.exists(key)

    async def get_or_set(
        self,
        key: str,
        value_func: Callable[[], Any],
        ttl: int = 300,
        backend: str = None,
        force_refresh: bool = False
    ) -> Any:
        """Get value from cache or compute and store it.

        Args:
            key: Cache key
            value_func: Function to call if cache miss
            ttl: Time-to-live in seconds
            backend: Cache backend to use
            force_refresh: Force refresh of cache

        Returns:
            Cached or computed value
        """
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
        backend: str = None,
        force_refresh: bool = False
    ) -> Any:
        """Get value from cache or compute and store it (async version).

        Args:
            key: Cache key
            value_func: Async function to call if cache miss
            ttl: Time-to-live in seconds
            backend: Cache backend to use
            force_refresh: Force refresh of cache

        Returns:
            Cached or computed value
        """
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

    def cached(
        self,
        prefix: str = None,
        ttl: int = 300,
        backend: str = None,
        skip_args: List[str] = None,
        force_refresh: bool = False
    ) -> Callable[[F], F]:
        """Decorator for caching function results.

        Args:
            prefix: Namespace prefix for cache keys
            ttl: Time-to-live in seconds
            backend: Cache backend to use
            skip_args: List of argument names to exclude from key generation
            force_refresh: Force refresh of cache

        Returns:
            Decorator function
        """
        def decorator(func: F) -> F:
            """Decorator that caches function results."""
            is_async = asyncio.iscoroutinefunction(func)

            if is_async:
                @functools.wraps(func)
                async def async_wrapper(*args, **kwargs):
                    # Generate cache key
                    key = generate_cache_key(prefix or func.__name__, func, args, kwargs, skip_args)

                    if force_refresh:
                        # Bypass cache
                        result = await func(*args, **kwargs)
                        await self.set(key, result, ttl, backend=backend)
                        return result

                    # Try to get from cache
                    cached_result = await self.get(key, backend=backend)
                    if cached_result is not None:
                        return cached_result

                    # Cache miss, call function
                    result = await func(*args, **kwargs)

                    # Store result in cache
                    await self.set(key, result, ttl, backend=backend)

                    return result
                return cast(F, async_wrapper)
            else:
                @functools.wraps(func)
                def sync_wrapper(*args, **kwargs):
                    # Generate cache key
                    key = generate_cache_key(prefix or func.__name__, func, args, kwargs, skip_args)

                    # For sync functions, we still need to run this in an event loop
                    async def _get_cached():
                        if force_refresh:
                            # Bypass cache
                            result = func(*args, **kwargs)
                            await self.set(key, result, ttl, backend=backend)
                            return result

                        # Try to get from cache
                        cached_result = await self.get(key, backend=backend)
                        if cached_result is not None:
                            return cached_result

                        # Cache miss, call function
                        result = func(*args, **kwargs)

                        # Store result in cache
                        await self.set(key, result, ttl, backend=backend)

                        return result

                    # Run in event loop
                    loop = asyncio.get_event_loop()
                    return loop.run_until_complete(_get_cached())
                return cast(F, sync_wrapper)

        return decorator

    async def initialize(self) -> None:
        """Initialize the cache service."""
        # Nothing to initialize here as backend initialization
        # is handled by the cache manager
        pass

    async def shutdown(self) -> None:
        """Shutdown the cache service."""
        # Nothing to shutdown here as backend shutdown
        # is handled by the cache manager
        pass
