# /backend/app/services/cache_service.py
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, TypeVar

from app.core.cache.decorators import cache_aside, cached, invalidate_cache, memoize
from app.core.cache.keys import (
    generate_cache_key,
    generate_list_key,
    generate_model_key,
    generate_query_key
)
from app.core.cache.manager import cache_manager
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface

T = TypeVar('T')

logger = get_logger("app.services.cache_service")

class CacheService:
    """Service for caching operations.
    
    This service provides a high-level interface for caching operations,
    with support for model caching, query caching, and more.
    """
    
    def __init__(self) -> None:
        """Initialize the cache service."""
        self.logger = logger
        
    async def initialize(self) -> None:
        """Initialize service resources."""
        self.logger.debug("Initializing cache service")
        
    async def shutdown(self) -> None:
        """Release service resources."""
        self.logger.debug("Shutting down cache service")
        
    async def get_model(
        self,
        model_name: str,
        model_id: str,
        backend: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get a model instance from the cache.
        
        Args:
            model_name: Model name
            model_id: Model ID
            backend: Cache backend to use
            
        Returns:
            Optional[Dict[str, Any]]: Cached model instance or None if not found
        """
        key = generate_model_key("model", model_name, model_id)
        return await cache_manager.get(key, backend)
        
    async def set_model(
        self,
        model_name: str,
        model_id: str,
        data: Dict[str, Any],
        ttl: Optional[int] = None,
        backend: Optional[str] = None
    ) -> bool:
        """Set a model instance in the cache.
        
        Args:
            model_name: Model name
            model_id: Model ID
            data: Model data
            ttl: Time-to-live in seconds
            backend: Cache backend to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        key = generate_model_key("model", model_name, model_id)
        return await cache_manager.set(key, data, ttl, backend)
        
    async def invalidate_model(
        self,
        model_name: str,
        model_id: str,
        backend: Optional[str] = None
    ) -> bool:
        """Invalidate a model instance in the cache.
        
        Args:
            model_name: Model name
            model_id: Model ID
            backend: Cache backend to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        key = generate_model_key("model", model_name, model_id)
        return await cache_manager.delete(key, backend)
        
    async def get_model_list(
        self,
        model_name: str,
        filters: Optional[Dict[str, Any]] = None,
        backend: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Get a list of model instances from the cache.
        
        Args:
            model_name: Model name
            filters: Optional filters
            backend: Cache backend to use
            
        Returns:
            Optional[List[Dict[str, Any]]]: Cached list or None if not found
        """
        key = generate_list_key("list", model_name, filters)
        return await cache_manager.get(key, backend)
        
    async def set_model_list(
        self,
        model_name: str,
        data: List[Dict[str, Any]],
        filters: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
        backend: Optional[str] = None
    ) -> bool:
        """Set a list of model instances in the cache.
        
        Args:
            model_name: Model name
            data: List data
            filters: Optional filters
            ttl: Time-to-live in seconds
            backend: Cache backend to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        key = generate_list_key("list", model_name, filters)
        return await cache_manager.set(key, data, ttl, backend)
        
    async def invalidate_model_list(
        self,
        model_name: str,
        backend: Optional[str] = None
    ) -> int:
        """Invalidate all lists of a model in the cache.
        
        Args:
            model_name: Model name
            backend: Cache backend to use
            
        Returns:
            int: Number of keys invalidated
        """
        pattern = f"list:{model_name}:*"
        return await cache_manager.invalidate_pattern(pattern, backend)
        
    async def get_query(
        self,
        query_name: str,
        params: Optional[Dict[str, Any]] = None,
        backend: Optional[str] = None
    ) -> Optional[Any]:
        """Get a query result from the cache.
        
        Args:
            query_name: Query name
            params: Optional query parameters
            backend: Cache backend to use
            
        Returns:
            Optional[Any]: Cached query result or None if not found
        """
        key = generate_query_key("query", query_name, params)
        return await cache_manager.get(key, backend)
        
    async def set_query(
        self,
        query_name: str,
        data: Any,
        params: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
        backend: Optional[str] = None
    ) -> bool:
        """Set a query result in the cache.
        
        Args:
            query_name: Query name
            data: Query result
            params: Optional query parameters
            ttl: Time-to-live in seconds
            backend: Cache backend to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        key = generate_query_key("query", query_name, params)
        return await cache_manager.set(key, data, ttl, backend)
        
    async def invalidate_query(
        self,
        query_name: str,
        backend: Optional[str] = None
    ) -> int:
        """Invalidate all results of a query in the cache.
        
        Args:
            query_name: Query name
            backend: Cache backend to use
            
        Returns:
            int: Number of keys invalidated
        """
        pattern = f"query:{query_name}:*"
        return await cache_manager.invalidate_pattern(pattern, backend)
        
    async def get_or_set(
        self,
        key: str,
        default_factory: callable,
        ttl: Optional[int] = None,
        backend: Optional[str] = None
    ) -> Any:
        """Get a value from the cache or set it if not found.
        
        Args:
            key: Cache key
            default_factory: Function to call to get default value
            ttl: Time-to-live in seconds
            backend: Cache backend to use
            
        Returns:
            Any: Cached value or default value
        """
        return await cache_manager.get_or_set(key, default_factory, ttl, backend)
        
    async def get_or_set_async(
        self,
        key: str,
        default_factory: callable,
        ttl: Optional[int] = None,
        backend: Optional[str] = None
    ) -> Any:
        """Get a value from the cache or set it if not found (async version).
        
        Args:
            key: Cache key
            default_factory: Async function to call to get default value
            ttl: Time-to-live in seconds
            backend: Cache backend to use
            
        Returns:
            Any: Cached value or default value
        """
        return await cache_manager.get_or_set_async(key, default_factory, ttl, backend)
