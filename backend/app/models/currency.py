from __future__ import annotations

"""Currency model definition.

This module defines the Currency model and related functionality for
currency and exchange rate management within the application.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Currency(Base):
    """Currency entity representing a monetary currency.

    Attributes:
        id: Unique identifier.
        code: ISO 4217 currency code.
        name: Currency name.
        symbol: Currency symbol.
        is_active: Whether the currency is active.
        is_base: Whether this is the base currency.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "currency"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(
        String(3), nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    symbol: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_base: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
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
    source_rates: Mapped[List["ExchangeRate"]] = relationship(
        "ExchangeRate",
        foreign_keys="[ExchangeRate.source_currency_id]",
        back_populates="source_currency",
    )
    target_rates: Mapped[List["ExchangeRate"]] = relationship(
        "ExchangeRate",
        foreign_keys="[ExchangeRate.target_currency_id]",
        back_populates="target_currency",
    )

    def __repr__(self) -> str:
        """Return string representation of Currency instance.

        Returns:
            String representation including code and name.
        """
        return f"<Currency {self.code} ({self.name})>"


class ExchangeRate(Base):
    """Exchange rate between two currencies.

    Attributes:
        id: Unique identifier.
        source_currency_id: ID of the source currency.
        target_currency_id: ID of the target currency.
        rate: Exchange rate value.
        effective_date: When the rate became effective.
        fetched_at: When the rate was fetched.
        data_source: API or source that provided the rate.
        created_at: Creation timestamp.
    """

    __tablename__ = "exchange_rate"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source_currency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("currency.id"), nullable=False, index=True
    )
    target_currency_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("currency.id"), nullable=False, index=True
    )
    rate: Mapped[float] = mapped_column(Float, nullable=False)
    effective_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    data_source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    source_currency: Mapped["Currency"] = relationship(
        "Currency", foreign_keys=[source_currency_id], back_populates="source_rates"
    )
    target_currency: Mapped["Currency"] = relationship(
        "Currency", foreign_keys=[target_currency_id], back_populates="target_rates"
    )

    __table_args__ = (
        UniqueConstraint(
            "source_currency_id",
            "target_currency_id",
            "effective_date",
            name="uix_exchange_rate_source_target_date",
        ),
    )

    def __repr__(self) -> str:
        """Return string representation of ExchangeRate instance.

        Returns:
            String representation including source, target, and rate.
        """
        return f"<ExchangeRate {self.source_currency_id} -> {self.target_currency_id}: {self.rate}>"
