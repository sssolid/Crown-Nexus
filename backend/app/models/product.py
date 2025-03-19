# backend/app/models/product.py
"""
Product catalog models.

This module defines the models for products, categories, and related entities
in the automotive aftermarket catalog. It supports:
- Core product data with advanced attributes
- Product descriptions and marketing content
- Product activity tracking
- Product supersession relationships
- Brand and manufacturer associations
- Media associations
- Categorization and classification
- Pricing and measurements
- Country of origin and compliance information

The models provide a comprehensive structure for managing automotive parts,
accessories, and their metadata.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.base_class import Base

# Import associations with a conditional to avoid circular imports
if TYPE_CHECKING:
    from app.models.associations import (
        product_fitment_association,
        product_media_association,
    )
else:
    from app.models.associations import (
        product_fitment_association,
        product_media_association,
    )

# For type hints only, not runtime imports
if TYPE_CHECKING:
    from app.models.media import Media
    from app.models.user import User


class Product(Base):
    """
    Product model representing automotive parts and accessories.

    This model stores core information about products including:
    - Basic product details (part number, application)
    - Product flags (vintage, late_model, soft, universal)
    - Search capabilities via search_vector
    - Relationships to descriptions, marketing, activities, etc.

    Attributes:
        id: Primary key UUID
        part_number: Unique identifier for the product
        part_number_stripped: Alphanumeric version of part_number
        application: Unformatted data for vehicle fitment applications
        vintage: Vintage fitments flag
        late_model: Late model fitments flag
        soft: Soft good flag
        universal: Universal fit flag
        search_vector: Full-text search vector
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    part_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    part_number_stripped: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False
    )
    application: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    vintage: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    late_model: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    soft: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    universal: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    search_vector: Mapped[Optional[Any]] = mapped_column(TSVECTOR, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true(), nullable=False
    )

    # Relationships
    descriptions: Mapped[List["ProductDescription"]] = relationship(
        "ProductDescription", back_populates="product", cascade="all, delete-orphan"
    )

    marketing: Mapped[List["ProductMarketing"]] = relationship(
        "ProductMarketing", back_populates="product", cascade="all, delete-orphan"
    )

    activities: Mapped[List["ProductActivity"]] = relationship(
        "ProductActivity", back_populates="product", cascade="all, delete-orphan"
    )

    # Supersession relationships
    superseded_by: Mapped[List["ProductSupersession"]] = relationship(
        "ProductSupersession",
        foreign_keys="ProductSupersession.old_product_id",
        back_populates="old_product",
        cascade="all, delete-orphan",
    )

    supersedes: Mapped[List["ProductSupersession"]] = relationship(
        "ProductSupersession",
        foreign_keys="ProductSupersession.new_product_id",
        back_populates="new_product",
        cascade="all, delete-orphan",
    )

    # Attributes
    attributes: Mapped[List["ProductAttribute"]] = relationship(
        "ProductAttribute", back_populates="product", cascade="all, delete-orphan"
    )

    # Pricing
    pricing: Mapped[List["ProductPricing"]] = relationship(
        "ProductPricing", back_populates="product", cascade="all, delete-orphan"
    )

    # Measurements
    measurements: Mapped[List["ProductMeasurement"]] = relationship(
        "ProductMeasurement", back_populates="product", cascade="all, delete-orphan"
    )

    # Brand history
    brand_history: Mapped[List["ProductBrandHistory"]] = relationship(
        "ProductBrandHistory",
        foreign_keys="ProductBrandHistory.product_id",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    # Media relationship - using fully qualified string to avoid circular imports
    media: Mapped[List["Media"]] = relationship(
        "app.models.media.Media",
        secondary=product_media_association,
        back_populates="products",
    )

    # Fitment relationship
    fitments: Mapped[List["Fitment"]] = relationship(
        "Fitment", secondary=product_fitment_association, back_populates="products"
    )

    # Stock relationship
    stock: Mapped[List["ProductStock"]] = relationship(
        "ProductStock", back_populates="product", cascade="all, delete-orphan"
    )

    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """
        String representation of the product.

        Returns:
            str: Product representation with part number
        """
        return f"<Product {self.part_number}>"


class ProductDescription(Base):
    """
    Product description model.

    Stores different types of descriptions for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        description_type: Type of description (Short, Long, Keywords, etc.)
        description: Description content
        created_at: Creation timestamp
    """

    __tablename__ = "product_description"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False
    )
    description_type: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="descriptions")

    def __repr__(self) -> str:
        """
        String representation of the product description.

        Returns:
            str: Product description representation
        """
        return f"<ProductDescription {self.description_type} for {self.product_id}>"


