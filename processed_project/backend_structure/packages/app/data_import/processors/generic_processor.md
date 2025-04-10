# Module: app.data_import.processors.generic_processor

**Path:** `app/data_import/processors/generic_processor.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Set, Type, TypeVar, cast
from pydantic import BaseModel, ValidationError
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.data_import.field_definitions import EntityFieldDefinitions, FieldDefinition, TransformationDirection, COMPLEX_FIELD_MAPPINGS, ExternalFieldInfo
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.processors.generic_processor")
T = T = TypeVar("T", bound=BaseModel)
```

## Classes

| Class | Description |
| --- | --- |
| `GenericProcessor` |  |

### Class: `GenericProcessor`
**Inherits from:** Generic[T]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `process` `async` |  |
| `validate` `async` |  |

##### `__init__`
```python
def __init__(self, field_definitions, model_type, source_type) -> None:
```

##### `process`
```python
async def process(self, data) -> List[Dict[(str, Any)]]:
```

##### `validate`
```python
async def validate(self, data) -> List[T]:
```
