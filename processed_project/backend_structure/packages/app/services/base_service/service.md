# Module: app.services.base_service.service

**Path:** `app/services/base_service/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
from app.core.permissions import Permission
from app.db.base_class import Base
from app.repositories.base import BaseRepository
from app.schemas.pagination import CursorPaginationParams, OffsetPaginationParams, PaginationResult
from app.services.base_service.contracts import BaseServiceProtocol
from app.services.base_service.operations import CreateUpdateOperations, ReadDeleteOperations
from app.services.base_service.permissions import PermissionHelper
from app.services.pagination.service import PaginationService
```

## Global Variables
```python
logger = logger = get_logger("app.services.base_service.service")
T = T = TypeVar("T", bound=Base)  # SQLAlchemy model type
C = C = TypeVar("C", bound=BaseModel)  # Create schema type
U = U = TypeVar("U", bound=BaseModel)  # Update schema type
R = R = TypeVar("R", bound=BaseModel)  # Response schema type
ID = ID = TypeVar("ID")  # ID type
```

## Classes

| Class | Description |
| --- | --- |
| `BaseService` |  |

### Class: `BaseService`
**Inherits from:** Generic[(T, C, U, R, ID)], BaseServiceProtocol[(T, ID, C, U, R)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `after_create` `async` |  |
| `after_delete` `async` |  |
| `after_update` `async` |  |
| `apply_filters` `async` |  |
| `before_create` `async` |  |
| `before_delete` `async` |  |
| `before_update` `async` |  |
| `create` `async` |  |
| `create_with_schema` `async` |  |
| `delete` `async` |  |
| `get` `async` |  |
| `get_all` `async` |  |
| `get_by_id` `async` |  |
| `get_multi` `async` |  |
| `get_paginated` `async` |  |
| `get_paginated_with_cursor` `async` |  |
| `initialize` `async` |  |
| `shutdown` `async` |  |
| `to_response` `async` |  |
| `to_response_multi` `async` |  |
| `update` `async` |  |
| `update_with_schema` `async` |  |
| `validate_create` `async` |  |
| `validate_delete` `async` |  |
| `validate_update` `async` |  |

##### `__init__`
```python
def __init__(self, db, model_class, create_schema, update_schema, response_schema, repository_class) -> None:
```

##### `after_create`
```python
async def after_create(self, entity, user_id) -> None:
```

##### `after_delete`
```python
async def after_delete(self, entity, user_id) -> None:
```

##### `after_update`
```python
async def after_update(self, updated_entity, original_entity, user_id) -> None:
```

##### `apply_filters`
```python
async def apply_filters(self, filters, user_id) -> Dict[(str, Any)]:
```

##### `before_create`
```python
async def before_create(self, data, user_id) -> None:
```

##### `before_delete`
```python
async def before_delete(self, entity, user_id) -> None:
```

##### `before_update`
```python
async def before_update(self, entity, data, user_id) -> None:
```

##### `create`
```python
async def create(self, data, user_id) -> T:
```

##### `create_with_schema`
```python
async def create_with_schema(self, schema, user_id) -> T:
```

##### `delete`
```python
async def delete(self, id, user_id, hard_delete) -> bool:
```

##### `get`
```python
async def get(self, id, user_id) -> T:
```

##### `get_all`
```python
async def get_all(self, page, page_size, filters, user_id) -> Dict[(str, Any)]:
```

##### `get_by_id`
```python
async def get_by_id(self, id, user_id) -> Optional[T]:
```

##### `get_multi`
```python
async def get_multi(self, user_id, page, page_size, filters, order_by) -> Dict[(str, Any)]:
```

##### `get_paginated`
```python
async def get_paginated(self, user_id, params, filters) -> PaginationResult[R]:
```

##### `get_paginated_with_cursor`
```python
async def get_paginated_with_cursor(self, user_id, params, filters) -> PaginationResult[R]:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

##### `to_response`
```python
async def to_response(self, entity) -> R:
```

##### `to_response_multi`
```python
async def to_response_multi(self, entities) -> List[R]:
```

##### `update`
```python
async def update(self, id, data, user_id) -> T:
```

##### `update_with_schema`
```python
async def update_with_schema(self, id, schema, user_id) -> Optional[T]:
```

##### `validate_create`
```python
async def validate_create(self, data, user_id) -> None:
```

##### `validate_delete`
```python
async def validate_delete(self, entity, user_id) -> None:
```

##### `validate_update`
```python
async def validate_update(self, entity, data, user_id) -> None:
```
