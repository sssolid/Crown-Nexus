from __future__ import annotations
'Elasticsearch search provider implementation.\n\nThis module provides a search provider that uses Elasticsearch for full-text search.\n'
import json
from typing import Any, Dict, List, Optional, Type
from elasticsearch import AsyncElasticsearch
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.core.config import settings
from app.core.exceptions import DatabaseException, ErrorCode, ServiceException
from app.logging import get_logger
from app.services.search.base import SearchProvider, SearchResult
from app.utils.retry import async_retry_on_network_errors
logger = get_logger('app.services.search.providers.elasticsearch')
class ElasticsearchSearchProvider(SearchProvider):
    def __init__(self, db: AsyncSession, model_class: Type[DeclarativeMeta], index_name: Optional[str]=None) -> None:
        self.db = db
        self.model_class = model_class
        self.index_name = index_name or model_class.__name__.lower()
        self.es_client: Optional[AsyncElasticsearch] = None
        self.search_fields: List[str] = []
        self.logger = logger
    async def initialize(self) -> None:
        if not settings.ELASTICSEARCH_HOST:
            self.logger.warning('Elasticsearch host not configured, provider will not be available')
            return
        try:
            self.es_client = AsyncElasticsearch([f'{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}'])
            if await self.es_client.ping():
                self.logger.info('Connected to Elasticsearch', host=settings.ELASTICSEARCH_HOST, port=settings.ELASTICSEARCH_PORT)
            else:
                self.logger.warning('Elasticsearch ping failed', host=settings.ELASTICSEARCH_HOST, port=settings.ELASTICSEARCH_PORT)
            model_name = self.model_class.__name__
            if model_name == 'Product':
                self.search_fields = ['name^3', 'description', 'sku^2', 'part_number^2']
            elif model_name == 'Fitment':
                self.search_fields = ['make^2', 'model^2', 'engine', 'transmission']
            else:
                self.search_fields = ['name^2', 'description', 'id', 'title']
            self.logger.debug(f"Initialized Elasticsearch search for {model_name} with fields: {', '.join(self.search_fields)}")
        except Exception as e:
            self.logger.error('Failed to connect to Elasticsearch', host=settings.ELASTICSEARCH_HOST, port=settings.ELASTICSEARCH_PORT, error=str(e), exc_info=True)
            self.es_client = None
    async def shutdown(self) -> None:
        if self.es_client:
            await self.es_client.close()
            self.logger.info('Elasticsearch client closed')
    @async_retry_on_network_errors(retries=2, delay=0.5)
    async def search(self, search_term: Optional[str]=None, filters: Optional[Dict[str, Any]]=None, page: int=1, page_size: int=20, **kwargs: Any) -> SearchResult:
        if not self.es_client:
            raise ServiceException(message='Elasticsearch client not initialized', code=ErrorCode.EXTERNAL_SERVICE_ERROR, details={'service': 'elasticsearch'})
        try:
            from_index = (page - 1) * page_size
            query: Dict[str, Any] = {'query': {'bool': {'must': [], 'filter': []}}, 'from': from_index, 'size': page_size, 'highlight': {'fields': {}}}
            if search_term:
                query['query']['bool']['must'].append({'multi_match': {'query': search_term, 'fields': self.search_fields, 'type': 'best_fields', 'fuzziness': 'AUTO'}})
                for field in self.search_fields:
                    base_field = field.split('^')[0]
                    query['highlight']['fields'][base_field] = {}
            else:
                query['query']['bool']['must'].append({'match_all': {}})
            if filters:
                for key, value in filters.items():
                    if isinstance(value, dict) and key == 'attributes':
                        for attr_key, attr_value in value.items():
                            query['query']['bool']['filter'].append({'term': {f'attributes.{attr_key}': attr_value}})
                    else:
                        query['query']['bool']['filter'].append({'term': {key: value}})
            self.logger.debug('Elasticsearch query built', search_term=search_term, filters=filters, query=json.dumps(query))
            result = await self.es_client.search(index=self.index_name, body=query)
            hits = result['hits']['hits']
            total = result['hits']['total']['value']
            self.logger.debug('Elasticsearch search results', hits_count=len(hits), total=total)
            entity_ids = [hit['_id'] for hit in hits]
            entities = []
            if entity_ids:
                try:
                    id_column = getattr(self.model_class, 'id')
                    db_query = select(self.model_class).where(id_column.in_(entity_ids))
                    db_result = await self.db.execute(db_query)
                    db_entities = {str(e.id): e for e in db_result.scalars().all()}
                    entities = [db_entities[eid] for eid in entity_ids if eid in db_entities]
                    self.logger.debug('Retrieved entities from database after ES search', entity_count=len(entities), found_ids=len(db_entities), total_ids=len(entity_ids))
                except SQLAlchemyError as e:
                    self.logger.error('Failed to fetch entities from database after ES search', error=str(e), entity_ids=entity_ids, exc_info=True)
                    raise DatabaseException(message='Failed to fetch entities after Elasticsearch search', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
            pages = (total + page_size - 1) // page_size if page_size > 0 else 0
            search_result = SearchResult({'items': entities, 'total': total, 'page': page, 'page_size': page_size, 'pages': pages, 'has_next': page < pages, 'has_prev': page > 1})
            if search_term:
                highlights = {}
                for hit in hits:
                    if '_source' in hit and 'id' in hit['_source'] and ('highlight' in hit):
                        highlights[hit['_source']['id']] = hit['highlight']
                search_result['highlights'] = highlights
            self.logger.info('Elasticsearch search successful', search_term=search_term, results_count=len(entities), total=total)
            return search_result
        except Exception as e:
            if isinstance(e, DatabaseException):
                raise
            self.logger.error('Elasticsearch search failed', search_term=search_term, error=str(e), exc_info=True)
            raise ServiceException(message='Failed to search with Elasticsearch', details={'service': 'elasticsearch'}, original_exception=e) from e