from __future__ import annotations
'Search service package for application-wide search functionality.\n\nThis package provides services for searching across various entity types\nand different backends, including database and Elasticsearch.\n'
from app.services.search.service import SearchService
def get_search_service(db):
    return SearchService(db)
__all__ = ['get_search_service', 'SearchService']