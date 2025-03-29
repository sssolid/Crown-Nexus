from __future__ import annotations
'\nPagination service implementation.\n\nThis module provides a service wrapper around the pagination system,\nmaking it available through the dependency manager.\n'
from typing import Any, Callable, Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.core.pagination.base import CursorPaginationParams, OffsetPaginationParams, PaginationResult
from app.core.pagination.manager import paginate_with_cursor, paginate_with_offset
from app.logging import get_logger
logger = get_logger('app.core.pagination.service')
T = TypeVar('T')
R = TypeVar('R')
class PaginationService:
    def __init__(self, db: Optional[AsyncSession]=None) -> None:
        self.db = db
        self._initialized = False
    async def initialize(self) -> None:
        if self._initialized:
            logger.debug('Pagination service already initialized')
            return
        logger.info('Initializing pagination service')
        self._initialized = True
    async def shutdown(self) -> None:
        if not self._initialized:
            return
        logger.info('Shutting down pagination service')
        self._initialized = False
    async def paginate_with_offset(self, model_class: Type[DeclarativeMeta], query: Select, params: OffsetPaginationParams, transform_func: Optional[Callable[[Any], Any]]=None, response_model: Optional[Type[Any]]=None, db: Optional[AsyncSession]=None) -> PaginationResult[Any]:
        session = db or self.db
        if session is None:
            logger.error('No database session provided for offset pagination')
            raise ValueError('Database session is required for pagination operations')
        logger.debug(f'Offset pagination requested for {model_class.__name__}', extra={'page': params.page, 'page_size': params.page_size})
        return await paginate_with_offset(db=session, model_class=model_class, query=query, params=params, transform_func=transform_func, response_model=response_model)
    async def paginate_with_cursor(self, model_class: Type[DeclarativeMeta], query: Select, params: CursorPaginationParams, transform_func: Optional[Callable[[Any], Any]]=None, response_model: Optional[Type[Any]]=None, db: Optional[AsyncSession]=None) -> PaginationResult[Any]:
        session = db or self.db
        if session is None:
            logger.error('No database session provided for cursor pagination')
            raise ValueError('Database session is required for pagination operations')
        logger.debug(f'Cursor pagination requested for {model_class.__name__}', extra={'cursor': bool(params.cursor), 'limit': params.limit})
        return await paginate_with_cursor(db=session, model_class=model_class, query=query, params=params, transform_func=transform_func, response_model=response_model)
_pagination_service: Optional[PaginationService] = None
def get_pagination_service(db: Optional[AsyncSession]=None) -> PaginationService:
    global _pagination_service
    if _pagination_service is None:
        _pagination_service = PaginationService(db)
    if db is not None:
        _pagination_service.db = db
    return _pagination_service