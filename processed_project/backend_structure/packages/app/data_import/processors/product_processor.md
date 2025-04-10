# Module: app.data_import.processors.product_processor

**Path:** `app/data_import/processors/product_processor.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, cast
from app.logging import get_logger
from app.domains.products.schemas import ProductCreate, ProductDescriptionCreate, ProductMarketingCreate
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS, COMPLEX_FIELD_MAPPINGS, ExternalFieldInfo
from app.data_import.processors.generic_processor import GenericProcessor
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.processors.product_processor")
```

## Classes

| Class | Description |
| --- | --- |
| `ProductProcessor` |  |

### Class: `ProductProcessor`
**Inherits from:** GenericProcessor[ProductCreate]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, source_type) -> None:
```
