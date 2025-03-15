from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
class ModelMapping(Base):
    __tablename__ = 'model_mappings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pattern = Column(String(255), nullable=False, index=True)
    mapping = Column(String(255), nullable=False)
    priority = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
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