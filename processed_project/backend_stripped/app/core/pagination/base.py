from __future__ import annotations
'\nBase interfaces and types for the pagination system.\n\nThis module defines common types, protocols, and interfaces\nused throughout the pagination components.\n'
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar
from pydantic import BaseModel, Field
from sqlalchemy.sql import Select
T = TypeVar('T')
R = TypeVar('R')
class SortDirection(str, Enum):
    ASC = 'asc'
    DESC = 'desc'
class SortField(BaseModel):
    field: str
    direction: SortDirection = SortDirection.ASC
class OffsetPaginationParams(BaseModel):
    page: int = Field(1, ge=1, description='Page number (1-indexed)')
    page_size: int = Field(20, ge=1, le=100, description='Number of items per page')
    sort: Optional[List[SortField]] = Field(None, description='Fields to sort by')
class CursorPaginationParams(BaseModel):
    cursor: Optional[str] = Field(None, description='Pagination cursor')
    limit: int = Field(20, ge=1, le=100, description='Maximum number of items to return')
    sort: Optional[List[SortField]] = Field(None, description='Fields to sort by')
class PaginationResult(Generic[R]):
    def __init__(self, items: List[R], total: int=0, page: Optional[int]=None, page_size: Optional[int]=None, pages: Optional[int]=None, next_cursor: Optional[str]=None, has_next: bool=False, has_prev: bool=False) -> None:
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.pages = pages
        self.next_cursor = next_cursor
        self.has_next = has_next
        self.has_prev = has_prev
    def to_dict(self) -> Dict[str, Any]:
        result = {'items': self.items, 'total': self.total, 'has_next': self.has_next, 'has_prev': self.has_prev}
        if self.page is not None:
            result['page'] = self.page
        if self.page_size is not None:
            result['page_size'] = self.page_size
        if self.pages is not None:
            result['pages'] = self.pages
        if self.next_cursor is not None:
            result['next_cursor'] = self.next_cursor
        return result
class PaginationProvider(Protocol, Generic[T, R]):
    async def paginate_with_offset(self, query: Select, params: OffsetPaginationParams, transform_func: Optional[callable]=None) -> PaginationResult[R]:
        ...
    async def paginate_with_cursor(self, query: Select, params: CursorPaginationParams, transform_func: Optional[callable]=None) -> PaginationResult[R]:
        ...