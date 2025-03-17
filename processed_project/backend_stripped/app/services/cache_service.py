from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, TypeVar
from app.core.cache.decorators import cache_aside, cached, invalidate_cache, memoize
from app.core.cache.keys import generate_cache_key, generate_list_key, generate_model_key, generate_query_key
from app.core.cache.manager import cache_manager
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
T = TypeVar('T')
logger = get_logger('app.services.cache_service')
class CacheService:
    def __init__(self) -> None:
        self.logger = logger
    async def initialize(self) -> None:
        self.logger.debug('Initializing cache service')
    async def shutdown(self) -> None:
        self.logger.debug('Shutting down cache service')
    async def get_model(self, model_name: str, model_id: str, backend: Optional[str]=None) -> Optional[Dict[str, Any]]:
        key = generate_model_key('model', model_name, model_id)
        return await cache_manager.get(key, backend)
    async def set_model(self, model_name: str, model_id: str, data: Dict[str, Any], ttl: Optional[int]=None, backend: Optional[str]=None) -> bool:
        key = generate_model_key('model', model_name, model_id)
        return await cache_manager.set(key, data, ttl, backend)
    async def invalidate_model(self, model_name: str, model_id: str, backend: Optional[str]=None) -> bool:
        key = generate_model_key('model', model_name, model_id)
        return await cache_manager.delete(key, backend)
    async def get_model_list(self, model_name: str, filters: Optional[Dict[str, Any]]=None, backend: Optional[str]=None) -> Optional[List[Dict[str, Any]]]:
        key = generate_list_key('list', model_name, filters)
        return await cache_manager.get(key, backend)
    async def set_model_list(self, model_name: str, data: List[Dict[str, Any]], filters: Optional[Dict[str, Any]]=None, ttl: Optional[int]=None, backend: Optional[str]=None) -> bool:
        key = generate_list_key('list', model_name, filters)
        return await cache_manager.set(key, data, ttl, backend)
    async def invalidate_model_list(self, model_name: str, backend: Optional[str]=None) -> int:
        pattern = f'list:{model_name}:*'
        return await cache_manager.invalidate_pattern(pattern, backend)
    async def get_query(self, query_name: str, params: Optional[Dict[str, Any]]=None, backend: Optional[str]=None) -> Optional[Any]:
        key = generate_query_key('query', query_name, params)
        return await cache_manager.get(key, backend)
    async def set_query(self, query_name: str, data: Any, params: Optional[Dict[str, Any]]=None, ttl: Optional[int]=None, backend: Optional[str]=None) -> bool:
        key = generate_query_key('query', query_name, params)
        return await cache_manager.set(key, data, ttl, backend)
    async def invalidate_query(self, query_name: str, backend: Optional[str]=None) -> int:
        pattern = f'query:{query_name}:*'
        return await cache_manager.invalidate_pattern(pattern, backend)
    async def get_or_set(self, key: str, default_factory: callable, ttl: Optional[int]=None, backend: Optional[str]=None) -> Any:
        return await cache_manager.get_or_set(key, default_factory, ttl, backend)
    async def get_or_set_async(self, key: str, default_factory: callable, ttl: Optional[int]=None, backend: Optional[str]=None) -> Any:
        return await cache_manager.get_or_set_async(key, default_factory, ttl, backend)