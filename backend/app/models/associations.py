# app/models/associations.py
from __future__ import annotations

"""
Many-to-many relationship tables for the application.

This module defines association tables that connect entities through
many-to-many relationships without creating separate model classes.
"""

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Table,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

# Product to Fitment relationship
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
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)

# Product to Media relationship
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
    Column("display_order", Integer, nullable=False, default=0),
    Column("is_primary", Integer, nullable=False, default=0),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)

# Product to TariffCode relationship
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
    Column(
        "assigned_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)

# Product to UnspscCode relationship
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
    Column(
        "assigned_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)

# Product to Country relationship (for origin information)
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
    Column("origin_type", Integer, nullable=False, default=0),
    Column("origin_order", Integer, nullable=False, default=0),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint("product_id", "country_id", name="uix_product_country"),
)

# Product to Hardware relationship
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
    Column("quantity", Integer, nullable=False, default=1),
    Column("is_optional", Integer, nullable=False, default=0),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint("product_id", "hardware_id", name="uix_product_hardware"),
)

# Product interchange information
product_interchange_association = Table(
    "product_interchange",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("interchange_number", Integer, nullable=False),
    Column(
        "brand_id",
        UUID(as_uuid=True),
        ForeignKey("brand.id", ondelete="SET NULL"),
        nullable=True,
    ),
    # CORRECTION: Changed from Integer to Text for notes
    Column("notes", Text, nullable=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint(
        "product_id", "interchange_number", "brand_id", name="uix_product_interchange"
    ),
)

# Product to PackagingType relationship
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
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)

# Product to Color relationship
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
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)

# Product to ConstructionType relationship
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
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)

# Product to Texture relationship
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
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)
