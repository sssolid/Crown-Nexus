from __future__ import annotations
from app.core.cache.decorators import cached
'Main search service implementation.\n\nThis module provides the primary SearchService that coordinates search\noperations across different backends and entity types.\n'
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import get_dependency
from app.core.exceptions import DatabaseException, ErrorCode
from app.logging import get_logger
from app.domains.products.models import Fitment, Product
from app.services.interfaces import ServiceInterface
from app.services.search.factory import SearchProviderFactory
logger = get_logger('app.services.search.service')
class SearchService(ServiceInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.logger = logger
    async def initialize(self) -> None:
        self.logger.debug('Initializing search service')
    async def shutdown(self) -> None:
        self.logger.debug('Shutting down search service')
        await SearchProviderFactory.shutdown_all()
    @cached(prefix='search:products', ttl=300, backend='redis')
    async def search_products(self, search_term: Optional[str]=None, attributes: Optional[Dict[str, Any]]=None, is_active: Optional[bool]=None, page: int=1, page_size: int=20, use_elasticsearch: bool=True) -> Dict[str, Any]:
        try:
            filters: Dict[str, Any] = {}
            if attributes:
                filters['attributes'] = attributes
            if is_active is not None:
                filters['is_active'] = is_active
            provider_type = 'elasticsearch' if use_elasticsearch and search_term else 'database'
            try:
                provider = await SearchProviderFactory.create_provider(provider_type, self.db, Product)
                results = await provider.search(search_term=search_term, filters=filters, page=page, page_size=page_size)
                self.logger.info(f'{provider_type.capitalize()} search successful', provider=provider_type, search_term=search_term, results_count=len(results.get('items', [])), total=results.get('total', 0))
                return results
            except Exception as e:
                if provider_type == 'elasticsearch' and (not isinstance(e, DatabaseException)):
                    self.logger.warning('Elasticsearch search failed, falling back to database', error=str(e), search_term=search_term)
                    provider = await SearchProviderFactory.create_provider('database', self.db, Product)
                    results = await provider.search(search_term=search_term, filters=filters, page=page, page_size=page_size)
                    self.logger.info('Database fallback search successful', search_term=search_term, results_count=len(results.get('items', [])), total=results.get('total', 0))
                    return results
                raise
        except Exception as e:
            self.logger.error('Search operation failed', search_term=search_term, provider_type=provider_type, error=str(e), exc_info=True)
            if isinstance(e, DatabaseException):
                raise
            raise DatabaseException(message='Failed to search products', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
    @cached(prefix='search:fitments', ttl=300, backend='redis')
    async def search_fitments(self, search_term: Optional[str]=None, year: Optional[int]=None, make: Optional[str]=None, model: Optional[str]=None, engine: Optional[str]=None, transmission: Optional[str]=None, page: int=1, page_size: int=20, use_elasticsearch: bool=True) -> Dict[str, Any]:
        try:
            filters: Dict[str, Any] = {}
            if year is not None:
                filters['year'] = year
            if make:
                filters['make'] = make.lower()
            if model:
                filters['model'] = model.lower()
            if engine:
                filters['engine'] = engine.lower()
            if transmission:
                filters['transmission'] = transmission.lower()
            provider_type = 'elasticsearch' if use_elasticsearch and search_term else 'database'
            try:
                provider = await SearchProviderFactory.create_provider(provider_type, self.db, Fitment)
                results = await provider.search(search_term=search_term, filters=filters, page=page, page_size=page_size)
                self.logger.info(f'{provider_type.capitalize()} search successful', provider=provider_type, search_term=search_term, results_count=len(results.get('items', [])), total=results.get('total', 0))
                return results
            except Exception as e:
                if provider_type == 'elasticsearch' and (not isinstance(e, DatabaseException)):
                    self.logger.warning('Elasticsearch search failed, falling back to database', error=str(e), search_term=search_term)
                    provider = await SearchProviderFactory.create_provider('database', self.db, Fitment)
                    results = await provider.search(search_term=search_term, filters=filters, page=page, page_size=page_size)
                    self.logger.info('Database fallback search successful', search_term=search_term, results_count=len(results.get('items', [])), total=results.get('total', 0))
                    return results
                raise
        except Exception as e:
            self.logger.error('Search operation failed', search_term=search_term, provider_type=provider_type, error=str(e), exc_info=True)
            if isinstance(e, DatabaseException):
                raise
            raise DatabaseException(message='Failed to search fitments', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
    async def global_search(self, search_term: str, entity_types: Optional[List[str]]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        if not entity_types:
            entity_types = ['products', 'fitments', 'categories']
        results: Dict[str, Any] = {}
        try:
            error_service = None
            try:
                error_service = get_dependency('error_service')
            except Exception:
                pass
            if 'products' in entity_types:
                try:
                    product_results = await self.search_products(search_term=search_term, page=page, page_size=page_size)
                    results['products'] = product_results
                except Exception as e:
                    self.logger.warning('Product search failed during global search', error=str(e))
                    if error_service:
                        error_service.handle_exception(e, request_id=getattr(self.db, 'request_id', None))
            if 'fitments' in entity_types:
                try:
                    fitment_results = await self.search_fitments(search_term=search_term, page=page, page_size=page_size)
                    results['fitments'] = fitment_results
                except Exception as e:
                    self.logger.warning('Fitment search failed during global search', error=str(e))
                    if error_service:
                        error_service.handle_exception(e, request_id=getattr(self.db, 'request_id', None))
            self.logger.info('Global search completed', search_term=search_term, entity_types=entity_types, results_counts={k: len(v.get('items', [])) for k, v in results.items()})
            return results
        except Exception as e:
            self.logger.error('Global search failed', search_term=search_term, entity_types=entity_types, error=str(e), exc_info=True)
            if not results:
                raise DatabaseException(message='Failed to perform global search', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
            return results