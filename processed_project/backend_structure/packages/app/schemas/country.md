# Module: app.schemas.country

**Path:** `app/schemas/country.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

## Classes

| Class | Description |
| --- | --- |
| `Country` |  |
| `CountryBase` |  |
| `CountryCreate` |  |
| `CountryInDB` |  |
| `CountryUpdate` |  |

### Class: `Country`
**Inherits from:** CountryInDB

### Class: `CountryBase`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `uppercase_codes` |  |

##### `uppercase_codes`
```python
@field_validator('iso_alpha_2', 'iso_alpha_3', mode='before')
@classmethod
def uppercase_codes(cls, v) -> str:
```

### Class: `CountryCreate`
**Inherits from:** CountryBase

### Class: `CountryInDB`
**Inherits from:** CountryBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `CountryUpdate`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `uppercase_codes` |  |

##### `uppercase_codes`
```python
@field_validator('iso_alpha_2', 'iso_alpha_3', 'currency', mode='before')
@classmethod
def uppercase_codes(cls, v) -> Optional[str]:
```
