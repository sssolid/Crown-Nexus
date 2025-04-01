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
from app.domains.api_key.models import ApiKey  # noqa: F401
from app.domains.users.models import User, UserRole  # noqa: F401
from app.domains.company.models import Company  # noqa: F401
from app.domains.currency.models import Currency, ExchangeRate  # noqa: F401
from app.domains.media.models import Media, MediaType, MediaVisibility  # noqa: F401
import app.domains.products.models  # noqa: F401

# Now models that depend on others:
from app.core.audit.models import AuditLog  # noqa: F401
from app.domains.model_mapping.models import ModelMapping  # noqa: F401

# Import associations after all models

# Import any future models here to ensure Alembic detects them
