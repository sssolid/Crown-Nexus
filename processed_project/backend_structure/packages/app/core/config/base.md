# Module: app.core.config.base

**Path:** `app/core/config/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

## Classes

| Class | Description |
| --- | --- |
| `BaseAppSettings` |  |
| `Environment` |  |
| `LogLevel` |  |

### Class: `BaseAppSettings`
**Inherits from:** BaseSettings

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
        json_schema_extra={
            # Disable JSON parsing for these fields
            "AVAILABLE_LOCALES": {"env_mode": "str"},
        },
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `parse_str_to_list` |  |

##### `parse_str_to_list`
```python
@field_validator('AVAILABLE_LOCALES', mode='before')
@classmethod
def parse_str_to_list(cls, v) -> List[str]:
```

### Class: `Environment`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `DEVELOPMENT` | `'development'` |
| `STAGING` | `'staging'` |
| `PRODUCTION` | `'production'` |

### Class: `LogLevel`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `DEBUG` | `'DEBUG'` |
| `INFO` | `'INFO'` |
| `WARNING` | `'WARNING'` |
| `ERROR` | `'ERROR'` |
| `CRITICAL` | `'CRITICAL'` |
