from __future__ import annotations
'Reference model definition.\n\nThis module defines reference data models such as Color, ConstructionType,\nTexture, PackagingType, Hardware, TariffCode, UnspscCode, and Warehouse.\n'
import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
if TYPE_CHECKING:
    from app.domains.products.models import ProductStock
    from app.domains.location.models import Address
class Color(Base):
    __tablename__ = 'color'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    hex_code: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f"<Color {self.name} ({self.hex_code or 'no hex'})>"
class ConstructionType(Base):
    __tablename__ = 'construction_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<ConstructionType {self.name}>'
class Texture(Base):
    __tablename__ = 'texture'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<Texture {self.name}>'
class PackagingType(Base):
    __tablename__ = 'packaging_type'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pies_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(20), nullable=False, default='Custom', server_default=func.text("'Custom'"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<PackagingType {self.name}>'
class Hardware(Base):
    __tablename__ = 'hardware_item'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    part_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<Hardware {self.name}>'
class TariffCode(Base):
    __tablename__ = 'tariff_code'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    country_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('country.id'), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    country = relationship('Country', back_populates='tariff_codes')
    def __repr__(self) -> str:
        return f'<TariffCode {self.code}>'
class UnspscCode(Base):
    __tablename__ = 'unspsc_code'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    segment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    family: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    class_: Mapped[Optional[str]] = mapped_column('class', String(255), nullable=True)
    commodity: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<UnspscCode {self.code}: {self.description}>'
class Warehouse(Base):
    __tablename__ = 'warehouse'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('address.id'), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=expression.true(), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    address: Mapped['Address'] = relationship('Address')
    stock: Mapped[List['ProductStock']] = relationship('ProductStock', back_populates='warehouse')
    def __repr__(self) -> str:
        return f'<Warehouse {self.name}>'