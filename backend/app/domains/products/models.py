from __future__ import annotations

"""Product model definition.

This module defines the Product model and related entities for
product management within the application.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy import UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.base_class import Base

# Avoid circular imports
if TYPE_CHECKING:
    from app.domains.media.models import Media
    from app.domains.reference.models import (
        Color,
        ConstructionType,
        Hardware,
        PackagingType,
        TariffCode,
        Texture,
        UnspscCode,
    )
    from app.domains.location.models import Country
else:
    # Import association tables
    from app.models.associations import (
        product_color_association,
        product_construction_type_association,
        product_country_origin_association,
        product_fitment_association,
        product_hardware_association,
        product_media_association,
        product_packaging_association,
        product_tariff_code_association,
        product_texture_association,
        product_unspsc_association,
    )


class Product(Base):
    """Product entity representing a sellable item.

    Attributes:
        id: Unique identifier.
        part_number: Product part number (unique).
        part_number_stripped: Normalized version of part number for searching.
        application: Product application or use case description.
        vintage: Whether the product is for vintage vehicles.
        late_model: Whether the product is for late model vehicles.
        soft: Whether the product is soft (e.g., fabric vs metal).
        universal: Whether the product is universal (fits multiple applications).
        search_vector: Full-text search vector.
        is_active: Whether the product is active in the catalog.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "product"
    __table_args__ = {"schema": "product"}

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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Foreign Key relationships
    descriptions: Mapped[List["ProductDescription"]] = relationship(
        "ProductDescription", back_populates="product", cascade="all, delete-orphan"
    )
    marketing: Mapped[List["ProductMarketing"]] = relationship(
        "ProductMarketing", back_populates="product", cascade="all, delete-orphan"
    )
    activities: Mapped[List["ProductActivity"]] = relationship(
        "ProductActivity", back_populates="product", cascade="all, delete-orphan"
    )
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
    attributes: Mapped[List["ProductAttribute"]] = relationship(
        "ProductAttribute", back_populates="product", cascade="all, delete-orphan"
    )
    pricing: Mapped[List["ProductPricing"]] = relationship(
        "ProductPricing", back_populates="product", cascade="all, delete-orphan"
    )
    measurements: Mapped[List["ProductMeasurement"]] = relationship(
        "ProductMeasurement", back_populates="product", cascade="all, delete-orphan"
    )
    brand_history: Mapped[List["ProductBrandHistory"]] = relationship(
        "ProductBrandHistory",
        foreign_keys="ProductBrandHistory.product_id",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    stock: Mapped[List["ProductStock"]] = relationship(
        "ProductStock", back_populates="product", cascade="all, delete-orphan"
    )

    # Many-to-many relationships using association tables
    media: Mapped[List["Media"]] = relationship(
        "Media",
        secondary=product_media_association,
        back_populates="products",
    )

    fitments: Mapped[List["Fitment"]] = relationship(
        "Fitment", secondary=product_fitment_association, back_populates="products"
    )

    tariff_codes: Mapped[List["TariffCode"]] = relationship(
        "TariffCode",
        secondary=product_tariff_code_association,
        backref="products",  # Simpler than back_populates if TariffCode doesn't define the relationship
    )

    unspsc_codes: Mapped[List["UnspscCode"]] = relationship(
        "UnspscCode",
        secondary=product_unspsc_association,
        backref="products",
    )

    countries_of_origin: Mapped[List["Country"]] = relationship(
        "Country",
        secondary=product_country_origin_association,
        backref="products_as_origin",
    )

    hardware_items: Mapped[List["Hardware"]] = relationship(
        "Hardware",
        secondary=product_hardware_association,
        backref="products",
    )

    colors: Mapped[List["Color"]] = relationship(
        "Color",
        secondary=product_color_association,
        backref="products",
    )

    construction_types: Mapped[List["ConstructionType"]] = relationship(
        "ConstructionType",
        secondary=product_construction_type_association,
        backref="products",
    )

    textures: Mapped[List["Texture"]] = relationship(
        "Texture",
        secondary=product_texture_association,
        backref="products",
    )

    packaging_types: Mapped[List["PackagingType"]] = relationship(
        "PackagingType",
        secondary=product_packaging_association,
        backref="products",
    )

    def __repr__(self) -> str:
        """Return string representation of Product instance.

        Returns:
            String representation including part number.
        """
        return f"<Product {self.part_number}>"


class ProductDescription(Base):
    """Product description entity representing a textual description of a product.

    Attributes:
        id: Unique identifier.
        product_id: ID of the associated product.
        description_type: Type of description (e.g., short, long, etc.).
        description: The actual description text.
        created_at: Creation timestamp.
    """

    __tablename__ = "product_description"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False
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
        """Return string representation of ProductDescription instance.

        Returns:
            String representation including description type and product ID.
        """
        return f"<ProductDescription {self.description_type} for {self.product_id}>"


class ProductMarketing(Base):
    """Product marketing entity representing marketing content for a product.

    Attributes:
        id: Unique identifier.
        product_id: ID of the associated product.
        marketing_type: Type of marketing content (e.g., bullet point, ad copy, etc.).
        content: The actual marketing content.
        position: Display order position.
        created_at: Creation timestamp.
    """

    __tablename__ = "product_marketing"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False
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
        """Return string representation of ProductMarketing instance.

        Returns:
            String representation including marketing type and product ID.
        """
        return f"<ProductMarketing {self.marketing_type} for {self.product_id}>"


class ProductActivity(Base):
    """Product activity entity representing status changes for a product.

    Attributes:
        id: Unique identifier.
        product_id: ID of the associated product.
        status: Product status (e.g., active, inactive, discontinued, etc.).
        reason: Reason for the status change.
        changed_by_id: ID of the user who made the change.
        changed_at: When the change was made.
    """

    __tablename__ = "product_activity"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user.id"), nullable=True
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
        """Return string representation of ProductActivity instance.

        Returns:
            String representation including status and product ID.
        """
        return f"<ProductActivity {self.status} for {self.product_id}>"


class ProductSupersession(Base):
    """Product supersession entity representing when one product replaces another.

    Attributes:
        id: Unique identifier.
        old_product_id: ID of the product being replaced.
        new_product_id: ID of the replacement product.
        reason: Reason for the supersession.
        changed_at: When the supersession was created.
    """

    __tablename__ = "product_supersession"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    old_product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    new_product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
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
        """Return string representation of ProductSupersession instance.

        Returns:
            String representation including old and new product IDs.
        """
        return f"<ProductSupersession {self.old_product_id} -> {self.new_product_id}>"


class Brand(Base):
    """Brand entity representing a product brand.

    Attributes:
        id: Unique identifier.
        name: Brand name.
        parent_company_id: ID of the parent company.
        created_at: Creation timestamp.
    """

    __tablename__ = "brand"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    parent_company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.company.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    parent_company = relationship("Company", foreign_keys=[parent_company_id])
    brand_history: Mapped[List["ProductBrandHistory"]] = relationship(
        "ProductBrandHistory",
        foreign_keys="[ProductBrandHistory.new_brand_id, ProductBrandHistory.old_brand_id]",
        primaryjoin="or_(Brand.id==ProductBrandHistory.new_brand_id, Brand.id==ProductBrandHistory.old_brand_id)",
        viewonly=True,
    )

    def __repr__(self) -> str:
        """Return string representation of Brand instance.

        Returns:
            String representation including name.
        """
        return f"<Brand {self.name}>"


class ProductBrandHistory(Base):
    """Product brand history entity representing brand changes for a product.

    Attributes:
        id: Unique identifier.
        product_id: ID of the associated product.
        old_brand_id: ID of the previous brand.
        new_brand_id: ID of the new brand.
        changed_by_id: ID of the user who made the change.
        changed_at: When the change was made.
    """

    __tablename__ = "product_brand_history"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    old_brand_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.brand.id"), nullable=True
    )
    new_brand_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.brand.id"), nullable=False
    )
    changed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.user.id"), nullable=True
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
        """Return string representation of ProductBrandHistory instance.

        Returns:
            String representation including product ID and brand change.
        """
        return f"<ProductBrandHistory {self.product_id}: {self.old_brand_id} -> {self.new_brand_id}>"


