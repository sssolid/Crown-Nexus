# Module: app.main

**Path:** `app/main.py`

[Back to Project Index](../../index.md)

## Imports
```python
from __future__ import annotations
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Callable, Optional
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import AppException, app_exception_handler, validation_exception_handler, generic_exception_handler
from app.middleware.metrics import MetricsMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.request_context import RequestContextMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.middleware.security import SecurityHeadersMiddleware, SecureRequestMiddleware
from app.middleware.rate_limiting import RateLimitMiddleware
from app.api.deps import get_current_user
from app.core.config import Environment, settings
from app.core.logging import get_logger, request_context, set_user_id
from app.core.error import initialize as initialize_error_system, shutdown as shutdown_error_system
from app.core.validation import initialize as initialize_validation_system, shutdown as shutdown_validation_system
from app.core.metrics import initialize as initialize_metrics_system, shutdown as shutdown_metrics_system
from app.core.rate_limiting import initialize as initialize_ratelimiting_system, shutdown as shutdown_ratelimiting_system, RateLimitRule, RateLimitStrategy
from app.core.pagination import initialize as initialize_pagination_system, shutdown as shutdown_pagination_system
from app.core.dependency_manager import register_services, initialize_services, shutdown_services
from app.core.cache.manager import initialize_cache
from app.fitment.api import router as fitment_router
from app.fitment.dependencies import initialize_mapping_engine
from app.core.startup.as400_sync import initialize_as400_sync, shutdown_as400_sync
from app.models.user import User
import uvicorn
```

## Global Variables
```python
logger = logger = get_logger("app.main")
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
| `health_check` |  |
| `lifespan` |  |
| `log_current_user` |  |

### `health_check`
```python
@app.get('/health')
async def health_check() -> dict:
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
