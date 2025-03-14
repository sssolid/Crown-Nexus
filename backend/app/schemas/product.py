# backend/app/schemas/product.py
"""
Product catalog schemas.

This module provides Pydantic schemas for product-related data validation
and serialization. The schemas support:
- Request validation for products, categories, and related entities
- Response serialization with properly structured data
- Pagination for list responses
- Validation rules for specific fields
- Support for the enhanced data model

These schemas ensure data integrity throughout the application's
product catalog functionality.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class DescriptionType(str, Enum):
    """
    Types of product descriptions.

    Defines the different categories of descriptions that can be associated
    with a product.
    """
    SHORT = "Short"
    LONG = "Long"
    KEYWORDS = "Keywords"
    SLANG = "Slang"
    NOTES = "Notes"


class MarketingType(str, Enum):
    """
    Types of product marketing content.

    Defines the different categories of marketing content that can be
    associated with a product.
    """
    BULLET_POINT = "Bullet Point"
    AD_COPY = "Ad Copy"


class ProductStatus(str, Enum):
    """
    Product status options.

    Defines the possible status values for product activities.
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
    OUT_OF_STOCK = "out_of_stock"
    PENDING = "pending"


# Category Schemas
class CategoryBase(BaseModel):
    """
    Base schema for Category data.

    Defines common fields used across category-related schemas.

    Attributes:
        name: Category name
        slug: URL-friendly version of name
        parent_id: Reference to parent category (optional)
        description: Category description (optional)
    """
    name: str
    slug: str
    parent_id: Optional[uuid.UUID] = None
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """
    Schema for creating a new Category.

    Extends the base category schema for creation requests.
    """
    pass


class CategoryUpdate(BaseModel):
    """
    Schema for updating an existing Category.

    Defines fields that can be updated on a category, with all
    fields being optional to allow partial updates.

    Attributes:
        name: Category name (optional)
        slug: URL-friendly version of name (optional)
        parent_id: Reference to parent category (optional, can be set to None)
        description: Category description (optional)
    """
    name: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[Union[uuid.UUID, None]] = Field(
        default=..., description="Parent category ID, can be null to make a top-level category"
    )
    description: Optional[str] = None


