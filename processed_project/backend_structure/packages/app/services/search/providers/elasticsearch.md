# Module: app.services.search.providers.elasticsearch

**Path:** `app/services/search/providers/elasticsearch.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, Type
from elasticsearch import AsyncElasticsearch
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.core.config import settings
from app.core.exceptions import DatabaseException, ErrorCode, ServiceException
from app.logging import get_logger
from app.services.search.base import SearchProvider, SearchResult
from app.utils.retry import async_retry_on_network_errors
```

## Global Variables
```python
logger = logger = get_logger("app.services.search.providers.elasticsearch")
```

## Classes

| Class | Description |
| --- | --- |
| `ElasticsearchSearchProvider` |  |

### Class: `ElasticsearchSearchProvider`
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
def __init__(self, db, model_class, index_name) -> None:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `search`
```python
@async_retry_on_network_errors(retries=2, delay=0.5)
async def search(self, search_term, filters, page, page_size, **kwargs) -> SearchResult:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
