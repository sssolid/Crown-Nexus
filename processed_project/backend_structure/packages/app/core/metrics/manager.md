# Module: app.core.metrics.manager

**Path:** `app/core/metrics/manager.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple
from app.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag, MetricType, MetricsConfig
from app.core.metrics.collectors import CounterCollector, GaugeCollector, HistogramCollector, SummaryCollector
from app.core.metrics.decorators import async_timed, timed
from app.core.metrics.prometheus import PrometheusManager
from app.core.metrics.trackers import CacheTracker, DatabaseTracker, HttpTracker, ServiceTracker
```

## Global Variables
```python
logger = logger = get_logger("app.core.metrics.manager")
```

## Functions

| Function | Description |
| --- | --- |
| `async_timed_function` |  |
| `create_counter` |  |
| `create_gauge` |  |
| `create_histogram` |  |
| `create_summary` |  |
| `get_current_metrics` |  |
| `increment_counter` |  |
| `initialize` |  |
| `observe_histogram` |  |
| `observe_summary` |  |
| `set_gauge` |  |
| `shutdown` |  |
| `timed_function` |  |
| `track_cache_operation` |  |
| `track_db_query` |  |
| `track_in_progress` |  |
| `track_request` |  |
| `track_service_call` |  |

### `async_timed_function`
```python
def async_timed_function(name, metric_type, labels_func, track_in_progress_flag, in_progress_metric) -> Callable:
```

### `create_counter`
```python
def create_counter(name, description, labelnames, namespace, subsystem) -> CounterCollector:
```

### `create_gauge`
```python
def create_gauge(name, description, labelnames, namespace, subsystem) -> GaugeCollector:
```

### `create_histogram`
```python
def create_histogram(name, description, labelnames, buckets, namespace, subsystem) -> HistogramCollector:
```

### `create_summary`
```python
def create_summary(name, description, labelnames, namespace, subsystem) -> SummaryCollector:
```

### `get_current_metrics`
```python
def get_current_metrics() -> Dict[(str, Dict[(str, Any)])]:
```

### `increment_counter`
```python
def increment_counter(name, amount, labels) -> None:
```

### `initialize`
```python
async def initialize(config) -> None:
```

### `observe_histogram`
```python
def observe_histogram(name, value, labels) -> None:
```

### `observe_summary`
```python
def observe_summary(name, value, labels) -> None:
```

### `set_gauge`
```python
def set_gauge(name, value, labels) -> None:
```

### `shutdown`
```python
async def shutdown() -> None:
```

### `timed_function`
```python
def timed_function(name, metric_type, labels_func, track_in_progress_flag, in_progress_metric) -> Callable:
```

### `track_cache_operation`
```python
def track_cache_operation(operation, backend, hit, duration, component) -> None:
```

### `track_db_query`
```python
def track_db_query(operation, entity, duration, error) -> None:
```

### `track_in_progress`
```python
def track_in_progress(metric_name, labels, count) -> None:
```

### `track_request`
```python
def track_request(method, endpoint, status_code, duration, error_code) -> None:
```

### `track_service_call`
```python
def track_service_call(component, action, duration, error) -> None:
```
