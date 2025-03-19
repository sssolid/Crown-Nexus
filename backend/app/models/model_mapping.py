"""
Model mapping database model.

This module defines the model mapping database model for storing
mappings between part application text patterns and structured vehicle data.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class ModelMapping(Base):
    """
    Model mapping database model.

    This model stores mappings between part application text patterns
    and structured make/model data in the format "Make|VehicleCode|Model".
    """

    __tablename__ = "model_mappings"

    # Use integer primary key instead of UUID for simplicity and better performance
    id = Column(Integer, primary_key=True, autoincrement=True)
    pattern = Column(String(255), nullable=False, index=True)
    mapping = Column(String(255), nullable=False)
    priority = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """Return string representation of model mapping."""
        return f"<ModelMapping(id={self.id}, pattern='{self.pattern}', mapping='{self.mapping}')>"

    @property
    def make(self) -> str:
        """Extract make from mapping string."""
        parts = self.mapping.split("|")
        return parts[0] if len(parts) > 0 else ""

    @property
    def vehicle_code(self) -> str:
        """Extract vehicle code from mapping string."""
        parts = self.mapping.split("|")
        return parts[1] if len(parts) > 1 else ""

    @property
    def model(self) -> str:
        """Extract model from mapping string."""
        parts = self.mapping.split("|")
        return parts[2] if len(parts) > 2 else ""
