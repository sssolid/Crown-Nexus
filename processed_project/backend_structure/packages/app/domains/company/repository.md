# Module: app.domains.company.repository

**Path:** `app/domains/company/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.company.models import Company
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

## Classes

| Class | Description |
| --- | --- |
| `CompanyRepository` |  |

### Class: `CompanyRepository`
**Inherits from:** BaseRepository[(Company, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_account_number` `async` |  |
| `find_by_industry` `async` |  |
| `find_by_name` `async` |  |
| `get_active_companies` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, company_id) -> Company:
```

##### `find_by_account_number`
```python
async def find_by_account_number(self, account_number) -> Optional[Company]:
```

##### `find_by_industry`
```python
async def find_by_industry(self, industry) -> List[Company]:
```

##### `find_by_name`
```python
async def find_by_name(self, name) -> Optional[Company]:
```

##### `get_active_companies`
```python
async def get_active_companies(self, page, page_size) -> Dict[(str, Any)]:
```
