# /app/core/pagination/factory.py
from __future__ import annotations

"""Factory for creating pagination providers.

This module provides a factory for creating different pagination provider instances
based on pagination type and configuration.
"""

from typing import Any, Dict, Generic, Optional, Type, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from app.core.logging import get_logger
from app.core.pagination.base import PaginationProvider

logger = get_logger(__name__)

T = TypeVar("T")  # Entity type
R = TypeVar("R")  # Result type


class PaginationProviderFactory(Generic[T, R]):
    """Factory for creating pagination provider instances."""

    # Registry of provider types to their classes
    _providers: Dict[str, Type[PaginationProvider]] = {}

    # Cache of already-created providers
    _provider_cache: Dict[str, PaginationProvider] = {}

    @classmethod
    def register_provider(
        cls, name: str, provider_class: Type[PaginationProvider]
    ) -> None:
        """Register a new pagination provider type.

        Args:
            name: Provider type name
            provider_class: Provider class

        Raises:
            ValueError: If a provider with the same name is already registered
        """
        if name in cls._providers:
            raise ValueError(f"Pagination provider '{name}' is already registered")

        cls._providers[name] = provider_class
        logger.debug(f"Registered pagination provider type: {name}")

    @classmethod
    def create_provider(
        cls,
        provider_type: str,
        db: AsyncSession,
        model_class: Type[DeclarativeMeta],
        response_model: Optional[Type[Any]] = None,
        **kwargs: Any,
    ) -> PaginationProvider[T, R]:
        """Create a pagination provider of the specified type.

        Args:
            provider_type: The type of provider to create ('offset', 'cursor')
            db: Database session
            model_class: SQLAlchemy model class
            response_model: Response model type (for generic type inference)
            **kwargs: Additional provider configuration

        Returns:
            PaginationProvider: The created provider

        Raises:
            ValueError: If the provider type is not supported
        """
        # Generate a cache key
        cache_key = f"{provider_type}:{model_class.__name__}"

        # Check if provider is already cached
        if cache_key in cls._provider_cache:
            return cast(PaginationProvider[T, R], cls._provider_cache[cache_key])

        # Create new provider based on type
        if provider_type not in cls._providers:
            raise ValueError(
                f"Unsupported pagination provider type: {provider_type}. "
                f"Supported types: {', '.join(cls._providers.keys())}"
            )

        provider_class = cls._providers[provider_type]

        # Create the provider
        provider = provider_class(db, model_class)

        # Cache the provider
        cls._provider_cache[cache_key] = provider

        logger.debug(
            f"Created pagination provider: {provider_type} for {model_class.__name__}"
        )
        return cast(PaginationProvider[T, R], provider)

    @classmethod
    def clear_cache(cls) -> None:
        """Clear provider cache."""
        cls._provider_cache.clear()
        logger.debug("Cleared pagination provider cache")
