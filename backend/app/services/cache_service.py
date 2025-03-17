# app/services/cache_service.py
from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
import logging
import time
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, Generic, List, Optional, Set, Type, TypeVar, Union, cast

from fastapi import Depends, Request
from pydantic import BaseModel

from app.core.cache.base import CacheBackend
from app.core.cache.keys import generate_cache_key, generate_list_key, generate_model_key, generate_query_key
from app.core.cache.manager import cache_manager
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

logger = get_logger("app.services.cache_service")

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


@dataclass
class CacheConfig:
    """Configuration for cache policies."""

    enabled: bool = True
    default_ttl: int = 3600  # 1 hour in seconds
    model_ttl: int = 3600  # 1 hour
    list_ttl: int = 300  # 5 minutes
    query_ttl: int = 300  # 5 minutes
    user_ttl: int = 1800  # 30 minutes
    always_refresh_on_write: bool = False  # Whether to always refresh cache on write operations
    allow_stale_on_error: bool = True  # Whether to return stale data on backend errors
    stale_grace_period: int = 86400  # 24 hours - how long to serve stale data after expiration


class CacheStrategy(str):
    """Cache strategy types."""

    NONE = "none"  # No caching
    READ_THROUGH = "read_through"  # Read from cache first, fall back to backend
    WRITE_THROUGH = "write_through"  # Write to cache and backend simultaneously
    WRITE_BACK = "write_back"  # Write to cache immediately, write to backend asynchronously
    WRITE_AROUND = "write_around"  # Write to backend only, invalidate cache
    REFRESH_AHEAD = "refresh_ahead"  # Preemptively refresh cache before expiration


class CacheTags:
    """Cache tag prefixes for groups of related cache entries."""

    USER = "user"
    PRODUCT = "product"
    ORDER = "order"
    COMPANY = "company"
    FITMENT = "fitment"
    MEDIA = "media"
    SETTINGS = "settings"
    CHAT = "chat"
    QUERY = "query"
    REPORT = "report"


