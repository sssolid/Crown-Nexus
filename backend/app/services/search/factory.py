# /app/services/search/factory.py
from __future__ import annotations

"""Factory for creating search providers.

This module provides a factory for creating different search provider instances
based on model type and configuration.
"""

from typing import Any, Dict, Optional, Type, cast

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from app.core.config import settings
from app.core.logging import get_logger
from app.models.product import Fitment, Product
from app.services.search.base import SearchProvider
from app.services.search.providers import (
    DatabaseSearchProvider,
    ElasticsearchSearchProvider
)

logger = get_logger("app.services.search.factory")


class SearchProviderFactory:
    """Factory for creating search provider instances."""

    # Cache of already-created providers
    _provider_cache: Dict[str, SearchProvider] = {}

    @classmethod
    async def create_provider(
        cls,
        provider_type: str,
        db: AsyncSession,
        model_class: Type[DeclarativeMeta],
        **kwargs: Any
    ) -> SearchProvider:
        """Create a search provider of the specified type.

        Args:
            provider_type: The type of provider to create ('database', 'elasticsearch')
            db: Database session
            model_class: SQLAlchemy model class to search
            **kwargs: Additional provider configuration

        Returns:
            SearchProvider: The created provider

        Raises:
            ValueError: If provider type is unsupported
        """
        # Generate a cache key
        cache_key = f"{provider_type}:{model_class.__name__}"

        # Check if provider is already cached
        if cache_key in cls._provider_cache:
            return cls._provider_cache[cache_key]

        # Create new provider based on type
        provider: Optional[SearchProvider] = None

        if provider_type == "database":
            provider = DatabaseSearchProvider(db, model_class)
        elif provider_type == "elasticsearch":
            provider = ElasticsearchSearchProvider(db, model_class, **kwargs)
        else:
            raise ValueError(f"Unsupported search provider type: {provider_type}")

        # Initialize the provider
        await provider.initialize()

        # Cache the provider
        cls._provider_cache[cache_key] = provider

        logger.debug(f"Created search provider: {provider_type} for {model_class.__name__}")
        return provider

    @classmethod
    async def create_default_provider(
        cls,
        db: AsyncSession,
        model_class: Type[DeclarativeMeta]
    ) -> SearchProvider:
        """Create the default search provider for a model.

        Args:
            db: Database session
            model_class: SQLAlchemy model class to search

        Returns:
            SearchProvider: The default provider for the model
        """
        # Use elasticsearch for Product and Fitment if available
        if model_class in [Product, Fitment] and settings.ELASTICSEARCH_HOST:
            try:
                return await cls.create_provider("elasticsearch", db, model_class)
            except Exception as e:
                logger.warning(
                    f"Failed to create Elasticsearch provider, falling back to database: {str(e)}"
                )

        # Default to database provider
        return await cls.create_provider("database", db, model_class)

    @classmethod
    async def shutdown_all(cls) -> None:
        """Shutdown all cached providers."""
        for key, provider in cls._provider_cache.items():
            try:
                await provider.shutdown()
                logger.debug(f"Shutdown search provider: {key}")
            except Exception as e:
                logger.error(f"Error shutting down search provider {key}: {str(e)}")

        cls._provider_cache.clear()
