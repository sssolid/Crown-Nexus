# Module: app.domains.autocare.pcdb.models

**Path:** `app/domains/autocare/pcdb/models.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
```

## Global Variables
```python
parts_to_alias = parts_to_alias = Table(
    "autocare_parts_to_alias",
    Base.metadata,
    mapped_column(
        "part_terminology_id",
        Integer,
        ForeignKey("autocare_parts.part_terminology_id"),
        primary_key=True,
    ),
    mapped_column(
        "alias_id", Integer, ForeignKey("autocare_alias.alias_id"), primary_key=True
    ),
)
parts_to_use = parts_to_use = Table(
    "autocare_parts_to_use",
    Base.metadata,
    mapped_column(
        "part_terminology_id",
        Integer,
        ForeignKey("autocare_parts.part_terminology_id"),
        primary_key=True,
    ),
    mapped_column(
        "use_id", Integer, ForeignKey("autocare_use.use_id"), primary_key=True
    ),
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
| `__tablename__` | `'autocare_alias'` |

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
| `__tablename__` | `'autocare_category'` |
| `part_categories` | `    part_categories = relationship("PartCategory", back_populates="category")` |
| `code_masters` | `    code_masters = relationship("CodeMaster", back_populates="category")` |

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
| `__tablename__` | `'autocare_code_master'` |
| `part` | `    part = relationship("Parts", foreign_keys=[part_terminology_id])` |
| `category` | `    category = relationship("Category", back_populates="code_masters")` |
| `subcategory` | `    subcategory = relationship("SubCategory", back_populates="code_masters")` |
| `position` | `    position = relationship("Position", back_populates="code_masters")` |

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
| `__tablename__` | `'autocare_pcdb_version'` |

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
| `__tablename__` | `'autocare_part_category'` |
| `part` | `    part = relationship("Parts", back_populates="categories")` |
| `subcategory` | `    subcategory = relationship("SubCategory", back_populates="part_categories")` |
| `category` | `    category = relationship("Category", back_populates="part_categories")` |

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
| `__tablename__` | `'autocare_part_position'` |
| `part` | `    part = relationship("Parts", back_populates="positions")` |
| `position` | `    position = relationship("Position", back_populates="part_positions")` |

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
| `__tablename__` | `'autocare_parts'` |
| `description` | `    description = relationship("PartsDescription", back_populates="parts")` |
| `categories` | `    categories = relationship("PartCategory", back_populates="part")` |
| `positions` | `    positions = relationship("PartPosition", back_populates="part")` |
| `attributes` | `    attributes = relationship("PartAttributeAssignment", back_populates="part")` |
| `supersessions` | `    supersessions = relationship(
        "PartsSupersession",
        foreign_keys="[PartsSupersession.new_part_terminology_id]",
        primaryjoin="Parts.part_terminology_id==PartsSupersession.new_part_terminology_id",
        backref="new_part",
    )` |
| `superseded_by` | `    superseded_by = relationship(
        "PartsSupersession",
        foreign_keys="[PartsSupersession.old_part_terminology_id]",
        primaryjoin="Parts.part_terminology_id==PartsSupersession.old_part_terminology_id",
        backref="old_part",
    )` |

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
| `__tablename__` | `'autocare_parts_description'` |
| `parts` | `    parts = relationship("Parts", back_populates="description")` |

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
| `__tablename__` | `'autocare_parts_supersession'` |

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
| `__tablename__` | `'autocare_position'` |
| `part_positions` | `    part_positions = relationship("PartPosition", back_populates="position")` |
| `code_masters` | `    code_masters = relationship("CodeMaster", back_populates="position")` |

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
| `__tablename__` | `'autocare_subcategory'` |
| `part_categories` | `    part_categories = relationship("PartCategory", back_populates="subcategory")` |
| `code_masters` | `    code_masters = relationship("CodeMaster", back_populates="subcategory")` |

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
| `__tablename__` | `'autocare_use'` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
