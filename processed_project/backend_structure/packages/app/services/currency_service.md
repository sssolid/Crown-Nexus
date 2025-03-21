# Module: app.services.currency_service

**Path:** `app/services/currency_service.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
from typing import Dict, List, Optional, Union
import httpx
from sqlalchemy import desc, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.cache.decorators import cached
from app.core.config import settings
from app.db.session import get_db_context
from app.models.currency import Currency, ExchangeRate
from app.core.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.services.currency_service")
```

## Classes

| Class | Description |
| --- | --- |
| `ExchangeRateService` |  |

### Class: `ExchangeRateService`

#### Attributes

| Name | Value |
| --- | --- |
| `API_URL` | `'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'` |
| `DATA_SOURCE` | `'exchangerate-api.com'` |

#### Methods

| Method | Description |
| --- | --- |
| `convert_amount` `async` |  |
| `fetch_latest_rates` `async` |  |
| `get_latest_exchange_rate` `async` |  |
| `update_exchange_rates` `async` |  |

##### `convert_amount`
```python
@classmethod
async def convert_amount(cls, db, amount, source_code, target_code) -> Optional[float]:
```

##### `fetch_latest_rates`
```python
@classmethod
async def fetch_latest_rates(cls, db, base_currency) -> Dict[(str, float)]:
```

##### `get_latest_exchange_rate`
```python
@classmethod
@cached(prefix='currency', ttl=3600, backend='redis')
async def get_latest_exchange_rate(cls, db, source_code, target_code) -> Optional[float]:
```

##### `update_exchange_rates`
```python
@classmethod
async def update_exchange_rates(cls, db, force) -> int:
```
