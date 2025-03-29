from __future__ import annotations
'Model mapping definition.\n\nThis module defines the ModelMapping model for translation between\ndifferent vehicle model naming systems.\n'
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
class ModelMapping(Base):
    __tablename__ = 'model_mapping'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pattern: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    mapping: Mapped[str] = mapped_column(String(255), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f"<ModelMapping(id={self.id}, pattern='{self.pattern}', mapping='{self.mapping}')>"
    @property
    def make(self) -> str:
        parts = self.mapping.split('|')
        return parts[0] if len(parts) > 0 else ''
    @property
    def vehicle_code(self) -> str:
        parts = self.mapping.split('|')
        return parts[1] if len(parts) > 1 else ''
    @property
    def model(self) -> str:
        parts = self.mapping.split('|')
        return parts[2] if len(parts) > 2 else ''