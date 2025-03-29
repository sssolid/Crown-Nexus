# Module: app.logging.config

**Path:** `app/logging/config.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
import logging
import logging.config
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import pythonjsonlogger.jsonlogger as pythonjsonlogger
import structlog
from structlog.stdlib import BoundLogger, LoggerFactory
from structlog.types import EventDict, Processor, WrappedLogger
import threading
```

## Global Variables
```python
DEFAULT_LOG_LEVEL = 'INFO'
```

## Functions

| Function | Description |
| --- | --- |
| `add_request_id_processor` |  |
| `add_service_info_processor` |  |
| `add_timestamp_processor` |  |
| `add_user_id_processor` |  |
| `configure_std_logging` |  |
| `configure_structlog` |  |
| `get_environment` |  |
| `get_log_level` |  |
| `get_logger` |  |
| `initialize_logging` |  |
| `reinitialize_logging` |  |
| `shutdown_logging` |  |

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

### `configure_std_logging`
```python
def configure_std_logging() -> None:
```

### `configure_structlog`
```python
def configure_structlog() -> None:
```

### `get_environment`
```python
def get_environment() -> str:
```

### `get_log_level`
```python
def get_log_level() -> str:
```

### `get_logger`
```python
def get_logger(name) -> BoundLogger:
```

### `initialize_logging`
```python
def initialize_logging() -> None:
```

### `reinitialize_logging`
```python
async def reinitialize_logging() -> None:
```

### `shutdown_logging`
```python
async def shutdown_logging() -> None:
```

## Classes

| Class | Description |
| --- | --- |
| `ConsoleRendererWithLineNumbers` |  |
| `RequestIdFilter` |  |
| `UserIdFilter` |  |

### Class: `ConsoleRendererWithLineNumbers`
**Inherits from:** structlog.dev.ConsoleRenderer

#### Methods

| Method | Description |
| --- | --- |
| `__call__` |  |

##### `__call__`
```python
def __call__(self, logger, name, event_dict) -> str:
```

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
