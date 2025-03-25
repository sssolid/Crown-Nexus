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
from app.db.base_class import Base  # noqa: F401

# Import models with proper dependency order
# First models that don't depend on others:
from app.domains.location.models import Country, Address  # noqa: F401
from app.domains.users.models import User, UserRole  # noqa: F401
from app.domains.company.models import Company  # noqa: F401
from app.domains.reference.models import (
    Color,
    ConstructionType,
    Hardware,
    PackagingType,
    Texture,
    TariffCode,
    UnspscCode,
    Warehouse,
)  # noqa: F401
from app.domains.currency.models import Currency, ExchangeRate  # noqa: F401
from app.domains.media.models import Media, MediaType, MediaVisibility  # noqa: F401

# Now models that depend on others:
from app.domains.products.models import (
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
)  # noqa: F401
from app.domains.audit.models import AuditLog  # noqa: F401
from app.domains.compliance.models import (
    Prop65Chemical,
    ProductChemical,
    ChemicalType,
    ProductDOTApproval,
    ApprovalStatus,
    ExposureScenario,
    HazardousMaterial,
    TransportRestriction,
    Warning,
)  # noqa: F401
from app.domains.model_mapping.models import ModelMapping  # noqa: F401
from app.domains.chat.models import (
    ChatRoom,
    ChatMember,
    ChatRoomType,
    ChatMemberRole,
    ChatMessage,
    MessageReaction,
    MessageType,
    RateLimitLog,
)  # noqa: F401
from app.domains.api_key.models import ApiKey  # noqa: F401

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
)  # noqa: F401

# Import any future models here to ensure Alembic detects them

