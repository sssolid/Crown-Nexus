# Module: app.domains.autocare.vcdb.repository

**Path:** `app/domains/autocare/vcdb/repository.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.vcdb.models import Vehicle, BaseVehicle, Make, Model, Year, SubModel, VehicleType, Region, VCdbVersion, DriveType, BrakeType, BrakeSystem, BrakeABS, BrakeConfig, BodyType, BodyNumDoors, BodyStyleConfig, EngineBlock, EngineBoreStroke, EngineBase, Aspiration, FuelType, CylinderHeadType, FuelDeliveryType, FuelDeliverySubType, FuelSystemControlType, FuelSystemDesign, FuelDeliveryConfig, EngineDesignation, EngineVIN, EngineVersion, Valves, Mfr, IgnitionSystemType, PowerOutput, EngineConfig, TransmissionType, TransmissionNumSpeeds, TransmissionControlType, TransmissionBase, TransmissionMfrCode, ElecControlled, Transmission, WheelBase
```

## Classes

| Class | Description |
| --- | --- |
| `BaseVehicleRepository` |  |
| `BodyStyleConfigRepository` |  |
| `BrakeConfigRepository` |  |
| `DriveTypeRepository` |  |
| `EngineConfigRepository` |  |
| `MakeRepository` |  |
| `ModelRepository` |  |
| `RegionRepository` |  |
| `SubModelRepository` |  |
| `TransmissionRepository` |  |
| `VCdbRepository` |  |
| `VehicleRepository` |  |
| `VehicleTypeRepository` |  |
| `WheelBaseRepository` |  |
| `YearRepository` |  |

