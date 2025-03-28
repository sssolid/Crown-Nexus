# Module: app.core.metrics.prometheus

**Path:** `app/core/metrics/prometheus.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
from typing import Optional
from prometheus_client import REGISTRY, start_http_server, push_to_gateway
from app.logging import get_logger
from app.core.metrics.base import MetricsConfig
```

## Global Variables
```python
logger = logger = get_logger("app.core.metrics.prometheus")
```

## Classes

| Class | Description |
| --- | --- |
| `PrometheusManager` |  |

### Class: `PrometheusManager`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `initialize` `async` |  |
| `shutdown` `async` |  |

##### `__init__`
```python
def __init__(self, config):
```

##### `initialize`
```python
async def initialize(self) -> None:
```

##### `shutdown`
```python
async def shutdown(self) -> None:
```
