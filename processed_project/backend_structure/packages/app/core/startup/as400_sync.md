# Module: app.core.startup.as400_sync

**Path:** `app/core/startup/as400_sync.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.config.integrations.as400 import as400_settings
from app.logging import get_logger
from app.services.as400_sync_service import as400_sync_service, SyncEntityType
```

## Global Variables
```python
logger = logger = get_logger("app.core.startup.as400_sync")
```

## Functions

| Function | Description |
| --- | --- |
| `initialize_as400_sync` |  |
| `shutdown_as400_sync` |  |

### `initialize_as400_sync`
```python
async def initialize_as400_sync() -> None:
```

### `shutdown_as400_sync`
```python
async def shutdown_as400_sync() -> None:
```
