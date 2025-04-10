# Module: app.core.audit.backends.logging

**Path:** `app/core/audit/backends/logging.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from app.core.audit.base import AuditBackend, AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.utils import anonymize_data
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.audit.backends.logging")
```

## Classes

| Class | Description |
| --- | --- |
| `LoggingAuditBackend` |  |

### Class: `LoggingAuditBackend`
**Inherits from:** AuditBackend

#### Attributes

| Name | Value |
| --- | --- |
| `__backend_name__` | `'logging'` |

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `health_check` `async` |  |
| `initialize` `async` |  |
| `log_event` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `health_check`
```python
async def health_check(self) -> Dict[(str, Any)]:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `log_event`
```python
async def log_event(self, event_type, level, context, details, options) -> str:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
