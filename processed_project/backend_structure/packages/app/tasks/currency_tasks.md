# Module: app.tasks.currency_tasks

**Path:** `app/tasks/currency_tasks.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Dict, Optional, List
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db_context
from app.services.currency_service import ExchangeRateService
from app.core.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.tasks.currency_tasks")
```

## Functions

| Function | Description |
| --- | --- |
| `init_currencies` |  |
| `update_exchange_rates` |  |

### `init_currencies`
```python
@shared_task
def init_currencies() -> Dict[(str, Optional[int])]:
```

### `update_exchange_rates`
```python
@shared_task(bind=True, max_retries=3, default_retry_delay=300, autoretry_for=(Exception), retry_backoff=True)
def update_exchange_rates(self) -> Dict[(str, Optional[int])]:
```
