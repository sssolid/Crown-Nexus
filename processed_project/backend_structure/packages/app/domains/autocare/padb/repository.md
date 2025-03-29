# Module: app.domains.autocare.padb.repository

**Path:** `app/domains/autocare/padb/repository.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.padb.models import PartAttribute, MetaData, MetaUOMCode, PartAttributeAssignment, MetaUomCodeAssignment, ValidValue, ValidValueAssignment, PAdbVersion
```

## Classes

| Class | Description |
| --- | --- |
| `MetaDataRepository` |  |
| `MetaUOMCodeRepository` |  |
| `PAdbRepository` |  |
| `PartAttributeRepository` |  |
| `ValidValueRepository` |  |

### Class: `MetaDataRepository`
**Inherits from:** BaseRepository[(MetaData, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_meta_id` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_meta_id`
```python
async def get_by_meta_id(self, meta_id) -> Optional[MetaData]:
```

### Class: `MetaUOMCodeRepository`
**Inherits from:** BaseRepository[(MetaUOMCode, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_meta_uom_id` `async` |  |
| `get_for_attribute_assignment` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_meta_uom_id`
```python
async def get_by_meta_uom_id(self, meta_uom_id) -> Optional[MetaUOMCode]:
```

##### `get_for_attribute_assignment`
```python
async def get_for_attribute_assignment(self, papt_id) -> List[MetaUOMCode]:
```

### Class: `PAdbRepository`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_attributes_for_part` `async` |  |
| `get_version` `async` |  |
| `update_version` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_attributes_for_part`
```python
async def get_attributes_for_part(self, part_terminology_id) -> List[Dict[(str, Any)]]:
```

##### `get_version`
```python
async def get_version(self) -> Optional[str]:
```

##### `update_version`
```python
async def update_version(self, version_date) -> PAdbVersion:
```

### Class: `PartAttributeRepository`
**Inherits from:** BaseRepository[(PartAttribute, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_pa_id` `async` |  |
| `search` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_pa_id`
```python
async def get_by_pa_id(self, pa_id) -> Optional[PartAttribute]:
```

##### `search`
```python
async def search(self, search_term, page, page_size) -> Dict[(str, Any)]:
```

### Class: `ValidValueRepository`
**Inherits from:** BaseRepository[(ValidValue, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `get_by_valid_value_id` `async` |  |
| `get_for_attribute_assignment` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `get_by_valid_value_id`
```python
async def get_by_valid_value_id(self, valid_value_id) -> Optional[ValidValue]:
```

##### `get_for_attribute_assignment`
```python
async def get_for_attribute_assignment(self, papt_id) -> List[ValidValue]:
```
