# Module: app.services.search.providers.database

**Path:** `app/services/search/providers/database.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.pagination import paginate_with_offset, OffsetPaginationParams
from typing import Any, Dict, List, Optional, Type, cast
from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.core.exceptions import DatabaseException, ErrorCode
from app.logging import get_logger
from app.domains.products.models import Fitment, Product
from app.services.search.base import SearchProvider, SearchResult
```

## Global Variables
```python
logger = logger = get_logger("app.services.search.providers.database")
```

## Classes

| Class | Description |
| --- | --- |
| `DatabaseSearchProvider` |  |

### Class: `DatabaseSearchProvider`
**Inherits from:** SearchProvider

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `initialize` `async` |  |
| `search` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self, db, model_class) -> None:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `search`
```python
async def search(self, search_term, filters, page, page_size, **kwargs) -> SearchResult:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
