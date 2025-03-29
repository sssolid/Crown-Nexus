# Module: app.fitment.models

**Path:** `app/fitment/models.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import re
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
```

## Classes

| Class | Description |
| --- | --- |
| `MappingRule` |  |
| `ModelMapping` |  |
| `PCDBPosition` |  |
| `PartApplication` |  |
| `PartFitment` |  |
| `PartTerminology` |  |
| `Position` |  |
| `PositionGroup` |  |
| `VCDBVehicle` |  |
| `ValidationResult` |  |
| `ValidationStatus` |  |
| `Vehicle` |  |

### Class: `MappingRule`
**Inherits from:** BaseModel

### Class: `ModelMapping`
**Inherits from:** BaseModel

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

### Class: `PCDBPosition`
**Inherits from:** BaseModel

### Class: `PartApplication`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `parse_application` |  |

##### `parse_application`
```python
@model_validator(mode='after')
def parse_application(self) -> 'PartApplication':
```

### Class: `PartFitment`
**Inherits from:** BaseModel

### Class: `PartTerminology`
**Inherits from:** BaseModel

### Class: `Position`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `FRONT` | `'Front'` |
| `REAR` | `'Rear'` |
| `LEFT` | `'Left'` |
| `RIGHT` | `'Right'` |
| `UPPER` | `'Upper'` |
| `LOWER` | `'Lower'` |
| `INNER` | `'Inner'` |
| `OUTER` | `'Outer'` |
| `CENTER` | `'Center'` |
| `NA` | `'N/A'` |
| `VARIES` | `'Varies with Application'` |

### Class: `PositionGroup`
**Inherits from:** BaseModel

### Class: `VCDBVehicle`
**Inherits from:** BaseModel

### Class: `ValidationResult`
**Inherits from:** BaseModel

### Class: `ValidationStatus`
**Inherits from:** Enum

#### Attributes

| Name | Value |
| --- | --- |
| `VALID` | `    VALID = auto()` |
| `WARNING` | `    WARNING = auto()` |
| `ERROR` | `    ERROR = auto()` |

### Class: `Vehicle`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(populate_by_name=True)` |

#### Methods

| Method | Description |
| --- | --- |
| `full_name` `@property` |  |

##### `full_name`
```python
@property
def full_name(self) -> str:
```
