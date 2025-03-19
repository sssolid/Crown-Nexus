# backend/app/models/location.py
"""
Location models.

This module defines models for geographical locations used throughout
the application:
- Countries with their ISO codes
- Physical addresses
- Geolocation data

These models support international shipping, taxation, regulatory compliance,
and other location-dependent functionality.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, String, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

# For type hints only, not runtime imports
if TYPE_CHECKING:
    from app.models.reference import Warehouse, TariffCode
    from app.models.product import Manufacturer
    from app.models.user import Company


class Country(Base):
    """
    Country model.

    Represents countries with ISO codes and related information.

    Attributes:
        id: Primary key UUID
        name: Full country name
        iso_alpha_2: 2-letter country code (US, etc.)
        iso_alpha_3: 3-letter country code (USA, etc.)
        iso_numeric: Numeric country code (840, etc.)
        region: Region name (North America, etc.)
        subregion: Subregion name (Northern America, etc.)
        currency: Currency code (USD, etc.)
        created_at: Creation timestamp
    """

    __tablename__ = "country"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    iso_alpha_2: Mapped[str] = mapped_column(
        String(2), nullable=False, unique=True, index=True
    )
    iso_alpha_3: Mapped[str] = mapped_column(
        String(3), nullable=False, unique=True, index=True
    )
    iso_numeric: Mapped[Optional[str]] = mapped_column(
        String(3), nullable=True, unique=True
    )
    region: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    subregion: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    addresses: Mapped[List["Address"]] = relationship(
        "Address", back_populates="country"
    )
    manufacturers: Mapped[List["Manufacturer"]] = relationship(
        "Manufacturer", back_populates="country"
    )
    tariff_codes: Mapped[List["TariffCode"]] = relationship(
        "TariffCode", back_populates="country"
    )

    def __repr__(self) -> str:
        """
        String representation of the country.

        Returns:
            str: Country representation
        """
        return f"<Country {self.name} ({self.iso_alpha_2})>"


class Address(Base):
    """
    Address model.

    Represents physical addresses for companies, warehouses, etc.

    Attributes:
        id: Primary key UUID
        street: Street address
        city: City name
        state: State or province
        postal_code: Postal or ZIP code
        country_id: Reference to country
        latitude: Geographical latitude
        longitude: Geographical longitude
        created_at: Creation timestamp
    """

    __tablename__ = "address"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("country.id"), nullable=False, index=True
    )
    latitude: Mapped[Optional[float]] = mapped_column(
        Float(precision=10, decimal_return_scale=7), nullable=True
    )
    longitude: Mapped[Optional[float]] = mapped_column(
        Float(precision=10, decimal_return_scale=7), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    country: Mapped["Country"] = relationship("Country", back_populates="addresses")
    warehouses: Mapped[List["Warehouse"]] = relationship(
        "Warehouse", foreign_keys="[Warehouse.address_id]"
    )
    manufacturers_primary: Mapped[List["Manufacturer"]] = relationship(
        "Manufacturer", foreign_keys="[Manufacturer.address_id]"
    )
    manufacturers_billing: Mapped[List["Manufacturer"]] = relationship(
        "Manufacturer", foreign_keys="[Manufacturer.billing_address_id]"
    )
    manufacturers_shipping: Mapped[List["Manufacturer"]] = relationship(
        "Manufacturer", foreign_keys="[Manufacturer.shipping_address_id]"
    )
    companies_headquarters: Mapped[List["Company"]] = relationship(
        "Company", foreign_keys="[Company.headquarters_address_id]"
    )
    companies_billing: Mapped[List["Company"]] = relationship(
        "Company", foreign_keys="[Company.billing_address_id]"
    )
    companies_shipping: Mapped[List["Company"]] = relationship(
        "Company", foreign_keys="[Company.shipping_address_id]"
    )

    def __repr__(self) -> str:
        """
        String representation of the address.

        Returns:
            str: Address representation
        """
        return f"<Address {self.street}, {self.city}, {self.postal_code}>"
