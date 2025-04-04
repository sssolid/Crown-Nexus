# Module: app.domains.autocare.vcdb.schemas

**Path:** `app/domains/autocare/vcdb/schemas.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
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
| `Valves` |  |
| `Vehicle` |  |
| `VehicleDetail` |  |
| `VehicleSearchParameters` |  |
| `VehicleSearchResponse` |  |
| `VehicleType` |  |
| `VehicleTypeGroup` |  |
| `WheelBase` |  |
| `Year` |  |

### Class: `Aspiration`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BaseVehicle`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BedConfig`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BedLength`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BedType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BodyNumDoors`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BodyStyleConfig`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BodyType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BrakeABS`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BrakeConfig`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BrakeSystem`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `BrakeType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `CylinderHeadType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `DriveType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ElecControlled`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `EngineBase`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `EngineBlock`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `EngineBoreStroke`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `EngineConfig`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `EngineDesignation`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `EngineVIN`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `EngineVersion`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FuelDeliveryConfig`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FuelDeliverySubType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FuelDeliveryType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FuelSystemControlType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FuelSystemDesign`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `FuelType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `IgnitionSystemType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Make`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Mfr`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `MfrBodyCode`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Model`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `PowerOutput`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `PublicationStage`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Region`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `SpringType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `SpringTypeConfig`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `SteeringConfig`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `SteeringSystem`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `SteeringType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `SubModel`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Transmission`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `TransmissionBase`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `TransmissionControlType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `TransmissionMfrCode`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `TransmissionNumSpeeds`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `TransmissionType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Valves`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Vehicle`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `VehicleDetail`
**Inherits from:** Vehicle

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `VehicleSearchParameters`
**Inherits from:** BaseModel

### Class: `VehicleSearchResponse`
**Inherits from:** BaseModel

### Class: `VehicleType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `VehicleTypeGroup`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `WheelBase`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Year`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |
