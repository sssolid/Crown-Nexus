# Module: app.domains.audit.service.factory

**Path:** `app/domains/audit/service/factory.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Dict, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.logging import get_logger
from app.domains.audit.service.base import AuditLogger
from app.domains.audit.service.loggers import DatabaseAuditLogger, FileAuditLogger, LoggingAuditLogger
```

## Global Variables
```python
logger = logger = get_logger("app.domains.audit.service.factory")
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
