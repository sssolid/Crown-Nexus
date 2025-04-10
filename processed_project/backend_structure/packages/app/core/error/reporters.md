# Module: app.core.error.reporters

**Path:** `app/core/error/reporters.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import json
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
import httpx
from app.core.error.base import ErrorContext, ErrorReporter, ErrorLogEntry
from app.logging.context import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.error.reporters")
```

## Classes

| Class | Description |
| --- | --- |
| `CompositeErrorReporter` |  |
| `DatabaseErrorReporter` |  |
| `ExternalServiceReporter` |  |
| `LoggingErrorReporter` |  |

### Class: `CompositeErrorReporter`
**Inherits from:** ErrorReporter

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `report_error` `async` |  |

##### `__init__`
```python
def __init__(self, reporters) -> None:
```

##### `report_error`
```python
async def report_error(self, exception, context) -> None:
```

### Class: `DatabaseErrorReporter`
**Inherits from:** ErrorReporter

#### Methods

| Method | Description |
| --- | --- |
| `report_error` `async` |  |

##### `report_error`
```python
async def report_error(self, exception, context) -> None:
```

### Class: `ExternalServiceReporter`
**Inherits from:** ErrorReporter

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `report_error` `async` |  |

##### `__init__`
```python
def __init__(self, service_url, api_key) -> None:
```

##### `report_error`
```python
async def report_error(self, exception, context) -> None:
```

### Class: `LoggingErrorReporter`
**Inherits from:** ErrorReporter

#### Methods

| Method | Description |
| --- | --- |
| `report_error` `async` |  |

##### `report_error`
```python
async def report_error(self, exception, context) -> None:
```
