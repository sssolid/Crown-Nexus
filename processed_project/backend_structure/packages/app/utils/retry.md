# Module: app.utils.retry

**Path:** `app/utils/retry.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import functools
import random
import time
from typing import Any, Callable, List, Optional, Protocol, Type, TypeVar, Union, cast, overload
from app.core.exceptions import NetworkException, ServiceException
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.utils.retry")
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
```

## Functions

| Function | Description |
| --- | --- |
| `async_retry` |  |
| `async_retry_on_network_errors` |  |
| `async_retry_with_timeout` |  |
| `retry` |  |
| `retry_on_network_errors` |  |
| `retry_with_timeout` |  |

### `async_retry`
```python
async def async_retry(func, retries=None, delay, backoff_factor, jitter, exceptions) -> Union[(Callable[([F], F)], F)]:
```

### `async_retry_on_network_errors`
```python
def async_retry_on_network_errors(retries, delay, backoff_factor, jitter) -> Callable[([F], F)]:
```

### `async_retry_with_timeout`
```python
async def async_retry_with_timeout(retries, delay, timeout, backoff_factor, jitter, exceptions) -> Callable[([F], F)]:
```

### `retry`
```python
def retry(func, retries=None, delay, backoff_factor, jitter, exceptions) -> Union[(Callable[([F], F)], F)]:
```

### `retry_on_network_errors`
```python
def retry_on_network_errors(retries, delay, backoff_factor, jitter) -> Callable[([F], F)]:
```

### `retry_with_timeout`
```python
def retry_with_timeout(retries, delay, timeout, backoff_factor, jitter, exceptions) -> Callable[([F], F)]:
```

## Classes

| Class | Description |
| --- | --- |
| `RetryableError` |  |

### Class: `RetryableError`
**Inherits from:** Protocol

#### Methods

| Method | Description |
| --- | --- |
| `is_retryable` |  |

##### `is_retryable`
```python
def is_retryable(self) -> bool:
```
