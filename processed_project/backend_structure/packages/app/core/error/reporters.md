# Module: app.core.error.reporters

**Path:** `app/core/error/reporters.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Optional
from app.core.logging import get_logger
from app.core.error.base import ErrorContext, ErrorReporter
```

## Global Variables
```python
logger = logger = get_logger("app.core.error.reporters")
```

## Classes

| Class | Description |
| --- | --- |
| `DatabaseErrorReporter` |  |
| `ExternalServiceReporter` |  |
| `LoggingErrorReporter` |  |

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
