# Module: app.core.base

**Path:** `app/core/base.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import abc
import contextlib
from datetime import datetime, timezone
from typing import Any, AsyncContextManager, Callable, ClassVar, Dict, List, Optional, Protocol, Type, TypeVar, Union
from pydantic import BaseModel
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.base")
T = T = TypeVar("T")
T_Service = T_Service = TypeVar("T_Service", bound="CoreService")
T_Manager = T_Manager = TypeVar("T_Manager", bound="CoreManager")
T_Backend = T_Backend = TypeVar("T_Backend", bound="CoreBackend")
T_Component = T_Component = TypeVar("T_Component", bound="InitializableComponent")
```

## Functions

| Function | Description |
| --- | --- |
| `discover_backends` |  |

### `discover_backends`
```python
def discover_backends(package_path) -> Dict[(str, Type[Any])]:
```

## Classes

| Class | Description |
| --- | --- |
| `CoreBackend` |  |
| `CoreManager` |  |
| `CoreService` |  |
| `HealthCheckable` |  |
| `HealthStatus` |  |
| `InitializableComponent` |  |
| `MetricsEnabled` |  |
| `ServiceConfig` |  |
| `ServiceRegistry` |  |

### Class: `CoreBackend`
**Inherits from:** InitializableComponent, Protocol

### Class: `CoreManager`
**Inherits from:** InitializableComponent, HealthCheckable

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `component_name` `@property` |  |
| `health_check` `async` |  |
| `initialize` `async` |  |
| `register_component` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `component_name`
```python
@property
@abc.abstractmethod
def component_name(self) -> str:
```

##### `health_check`
```python
async def health_check(self) -> Dict[(str, Any)]:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `register_component`
```python
def register_component(self, component) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

### Class: `CoreService`
**Inherits from:** abc.ABC

#### Methods

| Method | Description |
| --- | --- |
| `__aenter__` `async` |  |
| `__aexit__` `async` |  |
| `__init__` |  |
| `__new__` |  |
| `context` |  |
| `get_instance` |  |
| `health_check` `async` |  |
| `initialize` `async` |  |
| `is_initialized` `@property` |  |
| `register_component` |  |
| `service_name` `@property` |  |
| `shutdown` `async` |  |

##### `__aenter__`
```python
async def __aenter__(self) -> 'CoreService':
```

##### `__aexit__`
```python
async def __aexit__(self, *args) -> None:
```

##### `__init__`
```python
def __init__(self) -> None:
```

##### `__new__`
```python
def __new__(cls, *args, **kwargs) -> T_Service:
```

##### `context`
```python
def context(self) -> 'AsyncContextManager[CoreService]':
```

##### `get_instance`
```python
@classmethod
def get_instance(cls) -> T_Service:
```

##### `health_check`
```python
async def health_check(self) -> Dict[(str, Any)]:
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `is_initialized`
```python
@property
def is_initialized(self) -> bool:
```

##### `register_component`
```python
def register_component(self, component) -> None:
```

##### `service_name`
```python
@property
@abc.abstractmethod
def service_name(self) -> str:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

### Class: `HealthCheckable`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `health_check` `async` |  |

##### `health_check`
```python
async def health_check(self) -> Dict[(str, Any)]:
```

### Class: `HealthStatus`
**Inherits from:** BaseModel

### Class: `InitializableComponent`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `initialize` `async` |  |
| `shutdown` `async` |  |

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

### Class: `MetricsEnabled`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `increment_counter` |  |
| `record_gauge` |  |
| `record_timing` |  |

##### `increment_counter`
```python
def increment_counter(self, name, value, tags) -> None:
```

##### `record_gauge`
```python
def record_gauge(self, name, value, tags) -> None:
```

##### `record_timing`
```python
def record_timing(self, name, value, tags) -> None:
```

### Class: `ServiceConfig`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `from_settings` |  |

##### `from_settings`
```python
@classmethod
def from_settings(cls, settings_prefix, settings_obj) -> 'ServiceConfig':
```

### Class: `ServiceRegistry`

#### Methods

| Method | Description |
| --- | --- |
| `get` |  |
| `get_all` |  |
| `initialize_all` `async` |  |
| `register` |  |
| `shutdown_all` `async` |  |

##### `get`
```python
@classmethod
def get(cls, service_name) -> Optional[CoreService]:
```

##### `get_all`
```python
@classmethod
def get_all(cls) -> Dict[(str, CoreService)]:
```

##### `initialize_all`
```python
@classmethod
async def initialize_all(cls) -> None:
```

##### `register`
```python
@classmethod
def register(cls, service_name, service) -> None:
```

##### `shutdown_all`
```python
@classmethod
async def shutdown_all(cls) -> None:
```
