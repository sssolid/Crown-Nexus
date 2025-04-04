from __future__ import annotations
'\nFactory for creating pagination providers.\n\nThis module provides a factory for creating different pagination provider instances\nbased on pagination type and configuration.\n'
from typing import Any, Dict, Generic, Optional, Type, TypeVar, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.logging import get_logger
from app.core.pagination.base import PaginationProvider
logger = get_logger('app.core.pagination.factory')
T = TypeVar('T')
R = TypeVar('R')
class PaginationProviderFactory(Generic[T, R]):
    _providers: Dict[str, Type[PaginationProvider]] = {}
    _provider_cache: Dict[str, PaginationProvider] = {}
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[PaginationProvider]) -> None:
        if name in cls._providers:
            raise ValueError(f"Pagination provider '{name}' is already registered")
        cls._providers[name] = provider_class
        logger.debug(f'Registered pagination provider type: {name}')
    @classmethod
    def create_provider(cls, provider_type: str, db: AsyncSession, model_class: Type[DeclarativeMeta], response_model: Optional[Type[Any]]=None, **kwargs: Any) -> PaginationProvider[T, R]:
        cache_key = f'{provider_type}:{model_class.__name__}'
        if cache_key in cls._provider_cache:
            return cast(PaginationProvider[T, R], cls._provider_cache[cache_key])
        if provider_type not in cls._providers:
            raise ValueError(f"Unsupported pagination provider type: {provider_type}. Supported types: {', '.join(cls._providers.keys())}")
        provider_class = cls._providers[provider_type]
        provider = provider_class(db, model_class)
        cls._provider_cache[cache_key] = provider
        logger.debug(f'Created pagination provider: {provider_type} for {model_class.__name__}')
        return cast(PaginationProvider[T, R], provider)
    @classmethod
    def clear_cache(cls) -> None:
        cls._provider_cache.clear()
        logger.debug('Cleared pagination provider cache')