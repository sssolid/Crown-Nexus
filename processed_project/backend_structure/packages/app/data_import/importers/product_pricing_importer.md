# Module: app.data_import.importers.product_pricing_importer

**Path:** `app/data_import/importers/product_pricing_importer.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.exceptions import DatabaseException, ResourceNotFoundException
from app.domains.products.schemas import ProductPricingImport
from app.domains.products.models import Product, PriceType, ProductPricing
from app.logging import get_logger
from app.data_import.importers.base import Importer
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.importers.product_pricing_importer")
```

## Classes

| Class | Description |
| --- | --- |
| `ProductPricingImporter` |  |

### Class: `ProductPricingImporter`
**Inherits from:** Importer[ProductPricingImport]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `import_data` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `import_data`
```python
async def import_data(self, data) -> Dict[(str, Any)]:
```
