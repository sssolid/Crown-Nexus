# Module: app.core.validation.service

**Path:** `app/core/validation/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union
from datetime import date, datetime
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.factory import ValidatorFactory
from app.core.validation.manager import validate_composite, validate_credit_card, validate_data, validate_date, validate_email, validate_enum, validate_ip_address, validate_length, validate_model, validate_password_strength, validate_phone, validate_range, validate_regex, validate_required, validate_unique, validate_url, validate_uuid
```

## Global Variables
```python
logger = logger = get_logger("app.core.validation.service")
```

## Functions

| Function | Description |
| --- | --- |
| `get_validation_service` |  |

### `get_validation_service`
```python
def get_validation_service(db) -> ValidationService:
```

## Classes

| Class | Description |
| --- | --- |
| `ValidationService` |  |

### Class: `ValidationService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `create_validator` |  |
| `get_available_validators` |  |
| `initialize` `async` |  |
| `shutdown` `async` |  |
| `validate_composite` |  |
| `validate_credit_card` |  |
| `validate_data` |  |
| `validate_date` |  |
| `validate_email` |  |
| `validate_enum` |  |
| `validate_ip_address` |  |
| `validate_length` |  |
| `validate_model` |  |
| `validate_password_strength` |  |
| `validate_phone` |  |
| `validate_range` |  |
| `validate_regex` |  |
| `validate_required` |  |
| `validate_unique` `async` |  |
| `validate_url` |  |
| `validate_uuid` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `create_validator`
```python
def create_validator(self, validator_type, **options) -> Validator:
```

##### `get_available_validators`
```python
def get_available_validators(self) -> List[str]:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

##### `validate_composite`
```python
def validate_composite(self, data, rules) -> Tuple[(bool, List[Dict[(str, Any)]])]:
```

##### `validate_credit_card`
```python
def validate_credit_card(self, card_number) -> bool:
```

##### `validate_data`
```python
def validate_data(self, data, schema_class) -> BaseModel:
```

##### `validate_date`
```python
def validate_date(self, value, min_date, max_date, format_str) -> bool:
```

##### `validate_email`
```python
def validate_email(self, email) -> bool:
```

##### `validate_enum`
```python
def validate_enum(self, value, enum_class) -> bool:
```

##### `validate_ip_address`
```python
def validate_ip_address(self, ip, version) -> bool:
```

##### `validate_length`
```python
def validate_length(self, value, min_length, max_length) -> bool:
```

##### `validate_model`
```python
def validate_model(self, model, include, exclude) -> None:
```

##### `validate_password_strength`
```python
def validate_password_strength(self, password, min_length, require_lowercase, require_uppercase, require_digit, require_special) -> bool:
```

##### `validate_phone`
```python
def validate_phone(self, phone) -> bool:
```

##### `validate_range`
```python
def validate_range(self, value, min_value, max_value) -> bool:
```

##### `validate_regex`
```python
def validate_regex(self, value, pattern) -> bool:
```

##### `validate_required`
```python
def validate_required(self, value) -> bool:
```

##### `validate_unique`
```python
async def validate_unique(self, field, value, model, exclude_id) -> bool:
```

##### `validate_url`
```python
def validate_url(self, url) -> bool:
```

##### `validate_uuid`
```python
def validate_uuid(self, value) -> bool:
```
