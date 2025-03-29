# Module: app.repositories.base

**Path:** `app/repositories/base.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseException
from app.logging import get_logger
from app.db.base_class import Base
from app.db.utils import bulk_create, count_query, create_object, delete_object, get_by_id, get_by_ids, paginate, update_object, upsert
```

## Global Variables
```python
logger = logger = get_logger("app.repositories.base")
T = T = TypeVar("T", bound=Base)
ID = ID = TypeVar("ID")
```

## Classes

| Class | Description |
| --- | --- |
| `BaseRepository` |  |

### Class: `BaseRepository`
**Inherits from:** Generic[(T, ID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `bulk_create` `async` |  |
| `count` `async` |  |
| `create` `async` |  |
| `delete` `async` |  |
| `exists` `async` |  |
| `find_one_by` `async` |  |
| `get_all` `async` |  |
| `get_by_id` `async` |  |
| `get_by_ids` `async` |  |
| `update` `async` |  |
| `upsert` `async` |  |

##### `__init__`
```python
def __init__(self, model, db) -> None:
```

##### `bulk_create`
```python
async def bulk_create(self, items) -> List[T]:
```

##### `count`
```python
async def count(self, filters) -> int:
```

##### `create`
```python
async def create(self, data) -> T:
```

##### `delete`
```python
async def delete(self, id_value, user_id, hard_delete) -> bool:
```

##### `exists`
```python
async def exists(self, filters) -> bool:
```

##### `find_one_by`
```python
async def find_one_by(self, filters) -> Optional[T]:
```

##### `get_all`
```python
async def get_all(self, page, page_size, order_by, filters) -> Dict[(str, Any)]:
```

##### `get_by_id`
```python
async def get_by_id(self, id_value) -> Optional[T]:
```

##### `get_by_ids`
```python
async def get_by_ids(self, ids) -> List[T]:
```

##### `update`
```python
async def update(self, id_value, data, user_id) -> Optional[T]:
```

##### `upsert`
```python
async def upsert(self, data, unique_fields) -> T:
```
