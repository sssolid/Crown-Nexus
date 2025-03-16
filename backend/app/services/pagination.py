# app/services/pagination.py
from __future__ import annotations

import base64
import json
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union, cast

from fastapi import HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import Column, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import ClauseElement

from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.db.base_class import Base
from app.db.utils import count_query, execute_query
from app.schemas.pagination import (
    CursorPaginationParams,
    OffsetPaginationParams,
    PaginationResult,
    SortDirection,
    SortField,
)

logger = get_logger("app.services.pagination")

T = TypeVar("T", bound=Base)
R = TypeVar("R", bound=BaseModel)


class PaginationService(Generic[T, R]):
    """Service for handling pagination.
    
    This service supports both offset-based and cursor-based pagination.
    
    Attributes:
        db: Database session
        model: SQLAlchemy model class
        response_model: Pydantic response model
    """
    
    def __init__(
        self, 
        db: AsyncSession, 
        model: Type[T], 
        response_model: Type[R],
    ) -> None:
        """Initialize the pagination service.
        
        Args:
            db: Database session
            model: SQLAlchemy model class
            response_model: Pydantic response model
        """
        self.db = db
        self.model = model
        self.response_model = response_model
    
    async def paginate_with_offset(
        self,
        query: Select,
        params: OffsetPaginationParams,
        transform_func: Optional[Callable[[T], R]] = None,
    ) -> PaginationResult[R]:
        """Paginate query results using offset-based pagination.
        
        Args:
            query: SQLAlchemy query
            params: Pagination parameters
            transform_func: Function to transform items
            
        Returns:
            PaginationResult[R]: Paginated results
            
        Raises:
            ValidationException: If pagination parameters are invalid
        """
        # Count total items
        total = await count_query(self.db, query)
        
        # Calculate pagination metadata
        page = params.page
        page_size = params.page_size
        pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        if page > pages and pages > 0:
            page = pages
            
        # Apply sorting
        if params.sort:
            query = self._apply_sorting(query, params.sort)
            
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # Execute query
        result = await execute_query(self.db, query)
        items = list(result.scalars().all())
        
        # Transform items if needed
        transformed_items = items
        if transform_func:
            transformed_items = [transform_func(item) for item in items]
        elif hasattr(self.response_model, "from_orm"):
            transformed_items = [self.response_model.from_orm(item) for item in items]
        
        # Create pagination result
        return PaginationResult[R](
            items=transformed_items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )
    
    async def paginate_with_cursor(
        self,
        query: Select,
        params: CursorPaginationParams,
        transform_func: Optional[Callable[[T], R]] = None,
    ) -> PaginationResult[R]:
        """Paginate query results using cursor-based pagination.
        
        Args:
            query: SQLAlchemy query
            params: Pagination parameters
            transform_func: Function to transform items
            
        Returns:
            PaginationResult[R]: Paginated results
            
        Raises:
            ValidationException: If pagination parameters are invalid
        """
        # Ensure we have at least one sort field
        sort_fields = params.sort or [SortField(field="id", direction=SortDirection.ASC)]
        
        # Decode cursor if provided
        cursor_values = None
        if params.cursor:
            try:
                cursor_values = self._decode_cursor(params.cursor)
            except Exception as e:
                logger.warning(f"Invalid cursor: {str(e)}")
                raise ValidationException(
                    message="Invalid cursor format"
                )
        
        # Apply filter based on cursor
        original_query = query
        if cursor_values:
            query = self._apply_cursor_filter(query, sort_fields, cursor_values)
        
        # Apply sorting
        query = self._apply_sorting(query, sort_fields)
        
        # Apply limit
        query = query.limit(params.limit + 1)  # +1 to check if there are more items
        
        # Execute query
        result = await execute_query(self.db, query)
        items = list(result.scalars().all())
        
        # Count total (only for the first page)
        total = 0
        if not params.cursor:
            total = await count_query(self.db, original_query)
        
        # Check if there are more items
        has_next = len(items) > params.limit
        if has_next:
            items = items[:params.limit]  # Remove the extra item
        
        # Generate next cursor
        next_cursor = None
        if has_next and items:
            next_cursor = self._encode_cursor(items[-1], sort_fields)
        
        # Transform items if needed
        transformed_items = items
        if transform_func:
            transformed_items = [transform_func(item) for item in items]
        elif hasattr(self.response_model, "from_orm"):
            transformed_items = [self.response_model.from_orm(item) for item in items]
        
        # Create pagination result
        return PaginationResult[R](
            items=transformed_items,
            total=total,
            next_cursor=next_cursor,
            has_next=has_next,
            has_prev=bool(params.cursor),
        )
    
    def _apply_sorting(self, query: Select, sort_fields: List[SortField]) -> Select:
        """Apply sorting to a query.
        
        Args:
            query: SQLAlchemy query
            sort_fields: Fields to sort by
            
        Returns:
            Select: Query with sorting applied
            
        Raises:
            ValidationException: If sort field is invalid
        """
        for sort_field in sort_fields:
            field_name = sort_field.field
            
            # Get column to sort by
            if not hasattr(self.model, field_name):
                raise ValidationException(
                    message=f"Invalid sort field: {field_name}"
                )
                
            column = getattr(self.model, field_name)
            
            # Apply sort direction
            if sort_field.direction == SortDirection.DESC:
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))
        
        return query
    
    def _apply_cursor_filter(
        self,
        query: Select,
        sort_fields: List[SortField],
        cursor_values: Dict[str, Any],
    ) -> Select:
        """Apply cursor-based filtering to a query.
        
        Args:
            query: SQLAlchemy query
            sort_fields: Fields used for sorting
            cursor_values: Values from cursor
            
        Returns:
            Select: Query with cursor filter applied
            
        Raises:
            ValidationException: If cursor field is invalid
        """
        # Build a filter condition based on sort fields and cursor values
        conditions = []
        for i, sort_field in enumerate(sort_fields):
            field_name = sort_field.field
            
            # Ensure field exists in cursor values
            if field_name not in cursor_values:
                continue
                
            # Get column and value
            if not hasattr(self.model, field_name):
                raise ValidationException(
                    message=f"Invalid cursor field: {field_name}"
                )
                
            column = getattr(self.model, field_name)
            value = cursor_values[field_name]
            
            # Create condition based on sort direction
            if i == 0:
                # First field uses > or < depending on sort direction
                if sort_field.direction == SortDirection.ASC:
                    conditions.append(column > value)
                else:
                    conditions.append(column < value)
            else:
                # Subsequent fields use equality for previous fields
                previous_field = sort_fields[i-1].field
                previous_column = getattr(self.model, previous_field)
                previous_value = cursor_values[previous_field]
                
                # Add condition for equality on previous field
                conditions.append(previous_column == previous_value)
                
                # Add condition for current field
                if sort_field.direction == SortDirection.ASC:
                    conditions.append(column > value)
                else:
                    conditions.append(column < value)
        
        # Apply conditions to query
        if conditions:
            query = query.where(*conditions)
        
        return query
    
    def _encode_cursor(self, item: T, sort_fields: List[SortField]) -> str:
        """Encode a cursor from an item.
        
        Args:
            item: Item to encode
            sort_fields: Fields used for sorting
            
        Returns:
            str: Encoded cursor
        """
        cursor_data = {}
        
        for sort_field in sort_fields:
            field_name = sort_field.field
            
            if not hasattr(item, field_name):
                continue
                
            value = getattr(item, field_name)
            
            # Handle special types
            if isinstance(value, (datetime, uuid.UUID)):
                value = str(value)
                
            cursor_data[field_name] = value
        
        # Encode cursor as base64
        cursor_json = json.dumps(cursor_data)
        return base64.b64encode(cursor_json.encode('utf-8')).decode('utf-8')
    
    def _decode_cursor(self, cursor: str) -> Dict[str, Any]:
        """Decode a cursor into values.
        
        Args:
            cursor: Encoded cursor
            
        Returns:
            Dict[str, Any]: Decoded cursor values
            
        Raises:
            ValueError: If cursor format is invalid
        """
        try:
            cursor_json = base64.b64decode(cursor.encode('utf-8')).decode('utf-8')
            return json.loads(cursor_json)
        except Exception as e:
            raise ValueError(f"Invalid cursor format: {str(e)}")
