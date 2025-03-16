from __future__ import annotations
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from fastapi import Query
from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel
T = TypeVar('T')
class SortDirection(str, Enum):
    ASC = 'asc'
    DESC = 'desc'
class SortField(BaseModel):
    field: str = Field(..., description='Field name to sort by')
    direction: SortDirection = Field(default=SortDirection.ASC, description='Sort direction')
    @classmethod
    def from_string(cls, sort_string: str) -> 'SortField':
        if ':' in sort_string:
            field, direction = sort_string.split(':', 1)
            return cls(field=field, direction=SortDirection(direction.lower()))
        else:
            return cls(field=sort_string)
class OffsetPaginationParams(BaseModel):
    page: int = Field(1, ge=1, description='Page number (1-indexed)')
    page_size: int = Field(20, ge=1, le=100, description='Number of items per page')
    sort: Optional[List[SortField]] = Field(None, description='Fields to sort by')
    @validator('sort', pre=True)
    def parse_sort(cls, value: Any) -> Optional[List[SortField]]:
        if value is None:
            return None
        if isinstance(value, str):
            return [SortField.from_string(value)]
        if isinstance(value, list):
            result = []
            for item in value:
                if isinstance(item, str):
                    result.append(SortField.from_string(item))
                elif isinstance(item, dict):
                    result.append(SortField(**item))
                elif isinstance(item, SortField):
                    result.append(item)
            return result
        return None
class CursorPaginationParams(BaseModel):
    cursor: Optional[str] = Field(None, description='Cursor for pagination')
    limit: int = Field(20, ge=1, le=100, description='Maximum number of items to return')
    sort: Optional[List[SortField]] = Field(None, description='Fields to sort by')
    @validator('sort', pre=True)
    def parse_sort(cls, value: Any) -> Optional[List[SortField]]:
        if value is None:
            return None
        if isinstance(value, str):
            return [SortField.from_string(value)]
        if isinstance(value, list):
            result = []
            for item in value:
                if isinstance(item, str):
                    result.append(SortField.from_string(item))
                elif isinstance(item, dict):
                    result.append(SortField(**item))
                elif isinstance(item, SortField):
                    result.append(item)
            return result
        return None
class PaginationResult(GenericModel, Generic[T]):
    items: List[T] = Field(..., description='Items in the current page')
    total: int = Field(..., description='Total number of items')
    page: Optional[int] = Field(None, description='Current page number (for offset pagination)')
    page_size: Optional[int] = Field(None, description='Items per page (for offset pagination)')
    pages: Optional[int] = Field(None, description='Total number of pages (for offset pagination)')
    next_cursor: Optional[str] = Field(None, description='Cursor for next page (for cursor pagination)')
    prev_cursor: Optional[str] = Field(None, description='Cursor for previous page (for cursor pagination)')
    has_next: bool = Field(..., description='Whether there are more items')
    has_prev: bool = Field(..., description='Whether there are previous items')
def offset_pagination_params(page: int=Query(1, ge=1, description='Page number (1-indexed)'), page_size: int=Query(20, ge=1, le=100, description='Number of items per page'), sort: Optional[str]=Query(None, description='Sort fields (comma separated, prefix with - for desc)')) -> OffsetPaginationParams:
    sort_fields = None
    if sort:
        sort_fields = []
        for field in sort.split(','):
            field = field.strip()
            if field:
                if field.startswith('-'):
                    sort_fields.append(SortField(field=field[1:], direction=SortDirection.DESC))
                else:
                    sort_fields.append(SortField(field=field, direction=SortDirection.ASC))
    return OffsetPaginationParams(page=page, page_size=page_size, sort=sort_fields)
def cursor_pagination_params(cursor: Optional[str]=Query(None, description='Cursor for pagination'), limit: int=Query(20, ge=1, le=100, description='Maximum number of items to return'), sort: Optional[str]=Query(None, description='Sort fields (comma separated, prefix with - for desc)')) -> CursorPaginationParams:
    sort_fields = None
    if sort:
        sort_fields = []
        for field in sort.split(','):
            field = field.strip()
            if field:
                if field.startswith('-'):
                    sort_fields.append(SortField(field=field[1:], direction=SortDirection.DESC))
                else:
                    sort_fields.append(SortField(field=field, direction=SortDirection.ASC))
    return CursorPaginationParams(cursor=cursor, limit=limit, sort=sort_fields)