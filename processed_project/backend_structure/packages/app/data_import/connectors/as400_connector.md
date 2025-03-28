# Module: app.data_import.connectors.as400_connector

**Path:** `app/data_import/connectors/as400_connector.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import os
from typing import Any, Dict, List, Optional, Set
import pyodbc
from pydantic import BaseModel, Field, SecretStr, validator
from cryptography.fernet import Fernet
from app.core.exceptions import DatabaseException, SecurityException
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.connectors.as400_connector")
```

## Classes

| Class | Description |
| --- | --- |
| `AS400ConnectionConfig` |  |
| `AS400Connector` |  |
| `Config` |  |

### Class: `AS400ConnectionConfig`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_allowed_lists` |  |
| `validate_port` |  |

##### `validate_allowed_lists`
```python
@validator('allowed_tables', 'allowed_schemas')
def validate_allowed_lists(cls, v) -> Optional[List[str]]:
```

##### `validate_port`
```python
@validator('port')
def validate_port(cls, v) -> Optional[int]:
```

### Class: `AS400Connector`

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

### Class: `Config`

#### Attributes

| Name | Value |
| --- | --- |
| `validate_assignment` | `True` |
| `extra` | `'forbid'` |
