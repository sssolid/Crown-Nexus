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
from app.models.user import Company, User  # noqa
from app.models.associations import product_fitment_association, product_media_association  # noqa
from app.models.product import Category, Fitment, Product  # noqa
from app.models.media import Media, MediaType, MediaVisibility  # noqa

# Import any future models here to ensure Alembic detects them
