# backend/app/models/currency.py
"""
Currency models.

This module defines models for currency management and exchange rates:
- Currency information and codes
- Historical exchange rates between currencies
- API configuration for rate updates

These models support price conversion, international sales, and
financial reporting across different currencies.
"""

from __future__ import annotations

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
    """
    Currency model.

    Represents currency information:
    - ISO codes
    - Name
    - Symbol
    - Active status

    Attributes:
        id: Primary key UUID
        code: ISO 4217 currency code (USD, EUR, etc.)
        name: Currency name
        symbol: Currency symbol
        is_active: Whether the currency is active
        is_base: Whether this is the base currency for the system
        created_at: Creation timestamp
        updated_at: Last update timestamp
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
        """
        String representation of the currency.

        Returns:
            str: Currency representation
        """
        return f"<Currency {self.code} ({self.name})>"


class ExchangeRate(Base):
    """
    Exchange rate model.

    Tracks historical exchange rates between currencies:
    - Source and target currencies
    - Rate value
    - Effective date

    Attributes:
        id: Primary key UUID
        source_currency_id: Reference to source currency
        target_currency_id: Reference to target currency
        rate: Exchange rate value
        effective_date: When the rate became effective
        fetched_at: When the rate was fetched from the API
        data_source: API or source that provided the rate
        created_at: Creation timestamp
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

    # Ensure we don't have duplicate entries for same currency pair and date
    __table_args__ = (
        UniqueConstraint(
            "source_currency_id",
            "target_currency_id",
            "effective_date",
            name="uix_exchange_rate_source_target_date",
        ),
    )

    def __repr__(self) -> str:
        """
        String representation of the exchange rate.

        Returns:
            str: Exchange rate representation
        """
        return f"<ExchangeRate {self.source_currency_id} -> {self.target_currency_id}: {self.rate}>"
