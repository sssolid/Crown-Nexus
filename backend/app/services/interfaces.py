# /backend/app/services/interfaces.py
from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar

T = TypeVar("T")  # Entity type
ID = TypeVar("ID")  # ID type
C = TypeVar("C")  # Create schema type
U = TypeVar("U")  # Update schema type
R = TypeVar("R")  # Response schema type


class ServiceInterface(Protocol, Generic[T, ID]):
    """Base protocol for all services.

    This protocol defines the standard interface that all services must implement.
    """

    async def initialize(self) -> None:
        """Initialize service resources.

        This method should be called during application startup to initialize
        any resources needed by the service.
        """
        ...

    async def shutdown(self) -> None:
        """Release service resources.

        This method should be called during application shutdown to release
        any resources held by the service.
        """
        ...

    async def get_by_id(self, id: ID, user_id: Optional[str] = None) -> Optional[T]:
        """Get entity by ID.

        Args:
            id: Entity ID
            user_id: Optional user ID for permission checks

        Returns:
            Optional[T]: The entity if found, None otherwise
        """
        ...

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
        ...

    async def create(self, data: Dict[str, Any], user_id: Optional[str] = None) -> T:
        """Create a new entity.

        Args:
            data: Entity data
            user_id: Optional user ID for permission checks

        Returns:
            T: The created entity
        """
        ...

    async def update(
        self, id: ID, data: Dict[str, Any], user_id: Optional[str] = None
    ) -> Optional[T]:
        """Update an existing entity.

        Args:
            id: Entity ID
            data: Updated entity data
            user_id: Optional user ID for permission checks

        Returns:
            Optional[T]: The updated entity if found, None otherwise
        """
        ...

    async def delete(self, id: ID, user_id: Optional[str] = None) -> bool:
        """Delete an entity.

        Args:
            id: Entity ID
            user_id: Optional user ID for permission checks

        Returns:
            bool: True if the entity was deleted, False otherwise
        """
        ...


class CrudServiceInterface(ServiceInterface[T, ID], Generic[T, ID, C, U, R]):
    """Extended interface for CRUD services with schema validation.

    This interface extends the base service interface with methods that use
    Pydantic models for validation.
    """

    async def create_with_schema(self, schema: C, user_id: Optional[str] = None) -> T:
        """Create a new entity using a Pydantic schema.

        Args:
            schema: Create schema
            user_id: Optional user ID for permission checks

        Returns:
            T: The created entity
        """
        ...

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
        ...

    async def to_response(self, entity: T) -> R:
        """Convert entity to response schema.

        Args:
            entity: Entity to convert

        Returns:
            R: Response schema
        """
        ...

    async def to_response_multi(self, entities: List[T]) -> List[R]:
        """Convert entities to response schemas.

        Args:
            entities: Entities to convert

        Returns:
            List[R]: Response schemas
        """
        ...


class ReadOnlyServiceInterface(ServiceInterface[T, ID], Generic[T, ID, R]):
    """Interface for read-only services.

    This interface provides only read operations, useful for services
    that don't need to modify data.
    """

    async def to_response(self, entity: T) -> R:
        """Convert entity to response schema.

        Args:
            entity: Entity to convert

        Returns:
            R: Response schema
        """
        ...

    async def to_response_multi(self, entities: List[T]) -> List[R]:
        """Convert entities to response schemas.

        Args:
            entities: Entities to convert

        Returns:
            List[R]: Response schemas
        """
        ...
