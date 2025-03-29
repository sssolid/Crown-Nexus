# Module: app.domains.autocare.vcdb.models

**Path:** `app/domains/autocare/vcdb/models.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
```

## Global Variables
```python
vehicle_to_drive_type = vehicle_to_drive_type = Table(
    "autocare_vehicle_to_drive_type",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "drive_type_id",
        Integer,
        ForeignKey("autocare_drive_type.drive_type_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_brake_config = vehicle_to_brake_config = Table(
    "autocare_vehicle_to_brake_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "brake_config_id",
        Integer,
        ForeignKey("autocare_brake_config.brake_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_bed_config = vehicle_to_bed_config = Table(
    "autocare_vehicle_to_bed_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "bed_config_id",
        Integer,
        ForeignKey("autocare_bed_config.bed_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_body_style_config = vehicle_to_body_style_config = Table(
    "autocare_vehicle_to_body_style_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "body_style_config_id",
        Integer,
        ForeignKey("autocare_body_style_config.body_style_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_mfr_body_code = vehicle_to_mfr_body_code = Table(
    "autocare_vehicle_to_mfr_body_code",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "mfr_body_code_id",
        Integer,
        ForeignKey("autocare_mfr_body_code.mfr_body_code_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_engine_config = vehicle_to_engine_config = Table(
    "autocare_vehicle_to_engine_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "engine_config_id",
        Integer,
        ForeignKey("autocare_engine_config.engine_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_spring_type_config = vehicle_to_spring_type_config = Table(
    "autocare_vehicle_to_spring_type_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "spring_type_config_id",
        Integer,
        ForeignKey("autocare_spring_type_config.spring_type_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_steering_config = vehicle_to_steering_config = Table(
    "autocare_vehicle_to_steering_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "steering_config_id",
        Integer,
        ForeignKey("autocare_steering_config.steering_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_transmission = vehicle_to_transmission = Table(
    "autocare_vehicle_to_transmission",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "transmission_id",
        Integer,
        ForeignKey("autocare_transmission.transmission_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_wheel_base = vehicle_to_wheel_base = Table(
    "autocare_vehicle_to_wheel_base",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "wheel_base_id",
        Integer,
        ForeignKey("autocare_wheel_base.wheel_base_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
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
| `EngineBlock` |  |
| `EngineBoreStroke` |  |
| `EngineConfig` |  |
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
| `VehicleType` |  |
| `VehicleTypeGroup` |  |
| `WheelBase` |  |
| `Year` |  |

### Class: `Aspiration`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'autocare_aspiration'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="aspiration")` |

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
| `__tablename__` | `'autocare_base_vehicle'` |
| `year` | `    year = relationship("Year", back_populates="base_vehicles")` |
| `make` | `    make = relationship("Make", back_populates="base_vehicles")` |
| `model` | `    model = relationship("Model", back_populates="base_vehicles")` |
| `vehicles` | `    vehicles = relationship("Vehicle", back_populates="base_vehicle")` |

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
| `__tablename__` | `'autocare_bed_config'` |
| `bed_length` | `    bed_length = relationship("BedLength", back_populates="bed_configs")` |
| `bed_type` | `    bed_type = relationship("BedType", back_populates="bed_configs")` |

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
| `__tablename__` | `'autocare_bed_length'` |
| `bed_configs` | `    bed_configs = relationship("BedConfig", back_populates="bed_length")` |

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
| `__tablename__` | `'autocare_bed_type'` |
| `bed_configs` | `    bed_configs = relationship("BedConfig", back_populates="bed_type")` |

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
| `__tablename__` | `'autocare_body_num_doors'` |
| `body_style_configs` | `    body_style_configs = relationship(
        "BodyStyleConfig", back_populates="body_num_doors"
    )` |

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
| `__tablename__` | `'autocare_body_style_config'` |
| `body_num_doors` | `    body_num_doors = relationship("BodyNumDoors", back_populates="body_style_configs")` |
| `body_type` | `    body_type = relationship("BodyType", back_populates="body_style_configs")` |

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
| `__tablename__` | `'autocare_body_type'` |
| `body_style_configs` | `    body_style_configs = relationship("BodyStyleConfig", back_populates="body_type")` |

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
| `__tablename__` | `'autocare_brake_abs'` |
| `brake_configs` | `    brake_configs = relationship("BrakeConfig", back_populates="brake_abs")` |

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
| `__tablename__` | `'autocare_brake_config'` |
| `front_brake_type` | `    front_brake_type = relationship(
        "BrakeType",
        foreign_keys=[front_brake_type_id],
        back_populates="front_brake_configs",
    )` |
