# Module: app.core.audit.models

**Path:** `app/core/audit/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, String, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.domains.users.models import User
from app.domains.company.models import Company
```

## Classes

| Class | Description |
| --- | --- |
| `AuditLog` |  |

### Class: `AuditLog`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'audit_log'` |
| `__table_args__` | `    __table_args__ = (
        Index("ix_audit_log_timestamp_desc", timestamp.desc()),
        Index("ix_audit_log_user_id_timestamp", user_id, timestamp.desc()),
        Index(
            "ix_audit_log_resource_timestamp",
            resource_type,
            resource_id,
            timestamp.desc(),
        ),
        Index("ix_audit_log_event_type_timestamp", event_type, timestamp.desc()),
        {"schema": "audit"},
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |
| `to_dict` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

##### `to_dict`
```python
def to_dict(self) -> Dict[(str, Any)]:
```
