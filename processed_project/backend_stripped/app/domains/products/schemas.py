from __future__ import annotations
'Product schema definitions.\n\nThis module defines Pydantic schemas for product-related objects,\nincluding products, descriptions, prices, and inventory.\n'
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
class DescriptionType(str, Enum):
    SHORT = 'Short'
    LONG = 'Long'
    KEYWORDS = 'Keywords'
    SLANG = 'Slang'
    NOTES = 'Notes'
class MarketingType(str, Enum):
    BULLET_POINT = 'Bullet Point'
    AD_COPY = 'Ad Copy'
class ProductStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DISCONTINUED = 'discontinued'
    OUT_OF_STOCK = 'out_of_stock'
    PENDING = 'pending'
class ProductDescriptionBase(BaseModel):
    description_type: DescriptionType = Field(..., description='Type of description')
    description: str = Field(..., description='Description text')
class ProductDescriptionCreate(ProductDescriptionBase):
    pass
class ProductDescriptionUpdate(BaseModel):
    description_type: Optional[DescriptionType] = Field(None, description='Type of description')
    description: Optional[str] = Field(None, description='Description text')
class ProductDescriptionInDB(ProductDescriptionBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    product_id: uuid.UUID = Field(..., description='Product ID')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class ProductDescription(ProductDescriptionInDB):
    pass
class ProductMarketingBase(BaseModel):
    marketing_type: MarketingType = Field(..., description='Type of marketing content')
    content: str = Field(..., description='Marketing content')
    position: Optional[int] = Field(None, description='Display order position')
class ProductMarketingCreate(ProductMarketingBase):
    pass
class ProductMarketingUpdate(BaseModel):
    marketing_type: Optional[MarketingType] = Field(None, description='Type of marketing content')
    content: Optional[str] = Field(None, description='Marketing content')
    position: Optional[int] = Field(None, description='Display order position')
class ProductMarketingInDB(ProductMarketingBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    product_id: uuid.UUID = Field(..., description='Product ID')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class ProductMarketing(ProductMarketingInDB):
    pass
class ProductActivityBase(BaseModel):
    status: ProductStatus = Field(..., description='Product status')
    reason: Optional[str] = Field(None, description='Reason for status change')
class ProductActivityCreate(ProductActivityBase):
    pass
class ProductActivityInDB(ProductActivityBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    product_id: uuid.UUID = Field(..., description='Product ID')
    changed_by_id: Optional[uuid.UUID] = Field(None, description='User who changed the status')
    changed_at: datetime = Field(..., description='When the status was changed')
    model_config = ConfigDict(from_attributes=True)
class ProductActivity(ProductActivityInDB):
    changed_by: Optional[Dict[str, Any]] = Field(None, description='User who changed the status')
class BrandBase(BaseModel):
    name: str = Field(..., description='Brand name')
    parent_company_id: Optional[uuid.UUID] = Field(None, description='Parent company ID')
class BrandCreate(BrandBase):
    pass
class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Brand name')
    parent_company_id: Optional[Union[uuid.UUID, None]] = Field(default=..., description='Parent company ID, can be null to remove company association')
class BrandInDB(BrandBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class Brand(BrandInDB):
    parent_company: Optional[Dict[str, Any]] = Field(None, description='Parent company details')
class ProductSupersessionBase(BaseModel):
    old_product_id: uuid.UUID = Field(..., description='ID of replaced product')
    new_product_id: uuid.UUID = Field(..., description='ID of replacement product')
    reason: Optional[str] = Field(None, description='Reason for supersession')
class ProductSupersessionCreate(ProductSupersessionBase):
    pass
class ProductSupersessionUpdate(BaseModel):
    reason: Optional[str] = Field(None, description='Reason for supersession')
class ProductSupersessionInDB(ProductSupersessionBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    changed_at: datetime = Field(..., description='When the supersession was created')
    model_config = ConfigDict(from_attributes=True)
class ProductSupersession(ProductSupersessionInDB):
    old_product: Optional[Dict[str, Any]] = Field(None, description='Old product details')
    new_product: Optional[Dict[str, Any]] = Field(None, description='New product details')
class ProductMeasurementBase(BaseModel):
    manufacturer_id: Optional[uuid.UUID] = Field(None, description='Manufacturer ID')
    length: Optional[float] = Field(None, description='Length measurement')
    width: Optional[float] = Field(None, description='Width measurement')
    height: Optional[float] = Field(None, description='Height measurement')
    weight: Optional[float] = Field(None, description='Weight measurement')
    volume: Optional[float] = Field(None, description='Volume measurement')
    dimensional_weight: Optional[float] = Field(None, description='Dimensional weight')
class ProductMeasurementCreate(ProductMeasurementBase):
    pass
class ProductMeasurementUpdate(ProductMeasurementBase):
    pass
class ProductMeasurementInDB(ProductMeasurementBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    product_id: uuid.UUID = Field(..., description='Product ID')
    effective_date: datetime = Field(..., description='When measurements became effective')
    model_config = ConfigDict(from_attributes=True)
class ProductMeasurement(ProductMeasurementInDB):
    manufacturer: Optional[Dict[str, Any]] = Field(None, description='Manufacturer details')
class ProductStockBase(BaseModel):
    warehouse_id: uuid.UUID = Field(..., description='Warehouse ID')
    quantity: int = Field(0, ge=0, description='Stock quantity')
class ProductStockCreate(ProductStockBase):
    pass
class ProductStockUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=0, description='Stock quantity')
class ProductStockInDB(ProductStockBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    product_id: uuid.UUID = Field(..., description='Product ID')
    last_updated: datetime = Field(..., description='When stock was last updated')
    model_config = ConfigDict(from_attributes=True)
class ProductStock(ProductStockInDB):
    warehouse: Dict[str, Any] = Field(..., description='Warehouse details')
class ProductBase(BaseModel):
    part_number: str = Field(..., description='Product part number')
    part_number_stripped: Optional[str] = Field(None, description='Normalized part number')
    application: Optional[str] = Field(None, description='Product application/use case')
    vintage: bool = Field(False, description='Whether for vintage vehicles')
    late_model: bool = Field(False, description='Whether for late model vehicles')
    soft: bool = Field(False, description='Whether product is soft')
    universal: bool = Field(False, description='Whether product is universal')
    is_active: bool = Field(True, description='Whether product is active')
    @model_validator(mode='after')
    def generate_part_number_stripped(self) -> 'ProductBase':
        if not self.part_number_stripped and self.part_number:
            self.part_number_stripped = ''.join((c for c in self.part_number if c.isalnum())).upper()
        return self
class ProductCreate(ProductBase):
    descriptions: Optional[List[ProductDescriptionCreate]] = Field(None, description='Product descriptions')
    marketing: Optional[List[ProductMarketingCreate]] = Field(None, description='Product marketing content')
class ProductUpdate(BaseModel):
    part_number: Optional[str] = Field(None, description='Product part number')
    application: Optional[str] = Field(None, description='Product application/use case')
    vintage: Optional[bool] = Field(None, description='Whether for vintage vehicles')
    late_model: Optional[bool] = Field(None, description='Whether for late model vehicles')
    soft: Optional[bool] = Field(None, description='Whether product is soft')
    universal: Optional[bool] = Field(None, description='Whether product is universal')
    is_active: Optional[bool] = Field(None, description='Whether product is active')
class ProductInDB(ProductBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class Product(ProductInDB):
    descriptions: List[ProductDescription] = Field([], description='Product descriptions')
    marketing: List[ProductMarketing] = Field([], description='Product marketing content')
    activities: List[ProductActivity] = Field([], description='Product status activities')
    superseded_by: List[ProductSupersession] = Field([], description='Products that replace this one')
    supersedes: List[ProductSupersession] = Field([], description='Products this one replaces')
    measurements: List[ProductMeasurement] = Field([], description='Product measurements')
    stock: List[ProductStock] = Field([], description='Product stock levels')
class FitmentBase(BaseModel):
    year: int = Field(..., description='Vehicle year')
    make: str = Field(..., description='Vehicle make')
    model: str = Field(..., description='Vehicle model')
    engine: Optional[str] = Field(None, description='Engine specification')
    transmission: Optional[str] = Field(None, description='Transmission specification')
    attributes: Dict[str, Any] = Field(default_factory=dict, description='Additional attributes')
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
    year: Optional[int] = Field(None, description='Vehicle year')
    make: Optional[str] = Field(None, description='Vehicle make')
    model: Optional[str] = Field(None, description='Vehicle model')
    engine: Optional[str] = Field(None, description='Engine specification')
    transmission: Optional[str] = Field(None, description='Transmission specification')
    attributes: Optional[Dict[str, Any]] = Field(None, description='Additional attributes')
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
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class Fitment(FitmentInDB):
    pass
class PaginatedResponse(BaseModel):
    items: List[Any] = Field(..., description='List of items')
    total: int = Field(..., description='Total number of items')
    page: int = Field(..., description='Current page number')
    page_size: int = Field(..., description='Number of items per page')
    pages: int = Field(..., description='Total number of pages')
class ProductListResponse(PaginatedResponse):
    items: List[Product] = Field(..., description='List of products')
class FitmentListResponse(PaginatedResponse):
    items: List[Fitment] = Field(..., description='List of fitments')