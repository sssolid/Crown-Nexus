# Module: app.data_import.processors.product_processor

**Path:** `app/data_import/processors/product_processor.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, validator
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.domains.products.schemas import ProductCreate
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.processors.product_processor")
```

## Classes

| Class | Description |
| --- | --- |
| `ProductMappingConfig` |  |
| `ProductProcessor` |  |

### Class: `ProductMappingConfig`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_boolean_values` |  |

##### `validate_boolean_values`
```python
@validator('boolean_true_values', 'boolean_false_values')
def validate_boolean_values(cls, v) -> List[str]:
```

### Class: `ProductProcessor`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `process` `async` |  |
| `validate` `async` |  |

##### `__init__`
```python
def __init__(self, config) -> None:
```

##### `process`
```python
async def process(self, data) -> List[Dict[(str, Any)]]:
```

##### `validate`
```python
async def validate(self, data) -> List[ProductCreate]:
```
