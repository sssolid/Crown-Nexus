# Module: app.commands.init_currencies

**Path:** `app/commands/init_currencies.py`

[Back to Project Index](../../../index.md)

## Imports
```python
import asyncio
import typer
from sqlalchemy import select
from app.db.session import get_db_context
from app.domains.currency.models import Currency
from app.domains.currency.tasks import init_currencies as init_currencies_task
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
