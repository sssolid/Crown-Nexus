from __future__ import annotations

"""Product schema definitions.

This module defines Pydantic schemas for product-related objects,
including products, descriptions, prices, and inventory.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class DescriptionType(str, Enum):
    """Types of product descriptions.

    Attributes:
        SHORT: Brief product description.
        LONG: Detailed product description.
        KEYWORDS: Keywords for search.
        SLANG: Colloquial terms for the product.
        NOTES: Internal notes about the product.
    """

    SHORT = "Short"
    LONG = "Long"
    KEYWORDS = "Keywords"
    SLANG = "Slang"
    NOTES = "Notes"


class MarketingType(str, Enum):
    """Types of product marketing content.

    Attributes:
        BULLET_POINT: Bullet point features.
        AD_COPY: Advertising copy.
    """

    BULLET_POINT = "Bullet Point"
    AD_COPY = "Ad Copy"


class ProductStatus(str, Enum):
    """Product status values.

    Attributes:
        ACTIVE: Product is active and available.
        INACTIVE: Product is temporarily inactive.
        DISCONTINUED: Product is permanently discontinued.
        OUT_OF_STOCK: Product is out of stock.
        PENDING: Product is pending approval or release.
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
    OUT_OF_STOCK = "out_of_stock"
    PENDING = "pending"


class ProductDescriptionBase(BaseModel):
    """Base schema for ProductDescription data.

    Attributes:
        description_type: Type of description.
        description: The description text.
    """

    description_type: DescriptionType = Field(..., description="Type of description")
    description: str = Field(..., description="Description text")


class ProductDescriptionCreate(ProductDescriptionBase):
    """Schema for creating a new ProductDescription."""

    pass


class ProductDescriptionUpdate(BaseModel):
    """Schema for updating an existing ProductDescription.

    All fields are optional to allow partial updates.
    """

    description_type: Optional[DescriptionType] = Field(
        None, description="Type of description"
    )
    description: Optional[str] = Field(None, description="Description text")


