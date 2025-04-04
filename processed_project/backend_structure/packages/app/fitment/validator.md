# Module: app.fitment.validator

**Path:** `app/fitment/validator.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
from typing import Dict, List, Set
from models import PartFitment, PCDBPosition, Position, ValidationResult, ValidationStatus, VCDBVehicle
```

## Global Variables
```python
logger = logger = get_logger("app.fitment.validator")
```

## Classes

| Class | Description |
| --- | --- |
| `FitmentValidator` |  |

### Class: `FitmentValidator`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `validate_fitment` |  |

##### `__init__`
```python
def __init__(self, part_terminology_id, pcdb_positions) -> None:
```

##### `validate_fitment`
```python
def validate_fitment(self, fitment, available_vehicles) -> ValidationResult:
```
