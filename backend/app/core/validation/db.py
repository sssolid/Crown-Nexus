from __future__ import annotations

"""Database-specific validators.

This module provides validators that require database access,
such as unique field validation.
"""

from typing import Any, Dict, List, Optional, Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.core.validation.base import ValidationResult, Validator

logger = get_logger("app.core.validation.db")


class UniqueValidator(Validator):
    """Validator that checks if a value is unique in the database.

    This validator requires an async database session and must be used
    with the validate_async method.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the unique validator.

        Args:
            db: The SQLAlchemy async database session
        """
        self.db = db

    async def validate_async(
        self,
        value: Any,
        field: str,
        model: Any,
        exclude_id: Optional[str] = None,
        **kwargs: Any
    ) -> ValidationResult:
        """Asynchronously validate that a value is unique in the database.

        Args:
            value: The value to check for uniqueness
            field: The field name in the model
            model: The SQLAlchemy model class
            exclude_id: Optional ID to exclude from the uniqueness check
            **kwargs: Additional keyword arguments

        Returns:
            ValidationResult: The validation result
        """
        logger.debug(
            f"Checking uniqueness of '{field}' in {model.__name__}",
            field=field,
            value=value,
            model=model.__name__,
            exclude_id=exclude_id,
        )

        query = select(model).filter(getattr(model, field) == value)

        if exclude_id:
            query = query.filter(model.id != exclude_id)

        result = await self.db.execute(query)
        existing = result.first()

        if existing:
            logger.debug(
                f"Value '{value}' already exists for field '{field}' in {model.__name__}",
                field=field,
                value=value,
                model=model.__name__,
            )
            return ValidationResult(
                is_valid=False,
                errors=[
                    {
                        "msg": f"Value '{value}' already exists for field '{field}'",
                        "type": "unique_error",
                        "field": field,
                        "value": value,
                    }
                ],
            )

        logger.debug(
            f"Value '{value}' is unique for field '{field}' in {model.__name__}",
            field=field,
            value=value,
            model=model.__name__,
        )
        return ValidationResult(is_valid=True)

    def validate(
        self,
        value: Any,
        field: str = "",
        model: Any = None,
        exclude_id: Optional[str] = None,
        **kwargs: Any
    ) -> ValidationResult:
        """Synchronous validation method - not supported.

        Raises:
            ValidationException: Always, as this validator requires async operations
        """
        error_msg = "UniqueValidator requires async operations. Use validate_async instead."
        logger.error(error_msg)
        raise ValidationException(
            "Validation method error",
            errors=[
                {
                    "loc": ["method", "validate"],
                    "msg": error_msg,
                    "type": "method_error.async_required",
                    "hint": "Use 'await validator.validate_async()' instead of 'validator.validate()'",
                }
            ],
        )
