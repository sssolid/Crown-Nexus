# Module: app.domains.autocare.vcdb.service

**Path:** `app/domains/autocare/vcdb/service.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import VCdbException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.vcdb.repository import VCdbRepository
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.vcdb.service")
```

## Classes

| Class | Description |
| --- | --- |
| `VCdbService` |  |

### Class: `VCdbService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `find_base_vehicle` `async` |  |
| `get_all_submodels` `async` |  |
| `get_base_vehicle` `async` |  |
| `get_body_style_config` `async` |  |
| `get_brake_config` `async` |  |
| `get_drive_types` `async` |  |
| `get_engine_base` `async` |  |
| `get_engine_base2` `async` |  |
| `get_engine_config2` `async` |  |
| `get_engine_config_details` `async` |  |
| `get_engine_configs` `async` |  |
| `get_make_by_id` `async` |  |
| `get_makes` `async` |  |
| `get_makes_by_year` `async` |  |
| `get_model_by_id` `async` |  |
| `get_models_by_year_make` `async` |  |
| `get_regions` `async` |  |
| `get_regions_by_parent` `async` |  |
| `get_stats` `async` |  |
| `get_submodels_by_base_vehicle` `async` |  |
| `get_transmission` `async` |  |
| `get_vehicle_by_id` `async` |  |
| `get_vehicle_configurations` `async` |  |
| `get_vehicle_configurations2` `async` |  |
| `get_vehicle_details` `async` |  |
| `get_vehicle_types` `async` |  |
| `get_vehicle_types_by_group` `async` |  |
| `get_version` `async` |  |
| `get_wheel_bases` `async` |  |
| `get_year_range` `async` |  |
| `get_years` `async` |  |
| `import_from_aces` `async` |  |
| `search_base_vehicles` `async` |  |
| `search_engine_bases` `async` |  |
| `search_engine_bases2` `async` |  |
| `search_engine_configs` `async` |  |
| `search_engine_configs2` `async` |  |
| `search_makes` `async` |  |
| `search_models` `async` |  |
| `search_submodels` `async` |  |
| `search_transmissions` `async` |  |
| `search_vehicles` `async` |  |
| `update_database` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `find_base_vehicle`
```python
async def find_base_vehicle(self, year_id, make_id, model_id) -> Optional[Dict[(str, Any)]]:
```

##### `get_all_submodels`
```python
async def get_all_submodels(self) -> List[Dict[(str, Any)]]:
```

##### `get_base_vehicle`
```python
async def get_base_vehicle(self, base_vehicle_id) -> Dict[(str, Any)]:
```

##### `get_body_style_config`
```python
async def get_body_style_config(self, body_style_config_id) -> Dict[(str, Any)]:
```

##### `get_brake_config`
```python
async def get_brake_config(self, brake_config_id) -> Dict[(str, Any)]:
```

##### `get_drive_types`
```python
async def get_drive_types(self) -> List[Dict[(str, Any)]]:
```

##### `get_engine_base`
```python
async def get_engine_base(self, engine_base_id) -> Dict[(str, Any)]:
```

##### `get_engine_base2`
```python
async def get_engine_base2(self, engine_base_id) -> Dict[(str, Any)]:
```

##### `get_engine_config2`
```python
async def get_engine_config2(self, engine_config_id) -> Dict[(str, Any)]:
```

##### `get_engine_config_details`
```python
async def get_engine_config_details(self, engine_config_id) -> Dict[(str, Any)]:
```

##### `get_engine_configs`
```python
async def get_engine_configs(self, engine_config_id) -> Dict[(str, Any)]:
```

##### `get_make_by_id`
```python
async def get_make_by_id(self, make_id) -> Dict[(str, Any)]:
```

##### `get_makes`
```python
async def get_makes(self) -> List[Dict[(str, Any)]]:
```

##### `get_makes_by_year`
```python
async def get_makes_by_year(self, year) -> List[Dict[(str, Any)]]:
```