class AttributeDefinition(Base):
    """Attribute definition entity representing a product attribute type.

    Attributes:
        id: Unique identifier.
        name: Attribute name.
        code: Attribute code (unique).
        description: Attribute description.
        data_type: Data type (e.g., string, number, boolean, etc.).
        is_required: Whether the attribute is required.
        default_value: Default value for the attribute.
        validation_regex: Regex for validation of string values.
        min_value: Minimum allowed value for numeric attributes.
        max_value: Maximum allowed value for numeric attributes.
        options: Available options for enum-like attributes.
        display_order: Display order position.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "attribute_definition"
    __table_args__ = {"schema": "product"}

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
        """Return string representation of AttributeDefinition instance.

        Returns:
            String representation including code.
        """
        return f"<AttributeDefinition {self.code}>"


class ProductAttribute(Base):
    """Product attribute entity representing a specific attribute value for a product.

    Attributes:
        id: Unique identifier.
        product_id: ID of the associated product.
        attribute_id: ID of the attribute definition.
        value_string: String value.
        value_number: Numeric value.
        value_boolean: Boolean value.
        value_date: Date value.
        value_json: JSON value.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "product_attribute"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    attribute_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product.attribute_definition.id"),
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
        UniqueConstraint("product_id", "attribute_id", name="uix_product_attribute"),
        {"schema": "product"},
    )

    def __repr__(self) -> str:
        """Return string representation of ProductAttribute instance.

        Returns:
            String representation including product ID and attribute ID.
        """
        return f"<ProductAttribute {self.product_id}: {self.attribute_id}>"


