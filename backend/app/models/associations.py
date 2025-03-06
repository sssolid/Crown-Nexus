# backend/app/models/associations.py
"""
Database association tables.

This module defines SQLAlchemy association tables for many-to-many
relationships between models. These tables enable:
- Products to be associated with multiple fitments
- Products to be associated with multiple media assets

Association tables are defined directly without using the Base class
to keep them lightweight and focused on their relationship function.
"""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

# Association table for many-to-many relationship between products and fitments
product_fitment_association = Table(
    "product_fitment",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "fitment_id",
        UUID(as_uuid=True),
        ForeignKey("fitment.id", ondelete="CASCADE"),
        primary_key=True
    ),
)

# Association table for many-to-many relationship between products and media
product_media_association = Table(
    "product_media",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "media_id",
        UUID(as_uuid=True),
        ForeignKey("media.id", ondelete="CASCADE"),
        primary_key=True
    ),
)
