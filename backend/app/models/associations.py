# backend/app/models/associations.py
"""
Association tables for many-to-many relationships.

This module defines SQLAlchemy association tables that establish
many-to-many relationships between different entities in the application:
- Products and fitments (vehicle compatibility)
- Products and media assets
- Products and warehouses (stock levels)
- And other many-to-many relationships as needed

These tables don't have their own identity beyond connecting related entities
and should not contain business logic.
"""

from __future__ import annotations

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Table,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

# Association table for products and fitments
product_fitment_association = Table(
    "product_fitment",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "fitment_id",
        UUID(as_uuid=True),
        ForeignKey("fitment.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Metadata
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
)

# Association table for products and media
product_media_association = Table(
    "product_media",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "media_id",
        UUID(as_uuid=True),
        ForeignKey("media.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Optional sequence for ordering media items
    Column("display_order", Integer, nullable=False, default=0),
    # Is this the primary/featured media for the product
    Column("is_primary", Integer, nullable=False, default=0),
    # Metadata
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
)

# Association table for products and tariff codes
product_tariff_code_association = Table(
    "product_tariff_code",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tariff_code_id",
        UUID(as_uuid=True),
        ForeignKey("tariff_code.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Metadata
    Column(
        "assigned_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)

# Association table for products and UNSPSC codes
product_unspsc_association = Table(
    "product_unspsc",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "unspsc_code_id",
        UUID(as_uuid=True),
        ForeignKey("unspsc_code.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Metadata
    Column(
        "assigned_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)

# Association table for products and countries of origin
product_country_origin_association = Table(
    "product_country_origin",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "country_id",
        UUID(as_uuid=True),
        ForeignKey("country.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "manufacturer_id",
        UUID(as_uuid=True),
        ForeignKey("manufacturer.id", ondelete="SET NULL"),
        nullable=True,
    ),
    # Type of origin (Origin, Assembly, etc.)
    Column("origin_type", Integer, nullable=False, default=0),
    # Order for organizing countries
    Column("origin_order", Integer, nullable=False, default=0),
    # Metadata
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
    # Add a unique constraint for product_id and country_id
    UniqueConstraint("product_id", "country_id", name="uix_product_country"),
)

# Association table for products and hardware items
product_hardware_association = Table(
    "product_hardware",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "hardware_id",
        UUID(as_uuid=True),
        ForeignKey("hardware_item.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Number of hardware pieces included
    Column("quantity", Integer, nullable=False, default=1),
    # Is the hardware required
    Column("is_optional", Integer, nullable=False, default=0),
    # Metadata
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
    # Add a unique constraint for product_id and hardware_id
    UniqueConstraint("product_id", "hardware_id", name="uix_product_hardware"),
)

# Association table for products and interchanges
product_interchange_association = Table(
    "product_interchange",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Interchange number (part number from another brand/supplier)
    Column("interchange_number", Integer, nullable=False),
    # Optional brand reference
    Column(
        "brand_id",
        UUID(as_uuid=True),
        ForeignKey("brand.id", ondelete="SET NULL"),
        nullable=True,
    ),
    # Optional compatibility notes
    Column("notes", Integer, nullable=True),
    # Metadata
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
    # Primary key is product_id and interchange_number
    UniqueConstraint(
        "product_id", "interchange_number", "brand_id", name="uix_product_interchange"
    ),
)

# Association table for products and packaging types
product_packaging_association = Table(
    "product_packaging",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "packaging_type_id",
        UUID(as_uuid=True),
        ForeignKey("packaging_type.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Metadata
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
)

# Association table for products and colors
product_color_association = Table(
    "product_color",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "color_id",
        UUID(as_uuid=True),
        ForeignKey("color.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Metadata
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
)

# Association table for products and construction types
product_construction_type_association = Table(
    "product_construction_type",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "construction_type_id",
        UUID(as_uuid=True),
        ForeignKey("construction_type.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Metadata
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
)

# Association table for products and textures
product_texture_association = Table(
    "product_texture",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "texture_id",
        UUID(as_uuid=True),
        ForeignKey("texture.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    # Metadata
    Column(
        "created_at", DateTime(timezone=True), nullable=False, server_default=func.now()
    ),
)
