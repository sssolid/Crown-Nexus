# Module: app.domains.products.models

**Path:** `app/domains/products/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
import typing
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy import UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.media.models import Media
from app.domains.reference.models import Color, ConstructionType, Hardware, PackagingType, TariffCode, Texture, UnspscCode, Warehouse
from app.domains.location.models import Country
from app.domains.products.associations import product_media_association, product_fitment_association, product_tariff_code_association, product_unspsc_association, product_country_origin_association, product_hardware_association, product_color_association, product_construction_type_association, product_texture_association, product_packaging_association, product_interchange_association
```

## Classes

| Class | Description |
| --- | --- |
| `AttributeDefinition` |  |
| `Brand` |  |
| `Fitment` |  |
| `Manufacturer` |  |
| `PriceType` |  |
| `Product` |  |
| `ProductActivity` |  |
| `ProductAttribute` |  |
| `ProductBrandHistory` |  |
| `ProductDescription` |  |
| `ProductMarketing` |  |
| `ProductMeasurement` |  |
| `ProductPricing` |  |
| `ProductStock` |  |
| `ProductSupersession` |  |

### Class: `AttributeDefinition`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'attribute_definition'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Brand`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'brand'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |
| `parent_company` | `    parent_company = relationship("Company", foreign_keys=[parent_company_id])` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Fitment`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'fitment'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Manufacturer`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'manufacturer'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |
| `company` | `    company = relationship("Company", foreign_keys=[company_id])` |
| `address` | `    address = relationship("Address", foreign_keys=[address_id])` |
| `billing_address` | `    billing_address = relationship("Address", foreign_keys=[billing_address_id])` |
| `shipping_address` | `    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])` |
| `country` | `    country = relationship("Country", foreign_keys=[country_id])` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PriceType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'price_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Product`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductActivity`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_activity'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductAttribute`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_attribute'` |
| `__table_args__` | `    __table_args__ = (
        UniqueConstraint("product_id", "attribute_id", name="uix_product_attribute"),
        {"schema": "product"},
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductBrandHistory`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_brand_history'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductDescription`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_description'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductMarketing`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_marketing'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductMeasurement`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_measurement'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductPricing`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_pricing'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductStock`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_stock'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductSupersession`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_supersession'` |
| `__table_args__` | `    __table_args__ = {"schema": "product"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
