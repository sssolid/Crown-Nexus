# Module: app.domains.autocare.padb.service

**Path:** `app/domains/autocare/padb/service.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
from datetime import datetime
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import PAdbException
from app.domains.autocare.padb.repository import PAdbRepository
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.padb.service")
```

## Classes

| Class | Description |
| --- | --- |
| `PAdbService` |  |

### Class: `PAdbService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_attribute_details` `async` |  |
| `get_part_attributes` `async` |  |
| `get_stats` `async` |  |
| `get_version` `async` |  |
| `search_attributes` `async` |  |
| `update_database` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_attribute_details`
```python
async def get_attribute_details(self, pa_id) -> Dict[(str, Any)]:
```

##### `get_part_attributes`
```python
async def get_part_attributes(self, part_terminology_id) -> Dict[(str, Any)]:
```

##### `get_stats`
```python
async def get_stats(self) -> Dict[(str, Any)]:
```

##### `get_version`
```python
async def get_version(self) -> str:
```

##### `search_attributes`
```python
async def search_attributes(self, search_term, page, page_size) -> Dict[(str, Any)]:
```

##### `update_database`
```python
async def update_database(self, file_path) -> Dict[(str, Any)]:
```
