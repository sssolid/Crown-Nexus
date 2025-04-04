# Module: app.domains.currency.models

**Path:** `app/domains/currency/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
```

## Classes

| Class | Description |
| --- | --- |
| `Currency` |  |
| `ExchangeRate` |  |

### Class: `Currency`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'currency'` |
| `__table_args__` | `    __table_args__ = {"schema": "currency"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ExchangeRate`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'exchange_rate'` |
| `__table_args__` | `    __table_args__ = (
        UniqueConstraint(
            "source_currency_id",
            "target_currency_id",
            "effective_date",
            name="uix_exchange_rate_source_target_date",
        ),
        {"schema": "currency"},
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
