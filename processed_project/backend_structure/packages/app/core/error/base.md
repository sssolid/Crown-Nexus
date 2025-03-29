# Module: app.core.error.base

**Path:** `app/core/error/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union
from pydantic import BaseModel, Field
from app.logging.context import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.error.base")
F = F = TypeVar("F")
T = T = TypeVar("T")
```

## Classes

| Class | Description |
| --- | --- |
| `Config` |  |
| `ErrorContext` |  |
| `ErrorHandler` |  |
| `ErrorLogEntry` |  |
| `ErrorReporter` |  |

### Class: `Config`

#### Attributes

| Name | Value |
| --- | --- |
| `extra` | `'allow'` |

### Class: `ErrorContext`
**Inherits from:** BaseModel

### Class: `ErrorHandler`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `handle_error` `async` |  |

##### `handle_error`
```python
async def handle_error(self, exception, context) -> Any:
```

### Class: `ErrorLogEntry`
**Inherits from:** BaseModel

### Class: `ErrorReporter`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `report_error` `async` |  |

##### `report_error`
```python
async def report_error(self, exception, context) -> None:
```
