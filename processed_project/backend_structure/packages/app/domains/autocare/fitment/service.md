# Module: app.domains.autocare.fitment.service

**Path:** `app/domains/autocare/fitment/service.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import MappingNotFoundException, ImportException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.fitment.repository import FitmentMappingRepository
from app.domains.autocare.fitment.models import FitmentMapping
from app.domains.products.repository import ProductRepository
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.fitment.service")
```

## Classes

| Class | Description |
| --- | --- |
| `FitmentMappingService` |  |

### Class: `FitmentMappingService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `create_mapping` `async` |  |
| `delete_mapping` `async` |  |
| `find_mappings_by_product` `async` |  |
| `get_mapping` `async` |  |
| `get_mapping_history` `async` |  |
| `import_from_aces` `async` |  |
| `search_mappings` `async` |  |
| `update_mapping` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `create_mapping`
```python
async def create_mapping(self, data, user_id) -> FitmentMapping:
```

##### `delete_mapping`
```python
async def delete_mapping(self, mapping_id, user_id) -> None:
```

##### `find_mappings_by_product`
```python
async def find_mappings_by_product(self, product_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_mapping`
```python
async def get_mapping(self, mapping_id) -> Dict[(str, Any)]:
```

##### `get_mapping_history`
```python
async def get_mapping_history(self, mapping_id, page, page_size) -> Dict[(str, Any)]:
```

##### `import_from_aces`
```python
async def import_from_aces(self, file_path, params) -> Dict[(str, Any)]:
```

##### `search_mappings`
```python
async def search_mappings(self, product_query, is_validated, is_manual, page, page_size) -> Dict[(str, Any)]:
```

##### `update_mapping`
```python
async def update_mapping(self, mapping_id, data, user_id) -> FitmentMapping:
```
