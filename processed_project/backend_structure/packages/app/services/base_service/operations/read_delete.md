# Module: app.services.base_service.operations.read_delete

**Path:** `app/services/base_service/operations/read_delete.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ErrorCode, PermissionDeniedException, ResourceNotFoundException
from app.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import transactional
```

## Global Variables
```python
logger = logger = get_logger("app.services.base_service.operations.read_delete")
T = T = TypeVar("T", bound=Base)  # SQLAlchemy model type
R = R = TypeVar("R", bound=BaseModel)  # Response schema type
ID = ID = TypeVar("ID")  # ID type
```

## Classes

| Class | Description |
| --- | --- |
| `ReadDeleteOperations` |  |

### Class: `ReadDeleteOperations`
**Inherits from:** Generic[(T, R, ID)]

#### Methods

| Method | Description |
| --- | --- |
| `delete` `async` |  |
| `get` `async` |  |
| `get_all` `async` |  |
| `get_by_id` `async` |  |
| `get_multi` `async` |  |
| `to_response` `async` |  |
| `to_response_multi` `async` |  |

##### `delete`
```python
@transactional
async def delete(self, db, repository, id, user_id, hard_delete, required_permission, validate_func, before_func, after_func, get_user_func) -> bool:
```

##### `get`
```python
@transactional
async def get(self, db, repository, id, user_id, required_permission, get_user_func) -> T:
```

##### `get_all`
```python
async def get_all(self, db, repository, page, page_size, filters, user_id, required_permission, get_user_func, apply_filters_func) -> Dict[(str, Any)]:
```

##### `get_by_id`
```python
async def get_by_id(self, db, repository, id, user_id, required_permission, get_user_func) -> Optional[T]:
```

##### `get_multi`
```python
@transactional
async def get_multi(self, db, repository, user_id, page, page_size, filters, order_by, required_permission, get_user_func, apply_filters_func) -> Dict[(str, Any)]:
```

##### `to_response`
```python
async def to_response(self, entity, response_model) -> R:
```

##### `to_response_multi`
```python
async def to_response_multi(self, entities, response_model) -> List[R]:
```
