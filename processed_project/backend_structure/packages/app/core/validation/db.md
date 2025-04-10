# Module: app.core.validation.db

**Path:** `app/core/validation/db.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Type, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
```

## Global Variables
```python
logger = logger = get_logger("app.core.validation.db")
```

## Classes

| Class | Description |
| --- | --- |
| `UniqueValidator` |  |

### Class: `UniqueValidator`
**Inherits from:** Validator

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `validate` |  |
| `validate_async` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `validate`
```python
def validate(self, value, field, model, exclude_id, **kwargs) -> ValidationResult:
```

##### `validate_async`
```python
async def validate_async(self, value, field, model, exclude_id, **kwargs) -> ValidationResult:
```
