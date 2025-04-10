# Module: app.api.v1.endpoints.autocare.vcdb

**Path:** `app/api/v1/endpoints/autocare/vcdb.py`

[Back to Project Index](../../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Annotated, Any, Dict, List, Optional, Tuple, Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db, get_pagination
from app.api.responses import paginated_response, success_response
from app.domains.autocare.vcdb.service import VCdbService
from app.domains.users.models import User
```

## Global Variables
```python
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `find_base_vehicle` |  |
| `get_all_submodels` |  |
| `get_base_vehicle` |  |
| `get_body_style_config` |  |
| `get_brake_config` |  |
| `get_drive_types` |  |
| `get_engine_config` |  |
| `get_make_by_id` |  |
| `get_makes` |  |
| `get_makes_by_year` |  |
| `get_model_by_id` |  |
| `get_models_by_year_make` |  |
| `get_regions` |  |
| `get_regions_by_parent` |  |
| `get_submodels_by_base_vehicle` |  |
| `get_transmission` |  |
| `get_vcdb_stats` |  |
| `get_vehicle_by_id` |  |
| `get_vehicle_configurations` |  |
| `get_vehicle_details` |  |
| `get_vehicle_types` |  |
| `get_vehicle_types_by_group` |  |
| `get_version` |  |
| `get_wheel_bases` |  |
| `get_year_range` |  |
| `get_years` |  |
| `search_base_vehicles` |  |
| `search_engine_configs` |  |
| `search_makes` |  |
| `search_models` |  |
| `search_submodels` |  |
| `search_transmissions` |  |
| `search_vehicles` |  |

### `find_base_vehicle`
```python
@router.get('/base-vehicles/find')
async def find_base_vehicle(db, year_id, make_id, model_id) -> Optional[Dict[(str, Any)]]:
```

### `get_all_submodels`
```python
@router.get('/submodels')
async def get_all_submodels(db) -> List[Dict[(str, Any)]]:
```

### `get_base_vehicle`
```python
@router.get('/base-vehicles/{base_vehicle_id}')
async def get_base_vehicle(base_vehicle_id, db) -> Dict[(str, Any)]:
```

### `get_body_style_config`
```python
@router.get('/body-style-configs/{body_style_config_id}')
async def get_body_style_config(body_style_config_id, db) -> Dict[(str, Any)]:
```

### `get_brake_config`
```python
@router.get('/brake-configs/{brake_config_id}')
async def get_brake_config(brake_config_id, db) -> Dict[(str, Any)]:
```

### `get_drive_types`
```python
@router.get('/drive-types')
async def get_drive_types(db) -> List[Dict[(str, Any)]]:
```

### `get_engine_config`
```python
@router.get('/engine-configs/{engine_config_id}')
async def get_engine_config(engine_config_id, db) -> Dict[(str, Any)]:
```

### `get_make_by_id`
```python
@router.get('/makes/{make_id}')
async def get_make_by_id(make_id, db) -> Dict[(str, Any)]:
```

### `get_makes`
```python
@router.get('/makes')
async def get_makes(db) -> List[Dict[(str, Any)]]:
```

### `get_makes_by_year`
```python
@router.get('/years/{year}/makes')
async def get_makes_by_year(year, db) -> List[Dict[(str, Any)]]:
```

### `get_model_by_id`
```python
@router.get('/models/{model_id}')
async def get_model_by_id(model_id, db) -> Dict[(str, Any)]:
```

### `get_models_by_year_make`
```python
@router.get('/years/{year}/makes/{make_id}/models')
async def get_models_by_year_make(year, make_id, db) -> List[Dict[(str, Any)]]:
```

### `get_regions`
```python
@router.get('/regions')
async def get_regions(db) -> List[Dict[(str, Any)]]:
```

### `get_regions_by_parent`
```python
@router.get('/regions/{parent_id}/children')
async def get_regions_by_parent(parent_id, db) -> List[Dict[(str, Any)]]:
```

### `get_submodels_by_base_vehicle`
```python
@router.get('/base-vehicles/{base_vehicle_id}/submodels')
async def get_submodels_by_base_vehicle(base_vehicle_id, db) -> List[Dict[(str, Any)]]:
```

### `get_transmission`
```python
@router.get('/transmissions/{transmission_id}')
async def get_transmission(transmission_id, db) -> Dict[(str, Any)]:
```

### `get_vcdb_stats`
```python
@router.get('/stats')
async def get_vcdb_stats(db) -> Dict[(str, Any)]:
```

### `get_vehicle_by_id`
```python
@router.get('/vehicles/{vehicle_id}')
async def get_vehicle_by_id(vehicle_id, db) -> Dict[(str, Any)]:
```

### `get_vehicle_configurations`
```python
@router.get('/vehicles/{vehicle_id}/configurations')
async def get_vehicle_configurations(vehicle_id, db, use_config2) -> Dict[(str, Any)]:
```

### `get_vehicle_details`
```python
@router.get('/vehicles/{vehicle_id}/details')
async def get_vehicle_details(vehicle_id, db) -> Dict[(str, Any)]:
```

### `get_vehicle_types`
```python
@router.get('/vehicle-types')
async def get_vehicle_types(db) -> List[Dict[(str, Any)]]:
```

### `get_vehicle_types_by_group`
```python
@router.get('/vehicle-type-groups/{group_id}/vehicle-types')
async def get_vehicle_types_by_group(group_id, db) -> List[Dict[(str, Any)]]:
```

### `get_version`
```python
@router.get('/version')
async def get_version(db) -> str:
```

### `get_wheel_bases`
```python
@router.get('/wheel-bases')
async def get_wheel_bases(db) -> List[Dict[(str, Any)]]:
```

### `get_year_range`
```python
@router.get('/years/range')
async def get_year_range(db) -> Tuple[(int, int)]:
```

### `get_years`
```python
@router.get('/years')
async def get_years(db) -> List[Dict[(str, Any)]]:
```

### `search_base_vehicles`
```python
@router.get('/base-vehicles/search')
async def search_base_vehicles(db, year, make, model, page, page_size) -> Dict[(str, Any)]:
```

### `search_engine_configs`
```python
@router.get('/engine-configs/search')
async def search_engine_configs(db, engine_base_id, fuel_type_id, aspiration_id, page, page_size) -> Dict[(str, Any)]:
```

### `search_makes`
```python
@router.get('/makes/search')
async def search_makes(db, search_term) -> List[Dict[(str, Any)]]:
```

### `search_models`
```python
@router.get('/models/search')
async def search_models(db, search_term) -> List[Dict[(str, Any)]]:
```

### `search_submodels`
```python
@router.get('/submodels/search')
async def search_submodels(db, search_term) -> List[Dict[(str, Any)]]:
```

### `search_transmissions`
```python
@router.get('/transmissions/search')
async def search_transmissions(db, transmission_type_id, transmission_num_speeds_id, transmission_control_type_id, page, page_size) -> Dict[(str, Any)]:
```

### `search_vehicles`
```python
@router.get('/vehicles/search')
async def search_vehicles(db, year, make, model, submodel, engine_config, transmission_type, body_type, page, page_size) -> Dict[(str, Any)]:
```
