# Module: app.core.logging

**Path:** `app/core/logging.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import logging
import logging.config
import sys
import threading
import uuid
from contextlib import contextmanager
import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, Union
import pythonjsonlogger
import structlog
from pythonjsonlogger import jsonlogger
from structlog.stdlib import BoundLogger
from structlog.types import EventDict, Processor, WrappedLogger
from app.core.config.base import Environment, LogLevel
```

## Global Variables
```python
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
```

## Functions

| Function | Description |
| --- | --- |
| `add_request_id_processor` |  |
| `add_service_info_processor` |  |
| `add_timestamp_processor` |  |
| `add_user_id_processor` |  |
| `clear_user_id` |  |
| `configure_std_logging` |  |
| `configure_structlog` |  |
| `get_logger` |  |
| `log_execution_time` |  |
| `log_execution_time_async` |  |
| `request_context` |  |
| `set_user_id` |  |
| `setup_logging` |  |

### `add_request_id_processor`
```python
def add_request_id_processor(logger, method_name, event_dict) -> EventDict:
```

### `add_service_info_processor`
```python
def add_service_info_processor(logger, method_name, event_dict) -> EventDict:
```

### `add_timestamp_processor`
```python
def add_timestamp_processor(logger, method_name, event_dict) -> EventDict:
```

### `add_user_id_processor`
```python
def add_user_id_processor(logger, method_name, event_dict) -> EventDict:
```

### `clear_user_id`
```python
def clear_user_id() -> None:
```

### `configure_std_logging`
```python
def configure_std_logging() -> None:
```

### `configure_structlog`
```python
def configure_structlog() -> None:
```

### `get_logger`
```python
def get_logger(name) -> BoundLogger:
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

### `setup_logging`
```python
def setup_logging() -> None:
```

## Classes

| Class | Description |
| --- | --- |
| `RequestIdFilter` |  |
| `UserIdFilter` |  |

### Class: `RequestIdFilter`
**Inherits from:** logging.Filter

#### Methods

| Method | Description |
| --- | --- |
| `filter` |  |

##### `filter`
```python
def filter(self, record) -> bool:
```

### Class: `UserIdFilter`
**Inherits from:** logging.Filter

#### Methods

| Method | Description |
| --- | --- |
| `filter` |  |

##### `filter`
```python
def filter(self, record) -> bool:
```
