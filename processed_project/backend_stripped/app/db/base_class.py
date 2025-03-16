from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, cast, ClassVar, get_args, get_origin, get_type_hints
from sqlalchemy import Column, DateTime, Boolean, String, inspect, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from sqlalchemy.sql.expression import Select
from app.core.logging import get_logger
logger = get_logger('app.db.base_class')
T = TypeVar('T', bound='Base')
@as_declarative()
class Base(DeclarativeBase):
    id: Column = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Column = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Column = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted: Column = Column(Boolean, default=False, nullable=False, index=True)
    created_by_id: Column = Column(UUID(as_uuid=True), nullable=True)
    updated_by_id: Column = Column(UUID(as_uuid=True), nullable=True)
    __exclude_from_dict__: ClassVar[List[str]] = ['is_deleted']
    __include_relationships__: ClassVar[bool] = False
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    def to_dict(self, exclude: Optional[List[str]]=None, include_relationships: Optional[bool]=None) -> Dict[str, Any]:
        exclude_fields = set(self.__exclude_from_dict__)
        if exclude:
            exclude_fields.update(exclude)
        include_rels = self.__include_relationships__ if include_relationships is None else include_relationships
        result = {}
        for key, value in inspect(self).dict.items():
            if key in exclude_fields or (key == 'is_deleted' and value):
                continue
            if key.startswith('_'):
                continue
            mapper = inspect(self.__class__)
            if key in mapper.relationships and (not include_rels):
                continue
            if isinstance(value, uuid.UUID):
                value = str(value)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[key] = value
        return result
    @classmethod
    def get_columns(cls) -> List[str]:
        return [c.name for c in inspect(cls).columns]
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        valid_fields = cls.get_columns()
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)
    @classmethod
    def filter_by_id(cls: Type[T], id_value: uuid.UUID) -> Select:
        return select(cls).where(cls.id == id_value, cls.is_deleted == False)
    @classmethod
    def active_only(cls) -> Select:
        return select(cls).where(cls.is_deleted == False)
    def soft_delete(self, user_id: Optional[uuid.UUID]=None) -> None:
        self.is_deleted = True
        if user_id:
            self.updated_by_id = user_id
    def restore(self, user_id: Optional[uuid.UUID]=None) -> None:
        self.is_deleted = False
        if user_id:
            self.updated_by_id = user_id
    def update_from_dict(self, data: Dict[str, Any], user_id: Optional[uuid.UUID]=None, exclude: Optional[List[str]]=None) -> None:
        if exclude is None:
            exclude = []
        exclude = exclude + ['id', 'created_at', 'created_by_id', 'is_deleted']
        columns = self.get_columns()
        for key, value in data.items():
            if key in columns and key not in exclude:
                setattr(self, key, value)
        if user_id:
            self.updated_by_id = user_id
    @classmethod
    def get_relationships(cls) -> Dict[str, Any]:
        return {r.key: r for r in inspect(cls).relationships}