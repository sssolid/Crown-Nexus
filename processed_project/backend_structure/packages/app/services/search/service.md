# Module: app.services.search.service

**Path:** `app/services/search/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.cache.decorators import cached
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import get_dependency
from app.core.exceptions import DatabaseException, ErrorCode
from app.logging import get_logger
from app.domains.products.models import Fitment, Product
from app.services.interfaces import ServiceInterface
from app.services.search.factory import SearchProviderFactory
```

## Global Variables
```python
logger = logger = get_logger("app.services.search.service")
```

## Classes

| Class | Description |
| --- | --- |
| `SearchService` |  |

### Class: `SearchService`
**Inherits from:** ServiceInterface

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `global_search` `async` |  |
| `initialize` `async` |  |
| `search_fitments` `async` |  |
| `search_products` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `global_search`
```python
async def global_search(self, search_term, entity_types, page, page_size) -> Dict[(str, Any)]:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `search_fitments`
```python
@cached(prefix='search:fitments', ttl=300, backend='redis')
async def search_fitments(self, search_term, year, make, model, engine, transmission, page, page_size, use_elasticsearch) -> Dict[(str, Any)]:
```

##### `search_products`
```python
@cached(prefix='search:products', ttl=300, backend='redis')
async def search_products(self, search_term, attributes, is_active, page, page_size, use_elasticsearch) -> Dict[(str, Any)]:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
