# Module: app.domains.autocare.importers.vcdb_importer

**Path:** `app/domains/autocare/importers/vcdb_importer.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.autocare.importers.flexible_importer import FlexibleImporter, SourceFormat, detect_source_format
from app.domains.autocare.vcdb.models import Make, Year, Model, VehicleType, VehicleTypeGroup, SubModel, Region, BaseVehicle, Vehicle, DriveType, BrakeType, BrakeSystem, BrakeABS, BrakeConfig, BodyType, BodyNumDoors, BodyStyleConfig, EngineBlock, EngineBoreStroke, EngineBase, EngineBase2, Aspiration, FuelType, CylinderHeadType, FuelDeliveryType, FuelDeliverySubType, FuelSystemControlType, FuelSystemDesign, FuelDeliveryConfig, EngineDesignation, EngineVIN, EngineVersion, Valves, Mfr, IgnitionSystemType, PowerOutput, EngineConfig, EngineConfig2, TransmissionType, TransmissionNumSpeeds, TransmissionControlType, TransmissionBase, TransmissionMfrCode, ElecControlled, Transmission, WheelBase, VCdbVersion, BedType, BedLength, BedConfig, MfrBodyCode, SpringType, SpringTypeConfig, SteeringType, SteeringSystem, SteeringConfig, PublicationStage, VehicleToDriveType, VehicleToBrakeConfig, VehicleToBedConfig, VehicleToBodyStyleConfig, VehicleToMfrBodyCode, VehicleToEngineConfig, VehicleToSpringTypeConfig, VehicleToSteeringConfig, VehicleToTransmission, VehicleToWheelBase
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.importers.vcdb_importer")
```

## Classes

| Class | Description |
| --- | --- |
| `VCdbImporter` |  |

### Class: `VCdbImporter`
**Inherits from:** FlexibleImporter

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, db, source_path, source_format, batch_size):
```
