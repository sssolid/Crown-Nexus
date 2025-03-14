# backend/app/services/search.py
"""
Search service.

This module provides search functionality for the application:
- Text search for products and fitments
- Faceted search and filtering
- Search result highlighting
- Elasticsearch integration

The search service improves user experience by providing fast
and relevant search results across all application data.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings
from app.models.product import Fitment, Product
from app.utils.db import paginate


class SearchService:
    """
    Service for search functionality.

    This service provides methods for searching across different
    entities in the application, with support for text search,
    filtering, and pagination.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the search service.

        Args:
            db: Database session
        """
        self.db = db
        self.es_client: Optional[AsyncElasticsearch] = None

    async def get_es_client(self) -> Optional[AsyncElasticsearch]:
        """
        Get Elasticsearch client instance.

        Returns:
            Optional[AsyncElasticsearch]: Elasticsearch client or None if not configured
        """
        if self.es_client is None and settings.ELASTICSEARCH_HOST:
            self.es_client = AsyncElasticsearch(
                [f"{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"]
            )
        return self.es_client

    async def search_products(
        self,
        search_term: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
        use_elasticsearch: bool = True,
    ) -> Dict[str, Any]:
        """
        Search for products with filtering and pagination.

        Args:
            search_term: Text to search for
            attributes: Filter by product attributes
            is_active: Filter by active status
            page: Page number
            page_size: Items per page
            use_elasticsearch: Whether to use Elasticsearch (if available)

        Returns:
            Dict[str, Any]: Search results with pagination
        """
        # Try to use Elasticsearch if enabled
        if use_elasticsearch and search_term:
            es_client = await self.get_es_client()
            if es_client:
                try:
                    return await self._search_products_elasticsearch(
                        es_client,
                        search_term,
                        attributes,
                        is_active,
                        page,
                        page_size,
                    )
                except Exception as e:
                    # Log the error and fall back to database search
                    print(f"Elasticsearch error: {e}")

        # Fall back to database search
        return await self._search_products_database(
            search_term,
            attributes,
            is_active,
            page,
            page_size,
        )

    async def _search_products_database(
        self,
        search_term: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        Search for products using database queries.

        Args:
            search_term: Text to search for
            attributes: Filter by product attributes
            is_active: Filter by active status
            page: Page number
            page_size: Items per page

        Returns:
            Dict[str, Any]: Search results with pagination
        """
        # Start with base query
        query = select(Product)

        # Apply filters
        if search_term:
            # Convert to lowercase and add wildcards
            search_pattern = f"%{search_term.lower()}%"
            query = query.where(
                or_(
                    func.lower(Product.name).like(search_pattern),
                    func.lower(Product.description).like(search_pattern),
                    func.lower(Product.sku).like(search_pattern),
                    func.lower(Product.part_number).like(search_pattern),
                )
            )

        if is_active is not None:
            query = query.where(Product.is_active == is_active)

        # Filter by attributes (more complex in PostgreSQL)
        if attributes:
            for key, value in attributes.items():
                # Use JSONB containment operator
                query = query.where(
                    Product.attributes.contains({key: value})
                )

        # Use the paginate utility for consistent pagination
        return await paginate(self.db, query, page, page_size)

    async def _search_products_elasticsearch(
        self,
        es_client: AsyncElasticsearch,
        search_term: str,
        attributes: Optional[Dict[str, Any]] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        Search for products using Elasticsearch.

        Args:
            es_client: Elasticsearch client
            search_term: Text to search for
            attributes: Filter by product attributes
            is_active: Filter by active status
            page: Page number
            page_size: Items per page

        Returns:
            Dict[str, Any]: Search results with pagination
        """
        # Calculate from/size for pagination
        from_index = (page - 1) * page_size

        # Build query
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": search_term,
                                "fields": ["name^3", "description", "sku^2", "part_number^2"],
                                "type": "best_fields",
                                "fuzziness": "AUTO"
                            }
                        }
                    ],
                    "filter": []
                }
            },
            "from": from_index,
            "size": page_size,
            "highlight": {
                "fields": {
                    "name": {},
                    "description": {}
                }
            }
        }

        # Add filters

        if is_active is not None:
            query["query"]["bool"]["filter"].append(
                {"term": {"is_active": is_active}}
            )

        if attributes:
            for key, value in attributes.items():
                query["query"]["bool"]["filter"].append(
                    {"term": {f"attributes.{key}": value}}
                )

        # Execute search
        result = await es_client.search(
            index="products",
            body=query,
        )

        # Extract results
        hits = result["hits"]["hits"]
        total = result["hits"]["total"]["value"]

        # Get IDs from search results
        product_ids = [hit["_id"] for hit in hits]

        # Fetch actual products from database
        products = []
        if product_ids:
            # Fetch products in the same order as search results
            query = select(Product).where(
                Product.id.in_(product_ids)
            )

            result = await self.db.execute(query)
            db_products = {str(p.id): p for p in result.scalars().all()}

            # Preserve original ordering from search results
            products = [db_products[pid] for pid in product_ids if pid in db_products]

        # Calculate pages
        pages = (total + page_size - 1) // page_size if page_size > 0 else 0

        return {
            "items": products,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    async def search_fitments(
        self,
        search_term: Optional[str] = None,
        year: Optional[int] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        engine: Optional[str] = None,
        transmission: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        Search for fitments with filtering and pagination.

        Args:
            search_term: Text to search for
            year: Filter by year
            make: Filter by make
            model: Filter by model
            engine: Filter by engine
            transmission: Filter by transmission
            page: Page number
            page_size: Items per page

        Returns:
            Dict[str, Any]: Search results with pagination
        """
        # Start with base query
        query = select(Fitment)

        # Apply filters
        if search_term:
            # Convert to lowercase and add wildcards
            search_pattern = f"%{search_term.lower()}%"
            query = query.where(
                or_(
                    func.lower(Fitment.make).like(search_pattern),
                    func.lower(Fitment.model).like(search_pattern),
                    func.lower(Fitment.engine).like(search_pattern),
                    func.lower(Fitment.transmission).like(search_pattern),
                )
            )

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

        # Use the paginate utility for consistent pagination
        return await paginate(self.db, query, page, page_size)

    async def global_search(
        self,
        search_term: str,
        entity_types: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        Search across multiple entity types.

        Args:
            search_term: Text to search for
            entity_types: List of entity types to search (products, fitments, categories)
            page: Page number
            page_size: Items per page

        Returns:
            Dict[str, Any]: Search results grouped by entity type
        """
        # Default to all entity types if not specified
        if not entity_types:
            entity_types = ["products", "fitments", "categories"]

        results = {}

        # Search products
        if "products" in entity_types:
            product_results = await self.search_products(
                search_term=search_term,
                page=page,
                page_size=page_size,
            )
            results["products"] = product_results

        # Search fitments
        if "fitments" in entity_types:
            fitment_results = await self.search_fitments(
                search_term=search_term,
                page=page,
                page_size=page_size,
            )
            results["fitments"] = fitment_results

        return results


# Dependency for the search service
async def get_search_service(db: AsyncSession = Depends(get_db)) -> SearchService:
    """
    Get search service instance.

    Args:
        db: Database session

    Returns:
        SearchService: Search service
    """
    return SearchService(db)
