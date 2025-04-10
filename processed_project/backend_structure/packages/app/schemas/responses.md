# Module: app.schemas.responses

**Path:** `app/schemas/responses.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
```

## Global Variables
```python
T = T = TypeVar("T")
```

## Classes

| Class | Description |
| --- | --- |
| `PaginatedResponse` |  |
| `Response` |  |
| `ResponseBase` |  |

### Class: `PaginatedResponse`
**Inherits from:** ResponseBase, Generic[T]

#### Methods

| Method | Description |
| --- | --- |
| `from_pagination_result` |  |

##### `from_pagination_result`
```python
@classmethod
def from_pagination_result(cls, items, pagination, message, code, meta, request_id) -> PaginatedResponse:
```

### Class: `Response`
**Inherits from:** ResponseBase, Generic[T]

#### Methods

| Method | Description |
| --- | --- |
| `error` |  |
| `success` |  |

##### `error`
```python
@classmethod
def error(cls, message, code, data, meta, request_id) -> Response:
```

##### `success`
```python
@classmethod
def success(cls, data, message, code, meta, pagination, request_id) -> Response:
```

### Class: `ResponseBase`
**Inherits from:** BaseModel
