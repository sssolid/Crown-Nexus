# Module: app.fitment.validator

**Path:** `app/fitment/validator.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import logging
from typing import Dict, List, Optional, Set, Tuple
from models import PartFitment, PartTerminology, PCDBPosition, Position, ValidationResult, ValidationStatus, VCDBVehicle
from exceptions import ValidationError
```

## Global Variables
```python
logger = logger = logging.getLogger(__name__)
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
