# Module: app.utils.circuit_breaker

**Path:** `app/utils/circuit_breaker.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import enum
import functools
import time
from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, cast
from app.core.exceptions import ServiceException, ErrorCode
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.utils.circuit_breaker")
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
```

## Functions

| Function | Description |
| --- | --- |
| `circuit_breaker` |  |

### `circuit_breaker`
```python
def circuit_breaker(name, failure_threshold, success_threshold, timeout, exception_types, fallback) -> Callable[([F], F)]:
```

## Classes

| Class | Description |
| --- | --- |
| `CircuitBreaker` |  |
| `CircuitBreakerConfig` |  |
| `CircuitState` |  |

### Class: `CircuitBreaker`

#### Methods

| Method | Description |
| --- | --- |
| `__call__` |  |
| `__init__` |  |
| `async_call` |  |
| `check_state` |  |
| `get` |  |
| `get_all_states` |  |
| `get_or_create` |  |
| `reset` |  |
| `reset_all` |  |

##### `__call__`
```python
def __call__(self, func) -> F:
```

##### `__init__`
```python
def __init__(self, name, config) -> None:
```

##### `async_call`
```python
def async_call(self, func) -> F:
```

##### `check_state`
```python
def check_state(self) -> None:
```

##### `get`
```python
@classmethod
def get(cls, name) -> CircuitBreaker:
```

##### `get_all_states`
```python
@classmethod
def get_all_states(cls) -> Dict[(str, CircuitState)]:
```

##### `get_or_create`
```python
@classmethod
def get_or_create(cls, name, config) -> CircuitBreaker:
```

##### `reset`
```python
def reset(self) -> None:
```

##### `reset_all`
```python
@classmethod
def reset_all(cls) -> None:
```

### Class: `CircuitBreakerConfig`
**Decorators:**
- `@dataclass`

### Class: `CircuitState`
**Inherits from:** enum.Enum

#### Attributes

| Name | Value |
| --- | --- |
| `CLOSED` | `'closed'` |
| `OPEN` | `'open'` |
| `HALF_OPEN` | `'half_open'` |
