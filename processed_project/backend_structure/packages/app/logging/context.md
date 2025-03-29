# Module: app.logging.context

**Path:** `app/logging/context.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, cast
import structlog
from structlog.stdlib import BoundLogger
from app.logging.config import _request_context, get_logger
```

## Global Variables
```python
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
```

## Functions

| Function | Description |
| --- | --- |
| `clear_user_id` |  |
| `log_execution_time` |  |
| `log_execution_time_async` |  |
| `request_context` |  |
| `set_user_id` |  |

### `clear_user_id`
```python
def clear_user_id() -> None:
```

### `log_execution_time`
```python
def log_execution_time(logger, level):
```

### `log_execution_time_async`
```python
def log_execution_time_async(logger, level):
```

### `request_context`
```python
@contextmanager
def request_context(request_id, user_id):
```

### `set_user_id`
```python
def set_user_id(user_id) -> None:
```
