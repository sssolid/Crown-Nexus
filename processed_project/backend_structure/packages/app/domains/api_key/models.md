# Module: app.domains.api_key.models

**Path:** `app/domains/api_key/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, String, JSON, ForeignKey, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.domains.users.models import User
```

## Classes

| Class | Description |
| --- | --- |
| `ApiKey` |  |

### Class: `ApiKey`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'api_key'` |
| `__table_args__` | `    __table_args__ = (
        Index("ix_api_keys_user_id_name", user_id, name, unique=True),
        {"schema": "api_key"},
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
def to_dict(self, include_secret) -> Dict[(str, Any)]:
```
