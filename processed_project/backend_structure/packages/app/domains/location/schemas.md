# Module: app.domains.location.schemas

**Path:** `app/domains/location/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

## Classes

| Class | Description |
| --- | --- |
| `Address` |  |
| `AddressBase` |  |
| `AddressCreate` |  |
| `AddressInDB` |  |
| `AddressUpdate` |  |
| `Country` |  |
| `CountryBase` |  |
| `CountryCreate` |  |
| `CountryInDB` |  |
| `CountryUpdate` |  |
| `GeocodeRequest` |  |
| `GeocodeResult` |  |

### Class: `Address`
**Inherits from:** AddressInDB

### Class: `AddressBase`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_latitude` |  |
| `validate_longitude` |  |

##### `validate_latitude`
```python
@field_validator('latitude')
@classmethod
def validate_latitude(cls, v) -> Optional[float]:
```

##### `validate_longitude`
```python
@field_validator('longitude')
@classmethod
def validate_longitude(cls, v) -> Optional[float]:
```

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

#### Methods

| Method | Description |
| --- | --- |
| `validate_latitude` |  |
| `validate_longitude` |  |

##### `validate_latitude`
```python
@field_validator('latitude')
@classmethod
def validate_latitude(cls, v) -> Optional[float]:
```

##### `validate_longitude`
```python
@field_validator('longitude')
@classmethod
def validate_longitude(cls, v) -> Optional[float]:
```

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
@field_validator('iso_alpha_2', 'iso_alpha_3', 'currency', mode='before')
@classmethod
def uppercase_codes(cls, v) -> Optional[str]:
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

### Class: `GeocodeRequest`
**Inherits from:** BaseModel

### Class: `GeocodeResult`
**Inherits from:** BaseModel
