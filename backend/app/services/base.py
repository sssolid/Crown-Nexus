# /backend/app/services/base.py
from __future__ import annotations

import uuid
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BusinessLogicException, 
    DatabaseException, 
    ErrorCode, 
    PermissionDeniedException, 
    ResourceAlreadyExistsException, 
    ResourceNotFoundException, 
    ValidationException
)
from app.core.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import count_query, transaction, transactional
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.pagination import (
    CursorPaginationParams, 
    OffsetPaginationParams, 
    PaginationResult
)
from app.services.interfaces import CrudServiceInterface
from app.services.pagination import PaginationService
from app.utils.errors import (
    ensure_not_none, 
    resource_already_exists, 
    resource_not_found, 
    validation_error
)

# Type variables
T = TypeVar("T", bound=Base)  # SQLAlchemy model
C = TypeVar("C", bound=BaseModel)  # Create schema
U = TypeVar("U", bound=BaseModel)  # Update schema
R = TypeVar("R", bound=BaseModel)  # Response schema
ID = TypeVar("ID")  # ID type

# Logger
logger = get_logger("app.services.base")

class BaseService(Generic[T, C, U, R, ID], CrudServiceInterface[T, ID, C, U, R]):
    """Base service for CRUD operations on entities.

    This service provides standardized CRUD operations with:
    - Integrated permissions checking
    - Transaction management
    - Error handling
    - Validation
    - Event dispatching
    - Logging

    Attributes:
        db: AsyncSession for database operations
        model: SQLAlchemy model class
        repository: Repository for database operations
        create_schema: Pydantic model for create operations
        update_schema: Pydantic model for update operations
        response_schema: Pydantic model for responses
        required_create_permission: Permission required for create operations
        required_read_permission: Permission required for read operations
        required_update_permission: Permission required for update operations
        required_delete_permission: Permission required for delete operations
    """

    def __init__(
        self,
        db: AsyncSession,
        model_class: Type[T],
        create_schema: Type[C],
        update_schema: Type[U],
        response_schema: Type[R],
        repository_class: Type[BaseRepository[T, ID]] = BaseRepository,
    ) -> None:
        """Initialize the service.

        Args:
            db: Database session
            model_class: SQLAlchemy model class
            create_schema: Pydantic model for create operations
            update_schema: Pydantic model for update operations
            response_schema: Pydantic model for responses
            repository_class: Repository class for database operations
        """
        self.db = db
        self.model = model_class
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.response_schema = response_schema
        self.repository = repository_class(model_class, db)
        self.pagination_service = PaginationService[T, R](db, model_class, response_schema)
        self.logger = logger.bind(service=self.__class__.__name__)
        
        # Default permissions
        self.required_create_permission: Optional[Permission] = None
        self.required_read_permission: Optional[Permission] = None
        self.required_update_permission: Optional[Permission] = None
        self.required_delete_permission: Optional[Permission] = None

    async def initialize(self) -> None:
        """Initialize service resources."""
        self.logger.debug("Initializing service")
        
    async def shutdown(self) -> None:
        """Release service resources."""
        self.logger.debug("Shutting down service")

    @transactional
    async def create(self, data: Dict[str, Any], user_id: Optional[str] = None) -> T:
        """Create new entity.

        Args:
            data: Entity data
            user_id: Current user ID

        Returns:
            T: Created entity

        Raises:
            ValidationException: If validation fails
            PermissionDeniedException: If user doesn't have permission
        """
        self.logger.debug(f"Creating entity with data: {data}")
        
        # Check permissions if user_id is provided and permission is required
        if user_id and self.required_create_permission:
            user = await self._get_user(user_id)
            if not PermissionChecker.has_permission(user, self.required_create_permission):
                self.logger.warning(
                    f"Permission denied for user {user_id} to create {self.model.__name__}"
                )
                raise PermissionDeniedException(
                    f"You don't have permission to create {self.model.__name__}",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": self.required_create_permission},
                    status_code=403,
                )

        # Validate data
        await self.validate_create(data, user_id)
        
        # Pre-create hook
        await self.before_create(data, user_id)
        
        try:
            # Create entity
            entity = await self.repository.create(data)
            
            # Post-create hook
            await self.after_create(entity, user_id)
            
            self.logger.info(
                f"Created {self.model.__name__} with ID: {getattr(entity, 'id', None)}"
            )
            return entity
        except Exception as e:
            self.logger.error(f"Error creating entity: {str(e)}")
            raise

    async def create_with_schema(self, schema: C, user_id: Optional[str] = None) -> T:
        """Create a new entity using a Pydantic schema.

        Args:
            schema: Create schema
            user_id: Optional user ID for permission checks

        Returns:
            T: The created entity
        """
        return await self.create(schema.dict(), user_id)

    @transactional
    async def delete(self, id: ID, user_id: Optional[str] = None, hard_delete: bool = False) -> bool:
        """Delete entity.

        Args:
            id: Entity ID
            user_id: Current user ID
            hard_delete: Whether to permanently delete

        Returns:
            bool: True if deleted

        Raises:
            ResourceNotFoundException: If entity not found
            PermissionDeniedException: If user doesn't have permission
        """
        self.logger.debug(f"Deleting entity with ID: {id}")
        
        # Get entity
        entity = await self.repository.get_by_id(id)
        if not entity:
            self.logger.warning(f"{self.model.__name__} with ID {id} not found")
            raise ResourceNotFoundException(
                f"{self.model.__name__} not found",
                code=ErrorCode.RESOURCE_NOT_FOUND,
                details={"id": str(id)},
                status_code=404,
            )
            
        # Check permissions if user_id is provided and permission is required
        if user_id and self.required_delete_permission:
            user = await self._get_user(user_id)
            if not PermissionChecker.has_permission(user, self.required_delete_permission):
                self.logger.warning(
                    f"Permission denied for user {user_id} to delete {self.model.__name__}"
                )
                raise PermissionDeniedException(
                    f"You don't have permission to delete {self.model.__name__}",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": self.required_delete_permission},
                    status_code=403,
                )
        
        # Validate delete
        await self.validate_delete(entity, user_id)
        
        # Pre-delete hook
        await self.before_delete(entity, user_id)
        
        try:
            # Delete entity
            result = await self.repository.delete(id, user_id, hard_delete)
            
            # Post-delete hook
            await self.after_delete(entity, user_id)
            
            self.logger.info(f"Deleted {self.model.__name__} with ID: {id}")
            return result
        except Exception as e:
            self.logger.error(f"Error deleting entity: {str(e)}")
            raise

    @transactional
    async def get(self, id: ID, user_id: Optional[str] = None) -> T:
        """Get entity by ID with permission check.

        Args:
            id: Entity ID
            user_id: Current user ID

        Returns:
            T: Entity

        Raises:
            ResourceNotFoundException: If entity not found
            PermissionDeniedException: If user doesn't have permission
        """
        self.logger.debug(f"Getting entity with ID: {id}")
        
        # Get entity
        entity = await self.repository.get_by_id(id)
        if not entity:
            self.logger.warning(f"{self.model.__name__} with ID {id} not found")
            raise ResourceNotFoundException(
                f"{self.model.__name__} not found",
                code=ErrorCode.RESOURCE_NOT_FOUND,
                details={"id": str(id)},
                status_code=404,
            )
            
        # Check permissions if user_id is provided and permission is required
        if user_id and self.required_read_permission:
            user = await self._get_user(user_id)
            if not PermissionChecker.has_permission(user, self.required_read_permission):
                self.logger.warning(
                    f"Permission denied for user {user_id} to read {self.model.__name__}"
                )
                raise PermissionDeniedException(
                    f"You don't have permission to read {self.model.__name__}",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": self.required_read_permission},
                    status_code=403,
                )
                
        self.logger.debug(f"Found {self.model.__name__} with ID: {id}")
        return entity

    async def get_by_id(self, id: ID, user_id: Optional[str] = None) -> Optional[T]:
        """Get entity by ID without raising exceptions.

        Args:
            id: Entity ID
            user_id: Current user ID

        Returns:
            Optional[T]: Entity or None if not found
        """
        try:
            return await self.get(id, user_id)
        except ResourceNotFoundException:
            return None
        except PermissionDeniedException:
            return None

    @transactional
    async def get_multi(
        self,
        user_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get multiple entities with pagination.

        Args:
            user_id: Current user ID
            page: Page number
            page_size: Items per page
            filters: Filters to apply
            order_by: Field to order by

        Returns:
            Dict[str, Any]: Paginated results

        Raises:
            PermissionDeniedException: If user doesn't have permission
        """
        self.logger.debug(
            f"Getting entities with page={page}, page_size={page_size}, filters={filters}"
        )
        
        # Check permissions if user_id is provided and permission is required
        if user_id and self.required_read_permission:
            user = await self._get_user(user_id)
            if not PermissionChecker.has_permission(user, self.required_read_permission):
                self.logger.warning(
                    f"Permission denied for user {user_id} to list {self.model.__name__}"
                )
                raise PermissionDeniedException(
                    f"You don't have permission to list {self.model.__name__}",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": self.required_read_permission},
                    status_code=403,
                )
                
        # Apply custom filters
        applied_filters = filters or {}
        if hasattr(self, "apply_filters"):
            applied_filters = await self.apply_filters(applied_filters, user_id)
            
        try:
            # Get paginated results
            result = await self.repository.get_all(
                page=page,
                page_size=page_size,
                order_by=order_by,
                filters=applied_filters,
            )
            
            self.logger.debug(
                f"Found {result.get('total', 0)} {self.model.__name__} entities"
            )
            return result
        except Exception as e:
            self.logger.error(f"Error getting entities: {str(e)}")
            raise

    async def get_all(
        self, 
        page: int = 1, 
        page_size: int = 20, 
        filters: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get all entities with pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            filters: Optional filters to apply
            user_id: Optional user ID for permission checks

        Returns:
            Dict[str, Any]: Paginated results
        """
        return await self.get_multi(user_id, page, page_size, filters)

    async def get_paginated(
        self, 
        user_id: Optional[str], 
        params: OffsetPaginationParams,
        filters: Optional[Dict[str, Any]] = None
    ) -> PaginationResult[R]:
        """Get paginated entities using offset-based pagination.

        Args:
            user_id: Current user ID
            params: Pagination parameters
            filters: Filters to apply

        Returns:
            PaginationResult[R]: Paginated results

        Raises:
            PermissionDeniedException: If user doesn't have permission
        """
        # Check permissions if user_id is provided and permission is required
        if user_id and self.required_read_permission:
            user = await self._get_user(user_id)
            if not PermissionChecker.has_permission(user, self.required_read_permission):
                self.logger.warning(
                    f"Permission denied for user {user_id} to list {self.model.__name__}"
                )
                raise PermissionDeniedException(
                    f"You don't have permission to list {self.model.__name__}",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": self.required_read_permission},
                    status_code=403,
                )
                
        # Build query
        query = self.repository.build_query(filters)
        
        # Get paginated results
        return await self.pagination_service.paginate_with_offset(
            query, 
            params,
            self.to_response
        )

    async def get_paginated_with_cursor(
        self, 
        user_id: Optional[str], 
        params: CursorPaginationParams,
        filters: Optional[Dict[str, Any]] = None
    ) -> PaginationResult[R]:
        """Get paginated entities using cursor-based pagination.

        Args:
            user_id: Current user ID
            params: Pagination parameters
            filters: Filters to apply

        Returns:
            PaginationResult[R]: Paginated results

        Raises:
            PermissionDeniedException: If user doesn't have permission
        """
        # Check permissions if user_id is provided and permission is required
        if user_id and self.required_read_permission:
            user = await self._get_user(user_id)
            if not PermissionChecker.has_permission(user, self.required_read_permission):
                self.logger.warning(
                    f"Permission denied for user {user_id} to list {self.model.__name__}"
                )
                raise PermissionDeniedException(
                    f"You don't have permission to list {self.model.__name__}",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": self.required_read_permission},
                    status_code=403,
                )
                
        # Build query
        query = self.repository.build_query(filters)
        
        # Get paginated results
        return await self.pagination_service.paginate_with_cursor(
            query, 
            params,
            self.to_response
        )

    @transactional
    async def update(
        self, 
        id: ID, 
        data: Dict[str, Any], 
        user_id: Optional[str] = None
    ) -> T:
        """Update entity.

        Args:
            id: Entity ID
            data: Updated data
            user_id: Current user ID

        Returns:
            T: Updated entity

        Raises:
            ResourceNotFoundException: If entity not found
            ValidationException: If validation fails
            PermissionDeniedException: If user doesn't have permission
        """
        self.logger.debug(f"Updating entity with ID: {id}, data: {data}")
        
        # Get entity
        entity = await self.repository.get_by_id(id)
        if not entity:
            self.logger.warning(f"{self.model.__name__} with ID {id} not found")
            raise ResourceNotFoundException(
                f"{self.model.__name__} not found",
                code=ErrorCode.RESOURCE_NOT_FOUND,
                details={"id": str(id)},
                status_code=404,
            )
            
        # Check permissions if user_id is provided and permission is required
        if user_id and self.required_update_permission:
            user = await self._get_user(user_id)
            if not PermissionChecker.has_permission(user, self.required_update_permission):
                self.logger.warning(
                    f"Permission denied for user {user_id} to update {self.model.__name__}"
                )
                raise PermissionDeniedException(
                    f"You don't have permission to update {self.model.__name__}",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": self.required_update_permission},
                    status_code=403,
                )
                
        # Validate update
        await self.validate_update(entity, data, user_id)
        
        # Pre-update hook
        original_entity = entity
        await self.before_update(entity, data, user_id)
        
        try:
            # Update entity
            updated_entity = await self.repository.update(id, data, user_id)
            if not updated_entity:
                raise ResourceNotFoundException(
                    f"{self.model.__name__} not found",
                    code=ErrorCode.RESOURCE_NOT_FOUND,
                    details={"id": str(id)},
                    status_code=404,
                )
                
            # Post-update hook
            await self.after_update(updated_entity, original_entity, user_id)
            
            self.logger.info(f"Updated {self.model.__name__} with ID: {id}")
            return updated_entity
        except Exception as e:
            self.logger.error(f"Error updating entity: {str(e)}")
            raise

    async def update_with_schema(
        self, 
        id: ID, 
        schema: U, 
        user_id: Optional[str] = None
    ) -> Optional[T]:
        """Update an existing entity using a Pydantic schema.

        Args:
            id: Entity ID
            schema: Update schema
            user_id: Optional user ID for permission checks

        Returns:
            Optional[T]: The updated entity if found, None otherwise
        """
        return await self.update(id, schema.dict(exclude_unset=True), user_id)

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

    async def validate_create(
        self, 
        data: Dict[str, Any], 
        user_id: Optional[str] = None
    ) -> None:
        """Validate data before creation.

        Args:
            data: Entity data
            user_id: Current user ID

        Raises:
            ValidationException: If validation fails
        """
        self.logger.debug(f"Validating create data: {data}")
        
        # Override in subclasses for custom validation
        pass

    async def validate_delete(
        self, 
        entity: T, 
        user_id: Optional[str] = None
    ) -> None:
        """Validate before deletion.

        Args:
            entity: Entity to delete
            user_id: Current user ID

        Raises:
            ValidationException: If validation fails
        """
        self.logger.debug(f"Validating delete for entity: {entity}")
        
        # Override in subclasses for custom validation
        pass

    async def validate_update(
        self, 
        entity: T, 
        data: Dict[str, Any], 
        user_id: Optional[str] = None
    ) -> None:
        """Validate data before update.

        Args:
            entity: Existing entity
            data: Updated data
            user_id: Current user ID

        Raises:
            ValidationException: If validation fails
        """
        self.logger.debug(f"Validating update data: {data} for entity: {entity}")
        
        # Override in subclasses for custom validation
        pass

    async def before_create(
        self, 
        data: Dict[str, Any], 
        user_id: Optional[str] = None
    ) -> None:
        """Hook before entity creation.

        Args:
            data: Entity data
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def after_create(
        self, 
        entity: T, 
        user_id: Optional[str] = None
    ) -> None:
        """Hook after entity creation.

        Args:
            entity: Created entity
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def before_update(
        self, 
        entity: T, 
        data: Dict[str, Any], 
        user_id: Optional[str] = None
    ) -> None:
        """Hook before entity update.

        Args:
            entity: Existing entity
            data: Updated data
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def after_update(
        self, 
        updated_entity: T, 
        original_entity: T, 
        user_id: Optional[str] = None
    ) -> None:
        """Hook after entity update.

        Args:
            updated_entity: Updated entity
            original_entity: Original entity before update
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def before_delete(
        self, 
        entity: T, 
        user_id: Optional[str] = None
    ) -> None:
        """Hook before entity deletion.

        Args:
            entity: Entity to delete
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def after_delete(
        self, 
        entity: T, 
        user_id: Optional[str] = None
    ) -> None:
        """Hook after entity deletion.

        Args:
            entity: Deleted entity
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def _get_user(self, user_id: str) -> User:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User: User model

        Raises:
            AuthenticationException: If user not found
        """
        from app.models.user import User
        
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()
        
        if not user:
            self.logger.warning(f"User with ID {user_id} not found")
            raise AuthenticationException(
                "User not found",
                code=ErrorCode.AUTHENTICATION_FAILED,
                details={"user_id": user_id},
                status_code=401,
            )
            
        return user