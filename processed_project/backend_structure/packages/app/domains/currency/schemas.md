# Module: app.domains.currency.schemas

**Path:** `app/domains/currency/schemas.py`

[Back to Project Index](../../../../index.md)

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
| `ConversionRequest` |  |
| `ConversionResponse` |  |
| `CurrencyBase` |  |
| `CurrencyCreate` |  |
| `CurrencyRead` |  |
| `CurrencyUpdate` |  |
| `ExchangeRateBase` |  |
| `ExchangeRateCreate` |  |
| `ExchangeRateRead` |  |

### Class: `ConversionRequest`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_currency_code` |  |

##### `validate_currency_code`
```python
@field_validator('source_currency', 'target_currency')
@classmethod
def validate_currency_code(cls, v) -> str:
```

### Class: `ConversionResponse`
**Inherits from:** BaseModel

### Class: `CurrencyBase`
**Inherits from:** BaseModel

### Class: `CurrencyCreate`
**Inherits from:** CurrencyBase

### Class: `CurrencyRead`
**Inherits from:** CurrencyBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `CurrencyUpdate`
**Inherits from:** BaseModel

### Class: `ExchangeRateBase`
**Inherits from:** BaseModel

### Class: `ExchangeRateCreate`
**Inherits from:** ExchangeRateBase

### Class: `ExchangeRateRead`
**Inherits from:** ExchangeRateBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |
