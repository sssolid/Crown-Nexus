# Module: app.data_import.processors.base

**Path:** `app/data_import/processors/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Protocol, TypeVar
```

## Global Variables
```python
T = T = TypeVar("T")
```

## Classes

| Class | Description |
| --- | --- |
| `Processor` |  |

### Class: `Processor`
**Inherits from:** Protocol[T]

#### Methods

| Method | Description |
| --- | --- |
| `process` `async` |  |
| `validate` `async` |  |

##### `process`
```python
async def process(self, data) -> List[Dict[(str, Any)]]:
```

##### `validate`
```python
async def validate(self, data) -> List[T]:
```
