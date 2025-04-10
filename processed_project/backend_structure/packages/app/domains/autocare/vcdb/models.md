# Module: app.domains.autocare.vcdb.models

**Path:** `app/domains/autocare/vcdb/models.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
```

## Classes

| Class | Description |
| --- | --- |
| `Aspiration` |  |
| `BaseVehicle` |  |
| `BedConfig` |  |
| `BedLength` |  |
| `BedType` |  |
| `BodyNumDoors` |  |
| `BodyStyleConfig` |  |
| `BodyType` |  |
| `BrakeABS` |  |
| `BrakeConfig` |  |
| `BrakeSystem` |  |
| `BrakeType` |  |
| `CylinderHeadType` |  |
| `DriveType` |  |
| `ElecControlled` |  |
| `EngineBase` |  |
| `EngineBase2` |  |
| `EngineBlock` |  |
| `EngineBoreStroke` |  |
| `EngineConfig` |  |
| `EngineConfig2` |  |
| `EngineDesignation` |  |
| `EngineVIN` |  |
| `EngineVersion` |  |
| `FuelDeliveryConfig` |  |
| `FuelDeliverySubType` |  |
| `FuelDeliveryType` |  |
| `FuelSystemControlType` |  |
| `FuelSystemDesign` |  |
| `FuelType` |  |
| `IgnitionSystemType` |  |
| `Make` |  |
| `Mfr` |  |
| `MfrBodyCode` |  |
| `Model` |  |
| `PowerOutput` |  |
| `PublicationStage` |  |
| `Region` |  |
| `SpringType` |  |
| `SpringTypeConfig` |  |
| `SteeringConfig` |  |
| `SteeringSystem` |  |
| `SteeringType` |  |
| `SubModel` |  |
| `Transmission` |  |
| `TransmissionBase` |  |
| `TransmissionControlType` |  |
| `TransmissionMfrCode` |  |
| `TransmissionNumSpeeds` |  |
| `TransmissionType` |  |
| `VCdbVersion` |  |
| `Valves` |  |
| `Vehicle` |  |
| `VehicleToBedConfig` |  |
| `VehicleToBodyStyleConfig` |  |
| `VehicleToBrakeConfig` |  |
| `VehicleToDriveType` |  |
| `VehicleToEngineConfig` |  |
| `VehicleToMfrBodyCode` |  |
| `VehicleToSpringTypeConfig` |  |
| `VehicleToSteeringConfig` |  |
| `VehicleToTransmission` |  |
| `VehicleToWheelBase` |  |
| `VehicleType` |  |
| `VehicleTypeGroup` |  |
| `WheelBase` |  |
| `Year` |  |

### Class: `Aspiration`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'aspiration'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BaseVehicle`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'base_vehicle'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BedConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'bed_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BedLength`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'bed_length'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BedType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'bed_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BodyNumDoors`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'body_num_doors'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BodyStyleConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'body_style_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BodyType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'body_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BrakeABS`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'brake_abs'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BrakeConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'brake_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BrakeSystem`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'brake_system'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `BrakeType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'brake_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `CylinderHeadType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'cylinder_head_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `DriveType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'drive_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ElecControlled`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'elec_controlled'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `EngineBase`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'engine_base'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `EngineBase2`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'engine_base2'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `EngineBlock`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'engine_block'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `EngineBoreStroke`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'engine_bore_stroke'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `EngineConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'engine_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `EngineConfig2`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'engine_config2'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `EngineDesignation`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'engine_designation'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `EngineVIN`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'engine_vin'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `EngineVersion`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'engine_version'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `FuelDeliveryConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'fuel_delivery_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `FuelDeliverySubType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'fuel_delivery_subtype'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `FuelDeliveryType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'fuel_delivery_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `FuelSystemControlType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'fuel_system_control_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `FuelSystemDesign`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'fuel_system_design'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `FuelType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'fuel_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `IgnitionSystemType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'ignition_system_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Make`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'make'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Mfr`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'mfr'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `MfrBodyCode`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'mfr_body_code'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Model`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'model'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PowerOutput`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'power_output'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PublicationStage`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'publication_stage'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Region`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'region'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `SpringType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'spring_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `SpringTypeConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'spring_type_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `SteeringConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'steering_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `SteeringSystem`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'steering_system'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `SteeringType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'steering_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `SubModel`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'submodel'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Transmission`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'transmission'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `TransmissionBase`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'transmission_base'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `TransmissionControlType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'transmission_control_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `TransmissionMfrCode`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'transmission_mfr_code'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `TransmissionNumSpeeds`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'transmission_num_speeds'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `TransmissionType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'transmission_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VCdbVersion`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vcdb_version'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Valves`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'valves'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Vehicle`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |
| `make` `@property` |  |
| `model` `@property` |  |
| `year` `@property` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

##### `make`
```python
@property
def make(self) -> Make:
```

##### `model`
```python
@property
def model(self) -> str:
```

##### `year`
```python
@property
def year(self) -> Optional[int]:
```

### Class: `VehicleToBedConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_bed_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleToBodyStyleConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_body_style_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleToBrakeConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_brake_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleToDriveType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_drive_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleToEngineConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_engine_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleToMfrBodyCode`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_mfr_body_code'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleToSpringTypeConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_spring_type_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleToSteeringConfig`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_steering_config'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleToTransmission`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_transmission'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleToWheelBase`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_to_wheel_base'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `VehicleTypeGroup`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'vehicle_type_group'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `WheelBase`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'wheel_base'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Year`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'year'` |
| `__table_args__` | `    __table_args__ = {"schema": "vcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
