# Module: app.core.config.fitment

**Path:** `app/core/config/fitment.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import os
from typing import Optional
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.config.base import Environment
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
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `validate_fitment_paths` |  |

##### `validate_fitment_paths`
```python
@model_validator(mode='after')
def validate_fitment_paths(self) -> 'FitmentSettings':
```
