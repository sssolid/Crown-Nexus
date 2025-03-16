# app/services/base.py
from __future__ import annotations

import uuid
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BusinessLogicException,
    DatabaseException,
    ValidationException,
)
from app.core.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import (
    count_query,
    transaction,
    transactional,
)
from app.models.user import User
from app.repositories.base import BaseRepository
from app.utils.errors import (
    ensure_not_none,
    resource_already_exists,
    resource_not_found,
    validation_error,
)

logger = get_logger("app.services.base")

# Generic type variables
T = TypeVar("T", bound=Base)  # SQLAlchemy model
C = TypeVar("C", bound=BaseModel)  # Create schema
U = TypeVar("U", bound=BaseModel)  # Update schema
R = TypeVar("R", bound=BaseModel)  # Response schema


class BaseService(Generic[T, C, U, R]):
    """Base service for CRUD operations on entities.
    
    This service provides standardized CRUD operations with:
    - Integrated permissions checking
    - Transaction management
    - Error handling
    - Validation
    
    Attributes:
        model: SQLAlchemy model class
        repository: Repository for database operations
        create_schema: Pydantic model for create operations
        update_schema: Pydantic model for update operations
        response_schema: Pydantic model for responses
    """
    
    def __init__(
        self,
        db: AsyncSession,
        model_class: Type[T],
        create_schema: Type[C],
        update_schema: Type[U],
        response_schema: Type[R],
    ) -> None:
        """Initialize the service.
        
        Args:
            db: Database session
            model_class: SQLAlchemy model class
            create_schema: Pydantic model for create operations
            update_schema: Pydantic model for update operations
            response_schema: Pydantic model for responses
        """
        self.db = db
        self.model = model_class
        self.repository = BaseRepository(model_class, db)
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema
        
        # Resource name for permissions and error messages
        self.resource_name = model_class.__name__
        
    @transactional
    async def get(self, id: Any, current_user: User) -> T:
        """Get entity by ID with permission check.
        
        Args:
            id: Entity ID
            current_user: Current authenticated user
            
        Returns:
            T: Entity
            
        Raises:
            ResourceNotFoundException: If entity not found
            PermissionDeniedException: If user doesn't have permission
        """
        # Check read permission
        permission = f"{self.resource_name.lower()}:read"
        PermissionChecker.ensure_object_permission(
            current_user, 
            {"id": id},  # Dummy object for permission check
            cast(Permission, permission),
        )
        
        # Get entity
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise resource_not_found(self.resource_name, id)
            
        # Check object-level permission
        PermissionChecker.ensure_object_permission(
            current_user, entity, cast(Permission, permission)
        )
        
        return entity
    
    @transactional
    async def get_multi(
        self,
        current_user: User,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get multiple entities with pagination.
        
        Args:
            current_user: Current authenticated user
            page: Page number
            page_size: Items per page
            filters: Filters to apply
            order_by: Field to order by
            
        Returns:
            Dict[str, Any]: Paginated results
            
        Raises:
            PermissionDeniedException: If user doesn't have permission
        """
        # Check read permission
        permission = f"{self.resource_name.lower()}:read"
        PermissionChecker.ensure_object_permission(
            current_user, 
            {},  # Dummy object for permission check
            cast(Permission, permission),
        )
        
        # Get entities
        result = await self.repository.get_all(
            page=page,
            page_size=page_size,
            filters=filters,
            order_by=order_by,
        )
        
        return result
    
    @transactional
    async def create(
        self, 
        obj_in: Union[C, Dict[str, Any]], 
        current_user: User,
    ) -> T:
        """Create new entity.
        
        Args:
            obj_in: Entity data
            current_user: Current authenticated user
            
        Returns:
            T: Created entity
            
        Raises:
            ValidationException: If validation fails
            PermissionDeniedException: If user doesn't have permission
        """
        # Check create permission
        permission = f"{self.resource_name.lower()}:create"
        PermissionChecker.ensure_object_permission(
            current_user, 
            {},  # Dummy object for permission check
            cast(Permission, permission),
        )
        
        # Validate input
        if isinstance(obj_in, dict):
            data = obj_in
        else:
            data = obj_in.dict(exclude_unset=True)
            
        # Pre-create validation
        await self.validate_create(data, current_user)
        
        # Add audit fields
        if hasattr(self.model, "created_by_id"):
            data["created_by_id"] = str(current_user.id)
            
        if hasattr(self.model, "updated_by_id"):
            data["updated_by_id"] = str(current_user.id)
            
        # Create entity
        try:
            entity = await self.repository.create(data)
            
            # Post-create processing
            await self.after_create(entity, current_user)
            
            return entity
        except Exception as e:
            logger.error(f"Error creating {self.resource_name}: {str(e)}")
            if isinstance(e, (ValidationException, BusinessLogicException)):
                raise
            raise DatabaseException(message=f"Failed to create {self.resource_name}: {str(e)}") from e
    
    @transactional
    async def update(
        self,
        id: Any,
        obj_in: Union[U, Dict[str, Any]],
        current_user: User,
    ) -> T:
        """Update entity.
        
        Args:
            id: Entity ID
            obj_in: Updated data
            current_user: Current authenticated user
            
        Returns:
            T: Updated entity
            
        Raises:
            ResourceNotFoundException: If entity not found
            ValidationException: If validation fails
            PermissionDeniedException: If user doesn't have permission
        """
        # Get existing entity
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise resource_not_found(self.resource_name, id)
            
        # Check update permission
        permission = f"{self.resource_name.lower()}:update"
        PermissionChecker.ensure_object_permission(
            current_user, entity, cast(Permission, permission)
        )
        
        # Validate input
        if isinstance(obj_in, dict):
            data = obj_in
        else:
            data = obj_in.dict(exclude_unset=True)
            
        # Pre-update validation
        await self.validate_update(entity, data, current_user)
        
        # Add audit fields
        if hasattr(self.model, "updated_by_id"):
            data["updated_by_id"] = str(current_user.id)
            
        # Update entity
        try:
            updated_entity = await self.repository.update(id, data, current_user.id)
            if not updated_entity:
                raise resource_not_found(self.resource_name, id)
                
            # Post-update processing
            await self.after_update(updated_entity, entity, current_user)
                
            return updated_entity
        except Exception as e:
            logger.error(f"Error updating {self.resource_name}: {str(e)}")
            if isinstance(e, (ValidationException, BusinessLogicException)):
                raise
            raise DatabaseException(message=f"Failed to update {self.resource_name}: {str(e)}") from e
    
    @transactional
    async def delete(
        self,
        id: Any,
        current_user: User,
        hard_delete: bool = False,
    ) -> bool:
        """Delete entity.
        
        Args:
            id: Entity ID
            current_user: Current authenticated user
            hard_delete: Whether to permanently delete
            
        Returns:
            bool: True if deleted
            
        Raises:
            ResourceNotFoundException: If entity not found
            PermissionDeniedException: If user doesn't have permission
        """
        # Get existing entity
        entity = await self.repository.get_by_id(id)
        if not entity:
            raise resource_not_found(self.resource_name, id)
            
        # Check delete permission
        permission = f"{self.resource_name.lower()}:delete"
        PermissionChecker.ensure_object_permission(
            current_user, entity, cast(Permission, permission)
        )
        
        # Pre-delete validation
        await self.validate_delete(entity, current_user)
        
        # Delete entity
        try:
            result = await self.repository.delete(id, current_user.id, hard_delete)
            if not result:
                raise resource_not_found(self.resource_name, id)
                
            # Post-delete processing
            await self.after_delete(entity, current_user)
                
            return result
        except Exception as e:
            logger.error(f"Error deleting {self.resource_name}: {str(e)}")
            if isinstance(e, (ValidationException, BusinessLogicException)):
                raise
            raise DatabaseException(message=f"Failed to delete {self.resource_name}: {str(e)}") from e
    
    async def to_response(self, entity: T) -> R:
        """Convert entity to response model.
        
        Args:
            entity: Entity to convert
            
        Returns:
            R: Response model
        """
        return self.response_schema.from_orm(entity)
    
    async def to_response_multi(self, entities: List[T]) -> List[R]:
        """Convert multiple entities to response models.
        
        Args:
            entities: Entities to convert
            
        Returns:
            List[R]: Response models
        """
        return [await self.to_response(entity) for entity in entities]
    
    # Hook methods for subclasses to override
    
    async def validate_create(self, data: Dict[str, Any], current_user: User) -> None:
        """Validate data before creation.
        
        Args:
            data: Entity data
            current_user: Current authenticated user
            
        Raises:
            ValidationException: If validation fails
        """
        pass
    
    async def validate_update(
        self, 
        entity: T, 
        data: Dict[str, Any], 
        current_user: User,
    ) -> None:
        """Validate data before update.
        
        Args:
            entity: Existing entity
            data: Updated data
            current_user: Current authenticated user
            
        Raises:
            ValidationException: If validation fails
        """
        pass
    
    async def validate_delete(self, entity: T, current_user: User) -> None:
        """Validate before deletion.
        
        Args:
            entity: Entity to delete
            current_user: Current authenticated user
            
        Raises:
            ValidationException: If validation fails
        """
        pass
    
    async def after_create(self, entity: T, current_user: User) -> None:
        """Hook for post-creation processing.
        
        Args:
            entity: Created entity
            current_user: Current authenticated user
        """
        pass
    
    async def after_update(
        self, 
        updated_entity: T, 
        original_entity: T, 
        current_user: User,
    ) -> None:
        """Hook for post-update processing.
        
        Args:
            updated_entity: Updated entity
            original_entity: Original entity before update
            current_user: Current authenticated user
        """
        pass
    
    async def after_delete(self, entity: T, current_user: User) -> None:
        """Hook for post-deletion processing.
        
        Args:
            entity: Deleted entity
            current_user: Current authenticated user
        """
        pass
