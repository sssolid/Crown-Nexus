# Module: app.db.utils

**Path:** `app/db/utils.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import contextlib
import functools
import time
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Type, TypeVar, Union, cast
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import Delete, Insert, Update
from app.core.dependency_manager import get_dependency
from app.core.exceptions import DataIntegrityException, DatabaseException, ErrorCode, TransactionException
from app.logging import get_logger
from app.db.base_class import Base
```

## Global Variables
```python
logger = logger = get_logger("app.db.utils")
T = T = TypeVar("T", bound=Base)
F = F = TypeVar("F", bound=Callable[..., Any])
```

## Functions

| Function | Description |
| --- | --- |
| `bulk_create` |  |
| `bulk_update` |  |
| `count_query` |  |
| `create_object` |  |
| `delete_object` |  |
| `execute_query` |  |
| `get_by_id` |  |
| `get_by_ids` |  |
| `paginate` |  |
| `track_db_delete` |  |
| `track_db_insert` |  |
| `track_db_query` |  |
| `track_db_select` |  |
| `track_db_transaction` |  |
| `track_db_update` |  |
| `transaction` |  |
| `transactional` |  |
| `update_object` |  |
| `upsert` |  |

### `bulk_create`
```python
async def bulk_create(db, model, objects) -> List[T]:
```

### `bulk_update`
```python
async def bulk_update(db, model, id_field, objects) -> int:
```

### `count_query`
```python
async def count_query(db, query) -> int:
```

### `create_object`
```python
async def create_object(db, model, obj_in) -> T:
```

### `delete_object`
```python
async def delete_object(db, model, id_value, user_id, hard_delete) -> bool:
```

### `execute_query`
```python
async def execute_query(db, query) -> Any:
```

### `get_by_id`
```python
async def get_by_id(db, model, id_value) -> Optional[T]:
```

### `get_by_ids`
```python
async def get_by_ids(db, model, ids) -> List[T]:
```

### `paginate`
```python
async def paginate(db, query, page, page_size, load_items) -> Dict[(str, Any)]:
```

### `track_db_delete`
```python
def track_db_delete(entity) -> Callable[([F], F)]:
```

### `track_db_insert`
```python
def track_db_insert(entity) -> Callable[([F], F)]:
```

### `track_db_query`
```python
def track_db_query(operation, entity) -> Callable[([F], F)]:
```

### `track_db_select`
```python
def track_db_select(entity) -> Callable[([F], F)]:
```

### `track_db_transaction`
```python
def track_db_transaction() -> Callable[([F], F)]:
```

### `track_db_update`
```python
def track_db_update(entity) -> Callable[([F], F)]:
```

### `transaction`
```python
@contextlib.asynccontextmanager
async def transaction(db) -> AsyncGenerator[(AsyncSession, None)]:
```

### `transactional`
```python
def transactional(func) -> F:
```

### `update_object`
```python
async def update_object(db, model, id_value, obj_in, user_id) -> Optional[T]:
```

### `upsert`
```python
async def upsert(db, model, data, unique_fields) -> T:
```
