# /app/services/base_service/contracts.py
from __future__ import annotations

"""Base contracts and protocols for service implementations.

This module defines common protocols and interfaces that all services should
implement, providing a standardized contract for CRUD operations and other
common service functionality.
"""

from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel

from app.db.base_class import Base
from app.services.interfaces import CrudServiceInterface

# Type variables
T = TypeVar("T", bound=Base)  # SQLAlchemy model type
C = TypeVar("C", bound=BaseModel)  # Create schema type
U = TypeVar("U", bound=BaseModel)  # Update schema type
R = TypeVar("R", bound=BaseModel)  # Response schema type
ID = TypeVar("ID")  # ID type


class BaseServiceProtocol(
    CrudServiceInterface[T, ID, C, U, R], Generic[T, ID, C, U, R]
):
    """Protocol defining the interface for base service functionality."""

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
        ...

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
        ...

    async def validate_delete(self, entity: T, user_id: Optional[str] = None) -> None:
        """Validate before deletion.

        Args:
            entity: Entity to delete
            user_id: Current user ID

        Raises:
            ValidationException: If validation fails
        """
        ...

    async def before_create(
        self, data: Dict[str, Any], user_id: Optional[str] = None
    ) -> None:
        """Hook before entity creation.

        Args:
            data: Entity data
            user_id: Current user ID
        """
        ...

    async def after_create(self, entity: T, user_id: Optional[str] = None) -> None:
        """Hook after entity creation.

        Args:
            entity: Created entity
            user_id: Current user ID
        """
        ...

    async def before_update(
        self, entity: T, data: Dict[str, Any], user_id: Optional[str] = None
    ) -> None:
        """Hook before entity update.

        Args:
            entity: Existing entity
            data: Updated data
            user_id: Current user ID
        """
        ...

    async def after_update(
        self, updated_entity: T, original_entity: T, user_id: Optional[str] = None
    ) -> None:
        """Hook after entity update.

        Args:
            updated_entity: Updated entity
            original_entity: Original entity before update
            user_id: Current user ID
        """
        ...

    async def before_delete(self, entity: T, user_id: Optional[str] = None) -> None:
        """Hook before entity deletion.

        Args:
            entity: Entity to delete
            user_id: Current user ID
        """
        ...

    async def after_delete(self, entity: T, user_id: Optional[str] = None) -> None:
        """Hook after entity deletion.

        Args:
            entity: Deleted entity
            user_id: Current user ID
        """
        ...
