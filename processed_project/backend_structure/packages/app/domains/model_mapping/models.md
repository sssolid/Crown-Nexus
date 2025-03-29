# Module: app.domains.model_mapping.models

**Path:** `app/domains/model_mapping/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
```

## Classes

| Class | Description |
| --- | --- |
| `ModelMapping` |  |

### Class: `ModelMapping`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'model_mapping'` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |
| `make` `@property` |  |
| `model` `@property` |  |
| `vehicle_code` `@property` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

##### `make`
```python
@property
def make(self) -> str:
```

##### `model`
```python
@property
def model(self) -> str:
```

##### `vehicle_code`
```python
@property
def vehicle_code(self) -> str:
```
