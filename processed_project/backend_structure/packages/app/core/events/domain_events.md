# Module: app.core.events.domain_events

**Path:** `app/core/events/domain_events.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, ClassVar, Dict, Generic, Optional, Type, TypeVar
```

## Global Variables
```python
T = T = TypeVar("T")
```

## Classes

| Class | Description |
| --- | --- |
| `DomainEvent` |  |
| `OrderCompletedEvent` |  |
| `ProductUpdatedEvent` |  |
| `TypedUserCreatedEvent` |  |
| `UserCreatedEvent` |  |
| `UserData` |  |

### Class: `DomainEvent`
**Inherits from:** Generic[T]
**Decorators:**
- `@dataclass`

#### Methods

| Method | Description |
| --- | --- |
| `create` |  |
| `from_dict` |  |
| `to_dict` |  |

##### `create`
```python
@classmethod
def create(cls, data, **context) -> DomainEvent[T]:
```

##### `from_dict`
```python
@classmethod
def from_dict(cls, data) -> DomainEvent:
```

##### `to_dict`
```python
def to_dict(self) -> Dict[(str, Any)]:
```

### Class: `OrderCompletedEvent`
**Inherits from:** DomainEvent[Dict[(str, Any)]]
**Decorators:**
- `@dataclass`

### Class: `ProductUpdatedEvent`
**Inherits from:** DomainEvent[Dict[(str, Any)]]
**Decorators:**
- `@dataclass`

### Class: `TypedUserCreatedEvent`
**Inherits from:** DomainEvent[UserData]
**Decorators:**
- `@dataclass`

### Class: `UserCreatedEvent`
**Inherits from:** DomainEvent[Dict[(str, Any)]]
**Decorators:**
- `@dataclass`

### Class: `UserData`
**Decorators:**
- `@dataclass`
