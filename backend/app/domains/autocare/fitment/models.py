from __future__ import annotations

"""Fitment mapping models.

This module defines models for mapping local product fitments to VCdb, PCdb, and PAdb entities.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, expression

from app.db.base_class import Base


class FitmentMapping(Base):
    """Model for mapping product fitments to autocare data."""

    __tablename__ = "autocare_fitment_mapping"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Product relation
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )

    # VCdb relations - can be nullified if manual fitment
    vehicle_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, index=True
    )
    base_vehicle_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, index=True
    )

    # PCdb relations
    part_terminology_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, index=True
    )
    position_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, index=True
    )

    # Additional attributes (can be used to store qualifiers or other data)
    attributes: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=expression.text("'{}'::jsonb"),
    )

    # Flags
    is_validated: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    is_manual: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )

    # Metadata
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=True
    )
    updated_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=True
    )

    # Relationships
    product = relationship("Product", foreign_keys=[product_id])
    created_by = relationship("User", foreign_keys=[created_by_id])
    updated_by = relationship("User", foreign_keys=[updated_by_id])

    def __repr__(self) -> str:
        return f"<FitmentMapping {self.id}: product={self.product_id}, vehicle={self.vehicle_id}>"


class FitmentMappingHistory(Base):
    """Model for tracking changes to fitment mappings."""

    __tablename__ = "autocare_fitment_mapping_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Reference to the mapping
    mapping_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("autocare_fitment_mapping.id"),
        nullable=False,
        index=True,
    )

    # Change details
    change_type: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )  # CREATE, UPDATE, DELETE

    # Previous values (stored as JSON)
    previous_values: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )

    # New values (stored as JSON)
    new_values: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    # Metadata
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    changed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=True
    )

    # Relationships
    mapping = relationship("FitmentMapping", foreign_keys=[mapping_id])
    changed_by = relationship("User", foreign_keys=[changed_by_id])

    def __repr__(self) -> str:
        return f"<FitmentMappingHistory {self.id}: mapping={self.mapping_id}, type={self.change_type}>"
