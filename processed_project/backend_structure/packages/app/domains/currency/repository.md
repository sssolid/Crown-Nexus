# Module: app.domains.currency.repository

**Path:** `app/domains/currency/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.currency.models import Currency, ExchangeRate
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, BusinessException
```

## Classes

| Class | Description |
| --- | --- |
| `CurrencyRepository` |  |
| `ExchangeRateRepository` |  |

### Class: `CurrencyRepository`
**Inherits from:** BaseRepository[(Currency, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_code` `async` |  |
| `get_active_currencies` `async` |  |
| `get_base_currency` `async` |  |
| `set_as_base` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, currency_id) -> Currency:
```

##### `find_by_code`
```python
async def find_by_code(self, code) -> Optional[Currency]:
```

##### `get_active_currencies`
```python
async def get_active_currencies(self) -> List[Currency]:
```

##### `get_base_currency`
```python
async def get_base_currency(self) -> Optional[Currency]:
```

##### `set_as_base`
```python
async def set_as_base(self, currency_id) -> Currency:
```

### Class: `ExchangeRateRepository`
**Inherits from:** BaseRepository[(ExchangeRate, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `convert` `async` |  |
| `find_latest_rate` `async` |  |
| `find_rate_at_date` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `convert`
```python
async def convert(self, source_currency_code, target_currency_code, amount) -> Tuple[(float, float, datetime)]:
```

##### `find_latest_rate`
```python
async def find_latest_rate(self, source_currency_id, target_currency_id) -> Optional[ExchangeRate]:
```

##### `find_rate_at_date`
```python
async def find_rate_at_date(self, source_currency_id, target_currency_id, date) -> Optional[ExchangeRate]:
```
