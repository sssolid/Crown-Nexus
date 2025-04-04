# Module: tests.utils

**Path:** `tests/utils.py`

[Back to Project Index](../../index.md)

## Imports
```python
from __future__ import annotations
import random
import string
from typing import Any, Dict, List, Optional, Type, TypeVar
from httpx import AsyncClient
from pydantic import BaseModel
```

## Global Variables
```python
M = M = TypeVar("M", bound=BaseModel)
```

## Functions

| Function | Description |
| --- | --- |
| `assert_model_data_matches` |  |
| `create_random_email` |  |
| `create_random_string` |  |
| `make_authenticated_request` |  |
| `validate_model_response` |  |

### `assert_model_data_matches`
```python
def assert_model_data_matches(model, data) -> None:
```

### `create_random_email`
```python
def create_random_email() -> str:
```

### `create_random_string`
```python
def create_random_string(length) -> str:
```

### `make_authenticated_request`
```python
async def make_authenticated_request(client, method, url, token, **kwargs) -> Any:
```

### `validate_model_response`
```python
def validate_model_response(response_data, model_type, exclude_fields) -> M:
```
