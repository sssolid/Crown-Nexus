from __future__ import annotations

"""
Synchronization history model.

This module defines models for tracking synchronization operations
and their outcomes, particularly for AS400 data integration.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class SyncEntityType(str, Enum):
    """Types of entities that can be synchronized."""

    PRODUCT = "product"
    MEASUREMENT = "measurement"
    STOCK = "stock"
    PRICING = "pricing"
    MANUFACTURER = "manufacturer"
    CUSTOMER = "customer"
    ORDER = "order"


class SyncStatus(str, Enum):
    """Status of synchronization operations."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SyncSource(str, Enum):
    """Source systems for synchronization."""

    AS400 = "as400"
    FILEMAKER = "filemaker"
    API = "api"
    EXTERNAL = "external"


class SyncHistory(Base):
    """History of synchronization operations."""

    __tablename__ = "sync_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, default=SyncSource.AS400.value
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True, default=SyncStatus.PENDING.value
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    records_processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    records_created: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    records_updated: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    records_failed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    sync_duration: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    triggered_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user.id"), nullable=True
    )
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    triggered_by = relationship("User", foreign_keys=[triggered_by_id])
    events: Mapped[List["SyncEvent"]] = relationship(
        "SyncEvent", back_populates="sync", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_sync_history_status_started_at", status, started_at.desc()),
        Index("ix_sync_history_entity_source", entity_type, source),
        {"schema": "sync_history"},
    )

    def __repr__(self) -> str:
        return (
            f"<SyncHistory(id={self.id}, "
            f"entity_type={self.entity_type}, "
            f"source={self.source}, "
            f"status={self.status})>"
        )

    def complete(
        self,
        status: SyncStatus,
        records_processed: int,
        records_created: int,
        records_updated: int,
        records_failed: int,
        error_message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Mark the sync as complete with results.

        Args:
            status: Final status
            records_processed: Number of records processed
            records_created: Number of records created
            records_updated: Number of records updated
            records_failed: Number of records that failed
            error_message: Error message if any
            details: Additional details
        """
        self.status = status.value
        self.completed_at = datetime.now()
        self.records_processed = records_processed
        self.records_created = records_created
        self.records_updated = records_updated
        self.records_failed = records_failed
        self.error_message = error_message

        if details:
            self.details = (
                details if self.details is None else {**self.details, **details}
            )

        # Calculate duration
        if self.started_at:
            self.sync_duration = (datetime.now() - self.started_at).total_seconds()

    def add_event(
        self, event_type: str, message: str, details: Optional[Dict[str, Any]] = None
    ) -> "SyncEvent":
        """
        Add an event to this sync operation.

        Args:
            event_type: Type of event
            message: Event message
            details: Additional details

        Returns:
            Created event
        """
        event = SyncEvent(
            sync_id=self.id, event_type=event_type, message=message, details=details
        )
        self.events.append(event)
        return event


class SyncEvent(Base):
    """Events during synchronization operations."""

    __tablename__ = "sync_event"
    __table_args__ = {"schema": "sync_history"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    sync_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sync_history.sync_history.id"), nullable=False, index=True
    )

    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    sync: Mapped[SyncHistory] = relationship("SyncHistory", back_populates="events")

    def __repr__(self) -> str:
        return (
            f"<SyncEvent(id={self.id}, "
            f"event_type={self.event_type}, "
            f"sync_id={self.sync_id})>"
        )
