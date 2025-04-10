# Module: app.domains.autocare.pcdb.models

**Path:** `app/domains/autocare/pcdb/models.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Table, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
```

## Global Variables
```python
parts_to_alias = parts_to_alias = Table(
    "parts_to_alias",
    Base.metadata,
    Column(
        "part_terminology_id",
        Integer,
        ForeignKey("pcdb.parts.part_terminology_id"),
        primary_key=True,
    ),
    Column(
        "alias_id",
        Integer,
        ForeignKey("pcdb.alias.alias_id"),
        primary_key=True,
    ),
    schema="pcdb",
)
parts_to_use = parts_to_use = Table(
    "parts_to_use",
    Base.metadata,
    Column(
        "part_terminology_id",
        Integer,
        ForeignKey("pcdb.parts.part_terminology_id"),
        primary_key=True,
    ),
    Column(
        "use_id",
        Integer,
        ForeignKey("pcdb.use.use_id"),
        primary_key=True,
    ),
    schema="pcdb",
)
```

## Classes

| Class | Description |
| --- | --- |
| `Alias` |  |
| `Category` |  |
| `CodeMaster` |  |
| `PCdbVersion` |  |
| `PartCategory` |  |
| `PartPosition` |  |
| `Parts` |  |
| `PartsDescription` |  |
| `PartsSupersession` |  |
| `Position` |  |
| `SubCategory` |  |
| `Use` |  |

### Class: `Alias`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'alias'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Category`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'category'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `CodeMaster`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'code_master'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PCdbVersion`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'pcdb_version'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PartCategory`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'part_category'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PartPosition`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'part_position'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Parts`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'parts'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PartsDescription`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'parts_description'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PartsSupersession`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'parts_supersession'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Position`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'position'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `SubCategory`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'subcategory'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Use`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'use'` |
| `__table_args__` | `    __table_args__ = {"schema": "pcdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
