# Module: app.services.vehicle

**Path:** `app/services/vehicle.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import re
from typing import Dict, List, Optional, Any
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.cache.decorators import cached
from app.core.exceptions import DatabaseException, ErrorCode, ValidationException
from app.logging import get_logger
from app.domains.products.models import Fitment
```

## Global Variables
```python
logger = logger = get_logger("app.services.vehicle")
```

## Functions

| Function | Description |
| --- | --- |
| `get_vehicle_service` |  |

### `get_vehicle_service`
```python
async def get_vehicle_service(db) -> VehicleDataService:
```

## Classes

| Class | Description |
| --- | --- |
| `VehicleDataService` |  |

### Class: `VehicleDataService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `decode_vin` `async` |  |
| `get_engines` `async` |  |
| `get_makes` `async` |  |
| `get_models` `async` |  |
| `get_transmissions` `async` |  |
| `get_years` `async` |  |
| `register` |  |
| `standardize_make` `async` |  |
| `validate_fitment` `async` |  |

##### `__init__`
```python
def __init__(self, db):
```

##### `decode_vin`
```python
@cached(ttl=86400, backend='redis')
async def decode_vin(self, vin) -> Optional[Dict[(str, Any)]]:
```

##### `get_engines`
```python
@cached(prefix='vehicle:engines', ttl=3600, backend='redis')
async def get_engines(self, make, model, year) -> List[str]:
```

##### `get_makes`
```python
@cached(ttl=3600, backend='redis', prefix='vehicle:makes')
async def get_makes(self, year) -> List[str]:
```

##### `get_models`
```python
@cached(prefix='vehicle:models', ttl=3600, backend='redis')
async def get_models(self, make, year) -> List[str]:
```

##### `get_transmissions`
```python
@cached(prefix='vehicle:transmissions', ttl=3600, backend='redis')
async def get_transmissions(self, make, model, year, engine) -> List[str]:
```

##### `get_years`
```python
@cached(prefix='vehicle:years', ttl=3600, backend='redis')
async def get_years(self) -> List[int]:
```

##### `register`
```python
@classmethod
def register(cls) -> None:
```

##### `standardize_make`
```python
@cached(ttl=3600, backend='redis')
async def standardize_make(self, make) -> str:
```

##### `validate_fitment`
```python
@cached(ttl=3600, backend='redis')
async def validate_fitment(self, year, make, model, engine, transmission) -> bool:
```
