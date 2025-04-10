from __future__ import annotations
'API response schemas.\n\nThis module defines standardized response formats for API endpoints.\n'
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
T = TypeVar('T')
class ResponseBase(BaseModel):
    success: bool = True
    message: str
    code: int
    meta: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None
class Response(ResponseBase, Generic[T]):
    data: Optional[T] = None
    pagination: Optional[Dict[str, Any]] = None
    @classmethod
    def success(cls, data: Optional[Any]=None, message: str='Request successful', code: int=200, meta: Optional[Dict[str, Any]]=None, pagination: Optional[Dict[str, Any]]=None, request_id: Optional[str]=None) -> Response:
        return cls(success=True, message=message, code=code, data=data, meta=meta, pagination=pagination, request_id=request_id)
    @classmethod
    def error(cls, message: str, code: int=400, data: Optional[Any]=None, meta: Optional[Dict[str, Any]]=None, request_id: Optional[str]=None) -> Response:
        return cls(success=False, message=message, code=code, data=data, meta=meta, request_id=request_id)
class PaginatedResponse(ResponseBase, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    @classmethod
    def from_pagination_result(cls, items: List[Any], pagination: Dict[str, Any], message: str='Request successful', code: int=200, meta: Optional[Dict[str, Any]]=None, request_id: Optional[str]=None) -> PaginatedResponse:
        return cls(success=True, message=message, code=code, items=items, total=pagination.get('total', 0), page=pagination.get('page', 1), page_size=pagination.get('page_size', len(items)), pages=pagination.get('pages', 1), meta=meta, request_id=request_id)