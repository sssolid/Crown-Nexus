# Module: app.core.events.service

**Path:** `app/core/events/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import inspect
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast
from app.core.events.backend import EventBackend, EventBackendType, EventHandler, get_event_backend, init_event_backend, init_domain_events, publish_event as backend_publish_event, subscribe_to_event as backend_subscribe_to_event
from app.core.events.exceptions import EventConfigurationException, EventPublishException, EventServiceException, EventHandlerException
from app.logging import get_logger
from app.core.dependency_manager import get_dependency
from app.core.dependency_manager import register_service
```

## Global Variables
```python
logger = logger = get_logger("app.core.events.service")
T = T = TypeVar("T")
Event = Event = Dict[str, Any]
HAS_METRICS = False
```

## Functions

| Function | Description |
| --- | --- |
| `get_event_service` |  |

### `get_event_service`
```python
def get_event_service() -> EventService:
```

## Classes

| Class | Description |
| --- | --- |
| `EventService` |  |

### Class: `EventService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `event_handler` |  |
| `initialize` `async` |  |
| `publish` `async` |  |
| `set_default_context` |  |
| `shutdown` `async` |  |
| `subscribe` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `event_handler`
```python
def event_handler(self, event_name, filter_func) -> Callable[([EventHandler], EventHandler)]:
```

##### `initialize`
```python
async def initialize(self, backend_type) -> None:
```

##### `publish`
```python
async def publish(self, event_name, payload, context) -> None:
```

##### `set_default_context`
```python
def set_default_context(self, context) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

##### `subscribe`
```python
def subscribe(self, event_name) -> Callable[([EventHandler], EventHandler)]:
```
