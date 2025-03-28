# Module: app.domains.autocare.fitment.models

**Path:** `app/domains/autocare/fitment/models.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, expression
from app.db.base_class import Base
```

## Classes

| Class | Description |
| --- | --- |
| `FitmentMapping` |  |
| `FitmentMappingHistory` |  |

### Class: `FitmentMapping`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'autocare_fitment_mapping'` |
| `product` | `    product = relationship("Product", foreign_keys=[product_id])` |
| `created_by` | `    created_by = relationship("User", foreign_keys=[created_by_id])` |
| `updated_by` | `    updated_by = relationship("User", foreign_keys=[updated_by_id])` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `FitmentMappingHistory`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'autocare_fitment_mapping_history'` |
| `mapping` | `    mapping = relationship("FitmentMapping", foreign_keys=[mapping_id])` |
| `changed_by` | `    changed_by = relationship("User", foreign_keys=[changed_by_id])` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
