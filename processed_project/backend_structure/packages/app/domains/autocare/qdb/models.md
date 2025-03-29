# Module: app.domains.autocare.qdb.models

**Path:** `app/domains/autocare/qdb/models.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
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
| `__tablename__` | `'autocare_group_number'` |
| `qualifier_groups` | `    qualifier_groups = relationship("QualifierGroup", back_populates="group_number")` |

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
| `__tablename__` | `'autocare_language'` |
| `translations` | `    translations = relationship("QualifierTranslation", back_populates="language")` |

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
| `__tablename__` | `'autocare_qdb_version'` |

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
| `__tablename__` | `'autocare_qualifier'` |
| `qualifier_type` | `    qualifier_type = relationship("QualifierType", back_populates="qualifiers")` |
| `translations` | `    translations = relationship("QualifierTranslation", back_populates="qualifier")` |
| `groups` | `    groups = relationship("QualifierGroup", back_populates="qualifier")` |
| `superseded_by` | `    superseded_by = relationship(
        "Qualifier",
        remote_side=[id],
        foreign_keys=[new_qualifier_id],
        backref="supersedes",
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
| `__tablename__` | `'autocare_qualifier_group'` |
| `group_number` | `    group_number = relationship("GroupNumber", back_populates="qualifier_groups")` |
| `qualifier` | `    qualifier = relationship("Qualifier", back_populates="groups")` |

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
| `__tablename__` | `'autocare_qualifier_translation'` |
| `qualifier` | `    qualifier = relationship("Qualifier", back_populates="translations")` |
| `language` | `    language = relationship("Language", back_populates="translations")` |

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
| `__tablename__` | `'autocare_qualifier_type'` |
| `qualifiers` | `    qualifiers = relationship("Qualifier", back_populates="qualifier_type")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
