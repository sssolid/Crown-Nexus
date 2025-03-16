from __future__ import annotations
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
    description_type: DescriptionType
    description: str
class ProductDescriptionCreate(ProductDescriptionBase):
    pass
class ProductDescriptionUpdate(BaseModel):
    description_type: Optional[DescriptionType] = None
    description: Optional[str] = None
class ProductDescriptionInDB(ProductDescriptionBase):
    id: uuid.UUID
    product_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class ProductDescription(ProductDescriptionInDB):
    pass
class ProductMarketingBase(BaseModel):
    marketing_type: MarketingType
    content: str
    position: Optional[int] = None
class ProductMarketingCreate(ProductMarketingBase):
    pass
class ProductMarketingUpdate(BaseModel):
    marketing_type: Optional[MarketingType] = None
    content: Optional[str] = None
    position: Optional[int] = None
class ProductMarketingInDB(ProductMarketingBase):
    id: uuid.UUID
    product_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class ProductMarketing(ProductMarketingInDB):
    pass
class ProductActivityBase(BaseModel):
    status: ProductStatus
    reason: Optional[str] = None
class ProductActivityCreate(ProductActivityBase):
    pass
class ProductActivityInDB(ProductActivityBase):
    id: uuid.UUID
    product_id: uuid.UUID
    changed_by_id: Optional[uuid.UUID] = None
    changed_at: datetime
    model_config = ConfigDict(from_attributes=True)
class ProductActivity(ProductActivityInDB):
    changed_by: Optional[Dict[str, Any]] = None
class BrandBase(BaseModel):
    name: str
    parent_company_id: Optional[uuid.UUID] = None
class BrandCreate(BrandBase):
    pass
class BrandUpdate(BaseModel):
    name: Optional[str] = None
    parent_company_id: Optional[Union[uuid.UUID, None]] = Field(default=..., description='Parent company ID, can be null')
class BrandInDB(BrandBase):
    id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class Brand(BrandInDB):
    parent_company: Optional[Dict[str, Any]] = None
class ProductSupersessionBase(BaseModel):
    old_product_id: uuid.UUID
    new_product_id: uuid.UUID
    reason: Optional[str] = None
class ProductSupersessionCreate(ProductSupersessionBase):
    pass
class ProductSupersessionUpdate(BaseModel):
    reason: Optional[str] = None
class ProductSupersessionInDB(ProductSupersessionBase):
    id: uuid.UUID
    changed_at: datetime
    model_config = ConfigDict(from_attributes=True)
class ProductSupersession(ProductSupersessionInDB):
    old_product: Optional[Dict[str, Any]] = None
    new_product: Optional[Dict[str, Any]] = None
class ProductMeasurementBase(BaseModel):
    manufacturer_id: Optional[uuid.UUID] = None
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    dimensional_weight: Optional[float] = None
class ProductMeasurementCreate(ProductMeasurementBase):
    pass
class ProductMeasurementUpdate(ProductMeasurementBase):
    pass
class ProductMeasurementInDB(ProductMeasurementBase):
    id: uuid.UUID
    product_id: uuid.UUID
    effective_date: datetime
    model_config = ConfigDict(from_attributes=True)
class ProductMeasurement(ProductMeasurementInDB):
    manufacturer: Optional[Dict[str, Any]] = None
class ProductStockBase(BaseModel):
    warehouse_id: uuid.UUID
    quantity: int = Field(ge=0, default=0)
class ProductStockCreate(ProductStockBase):
    pass
class ProductStockUpdate(BaseModel):
    quantity: Optional[int] = Field(ge=0, default=None)
class ProductStockInDB(ProductStockBase):
    id: uuid.UUID
    product_id: uuid.UUID
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)
class ProductStock(ProductStockInDB):
    warehouse: Dict[str, Any]
class ProductBase(BaseModel):
    part_number: str
    part_number_stripped: Optional[str] = None
    application: Optional[str] = None
    vintage: bool = False
    late_model: bool = False
    soft: bool = False
    universal: bool = False
    is_active: bool = True
    @model_validator(mode='after')
    def generate_part_number_stripped(self) -> 'ProductBase':
        if not self.part_number_stripped and self.part_number:
            self.part_number_stripped = ''.join((c for c in self.part_number if c.isalnum())).upper()
        return self
class ProductCreate(ProductBase):
    descriptions: Optional[List[ProductDescriptionCreate]] = None
    marketing: Optional[List[ProductMarketingCreate]] = None
class ProductUpdate(BaseModel):
    part_number: Optional[str] = None
    application: Optional[str] = None
    vintage: Optional[bool] = None
    late_model: Optional[bool] = None
    soft: Optional[bool] = None
    universal: Optional[bool] = None
    is_active: Optional[bool] = None
class ProductInDB(ProductBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
class Product(ProductInDB):
    descriptions: List[ProductDescription] = []
    marketing: List[ProductMarketing] = []
    activities: List[ProductActivity] = []
    superseded_by: List[ProductSupersession] = []
    supersedes: List[ProductSupersession] = []
    measurements: List[ProductMeasurement] = []
    stock: List[ProductStock] = []
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