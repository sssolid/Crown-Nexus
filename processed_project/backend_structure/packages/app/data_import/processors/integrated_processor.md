# Module: app.data_import.processors.integrated_processor

**Path:** `app/data_import/processors/integrated_processor.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Set, cast
from app.domains.products.schemas import ProductCreate, ProductDescriptionCreate, ProductMarketingCreate, ProductPricingImport
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS, COMPLEX_FIELD_MAPPINGS, ExternalFieldInfo
from app.data_import.processors.generic_processor import GenericProcessor
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.processors.integrated_processor")
```

## Classes

| Class | Description |
| --- | --- |
| `IntegratedProductProcessor` |  |

### Class: `IntegratedProductProcessor`
**Inherits from:** GenericProcessor[ProductCreate]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `process_pricing` `async` |  |
| `validate_pricing` `async` |  |

##### `__init__`
```python
def __init__(self, source_type) -> None:
```

##### `process_pricing`
```python
async def process_pricing(self, data) -> List[Dict[(str, Any)]]:
```

##### `validate_pricing`
```python
async def validate_pricing(self, data) -> List[ProductPricingImport]:
```
