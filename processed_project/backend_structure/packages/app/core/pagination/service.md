# Module: app.core.pagination.service

**Path:** `app/core/pagination/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Callable, Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.core.pagination.base import CursorPaginationParams, OffsetPaginationParams, PaginationResult
from app.core.pagination.manager import paginate_with_cursor, paginate_with_offset
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.pagination.service")
T = T = TypeVar("T")
R = R = TypeVar("R")
```

## Functions

| Function | Description |
| --- | --- |
| `get_pagination_service` |  |

### `get_pagination_service`
```python
def get_pagination_service(db) -> PaginationService:
```

## Classes

| Class | Description |
| --- | --- |
| `PaginationService` |  |

### Class: `PaginationService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `initialize` `async` |  |
| `paginate_with_cursor` `async` |  |
| `paginate_with_offset` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `paginate_with_cursor`
```python
async def paginate_with_cursor(self, model_class, query, params, transform_func, response_model, db) -> PaginationResult[Any]:
```

##### `paginate_with_offset`
```python
async def paginate_with_offset(self, model_class, query, params, transform_func, response_model, db) -> PaginationResult[Any]:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
