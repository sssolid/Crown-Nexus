# Module: app.core.validation.factory

**Path:** `app/core/validation/factory.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Type
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.core.validation.base import Validator
from app.core.validation.validators import CreditCardValidator, DateValidator, EmailValidator, EnumValidator, IPAddressValidator, LengthValidator, PasswordValidator, PhoneValidator, RangeValidator, RegexValidator, RequiredValidator, URLValidator, UUIDValidator
```

## Global Variables
```python
logger = logger = get_logger("app.core.validation.factory")
```

## Classes

| Class | Description |
| --- | --- |
| `ValidatorFactory` |  |

### Class: `ValidatorFactory`

#### Methods

| Method | Description |
| --- | --- |
| `create_validator` |  |
| `get_available_validators` |  |
| `register_validator` |  |

##### `create_validator`
```python
@classmethod
def create_validator(cls, validator_type, **options) -> Validator:
```

##### `get_available_validators`
```python
@classmethod
def get_available_validators(cls) -> List[str]:
```

##### `register_validator`
```python
@classmethod
def register_validator(cls, name, validator_class) -> None:
```
