# Module: app.core.rate_limiting.utils

**Path:** `app/core/rate_limiting/utils.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import time
from typing import Tuple
from app.logging import get_logger
from app.utils.redis_manager import get_key, set_key
```

## Global Variables
```python
logger = logger = get_logger("app.core.rate_limiting.utils")
```

## Functions

| Function | Description |
| --- | --- |
| `check_rate_limit` |  |
| `get_ttl` |  |

### `check_rate_limit`
```python
async def check_rate_limit(key, max_requests, window_seconds) -> Tuple[(bool, int, int)]:
```

### `get_ttl`
```python
async def get_ttl(key) -> int:
```
