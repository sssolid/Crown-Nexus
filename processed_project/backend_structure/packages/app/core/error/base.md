# Module: app.core.error.base

**Path:** `app/core/error/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Protocol, TypeVar
from pydantic import BaseModel
```

## Global Variables
```python
F = F = TypeVar("F")  # Function type
T = T = TypeVar("T")  # Generic type
```

## Classes

| Class | Description |
| --- | --- |
| `ErrorContext` |  |
| `ErrorReporter` |  |

### Class: `ErrorContext`
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
