# Module: app.services.base_service.operations.create_update

**Path:** `app/services/base_service/operations/create_update.py`

[Back to Project Index](../../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Generic, Optional, TypeVar
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
logger = logger = get_logger("app.services.base_service.operations.create_update")
T = T = TypeVar("T", bound=Base)  # SQLAlchemy model type
C = C = TypeVar("C", bound=BaseModel)  # Create schema type
U = U = TypeVar("U", bound=BaseModel)  # Update schema type
ID = ID = TypeVar("ID")  # ID type
```

## Classes

| Class | Description |
| --- | --- |
| `CreateUpdateOperations` |  |

### Class: `CreateUpdateOperations`
**Inherits from:** Generic[(T, C, U, ID)]

#### Methods

| Method | Description |
| --- | --- |
| `create` `async` |  |
| `create_with_schema` `async` |  |
| `update` `async` |  |
| `update_with_schema` `async` |  |

##### `create`
```python
@transactional
async def create(self, db, repository, data, user_id, required_permission, validate_func, before_func, after_func, get_user_func) -> T:
```

##### `create_with_schema`
```python
async def create_with_schema(self, db, repository, schema, user_id, required_permission, validate_func, before_func, after_func, get_user_func) -> T:
```

##### `update`
```python
@transactional
async def update(self, db, repository, id, data, user_id, required_permission, validate_func, before_func, after_func, get_user_func) -> T:
```

##### `update_with_schema`
```python
async def update_with_schema(self, db, repository, id, schema, user_id, required_permission, validate_func, before_func, after_func, get_user_func) -> Optional[T]:
```
