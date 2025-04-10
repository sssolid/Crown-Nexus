# Module: app.domains.autocare.handlers

**Path:** `app/domains/autocare/handlers.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
from typing import Any, Dict
from uuid import UUID
from app.core.events import subscribe_to_event
from app.db.session import get_db
from app.domains.autocare.fitment.repository import FitmentMappingRepository
from app.domains.products.repository import ProductRepository
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.handlers")
```

## Functions

| Function | Description |
| --- | --- |
| `handle_autocare_database_updated` |  |
| `handle_product_created` |  |

### `handle_autocare_database_updated`
```python
@subscribe_to_event('autocare.database_updated')
async def handle_autocare_database_updated(payload) -> None:
```

### `handle_product_created`
```python
@subscribe_to_event('products.product_created')
async def handle_product_created(payload) -> None:
```
