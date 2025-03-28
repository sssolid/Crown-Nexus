# Module: app.data_import.importers.as400_importers

**Path:** `app/data_import/importers/as400_importers.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, TypeVar
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseException
from app.logging import get_logger
from app.domains.products.models import Product, ProductMeasurement, ProductPricing, ProductStock, Manufacturer, PriceType
from app.domains.currency.models import Currency
from app.domains.reference.models import Warehouse
from app.domains.products.schemas import ProductCreate, ProductMeasurementCreate, ProductStock as ProductStockSchema
from app.data_import.importers.base import Importer
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.importers.as400_importers")
T = T = TypeVar("T")
```

## Classes

| Class | Description |
| --- | --- |
| `AS400BaseImporter` |  |
| `ProductAS400Importer` |  |
| `ProductMeasurementImporter` |  |
| `ProductPricingImporter` |  |
| `ProductStockImporter` |  |

### Class: `AS400BaseImporter`
**Inherits from:** Importer[T]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_existing_entities` `async` |  |
| `track_sync` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_existing_entities`
```python
async def get_existing_entities(self, id_field, id_values, model) -> Dict[(Any, Any)]:
```

##### `track_sync`
```python
async def track_sync(self, entity_type, created, updated, errors) -> None:
```

### Class: `ProductAS400Importer`
**Inherits from:** AS400BaseImporter[ProductCreate]

#### Methods

| Method | Description |
| --- | --- |
| `import_data` `async` |  |

##### `import_data`
```python
async def import_data(self, data) -> Dict[(str, Any)]:
```

### Class: `ProductMeasurementImporter`
**Inherits from:** AS400BaseImporter[ProductMeasurementCreate]

#### Methods

| Method | Description |
| --- | --- |
| `import_data` `async` |  |

##### `import_data`
```python
async def import_data(self, data) -> Dict[(str, Any)]:
```

### Class: `ProductPricingImporter`
**Inherits from:** AS400BaseImporter[Any]

#### Methods

| Method | Description |
| --- | --- |
| `import_data` `async` |  |

##### `import_data`
```python
async def import_data(self, data) -> Dict[(str, Any)]:
```

### Class: `ProductStockImporter`
**Inherits from:** AS400BaseImporter[ProductStockSchema]

#### Methods

| Method | Description |
| --- | --- |
| `import_data` `async` |  |

##### `import_data`
```python
async def import_data(self, data) -> Dict[(str, Any)]:
```
