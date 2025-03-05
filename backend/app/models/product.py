from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from app.db.base_class import Base
from app.models.associations import product_fitment_association, product_media_association

# For type hints only, not runtime imports
if TYPE_CHECKING:
    from app.models.media import Media


class Product(Base):
    """
    Product model representing automotive parts and accessories.

    Attributes:
        id: Primary key UUID
        sku: Stock keeping unit, unique identifier for product
        name: Product name
        description: Detailed product description
        part_number: Manufacturer part number
        category_id: Reference to product category
        attributes: JSON field for flexible product attributes
        is_active: Whether the product is active and available
        fitments: Associated vehicle fitments for this product
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    part_number: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("category.id"), nullable=True
    )
    attributes: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    fitments: Mapped[List["Fitment"]] = relationship(
        "Fitment",
        secondary=product_fitment_association,
        back_populates="products"
    )
    category: Mapped[Optional["Category"]] = relationship("Category")

    # Media relationship - using fully qualified string to avoid circular imports
    # but with proper type annotation for the IDE
    media: Mapped[List["Media"]] = relationship(
        "app.models.media.Media",
        secondary=product_media_association,
        back_populates="products"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        """String representation of the product."""
        return f"<Product {self.sku}: {self.name}>"


class Fitment(Base):
    """
    Fitment model representing vehicle compatibility information.

    Attributes:
        id: Primary key UUID
        year: Vehicle model year
        make: Vehicle manufacturer
        model: Vehicle model name
        engine: Engine specification
        transmission: Transmission type
        attributes: JSON field for additional fitment attributes
        products: Associated products for this fitment
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "fitment"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    make: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    engine: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    transmission: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    attributes: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )

    # Relationships
    products: Mapped[List[Product]] = relationship(
        "Product",
        secondary=product_fitment_association,
        back_populates="fitments"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        """String representation of the fitment."""
        return f"<Fitment {self.year} {self.make} {self.model}>"


class Category(Base):
    """
    Product category model.

    Attributes:
        id: Primary key UUID
        name: Category name
        slug: URL-friendly version of name
        parent_id: Reference to parent category for hierarchical structure
        description: Category description
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "category"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("category.id"), nullable=True
    )
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Self-referential relationship for hierarchy
    children: Mapped[List["Category"]] = relationship(
        "Category",
        backref=backref("parent", remote_side=[id]),
        cascade="all, delete-orphan",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        """String representation of the category."""
        return f"<Category {self.name}>"
