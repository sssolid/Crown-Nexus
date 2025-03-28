# Module: app.core.metrics.trackers

**Path:** `app/core/metrics/trackers.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Optional
from app.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag
```

## Global Variables
```python
logger = logger = get_logger("app.core.metrics.trackers")
```

## Classes

| Class | Description |
| --- | --- |
| `CacheTracker` |  |
| `DatabaseTracker` |  |
| `HttpTracker` |  |
| `ServiceTracker` |  |

### Class: `CacheTracker`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `track_operation` |  |

##### `__init__`
```python
def __init__(self, increment_counter_func, observe_histogram_func):
```

##### `track_operation`
```python
def track_operation(self, operation, backend, hit, duration, component) -> None:
```

### Class: `DatabaseTracker`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `track_query` |  |

##### `__init__`
```python
def __init__(self, increment_counter_func, observe_histogram_func, increment_error_func):
```

##### `track_query`
```python
def track_query(self, operation, entity, duration, error) -> None:
```

### Class: `HttpTracker`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `track_request` |  |

##### `__init__`
```python
def __init__(self, increment_counter_func, observe_histogram_func, increment_error_func):
```

##### `track_request`
```python
def track_request(self, method, endpoint, status_code, duration, error_code) -> None:
```

### Class: `ServiceTracker`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `track_call` |  |

##### `__init__`
```python
def __init__(self, increment_counter_func, observe_histogram_func, increment_error_func):
```

##### `track_call`
```python
def track_call(self, component, action, duration, error) -> None:
```
