# Module: app.domains.autocare.pcdb.repository

**Path:** `app/domains/autocare/pcdb/repository.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.pcdb.models import Parts, Category, SubCategory, Position, PartCategory, PartPosition, PartsSupersession, PCdbVersion
```

## Classes

| Class | Description |
| --- | --- |
| `CategoryRepository` |  |
| `PCdbRepository` |  |
| `PartsRepository` |  |
| `PositionRepository` |  |
| `SubCategoryRepository` |  |

### Class: `CategoryRepository`
**Inherits from:** BaseRepository[(Category, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_categories` `async` |  |
| `get_by_category_id` `async` |  |
| `search` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_categories`
```python
async def get_all_categories(self) -> List[Category]:
```

##### `get_by_category_id`
```python
async def get_by_category_id(self, category_id) -> Optional[Category]:
```

##### `search`
```python
async def search(self, search_term) -> List[Category]:
```

### Class: `PCdbRepository`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_version` `async` |  |
| `search_parts` `async` |  |
| `update_version` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_version`
```python
async def get_version(self) -> Optional[str]:
```

##### `search_parts`
```python
async def search_parts(self, search_term, categories, page, page_size) -> Dict[(str, Any)]:
```

##### `update_version`
```python
async def update_version(self, version_date) -> PCdbVersion:
```

### Class: `PartsRepository`
**Inherits from:** BaseRepository[(Parts, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_category` `async` |  |
| `get_by_terminology_id` `async` |  |
| `get_supersessions` `async` |  |
| `search` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_category`
```python
async def get_by_category(self, category_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_by_terminology_id`
```python
async def get_by_terminology_id(self, part_terminology_id) -> Optional[Parts]:
```

##### `get_supersessions`
```python
async def get_supersessions(self, part_terminology_id) -> Dict[(str, List[Parts])]:
```

##### `search`
```python
async def search(self, search_term, categories, page, page_size) -> Dict[(str, Any)]:
```

### Class: `PositionRepository`
**Inherits from:** BaseRepository[(Position, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_all_positions` `async` |  |
| `get_by_part` `async` |  |
| `get_by_position_id` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_all_positions`
```python
async def get_all_positions(self) -> List[Position]:
```

##### `get_by_part`
```python
async def get_by_part(self, part_terminology_id) -> List[Position]:
```

##### `get_by_position_id`
```python
async def get_by_position_id(self, position_id) -> Optional[Position]:
```

### Class: `SubCategoryRepository`
**Inherits from:** BaseRepository[(SubCategory, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_category` `async` |  |
| `get_by_subcategory_id` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_category`
```python
async def get_by_category(self, category_id) -> List[SubCategory]:
```

##### `get_by_subcategory_id`
```python
async def get_by_subcategory_id(self, subcategory_id) -> Optional[SubCategory]:
```
