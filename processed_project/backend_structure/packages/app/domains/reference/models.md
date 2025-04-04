# Module: app.domains.reference.models

**Path:** `app/domains/reference/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.products.models import ProductStock
from app.domains.location.models import Address
```

## Classes

| Class | Description |
| --- | --- |
| `Color` |  |
| `ConstructionType` |  |
| `Hardware` |  |
| `PackagingType` |  |
| `TariffCode` |  |
| `Texture` |  |
| `UnspscCode` |  |
| `Warehouse` |  |

### Class: `Color`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'color'` |
| `__table_args__` | `    __table_args__ = {"schema": "reference"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ConstructionType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'construction_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "reference"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Hardware`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'hardware_item'` |
| `__table_args__` | `    __table_args__ = {"schema": "reference"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PackagingType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'packaging_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "reference"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `TariffCode`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'tariff_code'` |
| `__table_args__` | `    __table_args__ = {"schema": "reference"}` |
| `country` | `    country = relationship("Country", back_populates="tariff_codes")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Texture`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'texture'` |
| `__table_args__` | `    __table_args__ = {"schema": "reference"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `UnspscCode`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'unspsc_code'` |
| `__table_args__` | `    __table_args__ = {"schema": "reference"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Warehouse`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'warehouse'` |
| `__table_args__` | `    __table_args__ = {"schema": "reference"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