| `rear_brake_type` | `    rear_brake_type = relationship(
        "BrakeType",
        foreign_keys=[rear_brake_type_id],
        back_populates="rear_brake_configs",
    )` |
| `brake_system` | `    brake_system = relationship("BrakeSystem", back_populates="brake_configs")` |
| `brake_abs` | `    brake_abs = relationship("BrakeABS", back_populates="brake_configs")` |

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
| `__tablename__` | `'autocare_brake_system'` |
| `brake_configs` | `    brake_configs = relationship("BrakeConfig", back_populates="brake_system")` |

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
| `__tablename__` | `'autocare_brake_type'` |
| `front_brake_configs` | `    front_brake_configs = relationship(
        "BrakeConfig",
        foreign_keys="[BrakeConfig.front_brake_type_id]",
        back_populates="front_brake_type",
    )` |
| `rear_brake_configs` | `    rear_brake_configs = relationship(
        "BrakeConfig",
        foreign_keys="[BrakeConfig.rear_brake_type_id]",
        back_populates="rear_brake_type",
    )` |

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
| `__tablename__` | `'autocare_cylinder_head_type'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="cylinder_head_type")` |

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
| `__tablename__` | `'autocare_drive_type'` |

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
| `__tablename__` | `'autocare_elec_controlled'` |
| `transmissions` | `    transmissions = relationship("Transmission", back_populates="elec_controlled")` |

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
| `__tablename__` | `'autocare_engine_base'` |
| `engine_block` | `    engine_block = relationship("EngineBlock", back_populates="engine_bases")` |
| `engine_bore_stroke` | `    engine_bore_stroke = relationship("EngineBoreStroke", back_populates="engine_bases")` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="engine_base")` |

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
| `__tablename__` | `'autocare_engine_block'` |
| `engine_bases` | `    engine_bases = relationship("EngineBase", back_populates="engine_block")` |

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
| `__tablename__` | `'autocare_engine_bore_stroke'` |
| `engine_bases` | `    engine_bases = relationship("EngineBase", back_populates="engine_bore_stroke")` |

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
| `__tablename__` | `'autocare_engine_config'` |
| `engine_base` | `    engine_base = relationship("EngineBase", back_populates="engine_configs")` |
| `engine_designation` | `    engine_designation = relationship(
        "EngineDesignation", back_populates="engine_configs"
    )` |
| `engine_vin` | `    engine_vin = relationship("EngineVIN", back_populates="engine_configs")` |
| `valves` | `    valves = relationship("Valves", back_populates="engine_configs")` |
| `fuel_delivery_config` | `    fuel_delivery_config = relationship(
        "FuelDeliveryConfig", back_populates="engine_configs"
    )` |
| `aspiration` | `    aspiration = relationship("Aspiration", back_populates="engine_configs")` |
| `cylinder_head_type` | `    cylinder_head_type = relationship(
        "CylinderHeadType", back_populates="engine_configs"
    )` |
| `fuel_type` | `    fuel_type = relationship("FuelType", back_populates="engine_configs")` |
| `ignition_system_type` | `    ignition_system_type = relationship(
        "IgnitionSystemType", back_populates="engine_configs"
    )` |
| `engine_mfr` | `    engine_mfr = relationship("Mfr", back_populates="engine_configs")` |
| `engine_version` | `    engine_version = relationship("EngineVersion", back_populates="engine_configs")` |
| `power_output` | `    power_output = relationship("PowerOutput", back_populates="engine_configs")` |

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
| `__tablename__` | `'autocare_engine_designation'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="engine_designation")` |

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
| `__tablename__` | `'autocare_engine_vin'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="engine_vin")` |

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
| `__tablename__` | `'autocare_engine_version'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="engine_version")` |

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
| `__tablename__` | `'autocare_fuel_delivery_config'` |
| `fuel_delivery_type` | `    fuel_delivery_type = relationship(
        "FuelDeliveryType", back_populates="fuel_delivery_configs"
    )` |
| `fuel_delivery_subtype` | `    fuel_delivery_subtype = relationship(
        "FuelDeliverySubType", back_populates="fuel_delivery_configs"
    )` |
| `fuel_system_control_type` | `    fuel_system_control_type = relationship(
        "FuelSystemControlType", back_populates="fuel_delivery_configs"
    )` |
| `fuel_system_design` | `    fuel_system_design = relationship(
        "FuelSystemDesign", back_populates="fuel_delivery_configs"
    )` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="fuel_delivery_config")` |

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
| `__tablename__` | `'autocare_fuel_delivery_subtype'` |
| `fuel_delivery_configs` | `    fuel_delivery_configs = relationship(
        "FuelDeliveryConfig", back_populates="fuel_delivery_subtype"
    )` |

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
| `__tablename__` | `'autocare_fuel_delivery_type'` |
| `fuel_delivery_configs` | `    fuel_delivery_configs = relationship(
        "FuelDeliveryConfig", back_populates="fuel_delivery_type"
    )` |

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
| `__tablename__` | `'autocare_fuel_system_control_type'` |
| `fuel_delivery_configs` | `    fuel_delivery_configs = relationship(
        "FuelDeliveryConfig", back_populates="fuel_system_control_type"
    )` |

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
| `__tablename__` | `'autocare_fuel_system_design'` |
| `fuel_delivery_configs` | `    fuel_delivery_configs = relationship(
        "FuelDeliveryConfig", back_populates="fuel_system_design"
    )` |

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
| `__tablename__` | `'autocare_fuel_type'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="fuel_type")` |

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
| `__tablename__` | `'autocare_ignition_system_type'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="ignition_system_type")` |

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
| `__tablename__` | `'autocare_make'` |
| `vehicles` | `    vehicles = relationship("Vehicle", back_populates="make")` |
| `base_vehicles` | `    base_vehicles = relationship("BaseVehicle", back_populates="make")` |

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
| `__tablename__` | `'autocare_mfr'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="engine_mfr")` |
| `transmission_configs` | `    transmission_configs = relationship(
        "Transmission", back_populates="transmission_mfr"
    )` |

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
| `__tablename__` | `'autocare_mfr_body_code'` |

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
| `__tablename__` | `'autocare_model'` |
| `base_vehicles` | `    base_vehicles = relationship("BaseVehicle", back_populates="model")` |
| `vehicle_type` | `    vehicle_type = relationship("VehicleType", back_populates="models")` |

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
| `__tablename__` | `'autocare_power_output'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="power_output")` |

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
| `__tablename__` | `'autocare_publication_stage'` |
| `vehicles` | `    vehicles = relationship("Vehicle", back_populates="publication_stage")` |

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
| `__tablename__` | `'autocare_region'` |
| `children` | `    children = relationship("Region", back_populates="parent", remote_side=[region_id])` |
| `parent` | `    parent = relationship("Region", back_populates="children", remote_side=[id])` |
| `vehicles` | `    vehicles = relationship("Vehicle", back_populates="region")` |

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
| `__tablename__` | `'autocare_spring_type'` |
| `front_spring_configs` | `    front_spring_configs = relationship(
        "SpringTypeConfig",
        foreign_keys="[SpringTypeConfig.front_spring_type_id]",
        back_populates="front_spring_type",
    )` |
