# Module: app.core.dependency_manager

**Path:** `app/core/dependency_manager.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import functools
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set, Type, TypeVar, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConfigurationException
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.dependency_manager")
T = T = TypeVar("T")
dependency_manager = dependency_manager = DependencyManager()
```

## Functions

| Function | Description |
| --- | --- |
| `get_dependency` |  |
| `get_service` |  |
| `initialize_services` |  |
| `inject_dependency` |  |
| `register_async_service` |  |
| `register_service` |  |
| `register_services` |  |
| `shutdown_services` |  |
| `with_dependencies` |  |

### `get_dependency`
```python
def get_dependency(name, **kwargs) -> Any:
```

### `get_service`
```python
def get_service(service_name, db) -> Any:
```

### `initialize_services`
```python
async def initialize_services() -> None:
```

### `inject_dependency`
```python
def inject_dependency(dependency_name) -> Callable:
```

### `register_async_service`
```python
def register_async_service(async_provider, name) -> Callable[(Ellipsis, Awaitable[T])]:
```

### `register_service`
```python
def register_service(provider, name) -> Callable[(Ellipsis, Any)]:
```

### `register_services`
```python
def register_services() -> None:
```

### `shutdown_services`
```python
async def shutdown_services() -> None:
```

### `with_dependencies`
```python
def with_dependencies(**dependencies) -> Callable:
```

## Classes

| Class | Description |
| --- | --- |
| `DependencyManager` |  |

### Class: `DependencyManager`

#### Methods

| Method | Description |
| --- | --- |
| `__new__` |  |
| `clear` |  |
| `clear_instance` |  |
| `get` |  |
| `get_all` |  |
| `get_instance` |  |
| `initialize_services` `async` |  |
| `register_dependency` |  |
| `register_dependency_relationship` |  |
| `register_service` |  |
| `shutdown_services` `async` |  |

##### `__new__`
```python
def __new__(cls) -> DependencyManager:
```

##### `clear`
```python
def clear(self) -> None:
```

##### `clear_instance`
```python
def clear_instance(self, name) -> None:
```

##### `get`
```python
def get(self, name, **kwargs) -> Any:
```

##### `get_all`
```python
def get_all(self, db) -> Dict[(str, Any)]:
```

##### `get_instance`
```python
def get_instance(self, cls, **kwargs) -> T:
```

##### `initialize_services`
```python
async def initialize_services(self) -> None:
```

##### `register_dependency`
```python
def register_dependency(self, name, instance) -> None:
```

##### `register_dependency_relationship`
```python
def register_dependency_relationship(self, service_name, depends_on) -> None:
```

##### `register_service`
```python
def register_service(self, provider, name) -> None:
```

##### `shutdown_services`
```python
async def shutdown_services(self) -> None:
```
