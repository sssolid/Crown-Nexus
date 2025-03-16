# app/schemas/responses.py
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class ResponseStatus(BaseModel):
    """Response status information.
    
    Attributes:
        success: Whether the request was successful
        code: HTTP status code
        message: Status message
        timestamp: Response timestamp
    """
    
    success: bool = Field(
        ..., 
        description="Whether the request was successful"
    )
    code: int = Field(
        ..., 
        description="HTTP status code"
    )
    message: str = Field(
        ..., 
        description="Status message"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )


class PaginationMeta(BaseModel):
    """Pagination metadata.
    
    Attributes:
        page: Current page number
        page_size: Number of items per page
        total_items: Total number of items
        total_pages: Total number of pages
        has_next: Whether there are more pages
        has_prev: Whether there are previous pages
    """
    
    page: int = Field(
        ..., 
        description="Current page number", 
        ge=1
    )
    page_size: int = Field(
        ..., 
        description="Number of items per page", 
        ge=1
    )
    total_items: int = Field(
        ..., 
        description="Total number of items", 
        ge=0
    )
    total_pages: int = Field(
        ..., 
        description="Total number of pages", 
        ge=0
    )
    has_next: bool = Field(
        ..., 
        description="Whether there are more pages"
    )
    has_prev: bool = Field(
        ..., 
        description="Whether there are previous pages"
    )
    
    @classmethod
    def from_pagination_result(cls, result: Dict[str, Any]) -> "PaginationMeta":
        """Create pagination metadata from pagination result.
        
        Args:
            result: Pagination result from service
            
        Returns:
            PaginationMeta: Pagination metadata
        """
        page = result.get("page", 1)
        page_size = result.get("page_size", 20)
        total_items = result.get("total", 0)
        total_pages = result.get("pages", 0)
        
        return cls(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )


class MetaData(BaseModel):
    """Response metadata.
    
    Attributes:
        pagination: Pagination metadata
        request_id: Request ID for tracking
        extra: Additional metadata
    """
    
    pagination: Optional[PaginationMeta] = Field(
        None, 
        description="Pagination metadata"
    )
    request_id: Optional[str] = Field(
        None, 
        description="Request ID for tracking"
    )
    extra: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional metadata"
    )


class Response(GenericModel, Generic[T]):
    """Standard API response envelope.
    
    All API responses are wrapped in this model to ensure a consistent format.
    
    Attributes:
        status: Response status information
        data: Response data
        meta: Response metadata
    """
    
    status: ResponseStatus = Field(
        ..., 
        description="Response status information"
    )
    data: Optional[T] = Field(
        None, 
        description="Response data"
    )
    meta: Optional[MetaData] = Field(
        None, 
        description="Response metadata"
    )
    
    @classmethod
    def success(
        cls,
        data: Optional[T] = None,
        message: str = "Request successful",
        code: int = 200,
        meta: Optional[Dict[str, Any]] = None,
        pagination: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> "Response[T]":
        """Create a success response.
        
        Args:
            data: Response data
            message: Success message
            code: HTTP status code
            meta: Additional metadata
            pagination: Pagination metadata
            request_id: Request ID for tracking
            
        Returns:
            Response[T]: Success response
        """
        status = ResponseStatus(
            success=True,
            code=code,
            message=message,
        )
        
        metadata = None
        if meta or pagination or request_id:
            pagination_meta = None
            if pagination:
                pagination_meta = PaginationMeta.from_pagination_result(pagination)
                
            metadata = MetaData(
                pagination=pagination_meta,
                request_id=request_id,
                extra=meta,
            )
        
        return cls(
            status=status,
            data=data,
            meta=metadata,
        )
    
    @classmethod
    def error(
        cls,
        message: str,
        code: int = 400,
        data: Optional[Any] = None,
        meta: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> "Response[T]":
        """Create an error response.
        
        Args:
            message: Error message
            code: HTTP status code
            data: Error data
            meta: Additional metadata
            request_id: Request ID for tracking
            
        Returns:
            Response[T]: Error response
        """
        status = ResponseStatus(
            success=False,
            code=code,
            message=message,
        )
        
        metadata = None
        if meta or request_id:
            metadata = MetaData(
                request_id=request_id,
                extra=meta,
            )
        
        return cls(
            status=status,
            data=data,
            meta=metadata,
        )


class PaginatedResponse(Response, Generic[T]):
    """Paginated API response.
    
    This is a specialized response model for paginated results.
    
    Attributes:
        data: List of items
        meta: Response metadata with pagination
    """
    
    data: List[T] = Field(
        ..., 
        description="List of items"
    )
    meta: MetaData = Field(
        ..., 
        description="Response metadata with pagination"
    )
    
    @classmethod
    def from_pagination_result(
        cls,
        items: List[T],
        pagination: Dict[str, Any],
        message: str = "Request successful",
        code: int = 200,
        meta: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> "PaginatedResponse[T]":
        """Create a paginated response from pagination result.
        
        Args:
            items: List of items
            pagination: Pagination metadata
            message: Success message
            code: HTTP status code
            meta: Additional metadata
            request_id: Request ID for tracking
            
        Returns:
            PaginatedResponse[T]: Paginated response
        """
        return Response.success(
            data=items,
            message=message,
            code=code,
            meta=meta,
            pagination=pagination,
            request_id=request_id,
          )