class ProductDescriptionInDB(ProductDescriptionBase):
    """Schema for ProductDescription data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    product_id: uuid.UUID = Field(..., description="Product ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class ProductDescription(ProductDescriptionInDB):
    """Schema for complete ProductDescription data in API responses."""

    pass


class ProductMarketingBase(BaseModel):
    """Base schema for ProductMarketing data.

    Attributes:
        marketing_type: Type of marketing content.
        content: The marketing content.
        position: Display order position.
    """

    marketing_type: MarketingType = Field(..., description="Type of marketing content")
    content: str = Field(..., description="Marketing content")
    position: Optional[int] = Field(None, description="Display order position")


class ProductMarketingCreate(ProductMarketingBase):
    """Schema for creating a new ProductMarketing."""

    pass


class ProductMarketingUpdate(BaseModel):
    """Schema for updating an existing ProductMarketing.

    All fields are optional to allow partial updates.
    """

    marketing_type: Optional[MarketingType] = Field(
        None, description="Type of marketing content"
    )
    content: Optional[str] = Field(None, description="Marketing content")
    position: Optional[int] = Field(None, description="Display order position")


class ProductMarketingInDB(ProductMarketingBase):
    """Schema for ProductMarketing data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    product_id: uuid.UUID = Field(..., description="Product ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class ProductMarketing(ProductMarketingInDB):
    """Schema for complete ProductMarketing data in API responses."""

    pass


class ProductActivityBase(BaseModel):
    """Base schema for ProductActivity data.

    Attributes:
        status: Product status.
        reason: Reason for the status change.
    """

    status: ProductStatus = Field(..., description="Product status")
    reason: Optional[str] = Field(None, description="Reason for status change")


class ProductActivityCreate(ProductActivityBase):
    """Schema for creating a new ProductActivity."""

    pass


class ProductActivityInDB(ProductActivityBase):
    """Schema for ProductActivity data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    product_id: uuid.UUID = Field(..., description="Product ID")
    changed_by_id: Optional[uuid.UUID] = Field(
        None, description="User who changed the status"
    )
    changed_at: datetime = Field(..., description="When the status was changed")

    model_config = ConfigDict(from_attributes=True)


class ProductActivity(ProductActivityInDB):
    """Schema for complete ProductActivity data in API responses.

    Includes related entities like user details.
    """

    changed_by: Optional[Dict[str, Any]] = Field(
        None, description="User who changed the status"
    )


class BrandBase(BaseModel):
    """Base schema for Brand data.

    Attributes:
        name: Brand name.
        parent_company_id: ID of the parent company.
    """

    name: str = Field(..., description="Brand name")
    parent_company_id: Optional[uuid.UUID] = Field(
        None, description="Parent company ID"
    )


class BrandCreate(BrandBase):
    """Schema for creating a new Brand."""

    pass


class BrandUpdate(BaseModel):
    """Schema for updating an existing Brand.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Brand name")
    parent_company_id: Optional[Union[uuid.UUID, None]] = Field(
        default=...,
        description="Parent company ID, can be null to remove company association",
    )


class BrandInDB(BrandBase):
    """Schema for Brand data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class Brand(BrandInDB):
    """Schema for complete Brand data in API responses.

    Includes related entities like parent company details.
    """

    parent_company: Optional[Dict[str, Any]] = Field(
        None, description="Parent company details"
    )


class ProductSupersessionBase(BaseModel):
    """Base schema for ProductSupersession data.

    Attributes:
        old_product_id: ID of the product being replaced.
        new_product_id: ID of the replacement product.
        reason: Reason for the supersession.
    """

    old_product_id: uuid.UUID = Field(..., description="ID of replaced product")
    new_product_id: uuid.UUID = Field(..., description="ID of replacement product")
    reason: Optional[str] = Field(None, description="Reason for supersession")


class ProductSupersessionCreate(ProductSupersessionBase):
    """Schema for creating a new ProductSupersession."""

    pass


class ProductSupersessionUpdate(BaseModel):
    """Schema for updating an existing ProductSupersession.

    All fields are optional to allow partial updates.
    """

    reason: Optional[str] = Field(None, description="Reason for supersession")


class ProductSupersessionInDB(ProductSupersessionBase):
    """Schema for ProductSupersession data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    changed_at: datetime = Field(..., description="When the supersession was created")

    model_config = ConfigDict(from_attributes=True)


class ProductSupersession(ProductSupersessionInDB):
    """Schema for complete ProductSupersession data in API responses.

    Includes related entities like product details.
    """

    old_product: Optional[Dict[str, Any]] = Field(
        None, description="Old product details"
    )
    new_product: Optional[Dict[str, Any]] = Field(
        None, description="New product details"
    )


class ProductMeasurementBase(BaseModel):
    """Base schema for ProductMeasurement data.

    Attributes:
        manufacturer_id: ID of the manufacturer.
        length: Length measurement.
        width: Width measurement.
        height: Height measurement.
        weight: Weight measurement.
        volume: Volume measurement.
        dimensional_weight: Dimensional weight for shipping calculations.
    """

    manufacturer_id: Optional[uuid.UUID] = Field(None, description="Manufacturer ID")
    length: Optional[float] = Field(None, description="Length measurement")
    width: Optional[float] = Field(None, description="Width measurement")
    height: Optional[float] = Field(None, description="Height measurement")
    weight: Optional[float] = Field(None, description="Weight measurement")
    volume: Optional[float] = Field(None, description="Volume measurement")
    dimensional_weight: Optional[float] = Field(None, description="Dimensional weight")


class ProductMeasurementCreate(ProductMeasurementBase):
    """Schema for creating a new ProductMeasurement."""

    pass


class ProductMeasurementUpdate(ProductMeasurementBase):
    """Schema for updating an existing ProductMeasurement.

    All fields are optional to allow partial updates.
    """

    pass


class ProductMeasurementInDB(ProductMeasurementBase):
    """Schema for ProductMeasurement data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    product_id: uuid.UUID = Field(..., description="Product ID")
    effective_date: datetime = Field(
        ..., description="When measurements became effective"
    )

    model_config = ConfigDict(from_attributes=True)


class ProductMeasurement(ProductMeasurementInDB):
    """Schema for complete ProductMeasurement data in API responses.

    Includes related entities like manufacturer details.
    """

    manufacturer: Optional[Dict[str, Any]] = Field(
        None, description="Manufacturer details"
    )


class ProductStockBase(BaseModel):
    """Base schema for ProductStock data.

    Attributes:
        warehouse_id: ID of the warehouse.
        quantity: Stock quantity.
    """

    warehouse_id: uuid.UUID = Field(..., description="Warehouse ID")
    quantity: int = Field(0, ge=0, description="Stock quantity")


class ProductStockCreate(ProductStockBase):
    """Schema for creating new ProductStock."""

    pass


class ProductStockUpdate(BaseModel):
    """Schema for updating an existing ProductStock.

    All fields are optional to allow partial updates.
    """

    quantity: Optional[int] = Field(None, ge=0, description="Stock quantity")


class ProductStockInDB(ProductStockBase):
    """Schema for ProductStock data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    product_id: uuid.UUID = Field(..., description="Product ID")
    last_updated: datetime = Field(..., description="When stock was last updated")

    model_config = ConfigDict(from_attributes=True)


class ProductStock(ProductStockInDB):
    """Schema for complete ProductStock data in API responses.

    Includes related entities like warehouse details.
    """

    warehouse: Dict[str, Any] = Field(..., description="Warehouse details")


class ProductBase(BaseModel):
    """Base schema for Product data.

    Attributes:
        part_number: Product part number.
        part_number_stripped: Normalized version of part number for searching.
        application: Product application or use case description.
        vintage: Whether the product is for vintage vehicles.
        late_model: Whether the product is for late model vehicles.
        soft: Whether the product is soft (e.g., fabric vs metal).
        universal: Whether the product is universal (fits multiple applications).
        is_active: Whether the product is active in the catalog.
    """

    part_number: str = Field(..., description="Product part number")
    part_number_stripped: Optional[str] = Field(
        None, description="Normalized part number"
    )
    application: Optional[str] = Field(None, description="Product application/use case")
    vintage: bool = Field(False, description="Whether for vintage vehicles")
    late_model: bool = Field(False, description="Whether for late model vehicles")
    soft: bool = Field(False, description="Whether product is soft")
    universal: bool = Field(False, description="Whether product is universal")
    is_active: bool = Field(True, description="Whether product is active")

    @model_validator(mode="after")
    def generate_part_number_stripped(self) -> "ProductBase":
        """Generate normalized part number if not provided.

        Returns:
            Self with normalized part number.
        """
        if not self.part_number_stripped and self.part_number:
            self.part_number_stripped = "".join(
                (c for c in self.part_number if c.isalnum())
            ).upper()
        return self


class ProductCreate(ProductBase):
    """Schema for creating a new Product.

    Includes nested creation of related entities.
    """

    descriptions: Optional[List[ProductDescriptionCreate]] = Field(
        None, description="Product descriptions"
    )
    marketing: Optional[List[ProductMarketingCreate]] = Field(
        None, description="Product marketing content"
    )


class ProductUpdate(BaseModel):
    """Schema for updating an existing Product.

    All fields are optional to allow partial updates.
    """

    part_number: Optional[str] = Field(None, description="Product part number")
    application: Optional[str] = Field(None, description="Product application/use case")
    vintage: Optional[bool] = Field(None, description="Whether for vintage vehicles")
    late_model: Optional[bool] = Field(
        None, description="Whether for late model vehicles"
    )
    soft: Optional[bool] = Field(None, description="Whether product is soft")
    universal: Optional[bool] = Field(None, description="Whether product is universal")
    is_active: Optional[bool] = Field(None, description="Whether product is active")


class ProductInDB(ProductBase):
    """Schema for Product data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class Product(ProductInDB):
    """Schema for complete Product data in API responses.

    Includes related entities like descriptions, marketing, etc.
    """

    descriptions: List[ProductDescription] = Field(
        [], description="Product descriptions"
    )
    marketing: List[ProductMarketing] = Field(
        [], description="Product marketing content"
    )
    activities: List[ProductActivity] = Field(
        [], description="Product status activities"
    )
    superseded_by: List[ProductSupersession] = Field(
        [], description="Products that replace this one"
    )
    supersedes: List[ProductSupersession] = Field(
        [], description="Products this one replaces"
    )
    measurements: List[ProductMeasurement] = Field(
        [], description="Product measurements"
    )
    stock: List[ProductStock] = Field([], description="Product stock levels")


class FitmentBase(BaseModel):
    """Base schema for Fitment data.

    Attributes:
        year: Vehicle year.
        make: Vehicle make.
        model: Vehicle model.
        engine: Engine specification.
        transmission: Transmission specification.
        attributes: Additional fitment attributes.
    """

    year: int = Field(..., description="Vehicle year")
    make: str = Field(..., description="Vehicle make")
    model: str = Field(..., description="Vehicle model")
    engine: Optional[str] = Field(None, description="Engine specification")
    transmission: Optional[str] = Field(None, description="Transmission specification")
    attributes: Dict[str, Any] = Field(
        default_factory=dict, description="Additional attributes"
    )

    @field_validator("year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        """Validate vehicle year.

        Args:
            v: The year to validate.

        Returns:
            Validated year.

        Raises:
            ValueError: If the year is outside valid range.
        """
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 2:
            raise ValueError(f"Year must be between 1900 and {current_year + 2}")
        return v


class FitmentCreate(FitmentBase):
    """Schema for creating a new Fitment."""

    pass


class FitmentUpdate(BaseModel):
    """Schema for updating an existing Fitment.

    All fields are optional to allow partial updates.
    """

    year: Optional[int] = Field(None, description="Vehicle year")
    make: Optional[str] = Field(None, description="Vehicle make")
    model: Optional[str] = Field(None, description="Vehicle model")
    engine: Optional[str] = Field(None, description="Engine specification")
    transmission: Optional[str] = Field(None, description="Transmission specification")
    attributes: Optional[Dict[str, Any]] = Field(
        None, description="Additional attributes"
    )

    @field_validator("year")
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        """Validate vehicle year if provided.

        Args:
            v: The year to validate or None.

        Returns:
            Validated year or None.

        Raises:
            ValueError: If the year is outside valid range.
        """
        if v is None:
            return v

        current_year = datetime.now().year
        if v < 1900 or v > current_year + 2:
            raise ValueError(f"Year must be between 1900 and {current_year + 2}")
        return v


class FitmentInDB(FitmentBase):
    """Schema for Fitment data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class Fitment(FitmentInDB):
    """Schema for complete Fitment data in API responses."""

    pass


class PaginatedResponse(BaseModel):
    """Base schema for paginated responses.

    Attributes:
        items: List of items.
        total: Total number of items.
        page: Current page number.
        page_size: Number of items per page.
        pages: Total number of pages.
    """

    items: List[Any] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")


class ProductListResponse(PaginatedResponse):
    """Schema for paginated product response.

    Overrides items type to be specifically List[Product].
    """

    items: List[Product] = Field(..., description="List of products")


class FitmentListResponse(PaginatedResponse):
    """Schema for paginated fitment response.

    Overrides items type to be specifically List[Fitment].
    """

    items: List[Fitment] = Field(..., description="List of fitments")