class CacheService:
    """Service for managing application caching.

    This service provides methods for caching and retrieving data,
    managing cache invalidation, and implementing different caching strategies.
    """

    def __init__(self) -> None:
        """Initialize the cache service."""
        self.logger = logger
        self.config = CacheConfig()

        # Reference to the cache backends in the manager
        self.redis_available = "redis" in cache_manager.backends
        self.memory_available = "memory" in cache_manager.backends

        # Default tags for entities (for cache invalidation)
        self.entity_tags: Dict[str, str] = {
            "user": CacheTags.USER,
            "product": CacheTags.PRODUCT,
            "order": CacheTags.ORDER,
            "company": CacheTags.COMPANY,
            "fitment": CacheTags.FITMENT,
            "media": CacheTags.MEDIA,
            "setting": CacheTags.SETTINGS,
            "chat": CacheTags.CHAT,
        }

    async def initialize(self) -> None:
        """Initialize the cache service."""
        self.logger.debug("Initializing cache service")

    async def shutdown(self) -> None:
        """Shutdown the cache service."""
        self.logger.debug("Shutting down cache service")

    async def get(self, key: str, default: Optional[T] = None, backend: Optional[str] = None) -> Optional[T]:
        """Get a value from the cache.

        Args:
            key: Cache key
            default: Default value if key doesn't exist
            backend: Optional backend name

        Returns:
            Cached value or default if not found
        """
        if not self.config.enabled:
            return default

        value = await cache_manager.get(key, backend)
        if value is None:
            return default

        self.logger.debug(f"Cache hit for key: {key}", backend=backend or "default")
        return value

    async def set(
        self,
        key: str,
        value: T,
        ttl: Optional[int] = None,
        backend: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
            backend: Optional backend name
            tags: Optional list of tags for cache invalidation

        Returns:
            True if successful, False otherwise
        """
        if not self.config.enabled:
            return False

        ttl = ttl if ttl is not None else self.config.default_ttl

        # Store value in cache
        result = await cache_manager.set(key, value, ttl, backend)

        # If we have tags, store the key in tag sets for later invalidation
        if tags and result and self.redis_available:
            for tag in tags:
                tag_key = f"cache:tag:{tag}"
                # Use Redis SET data structure to store keys associated with this tag
                redis_backend = cache_manager.backends.get("redis")
                if hasattr(redis_backend, "add_to_set"):
                    await redis_backend.add_to_set(tag_key, key)

        self.logger.debug(f"Cache set for key: {key}", ttl=ttl, backend=backend or "default", tags=tags)
        return result

    async def delete(self, key: str, backend: Optional[str] = None) -> bool:
        """Delete a value from the cache.

        Args:
            key: Cache key
            backend: Optional backend name

        Returns:
            True if successful, False otherwise
        """
        if not self.config.enabled:
            return False

        result = await cache_manager.delete(key, backend)
        self.logger.debug(f"Cache deleted for key: {key}", backend=backend or "default")
        return result

    async def exists(self, key: str, backend: Optional[str] = None) -> bool:
        """Check if a key exists in the cache.

        Args:
            key: Cache key
            backend: Optional backend name

        Returns:
            True if key exists, False otherwise
        """
        if not self.config.enabled:
            return False

        return await cache_manager.exists(key, backend)

    async def invalidate_pattern(self, pattern: str, backend: Optional[str] = None) -> int:
        """Invalidate keys matching a pattern.

        Args:
            pattern: Key pattern to invalidate
            backend: Optional backend name

        Returns:
            Number of invalidated keys
        """
        if not self.config.enabled:
            return 0

        count = await cache_manager.invalidate_pattern(pattern, backend)
        self.logger.debug(f"Invalidated {count} keys matching pattern: {pattern}", backend=backend or "default")
        return count

    async def invalidate_tag(self, tag: str) -> int:
        """Invalidate all keys associated with a tag.

        Args:
            tag: Tag to invalidate

        Returns:
            Number of invalidated keys
        """
        if not self.config.enabled or not self.redis_available:
            return 0

        try:
            tag_key = f"cache:tag:{tag}"
            redis_backend = cache_manager.backends.get("redis")

            # Get all keys for this tag
            if hasattr(redis_backend, "get_set_members"):
                keys = await redis_backend.get_set_members(tag_key)

                if not keys:
                    return 0

                # Delete all the keys
                count = await cache_manager.delete_many(keys)

                # Delete the tag set itself
                await redis_backend.delete(tag_key)

                self.logger.debug(f"Invalidated {count} keys with tag: {tag}")
                return count

            return 0
        except Exception as e:
            self.logger.error(f"Error invalidating tag: {str(e)}", tag=tag)
            return 0

    async def invalidate_entity(self, entity_type: str, entity_id: str) -> int:
        """Invalidate all cache entries related to a specific entity.

        Args:
            entity_type: Type of entity (e.g., "user", "product")
            entity_id: ID of the entity

        Returns:
            Number of invalidated cache entries
        """
        if not self.config.enabled:
            return 0

        tag = self.entity_tags.get(entity_type.lower(), entity_type.lower())

        # Invalidate by tag first
        tag_count = await self.invalidate_tag(f"{tag}:{entity_id}")

        # Also invalidate by pattern for backends that don't support tags
        pattern_count = await self.invalidate_pattern(f"{tag}:{entity_id}:*")

        # Add specific model key invalidation
        model_key = generate_model_key("model", entity_type, entity_id)
        model_result = await self.delete(model_key)

        return tag_count + pattern_count + (1 if model_result else 0)

    async def clear(self, backend: Optional[str] = None) -> bool:
        """Clear all cache data.

        Args:
            backend: Optional backend name

        Returns:
            True if successful, False otherwise
        """
        if not self.config.enabled:
            return False

        result = await cache_manager.clear(backend)
        self.logger.info(f"Cache cleared", backend=backend or "all")
        return result

    async def get_many(self, keys: List[str], backend: Optional[str] = None) -> Dict[str, Optional[T]]:
        """Get multiple values from the cache.

        Args:
            keys: List of cache keys
            backend: Optional backend name

        Returns:
            Dictionary mapping keys to values
        """
        if not self.config.enabled or not keys:
            return {key: None for key in keys}

        return await cache_manager.get_many(keys, backend)

    async def set_many(
        self,
        mapping: Dict[str, T],
        ttl: Optional[int] = None,
        backend: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Set multiple values in the cache.

        Args:
            mapping: Dictionary mapping keys to values
            ttl: Time-to-live in seconds
            backend: Optional backend name
            tags: Optional list of tags for cache invalidation

        Returns:
            True if successful, False otherwise
        """
        if not self.config.enabled or not mapping:
            return False

        ttl = ttl if ttl is not None else self.config.default_ttl

        # Store values in cache
        result = await cache_manager.set_many(mapping, ttl, backend)

        # If we have tags, store the keys in tag sets for later invalidation
        if tags and result and self.redis_available:
            for tag in tags:
                tag_key = f"cache:tag:{tag}"
                # Use Redis SET data structure to store keys associated with this tag
                redis_backend = cache_manager.backends.get("redis")
                if hasattr(redis_backend, "add_many_to_set"):
                    await redis_backend.add_many_to_set(tag_key, list(mapping.keys()))

        self.logger.debug(f"Cache set for {len(mapping)} keys", ttl=ttl, backend=backend or "default", tags=tags)
        return result

    async def delete_many(self, keys: List[str], backend: Optional[str] = None) -> int:
        """Delete multiple values from the cache.

        Args:
            keys: List of cache keys
            backend: Optional backend name

        Returns:
            Number of deleted keys
        """
        if not self.config.enabled or not keys:
            return 0

        count = await cache_manager.delete_many(keys, backend)
        self.logger.debug(f"Cache deleted for {count} keys", backend=backend or "default")
        return count

    async def get_or_set(
        self,
        key: str,
        value_func: Callable[[], T],
        ttl: Optional[int] = None,
        backend: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> T:
        """Get a value from cache or compute and store it if not present.

        Args:
            key: Cache key
            value_func: Function to compute the value
            ttl: Time-to-live in seconds
            backend: Optional backend name
            tags: Optional list of tags for cache invalidation

        Returns:
            Cached or computed value
        """
        if not self.config.enabled:
            return value_func()

        # Try to get from cache first
        cached_value = await self.get(key, backend=backend)
        if cached_value is not None:
            return cached_value

        # Compute value
        value = value_func()

        # Store in cache if not None
        if value is not None:
            await self.set(key, value, ttl, backend, tags)

        return value

    async def get_or_set_async(
        self,
        key: str,
        value_func: Callable[[], Any],
        ttl: Optional[int] = None,
        backend: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Any:
        """Get a value from cache or compute and store it if not present (async version).

        Args:
            key: Cache key
            value_func: Async function to compute the value
            ttl: Time-to-live in seconds
            backend: Optional backend name
            tags: Optional list of tags for cache invalidation

        Returns:
            Cached or computed value
        """
        if not self.config.enabled:
            return await value_func()

        # Try to get from cache first
        cached_value = await self.get(key, backend=backend)
        if cached_value is not None:
            return cached_value

        # Compute value
        value = await value_func()

        # Store in cache if not None
        if value is not None:
            await self.set(key, value, ttl, backend, tags)

        return value

    async def get_model(
        self,
        model_name: str,
        model_id: str,
        loader_func: Optional[Callable[[], Any]] = None,
        backend: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get a model from cache or load it from the database.

        Args:
            model_name: Model/entity name
            model_id: Entity ID
            loader_func: Optional function to load the model if not in cache
            backend: Optional backend name

        Returns:
            Model data dictionary or None
        """
        key = generate_model_key("model", model_name, model_id)

        if loader_func:
            return await self.get_or_set_async(
                key,
                loader_func,
                ttl=self.config.model_ttl,
                backend=backend,
                tags=[f"{self.entity_tags.get(model_name.lower(), model_name.lower())}:{model_id}"]
            )

        return await self.get(key, backend=backend)

    async def set_model(
        self,
        model_name: str,
        model_id: str,
        data: Dict[str, Any],
        ttl: Optional[int] = None,
        backend: Optional[str] = None
    ) -> bool:
        """Cache a model.

        Args:
            model_name: Model/entity name
            model_id: Entity ID
            data: Model data to cache
            ttl: Time-to-live in seconds
            backend: Optional backend name

        Returns:
            True if successful, False otherwise
        """
        key = generate_model_key("model", model_name, model_id)
        tag = self.entity_tags.get(model_name.lower(), model_name.lower())

        return await self.set(
            key,
            data,
            ttl or self.config.model_ttl,
            backend,
            tags=[f"{tag}:{model_id}"]
        )

    async def invalidate_model(
        self,
        model_name: str,
        model_id: str,
        backend: Optional[str] = None
    ) -> bool:
        """Invalidate a cached model.

        Args:
            model_name: Model/entity name
            model_id: Entity ID
            backend: Optional backend name

        Returns:
            True if successful, False otherwise
        """
        key = generate_model_key("model", model_name, model_id)

        # Also invalidate related keys by tag
        await self.invalidate_entity(model_name, model_id)

        return await self.delete(key, backend)

    async def get_model_list(
        self,
        model_name: str,
        filters: Optional[Dict[str, Any]] = None,
        loader_func: Optional[Callable[[], Any]] = None,
        backend: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Get a list of models from cache or load them from the database.

        Args:
            model_name: Model/entity name
            filters: Optional filters for the list
            loader_func: Optional function to load the list if not in cache
            backend: Optional backend name

        Returns:
            List of model data or None
        """
        key = generate_list_key("list", model_name, filters)
        tag = self.entity_tags.get(model_name.lower(), model_name.lower())

        if loader_func:
            return await self.get_or_set_async(
                key,
                loader_func,
                ttl=self.config.list_ttl,
                backend=backend,
                tags=[f"{tag}:list"]
            )

        return await self.get(key, backend=backend)

    async def set_model_list(
        self,
        model_name: str,
        data: List[Dict[str, Any]],
        filters: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
        backend: Optional[str] = None
    ) -> bool:
        """Cache a list of models.

        Args:
            model_name: Model/entity name
            data: List of model data to cache
            filters: Optional filters for the list
            ttl: Time-to-live in seconds
            backend: Optional backend name

        Returns:
            True if successful, False otherwise
        """
        key = generate_list_key("list", model_name, filters)
        tag = self.entity_tags.get(model_name.lower(), model_name.lower())

        return await self.set(
            key,
            data,
            ttl or self.config.list_ttl,
            backend,
            tags=[f"{tag}:list"]
        )

    async def invalidate_model_list(
        self,
        model_name: str,
        backend: Optional[str] = None
    ) -> int:
        """Invalidate all cached lists of a model type.

        Args:
            model_name: Model/entity name
            backend: Optional backend name

        Returns:
            Number of invalidated cache entries
        """
        tag = self.entity_tags.get(model_name.lower(), model_name.lower())

        # Invalidate tag
        tag_count = await self.invalidate_tag(f"{tag}:list")

        # Also invalidate by pattern
        pattern = f"list:{model_name}:*"
        pattern_count = await self.invalidate_pattern(pattern, backend)

        return tag_count + pattern_count

    async def get_query(
        self,
        query_name: str,
        params: Optional[Dict[str, Any]] = None,
        loader_func: Optional[Callable[[], Any]] = None,
        backend: Optional[str] = None
    ) -> Optional[Any]:
        """Get query results from cache or execute the query.

        Args:
            query_name: Name of the query
            params: Optional query parameters
            loader_func: Optional function to execute the query if results not in cache
            backend: Optional backend name

        Returns:
            Query results or None
        """
        key = generate_query_key("query", query_name, params)

        if loader_func:
            return await self.get_or_set_async(
                key,
                loader_func,
                ttl=self.config.query_ttl,
                backend=backend,
                tags=[f"{CacheTags.QUERY}:{query_name}"]
            )

        return await self.get(key, backend=backend)

    async def set_query(
        self,
        query_name: str,
        data: Any,
        params: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
        backend: Optional[str] = None
    ) -> bool:
        """Cache query results.

        Args:
            query_name: Name of the query
            data: Query results to cache
            params: Optional query parameters
            ttl: Time-to-live in seconds
            backend: Optional backend name

        Returns:
            True if successful, False otherwise
        """
        key = generate_query_key("query", query_name, params)

        return await self.set(
            key,
            data,
            ttl or self.config.query_ttl,
            backend,
            tags=[f"{CacheTags.QUERY}:{query_name}"]
        )

    async def invalidate_query(
        self,
        query_name: str,
        backend: Optional[str] = None
    ) -> int:
        """Invalidate all cached results for a query.

        Args:
            query_name: Name of the query
            backend: Optional backend name

        Returns:
            Number of invalidated cache entries
        """
        # Invalidate tag
        tag_count = await self.invalidate_tag(f"{CacheTags.QUERY}:{query_name}")

        # Also invalidate by pattern
        pattern = f"query:{query_name}:*"
        pattern_count = await self.invalidate_pattern(pattern, backend)

        return tag_count + pattern_count

    def cached(
        self,
        ttl: Optional[int] = None,
        prefix: str = "cache",
        backend: Optional[str] = None,
        tags: Optional[List[str]] = None,
        strategy: str = CacheStrategy.READ_THROUGH
    ):
        """Decorator for caching function results.

        Args:
            ttl: Time-to-live in seconds
            prefix: Cache key prefix
            backend: Optional backend name
            tags: Optional list of tags for cache invalidation
            strategy: Caching strategy

        Returns:
            Decorator function
        """
        def decorator(func: Callable):
            is_async = asyncio.iscoroutinefunction(func)

            cache_ttl = ttl or self.config.default_ttl

            if is_async:
                @wraps(func)
                async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                    if not self.config.enabled or strategy == CacheStrategy.NONE:
                        return await func(*args, **kwargs)

                    # Generate cache key based on function and arguments
                    key = self._generate_cache_key(prefix, func, args, kwargs)

                    # Read-through strategy: try cache first
                    if strategy in [CacheStrategy.READ_THROUGH, CacheStrategy.WRITE_THROUGH, CacheStrategy.REFRESH_AHEAD]:
                        cached_value = await self.get(key, backend=backend)
                        if cached_value is not None:
                            # For refresh-ahead, asynchronously refresh the cache if approaching expiration
                            if strategy == CacheStrategy.REFRESH_AHEAD and self.redis_available:
                                redis_backend = cache_manager.backends.get("redis")
                                if hasattr(redis_backend, "get_ttl"):
                                    remaining_ttl = await redis_backend.get_ttl(key)
                                    refresh_threshold = cache_ttl * 0.1  # Refresh when 10% of TTL remains

                                    if remaining_ttl is not None and remaining_ttl < refresh_threshold:
                                        # Asynchronously refresh the cache
                                        asyncio.create_task(self._refresh_cache_entry(func, args, kwargs, key, cache_ttl, backend, tags))

                            return cached_value

                    # Execute function
                    result = await func(*args, **kwargs)

                    # Cache the result if appropriate
                    if result is not None and strategy in [CacheStrategy.READ_THROUGH, CacheStrategy.WRITE_THROUGH, CacheStrategy.REFRESH_AHEAD]:
                        await self.set(key, result, cache_ttl, backend, tags)

                    return result

                return async_wrapper
            else:
                @wraps(func)
                def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                    if not self.config.enabled or strategy == CacheStrategy.NONE:
                        return func(*args, **kwargs)

                    # Generate cache key based on function and arguments
                    key = self._generate_cache_key(prefix, func, args, kwargs)

                    # Read-through strategy: try cache first
                    if strategy in [CacheStrategy.READ_THROUGH, CacheStrategy.WRITE_THROUGH, CacheStrategy.REFRESH_AHEAD]:
                        cached_value = asyncio.run(self.get(key, backend=backend))
                        if cached_value is not None:
                            return cached_value

                    # Execute function
                    result = func(*args, **kwargs)

                    # Cache the result if appropriate
                    if result is not None and strategy in [CacheStrategy.READ_THROUGH, CacheStrategy.WRITE_THROUGH, CacheStrategy.REFRESH_AHEAD]:
                        asyncio.run(self.set(key, result, cache_ttl, backend, tags))

                    return result

                return sync_wrapper

        return decorator

    def invalidate_after(
        self,
        model_name: Optional[str] = None,
        model_param: Optional[str] = None,
        tags: Optional[List[str]] = None,
        patterns: Optional[List[str]] = None
    ):
        """Decorator to invalidate cache after function execution.

        Args:
            model_name: Optional model name for invalidation
            model_param: Optional parameter name containing model ID
            tags: Optional list of tags to invalidate
            patterns: Optional list of patterns to invalidate

        Returns:
            Decorator function
        """
        def decorator(func: Callable):
            is_async = asyncio.iscoroutinefunction(func)

            if is_async:
                @wraps(func)
                async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                    result = await func(*args, **kwargs)

                    # Invalidate model cache if specified
                    if model_name and model_param and model_param in kwargs:
                        model_id = kwargs.get(model_param)
                        if model_id:
                            await self.invalidate_entity(model_name, str(model_id))

                    # Invalidate by tags
                    if tags:
                        for tag in tags:
                            await self.invalidate_tag(tag)

                    # Invalidate by patterns
                    if patterns:
                        for pattern in patterns:
                            await self.invalidate_pattern(pattern)

                    return result

                return async_wrapper
            else:
                @wraps(func)
                def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                    result = func(*args, **kwargs)

                    # Run cache invalidation in an asyncio event loop
                    async def invalidate():
                        # Invalidate model cache if specified
                        if model_name and model_param and model_param in kwargs:
                            model_id = kwargs.get(model_param)
                            if model_id:
                                await self.invalidate_entity(model_name, str(model_id))

                        # Invalidate by tags
                        if tags:
                            for tag in tags:
                                await self.invalidate_tag(tag)

                        # Invalidate by patterns
                        if patterns:
                            for pattern in patterns:
                                await self.invalidate_pattern(pattern)

                    asyncio.run(invalidate())

                    return result

                return sync_wrapper

        return decorator

    def _generate_cache_key(self, prefix: str, func: Callable, args: tuple, kwargs: dict) -> str:
        """Generate a cache key for a function call.

        Args:
            prefix: Cache key prefix
            func: Function being called
            args: Function arguments
            kwargs: Function keyword arguments

        Returns:
            Cache key
        """
        # Create function signature
        func_name = f"{func.__module__}.{func.__qualname__}"

        # Convert args and kwargs to a deterministic string
        args_str = json.dumps([self._prepare_for_json(arg) for arg in args], sort_keys=True)
        kwargs_str = json.dumps({k: self._prepare_for_json(v) for k, v in kwargs.items()}, sort_keys=True)

        # Generate hash
        key_parts = [prefix, func_name, args_str, kwargs_str]
        key_hash = hashlib.md5(json.dumps(key_parts).encode("utf-8")).hexdigest()

        return f"{prefix}:{func_name}:{key_hash}"

    def _prepare_for_json(self, obj: Any) -> Any:
        """Prepare an object for JSON serialization.

        Args:
            obj: Object to prepare

        Returns:
            JSON-serializable representation of the object
        """
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        elif hasattr(obj, "dict") and callable(obj.dict):
            return obj.dict()
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, (set, frozenset)):
            return sorted(list(obj))
        elif isinstance(obj, bytes):
            return obj.decode("utf-8", errors="ignore")
        elif inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isclass(obj):
            return f"{obj.__module__}.{obj.__qualname__}"
        elif isinstance(obj, Request):
            # For FastAPI Request objects, just use the path and query params
            return f"{obj.url.path}?{obj.url.query}"
        return obj

    async def _refresh_cache_entry(
        self,
        func: Callable,
        args: tuple,
        kwargs: dict,
        key: str,
        ttl: int,
        backend: Optional[str],
        tags: Optional[List[str]]
    ) -> None:
        """Refresh a cache entry asynchronously.

        Args:
            func: Function to call
            args: Function arguments
            kwargs: Function keyword arguments
            key: Cache key
            ttl: Time-to-live in seconds
            backend: Optional backend name
            tags: Optional list of tags
        """
        try:
            self.logger.debug(f"Asynchronously refreshing cache for key: {key}")

            # Execute function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Store in cache
            if result is not None:
                await self.set(key, result, ttl, backend, tags)
        except Exception as e:
            self.logger.error(f"Error refreshing cache: {str(e)}", key=key)
