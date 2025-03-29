# Module: app.core.validation.manager

**Path:** `app/core/validation/manager.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from datetime import date, datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union, cast
from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.error import resource_not_found, validation_error
from app.core.exceptions import BusinessException, ErrorCode, ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.db import UniqueValidator
from app.core.validation.factory import ValidatorFactory
```

## Global Variables
```python
logger = logger = get_logger("app.core.validation.manager")
```

## Functions

| Function | Description |
| --- | --- |
| `create_validator` |  |
| `initialize` |  |
| `register_validator` |  |
| `shutdown` |  |
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
| `validate_unique` |  |
| `validate_url` |  |
| `validate_uuid` |  |

### `create_validator`
```python
def create_validator(rule_type, **params) -> Callable[([Any], bool)]:
```

### `initialize`
```python
async def initialize() -> None:
```

### `register_validator`
```python
def register_validator(name, validator_class) -> None:
```

### `shutdown`
```python
async def shutdown() -> None:
```

### `validate_composite`
```python
def validate_composite(data, rules) -> Tuple[(bool, List[Dict[(str, Any)]])]:
```

### `validate_credit_card`
```python
def validate_credit_card(card_number) -> bool:
```

### `validate_data`
```python
def validate_data(data, schema_class) -> BaseModel:
```

### `validate_date`
```python
def validate_date(value, min_date, max_date, format_str) -> bool:
```

### `validate_email`
```python
def validate_email(email) -> bool:
```

### `validate_enum`
```python
def validate_enum(value, enum_class) -> bool:
```

### `validate_ip_address`
```python
def validate_ip_address(ip, version) -> bool:
```

### `validate_length`
```python
def validate_length(value, min_length, max_length) -> bool:
```

### `validate_model`
```python
def validate_model(model, include, exclude) -> None:
```

### `validate_password_strength`
```python
def validate_password_strength(password, min_length, require_lowercase, require_uppercase, require_digit, require_special) -> bool:
```

### `validate_phone`
```python
def validate_phone(phone) -> bool:
```

### `validate_range`
```python
def validate_range(value, min_value, max_value) -> bool:
```

### `validate_regex`
```python
def validate_regex(value, pattern) -> bool:
```

### `validate_required`
```python
def validate_required(value) -> bool:
```

### `validate_unique`
```python
async def validate_unique(field, value, model, db, exclude_id) -> bool:
```

### `validate_url`
```python
def validate_url(url) -> bool:
```

### `validate_uuid`
```python
def validate_uuid(value) -> bool:
```
