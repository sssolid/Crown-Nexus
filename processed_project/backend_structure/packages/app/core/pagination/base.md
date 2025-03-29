# Module: app.core.pagination.base

**Path:** `app/core/pagination/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar
from pydantic import BaseModel, Field
from sqlalchemy.sql import Select
```

## Global Variables
```python
T = T = TypeVar("T")  # Entity type
R = R = TypeVar("R")  # Result type
```

## Classes

| Class | Description |
| --- | --- |
| `CursorPaginationParams` |  |
| `OffsetPaginationParams` |  |
| `PaginationProvider` |  |
| `PaginationResult` |  |
| `SortDirection` |  |
| `SortField` |  |

### Class: `CursorPaginationParams`
**Inherits from:** BaseModel

### Class: `OffsetPaginationParams`
**Inherits from:** BaseModel

### Class: `PaginationProvider`
**Inherits from:** Protocol, Generic[(T, R)]

#### Methods

| Method | Description |
| --- | --- |
| `paginate_with_cursor` `async` |  |
| `paginate_with_offset` `async` |  |

##### `paginate_with_cursor`
```python
async def paginate_with_cursor(self, query, params, transform_func) -> PaginationResult[R]:
```

##### `paginate_with_offset`
```python
async def paginate_with_offset(self, query, params, transform_func) -> PaginationResult[R]:
```

### Class: `PaginationResult`
**Inherits from:** Generic[R]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `to_dict` |  |

##### `__init__`
```python
def __init__(self, items, total, page, page_size, pages, next_cursor, has_next, has_prev) -> None:
```

##### `to_dict`
```python
def to_dict(self) -> Dict[(str, Any)]:
```

### Class: `SortDirection`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `ASC` | `'asc'` |
| `DESC` | `'desc'` |

### Class: `SortField`
**Inherits from:** BaseModel