class CategoryInDB(CategoryBase):
    """
    Schema for Category as stored in the database.

    Extends the base category schema with database-specific fields.

    Attributes:
        id: Category UUID
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Category(CategoryInDB):
    """
    Schema for Category responses.

    This schema is used for API responses returning category data.
    It extends the database schema with child categories.

    Attributes:
        children: List of child categories
    """
    children: List["Category"] = []

    @property
    def has_children(self) -> bool:
        """
        Check if the category has child categories.

        Returns:
            bool: True if the category has children, False otherwise
        """
        return len(self.children) > 0


# Description Schemas
class ProductDescriptionBase(BaseModel):
    """
    Base schema for Product Description data.

    Defines common fields used across product description schemas.

    Attributes:
        description_type: Type of description
        description: Description content
    """
    description_type: DescriptionType
    description: str


class ProductDescriptionCreate(ProductDescriptionBase):
    """
    Schema for creating a new Product Description.

    Extends the base product description schema for creation requests.
    """
    pass


class ProductDescriptionUpdate(BaseModel):
    """
    Schema for updating an existing Product Description.

    Defines fields that can be updated on a product description.

    Attributes:
        description_type: Type of description (optional)
        description: Description content (optional)
    """
    description_type: Optional[DescriptionType] = None
    description: Optional[str] = None


class ProductDescriptionInDB(ProductDescriptionBase):
    """
    Schema for Product Description as stored in the database.

    Extends the base product description schema with database-specific fields.

    Attributes:
        id: Description UUID
        product_id: Product UUID
        created_at: Creation timestamp
    """
    id: uuid.UUID
    product_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductDescription(ProductDescriptionInDB):
    """
    Schema for Product Description responses.

    This schema is used for API responses returning product description data.
    """
    pass


# Marketing Schemas
class ProductMarketingBase(BaseModel):
    """
    Base schema for Product Marketing data.

    Defines common fields used across product marketing schemas.

    Attributes:
        marketing_type: Type of marketing content
        content: Marketing content
        position: Order for display (optional)
    """
    marketing_type: MarketingType
    content: str
    position: Optional[int] = None


class ProductMarketingCreate(ProductMarketingBase):
    """
    Schema for creating a new Product Marketing.

    Extends the base product marketing schema for creation requests.
    """
    pass


class ProductMarketingUpdate(BaseModel):
    """
    Schema for updating an existing Product Marketing.

    Defines fields that can be updated on product marketing content.

    Attributes:
        marketing_type: Type of marketing content (optional)
        content: Marketing content (optional)
        position: Order for display (optional)
    """
    marketing_type: Optional[MarketingType] = None
    content: Optional[str] = None
    position: Optional[int] = None


class ProductMarketingInDB(ProductMarketingBase):
    """
    Schema for Product Marketing as stored in the database.

    Extends the base product marketing schema with database-specific fields.

    Attributes:
        id: Marketing UUID
        product_id: Product UUID
        created_at: Creation timestamp
    """
    id: uuid.UUID
    product_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductMarketing(ProductMarketingInDB):
    """
    Schema for Product Marketing responses.

    This schema is used for API responses returning product marketing data.
    """
    pass


# Activity Schemas
class ProductActivityBase(BaseModel):
    """
    Base schema for Product Activity data.

    Defines common fields used across product activity schemas.

    Attributes:
        status: Product status
        reason: Reason for status change (optional)
    """
    status: ProductStatus
    reason: Optional[str] = None


class ProductActivityCreate(ProductActivityBase):
    """
    Schema for creating a new Product Activity.

    Extends the base product activity schema for creation requests.
    """
    pass


class ProductActivityInDB(ProductActivityBase):
    """
    Schema for Product Activity as stored in the database.

    Extends the base product activity schema with database-specific fields.

    Attributes:
        id: Activity UUID
        product_id: Product UUID
        changed_by_id: User UUID who made the change (optional)
        changed_at: When the change occurred
    """
    id: uuid.UUID
    product_id: uuid.UUID
    changed_by_id: Optional[uuid.UUID] = None
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductActivity(ProductActivityInDB):
    """
    Schema for Product Activity responses.

    This schema is used for API responses returning product activity data.

    Attributes:
        changed_by: User who made the change (optional)
    """
    changed_by: Optional[Dict[str, Any]] = None


# Brand Schemas
class BrandBase(BaseModel):
    """
    Base schema for Brand data.

    Defines common fields used across brand schemas.

    Attributes:
        name: Brand name
        parent_company_id: Parent company ID (optional)
    """
    name: str
    parent_company_id: Optional[uuid.UUID] = None


class BrandCreate(BrandBase):
    """
    Schema for creating a new Brand.

    Extends the base brand schema for creation requests.
    """
    pass


class BrandUpdate(BaseModel):
    """
    Schema for updating an existing Brand.

    Defines fields that can be updated on a brand.

    Attributes:
        name: Brand name (optional)
        parent_company_id: Parent company ID (optional)
    """
    name: Optional[str] = None
    parent_company_id: Optional[Union[uuid.UUID, None]] = Field(
        default=..., description="Parent company ID, can be null"
    )


class BrandInDB(BrandBase):
    """
    Schema for Brand as stored in the database.

    Extends the base brand schema with database-specific fields.

    Attributes:
        id: Brand UUID
        created_at: Creation timestamp
    """
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Brand(BrandInDB):
    """
    Schema for Brand responses.

    This schema is used for API responses returning brand data.

    Attributes:
        parent_company: Parent company information (optional)
    """
    parent_company: Optional[Dict[str, Any]] = None


# Supersession Schemas
class ProductSupersessionBase(BaseModel):
    """
    Base schema for Product Supersession data.

    Defines common fields used across product supersession schemas.

    Attributes:
        old_product_id: Product being replaced
        new_product_id: Replacement product
        reason: Explanation of why the product was superseded (optional)
    """
    old_product_id: uuid.UUID
    new_product_id: uuid.UUID
    reason: Optional[str] = None


class ProductSupersessionCreate(ProductSupersessionBase):
    """
    Schema for creating a new Product Supersession.

    Extends the base product supersession schema for creation requests.
    """
    pass


class ProductSupersessionUpdate(BaseModel):
    """
    Schema for updating an existing Product Supersession.

    Defines fields that can be updated on a product supersession.

    Attributes:
        reason: Explanation of why the product was superseded (optional)
    """
    reason: Optional[str] = None


class ProductSupersessionInDB(ProductSupersessionBase):
    """
    Schema for Product Supersession as stored in the database.

    Extends the base product supersession schema with database-specific fields.

    Attributes:
        id: Supersession UUID
        changed_at: When the change occurred
    """
    id: uuid.UUID
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductSupersession(ProductSupersessionInDB):
    """
    Schema for Product Supersession responses.

    This schema is used for API responses returning product supersession data.

    Attributes:
        old_product: Basic information about the product being replaced
        new_product: Basic information about the replacement product
    """
    old_product: Optional[Dict[str, Any]] = None
    new_product: Optional[Dict[str, Any]] = None


# Measurement Schemas
class ProductMeasurementBase(BaseModel):
    """
    Base schema for Product Measurement data.

    Defines common fields used across product measurement schemas.

    Attributes:
        manufacturer_id: Manufacturer UUID (optional)
        length: Length in inches (optional)
        width: Width in inches (optional)
        height: Height in inches (optional)
        weight: Weight in pounds (optional)
        volume: Volume in cubic inches (optional)
        dimensional_weight: DIM weight calculation (optional)
    """
    manufacturer_id: Optional[uuid.UUID] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    dimensional_weight: Optional[float] = None


class ProductMeasurementCreate(ProductMeasurementBase):
    """
    Schema for creating a new Product Measurement.

    Extends the base product measurement schema for creation requests.
    """
    pass


class ProductMeasurementUpdate(ProductMeasurementBase):
    """
    Schema for updating an existing Product Measurement.

    Fields are the same as the base schema since all are optional.
    """
    pass


class ProductMeasurementInDB(ProductMeasurementBase):
    """
    Schema for Product Measurement as stored in the database.

    Extends the base product measurement schema with database-specific fields.

    Attributes:
        id: Measurement UUID
        product_id: Product UUID
        effective_date: When measurements become effective
    """
    id: uuid.UUID
    product_id: uuid.UUID
    effective_date: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductMeasurement(ProductMeasurementInDB):
    """
    Schema for Product Measurement responses.

    This schema is used for API responses returning product measurement data.

    Attributes:
        manufacturer: Manufacturer information (optional)
    """
    manufacturer: Optional[Dict[str, Any]] = None


# Stock Schemas
class ProductStockBase(BaseModel):
    """
    Base schema for Product Stock data.

    Defines common fields used across product stock schemas.

    Attributes:
        warehouse_id: Warehouse UUID
        quantity: Quantity in stock
    """
    warehouse_id: uuid.UUID
    quantity: int = Field(ge=0, default=0)


class ProductStockCreate(ProductStockBase):
    """
    Schema for creating a new Product Stock.

    Extends the base product stock schema for creation requests.
    """
    pass


class ProductStockUpdate(BaseModel):
    """
    Schema for updating an existing Product Stock.

    Defines fields that can be updated on product stock.

    Attributes:
        quantity: Quantity in stock (optional)
    """
    quantity: Optional[int] = Field(ge=0, default=None)


class ProductStockInDB(ProductStockBase):
    """
    Schema for Product Stock as stored in the database.

    Extends the base product stock schema with database-specific fields.

    Attributes:
        id: Stock UUID
        product_id: Product UUID
        last_updated: Last stock update timestamp
    """
    id: uuid.UUID
    product_id: uuid.UUID
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductStock(ProductStockInDB):
    """
    Schema for Product Stock responses.

    This schema is used for API responses returning product stock data.

    Attributes:
        warehouse: Warehouse information
    """
    warehouse: Dict[str, Any]


# Product Base Schema
class ProductBase(BaseModel):
    """
    Base schema for Product data.

    Defines common fields used across product schemas.

    Attributes:
        part_number: Unique identifier for the product
        part_number_stripped: Alphanumeric version of part_number (auto-generated)
        application: Unformatted data for vehicle fitment applications (optional)
        vintage: Vintage fitments flag
        late_model: Late model fitments flag
        soft: Soft good flag
        universal: Universal fit flag
        is_active: Whether the product is active
        category_id: Reference to category (optional)
    """
    part_number: str
    part_number_stripped: Optional[str] = None
    application: Optional[str] = None
    vintage: bool = False
    late_model: bool = False
    soft: bool = False
    universal: bool = False
    is_active: bool = True
    category_id: Optional[uuid.UUID] = None

    @model_validator(mode='after')
    def generate_part_number_stripped(self) -> 'ProductBase':
        """
        Generate the stripped part number if not provided.

        Returns:
            ProductBase: Validated model instance
        """
        if not self.part_number_stripped and self.part_number:
            self.part_number_stripped = ''.join(
                c for c in self.part_number if c.isalnum()
            ).upper()
        return self


class ProductCreate(ProductBase):
    """
    Schema for creating a new Product.

    Extends the base product schema for creation requests.

    Attributes:
        descriptions: List of product descriptions (optional)
        marketing: List of marketing content (optional)
    """
    descriptions: Optional[List[ProductDescriptionCreate]] = None
    marketing: Optional[List[ProductMarketingCreate]] = None


class ProductUpdate(BaseModel):
    """
    Schema for updating an existing Product.

    Defines fields that can be updated on a product, with all
    fields being optional to allow partial updates.

    Attributes:
        part_number: Unique identifier for the product (optional)
        application: Unformatted data for vehicle fitment applications (optional)
        vintage: Vintage fitments flag (optional)
        late_model: Late model fitments flag (optional)
        soft: Soft good flag (optional)
        universal: Universal fit flag (optional)
        is_active: Whether the product is active (optional)
        category_id: Reference to category (optional, can be set to None)
    """
    part_number: Optional[str] = None
    application: Optional[str] = None
    vintage: Optional[bool] = None
    late_model: Optional[bool] = None
    soft: Optional[bool] = None
    universal: Optional[bool] = None
    is_active: Optional[bool] = None
    category_id: Optional[Union[uuid.UUID, None]] = Field(
        default=..., description="Category ID, can be null to remove from category"
    )


class ProductInDB(ProductBase):
    """
    Schema for Product as stored in the database.

    Extends the base product schema with database-specific fields.

    Attributes:
        id: Product UUID
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Product(ProductInDB):
    """
    Schema for Product responses.

    This schema is used for API responses returning product data.
    It extends the database schema with related entities.

    Attributes:
        category: Associated category information (optional)
        descriptions: List of product descriptions
        marketing: List of marketing content
        activities: List of product activities
        superseded_by: List of products this product is superseded by
        supersedes: List of products this product supersedes
        measurements: List of product measurements
        stock: List of product stock information
    """
    category: Optional[Category] = None
    descriptions: List[ProductDescription] = []
    marketing: List[ProductMarketing] = []
    activities: List[ProductActivity] = []
    superseded_by: List[ProductSupersession] = []
    supersedes: List[ProductSupersession] = []
    measurements: List[ProductMeasurement] = []
    stock: List[ProductStock] = []


