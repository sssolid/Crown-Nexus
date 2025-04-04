# Module: app.fitment.config

**Path:** `app/fitment/config.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import os
from functools import lru_cache
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

## Functions

| Function | Description |
| --- | --- |
| `get_settings` |  |

### `get_settings`
```python
@lru_cache(maxsize=1)
def get_settings() -> FitmentSettings:
```

## Classes

| Class | Description |
| --- | --- |
| `FitmentSettings` |  |

### Class: `FitmentSettings`
**Inherits from:** BaseSettings

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = SettingsConfigDict(
        env_prefix="FITMENT_", case_sensitive=False, extra="ignore"
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `validate_file_path` |  |
| `validate_optional_file_path` |  |

##### `validate_file_path`
```python
@validator('vcdb_path', 'pcdb_path')
def validate_file_path(self, v) -> str:
```

##### `validate_optional_file_path`
```python
@validator('model_mappings_path')
def validate_optional_file_path(self, v) -> Optional[str]:
```
