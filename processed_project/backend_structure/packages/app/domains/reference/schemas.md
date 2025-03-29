# Module: app.domains.reference.schemas

**Path:** `app/domains/reference/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

## Classes

| Class | Description |
| --- | --- |
| `Color` |  |
| `ColorBase` |  |
| `ColorCreate` |  |
| `ColorInDB` |  |
| `ColorUpdate` |  |
| `ConstructionType` |  |
| `ConstructionTypeBase` |  |
| `ConstructionTypeCreate` |  |
| `ConstructionTypeInDB` |  |
| `ConstructionTypeUpdate` |  |
| `Hardware` |  |
| `HardwareBase` |  |
| `HardwareCreate` |  |
| `HardwareInDB` |  |
| `HardwareUpdate` |  |
| `PackagingType` |  |
| `PackagingTypeBase` |  |
| `PackagingTypeCreate` |  |
| `PackagingTypeInDB` |  |
| `PackagingTypeUpdate` |  |
| `TariffCode` |  |
| `TariffCodeBase` |  |
| `TariffCodeCreate` |  |
| `TariffCodeInDB` |  |
| `TariffCodeUpdate` |  |
| `Texture` |  |
| `TextureBase` |  |
| `TextureCreate` |  |
| `TextureInDB` |  |
| `TextureUpdate` |  |
| `UnspscCode` |  |
| `UnspscCodeBase` |  |
| `UnspscCodeCreate` |  |
| `UnspscCodeInDB` |  |
| `UnspscCodeUpdate` |  |
| `Warehouse` |  |
| `WarehouseBase` |  |
| `WarehouseCreate` |  |
| `WarehouseInDB` |  |
| `WarehouseUpdate` |  |

### Class: `Color`
**Inherits from:** ColorInDB

### Class: `ColorBase`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_hex_code` |  |

##### `validate_hex_code`
```python
@field_validator('hex_code')
@classmethod
def validate_hex_code(cls, v) -> Optional[str]:
```

### Class: `ColorCreate`
**Inherits from:** ColorBase

### Class: `ColorInDB`
**Inherits from:** ColorBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ColorUpdate`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_hex_code` |  |

##### `validate_hex_code`
```python
@field_validator('hex_code')
@classmethod
def validate_hex_code(cls, v) -> Optional[str]:
```

### Class: `ConstructionType`
**Inherits from:** ConstructionTypeInDB

### Class: `ConstructionTypeBase`
**Inherits from:** BaseModel

### Class: `ConstructionTypeCreate`
**Inherits from:** ConstructionTypeBase

### Class: `ConstructionTypeInDB`
**Inherits from:** ConstructionTypeBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ConstructionTypeUpdate`
**Inherits from:** BaseModel

### Class: `Hardware`
**Inherits from:** HardwareInDB

### Class: `HardwareBase`
**Inherits from:** BaseModel

### Class: `HardwareCreate`
**Inherits from:** HardwareBase

### Class: `HardwareInDB`
**Inherits from:** HardwareBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `HardwareUpdate`
**Inherits from:** BaseModel

### Class: `PackagingType`
**Inherits from:** PackagingTypeInDB

### Class: `PackagingTypeBase`
**Inherits from:** BaseModel

### Class: `PackagingTypeCreate`
**Inherits from:** PackagingTypeBase

### Class: `PackagingTypeInDB`
**Inherits from:** PackagingTypeBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `PackagingTypeUpdate`
**Inherits from:** BaseModel

### Class: `TariffCode`
**Inherits from:** TariffCodeInDB

### Class: `TariffCodeBase`
**Inherits from:** BaseModel

### Class: `TariffCodeCreate`
**Inherits from:** TariffCodeBase

### Class: `TariffCodeInDB`
**Inherits from:** TariffCodeBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `TariffCodeUpdate`
**Inherits from:** BaseModel

### Class: `Texture`
**Inherits from:** TextureInDB

### Class: `TextureBase`
**Inherits from:** BaseModel

### Class: `TextureCreate`
**Inherits from:** TextureBase

### Class: `TextureInDB`
**Inherits from:** TextureBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `TextureUpdate`
**Inherits from:** BaseModel

### Class: `UnspscCode`
**Inherits from:** UnspscCodeInDB

### Class: `UnspscCodeBase`
**Inherits from:** BaseModel

### Class: `UnspscCodeCreate`
**Inherits from:** UnspscCodeBase

### Class: `UnspscCodeInDB`
**Inherits from:** UnspscCodeBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `UnspscCodeUpdate`
**Inherits from:** BaseModel

### Class: `Warehouse`
**Inherits from:** WarehouseInDB

### Class: `WarehouseBase`
**Inherits from:** BaseModel

### Class: `WarehouseCreate`
**Inherits from:** WarehouseBase

### Class: `WarehouseInDB`
**Inherits from:** WarehouseBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `WarehouseUpdate`
**Inherits from:** BaseModel
