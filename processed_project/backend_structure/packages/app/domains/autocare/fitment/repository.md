# Module: app.domains.autocare.fitment.repository

**Path:** `app/domains/autocare/fitment/repository.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import select, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.repositories.base import BaseRepository
from app.domains.autocare.fitment.models import FitmentMapping, FitmentMappingHistory
```

## Classes

| Class | Description |
| --- | --- |
| `FitmentMappingRepository` |  |

### Class: `FitmentMappingRepository`
**Inherits from:** BaseRepository[(FitmentMapping, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `create_with_history` `async` |  |
| `delete_with_history` `async` |  |
| `find_by_base_vehicle` `async` |  |
| `find_by_part` `async` |  |
| `find_by_product` `async` |  |
| `find_by_vehicle` `async` |  |
| `get_mapping_history` `async` |  |
| `search` `async` |  |
| `update_with_history` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `create_with_history`
```python
async def create_with_history(self, data, user_id) -> FitmentMapping:
```

##### `delete_with_history`
```python
async def delete_with_history(self, id, user_id) -> None:
```

##### `find_by_base_vehicle`
```python
async def find_by_base_vehicle(self, base_vehicle_id, page, page_size) -> Dict[(str, Any)]:
```

##### `find_by_part`
```python
async def find_by_part(self, part_terminology_id, page, page_size) -> Dict[(str, Any)]:
```

##### `find_by_product`
```python
async def find_by_product(self, product_id, page, page_size) -> Dict[(str, Any)]:
```

##### `find_by_vehicle`
```python
async def find_by_vehicle(self, vehicle_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_mapping_history`
```python
async def get_mapping_history(self, mapping_id, page, page_size) -> Dict[(str, Any)]:
```

##### `search`
```python
async def search(self, product_query, is_validated, is_manual, page, page_size) -> Dict[(str, Any)]:
```

##### `update_with_history`
```python
async def update_with_history(self, id, data, user_id) -> FitmentMapping:
```
