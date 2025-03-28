# Module: app.core.error

**Path:** `app/core/error/__init__.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
from app.core.error.manager import register_reporter, report_error, resource_not_found, resource_already_exists, validation_error, permission_denied, business_logic_error, ensure_not_none, handle_exception, initialize, shutdown
from app.core.error.reporters import LoggingErrorReporter, DatabaseErrorReporter, ExternalServiceReporter
```

## Global Variables
```python
__all__ = __all__ = [
    # Base types
    "ErrorContext",
    "ErrorReporter",
    # Factory
    "ErrorReporterFactory",
    # Core functions
    "register_reporter",
    "report_error",
    "resource_not_found",
    "resource_already_exists",
    "validation_error",
    "permission_denied",
    "business_logic_error",
    "ensure_not_none",
    "handle_exception",
    "initialize",
    "shutdown",
    # Reporter implementations
    "LoggingErrorReporter",
    "DatabaseErrorReporter",
    "ExternalServiceReporter",
]
```
