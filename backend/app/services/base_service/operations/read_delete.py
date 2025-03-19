# /app/services/base_service/operations/read_delete.py
from __future__ import annotations

"""Read and delete operations for the base service.

This module provides functionality for reading and deleting entities,
with support for permission checking, filtering, and hooks.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    ErrorCode,
    PermissionDeniedException,
    ResourceNotFoundException,
)
from app.core.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import transactional

logger = get_logger("app.services.base_service.operations.read_delete")

# Type variables
T = TypeVar("T", bound=Base)  # SQLAlchemy model type
R = TypeVar("R", bound=BaseModel)  # Response schema type
ID = TypeVar("ID")  # ID type


class ReadDeleteOperations(Generic[T, R, ID]):
    """Operations for reading and deleting entities."""

    @transactional
    async def get(
        self,
        db: AsyncSession,
        repository: Any,
        id: ID,
        user_id: Optional[str] = None,
        required_permission: Optional[Permission] = None,
        get_user_func: Optional[callable] = None,
    ) -> T:
        """Get entity by ID with permission check.

        Args:
            db: Database session
            repository: Repository for database operations
            id: Entity ID
            user_id: Current user ID
            required_permission: Required permission for this operation
            get_user_func: Function to get user by ID

        Returns:
            T: Entity

        Raises:
            ResourceNotFoundException: If entity not found
            PermissionDeniedException: If user doesn't have permission
        """
        logger.debug(f"Getting entity with ID: {id}")

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
                logger.warning(f"Permission denied for user {user_id} to read entity")
                raise PermissionDeniedException(
                    f"You don't have permission to read this entity",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": required_permission},
                    status_code=403,
                )

        logger.debug(f"Found entity with ID: {id}")
        return entity

    async def get_by_id(
        self,
        db: AsyncSession,
        repository: Any,
        id: ID,
        user_id: Optional[str] = None,
        required_permission: Optional[Permission] = None,
        get_user_func: Optional[callable] = None,
    ) -> Optional[T]:
        """Get entity by ID without raising exceptions.

        Args:
            db: Database session
            repository: Repository for database operations
            id: Entity ID
            user_id: Current user ID
            required_permission: Required permission for this operation
            get_user_func: Function to get user by ID

        Returns:
            Optional[T]: Entity or None if not found
        """
        try:
            return await self.get(
                db=db,
                repository=repository,
                id=id,
                user_id=user_id,
                required_permission=required_permission,
                get_user_func=get_user_func,
            )
        except ResourceNotFoundException:
            return None
        except PermissionDeniedException:
            return None

    @transactional
    async def get_multi(
        self,
        db: AsyncSession,
        repository: Any,
        user_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        required_permission: Optional[Permission] = None,
        get_user_func: Optional[callable] = None,
        apply_filters_func: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """Get multiple entities with pagination.

        Args:
            db: Database session
            repository: Repository for database operations
            user_id: Current user ID
            page: Page number
            page_size: Items per page
            filters: Filters to apply
            order_by: Field to order by
            required_permission: Required permission for this operation
            get_user_func: Function to get user by ID
            apply_filters_func: Function to apply custom filters

        Returns:
            Dict[str, Any]: Paginated results

        Raises:
            PermissionDeniedException: If user doesn't have permission
        """
        logger.debug(
            f"Getting entities with page={page}, page_size={page_size}, filters={filters}"
        )

        # Check permissions if user_id is provided and permission is required
        if user_id and required_permission and get_user_func:
            user = await get_user_func(user_id)
            if not PermissionChecker.has_permission(user, required_permission):
                logger.warning(f"Permission denied for user {user_id} to list entities")
                raise PermissionDeniedException(
                    f"You don't have permission to list entities",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": required_permission},
                    status_code=403,
                )

        # Apply custom filters
        applied_filters = filters or {}
        if apply_filters_func:
            applied_filters = await apply_filters_func(applied_filters, user_id)

        try:
            # Get paginated results
            result = await repository.get_all(
                page=page,
                page_size=page_size,
                order_by=order_by,
                filters=applied_filters,
            )

            logger.debug(f"Found {result.get('total', 0)} entities")
            return result
        except Exception as e:
            logger.error(f"Error getting entities: {str(e)}")
            raise

    async def get_all(
        self,
        db: AsyncSession,
        repository: Any,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        required_permission: Optional[Permission] = None,
        get_user_func: Optional[callable] = None,
        apply_filters_func: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """Get all entities with pagination.

        Args:
            db: Database session
            repository: Repository for database operations
            page: Page number (1-indexed)
            page_size: Number of items per page
            filters: Optional filters to apply
            user_id: Optional user ID for permission checks
            required_permission: Required permission for this operation
            get_user_func: Function to get user by ID
            apply_filters_func: Function to apply custom filters

        Returns:
            Dict[str, Any]: Paginated results
        """
        return await self.get_multi(
            db=db,
            repository=repository,
            user_id=user_id,
            page=page,
            page_size=page_size,
            filters=filters,
            required_permission=required_permission,
            get_user_func=get_user_func,
            apply_filters_func=apply_filters_func,
        )

    async def to_response(self, entity: T, response_model: Type[R]) -> R:
        """Convert entity to response model.

        Args:
            entity: Entity to convert
            response_model: Response model class

        Returns:
            R: Response model
        """
        return response_model.from_orm(entity)

    async def to_response_multi(
        self, entities: List[T], response_model: Type[R]
    ) -> List[R]:
        """Convert multiple entities to response models.

        Args:
            entities: Entities to convert
            response_model: Response model class

        Returns:
            List[R]: Response models
        """
        return [await self.to_response(entity, response_model) for entity in entities]

    @transactional
    async def delete(
        self,
        db: AsyncSession,
        repository: Any,
        id: ID,
        user_id: Optional[str] = None,
        hard_delete: bool = False,
        required_permission: Optional[Permission] = None,
        validate_func: Optional[callable] = None,
        before_func: Optional[callable] = None,
        after_func: Optional[callable] = None,
        get_user_func: Optional[callable] = None,
    ) -> bool:
        """Delete entity.

        Args:
            db: Database session
            repository: Repository for database operations
            id: Entity ID
            user_id: Current user ID
            hard_delete: Whether to permanently delete
            required_permission: Required permission for this operation
            validate_func: Function for validating the deletion
            before_func: Function to call before deletion
            after_func: Function to call after deletion
            get_user_func: Function to get user by ID

        Returns:
            bool: True if deleted

        Raises:
            ResourceNotFoundException: If entity not found
            PermissionDeniedException: If user doesn't have permission
        """
        logger.debug(f"Deleting entity with ID: {id}")

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
                logger.warning(f"Permission denied for user {user_id} to delete entity")
                raise PermissionDeniedException(
                    f"You don't have permission to delete this entity",
                    code=ErrorCode.PERMISSION_DENIED,
                    details={"required_permission": required_permission},
                    status_code=403,
                )

        # Validate delete
        if validate_func:
            await validate_func(entity, user_id)

        # Pre-delete hook
        if before_func:
            await before_func(entity, user_id)

        try:
            # Delete entity
            result = await repository.delete(id, user_id, hard_delete)

            # Post-delete hook
            if after_func:
                await after_func(entity, user_id)

            logger.info(f"Deleted entity with ID: {id}")
            return result
        except Exception as e:
            logger.error(f"Error deleting entity: {str(e)}")
            raise
