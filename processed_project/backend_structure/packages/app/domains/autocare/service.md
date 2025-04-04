# Module: app.domains.autocare.service

**Path:** `app/domains/autocare/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
from pathlib import Path
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import publish_event
from app.domains.autocare.exceptions import AutocareException, ImportException, ExportException
from app.domains.autocare.schemas import AutocareImportParams, AutocareExportParams, DataType, FileFormat
from app.domains.autocare.vcdb.service import VCdbService
from app.domains.autocare.pcdb.service import PCdbService
from app.domains.autocare.padb.service import PAdbService
from app.domains.autocare.qdb.service import QdbService
from app.domains.autocare.fitment.service import FitmentMappingService
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.service")
```

## Classes

| Class | Description |
| --- | --- |
| `AutocareService` |  |

### Class: `AutocareService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `export_data` `async` |  |
| `get_database_versions` `async` |  |
| `import_data` `async` |  |
| `update_database` `async` |  |

##### `__init__`
```python
def __init__(self, db):
```

##### `export_data`
```python
async def export_data(self, params) -> Dict[(str, Any)]:
```

##### `get_database_versions`
```python
async def get_database_versions(self) -> Dict[(str, str)]:
```

##### `import_data`
```python
async def import_data(self, params) -> Dict[(str, Any)]:
```

##### `update_database`
```python
async def update_database(self, database_type, file_path) -> Dict[(str, Any)]:
```
