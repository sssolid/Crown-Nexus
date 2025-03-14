# backend/app/db/base.py
"""
SQLAlchemy models import module.

This module imports all SQLAlchemy models to ensure they're registered
with the declarative base. This is particularly important for Alembic
to detect models correctly when generating migrations.

This file should be imported by Alembic and not directly by application code.
The application should import models from their individual modules instead.
"""

from __future__ import annotations

# Import Base class
from app.db.base_class import Base

# Import all models for Alembic to detect
# NOTE: Order matters here due to foreign key relationships

# User-related models
from app.models.user import Company, User, UserRole  # noqa

# Association tables
from app.models.associations import (
    product_fitment_association,
    product_media_association,
    product_tariff_code_association,
    product_unspsc_association,
    product_country_origin_association,
    product_hardware_association,
    product_interchange_association,
    product_packaging_association,
    product_color_association,
    product_construction_type_association,
    product_texture_association
)  # noqa

# Location models
from app.models.location import Address, Country  # noqa

# Reference models
from app.models.reference import (
    Color,
    ConstructionType,
    Hardware,
    PackagingType,
    TariffCode,
    Texture,
    UnspscCode,
    Warehouse
)  # noqa

# Product models
from app.models.product import (
    AttributeDefinition,
    Brand,
    Fitment,
    Manufacturer,
    PriceType,
    Product,
    ProductActivity,
    ProductAttribute,
    ProductBrandHistory,
    ProductDescription,
    ProductMarketing,
    ProductMeasurement,
    ProductPricing,
    ProductStock,
    ProductSupersession
)  # noqa

# Media models
from app.models.media import Media, MediaType, MediaVisibility  # noqa

# Compliance models
from app.models.compliance import Prop65Chemical, ProductChemical  # noqa

# Import any future models here to ensure Alembic detects them