class ProductMarketing(Base):
    """
    Product marketing model.

    Stores marketing content for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        marketing_type: Type of marketing content (Bullet Point, Ad Copy)
        content: Marketing content
        position: Order for display
        created_at: Creation timestamp
    """

    __tablename__ = "product_marketing"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False
    )
    marketing_type: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="marketing")

    def __repr__(self) -> str:
        """
        String representation of the product marketing.

        Returns:
            str: Product marketing representation
        """
        return f"<ProductMarketing {self.marketing_type} for {self.product_id}>"


class ProductActivity(Base):
    """
    Product activity model.

    Tracks status changes for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        status: Product status (active, inactive)
        reason: Reason for status change
        changed_by: User who made the change
        changed_at: When the change occurred
    """

    __tablename__ = "product_activity"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=True
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="activities")
    changed_by: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[changed_by_id]
    )

    def __repr__(self) -> str:
        """
        String representation of the product activity.

        Returns:
            str: Product activity representation
        """
        return f"<ProductActivity {self.status} for {self.product_id}>"


class ProductSupersession(Base):
    """
    Product supersession model.

    Tracks product replacements.

    Attributes:
        id: Primary key UUID
        old_product_id: Product being replaced
        new_product_id: Replacement product
        reason: Explanation of why the product was superseded
        changed_at: When the change occurred
    """

    __tablename__ = "product_supersession"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    old_product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    new_product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    old_product: Mapped["Product"] = relationship(
        "Product", foreign_keys=[old_product_id], back_populates="superseded_by"
    )
    new_product: Mapped["Product"] = relationship(
        "Product", foreign_keys=[new_product_id], back_populates="supersedes"
    )

    def __repr__(self) -> str:
        """
        String representation of the product supersession.

        Returns:
            str: Product supersession representation
        """
        return f"<ProductSupersession {self.old_product_id} -> {self.new_product_id}>"


class Brand(Base):
    """
    Brand model.

    Represents product brands.

    Attributes:
        id: Primary key UUID
        name: Brand name
        parent_company_id: Reference to parent company
        created_at: Creation timestamp
    """

    __tablename__ = "brand"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    parent_company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    parent_company = relationship("Company", foreign_keys=[parent_company_id])

    # Brand history
    brand_history: Mapped[List["ProductBrandHistory"]] = relationship(
        "ProductBrandHistory",
        foreign_keys="[ProductBrandHistory.new_brand_id, ProductBrandHistory.old_brand_id]",
        primaryjoin="or_(Brand.id==ProductBrandHistory.new_brand_id, "
        "Brand.id==ProductBrandHistory.old_brand_id)",
        viewonly=True,
    )

    def __repr__(self) -> str:
        """
        String representation of the brand.

        Returns:
            str: Brand representation
        """
        return f"<Brand {self.name}>"


class ProductBrandHistory(Base):
    """
    Product brand history model.

    Tracks brand changes for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        old_brand_id: Previous brand
        new_brand_id: New brand
        changed_by_id: User who made the change
        changed_at: When the change occurred
    """

    __tablename__ = "product_brand_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    old_brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("brand.id"), nullable=True
    )
    new_brand_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("brand.id"), nullable=False
    )
    changed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=True
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    product: Mapped["Product"] = relationship(
        "Product", foreign_keys=[product_id], back_populates="brand_history"
    )
    old_brand: Mapped[Optional["Brand"]] = relationship(
        "Brand", foreign_keys=[old_brand_id]
    )
    new_brand: Mapped["Brand"] = relationship("Brand", foreign_keys=[new_brand_id])
    changed_by: Mapped[Optional["User"]] = relationship(
        "User", foreign_keys=[changed_by_id]
    )

    def __repr__(self) -> str:
        """
        String representation of the product brand history.

        Returns:
            str: Product brand history representation
        """
        return f"<ProductBrandHistory {self.product_id}: {self.old_brand_id} -> {self.new_brand_id}>"


