# Module: app.services.search.base

**Path:** `app/services/search/base.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Optional, Protocol, TypeVar
```

## Global Variables
```python
T = T = TypeVar("T")  # Entity type
```

## Classes

| Class | Description |
| --- | --- |
| `SearchProvider` |  |
| `SearchResult` |  |

### Class: `SearchProvider`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `initialize` `async` |  |
| `search` `async` |  |
| `shutdown` `async` |  |

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `search`
```python
async def search(self, search_term, filters, page, page_size, **kwargs) -> Dict[(str, Any)]:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

### Class: `SearchResult`
**Inherits from:** Dict[(str, Any)]
