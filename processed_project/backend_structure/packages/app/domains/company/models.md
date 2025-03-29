# Module: app.domains.company.models

**Path:** `app/domains/company/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.chat.models import ChatRoom
from app.domains.audit.models import AuditLog
from app.domains.location.models import Address
from app.domains.users.models import User
from app.domains.audit.models import AuditLog
from app.domains.products.models import Brand
```

## Classes

| Class | Description |
| --- | --- |
| `Company` |  |

### Class: `Company`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'company'` |
| `headquarters_address` | `    headquarters_address = relationship(
        "Address", foreign_keys=[headquarters_address_id]
    )` |
| `billing_address` | `    billing_address = relationship("Address", foreign_keys=[billing_address_id])` |
| `shipping_address` | `    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
