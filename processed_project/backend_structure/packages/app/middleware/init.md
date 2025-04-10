# Module: app.middleware

**Path:** `app/middleware/__init__.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from app.middleware.request_context import RequestContextMiddleware
from app.middleware.tracing import TracingMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.middleware.timeout import TimeoutMiddleware
from app.middleware.compression import CompressionMiddleware
from app.middleware.security import SecurityHeadersMiddleware, SecureRequestMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.cache_control import CacheControlMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.cors import EnhancedCORSMiddleware
```

## Global Variables
```python
__all__ = __all__ = [
    "RequestContextMiddleware",
    "TracingMiddleware",
    "MetricsMiddleware",
    "TimeoutMiddleware",
    "CompressionMiddleware",
    "SecurityHeadersMiddleware",
    "SecureRequestMiddleware",
    "RateLimitMiddleware",
    "CacheControlMiddleware",
    "ResponseFormatterMiddleware",
    "ErrorHandlerMiddleware",
    "EnhancedCORSMiddleware",
]
```
