from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator
class CategoryBase(BaseModel):
    name: str
    slug: str
    parent_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
class CategoryCreate(CategoryBase):
    pass
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[Union[uuid.UUID, None]] = Field(default=..., description='Parent category ID, can be null to make a top-level category')
    description: Optional[str] = None
class CategoryInDB(CategoryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
class Category(CategoryInDB):
    children: List['Category'] = []
    @property
    def has_children(self) -> bool:
        return len(self.children) > 0
class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    part_number: Optional[str] = None
    category_id: Optional[uuid.UUID] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
class ProductCreate(ProductBase):
    pass
class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    part_number: Optional[str] = None
    category_id: Optional[Union[uuid.UUID, None]] = Field(default=..., description='Category ID, can be null to remove from category')
    attributes: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
class ProductInDB(ProductBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
class Product(ProductInDB):
    category: Optional[Category] = None
class FitmentBase(BaseModel):
    year: int
    make: str
    model: str
    engine: Optional[str] = None
    transmission: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    @field_validator('year')
    @classmethod
    def validate_year(cls, v: int) -> int:
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 2:
            raise ValueError(f'Year must be between 1900 and {current_year + 2}')
        return v
class FitmentCreate(FitmentBase):
    pass
class FitmentUpdate(BaseModel):
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    engine: Optional[str] = None
    transmission: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    @field_validator('year')
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 2:
            raise ValueError(f'Year must be between 1900 and {current_year + 2}')
        return v
class FitmentInDB(FitmentBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
class Fitment(FitmentInDB):
    pass
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    pages: int
class ProductListResponse(PaginatedResponse):
    items: List[Product]
class FitmentListResponse(PaginatedResponse):
    items: List[Fitment]
Category.model_rebuild()