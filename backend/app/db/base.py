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

from app.models.api_key import ApiKey  # noqa
from app.models.audit import AuditLog  # noqa
from app.models.chat import (
    ChatRoom,
    ChatMember,
    ChatRoomType,
    ChatMemberRole,
    ChatMessage,
    MessageReaction,
    MessageType,
    RateLimitLog,
)  # noqa
from app.models.company import Company  # noqa
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
)  # noqa
from app.models.currency import Currency, ExchangeRate  # noqa
from app.models.location import Address, Country  # noqa
from app.models.media import Media, MediaType, MediaVisibility  # noqa
from app.models.model_mapping import ModelMapping  # noqa
from app.models.product import (
    Product,
    ProductActivity,
    ProductAttribute,
    ProductBrandHistory,
    ProductDescription,
    ProductMarketing,
    ProductMeasurement,
    ProductPricing,
    ProductStock,
    ProductSupersession,
    Brand,
    Fitment,
    Manufacturer,
    PriceType,
    AttributeDefinition,
)  # noqa
from app.models.reference import (
    Warehouse,
    TariffCode,
    Texture,
    UnspscCode,
    Color,
    ConstructionType,
    Hardware,
    PackagingType,
)  # noqa
from app.models.user import User, UserRole  # noqa

# Import any future models here to ensure Alembic detects them
