# backend/app/models/reference.py
"""
Reference data models.

This module defines models for various reference data used throughout
the application. These models represent relatively static lookup tables
that provide standardization and categorization:
- Colors
- Construction types (materials)
- Textures
- Packaging types
- Hardware items
- Classification codes
- Warehouses

The models follow a consistent pattern with standardized audit fields
and appropriate relationships to related entities.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    text
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.base_class import Base

# For type hints only, not runtime imports
if TYPE_CHECKING:
    from app.models.product import Product


class Color(Base):
    """
    Color model.

    Represents standard color names and their hex codes.

    Attributes:
        id: Primary key UUID
        name: Standard color name
        hex_code: Hex code for digital representation (optional)
        created_at: Creation timestamp
    """
    __tablename__ = "color"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    hex_code: Mapped[Optional[str]] = mapped_column(
        String(7), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """
        String representation of the color.

        Returns:
            str: Color representation
        """
        return f"<Color {self.name} ({self.hex_code or 'no hex'})>"


class ConstructionType(Base):
    """
    Construction type model.

    Represents materials used in product construction.

    Attributes:
        id: Primary key UUID
        name: Material name
        description: Optional description
        created_at: Creation timestamp
    """
    __tablename__ = "construction_type"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """
        String representation of the construction type.

        Returns:
            str: Construction type representation
        """
        return f"<ConstructionType {self.name}>"


class Texture(Base):
    """
    Texture model.

    Represents surface textures of products.

    Attributes:
        id: Primary key UUID
        name: Texture name
        description: Optional description
        created_at: Creation timestamp
    """
    __tablename__ = "texture"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """
        String representation of the texture.

        Returns:
            str: Texture representation
        """
        return f"<Texture {self.name}>"


class PackagingType(Base):
    """
    Packaging type model.

    Represents types of product packaging.

    Attributes:
        id: Primary key UUID
        pies_code: AutoCare PCdb PIES Code (optional)
        name: Packaging type name
        description: Optional description
        source: Source of the data
        created_at: Creation timestamp
    """
    __tablename__ = "packaging_type"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    pies_code: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )
    source: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Custom", server_default=text("'Custom'")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """
        String representation of the packaging type.

        Returns:
            str: Packaging type representation
        """
        return f"<PackagingType {self.name}>"


class Hardware(Base):
    """
    Hardware item model.

    Represents hardware items included with products.

    Attributes:
        id: Primary key UUID
        name: Name of the hardware item
        description: Optional details
        part_number: Optional part number for the hardware item
        created_at: Creation timestamp
    """
    __tablename__ = "hardware_item"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )
    part_number: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """
        String representation of the hardware item.

        Returns:
            str: Hardware item representation
        """
        return f"<Hardware {self.name}>"


class TariffCode(Base):
    """
    Tariff code model.

    Represents HS, HTS, or other tariff codes.

    Attributes:
        id: Primary key UUID
        code: Tariff code
        description: Description of the code
        country_id: Country this code applies to (optional)
        created_at: Creation timestamp
    """
    __tablename__ = "tariff_code"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(
        String(15), nullable=False, index=True
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    country_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("country.id"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    country = relationship("Country")

    def __repr__(self) -> str:
        """
        String representation of the tariff code.

        Returns:
            str: Tariff code representation
        """
        return f"<TariffCode {self.code}>"


class UnspscCode(Base):
    """
    UNSPSC code model.

    Represents United Nations Standard Products and Services Code.

    Attributes:
        id: Primary key UUID
        code: 8- or 10-digit UNSPSC code
        description: UNSPSC category description
        segment: High-level category
        family: Sub-category
        class: Product class
        commodity: Specific commodity category
        created_at: Creation timestamp
    """
    __tablename__ = "unspsc_code"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(
        String(10), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    segment: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    family: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    class_: Mapped[Optional[str]] = mapped_column(
        "class", String(255), nullable=True  # class is a reserved word
    )
    commodity: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """
        String representation of the UNSPSC code.

        Returns:
            str: UNSPSC code representation
        """
        return f"<UnspscCode {self.code}: {self.description}>"


class Warehouse(Base):
    """
    Warehouse model.

    Represents product storage locations.

    Attributes:
        id: Primary key UUID
        name: Warehouse name
        address_id: Reference to address (optional)
        is_active: Whether the warehouse is active
        created_at: Creation timestamp
    """
    __tablename__ = "warehouse"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("address.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true(), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    address = relationship("Address")
    stock = relationship("ProductStock", back_populates="warehouse")

    def __repr__(self) -> str:
        """
        String representation of the warehouse.

        Returns:
            str: Warehouse representation
        """
        return f"<Warehouse {self.name}>"
