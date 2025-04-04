# Module: app.domains.autocare.padb.models

**Path:** `app/domains/autocare/padb/models.py`

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
| `MeasurementGroup` |  |
| `MetaData` |  |
| `MetaUOMCode` |  |
| `MetaUomCodeAssignment` |  |
| `PAdbVersion` |  |
| `PartAttribute` |  |
| `PartAttributeAssignment` |  |
| `PartAttributeStyle` |  |
| `PartTypeStyle` |  |
| `Style` |  |
| `ValidValue` |  |
| `ValidValueAssignment` |  |

### Class: `MeasurementGroup`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'measurement_group'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `uom_codes` | `    uom_codes = relationship("MetaUOMCode", back_populates="measurement_group")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `MetaData`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'metadata'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `assignments` | `    assignments = relationship("PartAttributeAssignment", back_populates="metadata_info")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `MetaUOMCode`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'meta_uom_code'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `measurement_group` | `    measurement_group = relationship("MeasurementGroup", back_populates="uom_codes")` |
| `assignments` | `    assignments = relationship("MetaUomCodeAssignment", back_populates="meta_uom")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `MetaUomCodeAssignment`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'meta_uom_code_assignment'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `attribute_assignment` | `    attribute_assignment = relationship(
        "PartAttributeAssignment", back_populates="uom_assignments"
    )` |
| `meta_uom` | `    meta_uom = relationship("MetaUOMCode", back_populates="assignments")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PAdbVersion`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'padb_version'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PartAttribute`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'part_attribute'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `assignments` | `    assignments = relationship("PartAttributeAssignment", back_populates="attribute")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PartAttributeAssignment`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'part_attribute_assignment'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `part` | `    part = relationship("Parts", foreign_keys=[part_terminology_id])` |
| `attribute` | `    attribute = relationship("PartAttribute", back_populates="assignments")` |
| `metadata_info` | `    metadata_info = relationship("MetaData", back_populates="assignments")` |
| `uom_assignments` | `    uom_assignments = relationship(
        "MetaUomCodeAssignment", back_populates="attribute_assignment"
    )` |
| `valid_value_assignments` | `    valid_value_assignments = relationship(
        "ValidValueAssignment", back_populates="attribute_assignment"
    )` |
| `style` | `    style = relationship("PartAttributeStyle", back_populates="attribute_assignment")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PartAttributeStyle`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'part_attribute_style'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `style` | `    style = relationship("Style", back_populates="part_attribute_styles")` |
| `attribute_assignment` | `    attribute_assignment = relationship(
        "PartAttributeAssignment", back_populates="style"
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `PartTypeStyle`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'part_type_style'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `style` | `    style = relationship("Style", back_populates="part_type_styles")` |
| `part` | `    part = relationship("Parts", foreign_keys=[part_terminology_id])` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `Style`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'style'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `part_attribute_styles` | `    part_attribute_styles = relationship("PartAttributeStyle", back_populates="style")` |
| `part_type_styles` | `    part_type_styles = relationship("PartTypeStyle", back_populates="style")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ValidValue`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'valid_value'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `assignments` | `    assignments = relationship("ValidValueAssignment", back_populates="valid_value")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ValidValueAssignment`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'valid_value_assignment'` |
| `__table_args__` | `    __table_args__ = {"schema": "padb"}` |
| `attribute_assignment` | `    attribute_assignment = relationship(
        "PartAttributeAssignment", back_populates="valid_value_assignments"
    )` |
| `valid_value` | `    valid_value = relationship("ValidValue", back_populates="assignments")` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
