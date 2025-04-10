# Module: app.domains.model_mapping.schemas

**Path:** `app/domains/model_mapping/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

## Classes

| Class | Description |
| --- | --- |
| `ModelMapping` |  |
| `ModelMappingBase` |  |
| `ModelMappingCreate` |  |
| `ModelMappingInDB` |  |
| `ModelMappingPaginatedResponse` |  |
| `ModelMappingUpdate` |  |
| `VehicleMatchRequest` |  |
| `VehicleMatchResponse` |  |

### Class: `ModelMapping`
**Inherits from:** ModelMappingInDB

#### Methods

| Method | Description |
| --- | --- |
| `make` `@property` |  |
| `model` `@property` |  |
| `vehicle_code` `@property` |  |

##### `make`
```python
@property
def make(self) -> str:
```

##### `model`
```python
@property
def model(self) -> str:
```

##### `vehicle_code`
```python
@property
def vehicle_code(self) -> str:
```

### Class: `ModelMappingBase`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_mapping_format` |  |

##### `validate_mapping_format`
```python
@field_validator('mapping')
@classmethod
def validate_mapping_format(cls, v) -> str:
```

### Class: `ModelMappingCreate`
**Inherits from:** ModelMappingBase

### Class: `ModelMappingInDB`
**Inherits from:** ModelMappingBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ModelMappingPaginatedResponse`
**Inherits from:** BaseModel

### Class: `ModelMappingUpdate`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_mapping_format` |  |

##### `validate_mapping_format`
```python
@field_validator('mapping')
@classmethod
def validate_mapping_format(cls, v) -> Optional[str]:
```

### Class: `VehicleMatchRequest`
**Inherits from:** BaseModel

### Class: `VehicleMatchResponse`
**Inherits from:** BaseModel
