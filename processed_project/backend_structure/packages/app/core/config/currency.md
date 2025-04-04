# Module: app.core.config.currency

**Path:** `app/core/config/currency.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
```

## Classes

| Class | Description |
| --- | --- |
| `CurrencySettings` |  |

### Class: `CurrencySettings`
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
