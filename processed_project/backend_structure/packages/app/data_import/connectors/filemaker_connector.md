# Module: app.data_import.connectors.filemaker_connector

**Path:** `app/data_import/connectors/filemaker_connector.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional
import pyodbc
from pydantic import BaseModel, Field, validator
from app.core.exceptions import DatabaseException
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.connectors.filemaker_connector")
```

## Classes

| Class | Description |
| --- | --- |
| `FileMakerConnectionConfig` |  |
| `FileMakerConnector` |  |

### Class: `FileMakerConnectionConfig`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_port` |  |

##### `validate_port`
```python
@validator('port')
def validate_port(cls, v) -> Optional[int]:
```

### Class: `FileMakerConnector`

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
