from __future__ import annotations

"""Company model definition.

This module defines the Company model and related functionality for
company management within the application.
"""

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.base_class import Base
from app.domains.chat.models import ChatRoom
from app.core.audit.models import AuditLog

if TYPE_CHECKING:
    from app.domains.users.models import User
    from app.core.audit import AuditLog
    from app.domains.products.models import Brand


class Company(Base):
    """Company entity representing a business organization.

    Attributes:
        id: Unique identifier.
        name: Company name.
        headquarters_address_id: ID of the headquarters address.
        billing_address_id: ID of the billing address.
        shipping_address_id: ID of the shipping address.
        account_number: Unique account identifier.
        account_type: Type of account (client, supplier, etc).
        industry: Industry sector.
        is_active: Whether the company is active.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "company"
    __table_args__ = {"schema": "company"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    headquarters_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.address.id"), nullable=True
    )
    billing_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.address.id"), nullable=True
    )
    shipping_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.address.id"), nullable=True
    )
    account_number: Mapped[Optional[str]] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    account_type: Mapped[str] = mapped_column(String(50), nullable=False)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    headquarters_address = relationship(
        "Address", foreign_keys=[headquarters_address_id]
    )
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    users: Mapped[List["User"]] = relationship("User", back_populates="company")
    brands: Mapped[List["Brand"]] = relationship(
        "Brand",
        foreign_keys="[Brand.parent_company_id]",
        back_populates="parent_company",
    )
    chat_rooms: Mapped[List["ChatRoom"]] = relationship(
        "ChatRoom", back_populates="company"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog", back_populates="company"
    )

    def __repr__(self) -> str:
        """Return string representation of Company instance.

        Returns:
            String representation including name and account type.
        """
        return f"<Company {self.name} ({self.account_type})>"
