# Module: app.core.pagination.manager

**Path:** `app/core/pagination/manager.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union, cast
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.core.pagination.base import CursorPaginationParams, OffsetPaginationParams, PaginationProvider, PaginationResult
from app.core.pagination.factory import PaginationProviderFactory
from app.core.pagination.providers import CursorPaginationProvider, OffsetPaginationProvider
```

## Global Variables
```python
logger = logger = get_logger(__name__)
T = T = TypeVar("T")  # SQLAlchemy model type
R = R = TypeVar("R")  # Result type
```

## Functions

| Function | Description |
| --- | --- |
| `initialize` |  |
| `paginate_with_cursor` |  |
| `paginate_with_offset` |  |
| `shutdown` |  |

### `initialize`
```python
async def initialize() -> None:
```

### `paginate_with_cursor`
```python
async def paginate_with_cursor(db, model_class, query, params, transform_func, response_model) -> PaginationResult[Any]:
```

### `paginate_with_offset`
```python
async def paginate_with_offset(db, model_class, query, params, transform_func, response_model) -> PaginationResult[Any]:
```

### `shutdown`
```python
async def shutdown() -> None:
```