# Fitment Schemas
class FitmentBase(BaseModel):
    """
    Base schema for Fitment data.

    Defines common fields used across fitment-related schemas.

    Attributes:
        year: Vehicle model year
        make: Vehicle manufacturer
        model: Vehicle model name
        engine: Engine specification (optional)
        transmission: Transmission type (optional)
        attributes: Additional fitment attributes
    """
    year: int
    make: str
    model: str
    engine: Optional[str] = None
    transmission: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        """
        Validate the year is within a reasonable range.

        Args:
            v: Year value

        Returns:
            int: Validated year

        Raises:
            ValueError: If year is outside reasonable range
        """
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 2:  # Allow up to 2 years in the future for new models
            raise ValueError(f"Year must be between 1900 and {current_year + 2}")
        return v


class FitmentCreate(FitmentBase):
    """
    Schema for creating a new Fitment.

    Extends the base fitment schema for creation requests.
    """
    pass


class FitmentUpdate(BaseModel):
    """
    Schema for updating an existing Fitment.

    Defines fields that can be updated on a fitment, with all
    fields being optional to allow partial updates.

    Attributes:
        year: Vehicle model year (optional)
        make: Vehicle manufacturer (optional)
        model: Vehicle model name (optional)
        engine: Engine specification (optional)
        transmission: Transmission type (optional)
        attributes: Additional fitment attributes (optional)
    """
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    engine: Optional[str] = None
    transmission: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

    @field_validator("year")
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        """
        Validate the year is within a reasonable range if provided.

        Args:
            v: Year value (optional)

        Returns:
            Optional[int]: Validated year

        Raises:
            ValueError: If year is outside reasonable range
        """
        if v is None:
            return v

        current_year = datetime.now().year
        if v < 1900 or v > current_year + 2:
            raise ValueError(f"Year must be between 1900 and {current_year + 2}")
        return v


class FitmentInDB(FitmentBase):
    """
    Schema for Fitment as stored in the database.

    Extends the base fitment schema with database-specific fields.

    Attributes:
        id: Fitment UUID
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Fitment(FitmentInDB):
    """
    Schema for Fitment responses.

    This schema is used for API responses returning fitment data.
    """
    pass


# Pagination schemas
class PaginatedResponse(BaseModel):
    """
    Generic paginated response schema.

    This schema provides a structure for paginated list responses,
    including metadata about the pagination.

    Attributes:
        items: List of items
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        pages: Total number of pages
    """
    items: List[Any]
    total: int
    page: int
    page_size: int
    pages: int


class ProductListResponse(PaginatedResponse):
    """
    Paginated response for product listings.

    This schema specializes the generic paginated response for product listings.

    Attributes:
        items: List of products
    """
    items: List[Product]


class FitmentListResponse(PaginatedResponse):
    """
    Paginated response for fitment listings.

    This schema specializes the generic paginated response for fitment listings.

    Attributes:
        items: List of fitments
    """
    items: List[Fitment]


# Update forward references for nested models
Category.model_rebuild()
