# Module: app.api.v1.endpoints.currency

**Path:** `app/api/v1/endpoints/currency.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.domains.currency.models import Currency, ExchangeRate
from app.domains.currency.schemas import ConversionRequest, ConversionResponse, CurrencyRead, ExchangeRateRead
from app.domains.currency.service import ExchangeRateService
from app.domains.currency.tasks import update_exchange_rates
from app.domains.users.models import User
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `convert_currency` |  |
| `read_currencies` |  |
| `read_exchange_rates` |  |
| `trigger_exchange_rate_update` |  |

### `convert_currency`
```python
@router.post('/convert', response_model=ConversionResponse)
async def convert_currency(conversion, db, current_user) -> Any:
```

### `read_currencies`
```python
@router.get('/', response_model=List[CurrencyRead])
async def read_currencies(db, current_user, active_only) -> Any:
```

### `read_exchange_rates`
```python
@router.get('/rates', response_model=List[ExchangeRateRead])
async def read_exchange_rates(db, current_user, source_code, target_code, limit) -> Any:
```

### `trigger_exchange_rate_update`
```python
@router.post('/update', status_code=status.HTTP_202_ACCEPTED)
async def trigger_exchange_rate_update(background_tasks, db, current_user, async_update) -> Dict[(str, Any)]:
```
