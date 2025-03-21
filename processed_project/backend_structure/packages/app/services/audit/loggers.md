# Module: app.services.audit.loggers

**Path:** `app/services/audit/loggers.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import json
import uuid
import datetime
from typing import Any, Dict, List, Optional, Union, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import get_logger
from app.services.audit.base import AuditContext, AuditEventType, AuditLogLevel, AuditLogger, AuditOptions
```

## Global Variables
```python
logger = logger = get_logger("app.services.audit.loggers")
```

## Classes

| Class | Description |
| --- | --- |
| `BaseAuditLogger` |  |
| `DatabaseAuditLogger` |  |
| `FileAuditLogger` |  |
| `LoggingAuditLogger` |  |

### Class: `BaseAuditLogger`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

### Class: `DatabaseAuditLogger`
**Inherits from:** BaseAuditLogger, AuditLogger

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `log_event` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `log_event`
```python
async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, context, level, options) -> str:
```

### Class: `FileAuditLogger`
**Inherits from:** BaseAuditLogger, AuditLogger

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `log_event` `async` |  |

##### `__init__`
```python
def __init__(self, file_path) -> None:
```

##### `log_event`
```python
async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, context, level, options) -> str:
```

### Class: `LoggingAuditLogger`
**Inherits from:** BaseAuditLogger, AuditLogger

#### Methods

| Method | Description |
| --- | --- |
| `log_event` `async` |  |

##### `log_event`
```python
async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, context, level, options) -> str:
```
