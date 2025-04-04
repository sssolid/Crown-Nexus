# Module: app.domains.products.schemas

**Path:** `app/domains/products/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
```

## Classes

| Class | Description |
| --- | --- |
| `Brand` |  |
| `BrandBase` |  |
| `BrandCreate` |  |
| `BrandInDB` |  |
| `BrandUpdate` |  |
| `DescriptionType` |  |
| `Fitment` |  |
| `FitmentBase` |  |
| `FitmentCreate` |  |
| `FitmentInDB` |  |
| `FitmentListResponse` |  |
| `FitmentUpdate` |  |
| `MarketingType` |  |
| `PaginatedResponse` |  |
| `Product` |  |
| `ProductActivity` |  |
| `ProductActivityBase` |  |
| `ProductActivityCreate` |  |
| `ProductActivityInDB` |  |
| `ProductBase` |  |
| `ProductCreate` |  |
| `ProductDescription` |  |
| `ProductDescriptionBase` |  |
| `ProductDescriptionCreate` |  |
| `ProductDescriptionInDB` |  |
| `ProductDescriptionUpdate` |  |
| `ProductInDB` |  |
| `ProductListResponse` |  |
| `ProductMarketing` |  |
| `ProductMarketingBase` |  |
| `ProductMarketingCreate` |  |
| `ProductMarketingInDB` |  |
| `ProductMarketingUpdate` |  |
| `ProductMeasurement` |  |
| `ProductMeasurementBase` |  |
| `ProductMeasurementCreate` |  |
| `ProductMeasurementInDB` |  |
| `ProductMeasurementUpdate` |  |
| `ProductPricingBase` |  |
| `ProductPricingCreate` |  |
| `ProductPricingImport` |  |
| `ProductPricingUpdate` |  |
| `ProductStatus` |  |
| `ProductStock` |  |
| `ProductStockBase` |  |
| `ProductStockCreate` |  |
| `ProductStockInDB` |  |
| `ProductStockUpdate` |  |
| `ProductSupersession` |  |
| `ProductSupersessionBase` |  |
| `ProductSupersessionCreate` |  |
| `ProductSupersessionInDB` |  |
| `ProductSupersessionUpdate` |  |
| `ProductUpdate` |  |

### Class: `Brand`
**Inherits from:** BrandInDB

### Class: `BrandBase`
**Inherits from:** BaseModel

### Class: `BrandCreate`
**Inherits from:** BrandBase

### Class: `BrandInDB`
**Inherits from:** BrandBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BrandUpdate`
**Inherits from:** BaseModel

### Class: `DescriptionType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `STANDARD` | `'Standard'` |
| `SHORT` | `'Short'` |
| `LONG` | `'Long'` |
| `KEYWORDS` | `'Keywords'` |
| `SLANG` | `'Slang'` |
| `NOTES` | `'Notes'` |
| `LONG_ALLMODELS` | `'Long_AllModels'` |
| `LONG_JEEPONLY` | `'Long_JeepOnly'` |
| `LONG_NONJEEP` | `'Long_NonJeep'` |
| `EXTENDED` | `'Extended'` |
| `EXTENDED_NONJEEP` | `'Extended_NonJeep'` |
| `EXTENDED_UNLIMITED` | `'Extended_Unlimited'` |

### Class: `Fitment`
**Inherits from:** FitmentInDB

### Class: `FitmentBase`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_year` |  |

##### `validate_year`
```python
@field_validator('year')
@classmethod
def validate_year(cls, v) -> int:
```

### Class: `FitmentCreate`
**Inherits from:** FitmentBase

### Class: `FitmentInDB`
**Inherits from:** FitmentBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FitmentListResponse`
**Inherits from:** PaginatedResponse

### Class: `FitmentUpdate`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_year` |  |

##### `validate_year`
```python
@field_validator('year')
@classmethod
def validate_year(cls, v) -> Optional[int]:
```

### Class: `MarketingType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `BULLET_POINT` | `'Bullet Point'` |
| `AD_COPY` | `'Ad Copy'` |

### Class: `PaginatedResponse`
**Inherits from:** BaseModel

### Class: `Product`
**Inherits from:** ProductInDB

### Class: `ProductActivity`
**Inherits from:** ProductActivityInDB

### Class: `ProductActivityBase`
**Inherits from:** BaseModel

### Class: `ProductActivityCreate`
**Inherits from:** ProductActivityBase

### Class: `ProductActivityInDB`
**Inherits from:** ProductActivityBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ProductBase`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `generate_part_number_stripped` |  |

##### `generate_part_number_stripped`
```python
@model_validator(mode='after')
def generate_part_number_stripped(self) -> 'ProductBase':
```

### Class: `ProductCreate`
**Inherits from:** ProductBase

### Class: `ProductDescription`
**Inherits from:** ProductDescriptionInDB

### Class: `ProductDescriptionBase`
**Inherits from:** BaseModel

### Class: `ProductDescriptionCreate`
**Inherits from:** ProductDescriptionBase

### Class: `ProductDescriptionInDB`
**Inherits from:** ProductDescriptionBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ProductDescriptionUpdate`
**Inherits from:** BaseModel

### Class: `ProductInDB`
**Inherits from:** ProductBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ProductListResponse`
**Inherits from:** PaginatedResponse

### Class: `ProductMarketing`
**Inherits from:** ProductMarketingInDB

### Class: `ProductMarketingBase`
**Inherits from:** BaseModel

### Class: `ProductMarketingCreate`
**Inherits from:** ProductMarketingBase

### Class: `ProductMarketingInDB`
**Inherits from:** ProductMarketingBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ProductMarketingUpdate`
**Inherits from:** BaseModel

### Class: `ProductMeasurement`
**Inherits from:** ProductMeasurementInDB

### Class: `ProductMeasurementBase`
**Inherits from:** BaseModel

### Class: `ProductMeasurementCreate`
**Inherits from:** ProductMeasurementBase

### Class: `ProductMeasurementInDB`
**Inherits from:** ProductMeasurementBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ProductMeasurementUpdate`
**Inherits from:** ProductMeasurementBase

### Class: `ProductPricingBase`
**Inherits from:** BaseModel

### Class: `ProductPricingCreate`
**Inherits from:** ProductPricingBase

### Class: `ProductPricingImport`
**Inherits from:** BaseModel

### Class: `ProductPricingUpdate`
**Inherits from:** BaseModel

### Class: `ProductStatus`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `ACTIVE` | `'active'` |
| `INACTIVE` | `'inactive'` |
| `DISCONTINUED` | `'discontinued'` |
| `OUT_OF_STOCK` | `'out_of_stock'` |
| `PENDING` | `'pending'` |

### Class: `ProductStock`
**Inherits from:** ProductStockInDB

### Class: `ProductStockBase`
**Inherits from:** BaseModel

### Class: `ProductStockCreate`
**Inherits from:** ProductStockBase

### Class: `ProductStockInDB`
**Inherits from:** ProductStockBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ProductStockUpdate`
**Inherits from:** BaseModel

### Class: `ProductSupersession`
**Inherits from:** ProductSupersessionInDB

### Class: `ProductSupersessionBase`
**Inherits from:** BaseModel

### Class: `ProductSupersessionCreate`
**Inherits from:** ProductSupersessionBase

### Class: `ProductSupersessionInDB`
**Inherits from:** ProductSupersessionBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ProductSupersessionUpdate`
**Inherits from:** BaseModel

### Class: `ProductUpdate`
**Inherits from:** BaseModel
