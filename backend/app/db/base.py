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

# Import models with proper dependency order
# First models that don't depend on others:
from app.models.location import Country, Address
from app.models.company import Company
from app.models.user import User, UserRole
from app.models.reference import (
    Color,
    ConstructionType,
    Hardware,
    PackagingType,
    Texture,
    TariffCode,
    UnspscCode,
    Warehouse,
)
from app.models.currency import Currency, ExchangeRate
from app.models.media import Media, MediaType, MediaVisibility

# Now models that depend on others:
from app.models.product import (
    Product,
    Brand,
    Fitment,
    Manufacturer,
    PriceType,
    AttributeDefinition,
    ProductActivity,
    ProductAttribute,
    ProductBrandHistory,
    ProductDescription,
    ProductMarketing,
    ProductMeasurement,
    ProductPricing,
    ProductStock,
    ProductSupersession,
)
from app.models.audit import AuditLog
from app.models.compliance import (
    Prop65Chemical,
    ProductChemical,
    ChemicalType,
    ProductDOTApproval,
    ApprovalStatus,
    ExposureScenario,
    HazardousMaterial,
    TransportRestriction,
    Warning,
)
from app.models.model_mapping import ModelMapping
from app.models.chat import (
    ChatRoom,
    ChatMember,
    ChatRoomType,
    ChatMemberRole,
    ChatMessage,
    MessageReaction,
    MessageType,
    RateLimitLog,
)
from app.models.api_key import ApiKey

# Import associations after all models
from app.models.associations import (
    product_color_association,
    product_construction_type_association,
    product_country_origin_association,
    product_fitment_association,
    product_hardware_association,
    product_interchange_association,
    product_media_association,
    product_packaging_association,
    product_tariff_code_association,
    product_texture_association,
    product_unspsc_association,
)

# Import any future models here to ensure Alembic detects them
