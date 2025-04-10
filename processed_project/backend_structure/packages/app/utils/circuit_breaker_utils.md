# Module: app.utils.circuit_breaker_utils

**Path:** `app/utils/circuit_breaker_utils.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
from typing import Any, Callable
from fastapi import Request, Response
from app.utils.circuit_breaker import circuit_breaker
```

## Functions

| Function | Description |
| --- | --- |
| `safe_increment_counter` |  |
| `safe_is_rate_limited` |  |
| `safe_observe_histogram` |  |

### `safe_increment_counter`
```python
@circuit_breaker('metrics_service_log', failure_threshold=10, timeout=30)
def safe_increment_counter(metrics_service, *args, **kwargs) -> None:
```

### `safe_is_rate_limited`
```python
@circuit_breaker('redis_rate_limiter', failure_threshold=5, timeout=60)
async def safe_is_rate_limited(rate_limiter, key, rule) -> tuple[(bool, int, int)]:
```

### `safe_observe_histogram`
```python
@circuit_breaker('metrics_service_histogram', failure_threshold=10, timeout=30)
def safe_observe_histogram(metrics_service, *args, **kwargs) -> None:
```
