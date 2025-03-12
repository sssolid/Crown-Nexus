from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar
from sqlalchemy import Column, DateTime, inspect, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.expression import Select
T = TypeVar('T', bound='Base')
@as_declarative()
class Base:
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    def dict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
    @classmethod
    def filter_by_id(cls: Type[T], id: uuid.UUID) -> Select:
        from sqlalchemy import select
        return select(cls).where(cls.id == id)
    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)