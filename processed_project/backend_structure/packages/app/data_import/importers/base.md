# Module: app.data_import.importers.base

**Path:** `app/data_import/importers/base.py`

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
| `Importer` |  |

### Class: `Importer`
**Inherits from:** Protocol[T]

#### Methods

| Method | Description |
| --- | --- |
| `import_data` `async` |  |

##### `import_data`
```python
async def import_data(self, data) -> Dict[(str, Any)]:
```
