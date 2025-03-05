from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, func, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Base class for all database models.

    Attributes:
        id: Primary key
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.

        Returns:
            Dictionary representation of model
        """
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
