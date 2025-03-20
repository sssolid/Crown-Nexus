from __future__ import annotations

"""API Key model definition.

This module defines the API Key model for API authentication.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import Column, DateTime, String, JSON, ForeignKey, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User


class ApiKey(Base):
    """API Key entity for API authentication.

    Attributes:
        id: Unique identifier.
        user_id: ID of the user who owns the key.
        key_id: Public identifier for the API key.
        hashed_secret: Hashed secret part of the API key.
        name: Human-readable name for the key.
        is_active: Whether the key is active.
        last_used_at: When the key was last used.
        expires_at: When the key expires.
        permissions: Specific permissions granted to the key.
        extra_metadata: Additional metadata about the key.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "api_key"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key_id: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_secret: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, index=True
    )
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    permissions: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    extra_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="api_keys")

    __table_args__ = (Index("ix_api_keys_user_id_name", user_id, name, unique=True),)

    def __repr__(self) -> str:
        """Return string representation of ApiKey instance.

        Returns:
            String representation including id, user_id, and name.
        """
        return f"<ApiKey(id={self.id}, user_id={self.user_id}, name={self.name})>"

    def to_dict(self, include_secret: bool = False) -> Dict[str, Any]:
        """Convert the API key to a dictionary.

        Args:
            include_secret: Whether to include the hashed secret.

        Returns:
            Dictionary representation of the API key.
        """
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
            "extra_metadata": self.extra_metadata or {},
        }

        if include_secret:
            result["hashed_secret"] = self.hashed_secret

        return result
