# Module: app.commands.init_currencies

**Path:** `app/commands/init_currencies.py`

[Back to Project Index](../../../index.md)

## Imports
```python
import asyncio
import sys
import typer
from typing import List, Optional
from sqlalchemy import select
from app.core.config import settings
from app.db.session import get_db_context
from app.models.currency import Currency
from app.tasks.currency_tasks import init_currencies as init_currencies_task
```

## Global Variables
```python
app = app = typer.Typer()
```

## Functions

| Function | Description |
| --- | --- |
| `init_currencies` |  |

### `init_currencies`
```python
@app.command()
def init_currencies(force, sync, base_currency):
```
