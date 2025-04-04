# Module: app.data_import.connectors.base

**Path:** `app/data_import/connectors/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Protocol, TypeVar, Optional
```

## Global Variables
```python
T = T = TypeVar("T")
```

## Classes

| Class | Description |
| --- | --- |
| `Connector` |  |

### Class: `Connector`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `close` `async` |  |
| `connect` `async` |  |
| `extract` `async` |  |

##### `close`
```python
async def close(self) -> None:
```

##### `connect`
```python
async def connect(self) -> None:
```

##### `extract`
```python
async def extract(self, query, limit, **params) -> List[Dict[(str, Any)]]:
```
