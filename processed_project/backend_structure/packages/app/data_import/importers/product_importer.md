# Module: app.data_import.importers.product_importer

**Path:** `app/data_import/importers/product_importer.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseException
from app.logging import get_logger
from app.domains.products.models import Product, ProductDescription, ProductMarketing
from app.domains.products.schemas import ProductCreate
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.importers.product_importer")
```

## Classes

| Class | Description |
| --- | --- |
| `ProductImporter` |  |

### Class: `ProductImporter`

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
