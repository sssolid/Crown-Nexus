# Module: app.core.error.factory

**Path:** `app/core/error/factory.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.core.config import settings
from app.core.logging import get_logger
from app.core.error.base import ErrorReporter
from app.core.error.reporters import DatabaseErrorReporter, ExternalServiceReporter, LoggingErrorReporter
```

## Global Variables
```python
logger = logger = get_logger("app.core.error.factory")
```

## Classes

| Class | Description |
| --- | --- |
| `ErrorReporterFactory` |  |

### Class: `ErrorReporterFactory`

#### Methods

| Method | Description |
| --- | --- |
| `create_default_reporters` |  |
| `create_reporter` |  |

##### `create_default_reporters`
```python
@classmethod
def create_default_reporters(cls) -> List[ErrorReporter]:
```

##### `create_reporter`
```python
@classmethod
def create_reporter(cls, reporter_type, **kwargs) -> ErrorReporter:
```
