# Module: app.services.search.factory

**Path:** `app/services/search/factory.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.core.config import settings
from app.logging import get_logger
from app.domains.products.models import Fitment, Product
from app.services.search.base import SearchProvider
from app.services.search.providers import DatabaseSearchProvider, ElasticsearchSearchProvider
```

## Global Variables
```python
logger = logger = get_logger("app.services.search.factory")
```

## Classes

| Class | Description |
| --- | --- |
| `SearchProviderFactory` |  |

### Class: `SearchProviderFactory`

#### Methods

| Method | Description |
| --- | --- |
| `create_default_provider` `async` |  |
| `create_provider` `async` |  |
| `shutdown_all` `async` |  |

##### `create_default_provider`
```python
@classmethod
async def create_default_provider(cls, db, model_class) -> SearchProvider:
```

##### `create_provider`
```python
@classmethod
async def create_provider(cls, provider_type, db, model_class, **kwargs) -> SearchProvider:
```

##### `shutdown_all`
```python
@classmethod
async def shutdown_all(cls) -> None:
```
