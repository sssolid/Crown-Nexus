# Module: app.domains.model_mapping.repository

**Path:** `app/domains/model_mapping/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import re
from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.model_mapping.models import ModelMapping
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

## Classes

| Class | Description |
| --- | --- |
| `ModelMappingRepository` |  |

### Class: `ModelMappingRepository`
**Inherits from:** BaseRepository[(ModelMapping, int)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_make_model` `async` |  |
| `find_by_pattern` `async` |  |
| `get_active_mappings` `async` |  |
| `get_by_make` `async` |  |
| `match_vehicle_string` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, mapping_id) -> ModelMapping:
```

##### `find_by_make_model`
```python
async def find_by_make_model(self, make, model) -> List[ModelMapping]:
```

##### `find_by_pattern`
```python
async def find_by_pattern(self, pattern) -> List[ModelMapping]:
```

##### `get_active_mappings`
```python
async def get_active_mappings(self, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_make`
```python
async def get_by_make(self, make) -> List[ModelMapping]:
```

##### `match_vehicle_string`
```python
async def match_vehicle_string(self, vehicle_string) -> Optional[Dict[(str, str)]]:
```
