# Module: app.domains.autocare.qdb.models

**Path:** `app/domains/autocare/qdb/models.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
```

## Classes

| Class | Description |
| --- | --- |
| `GroupNumber` |  |
| `Language` |  |
| `QdbVersion` |  |
| `Qualifier` |  |
| `QualifierGroup` |  |
| `QualifierTranslation` |  |
| `QualifierType` |  |

### Class: `GroupNumber`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'group_number'` |
| `__table_args__` | `    __table_args__ = {"schema": "qdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Language`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'language'` |
| `__table_args__` | `    __table_args__ = {"schema": "qdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `QdbVersion`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'qdb_version'` |
| `__table_args__` | `    __table_args__ = {"schema": "qdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Qualifier`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'qualifier'` |
| `__table_args__` | `    __table_args__ = (
        ForeignKeyConstraint(
            ["new_qualifier_id"],
            ["qdb.qualifier.qualifier_id"],
            deferrable=True,
            initially="DEFERRED",
        ),
        {"schema": "qdb"},
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `QualifierGroup`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'qualifier_group'` |
| `__table_args__` | `    __table_args__ = {"schema": "qdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `QualifierTranslation`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'qualifier_translation'` |
| `__table_args__` | `    __table_args__ = {"schema": "qdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `QualifierType`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'qualifier_type'` |
| `__table_args__` | `    __table_args__ = {"schema": "qdb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