class PriceType(Base):
    """Price type entity representing a type of pricing (e.g., retail, wholesale, etc.).

    Attributes:
        id: Unique identifier.
        name: Price type name.
        description: Price type description.
        created_at: Creation timestamp.
    """

    __tablename__ = "price_type"
    __table_args__ = {"schema": "product"}

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
        """Return string representation of PriceType instance.

        Returns:
            String representation including name.
        """
        return f"<PriceType {self.name}>"


class ProductPricing(Base):
    """Product pricing entity representing a price for a product.

    Attributes:
        id: Unique identifier.
        product_id: ID of the associated product.
        pricing_type_id: ID of the price type.
        manufacturer_id: ID of the manufacturer.
        price: Price value.
        currency: Currency code.
        last_updated: When the price was last updated.
    """

    __tablename__ = "product_pricing"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    pricing_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.price_type.id"), nullable=False, index=True
    )
    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.manufacturer.id"), nullable=True, index=True
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
        """Return string representation of ProductPricing instance.

        Returns:
            String representation including product ID, pricing type, and price.
        """
        return f"<ProductPricing {self.product_id}: {self.pricing_type_id} = {self.price} {self.currency}>"


class Manufacturer(Base):
    """Manufacturer entity representing a product manufacturer.

    Attributes:
        id: Unique identifier.
        name: Manufacturer name.
        company_id: ID of the associated company.
        address_id: ID of the primary address.
        billing_address_id: ID of the billing address.
        shipping_address_id: ID of the shipping address.
        country_id: ID of the country of origin.
        created_at: Creation timestamp.
    """

    __tablename__ = "manufacturer"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.company.id"), nullable=True, index=True
    )
    address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.address.id"), nullable=True
    )
    billing_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.address.id"), nullable=True
    )
    shipping_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.address.id"), nullable=True
    )
    country_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.country.id"), nullable=True, index=True
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
    product_pricing: Mapped[List["ProductPricing"]] = relationship(
        "ProductPricing", back_populates="manufacturer"
    )
    product_measurements: Mapped[List["ProductMeasurement"]] = relationship(
        "ProductMeasurement", back_populates="manufacturer"
    )

    def __repr__(self) -> str:
        """Return string representation of Manufacturer instance.

        Returns:
            String representation including name.
        """
        return f"<Manufacturer {self.name}>"


class ProductMeasurement(Base):
    """Product measurement entity representing physical measurements of a product.

    Attributes:
        id: Unique identifier.
        product_id: ID of the associated product.
        manufacturer_id: ID of the manufacturer who provided the measurements.
        length: Length measurement.
        width: Width measurement.
        height: Height measurement.
        weight: Weight measurement.
        volume: Volume measurement.
        dimensional_weight: Dimensional weight for shipping calculations.
        effective_date: When the measurements became effective.
    """

    __tablename__ = "product_measurement"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.manufacturer.id"), nullable=True, index=True
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
        """Return string representation of ProductMeasurement instance.

        Returns:
            String representation including product ID.
        """
        return f"<ProductMeasurement {self.product_id}>"


class ProductStock(Base):
    """Product stock entity representing inventory levels for a product.

    Attributes:
        id: Unique identifier.
        product_id: ID of the associated product.
        warehouse_id: ID of the warehouse.
        quantity: Stock quantity.
        last_updated: When the stock level was last updated.
    """

    __tablename__ = "product_stock"
    __table_args__ = {"schema": "product"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("product.product.id"), nullable=False, index=True
    )
    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reference.warehouse.id"), nullable=False, index=True
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
        """Return string representation of ProductStock instance.

        Returns:
            String representation including product ID, warehouse ID, and quantity.
        """
        return (
            f"<ProductStock {self.product_id} @ {self.warehouse_id}: {self.quantity}>"
        )


class Fitment(Base):
    """Fitment entity representing vehicle compatibility for a product.

    Attributes:
        id: Unique identifier.
        year: Vehicle year.
        make: Vehicle make.
        model: Vehicle model.
        engine: Engine specification.
        transmission: Transmission specification.
        attributes: Additional fitment attributes.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "fitment"
    __table_args__ = {"schema": "product"}

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
    products: Mapped[List[Product]] = relationship(
        "Product", secondary=product_fitment_association, back_populates="fitments"
    )

    def __repr__(self) -> str:
        """Return string representation of Fitment instance.

        Returns:
            String representation including year, make, and model.
        """
        return f"<Fitment {self.year} {self.make} {self.model}>"
