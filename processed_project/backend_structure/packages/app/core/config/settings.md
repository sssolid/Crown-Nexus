# Module: app.core.config.settings

**Path:** `app/core/config/settings.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from functools import lru_cache
from typing import Any, Dict
from pydantic import model_validator
from pydantic_settings import SettingsConfigDict
from app.core.config.base import BaseAppSettings
from app.core.config.celery import CelerySettings
from app.core.config.currency import CurrencySettings
from app.core.config.database import DatabaseSettings
from app.core.config.fitment import FitmentSettings
from app.core.config.media import MediaSettings
from app.core.config.security import SecuritySettings
```

## Global Variables
```python
settings = settings = get_settings()
```

## Functions

| Function | Description |
| --- | --- |
| `get_settings` |  |

### `get_settings`
```python
@lru_cache
def get_settings() -> Settings:
```

## Classes

| Class | Description |
| --- | --- |
| `Settings` |  |

### Class: `Settings`
**Inherits from:** BaseAppSettings, DatabaseSettings, SecuritySettings, MediaSettings, FitmentSettings, CurrencySettings, CelerySettings

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
| `as400` `@property` |  |
| `elasticsearch` `@property` |  |
| `filemaker` `@property` |  |
| `model_dump` |  |
| `security` `@property` |  |
| `setup_celery_urls` |  |

##### `as400`
```python
@property
def as400(self) -> 'AS400Settings':
```

##### `elasticsearch`
```python
@property
def elasticsearch(self) -> 'ElasticsearchSettings':
```

##### `filemaker`
```python
@property
def filemaker(self) -> 'FilemakerSettings':
```

##### `model_dump`
```python
def model_dump(self, **kwargs) -> Dict[(str, Any)]:
```

##### `security`
```python
@property
def security(self) -> 'SecuritySettings':
```

##### `setup_celery_urls`
```python
@model_validator(mode='after')
def setup_celery_urls(self) -> 'Settings':
```
