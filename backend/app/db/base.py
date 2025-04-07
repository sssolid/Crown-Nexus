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

# Base class
from app.db.base_class import Base  # noqa: F401

# Sync
import app.domains.sync_history.models  # noqa: F401

# Location & Logistics
import app.domains.location.models  # noqa: F401  # Address, Company, Manufacturer, TariffCode, Warehouse

# Authentication & Identity
import app.domains.api_key.models  # noqa: F401
import app.domains.users.models  # noqa: F401

# Company & Communication
import app.domains.company.models  # noqa: F401  # Depends on Address, User, Brand, ChatRoom, AuditLog
import app.domains.chat.models  # noqa: F401  # Depends on Company, User

# Currency & Financial
import app.domains.currency.models  # noqa: F401

# Products
import app.domains.products.models  # noqa: F401
import app.domains.products.associations  # noqa: F401
import app.domains.media.models  # noqa: F401  # Depends on Product, Media
import app.domains.compliance.models  # noqa: F401  # Depends on Product, User
import app.domains.model_mapping.models  # noqa: F401

# Autocare Datasets
import app.domains.autocare.fitment.models  # noqa: F401
import app.domains.autocare.padb.models  # noqa: F401
import app.domains.autocare.pcdb.models  # noqa: F401
import app.domains.autocare.qdb.models  # noqa: F401
import app.domains.autocare.vcdb.models  # noqa: F401

# Reference & Misc
import app.domains.reference.models  # noqa: F401

# Audit
import app.core.audit.models  # noqa: F401
