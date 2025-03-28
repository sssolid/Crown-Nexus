# Module: app.domains.autocare.pcdb.schemas

**Path:** `app/domains/autocare/pcdb/schemas.py`

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
| `Category` |  |
| `Part` |  |
| `PartDetail` |  |
| `PartSearchParameters` |  |
| `PartSearchResponse` |  |
| `Position` |  |
| `SubCategory` |  |

### Class: `Category`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `Part`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `PartDetail`
**Inherits from:** Part

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `PartSearchParameters`
**Inherits from:** BaseModel

### Class: `PartSearchResponse`
**Inherits from:** BaseModel

### Class: `Position`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `SubCategory`
**Inherits from:** BaseModel

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |
