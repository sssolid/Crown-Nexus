from __future__ import annotations
'Factory for creating search providers.\n\nThis module provides a factory for creating different search provider instances\nbased on model type and configuration.\n'
from typing import Any, Dict, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.core.config import settings
from app.logging import get_logger
from app.domains.products.models import Fitment, Product
from app.services.search.base import SearchProvider
from app.services.search.providers import DatabaseSearchProvider, ElasticsearchSearchProvider
logger = get_logger('app.services.search.factory')
class SearchProviderFactory:
    _provider_cache: Dict[str, SearchProvider] = {}
    @classmethod
    async def create_provider(cls, provider_type: str, db: AsyncSession, model_class: Type[DeclarativeMeta], **kwargs: Any) -> SearchProvider:
        cache_key = f'{provider_type}:{model_class.__name__}'
        if cache_key in cls._provider_cache:
            return cls._provider_cache[cache_key]
        provider: Optional[SearchProvider] = None
        if provider_type == 'database':
            provider = DatabaseSearchProvider(db, model_class)
        elif provider_type == 'elasticsearch':
            provider = ElasticsearchSearchProvider(db, model_class, **kwargs)
        else:
            raise ValueError(f'Unsupported search provider type: {provider_type}')
        await provider.initialize()
        cls._provider_cache[cache_key] = provider
        logger.debug(f'Created search provider: {provider_type} for {model_class.__name__}')
        return provider
    @classmethod
    async def create_default_provider(cls, db: AsyncSession, model_class: Type[DeclarativeMeta]) -> SearchProvider:
        if model_class in [Product, Fitment] and settings.ELASTICSEARCH_HOST:
            try:
                return await cls.create_provider('elasticsearch', db, model_class)
            except Exception as e:
                logger.warning(f'Failed to create Elasticsearch provider, falling back to database: {str(e)}')
        return await cls.create_provider('database', db, model_class)
    @classmethod
    async def shutdown_all(cls) -> None:
        for key, provider in cls._provider_cache.items():
            try:
                await provider.shutdown()
                logger.debug(f'Shutdown search provider: {key}')
            except Exception as e:
                logger.error(f'Error shutting down search provider {key}: {str(e)}')
        cls._provider_cache.clear()