# Module: app.core.pagination.providers.cursor

**Path:** `app/core/pagination/providers/cursor.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import base64
import json
from datetime import datetime
import uuid
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, cast
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.logging import get_logger
from app.db.utils import count_query, execute_query
from app.core.pagination.base import CursorPaginationParams, PaginationProvider, PaginationResult, SortDirection, SortField
from app.core.pagination.exceptions import InvalidCursorException, InvalidSortFieldException
```

## Global Variables
```python
logger = logger = get_logger("app.core.pagination.providers.cursor")
T = T = TypeVar("T")
R = R = TypeVar("R")
```

## Classes

| Class | Description |
| --- | --- |
| `CursorPaginationProvider` |  |

### Class: `CursorPaginationProvider`
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