| `rear_spring_configs` | `    rear_spring_configs = relationship(
        "SpringTypeConfig",
        foreign_keys="[SpringTypeConfig.rear_spring_type_id]",
        back_populates="rear_spring_type",
    )` |

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
| `__tablename__` | `'autocare_spring_type_config'` |
| `front_spring_type` | `    front_spring_type = relationship(
        "SpringType",
        foreign_keys=[front_spring_type_id],
        back_populates="front_spring_configs",
    )` |
| `rear_spring_type` | `    rear_spring_type = relationship(
        "SpringType",
        foreign_keys=[rear_spring_type_id],
        back_populates="rear_spring_configs",
    )` |

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
| `__tablename__` | `'autocare_steering_config'` |
| `steering_type` | `    steering_type = relationship("SteeringType", back_populates="steering_configs")` |
| `steering_system` | `    steering_system = relationship("SteeringSystem", back_populates="steering_configs")` |

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
| `__tablename__` | `'autocare_steering_system'` |
| `steering_configs` | `    steering_configs = relationship("SteeringConfig", back_populates="steering_system")` |

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
| `__tablename__` | `'autocare_steering_type'` |
| `steering_configs` | `    steering_configs = relationship("SteeringConfig", back_populates="steering_type")` |

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
| `__tablename__` | `'autocare_submodel'` |
| `vehicles` | `    vehicles = relationship("Vehicle", back_populates="submodel")` |

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
| `__tablename__` | `'autocare_transmission'` |
| `transmission_base` | `    transmission_base = relationship("TransmissionBase", back_populates="transmissions")` |
| `transmission_mfr_code` | `    transmission_mfr_code = relationship(
        "TransmissionMfrCode", back_populates="transmissions"
    )` |
