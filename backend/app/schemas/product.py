from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Category Schemas
class CategoryBase(BaseModel):
    """Base schema for Category data."""
    name: str
    slug: str
    parent_id: Optional[uuid.UUID] = None
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a new Category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating an existing Category."""
    name: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[Union[uuid.UUID, None]] = Field(default=...)
    description: Optional[str] = None


class CategoryInDB(CategoryBase):
    """Schema for Category as stored in the database."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Category(CategoryInDB):
    """Schema for Category responses."""
    children: List["Category"] = []


# Product Schemas
class ProductBase(BaseModel):
    """Base schema for Product data."""
    sku: str
    name: str
    description: Optional[str] = None
    part_number: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True


class ProductCreate(ProductBase):
    """Schema for creating a new Product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing Product."""
    sku: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    part_number: Optional[str] = None
    category_id: Optional[Union[uuid.UUID, None]] = Field(default=...)
    attributes: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ProductInDB(ProductBase):
    """Schema for Product as stored in the database."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Product(ProductInDB):
    """Schema for Product responses."""
    category: Optional[Category] = None


# Fitment Schemas
class FitmentBase(BaseModel):
    """Base schema for Fitment data."""
    year: int
    make: str
    model: str
    engine: Optional[str] = None
    transmission: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        """Validate the year is within a reasonable range."""
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 2:  # Allow up to 2 years in the future for new models
            raise ValueError(f"Year must be between 1900 and {current_year + 2}")
        return v


class FitmentCreate(FitmentBase):
    """Schema for creating a new Fitment."""
    pass


class FitmentUpdate(BaseModel):
    """Schema for updating an existing Fitment."""
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    engine: Optional[str] = None
    transmission: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

    @field_validator("year")
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        """Validate the year is within a reasonable range if provided."""
        if v is None:
            return v
            
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 2:
            raise ValueError(f"Year must be between 1900 and {current_year + 2}")
        return v


class FitmentInDB(FitmentBase):
    """Schema for Fitment as stored in the database."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Fitment(FitmentInDB):
    """Schema for Fitment responses."""
    pass


# Pagination schemas
class PaginatedResponse(BaseModel):
    """Generic paginated response schema."""
    items: List[Any]
    total: int
    page: int
    page_size: int
    pages: int


class ProductListResponse(PaginatedResponse):
    """Paginated response for product listings."""
    items: List[Product]


class FitmentListResponse(PaginatedResponse):
    """Paginated response for fitment listings."""
    items: List[Fitment]


# Update forward references for nested models
Category.model_rebuild()
