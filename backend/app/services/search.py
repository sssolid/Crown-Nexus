"""
Search service for products and fitments.

This module provides search functionality for products and fitments,
with optional Elasticsearch integration for advanced text search.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings
from app.core.dependency_manager import get_dependency
from app.core.exceptions import (
    DatabaseException,
    ErrorCode,
    ExternalServiceException
)
from app.core.logging import get_logger
from app.models.product import Fitment, Product
from app.utils.cache import redis_cache
from app.utils.db import paginate
from app.utils.retry import async_retry_on_network_errors

logger = get_logger('app.services.search')

class SearchService:
    """Service for searching products and fitments."""

    def __init__(self, db: AsyncSession):
        """Initialize the search service.

        Args:
            db: Database session for database operations.
        """
        self.db = db
        self.es_client: Optional[AsyncElasticsearch] = None

    async def get_es_client(self) -> Optional[AsyncElasticsearch]:
        """Get or create an Elasticsearch client.

        Returns:
            AsyncElasticsearch client, or None if Elasticsearch is not configured.
        """
        if self.es_client is None and settings.ELASTICSEARCH_HOST:
            try:
                self.es_client = AsyncElasticsearch(
                    [f'{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}']
                )
                logger.info(
                    "Connected to Elasticsearch",
                    host=settings.ELASTICSEARCH_HOST,
                    port=settings.ELASTICSEARCH_PORT
                )
            except Exception as e:
                logger.error(
                    "Failed to connect to Elasticsearch",
                    host=settings.ELASTICSEARCH_HOST,
                    port=settings.ELASTICSEARCH_PORT,
                    error=str(e),
                    exc_info=True
                )
                # Don't raise - we'll fall back to database search
        return self.es_client

    @redis_cache(prefix='search:products', ttl=300)
    async def search_products(
        self,
        search_term: Optional[str]=None,
        attributes: Optional[Dict[str, Any]]=None,
        is_active: Optional[bool]=None,
        page: int=1,
        page_size: int=20,
        use_elasticsearch: bool=True
    ) -> Dict[str, Any]:
        """Search for products matching the given criteria.

        Args:
            search_term: Text to search for in product name, description, etc.
            attributes: Product attributes to filter by.
            is_active: Filter by active status.
            page: Page number for pagination.
            page_size: Items per page.
            use_elasticsearch: Whether to use Elasticsearch or database search.

        Returns:
            Dict containing search results and pagination info.

        Raises:
            DatabaseException: If the database search fails.
        """
        if use_elasticsearch and search_term:
            es_client = await self.get_es_client()
            if es_client:
                try:
                    results = await self._search_products_elasticsearch(
                        es_client, search_term, attributes, is_active, page, page_size
                    )
                    logger.info(
                        "Elasticsearch search successful",
                        search_term=search_term,
                        results_count=len(results.get('items', [])),
                        total=results.get('total', 0)
                    )
                    return results
                except Exception as e:
                    logger.warning(
                        "Elasticsearch search failed, falling back to database",
                        error=str(e),
                        search_term=search_term
                    )
                    # Fall back to database search

        try:
            results = await self._search_products_database(
                search_term, attributes, is_active, page, page_size
            )
            logger.info(
                "Database search successful",
                search_term=search_term,
                results_count=len(results.get('items', [])),
                total=results.get('total', 0)
            )
            return results
        except SQLAlchemyError as e:
            logger.error(
                "Database search failed",
                search_term=search_term,
                error=str(e),
                exc_info=True
            )
            raise DatabaseException(
                message="Failed to search products",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e
            ) from e

    async def _search_products_database(
        self,
        search_term: Optional[str]=None,
        attributes: Optional[Dict[str, Any]]=None,
        is_active: Optional[bool]=None,
        page: int=1,
        page_size: int=20
    ) -> Dict[str, Any]:
        """Search for products in the database.

        Args:
            search_term: Text to search for in product name, description, etc.
            attributes: Product attributes to filter by.
            is_active: Filter by active status.
            page: Page number for pagination.
            page_size: Items per page.

        Returns:
            Dict containing search results and pagination info.

        Raises:
            DatabaseException: If the database query fails.
        """
        try:
            query = select(Product)

            if search_term:
                search_pattern = f'%{search_term.lower()}%'
                query = query.where(or_(
                    func.lower(Product.name).like(search_pattern),
                    func.lower(Product.description).like(search_pattern),
                    func.lower(Product.sku).like(search_pattern),
                    func.lower(Product.part_number).like(search_pattern)
                ))

            if is_active is not None:
                query = query.where(Product.is_active == is_active)

            if attributes:
                for key, value in attributes.items():
                    query = query.where(Product.attributes.contains({key: value}))

            logger.debug(
                "Database search query built",
                search_term=search_term,
                is_active=is_active,
                attributes=attributes
            )

            return await paginate(self.db, query, page, page_size)

        except SQLAlchemyError as e:
            logger.error(
                "Database search query failed",
                search_term=search_term,
                error=str(e),
                exc_info=True
            )
            raise DatabaseException(
                message="Failed to search products in database",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e
            ) from e

    @async_retry_on_network_errors(retries=2, delay=0.5)
    async def _search_products_elasticsearch(
        self,
        es_client: AsyncElasticsearch,
        search_term: str,
        attributes: Optional[Dict[str, Any]]=None,
        is_active: Optional[bool]=None,
        page: int=1,
        page_size: int=20
    ) -> Dict[str, Any]:
        """Search for products using Elasticsearch.

        Args:
            es_client: Elasticsearch client.
            search_term: Text to search for.
            attributes: Product attributes to filter by.
            is_active: Filter by active status.
            page: Page number for pagination.
            page_size: Items per page.

        Returns:
            Dict containing search results and pagination info.

        Raises:
            ExternalServiceException: If the Elasticsearch query fails.
            DatabaseException: If fetching products from database after ES search fails.
        """
        try:
            from_index = (page - 1) * page_size
            query = {
                'query': {
                    'bool': {
                        'must': [{
                            'multi_match': {
                                'query': search_term,
                                'fields': ['name^3', 'description', 'sku^2', 'part_number^2'],
                                'type': 'best_fields',
                                'fuzziness': 'AUTO'
                            }
                        }],
                        'filter': []
                    }
                },
                'from': from_index,
                'size': page_size,
                'highlight': {
                    'fields': {
                        'name': {},
                        'description': {}
                    }
                }
            }

            if is_active is not None:
                query['query']['bool']['filter'].append({'term': {'is_active': is_active}})

            if attributes:
                for key, value in attributes.items():
                    query['query']['bool']['filter'].append({'term': {f'attributes.{key}': value}})

            logger.debug(
                "Elasticsearch query built",
                search_term=search_term,
                is_active=is_active,
                attributes=attributes,
                query=json.dumps(query)
            )

            result = await es_client.search(index='products', body=query)
            hits = result['hits']['hits']
            total = result['hits']['total']['value']

            logger.debug(
                "Elasticsearch search results",
                hits_count=len(hits),
                total=total
            )

            # Fetch actual product objects from database using IDs from ES
            product_ids = [hit['_id'] for hit in hits]
            products = []

            if product_ids:
                try:
                    query = select(Product).where(Product.id.in_(product_ids))
                    result = await self.db.execute(query)
                    db_products = {str(p.id): p for p in result.scalars().all()}
                    products = [db_products[pid] for pid in product_ids if pid in db_products]

                    logger.debug(
                        "Retrieved products from database after ES search",
                        product_count=len(products),
                        found_ids=len(db_products),
                        total_ids=len(product_ids)
                    )

                except SQLAlchemyError as e:
                    logger.error(
                        "Failed to fetch products from database after ES search",
                        error=str(e),
                        product_ids=product_ids,
                        exc_info=True
                    )
                    raise DatabaseException(
                        message="Failed to fetch products after Elasticsearch search",
                        code=ErrorCode.DATABASE_ERROR,
                        original_exception=e
                    ) from e

            pages = (total + page_size - 1) // page_size if page_size > 0 else 0
            return {
                'items': products,
                'total': total,
                'page': page,
                'page_size': page_size,
                'pages': pages
            }

        except Exception as e:
            if isinstance(e, DatabaseException):
                raise

            logger.error(
                "Elasticsearch search failed",
                search_term=search_term,
                error=str(e),
                exc_info=True
            )
            raise ExternalServiceException(
                message="Failed to search products in Elasticsearch",
                code=ErrorCode.EXTERNAL_SERVICE_ERROR,
                details={"service": "elasticsearch"},
                original_exception=e
            ) from e

    @redis_cache(prefix='search:fitments', ttl=300)
    async def search_fitments(
        self,
        search_term: Optional[str]=None,
        year: Optional[int]=None,
        make: Optional[str]=None,
        model: Optional[str]=None,
        engine: Optional[str]=None,
        transmission: Optional[str]=None,
        page: int=1,
        page_size: int=20
    ) -> Dict[str, Any]:
        """Search for fitments matching the given criteria.

        Args:
            search_term: Text to search for.
            year: Filter by year.
            make: Filter by make.
            model: Filter by model.
            engine: Filter by engine.
            transmission: Filter by transmission.
            page: Page number for pagination.
            page_size: Items per page.

        Returns:
            Dict containing search results and pagination info.

        Raises:
            DatabaseException: If the database query fails.
        """
        try:
            query = select(Fitment)

            if search_term:
                search_pattern = f'%{search_term.lower()}%'
                query = query.where(or_(
                    func.lower(Fitment.make).like(search_pattern),
                    func.lower(Fitment.model).like(search_pattern),
                    func.lower(Fitment.engine).like(search_pattern),
                    func.lower(Fitment.transmission).like(search_pattern)
                ))

            if year is not None:
                query = query.where(Fitment.year == year)

            if make:
                query = query.where(func.lower(Fitment.make) == make.lower())

            if model:
                query = query.where(func.lower(Fitment.model) == model.lower())

            if engine:
                query = query.where(func.lower(Fitment.engine) == engine.lower())

            if transmission:
                query = query.where(func.lower(Fitment.transmission) == transmission.lower())

            logger.debug(
                "Fitment search query built",
                search_term=search_term,
                year=year,
                make=make,
                model=model
            )

            result = await paginate(self.db, query, page, page_size)
            logger.info(
                "Fitment search successful",
                results_count=len(result.get('items', [])),
                total=result.get('total', 0)
            )

            return result

        except SQLAlchemyError as e:
            logger.error(
                "Fitment search failed",
                search_term=search_term,
                year=year,
                make=make,
                model=model,
                error=str(e),
                exc_info=True
            )
            raise DatabaseException(
                message="Failed to search fitments",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e
            ) from e

    async def global_search(
        self,
        search_term: str,
        entity_types: Optional[List[str]]=None,
        page: int=1,
        page_size: int=20
    ) -> Dict[str, Any]:
        """Search across multiple entity types.

        Args:
            search_term: Text to search for.
            entity_types: Types of entities to search.
            page: Page number for pagination.
            page_size: Items per page.

        Returns:
            Dict containing search results for each entity type.
        """
        if not entity_types:
            entity_types = ['products', 'fitments', 'categories']

        results = {}

        try:
            # Use error handling service if available
            error_service = None
            try:
                error_service = get_dependency('error_handling_service')
            except Exception:
                pass

            if 'products' in entity_types:
                try:
                    product_results = await self.search_products(
                        search_term=search_term,
                        page=page,
                        page_size=page_size
                    )
                    results['products'] = product_results
                except Exception as e:
                    logger.warning(
                        "Product search failed during global search",
                        error=str(e)
                    )
                    if error_service:
                        error_service.log_error("Product search failed during global search", e)
                    # Continue with other entity types

            if 'fitments' in entity_types:
                try:
                    fitment_results = await self.search_fitments(
                        search_term=search_term,
                        page=page,
                        page_size=page_size
                    )
                    results['fitments'] = fitment_results
                except Exception as e:
                    logger.warning(
                        "Fitment search failed during global search",
                        error=str(e)
                    )
                    if error_service:
                        error_service.log_error("Fitment search failed during global search", e)
                    # Continue with other entity types

            # Future: add other entity types here

            logger.info(
                "Global search completed",
                search_term=search_term,
                entity_types=entity_types,
                results_counts={k: len(v.get('items', [])) for k, v in results.items()}
            )

            return results

        except Exception as e:
            logger.error(
                "Global search failed",
                search_term=search_term,
                entity_types=entity_types,
                error=str(e),
                exc_info=True
            )
            # Return partial results if any
            if not results:
                raise DatabaseException(
                    message="Failed to perform global search",
                    code=ErrorCode.DATABASE_ERROR,
                    original_exception=e
                ) from e
            return results

    @classmethod
    def register(cls) -> None:
        """Register this service with the service registry."""
        from app.services import service_registry
        service_registry.register(cls, 'search_service')

async def get_search_service(db: AsyncSession=Depends(get_db)) -> SearchService:
    """Dependency for getting the search service.

    Args:
        db: Database session.

    Returns:
        SearchService instance.
    """
    try:
        # Try to get from dependency manager first
        from app.core.dependency_manager import get_dependency
        service = get_dependency('search_service', db=db)
        if service:
            return service
    except Exception:
        # Fall back to direct instantiation
        pass

    return SearchService(db)

# Register the service
SearchService.register()
