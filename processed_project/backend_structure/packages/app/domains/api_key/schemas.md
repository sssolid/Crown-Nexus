# Module: app.domains.api_key.schemas

**Path:** `app/domains/api_key/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

## Classes

| Class | Description |
| --- | --- |
| `ApiKey` |  |
| `ApiKeyBase` |  |
| `ApiKeyCreate` |  |
| `ApiKeyInDB` |  |
| `ApiKeyRevokeResponse` |  |
| `ApiKeyUpdate` |  |
| `ApiKeyWithSecret` |  |

### Class: `ApiKey`
**Inherits from:** ApiKeyInDB

### Class: `ApiKeyBase`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `normalize_name` |  |

##### `normalize_name`
```python
@field_validator('name')
@classmethod
def normalize_name(cls, v) -> str:
```

### Class: `ApiKeyCreate`
**Inherits from:** ApiKeyBase

### Class: `ApiKeyInDB`
**Inherits from:** ApiKeyBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ApiKeyRevokeResponse`
**Inherits from:** BaseModel

### Class: `ApiKeyUpdate`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `normalize_name` |  |

##### `normalize_name`
```python
@field_validator('name')
@classmethod
def normalize_name(cls, v) -> Optional[str]:
```

### Class: `ApiKeyWithSecret`
**Inherits from:** ApiKey
