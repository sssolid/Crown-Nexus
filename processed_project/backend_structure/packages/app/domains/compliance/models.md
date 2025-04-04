# Module: app.domains.compliance.models

**Path:** `app/domains/compliance/models.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, Date, DateTime, Enum as SQLAEnum, ForeignKey
from sqlalchemy import Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.products.models import Product
from app.domains.users.models import User
```

## Classes

| Class | Description |
| --- | --- |
| `ApprovalStatus` |  |
| `ChemicalType` |  |
| `ExposureScenario` |  |
| `HazardousMaterial` |  |
| `ProductChemical` |  |
| `ProductDOTApproval` |  |
| `Prop65Chemical` |  |
| `TransportRestriction` |  |
| `Warning` |  |

### Class: `ApprovalStatus`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `APPROVED` | `'Approved'` |
| `PENDING` | `'Pending'` |
| `REVOKED` | `'Revoked'` |
| `NOT_REQUIRED` | `'Not Required'` |

### Class: `ChemicalType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `CARCINOGEN` | `'Carcinogen'` |
| `REPRODUCTIVE_TOXICANT` | `'Reproductive Toxicant'` |
| `BOTH` | `'Both'` |

### Class: `ExposureScenario`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `CONSUMER` | `'Consumer'` |
| `OCCUPATIONAL` | `'Occupational'` |
| `ENVIRONMENTAL` | `'Environmental'` |

### Class: `HazardousMaterial`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'hazardous_material'` |
| `__table_args__` | `    __table_args__ = {"schema": "compliance"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductChemical`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_chemical'` |
| `__table_args__` | `    __table_args__ = {"schema": "compliance"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ProductDOTApproval`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'product_dot_approval'` |
| `__table_args__` | `    __table_args__ = {"schema": "compliance"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Prop65Chemical`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'prop65_chemical'` |
| `__table_args__` | `    __table_args__ = {"schema": "compliance"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `TransportRestriction`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `NONE` | `'NONE'` |
| `AIR` | `'AIR'` |
| `GROUND` | `'GROUND'` |
| `SEA` | `'SEA'` |
| `ALL` | `'ALL'` |

### Class: `Warning`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'warning'` |
| `__table_args__` | `    __table_args__ = {"schema": "compliance"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
