# /app/core/validation/db.py
from __future__ import annotations

"""Database-specific validators.

This module provides validators that require database access,
such as unique field validation.
"""

from typing import Any, Dict, List, Optional, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.validation.base import ValidationResult, Validator

logger = get_logger("app.core.validation.db")


class UniqueValidator(Validator):
    """Validator for unique field values in the database."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the unique validator.

        Args:
            db: Database session
        """
        self.db = db

    async def validate_async(
        self,
        value: Any,
        field: str,
        model: Any,
        exclude_id: Optional[str] = None,
        **kwargs: Any,
    ) -> ValidationResult:
        """Validate that a value is unique in the database.

        This is an async version needed for database operations.

        Args:
            value: The value to validate
            field: The field name to check
            model: The SQLAlchemy model class
            exclude_id: Optional ID to exclude from the check
            **kwargs: Additional validation parameters

        Returns:
            ValidationResult: The result of the validation
        """
        query = select(model).filter(getattr(model, field) == value)

        if exclude_id:
            query = query.filter(model.id != exclude_id)

        result = await self.db.execute(query)
        existing = result.first()

        if existing:
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

        return ValidationResult(is_valid=True)

    def validate(
        self,
        value: Any,
        field: str = "",
        model: Any = None,
        exclude_id: Optional[str] = None,
        **kwargs: Any,
    ) -> ValidationResult:
        """Non-async interface that's part of the Validator protocol.

        Since this validator requires async database operations,
        this method raises an exception if called directly.

        Args:
            value: The value to validate
            field: The field name to check
            model: The SQLAlchemy model class
            exclude_id: Optional ID to exclude from the check
            **kwargs: Additional validation parameters

        Raises:
            RuntimeError: Always, as this validator requires async operations
        """
        raise RuntimeError(
            "UniqueValidator requires async operations. " "Use validate_async instead."
        )