| `elec_controlled` | `    elec_controlled = relationship("ElecControlled", back_populates="transmissions")` |
| `transmission_mfr` | `    transmission_mfr = relationship("Mfr", back_populates="transmission_configs")` |

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
| `__tablename__` | `'autocare_transmission_base'` |
| `transmission_type` | `    transmission_type = relationship(
        "TransmissionType", back_populates="transmission_bases"
    )` |
| `transmission_num_speeds` | `    transmission_num_speeds = relationship(
        "TransmissionNumSpeeds", back_populates="transmission_bases"
    )` |
| `transmission_control_type` | `    transmission_control_type = relationship(
        "TransmissionControlType", back_populates="transmission_bases"
    )` |
| `transmissions` | `    transmissions = relationship("Transmission", back_populates="transmission_base")` |

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
| `__tablename__` | `'autocare_transmission_control_type'` |
| `transmission_bases` | `    transmission_bases = relationship(
        "TransmissionBase", back_populates="transmission_control_type"
    )` |

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
| `__tablename__` | `'autocare_transmission_mfr_code'` |
| `transmissions` | `    transmissions = relationship("Transmission", back_populates="transmission_mfr_code")` |

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
| `__tablename__` | `'autocare_transmission_num_speeds'` |
| `transmission_bases` | `    transmission_bases = relationship(
        "TransmissionBase", back_populates="transmission_num_speeds"
    )` |

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
| `__tablename__` | `'autocare_transmission_type'` |
| `transmission_bases` | `    transmission_bases = relationship(
        "TransmissionBase", back_populates="transmission_type"
    )` |

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
| `__tablename__` | `'autocare_vcdb_version'` |

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
| `__tablename__` | `'autocare_valves'` |
| `engine_configs` | `    engine_configs = relationship("EngineConfig", back_populates="valves")` |

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
| `__tablename__` | `'autocare_vehicle'` |
| `base_vehicle` | `    base_vehicle = relationship("BaseVehicle", back_populates="vehicles")` |
| `submodel` | `    submodel = relationship("SubModel", back_populates="vehicles")` |
| `region` | `    region = relationship("Region", back_populates="vehicles")` |
| `publication_stage` | `    publication_stage = relationship("PublicationStage", back_populates="vehicles")` |
| `drive_types` | `    drive_types = relationship("DriveType", secondary="autocare_vehicle_to_drive_type")` |
| `brake_configs` | `    brake_configs = relationship(
        "BrakeConfig", secondary="autocare_vehicle_to_brake_config"
    )` |
| `bed_configs` | `    bed_configs = relationship("BedConfig", secondary="autocare_vehicle_to_bed_config")` |
| `body_style_configs` | `    body_style_configs = relationship(
        "BodyStyleConfig", secondary="autocare_vehicle_to_body_style_config"
    )` |
| `mfr_body_codes` | `    mfr_body_codes = relationship(
        "MfrBodyCode", secondary="autocare_vehicle_to_mfr_body_code"
    )` |
| `engine_configs` | `    engine_configs = relationship(
        "EngineConfig", secondary="autocare_vehicle_to_engine_config"
    )` |
| `spring_type_configs` | `    spring_type_configs = relationship(
        "SpringTypeConfig", secondary="autocare_vehicle_to_spring_type_config"
    )` |
| `steering_configs` | `    steering_configs = relationship(
        "SteeringConfig", secondary="autocare_vehicle_to_steering_config"
    )` |
| `transmissions` | `    transmissions = relationship(
        "Transmission", secondary="autocare_vehicle_to_transmission"
    )` |
| `wheel_bases` | `    wheel_bases = relationship("WheelBase", secondary="autocare_vehicle_to_wheel_base")` |

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
def year(self) -> int:
```

### Class: `VehicleType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'autocare_vehicle_type'` |
| `models` | `    models = relationship("Model", back_populates="vehicle_type")` |
| `vehicle_type_group` | `    vehicle_type_group = relationship(
        "VehicleTypeGroup", back_populates="vehicle_types"
    )` |

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
| `__tablename__` | `'autocare_vehicle_type_group'` |
| `vehicle_types` | `    vehicle_types = relationship("VehicleType", back_populates="vehicle_type_group")` |

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
| `__tablename__` | `'autocare_wheel_base'` |

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
| `__tablename__` | `'autocare_year'` |
| `base_vehicles` | `    base_vehicles = relationship("BaseVehicle", back_populates="year")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
