# Module: app.core.metrics.collectors

**Path:** `app/core/metrics/collectors.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Dict, List, Optional
from prometheus_client import Counter, Gauge, Histogram, Summary
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.core.metrics.collectors")
```

## Classes

| Class | Description |
| --- | --- |
| `CounterCollector` |  |
| `GaugeCollector` |  |
| `HistogramCollector` |  |
| `MetricCollector` |  |
| `SummaryCollector` |  |

### Class: `CounterCollector`
**Inherits from:** MetricCollector

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `increment` |  |

##### `__init__`
```python
def __init__(self, name, description, labelnames, namespace, subsystem):
```

##### `increment`
```python
def increment(self, amount, labels) -> None:
```

### Class: `GaugeCollector`
**Inherits from:** MetricCollector

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `decrement` |  |
| `increment` |  |
| `set` |  |

##### `__init__`
```python
def __init__(self, name, description, labelnames, namespace, subsystem):
```

##### `decrement`
```python
def decrement(self, amount, labels) -> None:
```

##### `increment`
```python
def increment(self, amount, labels) -> None:
```

##### `set`
```python
def set(self, value, labels) -> None:
```

### Class: `HistogramCollector`
**Inherits from:** MetricCollector

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `observe` |  |

##### `__init__`
```python
def __init__(self, name, description, labelnames, buckets, namespace, subsystem):
```

##### `observe`
```python
def observe(self, value, labels) -> None:
```

### Class: `MetricCollector`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |

##### `__init__`
```python
def __init__(self, name, description, labelnames, namespace, subsystem):
```

### Class: `SummaryCollector`
**Inherits from:** MetricCollector

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `observe` |  |

##### `__init__`
```python
def __init__(self, name, description, labelnames, namespace, subsystem):
```

##### `observe`
```python
def observe(self, value, labels) -> None:
```
