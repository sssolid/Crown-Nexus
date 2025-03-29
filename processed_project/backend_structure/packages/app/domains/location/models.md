# Module: app.domains.location.models

**Path:** `app/domains/location/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.domains.reference.models import Warehouse, TariffCode
from app.domains.products.models import Manufacturer
from app.domains.company.schemas import Company
```

## Classes

| Class | Description |
| --- | --- |
| `Address` |  |
| `Country` |  |

### Class: `Address`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'address'` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Country`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'country'` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
