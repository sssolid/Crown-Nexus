# Module: app.core.validation.base

**Path:** `app/core/validation/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union
from pydantic import BaseModel
```

## Global Variables
```python
T = T = TypeVar("T")  # Input type
R = R = TypeVar("R", bound=bool)  # Result type (usually bool)
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
| `has_errors` `@property` |  |

##### `has_errors`
```python
@property
def has_errors(self) -> bool:
```

### Class: `Validator`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `validate` |  |

##### `validate`
```python
def validate(self, value, **kwargs) -> ValidationResult:
```

### Class: `ValidatorFactory`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `create_validator` |  |

##### `create_validator`
```python
def create_validator(self, validator_type, **options) -> Validator:
```
