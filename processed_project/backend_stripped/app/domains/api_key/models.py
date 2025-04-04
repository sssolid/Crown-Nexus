from __future__ import annotations
'API Key model definition.\n\nThis module defines the API Key model for API authentication.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, String, JSON, ForeignKey, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
if TYPE_CHECKING:
    from app.domains.users.models import User
class ApiKey(Base):
    __tablename__ = 'api_key'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.user.id', ondelete='CASCADE'), nullable=False, index=True)
    key_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_secret: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    permissions: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    extra_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='api_keys')
    __table_args__ = (Index('ix_api_keys_user_id_name', user_id, name, unique=True), {'schema': 'api_key'})
    def __repr__(self) -> str:
        return f'<ApiKey(id={self.id}, user_id={self.user_id}, name={self.name})>'
    def to_dict(self, include_secret: bool=False) -> Dict[str, Any]:
        result = {'id': str(self.id), 'user_id': str(self.user_id), 'key_id': self.key_id, 'name': self.name, 'is_active': self.is_active, 'created_at': self.created_at.isoformat() if self.created_at else None, 'updated_at': self.updated_at.isoformat() if self.updated_at else None, 'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None, 'expires_at': self.expires_at.isoformat() if self.expires_at else None, 'permissions': self.permissions or [], 'extra_metadata': self.extra_metadata or {}}
        if include_secret:
            result['hashed_secret'] = self.hashed_secret
        return result