# Module: app.data_import.processors.pricing_processor

**Path:** `app/data_import/processors/pricing_processor.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List
from app.logging import get_logger
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS
from app.data_import.processors.generic_processor import GenericProcessor
from app.data_import.schemas.pricing import ProductPricingImport
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.processors.pricing_processor")
```

## Classes

| Class | Description |
| --- | --- |
| `PricingProcessor` |  |

### Class: `PricingProcessor`
**Inherits from:** GenericProcessor[ProductPricingImport]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `process` `async` |  |

##### `__init__`
```python
def __init__(self, source_type) -> None:
```

##### `process`
```python
async def process(self, data) -> List[Dict[(str, Any)]]:
```
