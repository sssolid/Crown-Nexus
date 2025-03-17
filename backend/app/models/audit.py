# app/models/audit.py
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, DateTime, String, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.logging import get_logger

logger = get_logger("app.models.audit")


class AuditLog(Base):
    """SQLAlchemy model for audit logs.

    This model stores audit events for security and compliance purposes.
    """

    __tablename__ = "audit_logs"

    # Unique identifier for the audit log entry
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # When the event occurred
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)

    # Type of event (login, create, update, delete, etc.)
    event_type = Column(String, nullable=False, index=True)

    # Severity level (info, warning, error, critical)
    level = Column(String, nullable=False, index=True)

    # User who performed the action
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    user = relationship("User", back_populates="audit_logs")

    # IP address of the user
    ip_address = Column(String, nullable=True)

    # Resource that was affected
    resource_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    resource_type = Column(String, nullable=True, index=True)

    # Additional details about the event
    details = Column(JSON, nullable=True)

    # Optional fields for additional context
    request_id = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    session_id = Column(String, nullable=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    company = relationship("Company", back_populates="audit_logs")

    # Create indexes for common query patterns
    __table_args__ = (
        Index("ix_audit_logs_timestamp_desc", timestamp.desc()),
        Index("ix_audit_logs_user_id_timestamp", user_id, timestamp.desc()),
        Index("ix_audit_logs_resource_timestamp", resource_type, resource_id, timestamp.desc()),
        Index("ix_audit_logs_event_type_timestamp", event_type, timestamp.desc()),
    )

    def __repr__(self) -> str:
        """String representation of audit log entry."""
        return f"<AuditLog(id={self.id}, event_type={self.event_type}, timestamp={self.timestamp})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log entry to dictionary."""
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
