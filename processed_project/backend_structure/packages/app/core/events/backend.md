# Module: app.core.events.backend

**Path:** `app/core/events/backend.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import inspect
from app.logging import get_logger
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol
```

## Global Variables
```python
logger = logger = get_logger("app.core.events.backend")
EventHandler = EventHandler = Callable[[Dict[str, Any]], Any]
```

## Functions

| Function | Description |
| --- | --- |
| `get_event_backend` |  |
| `init_domain_events` |  |
| `init_event_backend` |  |
| `publish_event` |  |
| `register_event_handlers` |  |
| `subscribe_to_event` |  |

### `get_event_backend`
```python
def get_event_backend() -> EventBackend:
```

### `init_domain_events`
```python
def init_domain_events() -> None:
```

### `init_event_backend`
```python
def init_event_backend(backend_type, **kwargs) -> EventBackend:
```

### `publish_event`
```python
def publish_event(event_name, payload) -> None:
```

### `register_event_handlers`
```python
def register_event_handlers(*modules) -> None:
```

### `subscribe_to_event`
```python
def subscribe_to_event(event_name) -> Callable[([EventHandler], EventHandler)]:
```

## Classes

| Class | Description |
| --- | --- |
| `CeleryEventBackend` |  |
| `EventBackend` |  |
| `EventBackendType` |  |
| `EventPublisher` |  |
| `EventSubscriber` |  |
| `MemoryEventBackend` |  |

### Class: `CeleryEventBackend`
**Inherits from:** EventBackend

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `publish_event` |  |
| `subscribe` |  |

##### `__init__`
```python
def __init__(self, celery_app) -> None:
```

##### `publish_event`
```python
def publish_event(self, event_name, payload) -> None:
```

##### `subscribe`
```python
def subscribe(self, event_name, handler) -> None:
```

### Class: `EventBackend`
**Inherits from:** ABC, EventPublisher, EventSubscriber

#### Methods

| Method | Description |
| --- | --- |
| `publish_event` |  |
| `subscribe` |  |

##### `publish_event`
```python
@abstractmethod
def publish_event(self, event_name, payload) -> None:
```

##### `subscribe`
```python
@abstractmethod
def subscribe(self, event_name, handler) -> None:
```

### Class: `EventBackendType`
**Inherits from:** Enum

#### Attributes

| Name | Value |
| --- | --- |
| `CELERY` | `    CELERY = auto()` |
| `MEMORY` | `    MEMORY = auto()` |

### Class: `EventPublisher`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `publish_event` |  |

##### `publish_event`
```python
def publish_event(self, event_name, payload) -> None:
```

### Class: `EventSubscriber`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `subscribe` |  |

##### `subscribe`
```python
def subscribe(self, event_name, handler) -> None:
```

### Class: `MemoryEventBackend`
**Inherits from:** EventBackend

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `publish_event` |  |
| `subscribe` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `publish_event`
```python
def publish_event(self, event_name, payload) -> None:
```

##### `subscribe`
```python
def subscribe(self, event_name, handler) -> None:
```
