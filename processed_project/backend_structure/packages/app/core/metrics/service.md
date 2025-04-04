# Module: app.core.metrics.service

**Path:** `app/core/metrics/service.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from app.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag, MetricType, MetricsConfig
from app.core.metrics.collectors import CounterCollector, GaugeCollector, HistogramCollector, SummaryCollector
from app.core.metrics.exceptions import MetricsConfigurationException
from app.core.metrics.manager import increment_counter, set_gauge, observe_histogram, observe_summary, create_counter, create_gauge, create_histogram, create_summary, track_request, track_db_query, track_service_call, track_cache_operation, track_in_progress, timed_function, async_timed_function, initialize as initialize_manager, shutdown as shutdown_manager, get_current_metrics
```

## Global Variables
```python
logger = logger = get_logger("app.core.metrics.service")
F = F = TypeVar("F", bound=Callable[..., Any])
```

## Functions

| Function | Description |
| --- | --- |
| `get_metrics_service` |  |

### `get_metrics_service`
```python
def get_metrics_service() -> MetricsService:
```

## Classes

| Class | Description |
| --- | --- |
| `MetricsService` |  |

### Class: `MetricsService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `async_timed_function` |  |
| `create_counter` |  |
| `create_gauge` |  |
| `create_histogram` |  |
| `create_summary` |  |
| `get_current_metrics` |  |
| `increment_counter` |  |
| `initialize` `async` |  |
| `observe_histogram` |  |
| `observe_summary` |  |
| `set_gauge` |  |
| `shutdown` `async` |  |
| `timed_function` |  |
| `track_cache_operation` |  |
| `track_db_query` |  |
| `track_in_progress` |  |
| `track_request` |  |
| `track_service_call` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `async_timed_function`
```python
def async_timed_function(self, name, metric_type, labels_func, track_in_progress_flag, in_progress_metric) -> Callable:
```

##### `create_counter`
```python
def create_counter(self, name, description, labelnames, namespace, subsystem) -> CounterCollector:
```

##### `create_gauge`
```python
def create_gauge(self, name, description, labelnames, namespace, subsystem) -> GaugeCollector:
```

##### `create_histogram`
```python
def create_histogram(self, name, description, labelnames, buckets, namespace, subsystem) -> HistogramCollector:
```

##### `create_summary`
```python
def create_summary(self, name, description, labelnames, namespace, subsystem) -> SummaryCollector:
```

##### `get_current_metrics`
```python
def get_current_metrics(self) -> Dict[(str, Dict[(str, Any)])]:
```

##### `increment_counter`
```python
def increment_counter(self, name, amount, labels) -> None:
```

##### `initialize`
```python
async def initialize(self, config) -> None:
```

##### `observe_histogram`
```python
def observe_histogram(self, name, value, labels) -> None:
```

##### `observe_summary`
```python
def observe_summary(self, name, value, labels) -> None:
```

##### `set_gauge`
```python
def set_gauge(self, name, value, labels) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```

##### `timed_function`
```python
def timed_function(self, name, metric_type, labels_func, track_in_progress_flag, in_progress_metric) -> Callable:
```

##### `track_cache_operation`
```python
def track_cache_operation(self, operation, backend, hit, duration, component) -> None:
```

##### `track_db_query`
```python
def track_db_query(self, operation, entity, duration, error) -> None:
```

##### `track_in_progress`
```python
def track_in_progress(self, metric_name, labels, count) -> None:
```

##### `track_request`
```python
def track_request(self, method, endpoint, status_code, duration, error_code) -> None:
```

##### `track_service_call`
```python
def track_service_call(self, component, action, duration, error) -> None:
```
