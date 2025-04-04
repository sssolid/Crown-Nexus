# Module: app.domains.autocare.qdb.schemas

**Path:** `app/domains/autocare/qdb/schemas.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
```

## Classes

| Class | Description |
| --- | --- |
| `GroupNumber` |  |
| `Language` |  |
| `Qualifier` |  |
| `QualifierDetail` |  |
| `QualifierGroup` |  |
| `QualifierSearchParameters` |  |
| `QualifierSearchResponse` |  |
| `QualifierTranslation` |  |
| `QualifierType` |  |

### Class: `GroupNumber`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Language`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Qualifier`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `QualifierDetail`
**Inherits from:** Qualifier

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `QualifierGroup`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `QualifierSearchParameters`
**Inherits from:** BaseModel

### Class: `QualifierSearchResponse`
**Inherits from:** BaseModel

### Class: `QualifierTranslation`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `QualifierType`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |
