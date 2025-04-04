# Module: app.core.pagination.providers.offset

**Path:** `app/core/pagination/providers/offset.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Callable, Generic, List, Optional, TypeVar, cast
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.logging import get_logger
from app.db.utils import count_query, execute_query
from app.core.pagination.base import OffsetPaginationParams, PaginationProvider, PaginationResult, SortDirection, SortField
from app.core.pagination.exceptions import InvalidSortFieldException
```

## Global Variables
```python
logger = logger = get_logger("app.core.pagination.providers.offset")
T = T = TypeVar("T")
R = R = TypeVar("R")
```

## Classes

| Class | Description |
| --- | --- |
| `OffsetPaginationProvider` |  |

### Class: `OffsetPaginationProvider`
**Inherits from:** Generic[(T, R)], PaginationProvider[(T, R)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `paginate_with_cursor` `async` |  |
| `paginate_with_offset` `async` |  |

##### `__init__`
```python
def __init__(self, db, model_class) -> None:
```

##### `paginate_with_cursor`
```python
async def paginate_with_cursor(self, query, params, transform_func) -> PaginationResult[R]:
```

##### `paginate_with_offset`
```python
async def paginate_with_offset(self, query, params, transform_func) -> PaginationResult[R]:
```
