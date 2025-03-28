# Module: app.fitment.dependencies

**Path:** `app/fitment/dependencies.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import os
from functools import lru_cache
from app.core.config import settings as app_settings
from db import FitmentDBService
from exceptions import ConfigurationError
from mapper import FitmentMappingEngine
```

## Functions

| Function | Description |
| --- | --- |
| `get_fitment_db_service` |  |
| `get_fitment_mapping_engine` |  |
| `initialize_mapping_engine` |  |

### `get_fitment_db_service`
```python
@lru_cache(maxsize=1)
def get_fitment_db_service() -> FitmentDBService:
```

### `get_fitment_mapping_engine`
```python
@lru_cache(maxsize=1)
def get_fitment_mapping_engine() -> FitmentMappingEngine:
```

### `initialize_mapping_engine`
```python
async def initialize_mapping_engine() -> None:
```
