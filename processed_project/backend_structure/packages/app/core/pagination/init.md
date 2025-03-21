# Module: app.core.pagination

**Path:** `app/core/pagination/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.pagination.base import CursorPaginationParams, OffsetPaginationParams, PaginationResult, SortDirection, SortField
from app.core.pagination.manager import initialize, shutdown, paginate_with_offset, paginate_with_cursor
```

## Global Variables
```python
__all__ = __all__ = [
    # Base types
    "PaginationResult",
    "OffsetPaginationParams",
    "CursorPaginationParams",
    "SortDirection",
    "SortField",
    # Core functions
    "initialize",
    "shutdown",
    "paginate_with_offset",
    "paginate_with_cursor",
]
```
