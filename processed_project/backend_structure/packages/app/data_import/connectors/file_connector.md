# Module: app.data_import.connectors.file_connector

**Path:** `app/data_import/connectors/file_connector.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, validator
from app.core.exceptions import ConfigurationException
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.connectors.file_connector")
```

## Classes

| Class | Description |
| --- | --- |
| `FileConnectionConfig` |  |
| `FileConnector` |  |

### Class: `FileConnectionConfig`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_file_path` |  |
| `validate_file_type` |  |

##### `validate_file_path`
```python
@validator('file_path')
def validate_file_path(cls, v) -> str:
```

##### `validate_file_type`
```python
@validator('file_type')
def validate_file_type(cls, v, values) -> str:
```

### Class: `FileConnector`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `close` `async` |  |
| `connect` `async` |  |
| `extract` `async` |  |

##### `__init__`
```python
def __init__(self, config) -> None:
```

##### `close`
```python
async def close(self) -> None:
```

##### `connect`
```python
async def connect(self) -> None:
```

##### `extract`
```python
async def extract(self, query, limit, **params) -> List[Dict[(str, Any)]]:
```
