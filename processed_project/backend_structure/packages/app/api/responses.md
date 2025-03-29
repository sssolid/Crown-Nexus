# Module: app.api.responses

**Path:** `app/api/responses.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, TypeVar
from app.schemas.responses import Response, PaginatedResponse
from fastapi import status
from fastapi.responses import JSONResponse
```

## Global Variables
```python
T = T = TypeVar("T")
```

## Functions

| Function | Description |
| --- | --- |
| `created_response` |  |
| `error_response` |  |
| `no_content_response` |  |
| `paginated_response` |  |
| `success_response` |  |

### `created_response`
```python
def created_response(data, message, meta, request_id) -> JSONResponse:
```

### `error_response`
```python
def error_response(message, code, data, meta, request_id) -> JSONResponse:
```

### `no_content_response`
```python
def no_content_response() -> JSONResponse:
```

### `paginated_response`
```python
def paginated_response(items, pagination, message, code, meta, request_id) -> JSONResponse:
```

### `success_response`
```python
def success_response(data, message, code, meta, pagination, request_id) -> JSONResponse:
```
