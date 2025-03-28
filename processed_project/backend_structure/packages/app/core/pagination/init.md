# Module: app.core.pagination

**Path:** `app/core/pagination/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.pagination.base import CursorPaginationParams, OffsetPaginationParams, PaginationResult, SortDirection, SortField
from app.core.pagination.exceptions import InvalidCursorException, InvalidPaginationParamsException, InvalidSortFieldException, PaginationException
from app.core.pagination.manager import initialize, paginate_with_cursor, paginate_with_offset, shutdown
from app.core.pagination.service import PaginationService, get_pagination_service
```

## Global Variables
```python
__all__ = __all__ = [
    "PaginationResult",
    "OffsetPaginationParams",
    "CursorPaginationParams",
    "SortDirection",
    "SortField",
    "initialize",
    "shutdown",
    "paginate_with_offset",
    "paginate_with_cursor",
    "PaginationService",
    "get_pagination_service",
    "PaginationException",
    "InvalidPaginationParamsException",
    "InvalidCursorException",
    "InvalidSortFieldException",
]
```
