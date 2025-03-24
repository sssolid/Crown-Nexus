from __future__ import annotations

"""Location model definition.

This module defines the models for geographic locations including
countries and addresses.
"""

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.domains.reference.models import Warehouse, TariffCode

if TYPE_CHECKING:
    from app.domains.products.models import Manufacturer
    from app.domains.company.schemas import Company


class Country(Base):
    """Country entity representing a geographic country or territory.

    Attributes:
        id: Unique identifier.
        name: Country name.
        iso_alpha_2: ISO 3166-1 alpha-2 code (2 letters).
        iso_alpha_3: ISO 3166-1 alpha-3 code (3 letters).
        iso_numeric: ISO 3166-1 numeric code (3 digits).
        region: Geographic region.
        subregion: Geographic subregion.
        currency: ISO 4217 currency code.
        created_at: Creation timestamp.
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
        """Return string representation of Country instance.

        Returns:
            String representation including name and ISO code.
        """
        return f"<Country {self.name} ({self.iso_alpha_2})>"


class Address(Base):
    """Address entity representing a physical location.

    Attributes:
        id: Unique identifier.
        street: Street address.
        city: City name.
        state: State or province.
        postal_code: Postal or ZIP code.
        country_id: ID of the associated country.
        latitude: Geographic latitude.
        longitude: Geographic longitude.
        created_at: Creation timestamp.
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
        """Return string representation of Address instance.

        Returns:
            String representation including street, city, and postal code.
        """
        return f"<Address {self.street}, {self.city}, {self.postal_code}>"
