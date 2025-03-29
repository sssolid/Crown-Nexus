# Module: app.main

**Path:** `app/main.py`

[Back to Project Index](../../index.md)

## Imports
```python
from __future__ import annotations
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator, Callable, Optional
import uvicorn
from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import reinitialize_logging, shutdown_logging, get_logger, set_user_id
import app.db.base
from app.api.deps import get_current_user
from app.core.cache.manager import initialize_cache
from app.core.config import Environment, settings
from app.core.dependency_manager import register_services, initialize_services, shutdown_services, get_service
from app.core.error import initialize as initialize_error_system, shutdown as shutdown_error_system
from app.core.events import EventBackendType, init_event_backend, init_domain_events, EventConfigurationException
from app.core.exceptions import AppException, app_exception_handler, validation_exception_handler, generic_exception_handler
from app.middleware.logging import RequestLoggingMiddleware
from app.core.metrics import initialize as initialize_metrics_system, shutdown as shutdown_metrics_system
from app.core.pagination import initialize as initialize_pagination_system, shutdown as shutdown_pagination_system
from app.core.rate_limiting import initialize as initialize_ratelimiting_system, shutdown as shutdown_ratelimiting_system, RateLimitRule, RateLimitStrategy
from app.core.startup.as400_sync import initialize_as400_sync, shutdown_as400_sync
from app.core.validation import initialize as initialize_validation_system, shutdown as shutdown_validation_system
from app.domains.users.models import User
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.middleware.security import SecurityHeadersMiddleware, SecureRequestMiddleware
```

## Global Variables
```python
logger = logger = get_logger("app.main")
ExceptionHandlerType = ExceptionHandlerType = Callable[[Request, Exception], Response | JSONResponse]
app = app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)
media_path = media_path = Path(settings.MEDIA_ROOT).resolve()
host = '0.0.0.0'
port = 8000
```

## Functions

| Function | Description |
| --- | --- |
| `add_typed_middleware` |  |
| `health_check` |  |
| `initialize_event_system` |  |
| `lifespan` |  |
| `log_current_user` |  |

### `add_typed_middleware`
```python
def add_typed_middleware(app, middleware_class, **options) -> None:
```

### `health_check`
```python
@app.get('/health')
async def health_check() -> dict:
```

### `initialize_event_system`
```python
def initialize_event_system() -> None:
```

### `lifespan`
```python
@asynccontextmanager
async def lifespan(app) -> AsyncGenerator[(None, None)]:
```

### `log_current_user`
```python
async def log_current_user(current_user) -> Optional[User]:
```
