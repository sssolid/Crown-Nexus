# Module: app.services.interfaces

**Path:** `app/services/interfaces.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar
```

## Global Variables
```python
T = T = TypeVar("T")  # Entity type
ID = ID = TypeVar("ID")  # ID type
C = C = TypeVar("C")  # Create schema type
U = U = TypeVar("U")  # Update schema type
R = R = TypeVar("R")  # Response schema type
```

## Classes

| Class | Description |
| --- | --- |
| `CrudServiceInterface` |  |
| `ReadOnlyServiceInterface` |  |
| `ServiceInterface` |  |

### Class: `CrudServiceInterface`
**Inherits from:** ServiceInterface[(T, ID)], Generic[(T, ID, C, U, R)]

#### Methods

| Method | Description |
| --- | --- |
| `create_with_schema` `async` |  |
| `to_response` `async` |  |
| `to_response_multi` `async` |  |
| `update_with_schema` `async` |  |

##### `create_with_schema`
```python
async def create_with_schema(self, schema, user_id) -> T:
```

##### `to_response`
```python
async def to_response(self, entity) -> R:
```

##### `to_response_multi`
```python
async def to_response_multi(self, entities) -> List[R]:
```

##### `update_with_schema`
```python
async def update_with_schema(self, id, schema, user_id) -> Optional[T]:
```

### Class: `ReadOnlyServiceInterface`
**Inherits from:** ServiceInterface[(T, ID)], Generic[(T, ID, R)]

#### Methods

| Method | Description |
| --- | --- |
| `to_response` `async` |  |
| `to_response_multi` `async` |  |

##### `to_response`
```python
async def to_response(self, entity) -> R:
```

##### `to_response_multi`
```python
async def to_response_multi(self, entities) -> List[R]:
```

### Class: `ServiceInterface`
**Inherits from:** Protocol, Generic[(T, ID)]

#### Methods

| Method | Description |
| --- | --- |
| `create` `async` |  |
| `delete` `async` |  |
| `get_all` `async` |  |
| `get_by_id` `async` |  |
| `initialize` `async` |  |
| `shutdown` `async` |  |
| `update` `async` |  |

##### `create`
```python
async def create(self, data, user_id) -> T:
```

##### `delete`
```python
async def delete(self, id, user_id) -> bool:
```

##### `get_all`
```python
async def get_all(self, page, page_size, filters, user_id) -> Dict[(str, Any)]:
```

##### `get_by_id`
```python
async def get_by_id(self, id, user_id) -> Optional[T]:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

##### `update`
```python
async def update(self, id, data, user_id) -> Optional[T]:
```
