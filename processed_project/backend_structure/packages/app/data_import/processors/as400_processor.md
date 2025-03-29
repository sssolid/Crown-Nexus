# Module: app.data_import.processors.as400_processor

**Path:** `app/data_import/processors/as400_processor.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Set, Type, TypeVar, Union
from pydantic import BaseModel
from app.core.exceptions import ValidationException
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.data_import.processors.as400_processor")
T = T = TypeVar("T", bound=BaseModel)
```

## Classes

| Class | Description |
| --- | --- |
| `AS400BaseProcessor` |  |
| `AS400ProcessorConfig` |  |
| `InventoryAS400Processor` |  |
| `PricingAS400Processor` |  |
| `ProductAS400Processor` |  |

### Class: `AS400BaseProcessor`
**Inherits from:** Generic[T], ABC

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `process` `async` |  |
| `validate` `async` |  |

##### `__init__`
```python
def __init__(self, config, destination_model) -> None:
```

##### `process`
```python
async def process(self, data) -> List[Dict[(str, Any)]]:
```

##### `validate`
```python
async def validate(self, data) -> List[T]:
```

### Class: `AS400ProcessorConfig`
**Inherits from:** BaseModel

### Class: `InventoryAS400Processor`
**Inherits from:** AS400BaseProcessor[T]

### Class: `PricingAS400Processor`
**Inherits from:** AS400BaseProcessor[T]

### Class: `ProductAS400Processor`
**Inherits from:** AS400BaseProcessor[T]
