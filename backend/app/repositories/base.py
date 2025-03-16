# app/repositories/base.py
from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DatabaseException
from app.core.logging import get_logger
from app.db.base_class import Base
from app.db.utils import (
    bulk_create,
    count_query,
    create_object,
    delete_object,
    get_by_id,
    get_by_ids,
    paginate,
    update_object,
    upsert,
)

logger = get_logger("app.repositories.base")

T = TypeVar("T", bound=Base)
ID = TypeVar("ID")


class BaseRepository(Generic[T, ID]):
    """Generic repository for database operations.
    
    This class provides a standard interface for database operations,
    implementing the repository pattern for clean architecture.
    
    Attributes:
        model: SQLAlchemy model class
        db: Database session
    """
    
    def __init__(self, model: Type[T], db: AsyncSession) -> None:
        """Initialize the repository.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    async def get_by_id(self, id_value: ID) -> Optional[T]:
        """Get entity by ID.
        
        Args:
            id_value: Entity ID
            
        Returns:
            Optional[T]: Entity or None if not found
            
        Raises:
            DatabaseException: If a database error occurs
        """
        return await get_by_id(self.db, self.model, id_value)
    
    async def get_by_ids(self, ids: List[ID]) -> List[T]:
        """Get entities by IDs.
        
        Args:
            ids: List of entity IDs
            
        Returns:
            List[T]: List of found entities
            
        Raises:
            DatabaseException: If a database error occurs
        """
        return await get_by_ids(self.db, self.model, ids)
    
    async def get_all(
        self, 
        page: int = 1, 
        page_size: int = 100,
        order_by: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Get all entities with pagination.
        
        Args:
            page: Page number
            page_size: Page size
            order_by: Field to order by (prefix with - for descending)
            filters: Dictionary of field:value pairs for filtering
            
        Returns:
            Dict[str, Any]: Paginated results
            
        Raises:
            DatabaseException: If a database error occurs
        """
        query = self.model.active_only()
        
        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        
        # Apply ordering
        if order_by:
            is_desc = order_by.startswith("-")
            field_name = order_by[1:] if is_desc else order_by
            
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                query = query.order_by(field.desc() if is_desc else field)
        
        return await paginate(self.db, query, page, page_size)
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities matching filters.
        
        Args:
            filters: Dictionary of field:value pairs for filtering
            
        Returns:
            int: Count of matching entities
            
        Raises:
            DatabaseException: If a database error occurs
        """
        query = self.model.active_only()
        
        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        
        return await count_query(self.db, query)
    
    async def create(self, data: Dict[str, Any]) -> T:
        """Create a new entity.
        
        Args:
            data: Entity data
            
        Returns:
            T: Created entity
            
        Raises:
            DatabaseException: If a database error occurs
        """
        return await create_object(self.db, self.model, data)
    
    async def update(
        self, 
        id_value: ID, 
        data: Dict[str, Any], 
        user_id: Optional[Any] = None,
    ) -> Optional[T]:
        """Update an entity.
        
        Args:
            id_value: Entity ID
            data: Updated data
            user_id: ID of the user making the update
            
        Returns:
            Optional[T]: Updated entity or None if not found
            
        Raises:
            DatabaseException: If a database error occurs
        """
        return await update_object(self.db, self.model, id_value, data, user_id)
    
    async def delete(
        self, 
        id_value: ID, 
        user_id: Optional[Any] = None, 
        hard_delete: bool = False,
    ) -> bool:
        """Delete an entity.
        
        Args:
            id_value: Entity ID
            user_id: ID of the user performing the deletion
            hard_delete: Whether to permanently delete
            
        Returns:
            bool: True if deleted, False if not found
            
        Raises:
            DatabaseException: If a database error occurs
        """
        return await delete_object(
            self.db, self.model, id_value, user_id, hard_delete
        )
    
    async def bulk_create(self, items: List[Dict[str, Any]]) -> List[T]:
        """Create multiple entities.
        
        Args:
            items: List of entity data
            
        Returns:
            List[T]: Created entities
            
        Raises:
            DatabaseException: If a database error occurs
        """
        return await bulk_create(self.db, self.model, items)
    
    async def upsert(
        self, 
        data: Dict[str, Any], 
        unique_fields: List[str],
    ) -> T:
        """Insert or update an entity based on unique fields.
        
        Args:
            data: Entity data
            unique_fields: Fields to use for uniqueness check
            
        Returns:
            T: Created or updated entity
            
        Raises:
            DatabaseException: If a database error occurs
        """
        return await upsert(self.db, self.model, data, unique_fields)
    
    async def exists(self, filters: Dict[str, Any]) -> bool:
        """Check if an entity exists with the given filters.
        
        Args:
            filters: Filters to apply
            
        Returns:
            bool: True if entity exists
            
        Raises:
            DatabaseException: If a database error occurs
        """
        count = await self.count(filters)
        return count > 0
    
    async def find_one_by(self, filters: Dict[str, Any]) -> Optional[T]:
        """Find a single entity by filters.
        
        Args:
            filters: Filters to apply
            
        Returns:
            Optional[T]: Entity or None if not found
            
        Raises:
            DatabaseException: If a database error occurs
        """
        query = self.model.active_only()
        
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
        
        query = query.limit(1)
        
        try:
            result = await self.db.execute(query)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error finding {self.model.__name__} by filters: {str(e)}")
            raise DatabaseException(
                message=f"Failed to find {self.model.__name__} by filters: {str(e)}",
            ) from e
