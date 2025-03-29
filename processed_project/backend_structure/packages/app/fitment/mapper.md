# Module: app.fitment.mapper

**Path:** `app/fitment/mapper.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from functools import lru_cache
from typing import Any, Dict, List, Optional
from app.logging import get_logger
from db import FitmentDBService
from exceptions import MappingError
from models import PartTerminology, PCDBPosition, ValidationResult, ValidationStatus, VCDBVehicle
from parser import FitmentParser
from validator import FitmentValidator
```

## Global Variables
```python
logger = logger = get_logger("app.fitment.mapper")
```

## Classes

| Class | Description |
| --- | --- |
| `FitmentMappingEngine` |  |

### Class: `FitmentMappingEngine`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `batch_process_applications` |  |
| `configure` |  |
| `configure_from_database` `async` |  |
| `configure_from_file` |  |
| `get_part_terminology` |  |
| `get_pcdb_positions` |  |
| `get_vcdb_vehicles` |  |
| `process_application` |  |
| `refresh_mappings` `async` |  |
| `save_mapping_results` `async` |  |
| `serialize_validation_results` |  |

##### `__init__`
```python
def __init__(self, db_service) -> None:
```

##### `batch_process_applications`
```python
def batch_process_applications(self, application_texts, terminology_id) -> Dict[(str, List[ValidationResult])]:
```

##### `configure`
```python
def configure(self, model_mappings_path) -> None:
```

##### `configure_from_database`
```python
async def configure_from_database(self) -> None:
```

##### `configure_from_file`
```python
def configure_from_file(self, model_mappings_path) -> None:
```

##### `get_part_terminology`
```python
@lru_cache(maxsize=100)
def get_part_terminology(self, terminology_id) -> PartTerminology:
```

##### `get_pcdb_positions`
```python
@lru_cache(maxsize=100)
def get_pcdb_positions(self, terminology_id) -> List[PCDBPosition]:
```

##### `get_vcdb_vehicles`
```python
def get_vcdb_vehicles(self, year, make, model) -> List[VCDBVehicle]:
```

##### `process_application`
```python
def process_application(self, application_text, terminology_id) -> List[ValidationResult]:
```

##### `refresh_mappings`
```python
async def refresh_mappings(self) -> None:
```

##### `save_mapping_results`
```python
async def save_mapping_results(self, product_id, results) -> bool:
```

##### `serialize_validation_results`
```python
def serialize_validation_results(self, results) -> List[Dict[(str, Any)]]:
```
