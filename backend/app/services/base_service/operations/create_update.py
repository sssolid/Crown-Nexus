# /app/services/base_service/operations/create_update.py
from __future__ import annotations

"""Create and update operations for the base service.

This module provides functionality for creating and updating entities,
with support for validation, permission checking, and hooks.
"""

from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    ErrorCode,
    PermissionDeniedException,
    ResourceNotFoundException,
)
from app.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import transactional

logger = get_logger("app.services.base_service.operations.create_update")

# Type variables
T = TypeVar("T", bound=Base)  # SQLAlchemy model type
C = TypeVar("C", bound=BaseModel)  # Create schema type
U = TypeVar("U", bound=BaseModel)  # Update schema type
ID = TypeVar("ID")  # ID type


class CreateUpdateOperations(Generic[T, C, U, ID]):
    """Operations for creating and updating entities."""

    @transactional
    async def create(
        self,
        db: AsyncSession,
        repository: Any,
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        required_permission: Optional[Permission] = None,
        validate_func: Optional[callable] = None,
        before_func: Optional[callable] = None,
        after_func: Optional[callable] = None,
        get_user_func: Optional[callable] = None,
    ) -> T:
        """Create new entity.

        Args:
            db: Database session
            repository: Repository for database operations
            data: Entity data
            user_id: Current user ID
            required_permission: Required permission for this operation
            validate_func: Function for validating the data
            before_func: Function to call before creation
            after_func: Function to call after creation
            get_user_func: Function to get user by ID

        Returns:
            T: Created entity

        Raises:
            ValidationException: If validation fails
            PermissionDeniedException: If user doesn't have permission
        """
        logger.debug(f"Creating entity with data: {data}")

        # Check permissions if user_id is provided and permission is required
        if user_id and required_permission and get_user_func:
            user = await get_user_func(user_id)
            if not PermissionChecker.has_permission(user, required_permission):
                logger.warning(f"Permission denied for user {user_id} to create entity")
                raise PermissionDeniedException(
                    f"You don't have permission to create this entity",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": required_permission},
                    status_code=403,
                )

        # Validate data
        if validate_func:
            await validate_func(data, user_id)

        # Pre-create hook
        if before_func:
            await before_func(data, user_id)

        try:
            # Create entity
            entity = await repository.create(data)

            # Post-create hook
            if after_func:
                await after_func(entity, user_id)

            logger.info(f"Created entity with ID: {getattr(entity, 'id', None)}")
            return entity
        except Exception as e:
            logger.error(f"Error creating entity: {str(e)}")
            raise

    async def create_with_schema(
        self,
        db: AsyncSession,
        repository: Any,
        schema: C,
        user_id: Optional[str] = None,
        required_permission: Optional[Permission] = None,
        validate_func: Optional[callable] = None,
        before_func: Optional[callable] = None,
        after_func: Optional[callable] = None,
        get_user_func: Optional[callable] = None,
    ) -> T:
        """Create a new entity using a Pydantic schema.

        Args:
            db: Database session
            repository: Repository for database operations
            schema: Create schema
            user_id: Optional user ID for permission checks
            required_permission: Required permission for this operation
            validate_func: Function for validating the data
            before_func: Function to call before creation
            after_func: Function to call after creation
            get_user_func: Function to get user by ID

        Returns:
            T: The created entity
        """
        return await self.create(
            db=db,
            repository=repository,
            data=schema.model_dump(),
            user_id=user_id,
            required_permission=required_permission,
            validate_func=validate_func,
            before_func=before_func,
            after_func=after_func,
            get_user_func=get_user_func,
        )

    @transactional
    async def update(
        self,
        db: AsyncSession,
        repository: Any,
        id: ID,
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        required_permission: Optional[Permission] = None,
        validate_func: Optional[callable] = None,
        before_func: Optional[callable] = None,
        after_func: Optional[callable] = None,
        get_user_func: Optional[callable] = None,
    ) -> T:
        """Update entity.

        Args:
            db: Database session
            repository: Repository for database operations
            id: Entity ID
            data: Updated data
            user_id: Current user ID
            required_permission: Required permission for this operation
            validate_func: Function for validating the data
            before_func: Function to call before update
            after_func: Function to call after update
            get_user_func: Function to get user by ID

        Returns:
            T: Updated entity

        Raises:
            ResourceNotFoundException: If entity not found
            ValidationException: If validation fails
            PermissionDeniedException: If user doesn't have permission
        """
        logger.debug(f"Updating entity with ID: {id}, data: {data}")

        # Get entity
        entity = await repository.get_by_id(id)
        if not entity:
            logger.warning(f"Entity with ID {id} not found")
            raise ResourceNotFoundException(
                f"Entity not found",
                code=ErrorCode.RESOURCE_NOT_FOUND,
                details={"id": str(id)},
                status_code=404,
            )

        # Check permissions if user_id is provided and permission is required
        if user_id and required_permission and get_user_func:
            user = await get_user_func(user_id)
            if not PermissionChecker.has_permission(user, required_permission):
                logger.warning(f"Permission denied for user {user_id} to update entity")
                raise PermissionDeniedException(
                    f"You don't have permission to update this entity",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": required_permission},
                    status_code=403,
                )

        # Validate update
        if validate_func:
            await validate_func(entity, data, user_id)

        # Pre-update hook
        original_entity = entity
        if before_func:
            await before_func(entity, data, user_id)

        try:
            # Update entity
            updated_entity = await repository.update(id, data, user_id)
            if not updated_entity:
                raise ResourceNotFoundException(
                    f"Entity not found",
                    code=ErrorCode.RESOURCE_NOT_FOUND,
                    details={"id": str(id)},
                    status_code=404,
                )

            # Post-update hook
            if after_func:
                await after_func(updated_entity, original_entity, user_id)

            logger.info(f"Updated entity with ID: {id}")
            return updated_entity
        except Exception as e:
            logger.error(f"Error updating entity: {str(e)}")
            raise

    async def update_with_schema(
        self,
        db: AsyncSession,
        repository: Any,
        id: ID,
        schema: U,
        user_id: Optional[str] = None,
        required_permission: Optional[Permission] = None,
        validate_func: Optional[callable] = None,
        before_func: Optional[callable] = None,
        after_func: Optional[callable] = None,
        get_user_func: Optional[callable] = None,
    ) -> Optional[T]:
        """Update an existing entity using a Pydantic schema.

        Args:
            db: Database session
            repository: Repository for database operations
            id: Entity ID
            schema: Update schema
            user_id: Optional user ID for permission checks
            required_permission: Required permission for this operation
            validate_func: Function for validating the data
            before_func: Function to call before update
            after_func: Function to call after update
            get_user_func: Function to get user by ID

        Returns:
            Optional[T]: The updated entity if found, None otherwise
        """
        return await self.update(
            db=db,
            repository=repository,
            id=id,
            data=schema.model_dump(exclude_unset=True),
            user_id=user_id,
            required_permission=required_permission,
            validate_func=validate_func,
            before_func=before_func,
            after_func=after_func,
            get_user_func=get_user_func,
        )