##### `get_model_by_id`
```python
async def get_model_by_id(self, model_id) -> Dict[(str, Any)]:
```

##### `get_models_by_year_make`
```python
async def get_models_by_year_make(self, year, make_id) -> List[Dict[(str, Any)]]:
```

##### `get_regions`
```python
async def get_regions(self) -> List[Dict[(str, Any)]]:
```

##### `get_regions_by_parent`
```python
async def get_regions_by_parent(self, parent_id) -> List[Dict[(str, Any)]]:
```

##### `get_stats`
```python
async def get_stats(self) -> Dict[(str, Any)]:
```

##### `get_submodels_by_base_vehicle`
```python
async def get_submodels_by_base_vehicle(self, base_vehicle_id) -> List[Dict[(str, Any)]]:
```

##### `get_transmission`
```python
async def get_transmission(self, transmission_id) -> Dict[(str, Any)]:
```

##### `get_vehicle_by_id`
```python
async def get_vehicle_by_id(self, vehicle_id) -> Dict[(str, Any)]:
```

##### `get_vehicle_configurations`
```python
async def get_vehicle_configurations(self, vehicle_id) -> Dict[(str, List[Dict[(str, Any)]])]:
```

##### `get_vehicle_configurations2`
```python
async def get_vehicle_configurations2(self, vehicle_id) -> Dict[(str, List[Dict[(str, Any)]])]:
```

##### `get_vehicle_details`
```python
async def get_vehicle_details(self, vehicle_id) -> Dict[(str, Any)]:
```

##### `get_vehicle_types`
```python
async def get_vehicle_types(self) -> List[Dict[(str, Any)]]:
```

##### `get_vehicle_types_by_group`
```python
async def get_vehicle_types_by_group(self, group_id) -> List[Dict[(str, Any)]]:
```

##### `get_version`
```python
async def get_version(self) -> str:
```

##### `get_wheel_bases`
```python
async def get_wheel_bases(self) -> List[Dict[(str, Any)]]:
```

##### `get_year_range`
```python
async def get_year_range(self) -> Tuple[(int, int)]:
```

##### `get_years`
```python
async def get_years(self) -> List[Dict[(str, Any)]]:
```

##### `import_from_aces`
```python
async def import_from_aces(self, file_path, params) -> Dict[(str, Any)]:
```

##### `search_base_vehicles`
```python
async def search_base_vehicles(self, year, make, model, page, page_size) -> Dict[(str, Any)]:
```

##### `search_engine_bases`
```python
async def search_engine_bases(self, liter, cylinders, page, page_size) -> Dict[(str, Any)]:
```

##### `search_engine_bases2`
```python
async def search_engine_bases2(self, engine_block_id, engine_bore_stroke_id, page, page_size) -> Dict[(str, Any)]:
```

##### `search_engine_configs`
```python
async def search_engine_configs(self, engine_base_id, fuel_type_id, aspiration_id, page, page_size) -> Dict[(str, Any)]:
```

##### `search_engine_configs2`
```python
async def search_engine_configs2(self, engine_base_id, fuel_type_id, aspiration_id, page, page_size) -> Dict[(str, Any)]:
```

##### `search_makes`
```python
async def search_makes(self, search_term) -> List[Dict[(str, Any)]]:
```

##### `search_models`
```python
async def search_models(self, search_term) -> List[Dict[(str, Any)]]:
```

##### `search_submodels`
```python
async def search_submodels(self, search_term) -> List[Dict[(str, Any)]]:
```

##### `search_transmissions`
```python
async def search_transmissions(self, transmission_type_id, transmission_num_speeds_id, transmission_control_type_id, page, page_size) -> Dict[(str, Any)]:
```

##### `search_vehicles`
```python
async def search_vehicles(self, year, make, model, submodel, body_type, engine_config, transmission_type, page, page_size) -> Dict[(str, Any)]:
```

##### `update_database`
```python
async def update_database(self, file_path) -> Dict[(str, Any)]:
```
