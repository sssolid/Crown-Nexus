# Module: app.data_import.commands.sync_as400

**Path:** `app/data_import/commands/sync_as400.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, Optional
import typer
from app.core.config.integrations.as400 import get_as400_connector_config
from app.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
from app.services.as400_sync_service import as400_sync_service, SyncEntityType
```

## Global Variables
```python
logger = logger = get_logger("app.commands.sync_as400")
app = app = typer.Typer()
```

## Functions

| Function | Description |
| --- | --- |
| `schedule` |  |
| `status` |  |
| `sync` |  |
| `test_connection` |  |

### `schedule`
```python
@app.command()
def schedule(entity_type, delay) -> None:
```

### `status`
```python
@app.command()
def status(entity_type, json_output) -> None:
```

### `sync`
```python
@app.command()
def sync(entity_type, force, dry_run, output_file) -> None:
```

### `test_connection`
```python
@app.command()
def test_connection() -> None:
```
