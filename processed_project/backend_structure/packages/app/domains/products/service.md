# Module: app.domains.products.service

**Path:** `app/domains/products/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import get_dependency
from app.domains.products.models import Product
from app.domains.products.schemas import ProductCreate
```

## Classes

| Class | Description |
| --- | --- |
| `ProductService` |  |

### Class: `ProductService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `create_product` `async` |  |
| `get_product` `async` |  |

##### `__init__`
```python
def __init__(self, db):
```

##### `create_product`
```python
async def create_product(self, data) -> Product:
```

##### `get_product`
```python
async def get_product(self, product_id) -> Product:
```
