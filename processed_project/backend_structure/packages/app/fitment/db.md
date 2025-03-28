# Module: app.fitment.db

**Path:** `app/fitment/db.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple
import pyodbc
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.logging import get_logger
from exceptions import DatabaseError
from models import PCDBPosition, PartTerminology, VCDBVehicle
```

## Global Variables
```python
logger = logger = get_logger("app.fitment.db")
```

## Classes

| Class | Description |
| --- | --- |
| `AccessDBClient` |  |
| `FitmentDBService` |  |

### Class: `AccessDBClient`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `connect` |  |
| `query` |  |

##### `__init__`
```python
def __init__(self, db_path) -> None:
```

##### `connect`
```python
def connect(self) -> pyodbc.Connection:
```

##### `query`
```python
def query(self, sql, params) -> List[Dict[(str, Any)]]:
```

### Class: `FitmentDBService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `add_model_mapping` `async` |  |
| `delete_model_mapping` `async` |  |
| `get_model_mappings` `async` |  |
| `get_pcdb_part_terminology` |  |
| `get_pcdb_positions` |  |
| `get_session` `async` |  |
| `get_vcdb_vehicles` |  |
| `import_mappings_from_json` `async` |  |
| `load_model_mappings_from_json` |  |
| `save_fitment_results` `async` |  |
| `update_model_mapping` `async` |  |

##### `__init__`
```python
def __init__(self, vcdb_path, pcdb_path, sqlalchemy_url) -> None:
```

##### `add_model_mapping`
```python
async def add_model_mapping(self, pattern, mapping, priority) -> int:
```

##### `delete_model_mapping`
```python
async def delete_model_mapping(self, mapping_id) -> bool:
```

##### `get_model_mappings`
```python
async def get_model_mappings(self) -> Dict[(str, List[str])]:
```

##### `get_pcdb_part_terminology`
```python
def get_pcdb_part_terminology(self, terminology_id) -> PartTerminology:
```

##### `get_pcdb_positions`
```python
def get_pcdb_positions(self, position_ids) -> List[PCDBPosition]:
```

##### `get_session`
```python
@asynccontextmanager
async def get_session(self) -> AsyncGenerator[(AsyncSession, None)]:
```

##### `get_vcdb_vehicles`
```python
def get_vcdb_vehicles(self, year, make, model) -> List[VCDBVehicle]:
```

##### `import_mappings_from_json`
```python
async def import_mappings_from_json(self, json_data) -> int:
```

##### `load_model_mappings_from_json`
```python
def load_model_mappings_from_json(self, json_path) -> Dict[(str, List[str])]:
```

##### `save_fitment_results`
```python
async def save_fitment_results(self, product_id, fitments) -> bool:
```

##### `update_model_mapping`
```python
async def update_model_mapping(self, mapping_id, **kwargs) -> bool:
```
