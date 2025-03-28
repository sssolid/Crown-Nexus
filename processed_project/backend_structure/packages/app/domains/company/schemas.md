# Module: app.domains.company.schemas

**Path:** `app/domains/company/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.location.schemas import Address
```

## Classes

| Class | Description |
| --- | --- |
| `Company` |  |
| `CompanyBase` |  |
| `CompanyCreate` |  |
| `CompanyInDB` |  |
| `CompanyUpdate` |  |

### Class: `Company`
**Inherits from:** CompanyInDB

### Class: `CompanyBase`
**Inherits from:** BaseModel

### Class: `CompanyCreate`
**Inherits from:** CompanyBase

### Class: `CompanyInDB`
**Inherits from:** CompanyBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `CompanyUpdate`
**Inherits from:** BaseModel
