# Module: app.core.audit.backends.file

**Path:** `app/core/audit/backends/file.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from app.core.audit.base import AuditBackend, AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.exceptions import AuditBackendException
from app.core.audit.utils import anonymize_data
from app.core.base import InitializableComponent
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.audit.backends.file")
```

## Classes

| Class | Description |
| --- | --- |
| `FileAuditBackend` |  |

### Class: `FileAuditBackend`
**Inherits from:** AuditBackend, InitializableComponent

#### Attributes

| Name | Value |
| --- | --- |
| `__backend_name__` | `'file'` |

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
def __init__(self, file_path) -> None:
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
