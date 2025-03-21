# Module: app.schemas.address

**Path:** `app/schemas/address.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.country import Country
```

## Classes

| Class | Description |
| --- | --- |
| `Address` |  |
| `AddressBase` |  |
| `AddressCreate` |  |
| `AddressInDB` |  |
| `AddressUpdate` |  |

### Class: `Address`
**Inherits from:** AddressInDB

### Class: `AddressBase`
**Inherits from:** BaseModel

### Class: `AddressCreate`
**Inherits from:** AddressBase

### Class: `AddressInDB`
**Inherits from:** AddressBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `AddressUpdate`
**Inherits from:** BaseModel