class AttributeDefinition(Base):
    """
    Attribute definition model.

    Defines flexible product attributes.

    Attributes:
        id: Primary key UUID
        name: Attribute name
        code: Code for the attribute
        description: Description of the attribute
        data_type: Data type
        is_required: Whether the attribute is required
        default_value: Default value for the attribute
        validation_regex: Regular expression for validation
        min_value: Minimum value
        max_value: Maximum value
        options: For picklist values
        display_order: Order for displaying attributes
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "attribute_definition"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    is_required: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    default_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    validation_regex: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    min_value: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    max_value: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    options: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    display_order: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    attributes: Mapped[List["ProductAttribute"]] = relationship(
        "ProductAttribute", back_populates="attribute"
    )

    def __repr__(self) -> str:
        """
        String representation of the attribute definition.

        Returns:
            str: Attribute definition representation
        """
        return f"<AttributeDefinition {self.code}>"


class ProductAttribute(Base):
    """
    Product attribute model.

    Stores flexible attribute values for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        attribute_id: Reference to attribute definition
        value_string: String value
        value_number: Numeric value
        value_boolean: Boolean value
        value_date: Date value
        value_json: JSON value
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "product_attribute"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    attribute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("attribute_definition.id"),
        nullable=False,
        index=True,
    )
    value_string: Mapped[Optional[str]] = mapped_column(Text, nullable=True, index=True)
    value_number: Mapped[Optional[float]] = mapped_column(
        Numeric, nullable=True, index=True
    )
    value_boolean: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True, index=True
    )
    value_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    value_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="attributes")
    attribute: Mapped["AttributeDefinition"] = relationship(
        "AttributeDefinition", back_populates="attributes"
    )

    __table_args__ = (
        # Ensure a product can't have the same attribute twice
        UniqueConstraint("product_id", "attribute_id", name="uix_product_attribute"),
    )

    def __repr__(self) -> str:
        """
        String representation of the product attribute.

        Returns:
            str: Product attribute representation
        """
        return f"<ProductAttribute {self.product_id}: {self.attribute_id}>"


class PriceType(Base):
    """
    Price type model.

    Defines types of prices.

    Attributes:
        id: Primary key UUID
        name: Price type name
        description: Description of price type
        created_at: Creation timestamp
    """

    __tablename__ = "price_type"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    pricing: Mapped[List["ProductPricing"]] = relationship(
        "ProductPricing", back_populates="pricing_type"
    )

    def __repr__(self) -> str:
        """
        String representation of the price type.

        Returns:
            str: Price type representation
        """
        return f"<PriceType {self.name}>"


class ProductPricing(Base):
    """
    Product pricing model.

    Stores pricing information for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        pricing_type_id: Reference to price type
        manufacturer_id: Optional manufacturer reference
        price: The current price
        currency: Currency code
        last_updated: Last update timestamp
    """

    __tablename__ = "product_pricing"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    pricing_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("price_type.id"), nullable=False, index=True
    )
    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("manufacturer.id"), nullable=True, index=True
    )
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), default="USD", server_default=text("'USD'"), nullable=False
    )
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="pricing")
    pricing_type: Mapped["PriceType"] = relationship(
        "PriceType", back_populates="pricing"
    )
    manufacturer: Mapped[Optional["Manufacturer"]] = relationship(
        "Manufacturer", back_populates="product_pricing"
    )

    def __repr__(self) -> str:
        """
        String representation of the product pricing.

        Returns:
            str: Product pricing representation
        """
        return f"<ProductPricing {self.product_id}: {self.pricing_type_id} = {self.price} {self.currency}>"


