# /app/services/pagination/service.py
from __future__ import annotations

"""Main pagination service implementation.

This module provides the primary PaginationService that coordinates pagination
operations for different entity types and pagination strategies.
"""

from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select

from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.db.base_class import Base
from app.services.interfaces import ServiceInterface
from app.services.pagination.base import (
    CursorPaginationParams,
    OffsetPaginationParams,
    PaginationProvider,
    PaginationResult,
)
from app.services.pagination.factory import PaginationProviderFactory

logger = get_logger("app.services.pagination.service")

T = TypeVar("T", bound=Base)  # SQLAlchemy model type
ID = TypeVar("ID")
R = TypeVar("R", bound=BaseModel)  # Pydantic response type


class PaginationService(ServiceInterface[T, ID], Generic[T, ID, R]):
    """Service for handling pagination of query results.

    This service supports both offset-based and cursor-based pagination
    and provides a unified interface for paginating different entity types.
    """

    def __init__(
        self,
        db: AsyncSession,
        model_class: Type[T],
        response_model: Optional[Type[R]] = None,
    ) -> None:
        """Initialize the pagination service.

        Args:
            db: Database session
            model_class: SQLAlchemy model class
            response_model: Optional Pydantic response model for transforming results
        """
        self.db = db
        self.model_class = model_class
        self.response_model = response_model
        self.factory = PaginationProviderFactory[T, R]()
        self.logger = logger

    async def initialize(self) -> None:
        """Initialize the pagination service."""
        self.logger.debug("Initializing pagination service")

    async def shutdown(self) -> None:
        """Shutdown the pagination service."""
        self.logger.debug("Shutting down pagination service")

    async def paginate_with_offset(
        self,
        query: Select,
        params: OffsetPaginationParams,
        transform_func: Optional[Callable[[T], R]] = None,
    ) -> PaginationResult[R]:
        """Paginate query results using offset-based pagination.

        Args:
            query: SQLAlchemy select query
            params: Pagination parameters
            transform_func: Optional function to transform each result item

        Returns:
            Paginated results

        Raises:
            ValidationException: If pagination parameters are invalid
        """
        try:
            # Create offset pagination provider
            provider = self.factory.create_provider(
                "offset", self.db, self.model_class, self.response_model
            )

            # Determine transform function
            transform = transform_func
            if transform is None and self.response_model is not None:
                transform = self._create_default_transform_func()

            # Execute pagination
            result = await provider.paginate_with_offset(query, params, transform)

            self.logger.debug(
                f"Offset pagination for {self.model_class.__name__} completed",
                page=params.page,
                page_size=params.page_size,
                total=result.total,
                items_count=len(result.items),
            )

            return result

        except Exception as e:
            if isinstance(e, ValidationException):
                raise

            self.logger.error(
                f"Offset pagination failed: {str(e)}",
                model=self.model_class.__name__,
                params=params.model_dump(),
                exc_info=True,
            )

            raise ValidationException(
                message=f"Pagination failed: {str(e)}",
                details=[
                    {"loc": ["pagination"], "msg": str(e), "type": "pagination_error"}
                ],
            )

    async def paginate_with_cursor(
        self,
        query: Select,
        params: CursorPaginationParams,
        transform_func: Optional[Callable[[T], R]] = None,
    ) -> PaginationResult[R]:
        """Paginate query results using cursor-based pagination.

        Args:
            query: SQLAlchemy select query
            params: Pagination parameters
            transform_func: Optional function to transform each result item

        Returns:
            Paginated results

        Raises:
            ValidationException: If pagination parameters are invalid
        """
        try:
            # Create cursor pagination provider
            provider = self.factory.create_provider(
                "cursor", self.db, self.model_class, self.response_model
            )

            # Determine transform function
            transform = transform_func
            if transform is None and self.response_model is not None:
                transform = self._create_default_transform_func()

            # Execute pagination
            result = await provider.paginate_with_cursor(query, params, transform)

            self.logger.debug(
                f"Cursor pagination for {self.model_class.__name__} completed",
                cursor=bool(params.cursor),
                limit=params.limit,
                total=result.total,
                items_count=len(result.items),
                has_next=result.has_next,
            )

            return result

        except Exception as e:
            if isinstance(e, ValidationException):
                raise

            self.logger.error(
                f"Cursor pagination failed: {str(e)}",
                model=self.model_class.__name__,
                params=params.model_dump(),
                exc_info=True,
            )

            raise ValidationException(
                message=f"Pagination failed: {str(e)}",
                details=[
                    {"loc": ["pagination"], "msg": str(e), "type": "pagination_error"}
                ],
            )

    def _create_default_transform_func(self) -> Callable[[T], R]:
        """Create a default transform function using the response model.

        Returns:
            Function to transform database models to response models
        """
        if self.response_model is None:
            raise ValueError(
                "Response model is required for default transform function"
            )

        def transform(item: T) -> R:
            # Check if the response model has a from_orm method
            if hasattr(self.response_model, "from_orm"):
                return self.response_model.from_orm(item)
            else:
                # Fallback for models without from_orm
                return self.response_model(**item.__dict__)

        return transform
