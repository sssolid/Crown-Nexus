# Module: app.domains.autocare.importers.pipe_file_importer

**Path:** `app/domains/autocare/importers/pipe_file_importer.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import csv
import gc
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Generic, List, Optional, Set, Type, TypeVar
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base_class import Base
from app.domains.autocare.importers.base_importer import BaseImporter
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.importers.pipe_file_importer")
T = T = TypeVar("T", bound=Base)
```

## Classes

| Class | Description |
| --- | --- |
| `PipeFileImporter` |  |

### Class: `PipeFileImporter`
**Inherits from:** Generic[T]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `import_data` `async` |  |
| `register_many_to_many_table` |  |
| `register_table_mapping` |  |
| `set_import_order` |  |
| `validate_source` `async` |  |

##### `__init__`
```python
def __init__(self, db, source_path, schema_name, required_files, version_class, version_date_field, batch_size, encoding, delimiter) -> None:
```

##### `import_data`
```python
async def import_data(self) -> Dict[(str, Any)]:
```

##### `register_many_to_many_table`
```python
def register_many_to_many_table(self, file_name, table_name, field_mapping, transformers) -> None:
```

##### `register_table_mapping`
```python
def register_table_mapping(self, file_name, model_class, field_mapping, primary_key, transformers, validators) -> None:
```

##### `set_import_order`
```python
def set_import_order(self, order) -> None:
```

##### `validate_source`
```python
async def validate_source(self) -> bool:
```
