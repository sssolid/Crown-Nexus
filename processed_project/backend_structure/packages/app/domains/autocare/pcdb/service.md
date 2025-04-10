# Module: app.domains.autocare.pcdb.service

**Path:** `app/domains/autocare/pcdb/service.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging import get_logger
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import PCdbException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.pcdb.repository import PCdbRepository
```

## Global Variables
```python
logger = logger = get_logger("app.domains.autocare.pcdb.service")
```

## Classes

| Class | Description |
| --- | --- |
| `PCdbService` |  |

### Class: `PCdbService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_categories` `async` |  |
| `get_part_details` `async` |  |
| `get_stats` `async` |  |
| `get_subcategories_by_category` `async` |  |
| `get_version` `async` |  |
| `import_from_pies` `async` |  |
| `search_parts` `async` |  |
| `update_database` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_categories`
```python
async def get_categories(self) -> List[Dict[(str, Any)]]:
```

##### `get_part_details`
```python
async def get_part_details(self, part_terminology_id) -> Dict[(str, Any)]:
```

##### `get_stats`
```python
async def get_stats(self) -> Dict[(str, Any)]:
```

##### `get_subcategories_by_category`
```python
async def get_subcategories_by_category(self, category_id) -> List[Dict[(str, Any)]]:
```

##### `get_version`
```python
async def get_version(self) -> str:
```

##### `import_from_pies`
```python
async def import_from_pies(self, file_path, params) -> Dict[(str, Any)]:
```

##### `search_parts`
```python
async def search_parts(self, search_term, categories, subcategories, positions, page, page_size) -> Dict[(str, Any)]:
```

##### `update_database`
```python
async def update_database(self, file_path) -> Dict[(str, Any)]:
```
