# /app/services/base_service/service.py
from __future__ import annotations

"""Main base service implementation.

This module provides the primary BaseService that implements the CrudServiceInterface
with standardized CRUD operations, permission checking, and lifecycle hooks.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast

from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.core.logging import get_logger
from app.core.permissions import Permission
from app.db.base_class import Base
from app.repositories.base import BaseRepository
from app.schemas.pagination import (
    CursorPaginationParams,
    OffsetPaginationParams,
    PaginationResult,
)
from app.services.base_service.contracts import BaseServiceProtocol
from app.services.base_service.operations import (
    CreateUpdateOperations,
    ReadDeleteOperations,
)
from app.services.base_service.permissions import PermissionHelper
from app.services.interfaces import CrudServiceInterface
from app.services.pagination.service import PaginationService

logger = get_logger("app.services.base_service.service")

# Type variables
T = TypeVar("T", bound=Base)  # SQLAlchemy model type
C = TypeVar("C", bound=BaseModel)  # Create schema type
U = TypeVar("U", bound=BaseModel)  # Update schema type
R = TypeVar("R", bound=BaseModel)  # Response schema type
ID = TypeVar("ID")  # ID type


class BaseService(Generic[T, C, U, R, ID], BaseServiceProtocol[T, ID, C, U, R]):
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

        # Initialize operations
        self.create_update_ops = CreateUpdateOperations[T, C, U, ID]()
        self.read_delete_ops = ReadDeleteOperations[T, R, ID]()

        # Initialize pagination service
        self.pagination_service = PaginationService[T, R](
            db, model_class, response_schema
        )

        # Set logger context
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
        return await self.create_update_ops.create(
            db=self.db,
            repository=self.repository,
            data=data,
            user_id=user_id,
            required_permission=self.required_create_permission,
            validate_func=self.validate_create,
            before_func=self.before_create,
            after_func=self.after_create,
            get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id),
        )

    async def create_with_schema(self, schema: C, user_id: Optional[str] = None) -> T:
        """Create a new entity using a Pydantic schema.

        Args:
            schema: Create schema
            user_id: Optional user ID for permission checks

        Returns:
            T: The created entity
        """
        return await self.create_update_ops.create_with_schema(
            db=self.db,
            repository=self.repository,
            schema=schema,
            user_id=user_id,
            required_permission=self.required_create_permission,
            validate_func=self.validate_create,
            before_func=self.before_create,
            after_func=self.after_create,
            get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id),
        )

    async def delete(
        self, id: ID, user_id: Optional[str] = None, hard_delete: bool = False
    ) -> bool:
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
        return await self.read_delete_ops.delete(
            db=self.db,
            repository=self.repository,
            id=id,
            user_id=user_id,
            hard_delete=hard_delete,
            required_permission=self.required_delete_permission,
            validate_func=self.validate_delete,
            before_func=self.before_delete,
            after_func=self.after_delete,
            get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id),
        )

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
        return await self.read_delete_ops.get(
            db=self.db,
            repository=self.repository,
            id=id,
            user_id=user_id,
            required_permission=self.required_read_permission,
            get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id),
        )

    async def get_by_id(self, id: ID, user_id: Optional[str] = None) -> Optional[T]:
        """Get entity by ID without raising exceptions.

        Args:
            id: Entity ID
            user_id: Current user ID

        Returns:
            Optional[T]: Entity or None if not found
        """
        return await self.read_delete_ops.get_by_id(
            db=self.db,
            repository=self.repository,
            id=id,
            user_id=user_id,
            required_permission=self.required_read_permission,
            get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id),
        )

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
        return await self.read_delete_ops.get_multi(
            db=self.db,
            repository=self.repository,
            user_id=user_id,
            page=page,
            page_size=page_size,
            filters=filters,
            order_by=order_by,
            required_permission=self.required_read_permission,
            get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id),
            apply_filters_func=self.apply_filters,
        )

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
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
        return await self.get_multi(
            user_id=user_id, page=page, page_size=page_size, filters=filters
        )

    async def update(
        self, id: ID, data: Dict[str, Any], user_id: Optional[str] = None
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
        return await self.create_update_ops.update(
            db=self.db,
            repository=self.repository,
            id=id,
            data=data,
            user_id=user_id,
            required_permission=self.required_update_permission,
            validate_func=self.validate_update,
            before_func=self.before_update,
            after_func=self.after_update,
            get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id),
        )

    async def update_with_schema(
        self, id: ID, schema: U, user_id: Optional[str] = None
    ) -> Optional[T]:
        """Update an existing entity using a Pydantic schema.

        Args:
            id: Entity ID
            schema: Update schema
            user_id: Optional user ID for permission checks

        Returns:
            Optional[T]: The updated entity if found, None otherwise
        """
        return await self.create_update_ops.update_with_schema(
            db=self.db,
            repository=self.repository,
            id=id,
            schema=schema,
            user_id=user_id,
            required_permission=self.required_update_permission,
            validate_func=self.validate_update,
            before_func=self.before_update,
            after_func=self.after_update,
            get_user_func=lambda user_id: PermissionHelper.get_user(self.db, user_id),
        )

    async def get_paginated(
        self,
        user_id: Optional[str],
        params: OffsetPaginationParams,
        filters: Optional[Dict[str, Any]] = None,
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
        # Check permissions
        if user_id and self.required_read_permission:
            user = await PermissionHelper.get_user(self.db, user_id)
            if not hasattr(user, "has_permission") or not user.has_permission(
                self.required_read_permission
            ):
                self.logger.warning(
                    f"Permission denied for user {user_id} to list {self.model.__name__}"
                )
                raise PermissionDeniedException(
                    f"You don't have permission to list {self.model.__name__}",
                    code="PERMISSION_DENIED",
                    details={"required_permission": self.required_read_permission},
                    status_code=403,
                )

        # Apply filters
        applied_filters = filters or {}
        applied_filters = await self.apply_filters(applied_filters, user_id)

        # Build query
        query = self.repository.build_query(applied_filters)

        # Get paginated results
        return await self.pagination_service.paginate_with_offset(
            query, params, self.to_response
        )

    async def get_paginated_with_cursor(
        self,
        user_id: Optional[str],
        params: CursorPaginationParams,
        filters: Optional[Dict[str, Any]] = None,
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
        # Check permissions
        if user_id and self.required_read_permission:
            user = await PermissionHelper.get_user(self.db, user_id)
            if not hasattr(user, "has_permission") or not user.has_permission(
                self.required_read_permission
            ):
                self.logger.warning(
                    f"Permission denied for user {user_id} to list {self.model.__name__}"
                )
                raise PermissionDeniedException(
                    f"You don't have permission to list {self.model.__name__}",
                    code="PERMISSION_DENIED",
                    details={"required_permission": self.required_read_permission},
                    status_code=403,
                )

        # Apply filters
        applied_filters = filters or {}
        applied_filters = await self.apply_filters(applied_filters, user_id)

        # Build query
        query = self.repository.build_query(applied_filters)

        # Get paginated results
        return await self.pagination_service.paginate_with_cursor(
            query, params, self.to_response
        )

    async def to_response(self, entity: T) -> R:
        """Convert entity to response model.

        Args:
            entity: Entity to convert

        Returns:
            R: Response model
        """
        return await self.read_delete_ops.to_response(entity, self.response_schema)

    async def to_response_multi(self, entities: List[T]) -> List[R]:
        """Convert multiple entities to response models.

        Args:
            entities: Entities to convert

        Returns:
            List[R]: Response models
        """
        return await self.read_delete_ops.to_response_multi(
            entities, self.response_schema
        )

    async def apply_filters(
        self, filters: Dict[str, Any], user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Apply custom filters based on business logic.

        This method can be overridden in subclasses to add additional filters
        based on the user, entity type, or other business rules.

        Args:
            filters: Base filters to apply
            user_id: Current user ID

        Returns:
            Dict[str, Any]: Updated filters
        """
        # Default implementation returns filters unchanged
        return filters

    # Validation hooks - override in subclasses

    async def validate_create(
        self, data: Dict[str, Any], user_id: Optional[str] = None
    ) -> None:
        """Validate data before creation.

        Args:
            data: Entity data
            user_id: Current user ID

        Raises:
            ValidationException: If validation fails
        """
        # Override in subclasses for custom validation
        pass

    async def validate_update(
        self, entity: T, data: Dict[str, Any], user_id: Optional[str] = None
    ) -> None:
        """Validate data before update.

        Args:
            entity: Existing entity
            data: Updated data
            user_id: Current user ID

        Raises:
            ValidationException: If validation fails
        """
        # Override in subclasses for custom validation
        pass

    async def validate_delete(self, entity: T, user_id: Optional[str] = None) -> None:
        """Validate before deletion.

        Args:
            entity: Entity to delete
            user_id: Current user ID

        Raises:
            ValidationException: If validation fails
        """
        # Override in subclasses for custom validation
        pass

    # Lifecycle hooks - override in subclasses

    async def before_create(
        self, data: Dict[str, Any], user_id: Optional[str] = None
    ) -> None:
        """Hook before entity creation.

        Args:
            data: Entity data
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def after_create(self, entity: T, user_id: Optional[str] = None) -> None:
        """Hook after entity creation.

        Args:
            entity: Created entity
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def before_update(
        self, entity: T, data: Dict[str, Any], user_id: Optional[str] = None
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
        self, updated_entity: T, original_entity: T, user_id: Optional[str] = None
    ) -> None:
        """Hook after entity update.

        Args:
            updated_entity: Updated entity
            original_entity: Original entity before update
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def before_delete(self, entity: T, user_id: Optional[str] = None) -> None:
        """Hook before entity deletion.

        Args:
            entity: Entity to delete
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass

    async def after_delete(self, entity: T, user_id: Optional[str] = None) -> None:
        """Hook after entity deletion.

        Args:
            entity: Deleted entity
            user_id: Current user ID
        """
        # Override in subclasses for custom logic
        pass
