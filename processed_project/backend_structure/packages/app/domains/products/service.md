# Module: app.domains.products.service

**Path:** `app/domains/products/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.audit import get_audit_service
from app.core.audit.base import AuditEventType, AuditLogLevel, AuditContext
from app.core.dependency_manager import get_dependency
from app.core.events import EventService
from app.core.exceptions import BusinessException, ResourceNotFoundException
from app.domains.products.exceptions import ProductNotFoundException, DuplicatePartNumberException, ProductInactiveException, BrandNotFoundException
from app.domains.products.models import Product, ProductActivity, ProductDescription, ProductMarketing, ProductPricing, ProductStock, ProductSupersession, Brand
from app.domains.products.repository import ProductRepository, BrandRepository
from app.domains.products.schemas import ProductCreate, ProductUpdate, ProductDescriptionCreate, ProductMarketingCreate, ProductPricingCreate
from app.domains.sync_history.models import SyncEntityType, SyncSource, SyncStatus
from app.domains.sync_history.repository import SyncHistoryRepository
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.products.service")
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
| `batch_create_products` `async` |  |
| `batch_update_pricing` `async` |  |
| `create_product` `async` |  |
| `create_supersession` `async` |  |
| `delete_product` `async` |  |
| `get_product` `async` |  |
| `update_pricing` `async` |  |
| `update_product` `async` |  |
| `update_product_status` `async` |  |

##### `__init__`
```python
def __init__(self, db):
```

##### `batch_create_products`
```python
async def batch_create_products(self, products_data, user_id, sync_source) -> Dict[(str, Any)]:
```

##### `batch_update_pricing`
```python
async def batch_update_pricing(self, pricing_data_list, user_id, sync_source) -> Dict[(str, Any)]:
```

##### `create_product`
```python
async def create_product(self, data, user_id, import_id) -> Product:
```

##### `create_supersession`
```python
async def create_supersession(self, old_product_id, new_product_id, reason, user_id) -> ProductSupersession:
```

##### `delete_product`
```python
async def delete_product(self, product_id, user_id) -> None:
```

##### `get_product`
```python
async def get_product(self, product_id) -> Product:
```

##### `update_pricing`
```python
async def update_pricing(self, product_id, pricing_data, user_id, import_id) -> ProductPricing:
```

##### `update_product`
```python
async def update_product(self, product_id, data, user_id, import_id) -> Product:
```

##### `update_product_status`
```python
async def update_product_status(self, product_id, status, reason, user_id) -> Tuple[(Product, ProductActivity)]:
```
