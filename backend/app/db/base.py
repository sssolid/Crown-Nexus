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

# Import models with proper dependency order
# First models that don't depend on others:

# Now models that depend on others:

# Import associations after all models

# Import any future models here to ensure Alembic detects them
