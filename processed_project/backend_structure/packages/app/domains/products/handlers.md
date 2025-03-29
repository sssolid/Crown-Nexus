# Module: app.domains.products.handlers

**Path:** `app/domains/products/handlers.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
from typing import Any, Dict
from uuid import UUID
from app.core.events import subscribe_to_event
from app.db.session import get_db
from app.domains.products.repository import ProductRepository
```

## Global Variables
```python
logger = logger = get_logger("app.domains.products.handlers")
```

## Functions

| Function | Description |
| --- | --- |
| `handle_critical_stock_level` |  |
| `handle_price_update` |  |

### `handle_critical_stock_level`
```python
@subscribe_to_event('inventory.stock_level_critical')
async def handle_critical_stock_level(payload) -> None:
```

### `handle_price_update`
```python
@subscribe_to_event('pricing.price_update')
async def handle_price_update(payload) -> None:
```
