# Module: app.services.base_service.contracts

**Path:** `app/services/base_service/contracts.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel
from app.db.base_class import Base
from app.services.interfaces import CrudServiceInterface
```

## Global Variables
```python
T = T = TypeVar("T", bound=Base)  # SQLAlchemy model type
C = C = TypeVar("C", bound=BaseModel)  # Create schema type
U = U = TypeVar("U", bound=BaseModel)  # Update schema type
R = R = TypeVar("R", bound=BaseModel)  # Response schema type
ID = ID = TypeVar("ID")  # ID type
```

## Classes

| Class | Description |
| --- | --- |
| `BaseServiceProtocol` |  |

### Class: `BaseServiceProtocol`
**Inherits from:** CrudServiceInterface[(T, ID, C, U, R)], Generic[(T, ID, C, U, R)]

#### Methods

| Method | Description |
| --- | --- |
| `after_create` `async` |  |
| `after_delete` `async` |  |
| `after_update` `async` |  |
| `before_create` `async` |  |
| `before_delete` `async` |  |
| `before_update` `async` |  |
| `validate_create` `async` |  |
| `validate_delete` `async` |  |
| `validate_update` `async` |  |

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
