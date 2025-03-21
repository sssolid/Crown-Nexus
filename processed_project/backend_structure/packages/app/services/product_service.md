# Module: app.services.product_service

**Path:** `app/services/product_service.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import get_dependency
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
```

## Global Variables
```python
error_service = error_service = get_dependency("error_service")
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
