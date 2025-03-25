from __future__ import annotations

"""Model mapping definition.

This module defines the ModelMapping model for translation between
different vehicle model naming systems.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class ModelMapping(Base):
    """Model mapping entity for vehicle model translation.

    Attributes:
        id: Unique auto-incrementing identifier.
        pattern: Pattern to match in vehicle text.
        mapping: Mapping in format 'Make|VehicleCode|Model'.
        priority: Priority for mapping (higher values are processed first).
        active: Whether this mapping is active.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "model_mapping"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pattern: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mapping: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """Return string representation of ModelMapping instance.

        Returns:
            String representation including id, pattern, and mapping.
        """
        return f"<ModelMapping(id={self.id}, pattern='{self.pattern}', mapping='{self.mapping}')>"

    @property
    def make(self) -> str:
        """Get the make part of the mapping.

        Returns:
            The make value or empty string if not available.
        """
        parts = self.mapping.split("|")
        return parts[0] if len(parts) > 0 else ""

    @property
    def vehicle_code(self) -> str:
        """Get the vehicle code part of the mapping.

        Returns:
            The vehicle code value or empty string if not available.
        """
        parts = self.mapping.split("|")
        return parts[1] if len(parts) > 1 else ""

    @property
    def model(self) -> str:
        """Get the model part of the mapping.

        Returns:
            The model value or empty string if not available.
        """
        parts = self.mapping.split("|")
        return parts[2] if len(parts) > 2 else ""
