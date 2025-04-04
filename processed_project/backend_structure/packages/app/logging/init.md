# Module: app.logging

**Path:** `app/logging/__init__.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.logging.config import get_logger, initialize_logging, reinitialize_logging, shutdown_logging
from app.logging.context import clear_user_id, log_execution_time, log_execution_time_async, request_context, set_user_id
```

## Global Variables
```python
__all__ = __all__ = [
    "initialize_logging",
    "reinitialize_logging",
    "shutdown_logging",
    "get_logger",
    "request_context",
    "set_user_id",
    "clear_user_id",
    "log_execution_time",
    "log_execution_time_async",
]
```
