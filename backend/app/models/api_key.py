# app/models/api_key.py
from __future__ import annotations

import uuid
from typing import Any, Dict

from sqlalchemy import Column, DateTime, String, JSON, ForeignKey, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.logging import get_logger

logger = get_logger("app.models.api_key")


class ApiKey(Base):
    """SQLAlchemy model for API keys.

    This model stores API keys for authenticating API requests.
    """

    __tablename__ = "api_keys"

    # Unique identifier for the API key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # User who owns this API key
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user = relationship("User", back_populates="api_keys")

    # Key identifier (public part)
    key_id = Column(String, unique=True, nullable=False, index=True)

    # Hashed secret (never stored in plain text)
    hashed_secret = Column(String, nullable=False)

    # Name of the API key
    name = Column(String, nullable=False)

    # Whether the key is currently active
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    # When the key was last used
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    # Optional expiration date
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # Permissions granted to this key
    permissions = Column(JSON, nullable=True)

    # Metadata
    metadata = Column(JSON, nullable=True)

    # Indexes
    __table_args__ = (Index("ix_api_keys_user_id_name", user_id, name, unique=True),)

    def __repr__(self) -> str:
        """String representation of API key."""
        return f"<ApiKey(id={self.id}, user_id={self.user_id}, name={self.name})>"

    def to_dict(self, include_secret: bool = False) -> Dict[str, Any]:
        """Convert API key to dictionary."""
        result = {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "key_id": self.key_id,
            "name": self.name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_used_at": (
                self.last_used_at.isoformat() if self.last_used_at else None
            ),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "permissions": self.permissions or [],
            "metadata": self.metadata or {},
        }

        if include_secret:
            result["hashed_secret"] = self.hashed_secret

        return result