class Manufacturer(Base):
    """
    Manufacturer model.

    Represents product manufacturers.

    Attributes:
        id: Primary key UUID
        name: Manufacturer name
        company_id: Parent company if applicable
        address_id: Reference to address
        billing_address_id: Reference to billing address
        shipping_address_id: Reference to shipping address
        country_id: Manufacturing location
        created_at: Creation timestamp
    """

    __tablename__ = "manufacturer"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id"), nullable=True, index=True
    )
    address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("address.id"), nullable=True
    )
    billing_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("address.id"), nullable=True
    )
    shipping_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("address.id"), nullable=True
    )
    country_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("country.id"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])
    address = relationship("Address", foreign_keys=[address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    country = relationship("Country", foreign_keys=[country_id])

    # Product pricing
    product_pricing: Mapped[List["ProductPricing"]] = relationship(
        "ProductPricing", back_populates="manufacturer"
    )

    # Product measurements
    product_measurements: Mapped[List["ProductMeasurement"]] = relationship(
        "ProductMeasurement", back_populates="manufacturer"
    )

    def __repr__(self) -> str:
        """
        String representation of the manufacturer.

        Returns:
            str: Manufacturer representation
        """
        return f"<Manufacturer {self.name}>"


class ProductMeasurement(Base):
    """
    Product measurement model.

    Stores dimensional information for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        manufacturer_id: Optional manufacturer reference
        length: Length in inches
        width: Width in inches
        height: Height in inches
        weight: Weight in pounds
        volume: Volume in cubic inches
        dimensional_weight: DIM weight calculation
        effective_date: When measurements become effective
    """

    __tablename__ = "product_measurement"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("manufacturer.id"), nullable=True, index=True
    )
    length: Mapped[Optional[float]] = mapped_column(Numeric(10, 3), nullable=True)
    width: Mapped[Optional[float]] = mapped_column(Numeric(10, 3), nullable=True)
    height: Mapped[Optional[float]] = mapped_column(Numeric(10, 3), nullable=True)
    weight: Mapped[Optional[float]] = mapped_column(Numeric(10, 3), nullable=True)
    volume: Mapped[Optional[float]] = mapped_column(Numeric(10, 3), nullable=True)
    dimensional_weight: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 3), nullable=True
    )
    effective_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="measurements")
    manufacturer: Mapped[Optional["Manufacturer"]] = relationship(
        "Manufacturer", back_populates="product_measurements"
    )

    def __repr__(self) -> str:
        """
        String representation of the product measurement.

        Returns:
            str: Product measurement representation
        """
        return f"<ProductMeasurement {self.product_id}>"


class ProductStock(Base):
    """
    Product stock model.

    Tracks inventory levels for products.

    Attributes:
        id: Primary key UUID
        product_id: Reference to product
        warehouse_id: Reference to warehouse
        quantity: Quantity in stock
        last_updated: Last stock update timestamp
    """

    __tablename__ = "product_stock"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.id"), nullable=False, index=True
    )
    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("warehouse.id"), nullable=False, index=True
    )
    quantity: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"), nullable=False, index=True
    )
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="stock")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="stock")

    def __repr__(self) -> str:
        """
        String representation of the product stock.

        Returns:
            str: Product stock representation
        """
        return (
            f"<ProductStock {self.product_id} @ {self.warehouse_id}: {self.quantity}>"
        )


class Fitment(Base):
    """
    Fitment model representing vehicle compatibility information.

    This model stores information about vehicle compatibility for products:
    - Year/Make/Model data for basic vehicle identification
    - Engine and transmission details for specific applications
    - Flexible JSON attributes for additional fitment criteria

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
    engine: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True
    )
    transmission: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, index=True
    )
    attributes: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb")
    )

    # Relationships
    products: Mapped[List[Product]] = relationship(
        "Product", secondary=product_fitment_association, back_populates="fitments"
    )

    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """
        String representation of the fitment.

        Returns:
            str: Fitment representation with year, make, and model
        """
        return f"<Fitment {self.year} {self.make} {self.model}>"
