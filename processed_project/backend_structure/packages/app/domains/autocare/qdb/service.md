# Module: app.domains.autocare.qdb.service

**Path:** `app/domains/autocare/qdb/service.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import QdbException
from app.domains.autocare.qdb.repository import QdbRepository
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.qdb.service")
```

## Classes

| Class | Description |
| --- | --- |
| `QdbService` |  |

### Class: `QdbService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_languages` `async` |  |
| `get_qualifier_details` `async` |  |
| `get_qualifier_types` `async` |  |
| `get_stats` `async` |  |
| `get_version` `async` |  |
| `search_qualifiers` `async` |  |
| `update_database` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_languages`
```python
async def get_languages(self) -> List[Dict[(str, Any)]]:
```

##### `get_qualifier_details`
```python
async def get_qualifier_details(self, qualifier_id) -> Dict[(str, Any)]:
```

##### `get_qualifier_types`
```python
async def get_qualifier_types(self) -> List[Dict[(str, Any)]]:
```

##### `get_stats`
```python
async def get_stats(self) -> Dict[(str, Any)]:
```

##### `get_version`
```python
async def get_version(self) -> str:
```

##### `search_qualifiers`
```python
async def search_qualifiers(self, search_term, qualifier_type_id, language_id, page, page_size) -> Dict[(str, Any)]:
```

##### `update_database`
```python
async def update_database(self, file_path) -> Dict[(str, Any)]:
```
