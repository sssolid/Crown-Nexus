# Module: app.api.v1.endpoints.search

**Path:** `app/api/v1/endpoints/search.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db
from app.domains.users.models import User
from app.services.search import SearchService, get_search_service
from app.services.vehicle import VehicleDataService, get_vehicle_service
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `decode_vin` |  |
| `get_vehicle_engines` |  |
| `get_vehicle_makes` |  |
| `get_vehicle_models` |  |
| `get_vehicle_transmissions` |  |
| `get_vehicle_years` |  |
| `global_search` |  |
| `search_fitments` |  |
| `search_products` |  |
| `validate_vehicle_fitment` |  |

### `decode_vin`
```python
@router.get('/vehicle-data/decode-vin/{vin}')
async def decode_vin(vin, db, current_user, vehicle_service) -> Any:
```

### `get_vehicle_engines`
```python
@router.get('/vehicle-data/engines')
async def get_vehicle_engines(db, current_user, vehicle_service, make, model, year) -> List[str]:
```

### `get_vehicle_makes`
```python
@router.get('/vehicle-data/makes')
async def get_vehicle_makes(db, current_user, vehicle_service, year) -> List[str]:
```

### `get_vehicle_models`
```python
@router.get('/vehicle-data/models')
async def get_vehicle_models(db, current_user, vehicle_service, make, year) -> List[str]:
```

### `get_vehicle_transmissions`
```python
@router.get('/vehicle-data/transmissions')
async def get_vehicle_transmissions(db, current_user, vehicle_service, make, model, year, engine) -> List[str]:
```

### `get_vehicle_years`
```python
@router.get('/vehicle-data/years')
async def get_vehicle_years(db, current_user, vehicle_service) -> List[int]:
```

### `global_search`
```python
@router.get('/')
async def global_search(db, current_user, search_service, q, entity_types, page, page_size) -> Any:
```

### `search_fitments`
```python
@router.get('/fitments')
async def search_fitments(db, current_user, search_service, q, year, make, model, engine, transmission, page, page_size) -> Any:
```

### `search_products`
```python
@router.get('/products')
async def search_products(db, current_user, search_service, q, is_active, page, page_size, use_elasticsearch) -> Any:
```

### `validate_vehicle_fitment`
```python
@router.post('/vehicle-data/validate-fitment')
async def validate_vehicle_fitment(db, current_user, vehicle_service, year, make, model, engine, transmission) -> dict:
```
