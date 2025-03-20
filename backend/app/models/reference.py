from __future__ import annotations

"""Reference model definition.

This module defines reference data models such as Color, ConstructionType,
Texture, PackagingType, Hardware, TariffCode, UnspscCode, and Warehouse.
"""

import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.product import Product, ProductStock
    from app.models.location import Address


class Color(Base):
    """Color entity representing a product color.

    Attributes:
        id: Unique identifier.
        name: Color name.
        hex_code: Hexadecimal color code.
        created_at: Creation timestamp.
    """

    __tablename__ = "color"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    hex_code: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """Return string representation of Color instance.

        Returns:
            String representation including name and hex code.
        """
        return f"<Color {self.name} ({self.hex_code or 'no hex'})>"


class ConstructionType(Base):
    """Construction type entity representing a product construction method.

    Attributes:
        id: Unique identifier.
        name: Construction type name.
        description: Description of the construction type.
        created_at: Creation timestamp.
    """

    __tablename__ = "construction_type"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """Return string representation of ConstructionType instance.

        Returns:
            String representation including name.
        """
        return f"<ConstructionType {self.name}>"


class Texture(Base):
    """Texture entity representing a product texture.

    Attributes:
        id: Unique identifier.
        name: Texture name.
        description: Description of the texture.
        created_at: Creation timestamp.
    """

    __tablename__ = "texture"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """Return string representation of Texture instance.

        Returns:
            String representation including name.
        """
        return f"<Texture {self.name}>"


class PackagingType(Base):
    """Packaging type entity representing a product packaging method.

    Attributes:
        id: Unique identifier.
        pies_code: PIES standard code.
        name: Packaging type name.
        description: Description of the packaging type.
        source: Source of the packaging type data.
        created_at: Creation timestamp.
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
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Custom",
        server_default=func.text("'Custom'"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """Return string representation of PackagingType instance.

        Returns:
            String representation including name.
        """
        return f"<PackagingType {self.name}>"


class Hardware(Base):
    """Hardware item entity representing hardware used with products.

    Attributes:
        id: Unique identifier.
        name: Hardware item name.
        description: Description of the hardware item.
        part_number: Manufacturer part number.
        created_at: Creation timestamp.
    """

    __tablename__ = "hardware_item"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    part_number: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """Return string representation of Hardware instance.

        Returns:
            String representation including name.
        """
        return f"<Hardware {self.name}>"


class TariffCode(Base):
    """Tariff code entity representing a product tariff classification.

    Attributes:
        id: Unique identifier.
        code: Tariff code number.
        description: Description of the tariff code.
        country_id: ID of the country this tariff applies to.
        created_at: Creation timestamp.
    """

    __tablename__ = "tariff_code"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    country_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("country.id"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    country = relationship("Country", back_populates="tariff_codes")

    def __repr__(self) -> str:
        """Return string representation of TariffCode instance.

        Returns:
            String representation including code.
        """
        return f"<TariffCode {self.code}>"


class UnspscCode(Base):
    """UNSPSC code entity for product classification.

    Attributes:
        id: Unique identifier.
        code: UNSPSC code number.
        description: Description of the code.
        segment: Segment description.
        family: Family description.
        class_: Class description.
        commodity: Commodity description.
        created_at: Creation timestamp.
    """

    __tablename__ = "unspsc_code"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(
        String(10), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    segment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    family: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    class_: Mapped[Optional[str]] = mapped_column("class", String(255), nullable=True)
    commodity: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """Return string representation of UnspscCode instance.

        Returns:
            String representation including code and description.
        """
        return f"<UnspscCode {self.code}: {self.description}>"


class Warehouse(Base):
    """Warehouse entity representing a storage location.

    Attributes:
        id: Unique identifier.
        name: Warehouse name.
        address_id: ID of the warehouse address.
        is_active: Whether the warehouse is active.
        created_at: Creation timestamp.
    """

    __tablename__ = "warehouse"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("address.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=expression.true(),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    address: Mapped["Address"] = relationship("Address")
    stock: Mapped[List["ProductStock"]] = relationship(
        "ProductStock", back_populates="warehouse"
    )

    def __repr__(self) -> str:
        """Return string representation of Warehouse instance.

        Returns:
            String representation including name.
        """
        return f"<Warehouse {self.name}>"
