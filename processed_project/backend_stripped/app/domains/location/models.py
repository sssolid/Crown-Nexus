from __future__ import annotations
'Location model definition.\n\nThis module defines the models for geographic locations including\ncountries and addresses.\n'
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
    __tablename__ = 'country'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    iso_alpha_2: Mapped[str] = mapped_column(String(2), nullable=False, unique=True, index=True)
    iso_alpha_3: Mapped[str] = mapped_column(String(3), nullable=False, unique=True, index=True)
    iso_numeric: Mapped[Optional[str]] = mapped_column(String(3), nullable=True, unique=True)
    region: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    subregion: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    addresses: Mapped[List['Address']] = relationship('Address', back_populates='country')
    manufacturers: Mapped[List['Manufacturer']] = relationship('Manufacturer', back_populates='country')
    tariff_codes: Mapped[List['TariffCode']] = relationship('TariffCode', back_populates='country')
    def __repr__(self) -> str:
        return f'<Country {self.name} ({self.iso_alpha_2})>'
class Address(Base):
    __tablename__ = 'address'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    country_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('country.id'), nullable=False, index=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float(precision=10, decimal_return_scale=7), nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float(precision=10, decimal_return_scale=7), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    country: Mapped['Country'] = relationship('Country', back_populates='addresses')
    warehouses: Mapped[List['Warehouse']] = relationship('Warehouse', foreign_keys='[Warehouse.address_id]')
    manufacturers_primary: Mapped[List['Manufacturer']] = relationship('Manufacturer', foreign_keys='[Manufacturer.address_id]')
    manufacturers_billing: Mapped[List['Manufacturer']] = relationship('Manufacturer', foreign_keys='[Manufacturer.billing_address_id]')
    manufacturers_shipping: Mapped[List['Manufacturer']] = relationship('Manufacturer', foreign_keys='[Manufacturer.shipping_address_id]')
    companies_headquarters: Mapped[List['Company']] = relationship('Company', foreign_keys='[Company.headquarters_address_id]')
    companies_billing: Mapped[List['Company']] = relationship('Company', foreign_keys='[Company.billing_address_id]')
    companies_shipping: Mapped[List['Company']] = relationship('Company', foreign_keys='[Company.shipping_address_id]')
    def __repr__(self) -> str:
        return f'<Address {self.street}, {self.city}, {self.postal_code}>'