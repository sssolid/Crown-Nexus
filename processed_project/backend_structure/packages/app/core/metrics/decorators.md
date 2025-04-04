# Module: app.core.metrics.decorators

**Path:** `app/core/metrics/decorators.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import functools
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Generator, Optional, cast
from app.logging import get_logger
from app.core.metrics.base import F
```

## Global Variables
```python
logger = logger = get_logger("app.core.metrics.decorators")
```

## Functions

| Function | Description |
| --- | --- |
| `async_timed` |  |
| `timed` |  |
| `timer` |  |

### `async_timed`
```python
def async_timed(metric_type, name, observe_func, labels_func, track_in_progress, track_in_progress_func, in_progress_metric) -> Callable[([F], F)]:
```

### `timed`
```python
def timed(metric_type, name, observe_func, labels_func, track_in_progress, track_in_progress_func, in_progress_metric) -> Callable[([F], F)]:
```

### `timer`
```python
@contextmanager
def timer(metric_type, name, observe_func, labels, track_in_progress, track_in_progress_func, in_progress_metric) -> Generator[(None, None, None)]:
```
