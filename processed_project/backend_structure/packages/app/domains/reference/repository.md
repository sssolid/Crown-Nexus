# Module: app.domains.reference.repository

**Path:** `app/domains/reference/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.reference.models import Color, TariffCode, UnspscCode, Warehouse
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

## Classes

| Class | Description |
| --- | --- |
| `ColorRepository` |  |
| `TariffCodeRepository` |  |
| `UnspscCodeRepository` |  |
| `WarehouseRepository` |  |

### Class: `ColorRepository`
**Inherits from:** BaseRepository[(Color, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_hex` `async` |  |
| `find_by_name` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, color_id) -> Color:
```

##### `find_by_hex`
```python
async def find_by_hex(self, hex_code) -> Optional[Color]:
```

##### `find_by_name`
```python
async def find_by_name(self, name) -> Optional[Color]:
```

### Class: `TariffCodeRepository`
**Inherits from:** BaseRepository[(TariffCode, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_code` `async` |  |
| `get_by_country` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, tariff_code_id) -> TariffCode:
```

##### `find_by_code`
```python
async def find_by_code(self, code) -> List[TariffCode]:
```

##### `get_by_country`
```python
async def get_by_country(self, country_id) -> List[TariffCode]:
```

### Class: `UnspscCodeRepository`
**Inherits from:** BaseRepository[(UnspscCode, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_code` `async` |  |
| `find_by_description` `async` |  |
| `find_by_segment` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, unspsc_code_id) -> UnspscCode:
```

##### `find_by_code`
```python
async def find_by_code(self, code) -> Optional[UnspscCode]:
```

##### `find_by_description`
```python
async def find_by_description(self, description) -> List[UnspscCode]:
```

##### `find_by_segment`
```python
async def find_by_segment(self, segment) -> List[UnspscCode]:
```

### Class: `WarehouseRepository`
**Inherits from:** BaseRepository[(Warehouse, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_name` `async` |  |
| `get_active_warehouses` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, warehouse_id) -> Warehouse:
```

##### `find_by_name`
```python
async def find_by_name(self, name) -> Optional[Warehouse]:
```

##### `get_active_warehouses`
```python
async def get_active_warehouses(self) -> List[Warehouse]:
```
