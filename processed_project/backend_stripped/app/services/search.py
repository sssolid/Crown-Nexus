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
    def __init__(self, db: AsyncSession):
        self.db = db
        self.es_client: Optional[AsyncElasticsearch] = None
    async def get_es_client(self) -> Optional[AsyncElasticsearch]:
        if self.es_client is None and settings.ELASTICSEARCH_HOST:
            self.es_client = AsyncElasticsearch([f'{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}'])
        return self.es_client
    async def search_products(self, search_term: Optional[str]=None, attributes: Optional[Dict[str, Any]]=None, is_active: Optional[bool]=None, page: int=1, page_size: int=20, use_elasticsearch: bool=True) -> Dict[str, Any]:
        if use_elasticsearch and search_term:
            es_client = await self.get_es_client()
            if es_client:
                try:
                    return await self._search_products_elasticsearch(es_client, search_term, attributes, is_active, page, page_size)
                except Exception as e:
                    print(f'Elasticsearch error: {e}')
        return await self._search_products_database(search_term, attributes, is_active, page, page_size)
    async def _search_products_database(self, search_term: Optional[str]=None, attributes: Optional[Dict[str, Any]]=None, is_active: Optional[bool]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Product)
        if search_term:
            search_pattern = f'%{search_term.lower()}%'
            query = query.where(or_(func.lower(Product.name).like(search_pattern), func.lower(Product.description).like(search_pattern), func.lower(Product.sku).like(search_pattern), func.lower(Product.part_number).like(search_pattern)))
        if is_active is not None:
            query = query.where(Product.is_active == is_active)
        if attributes:
            for key, value in attributes.items():
                query = query.where(Product.attributes.contains({key: value}))
        return await paginate(self.db, query, page, page_size)
    async def _search_products_elasticsearch(self, es_client: AsyncElasticsearch, search_term: str, attributes: Optional[Dict[str, Any]]=None, is_active: Optional[bool]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        from_index = (page - 1) * page_size
        query = {'query': {'bool': {'must': [{'multi_match': {'query': search_term, 'fields': ['name^3', 'description', 'sku^2', 'part_number^2'], 'type': 'best_fields', 'fuzziness': 'AUTO'}}], 'filter': []}}, 'from': from_index, 'size': page_size, 'highlight': {'fields': {'name': {}, 'description': {}}}}
        if is_active is not None:
            query['query']['bool']['filter'].append({'term': {'is_active': is_active}})
        if attributes:
            for key, value in attributes.items():
                query['query']['bool']['filter'].append({'term': {f'attributes.{key}': value}})
        result = await es_client.search(index='products', body=query)
        hits = result['hits']['hits']
        total = result['hits']['total']['value']
        product_ids = [hit['_id'] for hit in hits]
        products = []
        if product_ids:
            query = select(Product).where(Product.id.in_(product_ids))
            result = await self.db.execute(query)
            db_products = {str(p.id): p for p in result.scalars().all()}
            products = [db_products[pid] for pid in product_ids if pid in db_products]
        pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        return {'items': products, 'total': total, 'page': page, 'page_size': page_size, 'pages': pages}
    async def search_fitments(self, search_term: Optional[str]=None, year: Optional[int]=None, make: Optional[str]=None, model: Optional[str]=None, engine: Optional[str]=None, transmission: Optional[str]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Fitment)
        if search_term:
            search_pattern = f'%{search_term.lower()}%'
            query = query.where(or_(func.lower(Fitment.make).like(search_pattern), func.lower(Fitment.model).like(search_pattern), func.lower(Fitment.engine).like(search_pattern), func.lower(Fitment.transmission).like(search_pattern)))
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
        return await paginate(self.db, query, page, page_size)
    async def global_search(self, search_term: str, entity_types: Optional[List[str]]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        if not entity_types:
            entity_types = ['products', 'fitments', 'categories']
        results = {}
        if 'products' in entity_types:
            product_results = await self.search_products(search_term=search_term, page=page, page_size=page_size)
            results['products'] = product_results
        if 'fitments' in entity_types:
            fitment_results = await self.search_fitments(search_term=search_term, page=page, page_size=page_size)
            results['fitments'] = fitment_results
        return results
async def get_search_service(db: AsyncSession=Depends(get_db)) -> SearchService:
    return SearchService(db)