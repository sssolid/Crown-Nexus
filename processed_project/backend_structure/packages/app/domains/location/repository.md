# Module: app.domains.location.repository

**Path:** `app/domains/location/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.location.models import Country, Address
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

## Classes

| Class | Description |
| --- | --- |
| `AddressRepository` |  |
| `CountryRepository` |  |

### Class: `AddressRepository`
**Inherits from:** BaseRepository[(Address, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_city` `async` |  |
| `find_by_postal_code` `async` |  |
| `search` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, address_id) -> Address:
```

##### `find_by_city`
```python
async def find_by_city(self, city, country_id) -> List[Address]:
```

##### `find_by_postal_code`
```python
async def find_by_postal_code(self, postal_code, country_id) -> List[Address]:
```

##### `search`
```python
async def search(self, search_term, page, page_size) -> Dict[(str, Any)]:
```

### Class: `CountryRepository`
**Inherits from:** BaseRepository[(Country, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_iso_code` `async` |  |
| `find_by_name` `async` |  |
| `get_by_currency` `async` |  |
| `get_by_region` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, country_id) -> Country:
```

##### `find_by_iso_code`
```python
async def find_by_iso_code(self, iso_code) -> Optional[Country]:
```

##### `find_by_name`
```python
async def find_by_name(self, name) -> List[Country]:
```

##### `get_by_currency`
```python
async def get_by_currency(self, currency_code) -> List[Country]:
```

##### `get_by_region`
```python
async def get_by_region(self, region) -> List[Country]:
```