### Class: `BaseVehicleRepository`
**Inherits from:** BaseRepository[(BaseVehicle, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `find_by_year_make_model` `async` |  |
| `get_by_base_vehicle_id` `async` |  |
| `search_by_criteria` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `find_by_year_make_model`
```python
async def find_by_year_make_model(self, year_id, make_id, model_id) -> Optional[BaseVehicle]:
```

##### `get_by_base_vehicle_id`
```python
async def get_by_base_vehicle_id(self, base_vehicle_id) -> Optional[BaseVehicle]:
```

##### `search_by_criteria`
```python
async def search_by_criteria(self, year, make, model, page, page_size) -> Dict[(str, Any)]:
```

### Class: `BodyStyleConfigRepository`
**Inherits from:** BaseRepository[(BodyStyleConfig, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_body_style_config_id` `async` |  |
| `get_by_body_type` `async` |  |
| `get_full_body_style_details` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_body_style_config_id`
```python
async def get_by_body_style_config_id(self, body_style_config_id) -> Optional[BodyStyleConfig]:
```

##### `get_by_body_type`
```python
async def get_by_body_type(self, body_type_id) -> List[BodyStyleConfig]:
```

##### `get_full_body_style_details`
```python
async def get_full_body_style_details(self, body_style_config_id) -> Dict[(str, Any)]:
```

### Class: `BrakeConfigRepository`
**Inherits from:** BaseRepository[(BrakeConfig, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_brake_config_id` `async` |  |
| `get_full_brake_config_details` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_brake_config_id`
```python
async def get_by_brake_config_id(self, brake_config_id) -> Optional[BrakeConfig]:
```

##### `get_full_brake_config_details`
```python
async def get_full_brake_config_details(self, brake_config_id) -> Dict[(str, Any)]:
```

### Class: `DriveTypeRepository`
**Inherits from:** BaseRepository[(DriveType, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_drive_types` `async` |  |
| `get_by_drive_type_id` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_drive_types`
```python
async def get_all_drive_types(self) -> List[DriveType]:
```

##### `get_by_drive_type_id`
```python
async def get_by_drive_type_id(self, drive_type_id) -> Optional[DriveType]:
```

### Class: `EngineConfigRepository`
**Inherits from:** BaseRepository[(EngineConfig, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_criteria` `async` |  |
| `get_by_engine_config_id` `async` |  |
| `get_full_engine_details` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_criteria`
```python
async def get_by_criteria(self, engine_base_id, fuel_type_id, aspiration_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_engine_config_id`
```python
async def get_by_engine_config_id(self, engine_config_id) -> Optional[EngineConfig]:
```

##### `get_full_engine_details`
```python
async def get_full_engine_details(self, engine_config_id) -> Dict[(str, Any)]:
```

### Class: `MakeRepository`
**Inherits from:** BaseRepository[(Make, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_makes` `async` |  |
| `get_by_make_id` `async` |  |
| `get_by_year` `async` |  |
| `search_by_name` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_makes`
```python
async def get_all_makes(self) -> List[Make]:
```

##### `get_by_make_id`
```python
async def get_by_make_id(self, make_id) -> Optional[Make]:
```

##### `get_by_year`
```python
async def get_by_year(self, year) -> List[Make]:
```

##### `search_by_name`
```python
async def search_by_name(self, name) -> List[Make]:
```

### Class: `ModelRepository`
**Inherits from:** BaseRepository[(Model, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_model_id` `async` |  |
| `get_by_vehicle_type` `async` |  |
| `get_by_year_make` `async` |  |
| `search_by_name` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_model_id`
```python
async def get_by_model_id(self, model_id) -> Optional[Model]:
```

##### `get_by_vehicle_type`
```python
async def get_by_vehicle_type(self, vehicle_type_id) -> List[Model]:
```

##### `get_by_year_make`
```python
async def get_by_year_make(self, year, make_id) -> List[Model]:
```

##### `search_by_name`
```python
async def search_by_name(self, name) -> List[Model]:
```

### Class: `RegionRepository`
**Inherits from:** BaseRepository[(Region, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_top_level_regions` `async` |  |
| `get_by_parent` `async` |  |
| `get_by_region_id` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_top_level_regions`
```python
async def get_all_top_level_regions(self) -> List[Region]:
```

##### `get_by_parent`
```python
async def get_by_parent(self, parent_id) -> List[Region]:
```

##### `get_by_region_id`
```python
async def get_by_region_id(self, region_id) -> Optional[Region]:
```

### Class: `SubModelRepository`
**Inherits from:** BaseRepository[(SubModel, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_submodels` `async` |  |
| `get_by_submodel_id` `async` |  |
| `search_by_name` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_submodels`
```python
async def get_all_submodels(self) -> List[SubModel]:
```

##### `get_by_submodel_id`
```python
async def get_by_submodel_id(self, submodel_id) -> Optional[SubModel]:
```

##### `search_by_name`
```python
async def search_by_name(self, name) -> List[SubModel]:
```

### Class: `TransmissionRepository`
**Inherits from:** BaseRepository[(Transmission, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_criteria` `async` |  |
| `get_by_transmission_id` `async` |  |
| `get_full_transmission_details` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_criteria`
```python
async def get_by_criteria(self, transmission_type_id, transmission_num_speeds_id, transmission_control_type_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_transmission_id`
```python
async def get_by_transmission_id(self, transmission_id) -> Optional[Transmission]:
```

##### `get_full_transmission_details`
```python
async def get_full_transmission_details(self, transmission_id) -> Dict[(str, Any)]:
```

### Class: `VCdbRepository`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_version` `async` |  |
| `update_version` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_version`
```python
async def get_version(self) -> Optional[str]:
```

##### `update_version`
```python
async def update_version(self, version_date) -> VCdbVersion:
```

### Class: `VehicleRepository`
**Inherits from:** BaseRepository[(Vehicle, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_vehicle_id` `async` |  |
| `get_submodels_by_base_vehicle` `async` |  |
| `get_vehicle_configurations` `async` |  |
| `search` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_vehicle_id`
```python
async def get_by_vehicle_id(self, vehicle_id) -> Optional[Vehicle]:
```

##### `get_submodels_by_base_vehicle`
```python
async def get_submodels_by_base_vehicle(self, base_vehicle_id) -> List[SubModel]:
```

##### `get_vehicle_configurations`
```python
async def get_vehicle_configurations(self, vehicle_id) -> Dict[(str, List[Any])]:
```

##### `search`
```python
async def search(self, year, make, model, submodel, body_type, engine_config, transmission_type, page, page_size) -> Dict[(str, Any)]:
```

### Class: `VehicleTypeRepository`
**Inherits from:** BaseRepository[(VehicleType, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_vehicle_types` `async` |  |
| `get_by_group` `async` |  |
| `get_by_vehicle_type_id` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_vehicle_types`
```python
async def get_all_vehicle_types(self) -> List[VehicleType]:
```

##### `get_by_group`
```python
async def get_by_group(self, vehicle_type_group_id) -> List[VehicleType]:
```

##### `get_by_vehicle_type_id`
```python
async def get_by_vehicle_type_id(self, vehicle_type_id) -> Optional[VehicleType]:
```

### Class: `WheelBaseRepository`
**Inherits from:** BaseRepository[(WheelBase, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_wheel_bases` `async` |  |
| `get_by_wheel_base_id` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_wheel_bases`
```python
async def get_all_wheel_bases(self) -> List[WheelBase]:
```

##### `get_by_wheel_base_id`
```python
async def get_by_wheel_base_id(self, wheel_base_id) -> Optional[WheelBase]:
```

### Class: `YearRepository`
**Inherits from:** BaseRepository[(Year, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_years` `async` |  |
| `get_by_year` `async` |  |
| `get_by_year_id` `async` |  |
| `get_year_range` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_years`
```python
async def get_all_years(self) -> List[Year]:
```

##### `get_by_year`
```python
async def get_by_year(self, year) -> Optional[Year]:
```

##### `get_by_year_id`
```python
async def get_by_year_id(self, year_id) -> Optional[Year]:
```

##### `get_year_range`
```python
async def get_year_range(self) -> Tuple[(int, int)]:
```
