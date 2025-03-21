from __future__ import annotations
'Core pagination functionality.\n\nThis module provides the main functions for paginating query results using\nboth offset-based and cursor-based pagination strategies.\n'
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union, cast
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.core.pagination.base import CursorPaginationParams, OffsetPaginationParams, PaginationProvider, PaginationResult
from app.core.pagination.factory import PaginationProviderFactory
from app.core.pagination.providers import CursorPaginationProvider, OffsetPaginationProvider
logger = get_logger(__name__)
T = TypeVar('T')
R = TypeVar('R')
PaginationProviderFactory._providers = {'offset': OffsetPaginationProvider, 'cursor': CursorPaginationProvider}
async def initialize() -> None:
    logger.info('Initializing pagination system')
async def shutdown() -> None:
    logger.info('Shutting down pagination system')
    PaginationProviderFactory.clear_cache()
async def paginate_with_offset(db: AsyncSession, model_class: Type[DeclarativeMeta], query: Select, params: OffsetPaginationParams, transform_func: Optional[Callable[[Any], Any]]=None, response_model: Optional[Type[Any]]=None) -> PaginationResult[Any]:
    try:
        provider = PaginationProviderFactory.create_provider('offset', db, model_class, response_model)
        transform = transform_func
        if transform is None and response_model is not None:
            transform = _create_default_transform_func(response_model)
        result = await provider.paginate_with_offset(query, params, transform)
        logger.debug(f'Offset pagination for {model_class.__name__} completed', extra={'page': params.page, 'page_size': params.page_size, 'total': result.total, 'items_count': len(result.items)})
        return result
    except Exception as e:
        if isinstance(e, ValidationException):
            raise
        logger.error(f'Offset pagination failed: {str(e)}', exc_info=True, extra={'model': model_class.__name__, 'params': params.model_dump()})
        raise ValidationException(message=f'Pagination failed: {str(e)}', details=[{'loc': ['pagination'], 'msg': str(e), 'type': 'pagination_error'}])
async def paginate_with_cursor(db: AsyncSession, model_class: Type[DeclarativeMeta], query: Select, params: CursorPaginationParams, transform_func: Optional[Callable[[Any], Any]]=None, response_model: Optional[Type[Any]]=None) -> PaginationResult[Any]:
    try:
        provider = PaginationProviderFactory.create_provider('cursor', db, model_class, response_model)
        transform = transform_func
        if transform is None and response_model is not None:
            transform = _create_default_transform_func(response_model)
        result = await provider.paginate_with_cursor(query, params, transform)
        logger.debug(f'Cursor pagination for {model_class.__name__} completed', extra={'cursor': bool(params.cursor), 'limit': params.limit, 'total': result.total, 'items_count': len(result.items), 'has_next': result.has_next})
        return result
    except Exception as e:
        if isinstance(e, ValidationException):
            raise
        logger.error(f'Cursor pagination failed: {str(e)}', exc_info=True, extra={'model': model_class.__name__, 'params': params.model_dump()})
        raise ValidationException(message=f'Pagination failed: {str(e)}', details=[{'loc': ['pagination'], 'msg': str(e), 'type': 'pagination_error'}])
def _create_default_transform_func(response_model: Type[Any]) -> Callable[[Any], Any]:
    if response_model is None:
        raise ValueError('Response model is required for default transform function')
    def transform(item: Any) -> Any:
        if hasattr(response_model, 'from_orm'):
            return response_model.from_orm(item)
        else:
            return response_model(**item.__dict__)
    return transform