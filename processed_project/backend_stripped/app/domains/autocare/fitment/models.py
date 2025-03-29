from __future__ import annotations
'Fitment mapping models.\n\nThis module defines models for mapping local product fitments to VCdb, PCdb, and PAdb entities.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, expression
from app.db.base_class import Base
class FitmentMapping(Base):
    __tablename__ = 'autocare_fitment_mapping'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('product.id'), nullable=False, index=True)
    vehicle_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    base_vehicle_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    part_terminology_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    position_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict, server_default=expression.text("'{}'::jsonb"))
    is_validated: Mapped[bool] = mapped_column(Boolean, default=False, server_default=expression.false(), nullable=False)
    is_manual: Mapped[bool] = mapped_column(Boolean, default=False, server_default=expression.false(), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    updated_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    product = relationship('Product', foreign_keys=[product_id])
    created_by = relationship('User', foreign_keys=[created_by_id])
    updated_by = relationship('User', foreign_keys=[updated_by_id])
    def __repr__(self) -> str:
        return f'<FitmentMapping {self.id}: product={self.product_id}, vehicle={self.vehicle_id}>'
class FitmentMappingHistory(Base):
    __tablename__ = 'autocare_fitment_mapping_history'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mapping_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('autocare_fitment_mapping.id'), nullable=False, index=True)
    change_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    previous_values: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    new_values: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    changed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    mapping = relationship('FitmentMapping', foreign_keys=[mapping_id])
    changed_by = relationship('User', foreign_keys=[changed_by_id])
    def __repr__(self) -> str:
        return f'<FitmentMappingHistory {self.id}: mapping={self.mapping_id}, type={self.change_type}>'