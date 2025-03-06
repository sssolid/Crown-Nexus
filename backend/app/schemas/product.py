# backend/app/schemas/product.py
"""
Product and catalog schemas.

This module provides Pydantic schemas for product-related data validation
and serialization. The schemas support:
- Request validation for products, categories, and fitments
- Response serialization with properly structured data
- Pagination for list responses
- Validation rules for specific fields like year ranges

These schemas ensure data integrity throughout the application's
product catalog functionality.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


# Product Schemas
class ProductBase(BaseModel):
    """
    Base schema for Product data.

    Defines common fields used across product-related schemas.

    Attributes:
        sku: Stock keeping unit
        name: Product name
        description: Product description (optional)
        part_number: Manufacturer part number (optional)
        category_id: Reference to category (optional)
        attributes: Additional product attributes
        is_active: Whether the product is active
    """
    sku: str
    name: str
    description: Optional[str] = None
    part_number: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True


class ProductCreate(ProductBase):
    """
    Schema for creating a new Product.

    Extends the base product schema for creation requests.
    """
    pass


class ProductUpdate(BaseModel):
    """
    Schema for updating an existing Product.

    Defines fields that can be updated on a product, with all
    fields being optional to allow partial updates.

    Attributes:
        sku: Stock keeping unit (optional)
        name: Product name (optional)
        description: Product description (optional)
        part_number: Manufacturer part number (optional)
        category_id: Reference to category (optional, can be set to None)
        attributes: Additional product attributes (optional)
        is_active: Whether the product is active (optional)
    """
    sku: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    part_number: Optional[str] = None
    category_id: Optional[Union[uuid.UUID, None]] = Field(
        default=..., description="Category ID, can be null to remove from category"
    )
    attributes: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


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
    It extends the database schema with the associated category.

    Attributes:
        category: Associated category information (optional)
    """
    category: Optional[Category] = None


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
    It extends the database schema with any additional computed fields.
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
