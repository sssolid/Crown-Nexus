# Module: app.services.audit.factory

**Path:** `app/services/audit/factory.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Dict, List, Optional, Type, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.logging import get_logger
from app.services.audit.base import AuditLogger
from app.services.audit.loggers import DatabaseAuditLogger, FileAuditLogger, LoggingAuditLogger
```

## Global Variables
```python
logger = logger = get_logger("app.services.audit.factory")
```

## Classes

| Class | Description |
| --- | --- |
| `AuditLoggerFactory` |  |

### Class: `AuditLoggerFactory`

#### Methods

| Method | Description |
| --- | --- |
| `create_default_loggers` |  |
| `create_logger` |  |
| `register_logger` |  |

##### `create_default_loggers`
```python
@classmethod
def create_default_loggers(cls, db) -> List[AuditLogger]:
```

##### `create_logger`
```python
@classmethod
def create_logger(cls, logger_type, db, **kwargs) -> AuditLogger:
```

##### `register_logger`
```python
@classmethod
def register_logger(cls, name, logger_class) -> None:
```
