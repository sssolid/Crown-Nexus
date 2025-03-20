from __future__ import annotations

"""Audit model definition.

This module defines the AuditLog model for tracking system activity.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING

from sqlalchemy import Column, DateTime, String, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.company import Company


class AuditLog(Base):
    """Audit log entity for tracking system activity.

    Attributes:
        id: Unique identifier.
        timestamp: When the audited event occurred.
        event_type: Type of event being audited.
        level: Log level (info, warning, error).
        user_id: ID of the user who performed the action.
        ip_address: IP address of the user.
        resource_id: ID of the affected resource.
        resource_type: Type of the affected resource.
        details: Additional details about the event.
        request_id: ID of the request that triggered the event.
        user_agent: User agent of the client.
        session_id: ID of the user's session.
        company_id: ID of the company context.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "audit_log"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    level: Mapped[str] = mapped_column(String, nullable=False, index=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    ip_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    resource_type: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, index=True
    )
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    request_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("company.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="audit_logs")
    company: Mapped[Optional["Company"]] = relationship(
        "Company", back_populates="audit_logs"
    )

    __table_args__ = (
        Index("ix_audit_log_timestamp_desc", timestamp.desc()),
        Index("ix_audit_log_user_id_timestamp", user_id, timestamp.desc()),
        Index(
            "ix_audit_log_resource_timestamp",
            resource_type,
            resource_id,
            timestamp.desc(),
        ),
        Index("ix_audit_log_event_type_timestamp", event_type, timestamp.desc()),
    )

    def __repr__(self) -> str:
        """Return string representation of AuditLog instance.

        Returns:
            String representation including id, event_type, and timestamp.
        """
        return f"<AuditLog(id={self.id}, event_type={self.event_type}, timestamp={self.timestamp})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert the audit log to a dictionary.

        Returns:
            Dictionary representation of the audit log.
        """
        return {
            "id": str(self.id),
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "level": self.level,
            "user_id": str(self.user_id) if self.user_id else None,
            "ip_address": self.ip_address,
            "resource_id": str(self.resource_id) if self.resource_id else None,
            "resource_type": self.resource_type,
            "details": self.details or {},
            "request_id": self.request_id,
            "user_agent": self.user_agent,
            "session_id": self.session_id,
            "company_id": str(self.company_id) if self.company_id else None,
        }
