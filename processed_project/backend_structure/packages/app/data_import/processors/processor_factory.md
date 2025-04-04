# Module: app.data_import.processors.processor_factory

**Path:** `app/data_import/processors/processor_factory.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, Optional, Type, Union
from pydantic import BaseModel
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS
from app.data_import.processors.generic_processor import GenericProcessor
from app.data_import.processors.integrated_processor import IntegratedProductProcessor
from app.data_import.processors.pricing_processor import PricingProcessor
from app.data_import.schemas.pricing import ProductPricingImport
from app.domains.products.schemas import ProductCreate, ProductMeasurementCreate, ProductStockCreate
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.processors.processor_factory")
create_processor = create_processor = ProcessorFactory.create_processor
```

## Classes

| Class | Description |
| --- | --- |
| `EntityType` |  |
| `ProcessorFactory` |  |
| `SourceType` |  |

### Class: `EntityType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `PRODUCT` | `'product'` |
| `PRODUCT_PRICING` | `'product_pricing'` |
| `PRODUCT_STOCK` | `'product_stock'` |
| `PRODUCT_MEASUREMENT` | `'product_measurement'` |

### Class: `ProcessorFactory`

#### Methods

| Method | Description |
| --- | --- |
| `create_processor` |  |

##### `create_processor`
```python
@classmethod
def create_processor(cls, entity_type, source_type, **kwargs) -> GenericProcessor:
```

### Class: `SourceType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `FILEMAKER` | `'filemaker'` |
| `AS400` | `'as400'` |
| `CSV` | `'csv'` |
