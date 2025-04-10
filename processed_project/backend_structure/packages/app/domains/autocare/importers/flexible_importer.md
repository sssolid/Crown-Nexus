# Module: app.domains.autocare.importers.flexible_importer

**Path:** `app/domains/autocare/importers/flexible_importer.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import csv
import gc
import json
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, Protocol, Set, Type, TypeVar, Union, cast
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base_class import Base
from app.domains.autocare.importers.base_importer import BaseImporter
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.importers.flexible_importer")
T = T = TypeVar("T", bound=Base)
```

## Functions

| Function | Description |
| --- | --- |
| `detect_source_format` |  |

### `detect_source_format`
```python
def detect_source_format(source_path) -> SourceFormat:
```

## Classes

| Class | Description |
| --- | --- |
| `DataSourceReader` |  |
| `FileReader` |  |
| `FlexibleImporter` |  |
| `JsonFileReader` |  |
| `PipeFileReader` |  |
| `SourceFormat` |  |

### Class: `DataSourceReader`
**Inherits from:** ABC

#### Methods

| Method | Description |
| --- | --- |
| `read_records` |  |
| `read_version` |  |
| `validate` |  |

##### `read_records`
```python
@abstractmethod
def read_records(self, source_name) -> Iterator[Dict[(str, Any)]]:
```

##### `read_version`
```python
@abstractmethod
def read_version(self) -> str:
```

##### `validate`
```python
@abstractmethod
def validate(self, required_sources) -> bool:
```

### Class: `FileReader`
**Inherits from:** DataSourceReader

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `validate` |  |

##### `__init__`
```python
def __init__(self, source_path, encoding):
```

##### `validate`
```python
def validate(self, required_sources) -> bool:
```

### Class: `FlexibleImporter`
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
def __init__(self, db, source_path, schema_name, required_sources, version_class, source_format, version_date_field, batch_size, encoding) -> None:
```

##### `import_data`
```python
async def import_data(self) -> Dict[(str, Any)]:
```

##### `register_many_to_many_table`
```python
def register_many_to_many_table(self, source_name, table_name, field_mapping, transformers) -> None:
```

##### `register_table_mapping`
```python
def register_table_mapping(self, source_name, model_class, field_mapping, primary_key, transformers, validators) -> None:
```

##### `set_import_order`
```python
def set_import_order(self, order) -> None:
```

##### `validate_source`
```python
async def validate_source(self) -> bool:
```

### Class: `JsonFileReader`
**Inherits from:** FileReader

#### Methods

| Method | Description |
| --- | --- |
| `read_records` |  |
| `read_version` |  |

##### `read_records`
```python
def read_records(self, source_name) -> Iterator[Dict[(str, Any)]]:
```

##### `read_version`
```python
def read_version(self) -> str:
```

### Class: `PipeFileReader`
**Inherits from:** FileReader

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `read_records` |  |
| `read_version` |  |

##### `__init__`
```python
def __init__(self, source_path, encoding, delimiter):
```

##### `read_records`
```python
def read_records(self, source_name) -> Iterator[Dict[(str, Any)]]:
```

##### `read_version`
```python
def read_version(self) -> str:
```

### Class: `SourceFormat`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `PIPE` | `'pipe'` |
| `JSON` | `'json'` |
