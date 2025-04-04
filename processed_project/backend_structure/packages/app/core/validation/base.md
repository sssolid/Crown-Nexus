# Module: app.core.validation.base

**Path:** `app/core/validation/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union, runtime_checkable
from pydantic import BaseModel, Field
```

## Global Variables
```python
T = T = TypeVar("T")
R = R = TypeVar("R", bound=bool)
```

## Classes

| Class | Description |
| --- | --- |
| `ValidationResult` |  |
| `Validator` |  |
| `ValidatorFactory` |  |

### Class: `ValidationResult`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `add_error` |  |
| `error_messages` `@property` |  |
| `has_errors` `@property` |  |

##### `add_error`
```python
def add_error(self, msg, error_type, loc, **context) -> None:
```

##### `error_messages`
```python
@property
def error_messages(self) -> List[str]:
```

##### `has_errors`
```python
@property
def has_errors(self) -> bool:
```

### Class: `Validator`
**Inherits from:** Protocol
**Decorators:**
- `@runtime_checkable`

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |
| `validate_async` `async` |  |

##### `validate`
```python
def validate(self, value, **kwargs) -> ValidationResult:
```

##### `validate_async`
```python
async def validate_async(self, value, **kwargs) -> ValidationResult:
```

### Class: `ValidatorFactory`
**Inherits from:** Protocol
**Decorators:**
- `@runtime_checkable`

#### Methods

| Method | Description |
| --- | --- |
| `create_validator` |  |

##### `create_validator`
```python
def create_validator(self, validator_type, **options) -> Validator:
```
