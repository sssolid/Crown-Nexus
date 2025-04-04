# Module: app.core.validation.validators

**Path:** `app/core/validation/validators.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import ipaddress
import re
import uuid
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
```

## Global Variables
```python
logger = logger = get_logger("app.core.validation.validators")
```

## Classes

| Class | Description |
| --- | --- |
| `CreditCardValidator` |  |
| `DateValidator` |  |
| `EmailValidator` |  |
| `EnumValidator` |  |
| `IPAddressValidator` |  |
| `LengthValidator` |  |
| `PasswordValidator` |  |
| `PhoneValidator` |  |
| `RangeValidator` |  |
| `RegexValidator` |  |
| `RequiredValidator` |  |
| `URLValidator` |  |
| `UUIDValidator` |  |

### Class: `CreditCardValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `validate` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `validate`
```python
def validate(self, value, **kwargs) -> ValidationResult:
```

### Class: `DateValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, min_date, max_date, format_str, **kwargs) -> ValidationResult:
```

### Class: `EmailValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `validate` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `validate`
```python
def validate(self, value, **kwargs) -> ValidationResult:
```

### Class: `EnumValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, enum_class, **kwargs) -> ValidationResult:
```

### Class: `IPAddressValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, version, **kwargs) -> ValidationResult:
```

### Class: `LengthValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, min_length, max_length, **kwargs) -> ValidationResult:
```

### Class: `PasswordValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, min_length, require_lowercase, require_uppercase, require_digit, require_special, **kwargs) -> ValidationResult:
```

### Class: `PhoneValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `validate` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `validate`
```python
def validate(self, value, **kwargs) -> ValidationResult:
```

### Class: `RangeValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, min_value, max_value, **kwargs) -> ValidationResult:
```

### Class: `RegexValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, pattern, **kwargs) -> ValidationResult:
```

### Class: `RequiredValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, **kwargs) -> ValidationResult:
```

### Class: `URLValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `validate` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `validate`
```python
def validate(self, value, **kwargs) -> ValidationResult:
```

### Class: `UUIDValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, **kwargs) -> ValidationResult:
```
