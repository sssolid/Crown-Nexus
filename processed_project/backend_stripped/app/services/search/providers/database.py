from __future__ import annotations
from app.core.pagination import paginate_with_offset, OffsetPaginationParams
'Database search provider implementation.\n\nThis module provides a search provider that queries the database directly.\n'
from typing import Any, Dict, List, Optional, Type, cast
from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.core.exceptions import DatabaseException, ErrorCode
from app.logging import get_logger
from app.domains.products.models import Fitment, Product
from app.services.search.base import SearchProvider, SearchResult
logger = get_logger('app.services.search.providers.database')
class DatabaseSearchProvider(SearchProvider):
    def __init__(self, db: AsyncSession, model_class: Type[DeclarativeMeta]) -> None:
        self.db = db
        self.model_class = model_class
        self.searchable_fields: List[str] = []
        self.logger = logger
    async def initialize(self) -> None:
        if self.model_class == Product:
            self.searchable_fields = ['name', 'description', 'sku', 'part_number']
        elif self.model_class == Fitment:
            self.searchable_fields = ['make', 'model', 'engine', 'transmission']
        else:
            for column_name in getattr(self.model_class, '__table__').columns.keys():
                if any((field in column_name.lower() for field in ['name', 'title', 'description', 'id', 'code'])):
                    self.searchable_fields.append(column_name)
        self.logger.debug(f"Initialized database search for {self.model_class.__name__} with searchable fields: {', '.join(self.searchable_fields)}")
    async def shutdown(self) -> None:
        pass
    async def search(self, search_term: Optional[str]=None, filters: Optional[Dict[str, Any]]=None, page: int=1, page_size: int=20, **kwargs: Any) -> SearchResult:
        try:
            query = select(self.model_class)
            if search_term:
                search_conditions = []
                search_pattern = f'%{search_term.lower()}%'
                for field_name in self.searchable_fields:
                    if hasattr(self.model_class, field_name):
                        column = getattr(self.model_class, field_name)
                        if hasattr(column, 'type') and hasattr(column.type, 'python_type'):
                            if column.type.python_type == str:
                                search_conditions.append(func.lower(column).like(search_pattern))
                if search_conditions:
                    query = query.where(or_(*search_conditions))
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model_class, key):
                        if isinstance(value, dict) and key == 'attributes':
                            for attr_key, attr_value in value.items():
                                query = query.where(getattr(self.model_class, key).contains({attr_key: attr_value}))
                        else:
                            query = query.where(getattr(self.model_class, key) == value)
            if hasattr(self.model_class, 'is_active') and (not (filters and 'is_active' in filters)):
                query = query.where(getattr(self.model_class, 'is_active') == True)
            self.logger.debug('Database search query built', search_term=search_term, filters=filters)
            params = OffsetPaginationParams(page=page, page_size=page_size)
            result = await paginate_with_offset(query, params)
            self.logger.info('Database search successful', search_term=search_term, results_count=len(result.get('items', [])), total=result.get('total', 0))
            return cast(SearchResult, result)
        except SQLAlchemyError as e:
            self.logger.error('Database search query failed', search_term=search_term, error=str(e), exc_info=True)
            raise DatabaseException(message='Failed to search in database', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e