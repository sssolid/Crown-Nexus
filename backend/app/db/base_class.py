# backend/app/db/base_class.py
"""
SQLAlchemy base model class.

This module defines the base SQLAlchemy model class used throughout the application.
It provides common functionality for all models, including automatic table name
generation, JSON serialization, and helper methods.

All application models should inherit from this Base class to ensure consistent
behavior and maintain compatibility with migrations.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy import Column, DateTime, inspect, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.expression import Select

# Create a type variable for the Base class for type hinting
T = TypeVar('T', bound='Base')


class Base(DeclarativeBase):
    """
    Base class for all database models.

    This class provides common functionality for all models, including:
    - Automatic table name generation
    - JSON serialization via the dict() method
    - Common field definitions like id, created_at, updated_at
    - Helper methods for common query operations

    All models should inherit from this class rather than defining
    their own Base class or using SQLAlchemy's declarative_base directly.
    """

    # Define common columns that should be available to all models
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Generate __tablename__ automatically based on class name
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name automatically from class name.

        The generated name is the lowercase version of the class name.

        Returns:
            str: Table name
        """
        return cls.__name__.lower()

    def dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.

        This method is useful for API responses and JSON serialization.
        It uses SQLAlchemy's inspection capabilities to convert all column
        attributes to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of model
        """
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    @classmethod
    def filter_by_id(cls: Type[T], id: uuid.UUID) -> Select:
        """
        Create a query to filter by id.

        Args:
            id: UUID primary key to filter by

        Returns:
            Select: SQLAlchemy select statement filtered by id
        """
        from sqlalchemy import select
        return select(cls).where(cls.id == id)

    def update(self, **kwargs: Any) -> None:
        """
        Update model attributes from keyword arguments.

        Args:
            **kwargs: Attributes to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
