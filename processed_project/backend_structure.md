# backend Project Structure
Generated on 2025-03-28 20:12:13

## Table of Contents
1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Packages and Modules](#packages-and-modules)

## Project Overview
- Project Name: backend
- Root Path: /home/runner/work/Crown-Nexus/Crown-Nexus/backend
- Packages: 2
- Top-level Modules: 0

## Directory Structure
```
backend/
├── alembic/
│   ├── versions/
│   │   └── __init__.py
│   ├── README
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── chat.py
│   │   │   │   ├── currency.py
│   │   │   │   ├── fitments.py
│   │   │   │   ├── i18n.py
│   │   │   │   ├── media.py
│   │   │   │   ├── products.py
│   │   │   │   ├── search.py
│   │   │   │   └── users.py
│   │   │   ├── __init__.py
│   │   │   └── router.py
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── responses.py
│   ├── commands/
│   │   ├── __init__.py
│   │   └── init_currencies.py
│   ├── core/
│   │   ├── cache/
│   │   │   ├── backends/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── memory.py
│   │   │   │   ├── null.py
│   │   │   │   └── redis.py
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── decorators.py
│   │   │   ├── exceptions.py
│   │   │   ├── keys.py
│   │   │   ├── manager.py
│   │   │   └── service.py
│   │   ├── config/
│   │   │   ├── integrations/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── as400.py
│   │   │   │   └── elasticsearch.py
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── celery.py
│   │   │   ├── currency.py
│   │   │   ├── database.py
│   │   │   ├── fitment.py
│   │   │   ├── media.py
│   │   │   ├── security.py
│   │   │   └── settings.py
│   │   ├── error/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── factory.py
│   │   │   ├── manager.py
│   │   │   ├── reporters.py
│   │   │   └── service.py
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   ├── backend.py
│   │   │   └── init.py
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── domain.py
│   │   │   ├── handlers.py
│   │   │   └── system.py
│   │   ├── metrics/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── collectors.py
│   │   │   ├── decorators.py
│   │   │   ├── exceptions.py
│   │   │   ├── manager.py
│   │   │   ├── prometheus.py
│   │   │   ├── service.py
│   │   │   └── trackers.py
│   │   ├── pagination/
│   │   │   ├── providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── cursor.py
│   │   │   │   └── offset.py
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── exceptions.py
│   │   │   ├── factory.py
│   │   │   ├── manager.py
│   │   │   └── service.py
│   │   ├── permissions/
│   │   │   ├── __init__.py
│   │   │   ├── checker.py
│   │   │   ├── decorators.py
│   │   │   ├── models.py
│   │   │   ├── permissions.py
│   │   │   └── utils.py
│   │   ├── rate_limiting/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── limiter.py
│   │   │   ├── models.py
│   │   │   ├── rate_limiter.py
│   │   │   ├── service.py
│   │   │   └── utils.py
│   │   ├── security/
│   │   │   ├── __init__.py
│   │   │   ├── api_keys.py
│   │   │   ├── csrf.py
│   │   │   ├── dependencies.py
│   │   │   ├── encryption.py
│   │   │   ├── models.py
│   │   │   ├── passwords.py
│   │   │   ├── tokens.py
│   │   │   └── validation.py
│   │   ├── startup/
│   │   │   ├── __init__.py
│   │   │   └── as400_sync.py
│   │   ├── validation/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── db.py
│   │   │   ├── factory.py
│   │   │   ├── manager.py
│   │   │   ├── service.py
│   │   │   └── validators.py
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── celeryconfig.py
│   │   ├── dependency_manager.py
│   │   └── dependency_manager.pyi
│   ├── data_import/
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── import_products.py
│   │   │   └── sync_as400.py
│   │   ├── connectors/
│   │   │   ├── __init__.py
│   │   │   ├── as400_connector.py
│   │   │   ├── base.py
│   │   │   ├── file_connector.py
│   │   │   └── filemaker_connector.py
│   │   ├── importers/
│   │   │   ├── __init__.py
│   │   │   ├── as400_importers.py
│   │   │   ├── base.py
│   │   │   └── product_importer.py
│   │   ├── pipeline/
│   │   │   ├── __init__.py
│   │   │   ├── as400_pipeline.py
│   │   │   ├── base.py
│   │   │   └── product_pipeline.py
│   │   ├── processors/
│   │   │   ├── __init__.py
│   │   │   ├── as400_processor.py
│   │   │   ├── base.py
│   │   │   └── product_processor.py
│   │   └── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── base_class.py
│   │   ├── session.py
│   │   └── utils.py
│   ├── domains/
│   │   ├── api_key/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── audit/
│   │   │   ├── service/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── factory.py
│   │   │   │   ├── loggers.py
│   │   │   │   ├── query.py
│   │   │   │   └── service.py
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── autocare/
│   │   │   ├── fitment/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── padb/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── pcdb/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── qdb/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── vcdb/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── chat/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   ├── service_DUPLICATEMAYBE.py
│   │   │   ├── tasks.py
│   │   │   └── websocket.py
│   │   ├── company/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── compliance/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── currency/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── tasks.py
│   │   ├── fitment/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── inventory/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── location/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── media/
│   │   │   ├── service/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── factory.py
│   │   │   │   ├── local.py
│   │   │   │   ├── s3.py
│   │   │   │   ├── service.py
│   │   │   │   └── thumbnails.py
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── model_mapping/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── products/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── reference/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── security/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── passwords.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── tokens.py
│   │   ├── sync_history/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── repository.py
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   └── __init__.py
│   ├── fitment/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── mapper.py
│   │   ├── models.py
│   │   ├── parser.py
│   │   └── validator.py
│   ├── i18n/
│   │   └── translations.py
│   ├── logging/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── context.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── error_handler.py
│   │   ├── logging.py
│   │   ├── metrics.py
│   │   ├── rate_limiting.py
│   │   ├── request_context.py
│   │   ├── response_formatter.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── associations.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── services/
│   │   ├── base_service/
│   │   │   ├── operations/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_update.py
│   │   │   │   └── read_delete.py
│   │   │   ├── __init__.py
│   │   │   ├── contracts.py
│   │   │   ├── permissions.py
│   │   │   └── service.py
│   │   ├── search/
│   │   │   ├── providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── database.py
│   │   │   │   └── elasticsearch.py
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── factory.py
│   │   │   └── service.py
│   │   ├── __init__.py
│   │   ├── as400_sync_service.py
│   │   ├── interfaces.py
│   │   ├── test_service.py
│   │   └── vehicle.py
│   ├── tasks/
│   │   └── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── circuit_breaker.py
│   │   ├── crypto.py
│   │   ├── file.py
│   │   ├── redis_manager.py
│   │   └── retry.py
│   ├── __init__.py
│   ├── as400_integration.md
│   └── main.py
├── autocare/
│   ├── ACES.xsd
│   ├── PAdb_schema.sql
│   ├── PCAdb_schema.sql
│   ├── PCdb_schema.sql
│   ├── PIES.xsd
│   ├── Qdb_schema.sql
│   └── VCdb_light_power_schema.sql
├── scripts/
│   ├── auto_translate.py
│   ├── bootstrap_countries.py
│   ├── database_bootstrap.py
│   ├── extract_messages.py
│   ├── init_db.py
│   └── reset_db.py
├── tests/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_products.py
│   │   │   └── test_users.py
│   │   └── __init__.py
│   ├── integration/
│   │   ├── test_api/
│   │   │   ├── test_auth.py
│   │   │   └── test_products.py
│   │   └── test_as400_sync.py
│   ├── unit/
│   │   ├── test_config.py
│   │   └── test_db.py
│   ├── utils/
│   │   └── factories.py
│   ├── __init__.py
│   ├── conftest.py
│   └── utils.py
├── DEVELOPERS_GUIDE.md
├── README.md
├── alembic.ini
├── backend.iml
├── pyproject.toml
├── pytest.ini
├── requirements.in
└── requirements.txt
```

## Packages and Modules
### Packages
### Package: app
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/__init__.py`

#### Module: main
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/main.py`

**Imports:**
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
from app.core.events import EventBackendType, init_event_backend, init_domain_events
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

**Global Variables:**
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

**Functions:**
```python
def add_typed_middleware(app, middleware_class, **options) -> None:
    """Add middleware with proper type annotations to avoid IDE warnings."""
```

```python
@app.get('/health')
async def health_check() -> dict:
    """Health check endpoint.  Returns: A dictionary with health status information"""
```

```python
@asynccontextmanager
async def lifespan(app) -> AsyncGenerator[(None, None)]:
    """Context manager for the application lifespan.

Handles initialization and shutdown of application components.

Args: app: The FastAPI application

Yields: None"""
```

```python
async def log_current_user(current_user) -> Optional[User]:
    """Dependency for logging the current user.

Args: current_user: The authenticated user

Returns: The authenticated user"""
```

#### Package: api
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/__init__.py`

##### Module: deps
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/deps.py`

**Imports:**
```python
from __future__ import annotations
from typing import Dict, List, Optional, Union, Callable
from app.core.security.dependencies import optional_oauth2_scheme
from app.domains.audit.service.service import AuditService
from fastapi import Depends, Query, WebSocket, status
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect
from app.core.exceptions import AuthenticationException, PermissionDeniedException, RateLimitException
from app.logging import get_logger, set_user_id
from app.core.permissions import Permission, PermissionChecker
from app.core.rate_limiting import RateLimiter, RateLimitRule
from app.core.security import decode_token, oauth2_scheme
from app.db.session import get_db
from app.domains.users.models import User, UserRole
from app.domains.users.repository import UserRepository
```

**Global Variables:**
```python
logger = logger = get_logger("app.api.deps")
PaginationParams = PaginationParams = Dict[str, Union[int, float]]
```

**Functions:**
```python
async def get_admin_user(current_user) -> User:
    """Get the current active admin user.

This dependency builds on get_current_active_user and ensures the user has admin role.

Args: current_user: Current authenticated user

Returns: User: Current active admin user

Raises: PermissionDeniedException: If user is not an admin"""
```

```python
async def get_audit_service(db) -> AuditService:
    """Get an instance of the audit service.

Args: db: Database session

Returns: AuditService: The audit service instance"""
```

```python
async def get_current_active_user(current_user) -> User:
    """Get the current active user.

This dependency builds on get_current_user and ensures the user is active in the system.

Args: current_user: Current authenticated user

Returns: User: Current active user

Raises: AuthenticationException: If user is inactive"""
```

```python
async def get_current_user(db, token) -> User:
    """Get the current authenticated user.

This dependency validates the JWT token, decodes it, and retrieves the corresponding user from the database.

Args: db: Database session token: JWT token

Returns: User: Authenticated user

Raises: AuthenticationException: If authentication fails"""
```

```python
async def get_current_user_ws(websocket, db) -> User:
    """Get the current authenticated user from WebSocket connection.

This dependency extracts the JWT token from WebSocket query parameters or cookies, validates it, and returns the corresponding user.

Args: websocket: WebSocket connection db: Database session

Returns: User: Authenticated user

Raises: WebSocketDisconnect: If authentication fails"""
```

```python
async def get_manager_user(current_user) -> User:
    """Get the current active manager or admin user.

This dependency builds on get_current_active_user and ensures the user has manager or admin role.

Args: current_user: Current authenticated user

Returns: User: Current active manager or admin user

Raises: PermissionDeniedException: If user is not a manager or admin"""
```

```python
async def get_optional_user(db, token) -> Optional[User]:
    """Get the current user if authenticated, otherwise None.

This dependency is useful for endpoints that can be accessed both by authenticated and anonymous users, with different behavior.

Args: db: Database session token: Optional JWT token

Returns: Optional[User]: Authenticated user or None"""
```

```python
def get_pagination(page, page_size) -> PaginationParams:
    """Get pagination parameters.

This dependency generates pagination parameters based on page number and size, with validation to ensure reasonable values.

Args: page: Page number (starting from 1) page_size: Number of items per page (max 100)

Returns: Dict: Pagination parameters"""
```

```python
def rate_limit(requests_per_window, window_seconds) -> Callable:
    """Rate limiting dependency for specific endpoints.

Args: requests_per_window: Number of allowed requests per window window_seconds: Time window in seconds

Returns: Callable: Dependency function"""
```

```python
def require_permission(permission):
    """Dependency to require a specific permission.

Args: permission: Required permission

Returns: Callable: Dependency function"""
```

```python
def require_permissions(permissions, require_all):
    """Dependency to require specific permissions.

Args: permissions: List of required permissions require_all: Whether all permissions are required (AND) or any (OR)

Returns: Callable: Dependency function"""
```

##### Module: responses
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/responses.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, TypeVar
from app.schemas.responses import Response, PaginatedResponse
from fastapi import status
from fastapi.responses import JSONResponse
```

**Global Variables:**
```python
T = T = TypeVar("T")
```

**Functions:**
```python
def created_response(data, message, meta, request_id) -> JSONResponse:
    """Create a 201 Created response.

Args: data: Response data message: Success message meta: Additional metadata request_id: Request ID for tracking

Returns: JSONResponse: Created response"""
```

```python
def error_response(message, code, data, meta, request_id) -> JSONResponse:
    """Create an error response.

Args: message: Error message code: HTTP status code data: Error data meta: Additional metadata request_id: Request ID for tracking

Returns: JSONResponse: Error response"""
```

```python
def no_content_response() -> JSONResponse:
    """Create a 204 No Content response.  Returns: JSONResponse: No content response"""
```

```python
def paginated_response(items, pagination, message, code, meta, request_id) -> JSONResponse:
    """Create a paginated response.

Args: items: List of items pagination: Pagination metadata message: Success message code: HTTP status code meta: Additional metadata request_id: Request ID for tracking

Returns: JSONResponse: Paginated response"""
```

```python
def success_response(data, message, code, meta, pagination, request_id) -> JSONResponse:
    """Create a success response.

Args: data: Response data message: Success message code: HTTP status code meta: Additional metadata pagination: Pagination metadata request_id: Request ID for tracking

Returns: JSONResponse: Success response"""
```

##### Package: v1
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/__init__.py`

###### Module: router
*API router configuration.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/router.py`

**Imports:**
```python
from __future__ import annotations
from fastapi import APIRouter
from app.api.v1.endpoints import auth, fitments, media, products, search, users
```

**Global Variables:**
```python
api_router = api_router = APIRouter()
```

###### Package: endpoints
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/__init__.py`

####### Module: auth
*Authentication API endpoints.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/auth.py`

**Imports:**
```python
from __future__ import annotations
from datetime import timedelta
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db
from app.core.config import settings
from app.domains.users.models import User, create_access_token, verify_password
from app.domains.users.schemas import Token, TokenPayload, User as UserSchema
```

**Global Variables:**
```python
router = router = APIRouter()
oauth2_scheme = oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
```

**Functions:**
```python
@router.post('/login', response_model=Token)
async def login_for_access_token(db, form_data) -> Any:
    """OAuth2 compatible token login endpoint.

This endpoint authenticates a user and provides a JWT access token for use in subsequent requests. It conforms to the OAuth2 password flow specification.

Args: db: Database session form_data: Form data with username (email) and password

Returns: Dict: JWT access token and type

Raises: HTTPException: If authentication fails due to invalid credentials or inactive user account"""
```

```python
@router.get('/me', response_model=UserSchema)
async def read_users_me(current_user) -> Any:
    """Get current user information.

This endpoint returns information about the currently authenticated user based on their JWT token.

Args: current_user: Current authenticated user (via dependency)

Returns: User: Current user information"""
```

```python
@router.get('/validate-token')
async def validate_token(token) -> dict:
    """Validate a JWT token.

This endpoint verifies if a token is valid and active. It's useful for client applications to check token validity without making a full API request.

Args: token: Decoded token payload (via dependency)

Returns: dict: Token validation status"""
```

####### Module: chat
*Chat API endpoints.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/chat.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.schemas.responses import Response
from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field, validator
from app.api.deps import get_current_active_user, get_db
from app.api.responses import created_response, error_response, success_response
from app.core.exceptions import BusinessException, ValidationException
from app.logging import get_logger, log_execution_time
from app.db.session import AsyncSession
from app.domains.chat.models import ChatMemberRole, ChatRoomType, MessageType
from app.domains.users.models import User
from app.core.dependency_manager import get_service
```

**Global Variables:**
```python
router = router = APIRouter()
logger = logger = get_logger("app.api.v1.endpoints.chat")
```

**Functions:**
```python
@router.post('/rooms/{room_id}/messages/{message_id}/reactions')
@log_execution_time(logger)
async def add_reaction(room_id, message_id, request, db, current_user) -> Response:
    """Add a reaction to a message.

Args: room_id: ID of the chat room message_id: ID of the message request: Reaction request data db: Database session current_user: Authenticated user making the request

Returns: Response with success status and message

Raises: HTTPException: If the message is not found or the user doesn't have access to the room"""
```

```python
@router.post('/rooms/{room_id}/members')
@log_execution_time(logger)
async def add_room_member(room_id, request, db, current_user) -> Response:
    """Add a member to a chat room.

Args: room_id: ID of the chat room request: Member addition request data db: Database session current_user: Authenticated user making the request

Returns: Response with success status and message

Raises: HTTPException: If validation fails, the room is not found, or the user lacks permissions"""
```

```python
@router.post('/direct-chats')
@log_execution_time(logger)
async def create_direct_chat(request, db, current_user) -> Response:
    """Create or get a direct chat between two users.

If a direct chat already exists between the users, it returns the existing chat. Otherwise, it creates a new direct chat.

Args: request: Direct chat creation request data db: Database session current_user: Authenticated user making the request

Returns: Response containing the direct chat room information

Raises: HTTPException: If the target user doesn't exist or an error occurs"""
```

```python
@router.post('/rooms/{room_id}/messages')
@log_execution_time(logger)
async def create_message(room_id, request, db, current_user) -> Response:
    """Create a new message in a chat room.

Args: room_id: ID of the chat room request: Message creation request data db: Database session current_user: Authenticated user making the request

Returns: Response containing the created message information

Raises: HTTPException: If the room is not found, the user doesn't have access, or validation fails"""
```

```python
@router.post('/rooms', status_code=status.HTTP_201_CREATED)
@log_execution_time(logger)
async def create_room(request, db, current_user) -> Response:
    """Create a new chat room.

Args: request: Room creation request data db: Database session current_user: Authenticated user making the request

Returns: Response with the created room information

Raises: HTTPException: If validation fails or an error occurs during room creation"""
```

```python
@router.delete('/rooms/{room_id}/messages/{message_id}')
@log_execution_time(logger)
async def delete_message(room_id, message_id, db, current_user) -> Response:
    """Delete a message.

Args: room_id: ID of the chat room message_id: ID of the message to delete db: Database session current_user: Authenticated user making the request

Returns: Response with success status and message

Raises: HTTPException: If the message is not found or the user doesn't have permission to delete it"""
```

```python
@router.put('/rooms/{room_id}/messages/{message_id}')
@log_execution_time(logger)
async def edit_message(room_id, message_id, request, db, current_user) -> Response:
    """Edit an existing message.

Args: room_id: ID of the chat room message_id: ID of the message to edit request: Message edit request data db: Database session current_user: Authenticated user making the request

Returns: Response with the updated message information

Raises: HTTPException: If the message is not found or the user doesn't have permission to edit it"""
```

```python
@router.get('/rooms/{room_id}')
@log_execution_time(logger)
async def get_room(room_id, db, current_user) -> Response:
    """Get a specific chat room by ID.

Args: room_id: ID of the chat room db: Database session current_user: Authenticated user making the request

Returns: Response containing the room information

Raises: HTTPException: If the room is not found or the user doesn't have access"""
```

```python
@router.get('/rooms/{room_id}/messages')
@log_execution_time(logger)
async def get_room_messages(room_id, before_id, limit, db, current_user) -> Response:
    """Get messages for a chat room.

Args: room_id: ID of the chat room before_id: Optional message ID to get messages before (for pagination) limit: Maximum number of messages to return db: Database session current_user: Authenticated user making the request

Returns: Response containing the list of messages

Raises: HTTPException: If the room is not found or the user doesn't have access"""
```

```python
@router.get('/rooms')
@log_execution_time(logger)
async def get_rooms(db, current_user) -> Response:
    """Get all chat rooms for the current user.

Args: db: Database session current_user: Authenticated user making the request

Returns: Response containing the list of rooms

Raises: HTTPException: If an error occurs during fetching rooms"""
```

```python
@router.delete('/rooms/{room_id}/messages/{message_id}/reactions/{reaction}')
@log_execution_time(logger)
async def remove_reaction(room_id, message_id, reaction, db, current_user) -> Response:
    """Remove a reaction from a message.

Args: room_id: ID of the chat room message_id: ID of the message reaction: Reaction emoji or code to remove db: Database session current_user: Authenticated user making the request

Returns: Response with success status and message

Raises: HTTPException: If the message is not found or the user doesn't have access to the room"""
```

```python
@router.delete('/rooms/{room_id}/members/{user_id}')
@log_execution_time(logger)
async def remove_room_member(room_id, user_id, db, current_user) -> Response:
    """Remove a member from a chat room.

Users can remove themselves (leave the room) or admins can remove any member. Owners can only be removed by other owners.

Args: room_id: ID of the chat room user_id: ID of the user to remove db: Database session current_user: Authenticated user making the request

Returns: Response with success status and message

Raises: HTTPException: If the room/member is not found or the user lacks permissions"""
```

```python
@router.put('/rooms/{room_id}/members/{user_id}')
@log_execution_time(logger)
async def update_room_member(room_id, user_id, request, db, current_user) -> Response:
    """Update a member's role in a chat room.

Args: room_id: ID of the chat room user_id: ID of the user to update request: Role update request data db: Database session current_user: Authenticated user making the request

Returns: Response with success status and message

Raises: HTTPException: If validation fails, the room/member is not found, or the user lacks permissions"""
```

**Classes:**
```python
class AddMemberRequest(BaseModel):
    """Request model for adding a member to a chat room."""
```
*Methods:*
```python
@validator('role')
    def validate_role(self, v) -> str:
        """Validate that the member role is valid.

Args: v: Role value to validate

Returns: The validated role

Raises: ValueError: If the role is not valid"""
```

```python
class CreateDirectChatRequest(BaseModel):
    """Request model for creating a direct chat between two users."""
```

```python
class CreateMessageRequest(BaseModel):
    """Request model for creating a new message."""
```
*Methods:*
```python
@validator('message_type')
    def validate_message_type(self, v) -> str:
        """Validate that the message type is valid.

Args: v: Message type value to validate

Returns: The validated message type

Raises: ValueError: If the message type is not valid"""
```

```python
class CreateRoomRequest(BaseModel):
    """Request model for creating a chat room."""
```
*Methods:*
```python
@validator('type')
    def validate_type(self, v) -> str:
        """Validate that the room type is valid.

Args: v: Room type value to validate

Returns: The validated room type

Raises: ValueError: If the room type is not valid"""
```

```python
class EditMessageRequest(BaseModel):
    """Request model for editing a message."""
```

```python
class ReactionRequest(BaseModel):
    """Request model for adding/removing a reaction to a message."""
```

```python
class UpdateMemberRequest(BaseModel):
    """Request model for updating a member's role in a chat room."""
```
*Methods:*
```python
@validator('role')
    def validate_role(self, v) -> str:
        """Validate that the member role is valid.

Args: v: Role value to validate

Returns: The validated role

Raises: ValueError: If the role is not valid"""
```

####### Module: currency
*Currency API endpoints.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/currency.py`

**Imports:**
```python
from __future__ import annotations
import datetime
from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.domains.currency.models import Currency, ExchangeRate
from app.domains.currency.schemas import ConversionRequest, ConversionResponse, CurrencyRead, ExchangeRateRead
from app.domains.currency.service import ExchangeRateService
from app.domains.currency.tasks import update_exchange_rates
from app.domains.users.models import User
```

**Global Variables:**
```python
router = router = APIRouter()
```

**Functions:**
```python
@router.post('/convert', response_model=ConversionResponse)
async def convert_currency(conversion, db, current_user) -> Any:
    """Convert an amount between currencies.

Args: conversion: Conversion request parameters db: Database session current_user: Current authenticated user

Returns: ConversionResponse: Conversion result

Raises: HTTPException: If currencies not found or conversion fails"""
```

```python
@router.get('/', response_model=List[CurrencyRead])
async def read_currencies(db, current_user, active_only) -> Any:
    """Get list of available currencies.

Args: db: Database session current_user: Current authenticated user active_only: Whether to return only active currencies (default: True)

Returns: List[CurrencyRead]: List of currencies"""
```

```python
@router.get('/rates', response_model=List[ExchangeRateRead])
async def read_exchange_rates(db, current_user, source_code, target_code, limit) -> Any:
    """Get exchange rates with optional filtering.

Args: db: Database session current_user: Current authenticated user source_code: Source currency code target_code: Target currency code limit: Maximum number of rates to return (default: 10)

Returns: List[ExchangeRateRead]: List of exchange rates"""
```

```python
@router.post('/update', status_code=status.HTTP_202_ACCEPTED)
async def trigger_exchange_rate_update(background_tasks, db, current_user, async_update) -> Dict[(str, Any)]:
    """Trigger an update of exchange rates.

Args: background_tasks: Background tasks db: Database session current_user: Current authenticated admin user async_update: Whether to update asynchronously or wait for completion

Returns: Dict[str, Any]: Result of the operation

Raises: HTTPException: If update fails"""
```

####### Module: fitments
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/fitments.py`

**Imports:**
```python
from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.domains.products.models import Fitment, Product, product_fitment_association
from app.domains.products.schemas import Fitment as FitmentSchema, FitmentCreate, FitmentListResponse, FitmentUpdate, Product as ProductSchema
from app.domains.users.models import User
```

**Global Variables:**
```python
router = router = APIRouter()
```

**Functions:**
```python
@router.post('/{fitment_id}/products/{product_id}')
async def associate_product_with_fitment(fitment_id, product_id, db, current_user) -> dict:
    """Associate a product with a fitment.

Args: fitment_id: Fitment ID product_id: Product ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.post('/', response_model=FitmentSchema, status_code=status.HTTP_201_CREATED)
async def create_fitment(db, fitment_in, current_user) -> Any:
    """Create new fitment.

Args: db: Database session fitment_in: Fitment data current_user: Current authenticated admin user

Returns: Fitment: Created fitment"""
```

```python
@router.delete('/{fitment_id}')
async def delete_fitment(fitment_id, db, current_user) -> dict:
    """Delete a fitment.

Args: fitment_id: Fitment ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.get('/{fitment_id}', response_model=FitmentSchema)
async def read_fitment(fitment_id, db, current_user) -> Any:
    """Get fitment by ID.

Args: fitment_id: Fitment ID db: Database session current_user: Current authenticated user

Returns: Fitment: Fitment with specified ID"""
```

```python
@router.get('/{fitment_id}/products', response_model=List[ProductSchema])
async def read_fitment_products(fitment_id, db, current_user, skip, limit) -> Any:
    """Get products associated with a fitment.

Args: fitment_id: Fitment ID db: Database session current_user: Current authenticated user skip: Number of products to skip limit: Maximum number of products to return

Returns: List[Product]: List of products associated with the fitment"""
```

```python
@router.get('/', response_model=FitmentListResponse)
async def read_fitments(db, current_user, year, make, model, engine, transmission, page, page_size) -> Any:
    """Retrieve fitments with filtering options.

Args: db: Database session current_user: Current authenticated user year: Filter by year make: Filter by make model: Filter by model engine: Filter by engine transmission: Filter by transmission page: Page number page_size: Number of items per page

Returns: FitmentListResponse: Paginated list of fitments"""
```

```python
@router.delete('/{fitment_id}/products/{product_id}')
async def remove_product_from_fitment(fitment_id, product_id, db, current_user) -> dict:
    """Remove association between a product and a fitment.

Args: fitment_id: Fitment ID product_id: Product ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.put('/{fitment_id}', response_model=FitmentSchema)
async def update_fitment(fitment_id, fitment_in, db, current_user) -> Any:
    """Update a fitment.

Args: fitment_id: Fitment ID fitment_in: Updated fitment data db: Database session current_user: Current authenticated admin user

Returns: Fitment: Updated fitment"""
```

####### Module: i18n
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/i18n.py`

**Imports:**
```python
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException, Path, status
from app.i18n.translations import i18n_manager, get_locale
```

**Global Variables:**
```python
router = router = APIRouter()
```

**Functions:**
```python
@router.get('/current-locale')
async def get_current_locale(locale) -> Dict[(str, str)]:
    """Get the current locale based on the request.

Args: locale: Current locale from dependency

Returns: Dict[str, str]: Current locale information"""
```

```python
@router.get('/messages/{locale}')
async def get_messages(locale) -> Dict[(str, Dict[(str, str)])]:
    """Get all translation messages for a specific locale.

Args: locale: Locale code (e.g., 'en', 'es')

Returns: Dict[str, Dict[str, str]]: Translation messages for the requested locale"""
```

####### Module: media
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/media.py`

**Imports:**
```python
from __future__ import annotations
import json
import os
from datetime import datetime
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination, get_optional_user
from app.domains.media.models import Media, MediaType, MediaVisibility
from app.domains.media.schemas import FileUploadResponse, Media as MediaSchema, MediaListResponse, MediaUpdate
from app.domains.products.models import Product, product_media_association
from app.domains.users.models import User
from app.utils.file import get_file_path, get_thumbnail_path, save_upload_file, validate_file
```

**Global Variables:**
```python
router = router = APIRouter()
```

**Functions:**
```python
@router.post('/{media_id}/products/{product_id}')
async def associate_media_with_product(media_id, product_id, db, current_user) -> dict:
    """Associate media with a product.

Args: media_id: Media ID product_id: Product ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.delete('/{media_id}')
async def delete_media(media_id, db, current_user) -> dict:
    """Delete media.

Args: media_id: Media ID db: Database session current_user: Current authenticated user

Returns: dict: Success message"""
```

```python
@router.get('/file/{media_id}')
async def get_media_file(media_id, db, current_user) -> Any:
    """Get the file for media.

Args: media_id: Media ID db: Database session current_user: Current authenticated user (optional for public files)

Returns: FileResponse: Media file"""
```

```python
@router.get('/thumbnail/{media_id}')
async def get_media_thumbnail(media_id, db, current_user) -> Any:
    """Get the thumbnail for an image.

Args: media_id: Media ID db: Database session current_user: Current authenticated user (optional for public files)

Returns: FileResponse: Thumbnail file or original file if thumbnail doesn't exist"""
```

```python
@router.get('/products/{product_id}', response_model=List[MediaSchema])
async def get_product_media(product_id, db, current_user, media_type) -> Any:
    """Get media associated with a product.

Args: product_id: Product ID db: Database session current_user: Current authenticated user media_type: Filter by media type

Returns: List[Media]: List of media associated with the product"""
```

```python
@router.get('/', response_model=MediaListResponse)
async def read_media(db, current_user, media_type, visibility, is_approved, product_id, page, page_size) -> Any:
    """Retrieve media with filtering options.

Args: db: Database session current_user: Current authenticated user media_type: Filter by media type visibility: Filter by visibility is_approved: Filter by approval status product_id: Filter by associated product page: Page number page_size: Number of items per page

Returns: MediaListResponse: Paginated list of media"""
```

```python
@router.get('/{media_id}', response_model=MediaSchema)
async def read_media_item(media_id, db, current_user) -> Any:
    """Get media by ID.

Args: media_id: Media ID db: Database session current_user: Current authenticated user

Returns: Media: Media with specified ID"""
```

```python
@router.delete('/{media_id}/products/{product_id}')
async def remove_media_from_product(media_id, product_id, db, current_user) -> dict:
    """Remove association between media and a product.

Args: media_id: Media ID product_id: Product ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.put('/{media_id}', response_model=MediaSchema)
async def update_media(media_id, media_in, db, current_user) -> Any:
    """Update media metadata.

Args: media_id: Media ID media_in: Updated media data db: Database session current_user: Current authenticated user

Returns: Media: Updated media"""
```

```python
@router.post('/upload', response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(background_tasks, db, current_user, file, media_type, visibility, metadata, product_id) -> Any:
    """Upload a new file.

Args: background_tasks: Background tasks db: Database session current_user: Current authenticated user file: Uploaded file media_type: Type of media visibility: Visibility level metadata: Additional metadata as JSON string product_id: ID of product to associate with the media

Returns: FileUploadResponse: Response with the created media"""
```

####### Module: products
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/products.py`

**Imports:**
```python
from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.domains.products.models import Brand, Product, ProductActivity, ProductBrandHistory, ProductDescription, ProductMarketing, ProductMeasurement, ProductStock, ProductSupersession
from app.domains.products.schemas import Brand as BrandSchema, BrandCreate, BrandUpdate, Product as ProductSchema, ProductCreate, ProductDescription as ProductDescriptionSchema, ProductDescriptionCreate, ProductDescriptionUpdate, ProductListResponse, ProductMarketing as ProductMarketingSchema, ProductMarketingCreate, ProductMarketingUpdate, ProductMeasurement as ProductMeasurementSchema, ProductMeasurementCreate, ProductStatus, ProductStock as ProductStockSchema, ProductStockCreate, ProductStockUpdate, ProductSupersession as ProductSupersessionSchema, ProductSupersessionCreate, ProductUpdate
from app.domains.reference.models import Warehouse
from app.domains.users.models import User
```

**Global Variables:**
```python
router = router = APIRouter()
```

**Functions:**
```python
@router.post('/brands/', response_model=BrandSchema, status_code=status.HTTP_201_CREATED)
async def create_brand(db, brand_in, current_user) -> Any:
    """Create new brand.

Args: db: Database session brand_in: Brand data current_user: Current authenticated admin user

Returns: Brand: Created brand"""
```

```python
@router.post('/', response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(db, product_in, current_user) -> Any:
    """Create new product.

Args: db: Database session product_in: Product data current_user: Current authenticated admin user

Returns: Product: Created product"""
```

```python
@router.post('/{product_id}/descriptions', response_model=ProductDescriptionSchema)
async def create_product_description(product_id, description_in, db, current_user) -> Any:
    """Add a description to a product.

Args: product_id: Product ID description_in: Description data db: Database session current_user: Current authenticated admin user

Returns: ProductDescription: Created description"""
```

```python
@router.post('/{product_id}/marketing', response_model=ProductMarketingSchema)
async def create_product_marketing(product_id, marketing_in, db, current_user) -> Any:
    """Add marketing content to a product.

Args: product_id: Product ID marketing_in: Marketing data db: Database session current_user: Current authenticated admin user

Returns: ProductMarketing: Created marketing content"""
```

```python
@router.post('/{product_id}/measurements', response_model=ProductMeasurementSchema)
async def create_product_measurement(product_id, measurement_in, db, current_user) -> Any:
    """Add measurements to a product.

Args: product_id: Product ID measurement_in: Measurement data db: Database session current_user: Current authenticated admin user

Returns: ProductMeasurement: Created measurement"""
```

```python
@router.post('/{product_id}/stock', response_model=ProductStockSchema)
async def create_product_stock(product_id, stock_in, db, current_user) -> Any:
    """Add stock information to a product.

Args: product_id: Product ID stock_in: Stock data db: Database session current_user: Current authenticated admin user

Returns: ProductStock: Created stock information"""
```

```python
@router.post('/{product_id}/supersessions', response_model=ProductSupersessionSchema)
async def create_product_supersession(product_id, supersession_in, db, current_user) -> Any:
    """Create a product supersession.

Args: product_id: Product ID supersession_in: Supersession data db: Database session current_user: Current authenticated admin user

Returns: ProductSupersession: Created supersession"""
```

```python
@router.delete('/brands/{brand_id}')
async def delete_brand(brand_id, db, current_user) -> dict:
    """Delete a brand.

Args: brand_id: Brand ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.delete('/{product_id}')
async def delete_product(product_id, db, current_user) -> dict:
    """Delete a product.

Args: product_id: Product ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.delete('/{product_id}/descriptions/{description_id}')
async def delete_product_description(product_id, description_id, db, current_user) -> dict:
    """Delete a product description.

Args: product_id: Product ID description_id: Description ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.delete('/{product_id}/marketing/{marketing_id}')
async def delete_product_marketing(product_id, marketing_id, db, current_user) -> dict:
    """Delete product marketing content.

Args: product_id: Product ID marketing_id: Marketing content ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.delete('/{product_id}/stock/{stock_id}')
async def delete_product_stock(product_id, stock_id, db, current_user) -> dict:
    """Delete product stock information.

Args: product_id: Product ID stock_id: Stock ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.delete('/{product_id}/supersessions/{supersession_id}')
async def delete_product_supersession(product_id, supersession_id, db, current_user) -> dict:
    """Delete a product supersession.

Args: product_id: Product ID supersession_id: Supersession ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message"""
```

```python
@router.get('/brands/{brand_id}', response_model=BrandSchema)
async def read_brand(brand_id, db, current_user) -> Any:
    """Get brand by ID.

Args: brand_id: Brand ID db: Database session current_user: Current authenticated user

Returns: Brand: Brand with specified ID"""
```

```python
@router.get('/brands/', response_model=List[BrandSchema])
async def read_brands(db, current_user, skip, limit) -> Any:
    """Retrieve brands.

Args: db: Database session current_user: Current authenticated user skip: Number of brands to skip limit: Maximum number of brands to return

Returns: List[Brand]: List of brands"""
```

```python
@router.get('/{product_id}', response_model=ProductSchema)
async def read_product(product_id, db, current_user) -> Any:
    """Get product by ID.

Args: product_id: Product ID db: Database session current_user: Current authenticated user

Returns: Product: Product with specified ID"""
```

```python
@router.get('/', response_model=ProductListResponse)
async def read_products(db, current_user, search, vintage, late_model, soft, universal, is_active, skip, limit, page, page_size) -> Any:
    """Retrieve products with filtering.

Args: db: Database session current_user: Current authenticated user search: Search term for product part number or application vintage: Filter by vintage flag late_model: Filter by late model flag soft: Filter by soft good flag universal: Filter by universal fit flag is_active: Filter by active status skip: Number of products to skip limit: Maximum number of products to return page: Page number page_size: Number of items per page

Returns: ProductListResponse: Paginated list of products"""
```

```python
@router.put('/brands/{brand_id}', response_model=BrandSchema)
async def update_brand(brand_id, brand_in, db, current_user) -> Any:
    """Update a brand.

Args: brand_id: Brand ID brand_in: Updated brand data db: Database session current_user: Current authenticated admin user

Returns: Brand: Updated brand"""
```

```python
@router.put('/{product_id}', response_model=ProductSchema)
async def update_product(product_id, product_in, db, current_user) -> Any:
    """Update a product.

Args: product_id: Product ID product_in: Updated product data db: Database session current_user: Current authenticated admin user

Returns: Product: Updated product"""
```

```python
@router.put('/{product_id}/descriptions/{description_id}', response_model=ProductDescriptionSchema)
async def update_product_description(product_id, description_id, description_in, db, current_user) -> Any:
    """Update a product description.

Args: product_id: Product ID description_id: Description ID description_in: Updated description data db: Database session current_user: Current authenticated admin user

Returns: ProductDescription: Updated description"""
```

```python
@router.put('/{product_id}/marketing/{marketing_id}', response_model=ProductMarketingSchema)
async def update_product_marketing(product_id, marketing_id, marketing_in, db, current_user) -> Any:
    """Update product marketing content.

Args: product_id: Product ID marketing_id: Marketing content ID marketing_in: Updated marketing data db: Database session current_user: Current authenticated admin user

Returns: ProductMarketing: Updated marketing content"""
```

```python
@router.put('/{product_id}/stock/{stock_id}', response_model=ProductStockSchema)
async def update_product_stock(product_id, stock_id, stock_in, db, current_user) -> Any:
    """Update product stock information.

Args: product_id: Product ID stock_id: Stock ID stock_in: Updated stock data db: Database session current_user: Current authenticated admin user

Returns: ProductStock: Updated stock information"""
```

####### Module: search
*Global search API endpoints.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/search.py`

**Imports:**
```python
from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db
from app.domains.users.models import User
from app.services.search import SearchService, get_search_service
from app.services.vehicle import VehicleDataService, get_vehicle_service
```

**Global Variables:**
```python
router = router = APIRouter()
```

**Functions:**
```python
@router.get('/vehicle-data/decode-vin/{vin}')
async def decode_vin(vin, db, current_user, vehicle_service) -> Any:
    """Decode a Vehicle Identification Number (VIN).

Args: vin: Vehicle Identification Number db: Database session current_user: Current authenticated user vehicle_service: Vehicle data service

Returns: Dict[str, Any]: Decoded vehicle data"""
```

```python
@router.get('/vehicle-data/engines')
async def get_vehicle_engines(db, current_user, vehicle_service, make, model, year) -> List[str]:
    """Get all available vehicle engines.

Args: db: Database session current_user: Current authenticated user vehicle_service: Vehicle data service make: Filter by make model: Filter by model year: Filter by year

Returns: List[str]: List of engines"""
```

```python
@router.get('/vehicle-data/makes')
async def get_vehicle_makes(db, current_user, vehicle_service, year) -> List[str]:
    """Get all available vehicle makes.

Args: db: Database session current_user: Current authenticated user vehicle_service: Vehicle data service year: Filter by year

Returns: List[str]: List of makes"""
```

```python
@router.get('/vehicle-data/models')
async def get_vehicle_models(db, current_user, vehicle_service, make, year) -> List[str]:
    """Get all available vehicle models.

Args: db: Database session current_user: Current authenticated user vehicle_service: Vehicle data service make: Filter by make year: Filter by year

Returns: List[str]: List of models"""
```

```python
@router.get('/vehicle-data/transmissions')
async def get_vehicle_transmissions(db, current_user, vehicle_service, make, model, year, engine) -> List[str]:
    """Get all available vehicle transmissions.

Args: db: Database session current_user: Current authenticated user vehicle_service: Vehicle data service make: Filter by make model: Filter by model year: Filter by year engine: Filter by engine

Returns: List[str]: List of transmissions"""
```

```python
@router.get('/vehicle-data/years')
async def get_vehicle_years(db, current_user, vehicle_service) -> List[int]:
    """Get all available vehicle years.

Args: db: Database session current_user: Current authenticated user vehicle_service: Vehicle data service

Returns: List[int]: List of years"""
```

```python
@router.get('/')
async def global_search(db, current_user, search_service, q, entity_types, page, page_size) -> Any:
    """Perform a global search across multiple entity types.

Args: db: Database session current_user: Current authenticated user search_service: Search service q: Search query entity_types: Entity types to search page: Page number page_size: Items per page

Returns: Dict[str, Any]: Search results grouped by entity type"""
```

```python
@router.get('/fitments')
async def search_fitments(db, current_user, search_service, q, year, make, model, engine, transmission, page, page_size) -> Any:
    """Search for fitments with filtering.

Args: db: Database session current_user: Current authenticated user search_service: Search service q: Search query year: Vehicle year filter make: Vehicle make filter model: Vehicle model filter engine: Vehicle engine filter transmission: Vehicle transmission filter page: Page number page_size: Items per page

Returns: Dict[str, Any]: Search results with pagination"""
```

```python
@router.get('/products')
async def search_products(db, current_user, search_service, q, is_active, page, page_size, use_elasticsearch) -> Any:
    """Search for products with filtering.

Args: db: Database session current_user: Current authenticated user search_service: Search service q: Search query is_active: Active status filter page: Page number page_size: Items per page use_elasticsearch: Whether to use Elasticsearch

Returns: Dict[str, Any]: Search results with pagination"""
```

```python
@router.post('/vehicle-data/validate-fitment')
async def validate_vehicle_fitment(db, current_user, vehicle_service, year, make, model, engine, transmission) -> dict:
    """Validate if a fitment combination exists.

Args: db: Database session current_user: Current authenticated user vehicle_service: Vehicle data service year: Vehicle year make: Vehicle make model: Vehicle model engine: Vehicle engine transmission: Vehicle transmission

Returns: dict: Validation result"""
```

####### Module: users
*User management API endpoints.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/users.py`

**Imports:**
```python
from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.domains.company.models import Company
from app.domains.company.schemas import CompanyCreate, CompanyUpdate
from app.domains.users.models import User, UserRole, get_password_hash
from app.domains.users.schemas import Company as CompanySchema, User as UserSchema, UserCreate, UserUpdate
```

**Global Variables:**
```python
router = router = APIRouter()
```

**Functions:**
```python
@router.post('/companies/', response_model=CompanySchema, status_code=status.HTTP_201_CREATED)
async def create_company(company_in, db, current_user) -> Any:
    """Create new company.

Args: company_in: Company data db: Database session current_user: Current authenticated admin user

Returns: Company: Created company

Raises: HTTPException: If account number already exists"""
```

```python
@router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_in, db, current_user) -> Any:
    """Create new user.

Args: user_in: User data db: Database session current_user: Current authenticated admin user

Returns: User: Created user

Raises: HTTPException: If email already exists or company not found"""
```

```python
@router.delete('/companies/{company_id}')
async def delete_company(company_id, db, current_user) -> dict:
    """Delete a company.

Args: company_id: Company ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message

Raises: HTTPException: If company not found or has associated users"""
```

```python
@router.delete('/{user_id}')
async def delete_user(user_id, db, current_user) -> dict:
    """Delete a user.

Args: user_id: User ID db: Database session current_user: Current authenticated admin user

Returns: dict: Success message

Raises: HTTPException: If user not found or is the current user"""
```

```python
@router.get('/companies/', response_model=List[CompanySchema])
async def read_companies(db, current_user, skip, limit, is_active) -> Any:
    """Retrieve companies with filtering options.

Args: db: Database session current_user: Current authenticated admin user skip: Number of companies to skip limit: Maximum number of companies to return is_active: Filter by active status

Returns: List[Company]: List of companies"""
```

```python
@router.get('/companies/{company_id}', response_model=CompanySchema)
async def read_company(company_id, db, current_user) -> Any:
    """Get company by ID.

Args: company_id: Company ID db: Database session current_user: Current authenticated admin user

Returns: Company: Company with specified ID

Raises: HTTPException: If company not found"""
```

```python
@router.get('/{user_id}', response_model=UserSchema)
async def read_user(user_id, db, current_user) -> Any:
    """Get user by ID.

Args: user_id: User ID db: Database session current_user: Current authenticated admin user

Returns: User: User with specified ID

Raises: HTTPException: If user not found"""
```

```python
@router.get('/me', response_model=UserSchema)
async def read_user_me(current_user, db) -> Any:
    """Get current user.

Args: current_user: Current authenticated user db: Database session

Returns: User: Current user with company information"""
```

```python
@router.get('/', response_model=List[UserSchema])
async def read_users(db, current_user, skip, limit, role, company_id, is_active) -> Any:
    """Retrieve users with filtering options.

Args: db: Database session current_user: Current authenticated admin user skip: Number of users to skip limit: Maximum number of users to return role: Filter by user role company_id: Filter by company ID is_active: Filter by active status

Returns: List[User]: List of users"""
```

```python
@router.put('/companies/{company_id}', response_model=CompanySchema)
async def update_company(company_id, company_in, db, current_user) -> Any:
    """Update a company.

Args: company_id: Company ID company_in: Updated company data db: Database session current_user: Current authenticated admin user

Returns: Company: Updated company

Raises: HTTPException: If company not found or account number already exists"""
```

```python
@router.put('/{user_id}', response_model=UserSchema)
async def update_user(user_id, user_in, db, current_user) -> Any:
    """Update a user.

Args: user_id: User ID user_in: Updated user data db: Database session current_user: Current authenticated admin user

Returns: User: Updated user

Raises: HTTPException: If user not found or company not found"""
```

#### Package: commands
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/commands`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/commands/__init__.py`

##### Module: init_currencies
*Command to initialize currencies in the database.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/commands/init_currencies.py`

**Imports:**
```python
import asyncio
import typer
from sqlalchemy import select
from app.db.session import get_db_context
from app.domains.currency.models import Currency
from app.domains.currency.tasks import init_currencies as init_currencies_task
```

**Global Variables:**
```python
app = app = typer.Typer()
```

**Functions:**
```python
@app.command()
def init_currencies(force, sync, base_currency):
    """Initialize currencies in the database."""
```

#### Package: core
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/__init__.py`

##### Module: celery_app
*Celery configuration.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/celery_app.py`

**Imports:**
```python
from __future__ import annotations
import os
from celery import Celery
from celery.schedules import crontab
```

**Global Variables:**
```python
celery_app = celery_app = Celery("crown_nexus")
```

**Functions:**
```python
def get_celery_app() -> Celery:
    """Get the Celery application instance."""
```

##### Module: celeryconfig
*Celery configuration settings.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/celeryconfig.py`

**Imports:**
```python
from __future__ import annotations
from kombu import Exchange, Queue
from app.core.config import settings
```

**Global Variables:**
```python
broker_url = broker_url = settings.CELERY_BROKER_URL
result_backend = result_backend = settings.CELERY_RESULT_BACKEND
task_serializer = 'json'
accept_content = accept_content = ["json"]
result_serializer = 'json'
enable_utc = True
timezone = 'UTC'
task_acks_late = True
task_reject_on_worker_lost = True
task_time_limit = 1800
task_soft_time_limit = 1500
worker_prefetch_multiplier = 1
worker_concurrency = 4
worker_max_tasks_per_child = 100
task_default_queue = 'default'
task_queues = task_queues = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("currency", Exchange("currency"), routing_key="currency"),
)
task_routes = task_routes = {
    "app.tasks.currency_tasks.*": {"queue": "currency"},
}
beat_schedule_filename = 'celerybeat-schedule'
```

##### Module: dependency_manager
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/dependency_manager.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import functools
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set, Type, TypeVar, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConfigurationException
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.dependency_manager")
T = T = TypeVar("T")
dependency_manager = dependency_manager = DependencyManager()
```

**Functions:**
```python
def get_dependency(name, **kwargs) -> Any:
    """Get a dependency by name.

Args: name: Name of the dependency **kwargs: Additional arguments to pass to the service provider

Returns: The dependency instance"""
```

```python
def get_service(service_name, db) -> Any:
    """Get a service by name.

Args: service_name: Name of the service to retrieve db: Optional database session to pass to the service provider

Returns: The service instance with the following type mappings: - "error_service" -> ErrorService - "user_service" -> UserService - "audit_service" -> AuditService - "search_service" -> SearchService - "media_service" -> MediaService

Examples: ```python # Get error service (returns ErrorService) error_service = get_service("error_service")

# Get user service with DB session (returns UserService) user_service = get_service("user_service", db=session) ```"""
```

```python
async def initialize_services() -> None:
    """Initialize all registered services."""
```

```python
def inject_dependency(dependency_name) -> Callable:
    """Decorator for injecting dependencies into functions.

Args: dependency_name: Name of the dependency to inject

Returns: Decorator function"""
```

```python
def register_async_service(async_provider, name) -> Callable[(Ellipsis, Awaitable[T])]:
    """Register an async service provider.

Args: async_provider: Async function that creates the service name: Optional name for the service (defaults to function name)

Returns: The original async provider function"""
```

```python
def register_service(provider, name) -> Callable[(Ellipsis, Any)]:
    """Decorator to register a service provider.

Args: provider: Function that creates the service name: Optional name for the service (defaults to function name)

Returns: The original provider function"""
```

```python
def register_services() -> None:
    """Register all application services with the dependency manager."""
```

```python
async def shutdown_services() -> None:
    """Shut down all services."""
```

```python
def with_dependencies(**dependencies) -> Callable:
    """Decorator for injecting multiple dependencies into a function.

Args: **dependencies: Mapping of parameter names to dependency names

Returns: Decorator function"""
```

**Classes:**
```python
class DependencyManager(object):
    """Singleton manager for application dependencies and services."""
```
*Methods:*
```python
    def __new__(cls) -> DependencyManager:
        """Create a new singleton instance if one doesn't exist."""
```
```python
    def clear(self) -> None:
        """Clear all dependency instances."""
```
```python
    def clear_instance(self, name) -> None:
        """Clear a specific dependency instance.  Args: name: Name of the dependency to clear"""
```
```python
    def get(self, name, **kwargs) -> Any:
        """Get or create a dependency by name.

Args: name: Name of the dependency **kwargs: Additional arguments to pass to the service provider

Returns: The dependency instance

Raises: ConfigurationException: If the dependency is not registered"""
```
```python
    def get_all(self, db) -> Dict[(str, Any)]:
        """Get all available services.

Args: db: Optional database session to pass to service providers

Returns: Dictionary of service name to service instance"""
```
```python
    def get_instance(self, cls, **kwargs) -> T:
        """Get an instance by its class type.

Args: cls: The class type to get an instance of **kwargs: Additional arguments to pass to the service provider

Returns: An instance of the specified class"""
```
```python
    async def initialize_services(self) -> None:
        """Initialize all registered services in dependency order."""
```
```python
    def register_dependency(self, name, instance) -> None:
        """Register an existing instance as a dependency.

Args: name: Name of the dependency instance: The dependency instance"""
```
```python
    def register_dependency_relationship(self, service_name, depends_on) -> None:
        """Register dependencies between services for ordered initialization.

Args: service_name: Name of the dependent service depends_on: Names of services this one depends on"""
```
```python
    def register_service(self, provider, name) -> None:
        """Register a service provider function.

Args: provider: Function that creates the service name: Name of the service"""
```
```python
    async def shutdown_services(self) -> None:
        """Shut down all services in reverse initialization order."""
```

##### Package: cache
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.cache.base import CacheBackend
from app.core.cache.decorators import cached, invalidate_cache, cache_aside, memoize
from app.core.cache.exceptions import CacheException, CacheConnectionException, CacheOperationException, CacheConfigurationException
from app.core.cache.keys import generate_cache_key, generate_list_key, generate_model_key, generate_query_key
from app.core.cache.manager import cache_manager, initialize_cache
from app.core.cache.service import CacheService, get_cache_service
```

**Global Variables:**
```python
__all__ = __all__ = [
    "CacheBackend",
    "cached",
    "invalidate_cache",
    "cache_aside",
    "memoize",
    "CacheException",
    "CacheConnectionException",
    "CacheOperationException",
    "CacheConfigurationException",
    "generate_cache_key",
    "generate_list_key",
    "generate_model_key",
    "generate_query_key",
    "cache_manager",
    "initialize_cache",
    "CacheService",
    "get_cache_service",
]
```

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/base.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Generic
```

**Global Variables:**
```python
T = T = TypeVar("T")
```

**Classes:**
```python
class CacheBackend(Protocol, Generic[T]):
    """Protocol defining cache backend interface."""
```
*Methods:*
```python
    async def clear(self) -> bool:
        """Clear all cache entries."""
```
```python
    async def decr(self, key, amount, default, ttl) -> int:
        """Decrement a counter in the cache."""
```
```python
    async def delete(self, key) -> bool:
        """Delete key from cache."""
```
```python
    async def delete_many(self, keys) -> int:
        """Delete multiple values from the cache."""
```
```python
    async def exists(self, key) -> bool:
        """Check if key exists in cache."""
```
```python
    async def get(self, key, default) -> Optional[T]:
        """Get value from cache by key."""
```
```python
    async def get_many(self, keys) -> Dict[(str, Optional[T])]:
        """Get multiple values from the cache."""
```
```python
    async def incr(self, key, amount, default, ttl) -> int:
        """Increment a counter in the cache."""
```
```python
    async def initialize(self) -> None:
        """Initialize the cache backend."""
```
```python
    async def invalidate_pattern(self, pattern) -> int:
        """Invalidate all keys matching a pattern."""
```
```python
    async def set(self, key, value, ttl) -> bool:
        """Set value in cache with optional TTL."""
```
```python
    async def set_many(self, mapping, ttl) -> bool:
        """Set multiple values in the cache."""
```
```python
    async def shutdown(self) -> None:
        """Shut down the cache backend."""
```

###### Module: decorators
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/decorators.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import functools
import time
from typing import Any, Callable, List, Optional, TypeVar, cast, Dict
from app.core.cache.keys import generate_cache_key
from app.core.cache.manager import cache_manager
from app.logging import get_logger
from app.core.dependency_manager import get_dependency
```

**Global Variables:**
```python
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
logger = logger = get_logger("app.core.cache.decorators")
HAS_METRICS = False
```

**Functions:**
```python
def cache_aside(key_func, ttl, backend, tags) -> Callable[([F], F)]:
    """Implement the cache-aside pattern with a custom key function.

Args: key_func: Function that generates a cache key from function arguments. ttl: Time-to-live in seconds (default: 300). backend: Cache backend to use (default: None, uses default backend). tags: Optional tags for cache invalidation.

Returns: Decorated function."""
```

```python
def cached(ttl, prefix, backend, skip_args, skip_kwargs, tags) -> Callable[([F], F)]:
    """Cache the result of a function.

Args: ttl: Time-to-live in seconds (default: 300). prefix: Cache key prefix (default: 'cache'). backend: Cache backend to use (default: None, uses default backend). skip_args: Argument indexes to skip when generating the cache key. skip_kwargs: Keyword argument names to skip when generating the cache key. tags: Optional tags for cache invalidation.

Returns: Decorated function."""
```

```python
def invalidate_cache(pattern, prefix, backend, tags) -> Callable[([F], F)]:
    """Invalidate cache entries matching a pattern after function execution.

Args: pattern: The pattern to match for invalidation. prefix: Cache key prefix (default: 'cache'). backend: Cache backend to use (default: None, uses default backend). tags: Optional tags for cache invalidation.

Returns: Decorated function."""
```

```python
def memoize(ttl, max_size) -> Callable[([F], F)]:
    """Memoize a function using in-memory caching.

Args: ttl: Time-to-live in seconds (default: None, meaning no expiration). max_size: Maximum number of items to keep in cache (default: 128).

Returns: Decorated function."""
```

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/exceptions.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
```

**Classes:**
```python
class CacheConfigurationException(CacheException):
```
*Methods:*
```python
    def __init__(self, message, details, original_exception) -> None:
```

```python
class CacheConnectionException(CacheException):
```
*Methods:*
```python
    def __init__(self, message, backend, details, original_exception) -> None:
```

```python
class CacheException(AppException):
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
```

```python
class CacheOperationException(CacheException):
```
*Methods:*
```python
    def __init__(self, message, operation, key, details, original_exception) -> None:
```

###### Module: keys
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/keys.py`

**Imports:**
```python
from __future__ import annotations
import hashlib
import inspect
import json
import re
from typing import Any, Callable, Dict, List, Optional, Tuple
```

**Functions:**
```python
def generate_cache_key(prefix, func, args, kwargs, skip_args, skip_kwargs) -> str:
    """Generate a cache key for a function call.

This function creates a deterministic key based on the function name, argument values, and keyword argument values. It's used by cache decorators to create unique keys for caching function results.

Args: prefix: Key prefix func: Function being called args: Positional arguments kwargs: Keyword arguments skip_args: Indices of positional arguments to skip skip_kwargs: Names of keyword arguments to skip

Returns: str: Cache key"""
```

```python
def generate_list_key(prefix, model_name, filters) -> str:
    """Generate a cache key for a list of model instances.

Args: prefix: Key prefix model_name: Model name filters: Optional filters

Returns: str: Cache key"""
```

```python
def generate_model_key(prefix, model_name, model_id, field) -> str:
    """Generate a cache key for a model instance.

Args: prefix: Key prefix model_name: Model name model_id: Model ID field: Optional field name

Returns: str: Cache key"""
```

```python
def generate_query_key(prefix, query_name, params) -> str:
    """Generate a cache key for a query result.

Args: prefix: Key prefix query_name: Query name params: Optional query parameters

Returns: str: Cache key"""
```

```python
def parse_pattern(pattern) -> re.Pattern:
    """Parse a glob pattern into a regex pattern.

Args: pattern: Glob pattern

Returns: re.Pattern: Regex pattern"""
```

###### Module: manager
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/manager.py`

**Imports:**
```python
from __future__ import annotations
import time
from typing import Dict, Optional, Any, TypeVar, List, Union, cast
from app.core.cache.backends import get_backend
from app.core.cache.base import CacheBackend
from app.core.config import settings
from app.logging import get_logger
from app.core.dependency_manager import get_dependency
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.cache.manager")
T = T = TypeVar("T")
HAS_METRICS = False
cache_manager = cache_manager = CacheManager()
```

**Functions:**
```python
async def initialize_cache() -> None:
    """Initialize the cache system."""
```

**Classes:**
```python
class CacheManager(object):
```
*Methods:*
```python
    def __init__(self):
```
```python
    async def clear(self, backend) -> bool:
        """Clear the cache.

Args: backend: Optional backend name.

Returns: True if successful, False otherwise."""
```
```python
    async def decr(self, key, amount, default, ttl, backend) -> int:
        """Decrement a counter.

Args: key: The cache key. amount: Amount to decrement by. default: Default value if key doesn't exist. ttl: Optional time-to-live in seconds. backend: Optional backend name.

Returns: New counter value."""
```
```python
    async def delete(self, key, backend) -> bool:
        """Delete a value from the cache.

Args: key: The cache key. backend: Optional backend name.

Returns: True if successful, False otherwise."""
```
```python
    async def delete_many(self, keys, backend) -> int:
        """Delete multiple values from the cache.

Args: keys: List of cache keys. backend: Optional backend name.

Returns: Number of deleted keys."""
```
```python
    async def exists(self, key, backend) -> bool:
        """Check if a key exists in the cache.

Args: key: The cache key. backend: Optional backend name.

Returns: True if key exists, False otherwise."""
```
```python
    async def get(self, key, default, backend) -> Optional[T]:
        """Get a value from the cache.

Args: key: The cache key. default: Default value if key doesn't exist. backend: Optional backend name.

Returns: The cached value or default."""
```
```python
    def get_backend(self, name) -> CacheBackend:
        """Get a cache backend by name.

Args: name: The backend name. If None, uses the default backend.

Returns: The cache backend instance.

Raises: ValueError: If the backend is not configured."""
```
```python
    async def get_many(self, keys, backend) -> Dict[(str, Optional[T])]:
        """Get multiple values from the cache.

Args: keys: List of cache keys. backend: Optional backend name.

Returns: Dictionary of key-value pairs."""
```
```python
    async def incr(self, key, amount, default, ttl, backend) -> int:
        """Increment a counter.

Args: key: The cache key. amount: Amount to increment by. default: Default value if key doesn't exist. ttl: Optional time-to-live in seconds. backend: Optional backend name.

Returns: New counter value."""
```
```python
    async def initialize(self) -> None:
        """Initialize the cache manager and backends."""
```
```python
    async def invalidate_pattern(self, pattern, backend) -> int:
        """Invalidate cache keys matching a pattern.

Args: pattern: The pattern to match. backend: Optional backend name.

Returns: Number of invalidated keys."""
```
```python
    async def set(self, key, value, ttl, backend) -> bool:
        """Set a value in the cache.

Args: key: The cache key. value: The value to cache. ttl: Optional time-to-live in seconds. backend: Optional backend name.

Returns: True if successful, False otherwise."""
```
```python
    async def set_many(self, mapping, ttl, backend) -> bool:
        """Set multiple values in the cache.

Args: mapping: Dictionary of key-value pairs. ttl: Optional time-to-live in seconds. backend: Optional backend name.

Returns: True if successful, False otherwise."""
```
```python
    async def shutdown(self) -> None:
        """Shutdown all cache backends."""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/service.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, TypeVar
from app.core.cache.manager import cache_manager
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.cache.service")
T = T = TypeVar("T")
```

**Functions:**
```python
def get_cache_service() -> CacheService:
    """Get the cache service singleton instance.  Returns: The cache service instance."""
```

**Classes:**
```python
class CacheService(object):
```
*Methods:*
```python
    def __init__(self) -> None:
```
```python
    async def clear(self, backend) -> bool:
        """Clear the cache.

Args: backend: Optional backend name.

Returns: True if successful, False otherwise."""
```
```python
    async def decr(self, key, amount, default, ttl, backend) -> int:
        """Decrement a counter.

Args: key: The cache key. amount: Amount to decrement by. default: Default value if key doesn't exist. ttl: Optional time-to-live in seconds. backend: Optional backend name.

Returns: New counter value."""
```
```python
    async def delete(self, key, backend) -> bool:
        """Delete a value from the cache.

Args: key: The cache key. backend: Optional backend name.

Returns: True if successful, False otherwise."""
```
```python
    async def delete_many(self, keys, backend) -> int:
        """Delete multiple values from the cache.

Args: keys: List of cache keys. backend: Optional backend name.

Returns: Number of deleted keys."""
```
```python
    async def exists(self, key, backend) -> bool:
        """Check if a key exists in the cache.

Args: key: The cache key. backend: Optional backend name.

Returns: True if key exists, False otherwise."""
```
```python
    async def get(self, key, default, backend) -> Optional[T]:
        """Get a value from the cache.

Args: key: The cache key. default: Default value if key doesn't exist. backend: Optional backend name.

Returns: The cached value or default."""
```
```python
    async def get_many(self, keys, backend) -> Dict[(str, Optional[T])]:
        """Get multiple values from the cache.

Args: keys: List of cache keys. backend: Optional backend name.

Returns: Dictionary of key-value pairs."""
```
```python
    async def incr(self, key, amount, default, ttl, backend) -> int:
        """Increment a counter.

Args: key: The cache key. amount: Amount to increment by. default: Default value if key doesn't exist. ttl: Optional time-to-live in seconds. backend: Optional backend name.

Returns: New counter value."""
```
```python
    async def initialize(self) -> None:
        """Initialize the cache service."""
```
```python
    async def invalidate_pattern(self, pattern, backend) -> int:
        """Invalidate cache keys matching a pattern.

Args: pattern: The pattern to match. backend: Optional backend name.

Returns: Number of invalidated keys."""
```
```python
    async def set(self, key, value, ttl, backend) -> bool:
        """Set a value in the cache.

Args: key: The cache key. value: The value to cache. ttl: Optional time-to-live in seconds. backend: Optional backend name.

Returns: True if successful, False otherwise."""
```
```python
    async def set_many(self, mapping, ttl, backend) -> bool:
        """Set multiple values in the cache.

Args: mapping: Dictionary of key-value pairs. ttl: Optional time-to-live in seconds. backend: Optional backend name.

Returns: True if successful, False otherwise."""
```
```python
    async def shutdown(self) -> None:
        """Shutdown the cache service."""
```

###### Package: backends
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/backends`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/backends/__init__.py`

**Imports:**
```python
from __future__ import annotations
from typing import Dict, Any
from app.core.cache.backends.memory import MemoryCacheBackend
from app.core.cache.backends.null import NullCacheBackend
from app.core.cache.backends.redis import RedisCacheBackend
```

**Global Variables:**
```python
__all__ = __all__ = ["MemoryCacheBackend", "RedisCacheBackend", "NullCacheBackend", "get_backend"]
```

**Functions:**
```python
def get_backend(name) -> Any:
    """Get cache backend by name."""
```

####### Module: memory
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/backends/memory.py`

**Imports:**
```python
from __future__ import annotations
import fnmatch
import time
from collections import OrderedDict
from threading import RLock
from typing import Any, Dict, List, Optional, TypeVar
from app.core.cache.base import CacheBackend
from app.logging import get_logger
```

**Global Variables:**
```python
T = T = TypeVar("T")
logger = logger = get_logger("app.core.cache.memory")
```

**Classes:**
```python
class MemoryCacheBackend(CacheBackend[T]):
    """In-memory cache backend implementation.

This backend stores cached values in memory, with optional TTL expiration. It's suitable for development and testing environments, or for small-scale production use where persistence is not required."""
```
*Methods:*
```python
    def __init__(self, max_size, clean_interval) -> None:
        """Initialize the memory cache backend.

Args: max_size: Maximum number of items to store in the cache clean_interval: Interval between cleanup runs in seconds"""
```
```python
    async def clear(self) -> bool:
        """Clear all cached values.  Returns: bool: True if successful, False otherwise"""
```
```python
    async def decr(self, key, amount, default, ttl) -> int:
        """Decrement a counter in the cache.

Args: key: Cache key amount: Amount to decrement by default: Default value if key doesn't exist ttl: Time-to-live in seconds

Returns: int: New counter value"""
```
```python
    async def delete(self, key) -> bool:
        """Delete a value from the cache.

Args: key: Cache key

Returns: bool: True if key was deleted, False if key wasn't found"""
```
```python
    async def delete_many(self, keys) -> int:
        """Delete multiple values from the cache.

Args: keys: List of cache keys

Returns: int: Number of keys deleted"""
```
```python
    async def exists(self, key) -> bool:
        """Check if a key exists in the cache.

Args: key: Cache key

Returns: bool: True if key exists and hasn't expired, False otherwise"""
```
```python
    async def get(self, key) -> Optional[T]:
        """Get a value from the cache.

Args: key: Cache key

Returns: Optional[T]: Cached value or None if not found or expired"""
```
```python
    async def get_many(self, keys) -> Dict[(str, Optional[T])]:
        """Get multiple values from the cache.

Args: keys: List of cache keys

Returns: Dict[str, Optional[T]]: Dictionary of key-value pairs"""
```
```python
    async def incr(self, key, amount, default, ttl) -> int:
        """Increment a counter in the cache.

Args: key: Cache key amount: Amount to increment by default: Default value if key doesn't exist ttl: Time-to-live in seconds

Returns: int: New counter value"""
```
```python
    async def initialize(self) -> None:
        """Initialize the memory cache backend.

This is a no-op for the memory backend since it doesn't require external connections, but implemented for interface consistency."""
```
```python
    async def invalidate_pattern(self, pattern) -> int:
        """Invalidate all keys matching a pattern.

Args: pattern: Key pattern to match (glob pattern)

Returns: int: Number of keys invalidated"""
```
```python
    async def set(self, key, value, ttl) -> bool:
        """Set a value in the cache.

Args: key: Cache key value: Value to cache ttl: Time-to-live in seconds

Returns: bool: True if successful, False otherwise"""
```
```python
    async def set_many(self, mapping, ttl) -> bool:
        """Set multiple values in the cache.

Args: mapping: Dictionary of key-value pairs to cache ttl: Time-to-live in seconds

Returns: bool: True if successful, False otherwise"""
```
```python
    async def shutdown(self) -> None:
        """Shut down the memory cache backend.  Clears all cached data and performs cleanup."""
```

####### Module: null
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/backends/null.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, TypeVar
from app.core.cache.base import CacheBackend
from app.logging import get_logger
```

**Global Variables:**
```python
T = T = TypeVar("T")
logger = logger = get_logger("app.core.cache.null")
```

**Classes:**
```python
class NullCacheBackend(CacheBackend[T]):
    """No-op cache backend for testing or disabling cache.

This backend doesn't actually store or retrieve any data. It simply provides the interface required by the CacheBackend protocol but performs no operations. Useful for testing or when caching needs to be disabled."""
```
*Methods:*
```python
    async def clear(self) -> bool:
        """No-op, always return success.  Returns: bool: Always True"""
```
```python
    async def decr(self, key, amount, default, ttl) -> int:
        """No-op decrement method.

Args: key: Cache key amount: Amount to decrement by default: Default value if key doesn't exist ttl: Time-to-live in seconds

Returns: int: Always the default value"""
```
```python
    async def delete(self, key) -> bool:
        """No-op, always return success.  Args: key: Cache key  Returns: bool: Always True"""
```
```python
    async def delete_many(self, keys) -> int:
        """No-op delete many method.  Args: keys: List of cache keys  Returns: int: Always 0"""
```
```python
    async def exists(self, key) -> bool:
        """Always return False.  Args: key: Cache key  Returns: bool: Always False"""
```
```python
    async def get(self, key, default) -> Optional[T]:
        """Always return default value.

Args: key: Cache key default: Default value to return

Returns: Default value (always)"""
```
```python
    async def get_many(self, keys) -> Dict[(str, Optional[T])]:
        """No-op get many method.

Args: keys: List of cache keys

Returns: Dict[str, Optional[T]]: Dictionary with None values for all keys"""
```
```python
    async def incr(self, key, amount, default, ttl) -> int:
        """No-op increment method.

Args: key: Cache key amount: Amount to increment by default: Default value if key doesn't exist ttl: Time-to-live in seconds

Returns: int: Always the default value"""
```
```python
    async def initialize(self) -> None:
        """Initialize the null cache backend.  This is a no-op method that exists for interface consistency."""
```
```python
    async def invalidate_pattern(self, pattern) -> int:
        """No-op invalidate method.  Args: pattern: Pattern to match  Returns: int: Always 0"""
```
```python
    async def set(self, key, value, ttl) -> bool:
        """No-op, always return success.

Args: key: Cache key value: Value to cache ttl: Time-to-live in seconds

Returns: bool: Always True"""
```
```python
    async def set_many(self, mapping, ttl) -> bool:
        """No-op set many method.

Args: mapping: Dictionary of key-value pairs ttl: Time-to-live in seconds

Returns: bool: Always True"""
```
```python
    async def shutdown(self) -> None:
        """Shut down the null cache backend.  This is a no-op method that exists for interface consistency."""
```

####### Module: redis
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/cache/backends/redis.py`

**Imports:**
```python
from __future__ import annotations
import json
import pickle
from typing import Any, Dict, List, Optional, TypeVar, cast
import redis.asyncio as redis
from redis.asyncio import Redis
from app.core.cache.base import CacheBackend
from app.core.config import settings
from app.logging import get_logger
```

**Global Variables:**
```python
T = T = TypeVar("T")
logger = logger = get_logger("app.core.cache.redis")
```

**Classes:**
```python
class RedisCacheBackend(CacheBackend[T]):
    """Redis implementation of the cache backend.

Provides caching functionality using Redis as the storage backend."""
```
*Methods:*
```python
    def __init__(self, redis_url, serializer, prefix, **redis_options) -> None:
        """Initialize the Redis cache backend.

Args: redis_url: Redis connection URL serializer: Serialization format (pickle or json) prefix: Cache key prefix **redis_options: Additional Redis client options"""
```
```python
    async def add_many_to_set(self, key, members) -> int:
        """Add multiple members to a Redis set.

Args: key: Set key members: Members to add

Returns: Number of members added"""
```
```python
    async def add_to_set(self, key, member) -> bool:
        """Add a member to a Redis set.

Args: key: Set key member: Member to add

Returns: True if successful, False otherwise"""
```
```python
    async def clear(self) -> bool:
        """Clear all cache data.  Returns: True if successful, False otherwise"""
```
```python
    async def decr(self, key, amount, default, ttl) -> int:
        """Decrement a counter in the cache.

Args: key: Cache key amount: Amount to decrement by default: Default value if key doesn't exist ttl: Time-to-live in seconds

Returns: New counter value"""
```
```python
    async def delete(self, key) -> bool:
        """Delete a value from the cache.  Args: key: Cache key  Returns: True if successful, False otherwise"""
```
```python
    async def delete_many(self, keys) -> int:
        """Delete multiple values from the cache.

Args: keys: List of cache keys

Returns: Number of deleted keys"""
```
```python
    async def exists(self, key) -> bool:
        """Check if a key exists in the cache.

Args: key: Cache key

Returns: True if key exists, False otherwise"""
```
```python
    async def get(self, key) -> Optional[T]:
        """Get a value from the cache.  Args: key: Cache key  Returns: Cached value or None if not found"""
```
```python
    async def get_many(self, keys) -> Dict[(str, Optional[T])]:
        """Get multiple values from the cache.

Args: keys: List of cache keys

Returns: Dictionary mapping keys to values"""
```
```python
    async def get_set_members(self, key) -> List[str]:
        """Get all members of a Redis set.  Args: key: Set key  Returns: List of set members"""
```
```python
    async def get_ttl(self, key) -> Optional[int]:
        """Get the remaining TTL for a key.

Args: key: Cache key

Returns: Remaining TTL in seconds or None if key doesn't exist"""
```
```python
    async def incr(self, key, amount, default, ttl) -> int:
        """Increment a counter in the cache.

Args: key: Cache key amount: Amount to increment by default: Default value if key doesn't exist ttl: Time-to-live in seconds

Returns: New counter value"""
```
```python
    async def initialize(self) -> None:
        """Initialize the Redis connection.

This method establishes the Redis connection during application startup."""
```
```python
    async def invalidate_pattern(self, pattern) -> int:
        """Invalidate keys matching a pattern.

Args: pattern: Key pattern to invalidate

Returns: Number of invalidated keys"""
```
```python
    async def remove_from_set(self, key, member) -> bool:
        """Remove a member from a Redis set.

Args: key: Set key member: Member to remove

Returns: True if successful, False otherwise"""
```
```python
    async def set(self, key, value, ttl) -> bool:
        """Set a value in the cache.

Args: key: Cache key value: Value to cache ttl: Time-to-live in seconds

Returns: True if successful, False otherwise"""
```
```python
    async def set_many(self, mapping, ttl) -> bool:
        """Set multiple values in the cache.

Args: mapping: Dictionary mapping keys to values ttl: Time-to-live in seconds

Returns: True if successful, False otherwise"""
```
```python
    async def shutdown(self) -> None:
        """Close the Redis connection.

This method is called during application shutdown to properly close the Redis connection."""
```

##### Package: config
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.config.base import Environment, LogLevel
from app.core.config.settings import Settings, get_settings, settings
```

**Global Variables:**
```python
__all__ = __all__ = [
    "Settings",
    "Environment",
    "LogLevel",
    "get_settings",
    "settings",
    "AS400Settings",
    "ElasticsearchSettings",
    "as400_settings",
    "elasticsearch_settings",
    "get_as400_connector_config",
]
```

**Functions:**
```python
def __getattr__(name) -> object:
    """Lazily import and return requested attributes.

This PEP 562 function allows delayed imports of module attributes."""
```

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/base.py`

**Imports:**
```python
from __future__ import annotations
from enum import Enum
from pathlib import Path
from typing import Any, List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Classes:**
```python
class BaseAppSettings(BaseSettings):
    """Base application settings and configuration."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
        json_schema_extra={
            # Disable JSON parsing for these fields
            "AVAILABLE_LOCALES": {"env_mode": "str"},
        },
    )
```
*Methods:*
```python
@field_validator('AVAILABLE_LOCALES', mode='before')
@classmethod
    def parse_str_to_list(cls, v) -> List[str]:
        """Parse string to list."""
```

```python
class Environment(str, Enum):
    """Application environment enumeration."""
```
*Class attributes:*
```python
DEVELOPMENT = 'development'
STAGING = 'staging'
PRODUCTION = 'production'
```

```python
class LogLevel(str, Enum):
    """Log level enumeration."""
```
*Class attributes:*
```python
DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'
```

###### Module: celery
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/celery.py`

**Imports:**
```python
from __future__ import annotations
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Classes:**
```python
class CelerySettings(BaseSettings):
    """Celery task queue settings."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )
```

###### Module: currency
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/currency.py`

**Imports:**
```python
from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Classes:**
```python
class CurrencySettings(BaseSettings):
    """Currency and exchange rate settings."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )
```

###### Module: database
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/database.py`

**Imports:**
```python
from __future__ import annotations
from typing import Optional
from pydantic import PostgresDsn, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Classes:**
```python
class DatabaseSettings(BaseSettings):
    """Database connection settings."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )
```
*Methods:*
```python
@model_validator(mode='after')
    def assemble_db_connection(self) -> 'DatabaseSettings':
        """Build the database URI if not provided directly."""
```
```python
@property
    def redis_uri(self) -> str:
        """Get Redis connection URI."""
```

###### Module: fitment
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/fitment.py`

**Imports:**
```python
from __future__ import annotations
import os
from typing import Optional
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.config.base import Environment
```

**Classes:**
```python
class FitmentSettings(BaseSettings):
    """Fitment database and processing settings."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )
```
*Methods:*
```python
@model_validator(mode='after')
    def validate_fitment_paths(self) -> 'FitmentSettings':
        """Validate fitment file paths in production."""
```

###### Module: media
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/media.py`

**Imports:**
```python
from __future__ import annotations
import os
from typing import Optional, Set
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.config.base import Environment
```

**Classes:**
```python
class MediaSettings(BaseSettings):
    """Media handling and storage settings."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )
```
*Methods:*
```python
@field_validator('MEDIA_ROOT')
@classmethod
    def create_media_directories(cls, v) -> str:
        """Create media directories if they don't exist."""
```
```python
@property
    def media_base_url(self) -> str:
        """Get media base URL."""
```
```python
@field_validator('MEDIA_STORAGE_TYPE')
@classmethod
    def validate_storage_type(cls, v) -> str:
        """Validate media storage type."""
```

###### Module: security
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/security.py`

**Imports:**
```python
from __future__ import annotations
import secrets
from typing import Any, List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Classes:**
```python
class SecuritySettings(BaseSettings):
    """Security-related application settings."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
        json_schema_extra={
            # Disable JSON parsing for these fields that use string-based parsing
            "ALLOWED_HOSTS": {"env_mode": "str"},
            "TRUSTED_PROXIES": {"env_mode": "str"},
            "BACKEND_CORS_ORIGINS": {"env_mode": "str"},
        },
    )
```
*Methods:*
```python
@field_validator('BACKEND_CORS_ORIGINS', mode='before')
@classmethod
    def assemble_cors_origins(cls, v) -> List[str]:
        """Parse CORS origins from string or list."""
```
```python
@field_validator('ALLOWED_HOSTS', 'TRUSTED_PROXIES', mode='before')
@classmethod
    def parse_str_to_list(cls, v) -> List[str]:
        """Parse string to list of strings if needed."""
```
```python
@field_validator('RATE_LIMIT_STORAGE')
@classmethod
    def validate_rate_limit_storage(cls, v) -> str:
        """Validate rate limit storage backend."""
```

###### Module: settings
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/settings.py`

**Imports:**
```python
from __future__ import annotations
from functools import lru_cache
from typing import Any, Dict
from pydantic import model_validator
from pydantic_settings import SettingsConfigDict
from app.core.config.base import BaseAppSettings
from app.core.config.celery import CelerySettings
from app.core.config.currency import CurrencySettings
from app.core.config.database import DatabaseSettings
from app.core.config.fitment import FitmentSettings
from app.core.config.media import MediaSettings
from app.core.config.security import SecuritySettings
```

**Global Variables:**
```python
settings = settings = get_settings()
```

**Functions:**
```python
@lru_cache
def get_settings() -> Settings:
    """Get application settings with caching."""
```

**Classes:**
```python
class Settings(BaseAppSettings, DatabaseSettings, SecuritySettings, MediaSettings, FitmentSettings, CurrencySettings, CelerySettings):
    """Combined application settings.

This class combines all modular settings into a single settings class for application-wide use, with any cross-module validations."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )
```
*Methods:*
```python
@property
    def as400(self) -> 'AS400Settings':
        """Access AS400 settings.

This allows accessing AS400 settings through the main settings object while keeping them modularly separated.

Returns: AS400Settings: The AS400 settings object"""
```
```python
@property
    def elasticsearch(self) -> 'ElasticsearchSettings':
        """Access Elasticsearch settings.

This allows accessing Elasticsearch settings through the main settings object while keeping them modularly separated.

Returns: ElasticsearchSettings: The Elasticsearch settings object"""
```
```python
    def model_dump(self, **kwargs) -> Dict[(str, Any)]:
        """Get settings as a dictionary."""
```
```python
@model_validator(mode='after')
    def setup_celery_urls(self) -> 'Settings':
        """Set up Celery broker and result backend URLs if not provided."""
```

###### Package: integrations
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/integrations`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/integrations/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.config.integrations.as400 import AS400Settings, as400_settings, get_as400_connector_config
from app.core.config.integrations.elasticsearch import ElasticsearchSettings, elasticsearch_settings
```

**Global Variables:**
```python
__all__ = __all__ = [
    "ElasticsearchSettings",
    "elasticsearch_settings",
    "AS400Settings",
    "as400_settings",
    "get_as400_connector_config",
]
```

####### Module: as400
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/integrations/as400.py`

**Imports:**
```python
from __future__ import annotations
import json
import logging
from typing import Any, Dict, List, Optional, Union
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Global Variables:**
```python
as400_settings = as400_settings = AS400Settings()
```

**Functions:**
```python
def get_as400_connector_config() -> Dict[(str, Any)]:
    """Get AS400 connector configuration from settings.

Returns: Dictionary with AS400 connector configuration"""
```

**Classes:**
```python
class AS400Settings(BaseSettings):
    """AS400 connection and synchronization settings.

All sensitive settings can be provided via environment variables for enhanced security."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
        json_schema_extra={
            # Disable JSON parsing for these fields
            "AS400_ALLOWED_TABLES": {"env_mode": "str"},
            "AS400_ALLOWED_SCHEMAS": {"env_mode": "str"},
            "AS400_SYNC_TABLES": {"env_mode": "str"},
        },
    )
```
*Methods:*
```python
@field_validator('AS400_SSL', 'AS400_ENCRYPT_CONNECTION', 'AS400_SYNC_ENABLED', mode='before')
@classmethod
    def parse_boolean(cls, v) -> bool:
        """Parse boolean from string if necessary."""
```
```python
@field_validator('AS400_ALLOWED_TABLES', 'AS400_ALLOWED_SCHEMAS', mode='before')
@classmethod
    def parse_str_to_list(cls, v) -> List[str]:
        """Parse string to list of strings if needed."""
```
```python
@field_validator('AS400_SYNC_TABLES', mode='before')
@classmethod
    def parse_sync_tables(cls, v) -> Dict[(str, str)]:
        """Parse sync tables from string if necessary."""
```
```python
@field_validator('AS400_SYNC_INTERVAL')
@classmethod
    def validate_interval(cls, v) -> int:
        """Validate sync interval is reasonable."""
```
```python
@field_validator('AS400_PORT')
@classmethod
    def validate_port(cls, v) -> Optional[int]:
        """Validate port is within allowed range."""
```

####### Module: elasticsearch
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config/integrations/elasticsearch.py`

**Imports:**
```python
from __future__ import annotations
from typing import Optional
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Global Variables:**
```python
elasticsearch_settings = elasticsearch_settings = ElasticsearchSettings()
```

**Classes:**
```python
class ElasticsearchSettings(BaseSettings):
    """Elasticsearch connection and configuration settings."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Allow extra fields in env file
    )
```
*Methods:*
```python
@property
    def elasticsearch_uri(self) -> str:
        """Get Elasticsearch connection URI."""
```

##### Package: error
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/error`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/error/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
from app.core.error.manager import register_reporter, report_error, resource_not_found, resource_already_exists, validation_error, permission_denied, business_logic_error, ensure_not_none, handle_exception, initialize, shutdown
from app.core.error.reporters import LoggingErrorReporter, DatabaseErrorReporter, ExternalServiceReporter
```

**Global Variables:**
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

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/error/base.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union
from pydantic import BaseModel, Field
from app.logging.context import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.error.base")
F = F = TypeVar("F")
T = T = TypeVar("T")
```

**Classes:**
```python
class Config(object):
```
*Class attributes:*
```python
extra = 'allow'
```

```python
class ErrorContext(BaseModel):
    """Context information for error reporting.

Contains details about where and how an error occurred, including function information, arguments, and request context."""
```

```python
class ErrorHandler(Protocol):
    """Protocol for error handlers.

Error handlers are responsible for handling errors and performing appropriate actions (logging, notifying, etc.)."""
```
*Methods:*
```python
    async def handle_error(self, exception, context) -> Any:
        """Handle an error with context information.

Args: exception: The exception to handle context: Context information about the error

Returns: Any result from handling the error"""
```

```python
class ErrorLogEntry(BaseModel):
    """Model for storing error log entries.

Contains detailed information about an error occurrence for storage in logs or databases."""
```

```python
class ErrorReporter(Protocol):
    """Protocol for error reporters.

Error reporters are responsible for reporting errors to various destinations (logs, databases, external services, etc.)."""
```
*Methods:*
```python
    async def report_error(self, exception, context) -> None:
        """Report an error with context information.

Args: exception: The exception to report context: Context information about the error"""
```

###### Module: factory
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/error/factory.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.core.config import settings
from app.logging import get_logger
from app.core.error.base import ErrorReporter
from app.core.error.reporters import DatabaseErrorReporter, ExternalServiceReporter, LoggingErrorReporter
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.error.factory")
```

**Classes:**
```python
class ErrorReporterFactory(object):
    """Factory for creating error reporters."""
```
*Methods:*
```python
@classmethod
    def create_default_reporters(cls) -> List[ErrorReporter]:
        """Create the default set of error reporters based on configuration settings.

Returns: List of ErrorReporter instances"""
```
```python
@classmethod
    def create_reporter(cls, reporter_type, **kwargs) -> ErrorReporter:
        """Create an error reporter of the specified type.

Args: reporter_type: Type of reporter to create ("logging", "database", or "external") **kwargs: Additional arguments to pass to the reporter constructor

Returns: An ErrorReporter instance

Raises: ValueError: If the reporter type is not supported"""
```
```python
@classmethod
    def create_reporter_by_name(cls, reporter_name) -> Optional[ErrorReporter]:
        """Create an error reporter by name based on configuration settings.

Args: reporter_name: Name of the reporter to create

Returns: An ErrorReporter instance or None if the reporter is not configured"""
```

###### Module: manager
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/error/manager.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import functools
import inspect
import traceback
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, Union
from app.core.exceptions import BusinessException, ErrorCode, PermissionDeniedException, ResourceAlreadyExistsException, ResourceNotFoundException, ValidationException
from app.logging.context import get_logger
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.error.manager")
T = T = TypeVar("T")
```

**Functions:**
```python
def business_logic_error(message, details) -> BusinessException:
    """Create a business logic error exception.

Args: message: Error message details: Additional error details

Returns: A configured BusinessException"""
```

```python
def create_error_context(function_name, args, kwargs, user_id, request_id) -> ErrorContext:
    """Create an error context from the current call frame.

Args: function_name: Optional name of the function args: Optional positional arguments kwargs: Optional keyword arguments user_id: Optional user ID request_id: Optional request ID

Returns: A configured ErrorContext"""
```

```python
def ensure_not_none(value, resource_type, resource_id, message) -> T:
    """Ensure a value is not None, raising an exception if it is.

Args: value: Value to check resource_type: Type of resource being checked resource_id: ID of the resource being checked message: Optional custom error message

Returns: The value, if it is not None

Raises: ResourceNotFoundException: If the value is None"""
```

```python
def error_context_decorator(user_id_param, request_id_param) -> Callable[([Callable[(Ellipsis, Any)]], Callable[(Ellipsis, Any)])]:
    """Decorator that adds error handling to a function.

Args: user_id_param: Optional parameter name for user ID request_id_param: Optional parameter name for request ID

Returns: A decorator function"""
```

```python
def handle_exception(exception, request_id, user_id, function_name) -> None:
    """Handle an exception by reporting it.

Args: exception: The exception to handle request_id: Optional request ID user_id: Optional user ID function_name: Optional function name"""
```

```python
async def initialize() -> None:
    """Initialize the error handling system."""
```

```python
def permission_denied(action, resource_type, permission) -> PermissionDeniedException:
    """Create a permission denied exception.

Args: action: Action that was attempted resource_type: Type of resource being accessed permission: Permission that was required

Returns: A configured PermissionDeniedException"""
```

```python
def register_reporter(reporter) -> None:
    """Register an error reporter.  Args: reporter: The error reporter to register"""
```

```python
async def report_error(exception, context) -> None:
    """Report an error using all registered reporters.

Args: exception: The exception to report context: Context information about the error"""
```

```python
def resource_already_exists(resource_type, identifier, field, message) -> ResourceAlreadyExistsException:
    """Create a resource already exists exception.

Args: resource_type: Type of resource that already exists identifier: Identifier of the resource field: Field name of the identifier (default: 'id') message: Optional custom error message

Returns: A configured ResourceAlreadyExistsException"""
```

```python
def resource_not_found(resource_type, resource_id, message) -> ResourceNotFoundException:
    """Create a resource not found exception.

Args: resource_type: Type of resource that was not found resource_id: ID of the resource that was not found message: Optional custom error message

Returns: A configured ResourceNotFoundException"""
```

```python
async def shutdown() -> None:
    """Shut down the error handling system."""
```

```python
def validation_error(field, message, error_type) -> ValidationException:
    """Create a validation error exception.

Args: field: Field that failed validation message: Error message error_type: Type of validation error

Returns: A configured ValidationException"""
```

###### Module: reporters
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/error/reporters.py`

**Imports:**
```python
from __future__ import annotations
import json
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
import httpx
from app.core.error.base import ErrorContext, ErrorReporter, ErrorLogEntry
from app.logging.context import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.error.reporters")
```

**Classes:**
```python
class CompositeErrorReporter(ErrorReporter):
    """Error reporter that delegates to multiple other reporters.

This reporter sends errors to multiple destinations by delegating to a collection of other error reporters."""
```
*Methods:*
```python
    def __init__(self, reporters) -> None:
        """Initialize with a list of reporters.  Args: reporters: List of error reporters to use"""
```
```python
    async def report_error(self, exception, context) -> None:
        """Report an error using all configured reporters.

Args: exception: The exception to report context: Context information about the error"""
```

```python
class DatabaseErrorReporter(ErrorReporter):
    """Error reporter that stores errors in a database.

This reporter formats error information and stores it in a database for later analysis and reporting."""
```
*Methods:*
```python
    async def report_error(self, exception, context) -> None:
        """Report an error by storing it in a database.

Args: exception: The exception to report context: Context information about the error"""
```

```python
class ExternalServiceReporter(ErrorReporter):
    """Error reporter that sends errors to an external service.

This reporter formats error information and sends it to an external error tracking or monitoring service via HTTP."""
```
*Methods:*
```python
    def __init__(self, service_url, api_key) -> None:
        """Initialize the reporter with service connection details.

Args: service_url: URL of the external error reporting service api_key: API key for authenticating with the service"""
```
```python
    async def report_error(self, exception, context) -> None:
        """Report an error by sending it to an external service.

Args: exception: The exception to report context: Context information about the error"""
```

```python
class LoggingErrorReporter(ErrorReporter):
    """Error reporter that logs errors using the application logging system.

This reporter formats error information and logs it via the structured logging system, ensuring consistent error logging across the application."""
```
*Methods:*
```python
    async def report_error(self, exception, context) -> None:
        """Report an error by logging it.

Args: exception: The exception to report context: Context information about the error"""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/error/service.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Type
from app.core.error.base import ErrorContext, ErrorReporter
from app.core.error.factory import ErrorReporterFactory
from app.core.error.manager import business_logic_error, handle_exception, initialize as initialize_manager, permission_denied, register_reporter, report_error, resource_already_exists, resource_not_found, shutdown as shutdown_manager, validation_error
from app.core.error.reporters import CompositeErrorReporter, DatabaseErrorReporter, ExternalServiceReporter, LoggingErrorReporter
from app.logging.context import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.error.service")
```

**Functions:**
```python
def get_error_service() -> ErrorService:
    """Get the error service singleton.  Returns: The error service instance"""
```

**Classes:**
```python
class ErrorService(object):
    """Service for error handling and reporting.

This service provides methods for creating and reporting errors, as well as initializing and managing error reporters."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the error service."""
```
```python
    def business_logic_error(self, message, details) -> Exception:
        """Create a business logic error exception.

Args: message: Error message details: Additional error details

Returns: A configured BusinessException"""
```
```python
    def handle_exception(self, exception, request_id, user_id, function_name) -> None:
        """Handle an exception by reporting it.

Args: exception: The exception to handle request_id: Optional request ID user_id: Optional user ID function_name: Optional function name"""
```
```python
    async def initialize(self) -> None:
        """Initialize the error service."""
```
```python
    def permission_denied(self, action, resource_type, permission) -> Exception:
        """Create a permission denied exception.

Args: action: Action that was attempted resource_type: Type of resource being accessed permission: Permission that was required

Returns: A configured PermissionDeniedException"""
```
```python
    async def register_reporter(self, reporter) -> None:
        """Register an error reporter.  Args: reporter: The error reporter to register"""
```
```python
    async def register_reporter_by_name(self, reporter_name) -> None:
        """Register an error reporter by name.  Args: reporter_name: Name of the reporter to register"""
```
```python
    async def report_error(self, exception, context) -> None:
        """Report an error with context.

Args: exception: The exception to report context: Context information for the error"""
```
```python
    def resource_already_exists(self, resource_type, identifier, field, message) -> Exception:
        """Create a resource already exists exception.

Args: resource_type: Type of resource that already exists identifier: Identifier of the resource field: Field name of the identifier (default: 'id') message: Optional custom error message

Returns: A configured ResourceAlreadyExistsException"""
```
```python
    def resource_not_found(self, resource_type, resource_id, message) -> Exception:
        """Create a resource not found exception.

Args: resource_type: Type of resource that was not found resource_id: ID of the resource that was not found message: Optional custom error message

Returns: A configured ResourceNotFoundException"""
```
```python
    async def shutdown(self) -> None:
        """Shut down the error service."""
```
```python
    def validation_error(self, field, message, error_type) -> Exception:
        """Create a validation error exception.

Args: field: Field that failed validation message: Error message error_type: Type of validation error

Returns: A configured ValidationException"""
```

##### Package: events
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/events`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/events/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.events.backend import EventBackendType, get_event_backend, init_domain_events, init_event_backend, publish_event, subscribe_to_event, register_event_handlers
```

**Global Variables:**
```python
__all__ = __all__ = [
    "EventBackendType",
    "get_event_backend",
    "init_domain_events",
    "init_event_backend",
    "publish_event",
    "subscribe_to_event",
    "register_event_handlers",  # Kept for backward compatibility
]
```

###### Module: backend
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/events/backend.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import inspect
from app.logging import get_logger
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.events.backend")
EventHandler = EventHandler = Callable[[Dict[str, Any]], Any]
```

**Functions:**
```python
def get_event_backend() -> EventBackend:
    """Get the configured event backend.

Returns: The configured event backend instance.

Raises: RuntimeError: If the event backend is not initialized"""
```

```python
def init_domain_events() -> None:
    """Initialize domain events by registering all pending handlers.

This should be called after the event backend is initialized."""
```

```python
def init_event_backend(backend_type, **kwargs) -> EventBackend:
    """Initialize the event backend to use.

Args: backend_type: Type of event backend to use **kwargs: Additional arguments to pass to the backend constructor

Returns: The initialized event backend instance

Raises: ValueError: If an unsupported backend type is requested"""
```

```python
def publish_event(event_name, payload) -> None:
    """Publish a domain event.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```

```python
def register_event_handlers(*modules) -> None:
    """Import modules to register their event handlers.

This function has been deprecated. Use init_domain_events() instead.

Args: *modules: Module objects to ensure are imported"""
```

```python
def subscribe_to_event(event_name) -> Callable[([EventHandler], EventHandler)]:
    """Decorator to subscribe a function to a domain event.

If the event backend is not yet initialized, handlers will be stored for later registration with init_domain_events().

Args: event_name: The name of the event to subscribe to

Returns: Decorator function that registers the handler"""
```

**Classes:**
```python
class CeleryEventBackend(EventBackend):
    """Celery implementation of the event backend."""
```
*Methods:*
```python
    def __init__(self, celery_app) -> None:
        """Initialize with a Celery application.  Args: celery_app: The Celery application instance"""
```
```python
    def publish_event(self, event_name, payload) -> None:
        """Publish an event using Celery tasks.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```
```python
    def subscribe(self, event_name, handler) -> None:
        """Subscribe a handler to an event using Celery task decoration.

Args: event_name: The name of the event to subscribe to handler: The function to call when the event is published"""
```

```python
class EventBackend(ABC, EventPublisher, EventSubscriber):
    """Abstract base class for event backend implementations."""
```
*Methods:*
```python
@abstractmethod
    def publish_event(self, event_name, payload) -> None:
        """Publish an event to subscribers.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```
```python
@abstractmethod
    def subscribe(self, event_name, handler) -> None:
        """Subscribe a handler to an event.

Args: event_name: The name of the event to subscribe to handler: The function to call when the event is published"""
```

```python
class EventBackendType(Enum):
    """Types of event backends supported."""
```
*Class attributes:*
```python
CELERY =     CELERY = auto()
MEMORY =     MEMORY = auto()
```

```python
class EventPublisher(Protocol):
    """Protocol defining the interface for publishing events."""
```
*Methods:*
```python
    def publish_event(self, event_name, payload) -> None:
        """Publish an event to subscribers.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```

```python
class EventSubscriber(Protocol):
    """Protocol defining the interface for subscribing to events."""
```
*Methods:*
```python
    def subscribe(self, event_name, handler) -> None:
        """Subscribe a handler to an event.

Args: event_name: The name of the event to subscribe to handler: The function to call when the event is published"""
```

```python
class MemoryEventBackend(EventBackend):
    """In-memory implementation of the event backend for testing or simple apps."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the in-memory event registry."""
```
```python
    def publish_event(self, event_name, payload) -> None:
        """Publish an event to all subscribers immediately in-process.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```
```python
    def subscribe(self, event_name, handler) -> None:
        """Subscribe a handler to an event for in-memory processing.

Args: event_name: The name of the event to subscribe to handler: The function to call when the event is published"""
```

###### Module: init
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/events/init.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import importlib
import inspect
from app.logging import get_logger
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.events.init")
EventHandler = EventHandler = Callable[[Dict[str, Any]], Any]
```

**Functions:**
```python
def get_event_backend() -> EventBackend:
    """Get the configured event backend.

Returns: The configured event backend instance

Raises: RuntimeError: If event backend is not initialized"""
```

```python
def init_domain_events() -> None:
    """Initialize domain events by registering all pending handlers.

This should be called after the event backend is initialized."""
```

```python
def init_event_backend(backend_type, **kwargs) -> None:
    """Initialize the event backend.

Args: backend_type: Type of event backend to use **kwargs: Additional arguments for the backend"""
```

```python
def publish_event(event_name, payload) -> None:
    """Publish a domain event.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```

```python
def subscribe_to_event(event_name) -> Callable[([EventHandler], EventHandler)]:
    """Decorator to register a handler for a domain event.

During application initialization, this will store the handler for later registration. After the event system is initialized, handlers will be registered with the backend.

Args: event_name: Name of the event to subscribe to

Returns: Decorator function"""
```

**Classes:**
```python
class CeleryEventBackend(EventBackend):
    """Celery implementation of the event backend."""
```
*Methods:*
```python
    def __init__(self, celery_app) -> None:
        """Initialize with a Celery application.  Args: celery_app: The Celery application instance"""
```
```python
    def publish_event(self, event_name, payload) -> None:
        """Publish an event using Celery tasks.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```
```python
    def subscribe(self, event_name, handler) -> None:
        """Subscribe a handler to an event using Celery task decoration.

Args: event_name: The name of the event to subscribe to handler: The function to call when the event is published"""
```

```python
class EventBackend(ABC, EventPublisher, EventSubscriber):
    """Abstract base class for event backend implementations."""
```
*Methods:*
```python
@abstractmethod
    def publish_event(self, event_name, payload) -> None:
        """Publish an event to subscribers.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```
```python
@abstractmethod
    def subscribe(self, event_name, handler) -> None:
        """Subscribe a handler to an event.

Args: event_name: The name of the event to subscribe to handler: The function to call when the event is published"""
```

```python
class EventBackendType(Enum):
    """Types of event backends supported."""
```
*Class attributes:*
```python
CELERY =     CELERY = auto()
MEMORY =     MEMORY = auto()
```

```python
class EventPublisher(Protocol):
    """Protocol defining the interface for publishing events."""
```
*Methods:*
```python
    def publish_event(self, event_name, payload) -> None:
        """Publish an event to subscribers.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```

```python
class EventSubscriber(Protocol):
    """Protocol defining the interface for subscribing to events."""
```
*Methods:*
```python
    def subscribe(self, event_name, handler) -> None:
        """Subscribe a handler to an event.

Args: event_name: The name of the event to subscribe to handler: The function to call when the event is published"""
```

```python
class MemoryEventBackend(EventBackend):
    """In-memory implementation of the event backend for testing or simple apps."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the in-memory event registry."""
```
```python
    def publish_event(self, event_name, payload) -> None:
        """Publish an event to all subscribers immediately in-process.

Args: event_name: The name of the event to publish payload: Event data to be sent to subscribers"""
```
```python
    def subscribe(self, event_name, handler) -> None:
        """Subscribe a handler to an event for in-memory processing.

Args: event_name: The name of the event to subscribe to handler: The function to call when the event is published"""
```

##### Package: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/exceptions`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/exceptions/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorDetail, ErrorResponse, ErrorSeverity
from app.core.exceptions.domain import AuthException, AuthenticationException, BusinessException, InvalidStateException, OperationNotAllowedException, PermissionDeniedException, ResourceAlreadyExistsException, ResourceException, ResourceNotFoundException, ValidationException
from app.core.exceptions.system import ConfigurationException, DatabaseException, DataIntegrityException, NetworkException, RateLimitException, SecurityException, ServiceException, SystemException, TransactionException
from app.core.exceptions.handlers import app_exception_handler, generic_exception_handler, validation_exception_handler
```

**Global Variables:**
```python
__all__ = __all__ = [
    # Base
    "AppException",
    "ErrorCategory",
    "ErrorCode",
    "ErrorDetail",
    "ErrorResponse",
    "ErrorSeverity",
    # Domain
    "AuthException",
    "AuthenticationException",
    "BusinessException",
    "InvalidStateException",
    "OperationNotAllowedException",
    "PermissionDeniedException",
    "ResourceAlreadyExistsException",
    "ResourceException",
    "ResourceNotFoundException",
    "ValidationException",
    # System
    "ConfigurationException",
    "DatabaseException",
    "DataIntegrityException",
    "NetworkException",
    "RateLimitException",
    "SecurityException",
    "ServiceException",
    "SystemException",
    "TransactionException",
    # Handlers
    "app_exception_handler",
    "generic_exception_handler",
    "validation_exception_handler",
]
```

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/exceptions/base.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
import traceback
import logging
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from app.logging.context import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.exceptions")
```

**Classes:**
```python
class AppException(Exception):
    """Base exception class for application exceptions.

Provides consistent error handling, formatting, and logging for all application exceptions."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, severity, category, original_exception) -> None:
        """Initialize the exception.

Args: message: Human-readable error message code: Error code identifier details: Additional details about the error status_code: HTTP status code for the error severity: Severity level of the error category: Category of the error original_exception: Original exception that caused this one"""
```
```python
    def log(self, request_id) -> None:
        """Log the exception with appropriate severity and context.

Args: request_id: Optional request ID for correlation"""
```
```python
    def to_response(self, request_id) -> ErrorResponse:
        """Convert the exception to a standardized error response.

Args: request_id: Optional request ID to include in the response

Returns: Formatted error response object"""
```

```python
class ErrorCategory(str, Enum):
    """Categories of errors in the application."""
```
*Class attributes:*
```python
VALIDATION = 'validation'
AUTH = 'auth'
RESOURCE = 'resource'
SYSTEM = 'system'
BUSINESS = 'business'
```

```python
class ErrorCode(str, Enum):
    """Specific error codes for different error scenarios."""
```
*Class attributes:*
```python
RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND'
RESOURCE_ALREADY_EXISTS = 'RESOURCE_ALREADY_EXISTS'
AUTHENTICATION_FAILED = 'AUTHENTICATION_FAILED'
PERMISSION_DENIED = 'PERMISSION_DENIED'
VALIDATION_ERROR = 'VALIDATION_ERROR'
BAD_REQUEST = 'BAD_REQUEST'
BUSINESS_LOGIC_ERROR = 'BUSINESS_LOGIC_ERROR'
INVALID_STATE = 'INVALID_STATE'
OPERATION_NOT_ALLOWED = 'OPERATION_NOT_ALLOWED'
DATABASE_ERROR = 'DATABASE_ERROR'
NETWORK_ERROR = 'NETWORK_ERROR'
SERVICE_ERROR = 'SERVICE_ERROR'
CONFIGURATION_ERROR = 'CONFIGURATION_ERROR'
SECURITY_ERROR = 'SECURITY_ERROR'
UNKNOWN_ERROR = 'UNKNOWN_ERROR'
```

```python
class ErrorDetail(BaseModel):
    """Detailed information about a specific error."""
```

```python
class ErrorResponse(BaseModel):
    """Standardized error response model."""
```
*Methods:*
```python
@field_validator('details', mode='before')
@classmethod
    def validate_details(cls, v) -> List[ErrorDetail]:
        """Validate and transform error details.

Args: v: The input value to validate

Returns: Processed list of error details"""
```

```python
class ErrorSeverity(str, Enum):
    """Severity levels for errors."""
```
*Class attributes:*
```python
WARNING = 'warning'
ERROR = 'error'
CRITICAL = 'critical'
```

###### Module: domain
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/exceptions/domain.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
```

**Classes:**
```python
class AuthException(AppException):
    """Base exception for authentication and authorization errors."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize an AuthException.

Args: message: Human-readable error message code: Error code from ErrorCode enum details: Additional details about the error status_code: HTTP status code to return original_exception: Original exception if this is a wrapper"""
```

```python
class AuthenticationException(AuthException):
    """Exception raised when authentication fails."""
```
*Methods:*
```python
    def __init__(self, message, details, original_exception) -> None:
        """Initialize an AuthenticationException.

Args: message: Human-readable error message details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

```python
class BusinessException(AppException):
    """Exception raised when a business rule is violated."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize a BusinessException.

Args: message: Human-readable error message code: Error code from ErrorCode enum details: Additional details about the error status_code: HTTP status code to return original_exception: Original exception if this is a wrapper"""
```

```python
class InvalidStateException(BusinessException):
    """Exception raised when an operation is attempted on an entity in an invalid state."""
```
*Methods:*
```python
    def __init__(self, message, current_state, expected_state, details, original_exception) -> None:
        """Initialize an InvalidStateException.

Args: message: Human-readable error message current_state: The current state of the entity expected_state: The expected state for the operation details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

```python
class OperationNotAllowedException(BusinessException):
    """Exception raised when an operation is not allowed due to business rules."""
```
*Methods:*
```python
    def __init__(self, message, operation, reason, details, original_exception) -> None:
        """Initialize an OperationNotAllowedException.

Args: message: Human-readable error message operation: The operation that was attempted reason: The reason the operation is not allowed details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

```python
class PermissionDeniedException(AuthException):
    """Exception raised when a user doesn't have permission for an action."""
```
*Methods:*
```python
    def __init__(self, message, action, resource_type, permission, details, original_exception) -> None:
        """Initialize a PermissionDeniedException.

Args: message: Human-readable error message action: The action that was attempted (e.g., "create", "read") resource_type: The type of resource being accessed permission: The permission that was required details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

```python
class ResourceAlreadyExistsException(ResourceException):
    """Exception raised when attempting to create a resource that already exists."""
```
*Methods:*
```python
    def __init__(self, resource_type, identifier, field, message, details, original_exception) -> None:
        """Initialize a ResourceAlreadyExistsException.

Args: resource_type: Type of resource that already exists identifier: Identifier value of the resource field: Field name that contains the identifier (defaults to "id") message: Optional custom message details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

```python
class ResourceException(AppException):
    """Base exception for resource-related errors."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize a ResourceException.

Args: message: Human-readable error message code: Error code from ErrorCode enum details: Additional details about the error status_code: HTTP status code to return original_exception: Original exception if this is a wrapper"""
```

```python
class ResourceNotFoundException(ResourceException):
    """Exception raised when a requested resource is not found."""
```
*Methods:*
```python
    def __init__(self, resource_type, resource_id, message, details, original_exception) -> None:
        """Initialize a ResourceNotFoundException.

Args: resource_type: Type of resource that was not found resource_id: ID of the resource that was not found message: Optional custom message (defaults to standard not found message) details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

```python
class ValidationException(AppException):
    """Exception raised when input validation fails."""
```
*Methods:*
```python
    def __init__(self, message, errors, details, original_exception) -> None:
        """Initialize a ValidationException.

Args: message: Human-readable error message errors: List of validation errors details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

###### Module: handlers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/exceptions/handlers.py`

**Imports:**
```python
from __future__ import annotations
import datetime
import traceback
from typing import Dict, Any
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.core.exceptions.base import AppException, ErrorCode, ErrorDetail, ErrorResponse, ErrorSeverity
from app.logging.context import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.exceptions.handlers")
```

**Functions:**
```python
async def app_exception_handler(request, exc) -> JSONResponse:
    """Handle application exceptions.

Args: request: The request that caused the exception exc: The application exception

Returns: A formatted JSON response with error details"""
```

```python
async def generic_exception_handler(request, exc) -> JSONResponse:
    """Handle generic exceptions.

Args: request: The request that caused the exception exc: The unhandled exception

Returns: A formatted JSON response with error details"""
```

```python
async def validation_exception_handler(request, exc) -> JSONResponse:
    """Handle validation exceptions.

Args: request: The request that caused the exception exc: The validation exception

Returns: A formatted JSON response with validation error details"""
```

###### Module: system
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/exceptions/system.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
```

**Classes:**
```python
class ConfigurationException(SystemException):
    """Exception raised when there is an issue with application configuration."""
```
*Methods:*
```python
    def __init__(self, message, component, details, original_exception) -> None:
        """Initialize a ConfigurationException.

Args: message: Human-readable error message component: The component with configuration issues details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

```python
class DataIntegrityException(DatabaseException):
    """Exception raised when a database operation would violate data integrity."""
```
*Methods:*
```python
    def __init__(self, message, details, original_exception) -> None:
        """Initialize a DataIntegrityException.

Args: message: Human-readable error message details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

```python
class DatabaseException(SystemException):
    """Exception raised when a database operation fails."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize a DatabaseException.

Args: message: Human-readable error message code: Error code from ErrorCode enum details: Additional details about the error status_code: HTTP status code to return original_exception: Original exception if this is a wrapper"""
```

```python
class NetworkException(SystemException):
    """Exception raised when a network operation fails."""
```
*Methods:*
```python
    def __init__(self, message, details, status_code, original_exception) -> None:
        """Initialize a NetworkException.

Args: message: Human-readable error message details: Additional details about the error status_code: HTTP status code to return original_exception: Original exception if this is a wrapper"""
```

```python
class RateLimitException(SecurityException):
    """Exception raised when a rate limit is exceeded."""
```
*Methods:*
```python
    def __init__(self, message, details, headers, original_exception) -> None:
        """Initialize a RateLimitException.

Args: message: Human-readable error message details: Additional details about the error headers: HTTP headers to include in the response original_exception: Original exception if this is a wrapper"""
```

```python
class SecurityException(SystemException):
    """Exception raised when a security-related issue occurs."""
```
*Methods:*
```python
    def __init__(self, message, details, status_code, original_exception) -> None:
        """Initialize a SecurityException.

Args: message: Human-readable error message details: Additional details about the error status_code: HTTP status code to return original_exception: Original exception if this is a wrapper"""
```

```python
class ServiceException(SystemException):
    """Exception raised when an external service call fails."""
```
*Methods:*
```python
    def __init__(self, message, service_name, details, status_code, original_exception) -> None:
        """Initialize a ServiceException.

Args: message: Human-readable error message service_name: Name of the external service that failed details: Additional details about the error status_code: HTTP status code to return original_exception: Original exception if this is a wrapper"""
```

```python
class SystemException(AppException):
    """Base exception for system-related errors."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize a SystemException.

Args: message: Human-readable error message code: Error code from ErrorCode enum details: Additional details about the error status_code: HTTP status code to return original_exception: Original exception if this is a wrapper"""
```

```python
class TransactionException(DatabaseException):
    """Exception raised when a database transaction fails."""
```
*Methods:*
```python
    def __init__(self, message, details, original_exception) -> None:
        """Initialize a TransactionException.

Args: message: Human-readable error message details: Additional details about the error original_exception: Original exception if this is a wrapper"""
```

##### Package: metrics
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics`

**__init__.py:**
*Metrics package for application monitoring and observability.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.metrics.base import MetricName, MetricTag, MetricType, MetricsConfig
from app.core.metrics.collectors import CounterCollector, GaugeCollector, HistogramCollector, SummaryCollector
from app.core.metrics.decorators import timer
from app.core.metrics.exceptions import MetricsException, MetricsConfigurationException, MetricsOperationException
from app.core.metrics.manager import initialize, shutdown, create_counter, create_gauge, create_histogram, create_summary, increment_counter, set_gauge, observe_histogram, observe_summary, track_in_progress, track_request, track_db_query, track_service_call, track_cache_operation, timed_function, async_timed_function, get_current_metrics
from app.core.metrics.service import MetricsService, get_metrics_service
from app.core.metrics.trackers import HttpTracker, DatabaseTracker, ServiceTracker, CacheTracker
```

**Global Variables:**
```python
__all__ = __all__ = [
    "MetricName",
    "MetricTag",
    "MetricType",
    "MetricsConfig",
    "CounterCollector",
    "GaugeCollector",
    "HistogramCollector",
    "SummaryCollector",
    "timer",
    "timed_function",
    "async_timed_function",
    "initialize",
    "shutdown",
    "create_counter",
    "create_gauge",
    "create_histogram",
    "create_summary",
    "increment_counter",
    "set_gauge",
    "observe_histogram",
    "observe_summary",
    "track_in_progress",
    "track_request",
    "track_db_query",
    "track_service_call",
    "track_cache_operation",
    "get_current_metrics",
    "HttpTracker",
    "DatabaseTracker",
    "ServiceTracker",
    "CacheTracker",
    "MetricsException",
    "MetricsConfigurationException",
    "MetricsOperationException",
    "MetricsService",
    "get_metrics_service",
]
```

###### Module: base
*Base types and interfaces for the metrics system.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics/base.py`

**Imports:**
```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TypeVar
```

**Global Variables:**
```python
F = F = TypeVar("F", bound=Callable[..., Any])
```

**Classes:**
```python
class MetricName(object):
    """Common metric names for consistent measurement."""
```
*Class attributes:*
```python
HTTP_REQUESTS_TOTAL = 'http_requests_total'
HTTP_REQUEST_DURATION_SECONDS = 'http_request_duration_seconds'
HTTP_REQUEST_SIZE_BYTES = 'http_request_size_bytes'
HTTP_RESPONSE_SIZE_BYTES = 'http_response_size_bytes'
HTTP_ERRORS_TOTAL = 'http_errors_total'
HTTP_IN_PROGRESS = 'http_requests_in_progress'
DB_QUERIES_TOTAL = 'db_queries_total'
DB_QUERY_DURATION_SECONDS = 'db_query_duration_seconds'
DB_CONNECTIONS_TOTAL = 'db_connections_total'
DB_CONNECTIONS_IN_USE = 'db_connections_in_use'
DB_TRANSACTION_DURATION_SECONDS = 'db_transaction_duration_seconds'
DB_ERRORS_TOTAL = 'db_errors_total'
SERVICE_CALLS_TOTAL = 'service_calls_total'
SERVICE_CALL_DURATION_SECONDS = 'service_call_duration_seconds'
SERVICE_ERRORS_TOTAL = 'service_errors_total'
CACHE_HIT_TOTAL = 'cache_hit_total'
CACHE_MISS_TOTAL = 'cache_miss_total'
CACHE_OPERATIONS_TOTAL = 'cache_operations_total'
CACHE_OPERATION_DURATION_SECONDS = 'cache_operation_duration_seconds'
USER_LOGINS_TOTAL = 'user_logins_total'
ORDERS_TOTAL = 'orders_total'
PRODUCTS_CREATED_TOTAL = 'products_created_total'
SYSTEM_MEMORY_BYTES = 'system_memory_bytes'
SYSTEM_CPU_USAGE = 'system_cpu_usage'
SYSTEM_DISK_USAGE_BYTES = 'system_disk_usage_bytes'
PROCESS_RESIDENT_MEMORY_BYTES = 'process_resident_memory_bytes'
PROCESS_VIRTUAL_MEMORY_BYTES = 'process_virtual_memory_bytes'
PROCESS_CPU_SECONDS_TOTAL = 'process_cpu_seconds_total'
PROCESS_OPEN_FDS = 'process_open_fds'
```

```python
class MetricTag(object):
    """Common metric tag names for consistent labeling."""
```
*Class attributes:*
```python
SERVICE = 'service'
ENVIRONMENT = 'environment'
VERSION = 'version'
INSTANCE = 'instance'
ENDPOINT = 'endpoint'
METHOD = 'method'
PATH = 'path'
STATUS_CODE = 'status_code'
OPERATION = 'operation'
ENTITY = 'entity'
QUERY_TYPE = 'query_type'
COMPONENT = 'component'
ACTION = 'action'
ERROR_TYPE = 'error_type'
ERROR_CODE = 'error_code'
RESOURCE_TYPE = 'resource_type'
RESOURCE_ID = 'resource_id'
USER_ID = 'user_id'
USER_ROLE = 'user_role'
CACHE_HIT = 'cache_hit'
CACHE_BACKEND = 'cache_backend'
```

```python
class MetricType(str, Enum):
    """Enum for different types of metrics."""
```
*Class attributes:*
```python
COUNTER = 'counter'
GAUGE = 'gauge'
HISTOGRAM = 'histogram'
SUMMARY = 'summary'
```

```python
@dataclass
class MetricsConfig(object):
    """Configuration for the metrics system."""
```

###### Module: collectors
*Metric collectors for different metric types.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics/collectors.py`

**Imports:**
```python
from __future__ import annotations
from typing import Dict, List, Optional
from prometheus_client import Counter, Gauge, Histogram, Summary
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.metrics.collectors")
```

**Classes:**
```python
class CounterCollector(MetricCollector):
    """Collector for counter metrics."""
```
*Methods:*
```python
    def __init__(self, name, description, labelnames, namespace, subsystem):
        """Initialize the counter collector.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional metric namespace subsystem: Optional metric subsystem"""
```
```python
    def increment(self, amount, labels) -> None:
        """Increment the counter.  Args: amount: Amount to increment by labels: Optional label values"""
```

```python
class GaugeCollector(MetricCollector):
    """Collector for gauge metrics."""
```
*Methods:*
```python
    def __init__(self, name, description, labelnames, namespace, subsystem):
        """Initialize the gauge collector.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional metric namespace subsystem: Optional metric subsystem"""
```
```python
    def decrement(self, amount, labels) -> None:
        """Decrement the gauge.  Args: amount: Amount to decrement by labels: Optional label values"""
```
```python
    def increment(self, amount, labels) -> None:
        """Increment the gauge.  Args: amount: Amount to increment by labels: Optional label values"""
```
```python
    def set(self, value, labels) -> None:
        """Set the gauge value.  Args: value: Value to set labels: Optional label values"""
```

```python
class HistogramCollector(MetricCollector):
    """Collector for histogram metrics."""
```
*Methods:*
```python
    def __init__(self, name, description, labelnames, buckets, namespace, subsystem):
        """Initialize the histogram collector.

Args: name: Metric name description: Metric description labelnames: Optional list of label names buckets: Optional histogram buckets namespace: Optional metric namespace subsystem: Optional metric subsystem"""
```
```python
    def observe(self, value, labels) -> None:
        """Record an observation.  Args: value: Value to observe labels: Optional label values"""
```

```python
class MetricCollector(object):
    """Base class for metric collectors."""
```
*Methods:*
```python
    def __init__(self, name, description, labelnames, namespace, subsystem):
        """Initialize the metric collector.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional metric namespace subsystem: Optional metric subsystem"""
```

```python
class SummaryCollector(MetricCollector):
    """Collector for summary metrics."""
```
*Methods:*
```python
    def __init__(self, name, description, labelnames, namespace, subsystem):
        """Initialize the summary collector.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional metric namespace subsystem: Optional metric subsystem"""
```
```python
    def observe(self, value, labels) -> None:
        """Record an observation.  Args: value: Value to observe labels: Optional label values"""
```

###### Module: decorators
*Metric decorators for measuring function performance.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics/decorators.py`

**Imports:**
```python
from __future__ import annotations
import functools
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Generator, Optional, cast
from app.logging import get_logger
from app.core.metrics.base import F
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.metrics.decorators")
```

**Functions:**
```python
def async_timed(metric_type, name, observe_func, labels_func, track_in_progress, track_in_progress_func, in_progress_metric) -> Callable[([F], F)]:
    """Decorator for timing async function execution.

Args: metric_type: Type of metric (histogram or summary) name: Metric name observe_func: Function to call for recording observations labels_func: Optional function to generate label values from function args track_in_progress: Whether to track in-progress operations track_in_progress_func: Function to call for tracking in-progress operations in_progress_metric: Optional name of gauge metric for tracking in-progress operations

Returns: Decorator function"""
```

```python
def timed(metric_type, name, observe_func, labels_func, track_in_progress, track_in_progress_func, in_progress_metric) -> Callable[([F], F)]:
    """Decorator for timing function execution.

Args: metric_type: Type of metric (histogram or summary) name: Metric name observe_func: Function to call for recording observations labels_func: Optional function to generate label values from function args track_in_progress: Whether to track in-progress operations track_in_progress_func: Function to call for tracking in-progress operations in_progress_metric: Optional name of gauge metric for tracking in-progress operations

Returns: Decorator function"""
```

```python
@contextmanager
def timer(metric_type, name, observe_func, labels, track_in_progress, track_in_progress_func, in_progress_metric) -> Generator[(None, None, None)]:
    """Context manager for timing operations.

Args: metric_type: Type of metric (histogram or summary) name: Metric name observe_func: Function to call for recording observations labels: Optional label values track_in_progress: Whether to track in-progress operations track_in_progress_func: Function to call for tracking in-progress operations in_progress_metric: Optional name of gauge metric for tracking in-progress operations"""
```

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics/exceptions.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
```

**Classes:**
```python
class MetricsConfigurationException(MetricsException):
    """Exception for metrics configuration errors."""
```
*Methods:*
```python
    def __init__(self, message, details, original_exception) -> None:
        """Initialize the metrics configuration exception.

Args: message: Error message details: Error details original_exception: Original causing exception"""
```

```python
class MetricsException(AppException):
    """Base exception for metrics-related errors."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the metrics exception.

Args: message: Error message code: Error code details: Error details status_code: HTTP status code original_exception: Original causing exception"""
```

```python
class MetricsOperationException(MetricsException):
    """Exception for metrics operation errors."""
```
*Methods:*
```python
    def __init__(self, message, operation, details, original_exception) -> None:
        """Initialize the metrics operation exception.

Args: message: Error message operation: The operation that failed details: Error details original_exception: Original causing exception"""
```

###### Module: manager
*Core metrics functionality.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics/manager.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple
from app.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag, MetricType, MetricsConfig
from app.core.metrics.collectors import CounterCollector, GaugeCollector, HistogramCollector, SummaryCollector
from app.core.metrics.decorators import async_timed, timed
from app.core.metrics.prometheus import PrometheusManager
from app.core.metrics.trackers import CacheTracker, DatabaseTracker, HttpTracker, ServiceTracker
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.metrics.manager")
```

**Functions:**
```python
def async_timed_function(name, metric_type, labels_func, track_in_progress_flag, in_progress_metric) -> Callable:
    """Create a decorator for timing async function execution.

Args: name: Metric name metric_type: Type of metric (histogram or summary) labels_func: Optional function to generate label values from function args track_in_progress_flag: Whether to track in-progress operations in_progress_metric: Optional name of gauge metric for tracking in-progress operations

Returns: Decorator function"""
```

```python
def create_counter(name, description, labelnames, namespace, subsystem) -> CounterCollector:
    """Create a new counter metric.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional metric namespace subsystem: Optional metric subsystem

Returns: CounterCollector object"""
```

```python
def create_gauge(name, description, labelnames, namespace, subsystem) -> GaugeCollector:
    """Create a new gauge metric.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional metric namespace subsystem: Optional metric subsystem

Returns: GaugeCollector object"""
```

```python
def create_histogram(name, description, labelnames, buckets, namespace, subsystem) -> HistogramCollector:
    """Create a new histogram metric.

Args: name: Metric name description: Metric description labelnames: Optional list of label names buckets: Optional histogram buckets namespace: Optional metric namespace subsystem: Optional metric subsystem

Returns: HistogramCollector object"""
```

```python
def create_summary(name, description, labelnames, namespace, subsystem) -> SummaryCollector:
    """Create a new summary metric.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional metric namespace subsystem: Optional metric subsystem

Returns: SummaryCollector object"""
```

```python
def get_current_metrics() -> Dict[(str, Dict[(str, Any)])]:
    """Get the current values of all metrics.  Returns: Dictionary of metric values by name"""
```

```python
def increment_counter(name, amount, labels) -> None:
    """Increment a counter metric.

Args: name: Metric name amount: Amount to increment by labels: Optional label values"""
```

```python
async def initialize(config) -> None:
    """Initialize the metrics system.  Args: config: Optional metrics configuration"""
```

```python
def observe_histogram(name, value, labels) -> None:
    """Record an observation in a histogram metric.

Args: name: Metric name value: Value to observe labels: Optional label values"""
```

```python
def observe_summary(name, value, labels) -> None:
    """Record an observation in a summary metric.

Args: name: Metric name value: Value to observe labels: Optional label values"""
```

```python
def set_gauge(name, value, labels) -> None:
    """Set a gauge metric value.

Args: name: Metric name value: Value to set labels: Optional label values"""
```

```python
async def shutdown() -> None:
    """Shutdown the metrics system."""
```

```python
def timed_function(name, metric_type, labels_func, track_in_progress_flag, in_progress_metric) -> Callable:
    """Create a decorator for timing function execution.

Args: name: Metric name metric_type: Type of metric (histogram or summary) labels_func: Optional function to generate label values from function args track_in_progress_flag: Whether to track in-progress operations in_progress_metric: Optional name of gauge metric for tracking in-progress operations

Returns: Decorator function"""
```

```python
def track_cache_operation(operation, backend, hit, duration, component) -> None:
    """Track cache operation metrics.

Args: operation: Cache operation (get, set, delete) backend: Cache backend (memory, redis) hit: Whether the operation was a cache hit duration: Operation duration in seconds component: Component using the cache"""
```

```python
def track_db_query(operation, entity, duration, error) -> None:
    """Track database query metrics.

Args: operation: Database operation (e.g., SELECT, INSERT) entity: Entity being queried duration: Query duration in seconds error: Optional error message if query failed"""
```

```python
def track_in_progress(metric_name, labels, count) -> None:
    """Track in-progress operations using gauges.

Args: metric_name: Name of the gauge metric to update labels: Label values that uniquely identify the operation count: Number to adjust the gauge by (1 for start, -1 for end)"""
```

```python
def track_request(method, endpoint, status_code, duration, error_code) -> None:
    """Track HTTP request metrics.

Args: method: HTTP method endpoint: Request endpoint status_code: Response status code duration: Request duration in seconds error_code: Optional error code if request failed"""
```

```python
def track_service_call(component, action, duration, error) -> None:
    """Track service call metrics.

Args: component: Service component name action: Action being performed duration: Call duration in seconds error: Optional error message if call failed"""
```

###### Module: prometheus
*Prometheus integration for metrics.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics/prometheus.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
from typing import Optional
from prometheus_client import REGISTRY, start_http_server, push_to_gateway
from app.logging import get_logger
from app.core.metrics.base import MetricsConfig
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.metrics.prometheus")
```

**Classes:**
```python
class PrometheusManager(object):
    """Manager for Prometheus integration."""
```
*Methods:*
```python
    def __init__(self, config):
        """Initialize the Prometheus manager.  Args: config: Metrics configuration"""
```
```python
    async def initialize(self) -> None:
        """Initialize Prometheus integration.

This sets up the HTTP metrics endpoint and/or push gateway based on configuration."""
```
```python
    async def shutdown(self) -> None:
        """Clean up Prometheus resources."""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics/service.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from app.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag, MetricType, MetricsConfig
from app.core.metrics.collectors import CounterCollector, GaugeCollector, HistogramCollector, SummaryCollector
from app.core.metrics.exceptions import MetricsConfigurationException
from app.core.metrics.manager import increment_counter, set_gauge, observe_histogram, observe_summary, create_counter, create_gauge, create_histogram, create_summary, track_request, track_db_query, track_service_call, track_cache_operation, track_in_progress, timed_function, async_timed_function, initialize as initialize_manager, shutdown as shutdown_manager, get_current_metrics
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.metrics.service")
F = F = TypeVar("F", bound=Callable[..., Any])
```

**Functions:**
```python
def get_metrics_service() -> MetricsService:
    """Get the metrics service singleton.  Returns: The metrics service instance"""
```

**Classes:**
```python
class MetricsService(object):
    """Service wrapper for the metrics system."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the metrics service."""
```
```python
    def async_timed_function(self, name, metric_type, labels_func, track_in_progress_flag, in_progress_metric) -> Callable:
        """Create a decorator for timing an async function.

Args: name: Metric name metric_type: Type of metric labels_func: Optional function to generate labels track_in_progress_flag: Whether to track in-progress operations in_progress_metric: Optional metric name for in-progress tracking

Returns: A decorator function"""
```
```python
    def create_counter(self, name, description, labelnames, namespace, subsystem) -> CounterCollector:
        """Create a counter metric.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional namespace subsystem: Optional subsystem

Returns: A counter collector instance"""
```
```python
    def create_gauge(self, name, description, labelnames, namespace, subsystem) -> GaugeCollector:
        """Create a gauge metric.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional namespace subsystem: Optional subsystem

Returns: A gauge collector instance"""
```
```python
    def create_histogram(self, name, description, labelnames, buckets, namespace, subsystem) -> HistogramCollector:
        """Create a histogram metric.

Args: name: Metric name description: Metric description labelnames: Optional list of label names buckets: Optional bucket definitions namespace: Optional namespace subsystem: Optional subsystem

Returns: A histogram collector instance"""
```
```python
    def create_summary(self, name, description, labelnames, namespace, subsystem) -> SummaryCollector:
        """Create a summary metric.

Args: name: Metric name description: Metric description labelnames: Optional list of label names namespace: Optional namespace subsystem: Optional subsystem

Returns: A summary collector instance"""
```
```python
    def get_current_metrics(self) -> Dict[(str, Dict[(str, Any)])]:
        """Get the current metrics data.  Returns: A dictionary of current metrics data"""
```
```python
    def increment_counter(self, name, amount, labels) -> None:
        """Increment a counter metric.

Args: name: Metric name amount: Amount to increment by labels: Optional label values"""
```
```python
    async def initialize(self, config) -> None:
        """Initialize the metrics service.  Args: config: Optional metrics configuration"""
```
```python
    def observe_histogram(self, name, value, labels) -> None:
        """Observe a value for a histogram metric.

Args: name: Metric name value: Value to observe labels: Optional label values"""
```
```python
    def observe_summary(self, name, value, labels) -> None:
        """Observe a value for a summary metric.

Args: name: Metric name value: Value to observe labels: Optional label values"""
```
```python
    def set_gauge(self, name, value, labels) -> None:
        """Set a gauge metric value.

Args: name: Metric name value: Value to set labels: Optional label values"""
```
```python
    async def shutdown(self) -> None:
        """Shutdown the metrics service."""
```
```python
    def timed_function(self, name, metric_type, labels_func, track_in_progress_flag, in_progress_metric) -> Callable:
        """Create a decorator for timing a function.

Args: name: Metric name metric_type: Type of metric labels_func: Optional function to generate labels track_in_progress_flag: Whether to track in-progress operations in_progress_metric: Optional metric name for in-progress tracking

Returns: A decorator function"""
```
```python
    def track_cache_operation(self, operation, backend, hit, duration, component) -> None:
        """Track a cache operation.

Args: operation: Cache operation type backend: Cache backend type hit: Whether the operation was a cache hit duration: Operation duration in seconds component: Optional component name"""
```
```python
    def track_db_query(self, operation, entity, duration, error) -> None:
        """Track a database query.

Args: operation: Database operation type entity: Entity being operated on duration: Query duration in seconds error: Optional error information"""
```
```python
    def track_in_progress(self, metric_name, labels, count) -> None:
        """Track in-progress operations.

Args: metric_name: Metric name labels: Label values count: Count to adjust by"""
```
```python
    def track_request(self, method, endpoint, status_code, duration, error_code) -> None:
        """Track an HTTP request.

Args: method: HTTP method endpoint: Request endpoint status_code: Response status code duration: Request duration in seconds error_code: Optional error code"""
```
```python
    def track_service_call(self, component, action, duration, error) -> None:
        """Track a service call.

Args: component: Service component action: Action being performed duration: Call duration in seconds error: Optional error information"""
```

###### Module: trackers
*Specialized trackers for common metric collection scenarios.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/metrics/trackers.py`

**Imports:**
```python
from __future__ import annotations
from typing import Optional
from app.logging import get_logger
from app.core.metrics.base import MetricName, MetricTag
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.metrics.trackers")
```

**Classes:**
```python
class CacheTracker(object):
    """Tracker for cache operation metrics."""
```
*Methods:*
```python
    def __init__(self, increment_counter_func, observe_histogram_func):
        """Initialize the cache tracker.

Args: increment_counter_func: Function to increment a counter observe_histogram_func: Function to observe a histogram"""
```
```python
    def track_operation(self, operation, backend, hit, duration, component) -> None:
        """Track cache operation metrics.

Args: operation: Cache operation (get, set, delete) backend: Cache backend (memory, redis) hit: Whether the operation was a cache hit duration: Operation duration in seconds component: Component using the cache"""
```

```python
class DatabaseTracker(object):
    """Tracker for database operation metrics."""
```
*Methods:*
```python
    def __init__(self, increment_counter_func, observe_histogram_func, increment_error_func):
        """Initialize the database tracker.

Args: increment_counter_func: Function to increment a counter observe_histogram_func: Function to observe a histogram increment_error_func: Function to increment an error counter"""
```
```python
    def track_query(self, operation, entity, duration, error) -> None:
        """Track database query metrics.

Args: operation: Database operation (e.g., SELECT, INSERT) entity: Entity being queried duration: Query duration in seconds error: Optional error message if query failed"""
```

```python
class HttpTracker(object):
    """Tracker for HTTP request metrics."""
```
*Methods:*
```python
    def __init__(self, increment_counter_func, observe_histogram_func, increment_error_func):
        """Initialize the HTTP tracker.

Args: increment_counter_func: Function to increment a counter observe_histogram_func: Function to observe a histogram increment_error_func: Function to increment an error counter"""
```
```python
    def track_request(self, method, endpoint, status_code, duration, error_code) -> None:
        """Track HTTP request metrics.

Args: method: HTTP method endpoint: Request endpoint status_code: Response status code duration: Request duration in seconds error_code: Optional error code if request failed"""
```

```python
class ServiceTracker(object):
    """Tracker for service call metrics."""
```
*Methods:*
```python
    def __init__(self, increment_counter_func, observe_histogram_func, increment_error_func):
        """Initialize the service tracker.

Args: increment_counter_func: Function to increment a counter observe_histogram_func: Function to observe a histogram increment_error_func: Function to increment an error counter"""
```
```python
    def track_call(self, component, action, duration, error) -> None:
        """Track service call metrics.

Args: component: Service component name action: Action being performed duration: Call duration in seconds error: Optional error message if call failed"""
```

##### Package: pagination
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.pagination.base import CursorPaginationParams, OffsetPaginationParams, PaginationResult, SortDirection, SortField
from app.core.pagination.exceptions import InvalidCursorException, InvalidPaginationParamsException, InvalidSortFieldException, PaginationException
from app.core.pagination.manager import initialize, paginate_with_cursor, paginate_with_offset, shutdown
from app.core.pagination.service import PaginationService, get_pagination_service
```

**Global Variables:**
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

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/base.py`

**Imports:**
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar
from pydantic import BaseModel, Field
from sqlalchemy.sql import Select
```

**Global Variables:**
```python
T = T = TypeVar("T")  # Entity type
R = R = TypeVar("R")  # Result type
```

**Classes:**
```python
class CursorPaginationParams(BaseModel):
    """Parameters for cursor-based pagination."""
```

```python
class OffsetPaginationParams(BaseModel):
    """Parameters for offset-based pagination."""
```

```python
class PaginationProvider(Protocol, Generic[(T, R)]):
    """Protocol for pagination providers."""
```
*Methods:*
```python
    async def paginate_with_cursor(self, query, params, transform_func) -> PaginationResult[R]:
        """Paginate query results using cursor-based pagination.

Args: query: SQLAlchemy select query params: Pagination parameters transform_func: Optional function to transform each result item

Returns: Paginated results"""
```
```python
    async def paginate_with_offset(self, query, params, transform_func) -> PaginationResult[R]:
        """Paginate query results using offset-based pagination.

Args: query: SQLAlchemy select query params: Pagination parameters transform_func: Optional function to transform each result item

Returns: Paginated results"""
```

```python
class PaginationResult(Generic[R]):
    """Result of a pagination operation."""
```
*Methods:*
```python
    def __init__(self, items, total, page, page_size, pages, next_cursor, has_next, has_prev) -> None:
        """Initialize the pagination result.

Args: items: List of items for the current page total: Total number of items (across all pages) page: Current page number (for offset pagination) page_size: Number of items per page (for offset pagination) pages: Total number of pages (for offset pagination) next_cursor: Cursor for fetching the next page (for cursor pagination) has_next: Whether there are more items after this page has_prev: Whether there are more items before this page"""
```
```python
    def to_dict(self) -> Dict[(str, Any)]:
        """Convert the pagination result to a dictionary.

Returns: Dictionary representation of the pagination result"""
```

```python
class SortDirection(str, Enum):
    """Sort direction options."""
```
*Class attributes:*
```python
ASC = 'asc'
DESC = 'desc'
```

```python
class SortField(BaseModel):
    """Model for sort field configuration."""
```

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/exceptions.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
```

**Classes:**
```python
class InvalidCursorException(PaginationException):
    """Exception raised when a pagination cursor is invalid."""
```
*Methods:*
```python
    def __init__(self, message, cursor, details, original_exception) -> None:
```

```python
class InvalidPaginationParamsException(PaginationException):
    """Exception raised when pagination parameters are invalid."""
```
*Methods:*
```python
    def __init__(self, message, params, details, original_exception) -> None:
```

```python
class InvalidSortFieldException(PaginationException):
    """Exception raised when a sort field is invalid."""
```
*Methods:*
```python
    def __init__(self, field, model, message, details, original_exception) -> None:
```

```python
class PaginationException(AppException):
    """Base exception for pagination errors."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
```

###### Module: factory
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/factory.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Generic, Optional, Type, TypeVar, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.logging import get_logger
from app.core.pagination.base import PaginationProvider
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.pagination.factory")
T = T = TypeVar("T")  # Entity type
R = R = TypeVar("R")  # Result type
```

**Classes:**
```python
class PaginationProviderFactory(Generic[(T, R)]):
    """Factory for creating pagination provider instances."""
```
*Methods:*
```python
@classmethod
    def clear_cache(cls) -> None:
        """Clear provider cache."""
```
```python
@classmethod
    def create_provider(cls, provider_type, db, model_class, response_model, **kwargs) -> PaginationProvider[(T, R)]:
        """Create a pagination provider of the specified type.

Args: provider_type: The type of provider to create ('offset', 'cursor') db: Database session model_class: SQLAlchemy model class response_model: Response model type (for generic type inference) **kwargs: Additional provider configuration

Returns: PaginationProvider: The created provider

Raises: ValueError: If the provider type is not supported"""
```
```python
@classmethod
    def register_provider(cls, name, provider_class) -> None:
        """Register a new pagination provider type.

Args: name: Provider type name provider_class: Provider class

Raises: ValueError: If a provider with the same name is already registered"""
```

###### Module: manager
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/manager.py`

**Imports:**
```python
from __future__ import annotations
import time
from typing import Any, Callable, Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.core.exceptions import ValidationException
from app.core.pagination.base import CursorPaginationParams, OffsetPaginationParams, PaginationResult
from app.core.pagination.exceptions import InvalidCursorException, InvalidPaginationParamsException
from app.core.pagination.factory import PaginationProviderFactory
from app.core.pagination.providers import CursorPaginationProvider, OffsetPaginationProvider
from app.logging import get_logger
from app.core.dependency_manager import get_dependency
from app.core.metrics.base import MetricName
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.pagination.manager")
HAS_METRICS = False
T = T = TypeVar("T")
R = R = TypeVar("R")
```

**Functions:**
```python
async def initialize() -> None:
    """Initialize the pagination system."""
```

```python
async def paginate_with_cursor(db, model_class, query, params, transform_func, response_model) -> PaginationResult[Any]:
    """Paginate query results using cursor-based pagination.

Args: db: Database session model_class: SQLAlchemy model class query: SQLAlchemy select query params: Cursor pagination parameters transform_func: Optional function to transform each result item response_model: Optional Pydantic model to convert results

Returns: PaginationResult with paginated items and metadata

Raises: InvalidCursorException: If the cursor is invalid InvalidPaginationParamsException: If pagination parameters are invalid ValidationException: If other validation errors occur"""
```

```python
async def paginate_with_offset(db, model_class, query, params, transform_func, response_model) -> PaginationResult[Any]:
    """Paginate query results using offset-based pagination.

Args: db: Database session model_class: SQLAlchemy model class query: SQLAlchemy select query params: Offset pagination parameters transform_func: Optional function to transform each result item response_model: Optional Pydantic model to convert results

Returns: PaginationResult with paginated items and metadata

Raises: InvalidPaginationParamsException: If pagination parameters are invalid ValidationException: If other validation errors occur"""
```

```python
async def shutdown() -> None:
    """Shutdown the pagination system and clean up resources."""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/service.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Callable, Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.core.pagination.base import CursorPaginationParams, OffsetPaginationParams, PaginationResult
from app.core.pagination.manager import paginate_with_cursor, paginate_with_offset
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.pagination.service")
T = T = TypeVar("T")
R = R = TypeVar("R")
```

**Functions:**
```python
def get_pagination_service(db) -> PaginationService:
    """Get or create a pagination service instance.

Args: db: Optional database session

Returns: PaginationService instance"""
```

**Classes:**
```python
class PaginationService(object):
    """Service for handling pagination operations.

This service provides methods for paginating query results using both offset-based and cursor-based pagination strategies."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the pagination service.  Args: db: Optional database session"""
```
```python
    async def initialize(self) -> None:
        """Initialize the pagination service."""
```
```python
    async def paginate_with_cursor(self, model_class, query, params, transform_func, response_model, db) -> PaginationResult[Any]:
        """Paginate query results using cursor-based pagination.

Args: model_class: SQLAlchemy model class query: SQLAlchemy select query params: Cursor pagination parameters transform_func: Optional function to transform each result item response_model: Optional Pydantic model to convert results db: Optional database session (overrides the one set in constructor)

Returns: PaginationResult with paginated items and metadata

Raises: ValueError: If no database session is provided InvalidCursorException: If the cursor is invalid InvalidPaginationParamsException: If pagination parameters are invalid"""
```
```python
    async def paginate_with_offset(self, model_class, query, params, transform_func, response_model, db) -> PaginationResult[Any]:
        """Paginate query results using offset-based pagination.

Args: model_class: SQLAlchemy model class query: SQLAlchemy select query params: Offset pagination parameters transform_func: Optional function to transform each result item response_model: Optional Pydantic model to convert results db: Optional database session (overrides the one set in constructor)

Returns: PaginationResult with paginated items and metadata

Raises: ValueError: If no database session is provided InvalidPaginationParamsException: If pagination parameters are invalid"""
```
```python
    async def shutdown(self) -> None:
        """Shutdown the pagination service."""
```

###### Package: providers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/providers`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/providers/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.pagination.providers.cursor import CursorPaginationProvider
from app.core.pagination.providers.offset import OffsetPaginationProvider
```

**Global Variables:**
```python
__all__ = __all__ = ["OffsetPaginationProvider", "CursorPaginationProvider"]
```

####### Module: cursor
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/providers/cursor.py`

**Imports:**
```python
from __future__ import annotations
import base64
import json
from datetime import datetime
import uuid
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, cast
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.logging import get_logger
from app.db.utils import count_query, execute_query
from app.core.pagination.base import CursorPaginationParams, PaginationProvider, PaginationResult, SortDirection, SortField
from app.core.pagination.exceptions import InvalidCursorException, InvalidSortFieldException
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.pagination.providers.cursor")
T = T = TypeVar("T")
R = R = TypeVar("R")
```

**Classes:**
```python
class CursorPaginationProvider(Generic[(T, R)], PaginationProvider[(T, R)]):
    """Cursor-based pagination provider implementation.

This provider implements pagination using the cursor-based approach, which is suitable for large datasets and continuous scrolling interfaces."""
```
*Methods:*
```python
    def __init__(self, db, model_class) -> None:
        """Initialize the cursor pagination provider.

Args: db: Database session model_class: SQLAlchemy model class"""
```
```python
    async def paginate_with_cursor(self, query, params, transform_func) -> PaginationResult[R]:
        """Paginate query results using cursor-based pagination.

Args: query: SQLAlchemy select query params: Cursor pagination parameters transform_func: Optional function to transform each result item

Returns: PaginationResult with paginated items and metadata

Raises: InvalidCursorException: If the cursor is invalid InvalidSortFieldException: If a sort field is invalid"""
```
```python
    async def paginate_with_offset(self, query, params, transform_func) -> PaginationResult[R]:
        """Offset-based pagination is not supported by this provider.

Args: query: SQLAlchemy select query params: Offset pagination parameters transform_func: Optional function to transform each result item

Raises: NotImplementedError: Always raised because this method is not supported"""
```

####### Module: offset
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/pagination/providers/offset.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Callable, Generic, List, Optional, TypeVar, cast
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from app.logging import get_logger
from app.db.utils import count_query, execute_query
from app.core.pagination.base import OffsetPaginationParams, PaginationProvider, PaginationResult, SortDirection, SortField
from app.core.pagination.exceptions import InvalidSortFieldException
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.pagination.providers.offset")
T = T = TypeVar("T")
R = R = TypeVar("R")
```

**Classes:**
```python
class OffsetPaginationProvider(Generic[(T, R)], PaginationProvider[(T, R)]):
    """Offset-based pagination provider implementation.

This provider implements pagination using the offset-based approach, which is suitable for most use cases where the total count is needed."""
```
*Methods:*
```python
    def __init__(self, db, model_class) -> None:
        """Initialize the offset pagination provider.

Args: db: Database session model_class: SQLAlchemy model class"""
```
```python
    async def paginate_with_cursor(self, query, params, transform_func) -> PaginationResult[R]:
        """Cursor-based pagination is not supported by this provider.

Args: query: SQLAlchemy select query params: Cursor pagination parameters transform_func: Optional function to transform each result item

Raises: NotImplementedError: Always raised because this method is not supported"""
```
```python
    async def paginate_with_offset(self, query, params, transform_func) -> PaginationResult[R]:
        """Paginate query results using offset-based pagination.

Args: query: SQLAlchemy select query params: Offset pagination parameters transform_func: Optional function to transform each result item

Returns: PaginationResult with paginated items and metadata

Raises: InvalidSortFieldException: If a sort field is invalid"""
```

##### Package: permissions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/permissions`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/permissions/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.permissions.models import Permission, UserRole, ROLE_PERMISSIONS
from app.core.permissions.checker import PermissionChecker, permissions
from app.core.permissions.decorators import require_permission, require_permissions, require_admin
from app.core.permissions.utils import get_user_by_id, check_owner_permission, has_any_permission, has_all_permissions
```

**Global Variables:**
```python
__all__ = __all__ = [
    # Models
    "Permission",
    "UserRole",
    "ROLE_PERMISSIONS",
    # Checker
    "PermissionChecker",
    "permissions",
    # Decorators
    "require_permission",
    "require_permissions",
    "require_admin",
    # Utilities
    "get_user_by_id",
    "check_owner_permission",
    "has_any_permission",
    "has_all_permissions",
]
```

###### Module: checker
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/permissions/checker.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, List, TYPE_CHECKING
from app.core.exceptions import PermissionDeniedException
from app.logging import get_logger
from app.core.permissions.models import Permission, ROLE_PERMISSIONS
from app.domains.users.models import User
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.permissions.checkers")
permissions = permissions = PermissionChecker()
```

**Classes:**
```python
class PermissionChecker(object):
    """Permission checker for authorization control.

This class provides methods to check if a user has the required permissions for a given action."""
```
*Methods:*
```python
@staticmethod
    def check_object_permission(user, obj, permission, owner_field) -> bool:
        """Check if a user has permission for a specific object.

This allows for object-level permissions where users can perform actions on objects they own, even if they don't have the global permission.

Args: user: User to check obj: Object to check permissions for permission: Required permission owner_field: Field name that contains the owner ID

Returns: bool: True if user has permission"""
```
```python
@staticmethod
    def ensure_object_permission(user, obj, permission, owner_field) -> None:
        """Ensure a user has permission for a specific object.

Args: user: User to check obj: Object to check permissions for permission: Required permission owner_field: Field name that contains the owner ID

Raises: PermissionDeniedException: If user doesn't have permission"""
```
```python
@staticmethod
    def has_permission(user, permission) -> bool:
        """Check if a user has a specific permission.

Args: user: User to check permission: Required permission

Returns: bool: True if user has the permission"""
```
```python
@staticmethod
    def has_permissions(user, permissions, require_all) -> bool:
        """Check if a user has multiple permissions.

Args: user: User to check permissions: Required permissions require_all: Whether all permissions are required (AND) or any (OR)

Returns: bool: True if user has the required permissions"""
```

###### Module: decorators
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/permissions/decorators.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Callable, List, TypeVar, cast, TYPE_CHECKING
from app.core.exceptions import PermissionDeniedException
from app.logging import get_logger
from app.core.permissions.checker import PermissionChecker
from app.core.permissions.models import Permission
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.permissions.decorators")
T = T = TypeVar("T", bound=Callable[..., Any])
```

**Functions:**
```python
def require_admin() -> Callable[([T], T)]:
    """Decorator to require admin role.  Returns: Callable: Decorator function"""
```

```python
def require_permission(permission) -> Callable[([T], T)]:
    """Decorator to require a specific permission.

Args: permission: Required permission

Returns: Callable: Decorator function"""
```

```python
def require_permissions(permissions, require_all) -> Callable[([T], T)]:
    """Decorator to require multiple permissions.

Args: permissions: Required permissions require_all: Whether all permissions are required (AND) or any (OR)

Returns: Callable: Decorator function"""
```

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/permissions/models.py`

**Imports:**
```python
from __future__ import annotations
import enum
from typing import Dict, Set, TYPE_CHECKING
from app.domains.users.models import UserRole
```

**Classes:**
```python
class Permission(str, enum.Enum):
    """Permission types for the application.

This enum defines all available permissions in the system. Permissions follow a resource:action format."""
```
*Class attributes:*
```python
USER_CREATE = 'user:create'
USER_READ = 'user:read'
USER_UPDATE = 'user:update'
USER_DELETE = 'user:delete'
USER_ADMIN = 'user:admin'
PRODUCT_CREATE = 'product:create'
PRODUCT_READ = 'product:read'
PRODUCT_UPDATE = 'product:update'
PRODUCT_DELETE = 'product:delete'
PRODUCT_ADMIN = 'product:admin'
MEDIA_CREATE = 'media:create'
MEDIA_READ = 'media:read'
MEDIA_UPDATE = 'media:update'
MEDIA_DELETE = 'media:delete'
MEDIA_ADMIN = 'media:admin'
FITMENT_CREATE = 'fitment:create'
FITMENT_READ = 'fitment:read'
FITMENT_UPDATE = 'fitment:update'
FITMENT_DELETE = 'fitment:delete'
FITMENT_ADMIN = 'fitment:admin'
COMPANY_CREATE = 'company:create'
COMPANY_READ = 'company:read'
COMPANY_UPDATE = 'company:update'
COMPANY_DELETE = 'company:delete'
COMPANY_ADMIN = 'company:admin'
SYSTEM_ADMIN = 'system:admin'
```

```python
class UserRole(str, enum.Enum):
    """User roles in the system."""
```
*Class attributes:*
```python
ADMIN = 'admin'
MANAGER = 'manager'
CLIENT = 'client'
DISTRIBUTOR = 'distributor'
READ_ONLY = 'read_only'
```

###### Module: permissions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/permissions/permissions.py`

**Imports:**
```python
from __future__ import annotations
from app.core.permissions.decorators import require_permission, require_permissions, require_admin
```

**Global Variables:**
```python
require_permission = require_permission = require_permission
require_permissions = require_permissions = require_permissions
require_admin = require_admin = require_admin
```

###### Module: utils
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/permissions/utils.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, List, Optional, Set, Union, TYPE_CHECKING
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
from app.domains.users.models import User
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.permissions.utils")
```

**Functions:**
```python
def check_owner_permission(user_id, entity_user_id, owner_field) -> bool:
    """Check if a user is the owner of an entity.

Args: user_id: User ID to check entity_user_id: User ID from the entity owner_field: Field name containing the owner ID

Returns: bool: True if user is the owner, False otherwise"""
```

```python
async def get_user_by_id(db, user_id) -> 'User':
    """Get user by ID.

Args: db: Database session user_id: User ID

Returns: User: User model

Raises: AuthenticationException: If user not found"""
```

```python
def has_all_permissions(user, permissions) -> bool:
    """Check if a user has all specified permissions.

Args: user: User to check permissions for permissions: List of permissions to check

Returns: bool: True if user has all permissions, False otherwise"""
```

```python
def has_any_permission(user, permissions) -> bool:
    """Check if a user has any of the specified permissions.

Args: user: User to check permissions for permissions: List of permissions to check

Returns: bool: True if user has any permission, False otherwise"""
```

##### Package: rate_limiting
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/rate_limiting`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/rate_limiting/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.rate_limiting.utils import check_rate_limit, get_ttl
from app.core.rate_limiting.exceptions import RateLimitingException, RateLimitExceededException, RateLimitingServiceException, RateLimitingConfigurationException
from app.core.rate_limiting.service import RateLimitingService, get_rate_limiting_service
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.rate_limiting.__init__")
__all__ = __all__ = [
    "RateLimitRule",
    "RateLimitStrategy",
    "RateLimiter",
    "initialize",
    "shutdown",
    "check_rate_limit",
    "get_ttl",
    "RateLimitingException",
    "RateLimitExceededException",
    "RateLimitingServiceException",
    "RateLimitingConfigurationException",
    "RateLimitingService",
    "get_rate_limiting_service",
]
```

**Functions:**
```python
async def initialize() -> None:
    """Initialize the rate limiting system.  This function is called during application startup."""
```

```python
async def shutdown() -> None:
    """Shut down the rate limiting system.  This function is called during application shutdown."""
```

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/rate_limiting/exceptions.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from app.core.exceptions.base import AppException, ErrorCategory, ErrorCode, ErrorSeverity
```

**Classes:**
```python
class RateLimitExceededException(RateLimitingException):
    """Exception raised when a rate limit is exceeded."""
```
*Methods:*
```python
    def __init__(self, message, details, headers, reset_seconds, original_exception) -> None:
        """Initialize a rate limit exceeded exception.

Args: message: Human-readable error message. details: Additional details about the error. headers: HTTP headers to include in the response. reset_seconds: Seconds until the rate limit resets. original_exception: The original exception that caused this one."""
```

```python
class RateLimitingConfigurationException(RateLimitingException):
    """Exception raised when the rate limiting configuration is invalid."""
```
*Methods:*
```python
    def __init__(self, message, details, original_exception) -> None:
        """Initialize a rate limiting configuration exception.

Args: message: Human-readable error message. details: Additional details about the error. original_exception: The original exception that caused this one."""
```

```python
class RateLimitingException(AppException):
    """Base exception for rate limiting errors."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize a rate limiting exception.

Args: message: Human-readable error message. code: Error code from ErrorCode enum. details: Additional details about the error. status_code: HTTP status code for the error. original_exception: The original exception that caused this one."""
```

```python
class RateLimitingServiceException(RateLimitingException):
    """Exception raised when the rate limiting service encounters an error."""
```
*Methods:*
```python
    def __init__(self, message, details, original_exception) -> None:
        """Initialize a rate limiting service exception.

Args: message: Human-readable error message. details: Additional details about the error. original_exception: The original exception that caused this one."""
```

###### Module: limiter
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/rate_limiting/limiter.py`

**Imports:**
```python
from __future__ import annotations
import time
from typing import Dict, Optional, Tuple
from fastapi import Request
from app.core.config import settings
from app.logging import get_logger
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.utils.redis_manager import get_redis_client, increment_counter
from app.core.dependency_manager import get_dependency
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.rate_limiting.limiter")
HAS_METRICS = False
```

**Classes:**
```python
class RateLimiter(object):
    """Rate limiter that enforces rate limits for various keys.

Supports both in-memory and Redis-based rate limiting with different strategies for generating rate limit keys."""
```
*Methods:*
```python
    def __init__(self, use_redis, prefix, default_rule) -> None:
        """Initialize the rate limiter.

Args: use_redis: Whether to use Redis for rate limiting. If None, will use Redis if the application is configured for it. prefix: Prefix for rate limit keys. default_rule: Default rate limit rule to apply."""
```
```python
    def get_key_for_request(self, request, rule) -> str:
        """Generate a rate limit key for a request.

Args: request: The request to generate a key for. rule: The rate limit rule that defines the key strategy.

Returns: A string key for rate limiting."""
```
```python
    async def is_rate_limited(self, key, rule) -> Tuple[(bool, int, int)]:
        """Check if a key is rate limited.

Args: key: The key to check. rule: Optional rate limit rule to apply. If not provided, the default rule will be used.

Returns: A tuple containing: - Whether the key is rate limited (True if limited) - The current count for the key - The maximum allowed count (limit)"""
```

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/rate_limiting/models.py`

**Imports:**
```python
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
```

**Classes:**
```python
@dataclass
class RateLimitRule(object):
    """Rule configuration for rate limiting.

Attributes: requests_per_window: Maximum number of requests allowed in the window. window_seconds: Size of the window in seconds. strategy: Strategy for determining the rate limit key. burst_multiplier: Multiplier for burst allowance above the limit. path_pattern: Pattern to match request paths this rule applies to. If None, applies to all paths. exclude_paths: List of path prefixes to exclude from rate limiting."""
```

```python
class RateLimitStrategy(str, Enum):
    """Strategy for determining the rate limit key."""
```
*Class attributes:*
```python
IP = 'ip'
USER = 'user'
COMBINED = 'combined'
```

###### Module: rate_limiter
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/rate_limiting/rate_limiter.py`

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/rate_limiting/service.py`

**Imports:**
```python
from __future__ import annotations
from typing import Dict, Optional, Tuple
from fastapi import Request
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule, RateLimitStrategy
from app.core.config import settings
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.rate_limiting.service")
```

**Functions:**
```python
def get_rate_limiting_service() -> RateLimitingService:
    """Get or create the rate limiting service singleton.  Returns: The rate limiting service instance."""
```

**Classes:**
```python
class RateLimitingService(object):
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the rate limiting service."""
```
```python
    def get_key_for_request(self, request, rule) -> str:
        """Generate a rate limit key for a request.

Args: request: The request to generate a key for. rule: The rate limit rule that defines the key strategy.

Returns: A string key for rate limiting.

Raises: RateLimitingServiceException: If the service is not initialized."""
```
```python
    async def initialize(self) -> None:
        """Initialize the rate limiting service.  If already initialized, this method does nothing."""
```
```python
    async def is_rate_limited(self, key, rule) -> Tuple[(bool, int, int)]:
        """Check if a key is rate limited.

Args: key: The key to check. rule: Optional rate limit rule to apply. If not provided, the default rule will be used.

Returns: A tuple containing: - Whether the key is rate limited (True if limited) - The current count for the key - The maximum allowed count (limit)

Raises: RateLimitingServiceException: If the service is not initialized."""
```
```python
    async def shutdown(self) -> None:
        """Shut down the rate limiting service.  If not initialized, this method does nothing."""
```

###### Module: utils
*Rate limiting utility functions.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/rate_limiting/utils.py`

**Imports:**
```python
from __future__ import annotations
import time
from typing import Tuple
from app.logging import get_logger
from app.utils.redis_manager import get_key, set_key
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.rate_limiting.utils")
```

**Functions:**
```python
async def check_rate_limit(key, max_requests, window_seconds) -> Tuple[(bool, int, int)]:
    """Check if a rate limit has been exceeded.

Args: key: The rate limit key. max_requests: The maximum number of requests allowed in the time window. window_seconds: The time window in seconds.

Returns: Tuple[bool, int, int]: A tuple containing a boolean indicating if the rate limit has been exceeded, the current request count, and the reset time in seconds."""
```

```python
async def get_ttl(key) -> int:
    """Get the TTL of a key in Redis.

Args: key: The key to get the TTL for.

Returns: int: The TTL in seconds, or 0 if the key doesn't exist or an error occurs."""
```

##### Package: security
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.security.api_keys import ApiKeyManager, generate_api_key, verify_api_key
from app.core.security.csrf import CsrfManager, generate_csrf_token, validate_csrf_token
from app.core.security.encryption import EncryptionManager, decrypt_data, encrypt_data, generate_secure_token
from app.core.security.models import ApiKeyData, PasswordPolicy, SecurityViolation, TokenClaimsModel, TokenPair, TokenType
from app.core.security.passwords import PasswordManager, get_password_hash, validate_password_policy, verify_password
from app.core.security.tokens import TokenManager, add_token_to_blacklist, create_token, create_token_pair, decode_token, is_token_blacklisted, refresh_tokens, revoke_token
from app.core.security.validation import ValidationManager, detect_suspicious_content, get_security_headers, is_trusted_ip, is_valid_enum_value, is_valid_hostname, moderate_content, sanitize_input, validate_json_input
from app.core.security.dependencies import get_current_user_id, get_token_from_header, oauth2_scheme
```

**Global Variables:**
```python
__all__ = __all__ = [
    # API Keys
    "ApiKeyManager",
    "generate_api_key",
    "verify_api_key",
    # CSRF
    "CsrfManager",
    "generate_csrf_token",
    "validate_csrf_token",
    # Dependencies
    "get_current_user_id",
    "get_token_from_header",
    "oauth2_scheme",
    # Encryption
    "EncryptionManager",
    "decrypt_data",
    "encrypt_data",
    "generate_secure_token",
    # Models
    "ApiKeyData",
    "PasswordPolicy",
    "SecurityViolation",
    "TokenClaimsModel",
    "TokenPair",
    "TokenType",
    # Passwords
    "PasswordManager",
    "get_password_hash",
    "validate_password_policy",
    "verify_password",
    # Tokens
    "TokenManager",
    "add_token_to_blacklist",
    "create_token",
    "create_token_pair",
    "decode_token",
    "is_token_blacklisted",
    "refresh_tokens",
    "revoke_token",
    # Validation
    "ValidationManager",
    "detect_suspicious_content",
    "get_security_headers",
    "is_trusted_ip",
    "is_valid_enum_value",
    "is_valid_hostname",
    "moderate_content",
    "sanitize_input",
    "validate_json_input",
]
```

###### Module: api_keys
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security/api_keys.py`

**Imports:**
```python
from __future__ import annotations
import hashlib
import hmac
import secrets
import uuid
import datetime
from typing import List, Optional
from app.logging import get_logger
from app.core.security.models import ApiKeyData, TokenType
from app.core.security.tokens import create_token
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.security.api_keys")
```

**Functions:**
```python
def generate_api_key(user_id, name, permissions) -> ApiKeyData:
    """Generate a new API key.

Args: user_id: The user ID. name: The name of the API key. permissions: Optional list of permissions.

Returns: ApiKeyData: The generated API key data."""
```

```python
def verify_api_key(api_key, stored_hash) -> bool:
    """Verify an API key against its stored hash.

Args: api_key: The API key to verify. stored_hash: The stored hash to verify against.

Returns: bool: True if the API key is valid, False otherwise."""
```

**Classes:**
```python
class ApiKeyManager(object):
    """Manager for API key-related functionality."""
```
*Methods:*
```python
    def generate_api_key(self, user_id, name, permissions) -> ApiKeyData:
        """Generate a new API key.

Args: user_id: The user ID. name: The name of the API key. permissions: Optional list of permissions.

Returns: ApiKeyData: The generated API key data."""
```
```python
    def parse_api_key(self, api_key) -> Optional[str]:
        """Parse an API key to extract its ID.

Args: api_key: The API key to parse.

Returns: Optional[str]: The API key ID, or None if parsing fails."""
```
```python
    def verify_api_key(self, api_key, stored_hash) -> bool:
        """Verify an API key against its stored hash.

Args: api_key: The API key to verify. stored_hash: The stored hash to verify against.

Returns: bool: True if the API key is valid, False otherwise."""
```

###### Module: csrf
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security/csrf.py`

**Imports:**
```python
from __future__ import annotations
import hmac
import secrets
import time
from typing import Optional, Tuple
from app.core.config import settings
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.security.csrf")
```

**Functions:**
```python
def generate_csrf_token(session_id) -> str:
    """Generate a CSRF token.

Args: session_id: The session ID to bind the token to.

Returns: str: The generated CSRF token."""
```

```python
def validate_csrf_token(token, session_id) -> bool:
    """Validate a CSRF token.

Args: token: The token to validate. session_id: The session ID to validate against.

Returns: bool: True if the token is valid, False otherwise."""
```

**Classes:**
```python
class CsrfManager(object):
    """Manager for CSRF token-related functionality."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the CSRF manager."""
```
```python
    def generate_token(self, session_id) -> str:
        """Generate a CSRF token.

Args: session_id: The session ID to bind the token to.

Returns: str: The generated CSRF token."""
```
```python
    def parse_token(self, token) -> Optional[Tuple[(str, int, str, str)]]:
        """Parse a CSRF token.

Args: token: The token to parse.

Returns: Optional[Tuple[str, int, str, str]]: A tuple containing the parsed token parts, or None if parsing fails."""
```
```python
    def validate_token(self, token, session_id) -> bool:
        """Validate a CSRF token.

Args: token: The token to validate. session_id: The session ID to validate against.

Returns: bool: True if the token is valid, False otherwise."""
```

###### Module: dependencies
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security/dependencies.py`

**Imports:**
```python
from __future__ import annotations
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
from app.core.security.tokens import decode_token
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.security.dependencies")
oauth2_scheme = oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
optional_oauth2_scheme = optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False
)
```

**Functions:**
```python
async def get_current_user_id(token) -> str:
    """Get the current user ID from a token.

Args: token: The token to decode.

Returns: str: The user ID.

Raises: AuthenticationException: If the token is invalid."""
```

```python
async def get_token_from_header(token) -> str:
    """Get a token from the Authorization header.

Args: token: The token from the OAuth2 scheme.

Returns: str: The token."""
```

###### Module: encryption
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security/encryption.py`

**Imports:**
```python
from __future__ import annotations
import base64
import binascii
import json
from typing import Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings
from app.core.exceptions import SecurityException, ErrorCode, ConfigurationException
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.security.encryption")
```

**Functions:**
```python
def decrypt_data(encrypted_data) -> Union[(str, dict)]:
    """Decrypt data.

Args: encrypted_data: The encrypted data as a base64-encoded string.

Returns: Union[str, dict]: The decrypted data.

Raises: SecurityException: If decryption fails."""
```

```python
def encrypt_data(data) -> str:
    """Encrypt data.

Args: data: The data to encrypt.

Returns: str: The encrypted data as a base64-encoded string.

Raises: SecurityException: If encryption fails."""
```

```python
def generate_secure_token(length) -> str:
    """Generate a cryptographically secure random token.

Args: length: The length of the token in bytes.

Returns: str: The generated token.

Raises: SecurityException: If token generation fails. ValueError: If the token length is too short."""
```

**Classes:**
```python
class EncryptionManager(object):
    """Manager for encryption-related functionality."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the encryption manager."""
```
```python
    def decrypt_data(self, encrypted_data) -> Union[(str, dict)]:
        """Decrypt data.

Args: encrypted_data: The encrypted data as a base64-encoded string.

Returns: Union[str, dict]: The decrypted data."""
```
```python
    def encrypt_data(self, data) -> str:
        """Encrypt data.

Args: data: The data to encrypt.

Returns: str: The encrypted data as a base64-encoded string."""
```
```python
    def generate_secure_token(self, length) -> str:
        """Generate a cryptographically secure random token.

Args: length: The length of the token in bytes.

Returns: str: The generated token."""
```

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security/models.py`

**Imports:**
```python
from __future__ import annotations
import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
```

**Classes:**
```python
class ApiKeyData(BaseModel):
    """Model representing API key data."""
```

```python
class PasswordPolicy(BaseModel):
    """Model representing password policy settings."""
```

```python
class SecurityViolation(str, Enum):
    """Types of security violations that can occur."""
```
*Class attributes:*
```python
INVALID_TOKEN = 'invalid_token'
EXPIRED_TOKEN = 'expired_token'
CSRF_VIOLATION = 'csrf_violation'
RATE_LIMIT_EXCEEDED = 'rate_limit_exceeded'
BRUTE_FORCE_ATTEMPT = 'brute_force_attempt'
SUSPICIOUS_ACTIVITY = 'suspicious_activity'
UNAUTHORIZED_ACCESS = 'unauthorized_access'
INVALID_IP = 'invalid_ip'
PERMISSION_VIOLATION = 'permission_violation'
INJECTION_ATTEMPT = 'injection_attempt'
XSS_ATTEMPT = 'xss_attempt'
```

```python
class TokenClaimsModel(BaseModel):
    """Model representing the claims in a JWT token."""
```

```python
class TokenPair(BaseModel):
    """Model representing an access and refresh token pair."""
```

```python
class TokenType(str, Enum):
    """Types of tokens used in the system."""
```
*Class attributes:*
```python
ACCESS = 'access'
REFRESH = 'refresh'
RESET_PASSWORD = 'reset_password'
EMAIL_VERIFICATION = 'email_verification'
INVITATION = 'invitation'
API_KEY = 'api_key'
CSRF = 'csrf'
SESSION = 'session'
```

###### Module: passwords
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security/passwords.py`

**Imports:**
```python
from __future__ import annotations
import re
from pathlib import Path
from typing import Optional, Set, Tuple
from passlib.context import CryptContext
from app.core.config import settings
from app.logging import get_logger
from app.core.security.models import PasswordPolicy
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.security.passwords")
pwd_context = pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**Functions:**
```python
def get_password_hash(password) -> str:
    """Hash a password using bcrypt.

Args: password: The password to hash.

Returns: str: The hashed password."""
```

```python
async def validate_password_policy(password, user_id) -> Tuple[(bool, Optional[str])]:
    """Validate a password against the password policy.

Args: password: The password to validate. user_id: Optional user ID for password history checks.

Returns: Tuple[bool, Optional[str]]: A tuple containing a boolean indicating if the password is valid and an optional error message if it's not."""
```

```python
def verify_password(plain_password, hashed_password) -> bool:
    """Verify a password against its hash.

Args: plain_password: The plain text password. hashed_password: The hashed password to verify against.

Returns: bool: True if the password matches the hash, False otherwise."""
```

**Classes:**
```python
class PasswordManager(object):
    """Manager for password-related functionality."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the password manager."""
```
```python
    def hash_password(self, password) -> str:
        """Hash a password using bcrypt.

Args: password: The password to hash.

Returns: str: The hashed password."""
```
```python
    async def validate_password_policy(self, password, user_id) -> Tuple[(bool, Optional[str])]:
        """Validate a password against the password policy.

Args: password: The password to validate. user_id: Optional user ID for password history checks.

Returns: Tuple[bool, Optional[str]]: A tuple containing a boolean indicating if the password is valid and an optional error message if it's not."""
```
```python
    def verify_password(self, plain_password, hashed_password) -> bool:
        """Verify a password against its hash.

Args: plain_password: The plain text password. hashed_password: The hashed password to verify against.

Returns: bool: True if the password matches the hash, False otherwise."""
```

###### Module: tokens
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security/tokens.py`

**Imports:**
```python
from __future__ import annotations
import datetime
import uuid
from typing import Any, Dict, List, Optional, Union
from jose import JWTError, jwt
from pydantic import ValidationError
from app.core.config import settings
from app.core.exceptions import AuthenticationException
from app.logging import get_logger
from app.core.security.models import TokenClaimsModel, TokenPair, TokenType
from app.utils.redis_manager import get_key, set_key
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.security.tokens")
```

**Functions:**
```python
async def add_token_to_blacklist(token_jti, expires_at) -> None:
    """Add a token to the blacklist.

Args: token_jti: The JWT ID of the token. expires_at: The expiration time of the token."""
```

```python
def create_token(subject, token_type, expires_delta, role, permissions, user_data) -> str:
    """Create a JWT token.

Args: subject: The subject of the token (usually the user ID). token_type: The type of token to create. expires_delta: Optional expiration time delta. role: Optional user role. permissions: Optional list of permissions. user_data: Optional additional user data.

Returns: str: The encoded JWT token."""
```

```python
def create_token_pair(user_id, role, permissions, user_data) -> TokenPair:
    """Create an access and refresh token pair.

Args: user_id: The user ID. role: The user role. permissions: Optional list of permissions. user_data: Optional additional user data.

Returns: TokenPair: A model containing the access and refresh tokens."""
```

```python
async def decode_token(token) -> TokenClaimsModel:
    """Decode and validate a JWT token.

Args: token: The token to decode.

Returns: TokenClaimsModel: The decoded token claims.

Raises: AuthenticationException: If the token is invalid."""
```

```python
def generate_token_jti() -> str:
    """Generate a unique JWT ID.  Returns: str: A unique identifier for a JWT token."""
```

```python
async def is_token_blacklisted(token_jti) -> bool:
    """Check if a token is blacklisted.

Args: token_jti: The JWT ID of the token.

Returns: bool: True if the token is blacklisted, False otherwise."""
```

```python
async def refresh_tokens(refresh_token) -> TokenPair:
    """Refresh an access token using a refresh token.

Args: refresh_token: The refresh token.

Returns: TokenPair: A new token pair.

Raises: AuthenticationException: If the token is invalid."""
```

```python
async def revoke_token(token) -> None:
    """Revoke a token by adding it to the blacklist.

Args: token: The token to revoke.

Raises: AuthenticationException: If the token is invalid."""
```

**Classes:**
```python
class TokenManager(object):
    """Manager for token-related functionality."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the token manager."""
```

###### Module: validation
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security/validation.py`

**Imports:**
```python
from __future__ import annotations
import ipaddress
import json
import re
from typing import Any, Dict, Set, Tuple, Optional, Type
from enum import Enum
from app.core.config import settings
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.security.validation")
```

**Functions:**
```python
def detect_suspicious_content(content) -> bool:
    """Detect potentially malicious content.

Args: content: The content to check.

Returns: bool: True if suspicious content is detected, False otherwise."""
```

```python
def get_security_headers() -> Dict[(str, str)]:
    """Get security headers for HTTP responses.

Returns: Dict[str, str]: A dictionary of security headers."""
```

```python
def is_trusted_ip(ip_address) -> bool:
    """Check if an IP address is in the trusted proxies list.

Args: ip_address: The IP address to check.

Returns: bool: True if the IP address is trusted, False otherwise."""
```

```python
def is_valid_enum_value(enum_class, value) -> bool:
    """Check if a value is a valid member of an Enum class.

Args: enum_class: The Enum class to check against. value: The value to check.

Returns: bool: True if the value is a valid enum member, False otherwise."""
```

```python
def is_valid_hostname(hostname) -> bool:
    """Validate a hostname.

Args: hostname: The hostname to validate.

Returns: bool: True if the hostname is valid, False otherwise."""
```

```python
def moderate_content(content, content_type) -> Tuple[(bool, Optional[str])]:
    """Moderate content for inappropriate or harmful material.

Args: content: The content to moderate. content_type: The type of content (text, image, etc.)

Returns: Tuple[bool, Optional[str]]: A tuple containing a boolean indicating if the content is acceptable and an optional reason if it's not."""
```

```python
def sanitize_input(input_str) -> str:
    """Sanitize user input by escaping HTML characters.

Args: input_str: The input string to sanitize.

Returns: str: The sanitized string."""
```

```python
def validate_json_input(json_data) -> bool:
    """Validate JSON input for suspicious content and structure.

Args: json_data: The JSON data to validate.

Returns: bool: True if the JSON is valid and safe, False otherwise."""
```

**Classes:**
```python
class ValidationManager(object):
    """Manager for input validation and sanitization."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the validation manager."""
```
```python
    def detect_suspicious_content(self, content) -> bool:
        """Detect potentially malicious content.

Args: content: The content to check.

Returns: bool: True if suspicious content is detected, False otherwise."""
```
```python
    def get_security_headers(self) -> Dict[(str, str)]:
        """Get security headers for HTTP responses.

Returns: Dict[str, str]: A dictionary of security headers."""
```
```python
    def is_trusted_ip(self, ip_address) -> bool:
        """Check if an IP address is in the trusted proxies list.

Args: ip_address: The IP address to check.

Returns: bool: True if the IP address is trusted, False otherwise."""
```
```python
    def is_valid_enum_value(self, enum_class, value) -> bool:
        """Check if a value is a valid member of an Enum class.

Args: enum_class: The Enum class to check against. value: The value to check.

Returns: bool: True if the value is a valid enum member, False otherwise."""
```
```python
    def is_valid_hostname(self, hostname) -> bool:
        """Validate a hostname.

Args: hostname: The hostname to validate.

Returns: bool: True if the hostname is valid, False otherwise."""
```
```python
    def moderate_content(self, content, content_type) -> Tuple[(bool, Optional[str])]:
        """Moderate content for inappropriate or harmful material.

Args: content: The content to moderate. content_type: The type of content (text, image, etc.)

Returns: Tuple[bool, Optional[str]]: A tuple containing a boolean indicating if the content is acceptable and an optional reason if it's not."""
```
```python
    def sanitize_input(self, input_str) -> str:
        """Sanitize user input by escaping HTML characters.

Args: input_str: The input string to sanitize.

Returns: str: The sanitized string."""
```
```python
    def validate_json_input(self, json_data) -> bool:
        """Validate JSON input for suspicious content.

Args: json_data: The JSON data to validate.

Returns: bool: True if the JSON is valid and safe, False otherwise."""
```

##### Package: startup
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/startup`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/startup/__init__.py`

###### Module: as400_sync
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/startup/as400_sync.py`

**Imports:**
```python
from __future__ import annotations
from app.core.config.integrations.as400 import as400_settings
from app.logging import get_logger
from app.services.as400_sync_service import as400_sync_service, SyncEntityType
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.startup.as400_sync")
```

**Functions:**
```python
async def initialize_as400_sync() -> None:
    """Initialize the AS400 sync service.  This function should be called during application startup."""
```

```python
async def shutdown_as400_sync() -> None:
    """Shut down the AS400 sync service.  This function should be called during application shutdown."""
```

##### Package: validation
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/validation`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/validation/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.db import UniqueValidator
from app.core.validation.factory import ValidatorFactory
from app.core.validation.manager import validate_data, validate_model, validate_email, validate_phone, validate_date, validate_length, validate_range, validate_regex, validate_required, validate_unique, validate_url, validate_uuid, validate_credit_card, validate_ip_address, validate_password_strength, validate_enum, validate_composite, create_validator, register_validator, initialize, shutdown
from app.core.validation.service import ValidationService, get_validation_service
from app.core.validation.validators import CreditCardValidator, DateValidator, EmailValidator, EnumValidator, IPAddressValidator, LengthValidator, PasswordValidator, PhoneValidator, RangeValidator, RegexValidator, RequiredValidator, URLValidator, UUIDValidator
```

**Global Variables:**
```python
__all__ = __all__ = [
    # Base types
    "ValidationResult",
    "Validator",
    "ValidatorFactory",
    # High-level validation functions
    "validate_data",
    "validate_model",
    # Type-specific validation functions
    "validate_email",
    "validate_phone",
    "validate_date",
    "validate_length",
    "validate_range",
    "validate_regex",
    "validate_required",
    "validate_unique",
    "validate_url",
    "validate_uuid",
    "validate_credit_card",
    "validate_ip_address",
    "validate_password_strength",
    "validate_enum",
    "validate_composite",
    # Factory and registration functions
    "create_validator",
    "register_validator",
    # Lifecycle functions
    "initialize",
    "shutdown",
    # Service
    "ValidationService",
    "get_validation_service",
    # Validator implementations
    "CreditCardValidator",
    "DateValidator",
    "EmailValidator",
    "EnumValidator",
    "IPAddressValidator",
    "LengthValidator",
    "PasswordValidator",
    "PhoneValidator",
    "RangeValidator",
    "RegexValidator",
    "RequiredValidator",
    "URLValidator",
    "UUIDValidator",
    "UniqueValidator",
]
```

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/validation/base.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Union, runtime_checkable
from pydantic import BaseModel, Field
```

**Global Variables:**
```python
T = T = TypeVar("T")
R = R = TypeVar("R", bound=bool)
```

**Classes:**
```python
class ValidationResult(BaseModel):
    """Result of a validation operation.

This class represents the result of a validation operation, including whether the validation was successful and any validation errors."""
```
*Methods:*
```python
    def add_error(self, msg, error_type, loc, **context) -> None:
        """Add an error to the validation result.

Args: msg: The error message error_type: The type of error loc: Optional location of the error (field name or path) **context: Additional context for the error"""
```
```python
@property
    def error_messages(self) -> List[str]:
        """Get a list of error messages.  Returns: List[str]: List of error message strings"""
```
```python
@property
    def has_errors(self) -> bool:
        """Check if there are any validation errors.  Returns: bool: True if there are errors, False otherwise"""
```

```python
@runtime_checkable
class Validator(Protocol):
    """Protocol defining the interface for validators.

Validators must implement the validate method, which takes a value and optional additional parameters and returns a ValidationResult."""
```
*Methods:*
```python
    def validate(self, value, **kwargs) -> ValidationResult:
        """Validate a value.

Args: value: The value to validate **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```
```python
    async def validate_async(self, value, **kwargs) -> ValidationResult:
        """Asynchronously validate a value.

This method is optional. Validators that require async operations should implement this method. Default implementation raises NotImplementedError.

Args: value: The value to validate **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation

Raises: NotImplementedError: If the validator doesn't support async validation"""
```

```python
@runtime_checkable
class ValidatorFactory(Protocol):
    """Protocol defining the interface for validator factories.

Validator factories must implement the create_validator method, which creates and returns validator instances based on a validator type."""
```
*Methods:*
```python
    def create_validator(self, validator_type, **options) -> Validator:
        """Create a validator instance.

Args: validator_type: The type of validator to create **options: Additional options for the validator

Returns: Validator: An instance of the requested validator"""
```

###### Module: db
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/validation/db.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Type, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.validation.db")
```

**Classes:**
```python
class UniqueValidator(Validator):
    """Validator that checks if a value is unique in the database.

This validator requires an async database session and must be used with the validate_async method."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the unique validator.  Args: db: The SQLAlchemy async database session"""
```
```python
    def validate(self, value, field, model, exclude_id, **kwargs) -> ValidationResult:
        """Synchronous validation method - not supported.

Raises: ValidationException: Always, as this validator requires async operations"""
```
```python
    async def validate_async(self, value, field, model, exclude_id, **kwargs) -> ValidationResult:
        """Asynchronously validate that a value is unique in the database.

Args: value: The value to check for uniqueness field: The field name in the model model: The SQLAlchemy model class exclude_id: Optional ID to exclude from the uniqueness check **kwargs: Additional keyword arguments

Returns: ValidationResult: The validation result"""
```

###### Module: factory
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/validation/factory.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Type
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.core.validation.base import Validator
from app.core.validation.validators import CreditCardValidator, DateValidator, EmailValidator, EnumValidator, IPAddressValidator, LengthValidator, PasswordValidator, PhoneValidator, RangeValidator, RegexValidator, RequiredValidator, URLValidator, UUIDValidator
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.validation.factory")
```

**Classes:**
```python
class ValidatorFactory(object):
    """Factory for creating validator instances.

This class provides methods to register and create different types of validators."""
```
*Methods:*
```python
@classmethod
    def create_validator(cls, validator_type, **options) -> Validator:
        """Create a validator instance of the specified type.

Args: validator_type: The type of validator to create **options: Additional options for the validator

Returns: Validator: An instance of the requested validator

Raises: ValidationException: If the validator type is not supported"""
```
```python
@classmethod
    def get_available_validators(cls) -> List[str]:
        """Get a list of all available validator types.

Returns: List[str]: List of registered validator type names"""
```
```python
@classmethod
    def register_validator(cls, name, validator_class) -> None:
        """Register a new validator type.

Args: name: The name to register the validator under validator_class: The validator class to register

Raises: ValidationException: If a validator with the same name is already registered"""
```

###### Module: manager
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/validation/manager.py`

**Imports:**
```python
from __future__ import annotations
from datetime import date, datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union, cast
from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.error import resource_not_found, validation_error
from app.core.exceptions import BusinessException, ErrorCode, ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.db import UniqueValidator
from app.core.validation.factory import ValidatorFactory
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.validation.manager")
```

**Functions:**
```python
def create_validator(rule_type, **params) -> Callable[([Any], bool)]:
    """Create a validator function for a specific rule type.

Args: rule_type: The type of validator to create **params: Additional parameters for the validator

Returns: Callable[[Any], bool]: A function that takes a value and returns a boolean

Raises: ValidationException: If the validator type is not supported"""
```

```python
async def initialize() -> None:
    """Initialize the validation system."""
```

```python
def register_validator(name, validator_class) -> None:
    """Register a custom validator.

Args: name: The name to register the validator under validator_class: The validator class to register

Raises: ValidationException: If a validator with the same name is already registered"""
```

```python
async def shutdown() -> None:
    """Shutdown the validation system."""
```

```python
def validate_composite(data, rules) -> Tuple[(bool, List[Dict[(str, Any)]])]:
    """Validate data against multiple validation rules.

Args: data: The data to validate rules: Dictionary mapping field names to validation rules

Returns: Tuple[bool, List[Dict[str, Any]]]: A tuple containing a boolean indicating validation success and a list of validation errors"""
```

```python
def validate_credit_card(card_number) -> bool:
    """Validate a credit card number.

Args: card_number: The credit card number to validate

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_data(data, schema_class) -> BaseModel:
    """Validate data against a Pydantic schema.

Args: data: The data to validate schema_class: The Pydantic model class to validate against

Returns: BaseModel: The validated model instance

Raises: ValidationException: If validation fails"""
```

```python
def validate_date(value, min_date, max_date, format_str) -> bool:
    """Validate a date value.

Args: value: The date to validate (string, date, or datetime) min_date: Optional minimum allowed date max_date: Optional maximum allowed date format_str: Optional date format string for parsing string dates

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_email(email) -> bool:
    """Validate an email address.

Args: email: The email address to validate

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_enum(value, enum_class) -> bool:
    """Validate that a value is a valid enum value.

Args: value: The value to validate enum_class: The enum class to validate against

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_ip_address(ip, version) -> bool:
    """Validate an IP address.

Args: ip: The IP address to validate version: Optional IP version (4 or 6)

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_length(value, min_length, max_length) -> bool:
    """Validate string length.

Args: value: The string to validate min_length: Optional minimum length max_length: Optional maximum length

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_model(model, include, exclude) -> None:
    """Validate an existing Pydantic model instance.

Args: model: The model instance to validate include: Optional set of fields to include in validation exclude: Optional set of fields to exclude from validation

Raises: ValidationException: If validation fails"""
```

```python
def validate_password_strength(password, min_length, require_lowercase, require_uppercase, require_digit, require_special) -> bool:
    """Validate password strength.

Args: password: The password to validate min_length: Minimum password length require_lowercase: Whether to require lowercase letters require_uppercase: Whether to require uppercase letters require_digit: Whether to require digits require_special: Whether to require special characters

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_phone(phone) -> bool:
    """Validate a phone number.

Args: phone: The phone number to validate

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_range(value, min_value, max_value) -> bool:
    """Validate numeric range.

Args: value: The number to validate min_value: Optional minimum value max_value: Optional maximum value

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_regex(value, pattern) -> bool:
    """Validate string against a regex pattern.

Args: value: The string to validate pattern: The regex pattern to validate against

Returns: bool: True if valid, False otherwise"""
```

```python
def validate_required(value) -> bool:
    """Validate that a value is not None or empty.

Args: value: The value to validate

Returns: bool: True if valid, False otherwise"""
```

```python
async def validate_unique(field, value, model, db, exclude_id) -> bool:
    """Validate that a field value is unique in the database.

Args: field: The field name to check value: The field value to check model: The SQLAlchemy model class db: The database session exclude_id: Optional ID to exclude from the uniqueness check

Returns: bool: True if unique, False otherwise"""
```

```python
def validate_url(url) -> bool:
    """Validate a URL.  Args: url: The URL to validate  Returns: bool: True if valid, False otherwise"""
```

```python
def validate_uuid(value) -> bool:
    """Validate a UUID string.

Args: value: The UUID string to validate

Returns: bool: True if valid, False otherwise"""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/validation/service.py`

**Imports:**
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union
from datetime import date, datetime
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
from app.core.validation.factory import ValidatorFactory
from app.core.validation.manager import validate_composite, validate_credit_card, validate_data, validate_date, validate_email, validate_enum, validate_ip_address, validate_length, validate_model, validate_password_strength, validate_phone, validate_range, validate_regex, validate_required, validate_unique, validate_url, validate_uuid
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.validation.service")
```

**Functions:**
```python
def get_validation_service(db) -> ValidationService:
    """Get the validation service instance.

This function is intended to be used with the dependency injection system.

Args: db: Optional database session

Returns: ValidationService: The validation service instance"""
```

**Classes:**
```python
class ValidationService(object):
    """Service for performing validations throughout the application.

This service provides a high-level interface to the validation system, with methods for validating different types of data."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the validation service.

Args: db: Optional database session for validations requiring database access"""
```
```python
    def create_validator(self, validator_type, **options) -> Validator:
        """Create a validator instance.

Args: validator_type: The type of validator to create **options: Additional options for the validator

Returns: Validator: The validator instance

Raises: ValidationException: If the validator type is not supported"""
```
```python
    def get_available_validators(self) -> List[str]:
        """Get a list of all available validator types.

Returns: List[str]: List of registered validator type names"""
```
```python
    async def initialize(self) -> None:
        """Initialize the validation service."""
```
```python
    async def shutdown(self) -> None:
        """Shutdown the validation service."""
```
```python
    def validate_composite(self, data, rules) -> Tuple[(bool, List[Dict[(str, Any)]])]:
        """Validate data against multiple validation rules.

Args: data: The data to validate rules: Dictionary mapping field names to validation rules

Returns: Tuple[bool, List[Dict[str, Any]]]: A tuple containing a boolean indicating validation success and a list of validation errors"""
```
```python
    def validate_credit_card(self, card_number) -> bool:
        """Validate a credit card number.

Args: card_number: The credit card number to validate

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_data(self, data, schema_class) -> BaseModel:
        """Validate data against a Pydantic schema.

Args: data: The data to validate schema_class: The Pydantic model class to validate against

Returns: BaseModel: The validated model instance

Raises: ValidationException: If validation fails"""
```
```python
    def validate_date(self, value, min_date, max_date, format_str) -> bool:
        """Validate a date value.

Args: value: The date to validate (string, date, or datetime) min_date: Optional minimum allowed date max_date: Optional maximum allowed date format_str: Optional date format string for parsing string dates

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_email(self, email) -> bool:
        """Validate an email address.

Args: email: The email address to validate

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_enum(self, value, enum_class) -> bool:
        """Validate that a value is a valid enum value.

Args: value: The value to validate enum_class: The enum class to validate against

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_ip_address(self, ip, version) -> bool:
        """Validate an IP address.

Args: ip: The IP address to validate version: Optional IP version (4 or 6)

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_length(self, value, min_length, max_length) -> bool:
        """Validate string length.

Args: value: The string to validate min_length: Optional minimum length max_length: Optional maximum length

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_model(self, model, include, exclude) -> None:
        """Validate an existing Pydantic model instance.

Args: model: The model instance to validate include: Optional set of fields to include in validation exclude: Optional set of fields to exclude from validation

Raises: ValidationException: If validation fails"""
```
```python
    def validate_password_strength(self, password, min_length, require_lowercase, require_uppercase, require_digit, require_special) -> bool:
        """Validate password strength.

Args: password: The password to validate min_length: Minimum password length require_lowercase: Whether to require lowercase letters require_uppercase: Whether to require uppercase letters require_digit: Whether to require digits require_special: Whether to require special characters

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_phone(self, phone) -> bool:
        """Validate a phone number.

Args: phone: The phone number to validate

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_range(self, value, min_value, max_value) -> bool:
        """Validate numeric range.

Args: value: The number to validate min_value: Optional minimum value max_value: Optional maximum value

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_regex(self, value, pattern) -> bool:
        """Validate string against a regex pattern.

Args: value: The string to validate pattern: The regex pattern to validate against

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_required(self, value) -> bool:
        """Validate that a value is not None or empty.

Args: value: The value to validate

Returns: bool: True if valid, False otherwise"""
```
```python
    async def validate_unique(self, field, value, model, exclude_id) -> bool:
        """Validate that a field value is unique in the database.

Args: field: The field name to check value: The field value to check model: The SQLAlchemy model class exclude_id: Optional ID to exclude from the uniqueness check

Returns: bool: True if unique, False otherwise

Raises: ValidationException: If no database session is available"""
```
```python
    def validate_url(self, url) -> bool:
        """Validate a URL.  Args: url: The URL to validate  Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_uuid(self, value) -> bool:
        """Validate a UUID string.

Args: value: The UUID string to validate

Returns: bool: True if valid, False otherwise"""
```

###### Module: validators
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/validation/validators.py`

**Imports:**
```python
from __future__ import annotations
import ipaddress
import re
import uuid
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union
from app.logging import get_logger
from app.core.validation.base import ValidationResult, Validator
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.validation.validators")
```

**Classes:**
```python
class CreditCardValidator(Validator):
    """Validator for credit card numbers."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the credit card validator."""
```
```python
    def validate(self, value, **kwargs) -> ValidationResult:
        """Validate a credit card number using the Luhn algorithm.

Args: value: The credit card number to validate **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class DateValidator(Validator):
    """Validator for dates."""
```
*Methods:*
```python
    def validate(self, value, min_date, max_date, format_str, **kwargs) -> ValidationResult:
        """Validate a date.

Args: value: The date to validate min_date: Optional minimum date max_date: Optional maximum date format_str: Optional date format string for parsing string dates **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class EmailValidator(Validator):
    """Validator for email addresses."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the email validator."""
```
```python
    def validate(self, value, **kwargs) -> ValidationResult:
        """Validate an email address.

Args: value: The email address to validate **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class EnumValidator(Validator):
    """Validator for enum values."""
```
*Methods:*
```python
    def validate(self, value, enum_class, **kwargs) -> ValidationResult:
        """Validate that a value is a valid enum member.

Args: value: The value to validate enum_class: The Enum class to validate against **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class IPAddressValidator(Validator):
    """Validator for IP addresses."""
```
*Methods:*
```python
    def validate(self, value, version, **kwargs) -> ValidationResult:
        """Validate an IP address.

Args: value: The IP address to validate version: Optional IP version (4 or 6) **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class LengthValidator(Validator):
    """Validator for string length."""
```
*Methods:*
```python
    def validate(self, value, min_length, max_length, **kwargs) -> ValidationResult:
        """Validate the length of a string.

Args: value: The string to validate min_length: Optional minimum length max_length: Optional maximum length **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class PasswordValidator(Validator):
    """Validator for password strength."""
```
*Methods:*
```python
    def validate(self, value, min_length, require_lowercase, require_uppercase, require_digit, require_special, **kwargs) -> ValidationResult:
        """Validate password strength.

Args: value: The password to validate min_length: Minimum password length require_lowercase: Whether to require at least one lowercase letter require_uppercase: Whether to require at least one uppercase letter require_digit: Whether to require at least one digit require_special: Whether to require at least one special character **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class PhoneValidator(Validator):
    """Validator for phone numbers."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the phone validator."""
```
```python
    def validate(self, value, **kwargs) -> ValidationResult:
        """Validate a phone number.

Args: value: The phone number to validate **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class RangeValidator(Validator):
    """Validator for numeric ranges."""
```
*Methods:*
```python
    def validate(self, value, min_value, max_value, **kwargs) -> ValidationResult:
        """Validate a numeric value against a range.

Args: value: The number to validate min_value: Optional minimum value max_value: Optional maximum value **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class RegexValidator(Validator):
    """Validator for regex patterns."""
```
*Methods:*
```python
    def validate(self, value, pattern, **kwargs) -> ValidationResult:
        """Validate a string against a regex pattern.

Args: value: The string to validate pattern: The regex pattern to validate against **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class RequiredValidator(Validator):
    """Validator for required values."""
```
*Methods:*
```python
    def validate(self, value, **kwargs) -> ValidationResult:
        """Validate that a value is not empty.

Args: value: The value to validate **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class URLValidator(Validator):
    """Validator for URLs."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the URL validator."""
```
```python
    def validate(self, value, **kwargs) -> ValidationResult:
        """Validate a URL.

Args: value: The URL to validate **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

```python
class UUIDValidator(Validator):
    """Validator for UUIDs."""
```
*Methods:*
```python
    def validate(self, value, **kwargs) -> ValidationResult:
        """Validate a UUID.

Args: value: The UUID string to validate **kwargs: Additional validation parameters

Returns: ValidationResult: The result of the validation"""
```

#### Package: data_import
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/__init__.py`

**Imports:**
```python
from __future__ import annotations
```

##### Package: commands
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/commands`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/commands/__init__.py`

**Imports:**
```python
from __future__ import annotations
import typer
from app.data_import.commands.import_products import app as import_products_app
```

**Global Variables:**
```python
app = app = typer.Typer()
__all__ = __all__ = ["app"]
```

###### Module: import_products
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/commands/import_products.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import json
import sys
from typing import Dict, Optional
import typer
from app.logging import get_logger
from app.data_import.connectors.file_connector import FileConnector, FileConnectionConfig
from app.data_import.connectors.filemaker_connector import FileMakerConnector, FileMakerConnectionConfig
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.pipeline.product_pipeline import ProductPipeline
from app.data_import.processors.product_processor import ProductMappingConfig, ProductProcessor
from app.db.session import get_db_context
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.commands.import_products")
app = app = typer.Typer()
```

**Functions:**
```python
@app.command()
def import_products(source_type, config_file, query, dry_run, output_file, dsn, username, password, database, file_path, mapping_file, file_type, disable_ssl, limit) -> None:
    """Import products from FileMaker or file.

This command extracts product data from FileMaker or a file, processes and validates it, and imports it into the database."""
```

###### Module: sync_as400
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/commands/sync_as400.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, Optional
import typer
from app.core.config.integrations.as400 import get_as400_connector_config
from app.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
from app.services.as400_sync_service import as400_sync_service, SyncEntityType
```

**Global Variables:**
```python
logger = logger = get_logger("app.commands.sync_as400")
app = app = typer.Typer()
```

**Functions:**
```python
@app.command()
def schedule(entity_type, delay) -> None:
    """Schedule AS400 data synchronization for a specific entity type.

This command schedules the synchronization of data from AS400 to run after the specified delay."""
```

```python
@app.command()
def status(entity_type, json_output) -> None:
    """Get the status of AS400 data synchronization.

This command retrieves the status of all or a specific entity type's synchronization operations."""
```

```python
@app.command()
def sync(entity_type, force, dry_run, output_file) -> None:
    """Run AS400 data synchronization for a specific entity type.

This command triggers the synchronization of data from AS400 to the application database for the specified entity type."""
```

```python
@app.command()
def test_connection() -> None:
    """Test the AS400 connection.

This command verifies that the application can connect to the AS400 database using the configured settings."""
```

##### Package: connectors
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/connectors`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/connectors/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector, FileConnectionConfig
from app.data_import.connectors.filemaker_connector import FileMakerConnector, FileMakerConnectionConfig
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
```

**Global Variables:**
```python
__all__ = __all__ = [
    "Connector",
    "FileConnector",
    "FileConnectionConfig",
    "FileMakerConnector",
    "FileMakerConnectionConfig",
    "AS400Connector",
    "AS400ConnectionConfig",
]
```

###### Module: as400_connector
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/connectors/as400_connector.py`

**Imports:**
```python
from __future__ import annotations
import os
from typing import Any, Dict, List, Optional, Set
import pyodbc
from pydantic import BaseModel, Field, SecretStr, validator
from cryptography.fernet import Fernet
from app.core.exceptions import DatabaseException, SecurityException
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.connectors.as400_connector")
```

**Classes:**
```python
class AS400ConnectionConfig(BaseModel):
    """Configuration for connecting to AS400/iSeries databases securely."""
```
*Methods:*
```python
@validator('allowed_tables', 'allowed_schemas')
    def validate_allowed_lists(cls, v) -> Optional[List[str]]:
        """Validate and normalize allowed lists."""
```
```python
@validator('port')
    def validate_port(cls, v) -> Optional[int]:
        """Validate port is within allowed range."""
```

```python
class AS400Connector(object):
    """Secure connector for AS400/iSeries databases.

Implements multiple security layers: 1. SecretStr for password handling 2. Whitelist for allowed tables and schemas 3. Read-only operations only 4. SSL/TLS encryption when available 5. Timeouts to prevent hanging connections 6. Detailed audit logging"""
```
*Methods:*
```python
    def __init__(self, config) -> None:
        """Initialize the AS400 connector with secure configuration.

Args: config: Configuration for the AS400 connection"""
```
```python
    async def close(self) -> None:
        """Safely close the AS400 connection.  Raises: DatabaseException: If closing the connection fails"""
```
```python
    async def connect(self) -> None:
        """Establish a secure connection to the AS400 database.

Raises: SecurityException: If security requirements aren't met DatabaseException: If connection fails ConfigurationException: If configuration is invalid"""
```
```python
    async def extract(self, query, limit, **params) -> List[Dict[(str, Any)]]:
        """Securely extract data from AS400.

Args: query: SQL query or table name limit: Maximum number of records to return **params: Query parameters

Returns: List of dictionaries containing the query results

Raises: SecurityException: If the query attempts to access unauthorized tables DatabaseException: If the query fails to execute"""
```

```python
class Config(object):
    """Pydantic config."""
```
*Class attributes:*
```python
validate_assignment = True
extra = 'forbid'
```

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/connectors/base.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Protocol, TypeVar, Optional
```

**Global Variables:**
```python
T = T = TypeVar("T")
```

**Classes:**
```python
class Connector(Protocol):
    """Protocol for data source connectors."""
```
*Methods:*
```python
    async def close(self) -> None:
        """Close the connection.  Raises: ConnectionError: If closing the connection fails"""
```
```python
    async def connect(self) -> None:
        """Establish connection to the data source.

Raises: ConnectionError: If connection cannot be established"""
```
```python
    async def extract(self, query, limit, **params) -> List[Dict[(str, Any)]]:
        """Extract data from the source.

Args: query: Query string or identifier for the data to extract limit: Maximum number of records to retrieve params: Additional parameters for the query

Returns: List of records as dictionaries

Raises: ValueError: If query is invalid ConnectionError: If connection issues occur during extraction"""
```

###### Module: file_connector
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/connectors/file_connector.py`

**Imports:**
```python
from __future__ import annotations
import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, validator
from app.core.exceptions import ConfigurationException
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.connectors.file_connector")
```

**Classes:**
```python
class FileConnectionConfig(BaseModel):
    """Configuration for file connections."""
```
*Methods:*
```python
@validator('file_path')
    def validate_file_path(cls, v) -> str:
```
```python
@validator('file_type')
    def validate_file_type(cls, v, values) -> str:
```

```python
class FileConnector(object):
    """Connector for file-based data sources (CSV, JSON)."""
```
*Methods:*
```python
    def __init__(self, config) -> None:
        """Initialize the File connector.  Args: config: File connection configuration"""
```
```python
    async def close(self) -> None:
        """Close the connection (clear file data from memory)."""
```
```python
    async def connect(self) -> None:
        """Establish connection to the file.

This method loads the file data into memory.

Raises: ConfigurationException: If the file cannot be loaded"""
```
```python
    async def extract(self, query, limit, **params) -> List[Dict[(str, Any)]]:
        """Extract data from the file.

The query parameter is optional for file connectors and can be used to filter the data based on specific criteria.

Args: query: Optional filter criteria limit: Maximum number of records to retrieve params: Additional parameters

Returns: List of records as dictionaries

Raises: ConfigurationException: If extraction fails"""
```

###### Module: filemaker_connector
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/connectors/filemaker_connector.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional
import pyodbc
from pydantic import BaseModel, Field, validator
from app.core.exceptions import DatabaseException
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.connectors.filemaker_connector")
```

**Classes:**
```python
class FileMakerConnectionConfig(BaseModel):
    """Configuration for FileMaker ODBC connection."""
```
*Methods:*
```python
@validator('port')
    def validate_port(cls, v) -> Optional[int]:
```

```python
class FileMakerConnector(object):
    """Connector for FileMaker databases using ODBC."""
```
*Methods:*
```python
    def __init__(self, config) -> None:
        """Initialize the FileMaker connector.  Args: config: FileMaker connection configuration"""
```
```python
    async def close(self) -> None:
        """Close the connection to FileMaker.  Raises: DatabaseException: If closing the connection fails"""
```
```python
    async def connect(self) -> None:
        """Establish connection to the FileMaker database.  Raises: DatabaseException: If connection fails"""
```
```python
    async def extract(self, query, limit, **params) -> List[Dict[(str, Any)]]:
        """Extract data from FileMaker.

Args: query: SQL query or table/layout name limit: Maximum number of records to retrieve params: Parameters for the query

Returns: List of records as dictionaries

Raises: DatabaseException: If extraction fails"""
```

##### Package: importers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/importers`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/importers/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.data_import.importers.base import Importer
from app.data_import.importers.product_importer import ProductImporter
```

**Global Variables:**
```python
__all__ = __all__ = [
    "Importer",
    "ProductImporter",
]
```

###### Module: as400_importers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/importers/as400_importers.py`

**Imports:**
```python
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, TypeVar
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseException
from app.logging import get_logger
from app.domains.products.models import Product, ProductMeasurement, ProductPricing, ProductStock, Manufacturer, PriceType
from app.domains.currency.models import Currency
from app.domains.reference.models import Warehouse
from app.domains.products.schemas import ProductCreate, ProductMeasurementCreate, ProductStock as ProductStockSchema
from app.data_import.importers.base import Importer
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.importers.as400_importers")
T = T = TypeVar("T")
```

**Classes:**
```python
class AS400BaseImporter(Importer[T]):
    """Base class for AS400 data importers.

Provides common functionality for AS400 data import operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the importer with a database session.  Args: db: SQLAlchemy async session"""
```
```python
    async def get_existing_entities(self, id_field, id_values, model) -> Dict[(Any, Any)]:
        """Get existing entities by their IDs.

Args: id_field: Field name for the ID id_values: List of ID values to look up model: SQLAlchemy model class

Returns: Dictionary mapping ID values to entity instances"""
```
```python
    async def track_sync(self, entity_type, created, updated, errors) -> None:
        """Track synchronization statistics.

Args: entity_type: Type of entity being synced created: Number of created entities updated: Number of updated entities errors: Number of errors"""
```

```python
class ProductAS400Importer(AS400BaseImporter[ProductCreate]):
    """Importer for product data from AS400."""
```
*Methods:*
```python
    async def import_data(self, data) -> Dict[(str, Any)]:
        """Import product data from AS400.

Args: data: List of product data to import

Returns: Dictionary with import results"""
```

```python
class ProductMeasurementImporter(AS400BaseImporter[ProductMeasurementCreate]):
    """Importer for product measurement data from AS400."""
```
*Methods:*
```python
    async def import_data(self, data) -> Dict[(str, Any)]:
        """Import product measurement data.

Args: data: List of measurements to import

Returns: Dictionary with import results"""
```

```python
class ProductPricingImporter(AS400BaseImporter[Any]):
    """Importer for product pricing data from AS400."""
```
*Methods:*
```python
    async def import_data(self, data) -> Dict[(str, Any)]:
        """Import product pricing data.

Args: data: List of pricing data to import

Returns: Dictionary with import results"""
```

```python
class ProductStockImporter(AS400BaseImporter[ProductStockSchema]):
    """Importer for product stock/inventory data from AS400."""
```
*Methods:*
```python
    async def import_data(self, data) -> Dict[(str, Any)]:
        """Import product stock data.

Args: data: List of stock data to import

Returns: Dictionary with import results"""
```

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/importers/base.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Protocol, TypeVar
```

**Global Variables:**
```python
T = T = TypeVar("T")
```

**Classes:**
```python
class Importer(Protocol[T]):
    """Protocol for data importers."""
```
*Methods:*
```python
    async def import_data(self, data) -> Dict[(str, Any)]:
        """Import data into the target system.

Args: data: List of records to import

Returns: Dictionary with import statistics

Raises: ValueError: If data cannot be imported DatabaseError: If database operations fail"""
```

###### Module: product_importer
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/importers/product_importer.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseException
from app.logging import get_logger
from app.domains.products.models import Product, ProductDescription, ProductMarketing
from app.domains.products.schemas import ProductCreate
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.importers.product_importer")
```

**Classes:**
```python
class ProductImporter(object):
    """Importer for product data."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the product importer.  Args: db: Database session"""
```
```python
    async def import_data(self, data) -> Dict[(str, Any)]:
        """Import product data into the database.

Args: data: List of validated product data to import

Returns: Dictionary with import statistics

Raises: DatabaseException: If database operations fail"""
```

##### Package: pipeline
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/pipeline`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/pipeline/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.data_import.pipeline.base import Pipeline
from app.data_import.pipeline.product_pipeline import ProductPipeline
```

**Global Variables:**
```python
__all__ = __all__ = [
    "Pipeline",
    "ProductPipeline",
]
```

###### Module: as400_pipeline
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/pipeline/as400_pipeline.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import time
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel
from app.core.exceptions import AppException
from app.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector
from app.data_import.importers.base import Importer
from app.data_import.processors.as400_processor import AS400BaseProcessor
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.pipeline.as400_pipeline")
T = T = TypeVar("T", bound=BaseModel)
```

**Classes:**
```python
class AS400Pipeline(Generic[T]):
    """Pipeline for synchronizing data from AS400 to the application database.

Orchestrates the extract, transform, load (ETL) process for AS400 data."""
```
*Methods:*
```python
    def __init__(self, connector, processor, importer, dry_run, chunk_size) -> None:
        """Initialize the AS400 pipeline.

Args: connector: AS400 connector for data extraction processor: Processor for data transformation importer: Importer for loading data dry_run: If True, don't actually import data chunk_size: Number of records to process at once"""
```
```python
    async def run(self, query, limit, **params) -> Dict[(str, Any)]:
        """Run the sync pipeline.

Args: query: SQL query or table name limit: Maximum number of records to process **params: Additional parameters for query

Returns: Dictionary with sync results"""
```

```python
class ParallelAS400Pipeline(Generic[T]):
    """Parallel pipeline for AS400 data synchronization.

Runs multiple pipelines concurrently for faster processing."""
```
*Methods:*
```python
    def __init__(self, pipelines, max_workers) -> None:
        """Initialize the parallel pipeline.

Args: pipelines: List of pipelines to run max_workers: Maximum number of concurrent workers"""
```
```python
    async def run(self) -> Dict[(str, Any)]:
        """Run all pipelines concurrently.  Returns: Dictionary with combined results"""
```

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/pipeline/base.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Protocol, TypeVar, Union
from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector
from app.data_import.connectors.filemaker_connector import FileMakerConnector
from app.data_import.importers.base import Importer
from app.data_import.processors.base import Processor
```

**Global Variables:**
```python
T = T = TypeVar("T")
```

**Classes:**
```python
class Pipeline(Protocol[T]):
    """Protocol for data import pipelines."""
```
*Methods:*
```python
    async def run(self, query, **params) -> Dict[(str, Any)]:
        """Run the complete ETL pipeline.

Args: query: Query string or identifier for the data to extract params: Additional parameters for the query

Returns: Dictionary with pipeline execution statistics

Raises: Exception: If any stage of the pipeline fails"""
```

###### Module: product_pipeline
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/pipeline/product_pipeline.py`

**Imports:**
```python
from __future__ import annotations
import time
from typing import Any, Dict, Optional, Union
from app.core.exceptions import AppException
from app.logging import get_logger
from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector
from app.data_import.connectors.filemaker_connector import FileMakerConnector
from app.data_import.importers.product_importer import ProductImporter
from app.data_import.processors.product_processor import ProductProcessor
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.pipeline.product_pipeline")
```

**Classes:**
```python
class ProductPipeline(object):
    """Pipeline for product data import."""
```
*Methods:*
```python
    def __init__(self, connector, processor, importer, dry_run) -> None:
        """Initialize the product import pipeline.

Args: connector: Data source connector processor: Product data processor importer: Product data importer dry_run: If True, do not import data"""
```
```python
    async def run(self, query, limit, **params) -> Dict[(str, Any)]:
        """Run the complete product import pipeline.

Args: query: Query string or identifier for the data to extract limit: Maximum number of records to retrieve params: Additional parameters for the query

Returns: Dictionary with pipeline execution statistics

Raises: AppException: If any stage of the pipeline fails"""
```

##### Package: processors
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/processors`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/processors/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.data_import.processors.base import Processor
from app.data_import.processors.product_processor import ProductProcessor, ProductMappingConfig
from app.data_import.processors.as400_processor import AS400BaseProcessor, AS400ProcessorConfig, ProductAS400Processor, PricingAS400Processor, InventoryAS400Processor
```

**Global Variables:**
```python
__all__ = __all__ = [
    "Processor",
    "ProductProcessor",
    "ProductMappingConfig",
    "AS400BaseProcessor",
    "AS400ProcessorConfig",
    "ProductAS400Processor",
    "PricingAS400Processor",
    "InventoryAS400Processor",
]
```

###### Module: as400_processor
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/processors/as400_processor.py`

**Imports:**
```python
from __future__ import annotations
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Set, Type, TypeVar, Union
from pydantic import BaseModel
from app.core.exceptions import ValidationException
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.processors.as400_processor")
T = T = TypeVar("T", bound=BaseModel)
```

**Classes:**
```python
class AS400BaseProcessor(Generic[T], ABC):
    """Base class for AS400 data processors.

Generic base processor that transforms data from AS400 format to the application's data model format."""
```
*Methods:*
```python
    def __init__(self, config, destination_model) -> None:
        """Initialize the processor with configuration and model.

Args: config: Processing configuration destination_model: The Pydantic model to convert data to"""
```
```python
    async def process(self, data) -> List[Dict[(str, Any)]]:
        """Process raw AS400 data into application format.

Args: data: List of dictionary records from AS400

Returns: List of processed dictionaries ready for validation"""
```
```python
    async def validate(self, data) -> List[T]:
        """Validate processed data against destination model.

Args: data: List of processed dictionaries

Returns: List of validated model instances

Raises: ValidationException: If validation fails"""
```

```python
class AS400ProcessorConfig(BaseModel):
    """Configuration for AS400 data processors."""
```

```python
class InventoryAS400Processor(AS400BaseProcessor[T]):
    """Processor for inventory/stock data from AS400."""
```

```python
class PricingAS400Processor(AS400BaseProcessor[T]):
    """Processor for pricing data from AS400."""
```

```python
class ProductAS400Processor(AS400BaseProcessor[T]):
    """Processor for product data from AS400."""
```

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/processors/base.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Protocol, TypeVar
```

**Global Variables:**
```python
T = T = TypeVar("T")
```

**Classes:**
```python
class Processor(Protocol[T]):
    """Protocol for data processors."""
```
*Methods:*
```python
    async def process(self, data) -> List[Dict[(str, Any)]]:
        """Process raw data into structured data.

Args: data: List of raw data records

Returns: List of processed records

Raises: ValueError: If data cannot be processed"""
```
```python
    async def validate(self, data) -> List[T]:
        """Validate processed data.

Args: data: List of processed records

Returns: List of validated records

Raises: ValidationError: If data fails validation"""
```

###### Module: product_processor
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/data_import/processors/product_processor.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field, validator
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.domains.products.schemas import ProductCreate
```

**Global Variables:**
```python
logger = logger = get_logger("app.data_import.processors.product_processor")
```

**Classes:**
```python
class ProductMappingConfig(BaseModel):
    """Configuration for mapping source data to product schema."""
```
*Methods:*
```python
@validator('boolean_true_values', 'boolean_false_values')
    def validate_boolean_values(cls, v) -> List[str]:
```

```python
class ProductProcessor(object):
    """Processor for transforming raw product data into product schema."""
```
*Methods:*
```python
    def __init__(self, config) -> None:
        """Initialize the product processor.  Args: config: Product mapping configuration"""
```
```python
    async def process(self, data) -> List[Dict[(str, Any)]]:
        """Process raw data into product schema.

Args: data: List of raw data records

Returns: List of processed product records

Raises: ValueError: If data cannot be processed"""
```
```python
    async def validate(self, data) -> List[ProductCreate]:
        """Validate processed data against the product schema.

Args: data: List of processed product records

Returns: List of validated product create models

Raises: ValidationException: If validation fails"""
```

#### Package: db
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/db`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/db/__init__.py`

##### Module: base
*SQLAlchemy models import module.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/db/base.py`

**Imports:**
```python
from __future__ import annotations
from app.db.base_class import Base
from app.domains.location.models import Country, Address
from app.domains.api_key.models import ApiKey
from app.domains.users.models import User, UserRole
from app.domains.company.models import Company
from app.domains.reference.models import Color, ConstructionType, Hardware, PackagingType, Texture, TariffCode, UnspscCode, Warehouse
from app.domains.currency.models import Currency, ExchangeRate
from app.domains.media.models import Media, MediaType, MediaVisibility
from app.domains.products.models import Product, Brand, Fitment, Manufacturer, PriceType, AttributeDefinition, ProductActivity, ProductAttribute, ProductBrandHistory, ProductDescription, ProductMarketing, ProductMeasurement, ProductPricing, ProductStock, ProductSupersession
from app.domains.audit.models import AuditLog
from app.domains.compliance.models import Prop65Chemical, ProductChemical, ChemicalType, ProductDOTApproval, ApprovalStatus, ExposureScenario, HazardousMaterial, TransportRestriction, Warning
from app.domains.model_mapping.models import ModelMapping
from app.domains.chat.models import ChatRoom, ChatMember, ChatRoomType, ChatMemberRole, ChatMessage, MessageReaction, MessageType, RateLimitLog
from app.models.associations import product_color_association, product_construction_type_association, product_country_origin_association, product_fitment_association, product_hardware_association, product_interchange_association, product_media_association, product_packaging_association, product_tariff_code_association, product_texture_association, product_unspsc_association
```

##### Module: base_class
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/db/base_class.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, ClassVar
from sqlalchemy import DateTime, Boolean, inspect, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.expression import Select
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.db.base_class")
T = T = TypeVar("T", bound="Base")
```

**Classes:**
```python
class Base(DeclarativeBase):
    """Enhanced base class for all database models.

This class provides common functionality for all models, including: - Automatic table name generation - Audit fields (created_at, updated_at, created_by_id, updated_by_id) - Soft deletion support - JSON serialization via the to_dict() method - Helper methods for common query operations"""
```
*Methods:*
```python
@declared_attr
    def __tablename__(self) -> str:
        """Generate table name automatically from class name.

Returns: str: Table name as lowercase class name"""
```
```python
@classmethod
    def active_only(cls) -> Select:
        """Create a query for non-deleted records only.

Returns: Select: SQLAlchemy select statement filtered to non-deleted records"""
```
```python
@classmethod
    def filter_by_id(cls, id_value) -> Select:
        """Create a query to filter by id.

Args: id_value: UUID primary key to filter by

Returns: Select: SQLAlchemy select statement filtered by id"""
```
```python
@classmethod
    def from_dict(cls, data) -> T:
        """Create a new instance from a dictionary.

Args: data: Dictionary containing model data

Returns: T: New model instance"""
```
```python
@classmethod
    def get_columns(cls) -> List[str]:
        """Get a list of column names for this model.  Returns: List[str]: Column names"""
```
```python
@classmethod
    def get_relationships(cls) -> Dict[(str, Any)]:
        """Get relationships defined on this model.

Returns: Dict[str, Any]: Dictionary of relationship names and their properties"""
```
```python
    def restore(self, user_id) -> None:
        """Restore a soft-deleted record.  Args: user_id: ID of the user restoring the record"""
```
```python
    def soft_delete(self, user_id) -> None:
        """Mark the record as deleted without removing from database.

Args: user_id: ID of the user performing the deletion"""
```
```python
    def to_dict(self, exclude, include_relationships) -> Dict[(str, Any)]:
        """Convert model instance to dictionary.

This method provides a consistent way to serialize models for API responses. It respects the exclude_from_dict and include_relationships configurations.

Args: exclude: Additional fields to exclude from the result include_relationships: Override __include_relationships__ setting

Returns: Dict[str, Any]: Dictionary representation of model"""
```
```python
    def update_from_dict(self, data, user_id, exclude) -> None:
        """Update model attributes from dictionary.

Args: data: Dictionary containing values to update user_id: ID of the user performing the update exclude: Fields to exclude from update"""
```

##### Module: session
*Database session management module.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/db/session.py`

**Imports:**
```python
from __future__ import annotations
import contextlib
from typing import AsyncGenerator, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
```

**Global Variables:**
```python
engine = engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,
    future=True,
    pool_pre_ping=True,  # Check connection validity before using from pool
)
async_session_maker = async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)
```

**Functions:**
```python
async def get_db() -> AsyncGenerator[(AsyncSession, None)]:
    """Get a database session.

This dependency provides an async database session that automatically rolls back any failed transactions and closes the session when done.

Yields: AsyncSession: Database session"""
```

```python
@contextlib.asynccontextmanager
async def get_db_context() -> AsyncGenerator[(AsyncSession, None)]:
    """Context manager for database sessions.

This is useful for scripts that need to handle their own transactions and session lifecycle outside of FastAPI's dependency injection.

Yields: AsyncSession: Database session"""
```

##### Module: utils
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/db/utils.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import contextlib
import functools
import time
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Type, TypeVar, Union, cast
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import Delete, Insert, Update
from app.core.dependency_manager import get_dependency
from app.core.exceptions import DataIntegrityException, DatabaseException, ErrorCode, TransactionException
from app.logging import get_logger
from app.db.base_class import Base
```

**Global Variables:**
```python
logger = logger = get_logger("app.db.utils")
T = T = TypeVar("T", bound=Base)
F = F = TypeVar("F", bound=Callable[..., Any])
```

**Functions:**
```python
async def bulk_create(db, model, objects) -> List[T]:
    """Create multiple database objects in a single operation.

Args: db: The database session model: The model class objects: List of object data dictionaries

Returns: List of created database objects

Raises: DatabaseException: If the bulk create operation fails DataIntegrityException: If a unique constraint is violated"""
```

```python
async def bulk_update(db, model, id_field, objects) -> int:
    """Update multiple database objects in a single operation.

Args: db: The database session model: The model class id_field: The field used to identify objects objects: List of object data dictionaries

Returns: Number of updated objects

Raises: DatabaseException: If the bulk update operation fails DataIntegrityException: If a unique constraint is violated"""
```

```python
async def count_query(db, query) -> int:
    """Count the results of a query.

Args: db: The database session query: The query to count

Returns: The number of results

Raises: DatabaseException: If the count operation fails"""
```

```python
async def create_object(db, model, obj_in) -> T:
    """Create a new database object.

Args: db: The database session model: The model class obj_in: The object data

Returns: The created database object

Raises: DatabaseException: If the object creation fails DataIntegrityException: If a unique constraint is violated"""
```

```python
async def delete_object(db, model, id_value, user_id, hard_delete) -> bool:
    """Delete a database object.

Args: db: The database session model: The model class id_value: The ID of the object to delete user_id: Optional user ID for tracking who performed the deletion hard_delete: Whether to permanently delete the object

Returns: True if the object was deleted, False if not found

Raises: DatabaseException: If the deletion fails DataIntegrityException: If the object is referenced by other objects"""
```

```python
async def execute_query(db, query) -> Any:
    """Execute a query with error handling.

Args: db: The database session query: The query to execute

Returns: The query result

Raises: DatabaseException: If the query execution fails"""
```

```python
async def get_by_id(db, model, id_value) -> Optional[T]:
    """Get a database object by ID.

Args: db: The database session model: The model class id_value: The ID value to look up

Returns: The database object, or None if not found

Raises: DatabaseException: If a database error occurs"""
```

```python
async def get_by_ids(db, model, ids) -> List[T]:
    """Get multiple database objects by their IDs.

Args: db: The database session model: The model class ids: The list of IDs to look up

Returns: A list of database objects

Raises: DatabaseException: If a database error occurs"""
```

```python
async def paginate(db, query, page, page_size, load_items) -> Dict[(str, Any)]:
    """Paginate query results.

Args: db: The database session query: The query to paginate page: The page number (1-based) page_size: The number of items per page load_items: Whether to load the items or just return metadata

Returns: Dictionary with items, total, page, page_size, and pages information

Raises: DatabaseException: If the pagination operation fails"""
```

```python
def track_db_delete(entity) -> Callable[([F], F)]:
    """Decorator to track database delete query performance.

Args: entity: The entity being deleted

Returns: Decorator function"""
```

```python
def track_db_insert(entity) -> Callable[([F], F)]:
    """Decorator to track database insert query performance.

Args: entity: The entity being inserted

Returns: Decorator function"""
```

```python
def track_db_query(operation, entity) -> Callable[([F], F)]:
    """Decorator to track database query performance.

Args: operation: The type of operation being performed entity: The entity being operated on

Returns: Decorator function"""
```

```python
def track_db_select(entity) -> Callable[([F], F)]:
    """Decorator to track database select query performance.

Args: entity: The entity being selected

Returns: Decorator function"""
```

```python
def track_db_transaction() -> Callable[([F], F)]:
    """Decorator to track database transaction performance.  Returns: Decorator function"""
```

```python
def track_db_update(entity) -> Callable[([F], F)]:
    """Decorator to track database update query performance.

Args: entity: The entity being updated

Returns: Decorator function"""
```

```python
@contextlib.asynccontextmanager
async def transaction(db) -> AsyncGenerator[(AsyncSession, None)]:
    """Context manager for database transactions.

This creates a transaction context that automatically handles commits and rollbacks. If the session is already in a transaction, it will use the existing transaction.

Args: db: The database session

Yields: The database session

Raises: TransactionException: If a database error occurs during the transaction"""
```

```python
def transactional(func) -> F:
    """Decorator for functions that should execute within a transaction.

Args: func: The function to wrap

Returns: The wrapped function

Raises: ValueError: If no database session is provided TransactionException: If a database error occurs during the transaction"""
```

```python
async def update_object(db, model, id_value, obj_in, user_id) -> Optional[T]:
    """Update a database object.

Args: db: The database session model: The model class id_value: The ID of the object to update obj_in: The update data user_id: Optional user ID for tracking who made the update

Returns: The updated database object, or None if not found

Raises: DatabaseException: If the update fails DataIntegrityException: If a unique constraint is violated"""
```

```python
async def upsert(db, model, data, unique_fields) -> T:
    """Update an existing object or create a new one if it doesn't exist.

Args: db: The database session model: The model class data: The object data unique_fields: Fields used to identify an existing object

Returns: The created or updated database object

Raises: DatabaseException: If the upsert operation fails"""
```

#### Package: domains
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/__init__.py`

##### Package: api_key
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/api_key`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/api_key/__init__.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/api_key/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, String, JSON, ForeignKey, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.domains.users.models import User
```

**Classes:**
```python
class ApiKey(Base):
    """API Key entity for API authentication.

Attributes: id: Unique identifier. user_id: ID of the user who owns the key. key_id: Public identifier for the API key. hashed_secret: Hashed secret part of the API key. name: Human-readable name for the key. is_active: Whether the key is active. last_used_at: When the key was last used. expires_at: When the key expires. permissions: Specific permissions granted to the key. extra_metadata: Additional metadata about the key. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'api_key'
__table_args__ =     __table_args__ = (Index("ix_api_keys_user_id_name", user_id, name, unique=True),)
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ApiKey instance.

Returns: String representation including id, user_id, and name."""
```
```python
    def to_dict(self, include_secret) -> Dict[(str, Any)]:
        """Convert the API key to a dictionary.

Args: include_secret: Whether to include the hashed secret.

Returns: Dictionary representation of the API key."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/api_key/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.api_key.models import ApiKey
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

**Classes:**
```python
class ApiKeyRepository(BaseRepository[(ApiKey, uuid.UUID)]):
    """Repository for API Key entity operations.

Provides methods for querying, creating, updating, and deleting API Key entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the API key repository.  Args: db: The database session."""
```
```python
    async def clean_expired_keys(self) -> int:
        """Clean up expired API keys.  Returns: Number of keys deactivated."""
```
```python
    async def create_api_key(self, user_id, name, permissions, extra_metadata, expires_in_days) -> Tuple[(ApiKey, str)]:
        """Create a new API key.

Args: user_id: ID of the user who will own the key. name: Human-readable name for the key. permissions: Optional list of permissions to grant. extra_metadata: Optional additional metadata. expires_in_days: Optional number of days until expiration.

Returns: Tuple containing (API key entity, secret).

Raises: ResourceNotFoundException: If the user doesn't exist."""
```
```python
    async def ensure_exists(self, api_key_id) -> ApiKey:
        """Ensure an API key exists by ID, raising an exception if not found.

Args: api_key_id: The API key ID to check.

Returns: The API key if found.

Raises: ResourceNotFoundException: If the API key is not found."""
```
```python
    async def find_by_key_id(self, key_id) -> Optional[ApiKey]:
        """Find an API key by its key ID.

Args: key_id: The key ID to search for.

Returns: The API key if found, None otherwise."""
```
```python
    async def get_by_user(self, user_id, active_only) -> List[ApiKey]:
        """Get API keys for a specific user.

Args: user_id: The user ID to filter by. active_only: Whether to include only active keys.

Returns: List of API keys for the user."""
```
```python
    async def revoke_all_user_keys(self, user_id) -> int:
        """Revoke all API keys for a user.

Args: user_id: The user ID whose keys to revoke.

Returns: Number of keys revoked."""
```
```python
    async def revoke_api_key(self, api_key_id) -> bool:
        """Revoke an API key.

Args: api_key_id: The API key ID to revoke.

Returns: True if the key was revoked, False otherwise."""
```
```python
    async def verify_api_key(self, key_id, secret) -> Optional[ApiKey]:
        """Verify an API key by checking the key ID and secret.

Args: key_id: The key ID to verify. secret: The secret to verify.

Returns: The API key if valid, None otherwise."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/api_key/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

**Classes:**
```python
class ApiKey(ApiKeyInDB):
    """Schema for API key data in API responses."""
```

```python
class ApiKeyBase(BaseModel):
    """Base schema for API key data.

Attributes: name: Human-readable name for the key. permissions: List of permissions granted to the key. extra_metadata: Additional metadata about the key. expires_at: When the key expires."""
```
*Methods:*
```python
@field_validator('name')
@classmethod
    def normalize_name(cls, v) -> str:
        """Normalize the API key name.  Args: v: The name to normalize.  Returns: Normalized name."""
```

```python
class ApiKeyCreate(ApiKeyBase):
    """Schema for creating a new API key.  Attributes: user_id: ID of the user who will own the key."""
```

```python
class ApiKeyInDB(ApiKeyBase):
    """Schema for API key data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ApiKeyRevokeResponse(BaseModel):
    """Schema for API key revocation response.

Attributes: id: ID of the revoked key. revoked: Whether the key was successfully revoked. message: Response message."""
```

```python
class ApiKeyUpdate(BaseModel):
    """Schema for updating an existing API key.  All fields are optional to allow partial updates."""
```
*Methods:*
```python
@field_validator('name')
@classmethod
    def normalize_name(cls, v) -> Optional[str]:
        """Normalize the API key name if provided.

Args: v: The name to normalize or None.

Returns: Normalized name or None."""
```

```python
class ApiKeyWithSecret(ApiKey):
    """Schema for API key including the secret.

This schema is only used when initially creating an API key."""
```

##### Package: audit
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/__init__.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, String, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.domains.users.models import User
from app.domains.company.schemas import Company
```

**Classes:**
```python
class AuditLog(Base):
    """Audit log entity for tracking system activity.

Attributes: id: Unique identifier. timestamp: When the audited event occurred. event_type: Type of event being audited. level: Log level (info, warning, error). user_id: ID of the user who performed the action. ip_address: IP address of the user. resource_id: ID of the affected resource. resource_type: Type of the affected resource. details: Additional details about the event. request_id: ID of the request that triggered the event. user_agent: User agent of the client. session_id: ID of the user's session. company_id: ID of the company context. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'audit_log'
__table_args__ =     __table_args__ = (
        Index("ix_audit_log_timestamp_desc", timestamp.desc()),
        Index("ix_audit_log_user_id_timestamp", user_id, timestamp.desc()),
        Index(
            "ix_audit_log_resource_timestamp",
            resource_type,
            resource_id,
            timestamp.desc(),
        ),
        Index("ix_audit_log_event_type_timestamp", event_type, timestamp.desc()),
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of AuditLog instance.

Returns: String representation including id, event_type, and timestamp."""
```
```python
    def to_dict(self) -> Dict[(str, Any)]:
        """Convert the audit log to a dictionary.  Returns: Dictionary representation of the audit log."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy import select, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.audit.models import AuditLog
from app.repositories.base import BaseRepository
```

**Classes:**
```python
class AuditLogRepository(BaseRepository[(AuditLog, uuid.UUID)]):
    """Repository for AuditLog entity operations.

Provides methods for querying, creating, and retrieving AuditLog entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the audit log repository.  Args: db: The database session."""
```
```python
    async def create_log(self, event_type, level, details, user_id, ip_address, resource_id, resource_type, request_id, user_agent, session_id, company_id, timestamp) -> AuditLog:
        """Create a new audit log entry.

Args: event_type: Type of event being audited. level: Log level (info, warning, error). details: Additional details about the event. user_id: ID of the user who performed the action. ip_address: IP address of the user. resource_id: ID of the affected resource. resource_type: Type of the affected resource. request_id: ID of the request that triggered the event. user_agent: User agent of the client. session_id: ID of the user's session. company_id: ID of the company context. timestamp: When the audited event occurred (defaults to now).

Returns: The created audit log entry."""
```
```python
    async def get_by_company(self, company_id, page, page_size) -> Dict[(str, Any)]:
        """Get paginated audit logs for a specific company.

Args: company_id: The company ID to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_event_type(self, event_type, page, page_size) -> Dict[(str, Any)]:
        """Get paginated audit logs for a specific event type.

Args: event_type: The event type to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_level(self, level, page, page_size) -> Dict[(str, Any)]:
        """Get paginated audit logs for a specific log level.

Args: level: The log level to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_resource(self, resource_type, resource_id, page, page_size) -> Dict[(str, Any)]:
        """Get paginated audit logs for a specific resource.

Args: resource_type: The resource type to filter by. resource_id: The resource ID to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_time_range(self, start_time, end_time, page, page_size) -> Dict[(str, Any)]:
        """Get paginated audit logs within a time range.

Args: start_time: The start time of the range. end_time: The end time of the range (defaults to now). page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_user(self, user_id, page, page_size) -> Dict[(str, Any)]:
        """Get paginated audit logs for a specific user.

Args: user_id: The user ID to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_recent_logs(self, hours, page, page_size) -> Dict[(str, Any)]:
        """Get paginated recent audit logs.

Args: hours: Number of hours to look back. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def search(self, search_term, page, page_size) -> Dict[(str, Any)]:
        """Search audit logs by various fields.

Args: search_term: The term to search for. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
```

**Classes:**
```python
class AuditEventType(str, Enum):
    """Types of auditable events.

This is a subset of common event types. The system can handle any string value for event_type, not just these enumerated ones."""
```
*Class attributes:*
```python
LOGIN = 'login'
LOGOUT = 'logout'
CREATE = 'create'
UPDATE = 'update'
DELETE = 'delete'
VIEW = 'view'
EXPORT = 'export'
IMPORT = 'import'
APPROVE = 'approve'
REJECT = 'reject'
PASSWORD_CHANGE = 'password_change'
ROLE_CHANGE = 'role_change'
API_ACCESS = 'api_access'
```

```python
class AuditLog(AuditLogInDB):
    """Schema for complete audit log data in API responses.

Includes related entities like user and company details."""
```

```python
class AuditLogBase(BaseModel):
    """Base schema for audit log data.

Attributes: timestamp: When the audited event occurred. event_type: Type of event being audited. level: Log level (info, warning, error). user_id: ID of the user who performed the action. ip_address: IP address of the user. resource_id: ID of the affected resource. resource_type: Type of the affected resource. details: Additional details about the event. request_id: ID of the request that triggered the event. user_agent: User agent of the client. session_id: ID of the user's session. company_id: ID of the company context."""
```

```python
class AuditLogCreate(AuditLogBase):
    """Schema for creating a new audit log entry."""
```

```python
class AuditLogExportFormat(str, Enum):
    """Export formats for audit logs.

Attributes: CSV: Comma-separated values format. JSON: JSON format. XML: XML format."""
```
*Class attributes:*
```python
CSV = 'csv'
JSON = 'json'
XML = 'xml'
```

```python
class AuditLogExportRequest(BaseModel):
    """Schema for requesting an audit log export.

Attributes: filter: Filter criteria for logs to export. format: Export format. include_details: Whether to include detailed information."""
```

```python
class AuditLogFilter(BaseModel):
    """Schema for filtering audit logs.

Attributes: start_date: Filter logs after this date. end_date: Filter logs before this date. event_type: Filter by event type. level: Filter by log level. user_id: Filter by user ID. resource_type: Filter by resource type. resource_id: Filter by resource ID. company_id: Filter by company ID."""
```

```python
class AuditLogInDB(AuditLogBase):
    """Schema for audit log data as stored in the database.  Includes database-specific fields like ID."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class AuditLogLevel(str, Enum):
    """Severity levels for audit logs.

Attributes: INFO: Informational events. WARNING: Warning events that might require attention. ERROR: Error events that indicate problems. CRITICAL: Critical events that require immediate attention."""
```
*Class attributes:*
```python
INFO = 'info'
WARNING = 'warning'
ERROR = 'error'
CRITICAL = 'critical'
```

```python
class AuditLogStatistics(BaseModel):
    """Schema for audit log statistics.

Attributes: total_count: Total number of log entries. by_level: Count of logs grouped by level. by_event_type: Count of logs grouped by event type. by_user: Count of logs grouped by user. by_resource_type: Count of logs grouped by resource type."""
```

###### Package: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/service`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/service/__init__.py`

**Imports:**
```python
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.audit.service.service import AuditService
```

**Functions:**
```python
def get_audit_service(db) -> AuditService:
    """Get or create an AuditService instance.

Args: db: Optional database session

Returns: An AuditService instance"""
```

####### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/service/base.py`

**Imports:**
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, TypeVar
from pydantic import BaseModel
```

**Global Variables:**
```python
T = T = TypeVar("T")  # Audit log entry type
```

**Classes:**
```python
class AuditContext(BaseModel):
    """Context information for an audit event."""
```

```python
class AuditEventType(str, Enum):
    """Enum for different types of audit events."""
```
*Class attributes:*
```python
USER_LOGIN = 'user_login'
USER_LOGOUT = 'user_logout'
LOGIN_FAILED = 'login_failed'
PASSWORD_RESET_REQUESTED = 'password_reset_requested'
PASSWORD_RESET_COMPLETED = 'password_reset_completed'
MFA_ENABLED = 'mfa_enabled'
MFA_DISABLED = 'mfa_disabled'
SESSION_EXPIRED = 'session_expired'
API_KEY_CREATED = 'api_key_created'
API_KEY_REVOKED = 'api_key_revoked'
USER_CREATED = 'user_created'
USER_UPDATED = 'user_updated'
USER_DELETED = 'user_deleted'
USER_ACTIVATED = 'user_activated'
USER_DEACTIVATED = 'user_deactivated'
PASSWORD_CHANGED = 'password_changed'
EMAIL_CHANGED = 'email_changed'
USER_PROFILE_UPDATED = 'user_profile_updated'
PERMISSION_CHANGED = 'permission_changed'
ROLE_ASSIGNED = 'role_assigned'
ROLE_REVOKED = 'role_revoked'
ACCESS_DENIED = 'access_denied'
PRODUCT_CREATED = 'product_created'
PRODUCT_UPDATED = 'product_updated'
PRODUCT_DELETED = 'product_deleted'
PRODUCT_ACTIVATED = 'product_activated'
PRODUCT_DEACTIVATED = 'product_deactivated'
PRICE_CHANGED = 'price_changed'
INVENTORY_UPDATED = 'inventory_updated'
ORDER_CREATED = 'order_created'
ORDER_UPDATED = 'order_updated'
ORDER_CANCELED = 'order_canceled'
ORDER_SHIPPED = 'order_shipped'
PAYMENT_RECEIVED = 'payment_received'
PAYMENT_REFUNDED = 'payment_refunded'
DATA_EXPORTED = 'data_exported'
DATA_IMPORTED = 'data_imported'
DATA_DELETED = 'data_deleted'
REPORT_GENERATED = 'report_generated'
SETTINGS_CHANGED = 'settings_changed'
CONFIGURATION_CHANGED = 'configuration_changed'
FEATURE_ENABLED = 'feature_enabled'
FEATURE_DISABLED = 'feature_disabled'
FILE_UPLOADED = 'file_uploaded'
FILE_DOWNLOADED = 'file_downloaded'
FILE_DELETED = 'file_deleted'
EMAIL_SENT = 'email_sent'
SMS_SENT = 'sms_sent'
NOTIFICATION_SENT = 'notification_sent'
CHAT_ROOM_CREATED = 'chat_room_created'
CHAT_MESSAGE_SENT = 'chat_message_sent'
CHAT_MESSAGE_EDITED = 'chat_message_edited'
CHAT_MESSAGE_DELETED = 'chat_message_deleted'
CHAT_MEMBER_ADDED = 'chat_member_added'
CHAT_MEMBER_REMOVED = 'chat_member_removed'
EXTERNAL_API_CALLED = 'external_api_called'
WEBHOOK_RECEIVED = 'webhook_received'
WEBHOOK_PROCESSED = 'webhook_processed'
SYSTEM_STARTED = 'system_started'
SYSTEM_STOPPED = 'system_stopped'
BACKUP_CREATED = 'backup_created'
BACKUP_RESTORED = 'backup_restored'
MAINTENANCE_MODE_ENABLED = 'maintenance_mode_enabled'
MAINTENANCE_MODE_DISABLED = 'maintenance_mode_disabled'
GDPR_DATA_EXPORT = 'gdpr_data_export'
GDPR_DATA_DELETED = 'gdpr_data_deleted'
TERMS_ACCEPTED = 'terms_accepted'
PRIVACY_POLICY_ACCEPTED = 'privacy_policy_accepted'
```

```python
class AuditLogLevel(str, Enum):
    """Enum for audit log severity levels."""
```
*Class attributes:*
```python
INFO = 'info'
WARNING = 'warning'
ERROR = 'error'
CRITICAL = 'critical'
```

```python
class AuditLogger(Protocol):
    """Protocol for audit loggers."""
```
*Methods:*
```python
    async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, context, level, options) -> str:
        """Log an audit event.

Args: event_type: Type of the audit event user_id: ID of the user who performed the action ip_address: IP address of the user resource_id: ID of the resource affected resource_type: Type of the resource affected details: Additional details about the event context: Additional context information level: Severity level of the event options: Audit logging options

Returns: str: The ID of the created audit event"""
```

```python
class AuditOptions(BaseModel):
    """Options for audit logging."""
```

####### Module: factory
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/service/factory.py`

**Imports:**
```python
from __future__ import annotations
from typing import Dict, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.logging import get_logger
from app.domains.audit.service.base import AuditLogger
from app.domains.audit.service.loggers import DatabaseAuditLogger, FileAuditLogger, LoggingAuditLogger
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.audit.service.factory")
```

**Classes:**
```python
class AuditLoggerFactory(object):
    """Factory for creating audit logger instances."""
```
*Methods:*
```python
@classmethod
    def create_default_loggers(cls, db) -> List[AuditLogger]:
        """Create the default set of audit loggers based on application settings.

Args: db: Optional database session for database loggers

Returns: List of default audit loggers"""
```
```python
@classmethod
    def create_logger(cls, logger_type, db, **kwargs) -> AuditLogger:
        """Create an audit logger of the specified type.

Args: logger_type: The type of logger to create db: Optional database session for database loggers **kwargs: Additional logger configuration

Returns: AuditLogger: The created logger

Raises: ValueError: If the logger type is not supported"""
```
```python
@classmethod
    def register_logger(cls, name, logger_class) -> None:
        """Register a new audit logger type.

Args: name: Logger type name logger_class: Logger class

Raises: ValueError: If a logger with the same name is already registered"""
```

####### Module: loggers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/service/loggers.py`

**Imports:**
```python
from __future__ import annotations
import json
import uuid
import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
from app.domains.audit.service.base import AuditContext, AuditEventType, AuditLogLevel, AuditLogger, AuditOptions
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.audit.service.loggers")
```

**Classes:**
```python
class BaseAuditLogger(object):
    """Base class for audit loggers with common functionality."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the base audit logger."""
```

```python
class DatabaseAuditLogger(BaseAuditLogger, AuditLogger):
    """Audit logger that logs events to the database."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the database audit logger.  Args: db: Database session for database operations"""
```
```python
    async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, context, level, options) -> str:
        """Log an audit event to the database.

Args: event_type: Type of the audit event user_id: ID of the user who performed the action ip_address: IP address of the user resource_id: ID of the resource affected resource_type: Type of the resource affected details: Additional details about the event context: Additional context information level: Severity level of the event options: Audit logging options

Returns: str: The ID of the created audit event"""
```

```python
class FileAuditLogger(BaseAuditLogger, AuditLogger):
    """Audit logger that logs events to a file."""
```
*Methods:*
```python
    def __init__(self, file_path) -> None:
        """Initialize the file audit logger.  Args: file_path: Path to the audit log file"""
```
```python
    async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, context, level, options) -> str:
        """Log an audit event to a file.

Args: event_type: Type of the audit event user_id: ID of the user who performed the action ip_address: IP address of the user resource_id: ID of the resource affected resource_type: Type of the resource affected details: Additional details about the event context: Additional context information level: Severity level of the event options: Audit logging options

Returns: str: The ID of the created audit event"""
```

```python
class LoggingAuditLogger(BaseAuditLogger, AuditLogger):
    """Audit logger that logs events to the application logging system."""
```
*Methods:*
```python
    async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, context, level, options) -> str:
        """Log an audit event to the application logging system.

Args: event_type: Type of the audit event user_id: ID of the user who performed the action ip_address: IP address of the user resource_id: ID of the resource affected resource_type: Type of the resource affected details: Additional details about the event context: Additional context information level: Severity level of the event options: Audit logging options

Returns: str: The ID of the created audit event"""
```

####### Module: query
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/service/query.py`

**Imports:**
```python
from __future__ import annotations
import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
from app.domains.audit.service.base import AuditEventType, AuditLogLevel
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.audit.service.query")
```

**Classes:**
```python
class AuditQuery(object):
    """Query functionality for audit logs."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the audit query.  Args: db: Database session for database operations"""
```
```python
    async def get_event_by_id(self, event_id) -> Optional[Dict[(str, Any)]]:
        """Retrieve a specific audit event by ID.

Args: event_id: The ID of the audit event to retrieve

Returns: The audit event or None if not found"""
```
```python
    async def get_events(self, user_id, event_type, resource_id, resource_type, start_time, end_time, level, limit, offset, sort_field, sort_order) -> Dict[(str, Any)]:
        """Retrieve audit events with filtering.

Args: user_id: Filter by user ID event_type: Filter by event type resource_id: Filter by resource ID resource_type: Filter by resource type start_time: Filter by start time end_time: Filter by end time level: Filter by log level limit: Maximum number of results to return offset: Result offset for pagination sort_field: Field to sort by sort_order: Sort order ("asc" or "desc")

Returns: Dictionary with audit log events and total count"""
```
```python
    async def get_resource_history(self, resource_type, resource_id, limit) -> List[Dict[(str, Any)]]:
        """Get history of actions performed on a specific resource.

Args: resource_type: The type of resource resource_id: The ID of the resource limit: Maximum number of results to return

Returns: List of audit events for the resource"""
```
```python
    async def get_user_activity(self, user_id, start_time, end_time, limit) -> List[Dict[(str, Any)]]:
        """Get recent activity for a specific user.

Args: user_id: The ID of the user start_time: Optional start time filter end_time: Optional end time filter limit: Maximum number of results to return

Returns: List of audit events for the user"""
```
```python
    async def purge_old_logs(self, days_to_keep) -> int:
        """Purge audit logs older than the specified number of days.

Args: days_to_keep: Number of days of logs to keep

Returns: Number of purged log entries"""
```

####### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/audit/service/service.py`

**Imports:**
```python
from __future__ import annotations
import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.logging import get_logger
from app.domains.audit.service.base import AuditContext, AuditEventType, AuditLogLevel, AuditLogger, AuditOptions
from app.domains.audit.service.factory import AuditLoggerFactory
from app.domains.audit.service.query import AuditQuery
from app.services.interfaces import ServiceInterface
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.audit.service.service")
```

**Classes:**
```python
class AuditService(ServiceInterface):
    """Service for recording and retrieving audit logs.

This service provides methods for logging user and system actions for security, compliance, and troubleshooting purposes."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the audit service.  Args: db: Optional database session"""
```
```python
    def add_logger(self, logger) -> None:
        """Add an audit logger to the service.  Args: logger: The audit logger to add"""
```
```python
    async def get_event_by_id(self, event_id) -> Optional[Dict[(str, Any)]]:
        """Retrieve a specific audit event by ID.

Args: event_id: The ID of the audit event to retrieve

Returns: The audit event or None if not found"""
```
```python
    async def get_events(self, user_id, event_type, resource_id, resource_type, start_time, end_time, level, limit, offset, sort_field, sort_order) -> Dict[(str, Any)]:
        """Retrieve audit events with filtering.

Args: user_id: Filter by user ID event_type: Filter by event type resource_id: Filter by resource ID resource_type: Filter by resource type start_time: Filter by start time end_time: Filter by end time level: Filter by log level limit: Maximum number of results to return offset: Result offset for pagination sort_field: Field to sort by sort_order: Sort order ("asc" or "desc")

Returns: Dictionary with audit log events and total count"""
```
```python
    async def get_resource_history(self, resource_type, resource_id, limit) -> List[Dict[(str, Any)]]:
        """Get history of actions performed on a specific resource.

Args: resource_type: The type of resource resource_id: The ID of the resource limit: Maximum number of results to return

Returns: List of audit events for the resource"""
```
```python
    async def get_user_activity(self, user_id, start_time, end_time, limit) -> List[Dict[(str, Any)]]:
        """Get recent activity for a specific user.

Args: user_id: The ID of the user start_time: Optional start time filter end_time: Optional end time filter limit: Maximum number of results to return

Returns: List of audit events for the user"""
```
```python
    async def initialize(self) -> None:
        """Initialize the audit service."""
```
```python
    async def log_event(self, event_type, user_id, ip_address, resource_id, resource_type, details, context, level, options) -> str:
        """Log an audit event.

Args: event_type: Type of the audit event user_id: ID of the user who performed the action ip_address: IP address of the user resource_id: ID of the resource affected resource_type: Type of the resource affected details: Additional details about the event context: Additional context information level: Severity level of the event options: Audit logging options

Returns: The ID of the created audit event"""
```
```python
    async def purge_old_logs(self, days_to_keep) -> int:
        """Purge audit logs older than the specified number of days.

Args: days_to_keep: Number of days of logs to keep

Returns: Number of purged log entries"""
```
```python
    async def shutdown(self) -> None:
        """Shutdown the audit service."""
```

##### Package: autocare
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.domains.autocare.vcdb.service import VCdbService
from app.domains.autocare.pcdb.service import PCdbService
from app.domains.autocare.padb.service import PAdbService
from app.domains.autocare.qdb.service import QdbService
from app.domains.autocare.fitment.service import FitmentMappingService
from app.domains.autocare.schemas import AutocareImportParams, AutocareExportParams, FitmentSearchParams
from app.domains.autocare.exceptions import AutocareException, InvalidVehicleDataException, InvalidPartDataException, MappingNotFoundException, ImportException, ExportException
from app.domains.autocare import handlers
```

**Global Variables:**
```python
__all__ = __all__ = [
    # Services
    "VCdbService",
    "PCdbService",
    "PAdbService",
    "QdbService",
    "FitmentMappingService",
    # Schemas
    "AutocareImportParams",
    "AutocareExportParams",
    "FitmentSearchParams",
    # Exceptions
    "AutocareException",
    "InvalidVehicleDataException",
    "InvalidPartDataException",
    "MappingNotFoundException",
    "ImportException",
    "ExportException",
]
```

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/exceptions.py`

**Imports:**
```python
from __future__ import annotations
from app.core.exceptions import BusinessException, ResourceNotFoundException
```

**Classes:**
```python
class AutocareException(BusinessException):
    """Base exception for all autocare domain exceptions."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize the exception.

Args: message: The error message details: Optional dictionary with additional error details"""
```

```python
class ExportException(AutocareException):
    """Raised when exporting data to ACES or PIES files fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize the exception.

Args: message: The error message details: Optional dictionary with additional error details"""
```

```python
class ImportException(AutocareException):
    """Raised when importing data from ACES or PIES files fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize the exception.

Args: message: The error message details: Optional dictionary with additional error details"""
```

```python
class InvalidPartDataException(AutocareException):
    """Raised when part data is invalid or incomplete."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize the exception.

Args: message: The error message details: Optional dictionary with additional error details"""
```

```python
class InvalidVehicleDataException(AutocareException):
    """Raised when vehicle data is invalid or incomplete."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize the exception.

Args: message: The error message details: Optional dictionary with additional error details"""
```

```python
class MappingNotFoundException(ResourceNotFoundException):
    """Raised when a requested fitment mapping cannot be found."""
```
*Methods:*
```python
    def __init__(self, resource_id, details) -> None:
        """Initialize the exception.

Args: resource_id: The ID of the mapping that wasn't found details: Optional dictionary with additional error details"""
```

```python
class PAdbException(AutocareException):
    """Raised when there's an issue with PAdb data."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize the exception.

Args: message: The error message details: Optional dictionary with additional error details"""
```

```python
class PCdbException(AutocareException):
    """Raised when there's an issue with PCdb data."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize the exception.

Args: message: The error message details: Optional dictionary with additional error details"""
```

```python
class QdbException(AutocareException):
    """Raised when there's an issue with Qdb data."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize the exception.

Args: message: The error message details: Optional dictionary with additional error details"""
```

```python
class VCdbException(AutocareException):
    """Raised when there's an issue with VCdb data."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize the exception.

Args: message: The error message details: Optional dictionary with additional error details"""
```

###### Module: handlers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/handlers.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
from typing import Any, Dict
from uuid import UUID
from app.core.events import subscribe_to_event
from app.db.session import get_db
from app.domains.autocare.fitment.repository import FitmentMappingRepository
from app.domains.products.repository import ProductRepository
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.autocare.handlers")
```

**Functions:**
```python
@subscribe_to_event('autocare.database_updated')
async def handle_autocare_database_updated(payload) -> None:
    """Handle updates to autocare databases.

This event handler is triggered when any of the autocare databases (VCdb, PCdb, PAdb, Qdb) are updated.

Args: payload: Event data containing information about the update"""
```

```python
@subscribe_to_event('products.product_created')
async def handle_product_created(payload) -> None:
    """Attempt to map a newly created product to autocare fitments.

Args: payload: Event data containing product information"""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/schemas.py`

**Imports:**
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator
```

**Classes:**
```python
class AutocareExportParams(BaseModel):
    """Parameters for exporting data.

Attributes: file_path: Path to the export file format: Format of the export file data_type: Type of data to export filters: Filters to apply to the data options: Additional export options"""
```

```python
class AutocareImportParams(BaseModel):
    """Parameters for importing data.

Attributes: file_path: Path to the import file format: Format of the import file mode: Import mode data_type: Type of data to import validate: Whether to validate data before import options: Additional import options"""
```

```python
class DataType(str, Enum):
    """Types of data to import or export.

Attributes: VEHICLES: Vehicle data PARTS: Part data FITMENTS: Fitment mapping data ALL: All data types"""
```
*Class attributes:*
```python
VEHICLES = 'vehicles'
PARTS = 'parts'
FITMENTS = 'fitments'
ALL = 'all'
```

```python
class FileFormat(str, Enum):
    """File formats for import and export operations.

Attributes: ACES_XML: ACES XML format PIES_XML: PIES XML format CSV: Comma-separated values EXCEL: Microsoft Excel format JSON: JSON format"""
```
*Class attributes:*
```python
ACES_XML = 'aces_xml'
PIES_XML = 'pies_xml'
CSV = 'csv'
EXCEL = 'excel'
JSON = 'json'
```

```python
class FitmentSearchParams(BaseModel):
    """Parameters for searching fitment data.

Attributes: year: Vehicle year make: Vehicle make model: Vehicle model submodel: Vehicle submodel part_number: Part number part_type: Part type brand: Brand page: Page number page_size: Page size"""
```
*Methods:*
```python
@model_validator(mode='after')
    def validate_search_criteria(self) -> 'FitmentSearchParams':
        """Validate that at least one search criterion is provided.

Returns: The validated model

Raises: ValueError: If no search criteria are provided"""
```

```python
class ImportMode(str, Enum):
    """Import modes for data ingestion.

Attributes: REPLACE: Replace existing data MERGE: Merge with existing data UPDATE: Update existing data only INSERT: Insert new data only"""
```
*Class attributes:*
```python
REPLACE = 'replace'
MERGE = 'merge'
UPDATE = 'update'
INSERT = 'insert'
```

```python
class PaginatedResponse(BaseModel):
    """Base schema for paginated responses.

Attributes: items: List of items total: Total number of items page: Current page number page_size: Number of items per page pages: Total number of pages"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/service.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
from pathlib import Path
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import publish_event
from app.domains.autocare.exceptions import AutocareException, ImportException, ExportException
from app.domains.autocare.schemas import AutocareImportParams, AutocareExportParams, DataType, FileFormat
from app.domains.autocare.vcdb.service import VCdbService
from app.domains.autocare.pcdb.service import PCdbService
from app.domains.autocare.padb.service import PAdbService
from app.domains.autocare.qdb.service import QdbService
from app.domains.autocare.fitment.service import FitmentMappingService
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.autocare.service")
```

**Classes:**
```python
class AutocareService(object):
    """Main service for autocare functionality.

This service provides high-level operations for importing, exporting, and working with autocare data across all subdomains."""
```
*Methods:*
```python
    def __init__(self, db):
        """Initialize the service.  Args: db: Database session"""
```
```python
    async def export_data(self, params) -> Dict[(str, Any)]:
        """Export data to an external file.

Args: params: Export parameters including file path, format, and filters

Returns: Export results including statistics

Raises: ExportException: If the export fails"""
```
```python
    async def get_database_versions(self) -> Dict[(str, str)]:
        """Get the current versions of all autocare databases.

Returns: Dictionary mapping database names to version strings"""
```
```python
    async def import_data(self, params) -> Dict[(str, Any)]:
        """Import data from an external file.

Args: params: Import parameters including file path, format, and options

Returns: Import results including statistics

Raises: ImportException: If the import fails"""
```
```python
    async def update_database(self, database_type, file_path) -> Dict[(str, Any)]:
        """Update a specific autocare database from a file.

Args: database_type: Type of database to update (vcdb, pcdb, padb, qdb) file_path: Path to the update file

Returns: Update results including version information

Raises: AutocareException: If the update fails"""
```

###### Package: fitment
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/fitment`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/fitment/__init__.py`

####### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/fitment/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, expression
from app.db.base_class import Base
```

**Classes:**
```python
class FitmentMapping(Base):
    """Model for mapping product fitments to autocare data."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_fitment_mapping'
product =     product = relationship("Product", foreign_keys=[product_id])
created_by =     created_by = relationship("User", foreign_keys=[created_by_id])
updated_by =     updated_by = relationship("User", foreign_keys=[updated_by_id])
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class FitmentMappingHistory(Base):
    """Model for tracking changes to fitment mappings."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_fitment_mapping_history'
mapping =     mapping = relationship("FitmentMapping", foreign_keys=[mapping_id])
changed_by =     changed_by = relationship("User", foreign_keys=[changed_by_id])
```
*Methods:*
```python
    def __repr__(self) -> str:
```

####### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/fitment/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import select, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.repositories.base import BaseRepository
from app.domains.autocare.fitment.models import FitmentMapping, FitmentMappingHistory
```

**Classes:**
```python
class FitmentMappingRepository(BaseRepository[(FitmentMapping, uuid.UUID)]):
    """Repository for FitmentMapping entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the fitment mapping repository.  Args: db: The database session."""
```
```python
    async def create_with_history(self, data, user_id) -> FitmentMapping:
        """Create a new fitment mapping and record history.

Args: data: The mapping data. user_id: Optional ID of the user creating the mapping.

Returns: The created mapping."""
```
```python
    async def delete_with_history(self, id, user_id) -> None:
        """Delete a fitment mapping and record history.

Args: id: The mapping ID. user_id: Optional ID of the user deleting the mapping.

Raises: ResourceNotFoundException: If the mapping is not found."""
```
```python
    async def find_by_base_vehicle(self, base_vehicle_id, page, page_size) -> Dict[(str, Any)]:
        """Find fitment mappings for a specific base vehicle.

Args: base_vehicle_id: The base vehicle ID. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def find_by_part(self, part_terminology_id, page, page_size) -> Dict[(str, Any)]:
        """Find fitment mappings for a specific part.

Args: part_terminology_id: The part terminology ID. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def find_by_product(self, product_id, page, page_size) -> Dict[(str, Any)]:
        """Find fitment mappings for a specific product.

Args: product_id: The product ID. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def find_by_vehicle(self, vehicle_id, page, page_size) -> Dict[(str, Any)]:
        """Find fitment mappings for a specific vehicle.

Args: vehicle_id: The vehicle ID. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_mapping_history(self, mapping_id, page, page_size) -> Dict[(str, Any)]:
        """Get history for a specific mapping.

Args: mapping_id: The mapping ID. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def search(self, product_query, is_validated, is_manual, page, page_size) -> Dict[(str, Any)]:
        """Search for fitment mappings with various filters.

Args: product_query: Optional product part number or name to search. is_validated: Optional validation status filter. is_manual: Optional manual entry filter. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def update_with_history(self, id, data, user_id) -> FitmentMapping:
        """Update a fitment mapping and record history.

Args: id: The mapping ID. data: The updated mapping data. user_id: Optional ID of the user updating the mapping.

Returns: The updated mapping.

Raises: ResourceNotFoundException: If the mapping is not found."""
```

####### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/fitment/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
```

**Classes:**
```python
class FitmentMapping(BaseModel):
    """Schema for fitment mapping data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FitmentMappingCreate(BaseModel):
    """Schema for creating a new fitment mapping."""
```

```python
class FitmentMappingDetail(FitmentMapping):
    """Schema for detailed fitment mapping data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FitmentMappingHistory(BaseModel):
    """Schema for fitment mapping history data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FitmentMappingHistoryResponse(BaseModel):
    """Schema for paginated fitment mapping history response."""
```

```python
class FitmentMappingSearchResponse(BaseModel):
    """Schema for paginated fitment mapping search response."""
```

```python
class FitmentMappingUpdate(BaseModel):
    """Schema for updating an existing fitment mapping."""
```

```python
class FitmentSearchParameters(BaseModel):
    """Schema for fitment mapping search parameters."""
```

```python
class ProductInfo(BaseModel):
    """Schema for minimal product information."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

####### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/fitment/service.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import MappingNotFoundException, ImportException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.fitment.repository import FitmentMappingRepository
from app.domains.autocare.fitment.models import FitmentMapping
from app.domains.products.repository import ProductRepository
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.autocare.fitment.service")
```

**Classes:**
```python
class FitmentMappingService(object):
    """Service for fitment mapping operations.

Provides methods for mapping products to autocare database entities."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the fitment mapping service.  Args: db: The database session."""
```
```python
    async def create_mapping(self, data, user_id) -> FitmentMapping:
        """Create a new fitment mapping.

Args: data: The mapping data. user_id: Optional ID of the user creating the mapping.

Returns: The created mapping.

Raises: ResourceNotFoundException: If the product is not found."""
```
```python
    async def delete_mapping(self, mapping_id, user_id) -> None:
        """Delete a fitment mapping.

Args: mapping_id: The mapping ID. user_id: Optional ID of the user deleting the mapping.

Raises: MappingNotFoundException: If the mapping is not found."""
```
```python
    async def find_mappings_by_product(self, product_id, page, page_size) -> Dict[(str, Any)]:
        """Find fitment mappings for a specific product.

Args: product_id: The product ID. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_mapping(self, mapping_id) -> Dict[(str, Any)]:
        """Get detailed information about a fitment mapping.

Args: mapping_id: The mapping ID.

Returns: Dict with detailed mapping information.

Raises: MappingNotFoundException: If the mapping is not found."""
```
```python
    async def get_mapping_history(self, mapping_id, page, page_size) -> Dict[(str, Any)]:
        """Get history for a specific mapping.

Args: mapping_id: The mapping ID. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info.

Raises: MappingNotFoundException: If the mapping is not found."""
```
```python
    async def import_from_aces(self, file_path, params) -> Dict[(str, Any)]:
        """Import fitment mappings from an ACES XML file.

Args: file_path: Path to the ACES XML file. params: Import parameters.

Returns: Dict with import results information."""
```
```python
    async def search_mappings(self, product_query, is_validated, is_manual, page, page_size) -> Dict[(str, Any)]:
        """Search for fitment mappings with various filters.

Args: product_query: Optional product part number or name to search. is_validated: Optional validation status filter. is_manual: Optional manual entry filter. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def update_mapping(self, mapping_id, data, user_id) -> FitmentMapping:
        """Update an existing fitment mapping.

Args: mapping_id: The mapping ID. data: The updated mapping data. user_id: Optional ID of the user updating the mapping.

Returns: The updated mapping.

Raises: MappingNotFoundException: If the mapping is not found."""
```

###### Package: padb
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/padb`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/padb/__init__.py`

####### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/padb/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
```

**Classes:**
```python
class MeasurementGroup(Base):
    """Model for measurement groupings."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_measurement_group'
uom_codes =     uom_codes = relationship("MetaUOMCode", back_populates="measurement_group")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class MetaData(Base):
    """Model for attribute metadata definitions."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_metadata'
assignments =     assignments = relationship("PartAttributeAssignment", back_populates="metadata")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class MetaUOMCode(Base):
    """Model for units of measure codes."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_meta_uom_code'
measurement_group =     measurement_group = relationship("MeasurementGroup", back_populates="uom_codes")
assignments =     assignments = relationship("MetaUomCodeAssignment", back_populates="meta_uom")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class MetaUomCodeAssignment(Base):
    """Model for assignments between attributes and UOM codes."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_meta_uom_code_assignment'
attribute_assignment =     attribute_assignment = relationship(
        "PartAttributeAssignment", back_populates="uom_assignments"
    )
meta_uom =     meta_uom = relationship("MetaUOMCode", back_populates="assignments")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PAdbVersion(Base):
    """Model for PAdb version tracking."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_padb_version'
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PartAttribute(Base):
    """Model for part attribute definitions."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_part_attribute'
assignments =     assignments = relationship("PartAttributeAssignment", back_populates="attribute")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PartAttributeAssignment(Base):
    """Model for assignments between parts, attributes, and metadata."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_part_attribute_assignment'
part =     part = relationship("Parts", foreign_keys=[part_terminology_id])
attribute =     attribute = relationship("PartAttribute", back_populates="assignments")
metadata =     metadata = relationship("MetaData", back_populates="assignments")
uom_assignments =     uom_assignments = relationship(
        "MetaUomCodeAssignment", back_populates="attribute_assignment"
    )
valid_value_assignments =     valid_value_assignments = relationship(
        "ValidValueAssignment", back_populates="attribute_assignment"
    )
style =     style = relationship("PartAttributeStyle", back_populates="attribute_assignment")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PartAttributeStyle(Base):
    """Model for part attribute styling."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_part_attribute_style'
style =     style = relationship("Style", back_populates="part_attribute_styles")
attribute_assignment =     attribute_assignment = relationship(
        "PartAttributeAssignment", back_populates="style"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PartTypeStyle(Base):
    """Model for part type styling."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_part_type_style'
style =     style = relationship("Style", back_populates="part_type_styles")
part =     part = relationship("Parts", foreign_keys=[part_terminology_id])
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class Style(Base):
    """Model for style definitions."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_style'
part_attribute_styles =     part_attribute_styles = relationship("PartAttributeStyle", back_populates="style")
part_type_styles =     part_type_styles = relationship("PartTypeStyle", back_populates="style")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class ValidValue(Base):
    """Model for valid values for attributes."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_valid_value'
assignments =     assignments = relationship("ValidValueAssignment", back_populates="valid_value")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class ValidValueAssignment(Base):
    """Model for assignments between attributes and valid values."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_valid_value_assignment'
attribute_assignment =     attribute_assignment = relationship(
        "PartAttributeAssignment", back_populates="valid_value_assignments"
    )
valid_value =     valid_value = relationship("ValidValue", back_populates="assignments")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

####### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/padb/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.padb.models import PartAttribute, MetaData, MetaUOMCode, PartAttributeAssignment, MetaUomCodeAssignment, ValidValue, ValidValueAssignment, PAdbVersion
```

**Classes:**
```python
class MetaDataRepository(BaseRepository[(MetaData, uuid.UUID)]):
    """Repository for MetaData entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the metadata repository.  Args: db: The database session."""
```
```python
    async def get_by_meta_id(self, meta_id) -> Optional[MetaData]:
        """Get metadata by its ID.

Args: meta_id: The metadata ID.

Returns: The metadata if found, None otherwise."""
```

```python
class MetaUOMCodeRepository(BaseRepository[(MetaUOMCode, uuid.UUID)]):
    """Repository for MetaUOMCode entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the UOM code repository.  Args: db: The database session."""
```
```python
    async def get_by_meta_uom_id(self, meta_uom_id) -> Optional[MetaUOMCode]:
        """Get a UOM code by its ID.

Args: meta_uom_id: The UOM code ID.

Returns: The UOM code if found, None otherwise."""
```
```python
    async def get_for_attribute_assignment(self, papt_id) -> List[MetaUOMCode]:
        """Get UOM codes for a specific attribute assignment.

Args: papt_id: The part attribute assignment ID.

Returns: List of UOM codes for the specified assignment."""
```

```python
class PAdbRepository(object):
    """Repository for PAdb entity operations.

Provides methods for querying PAdb data and managing database updates."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the PAdb repository.  Args: db: The database session."""
```
```python
    async def get_attributes_for_part(self, part_terminology_id) -> List[Dict[(str, Any)]]:
        """Get all attributes for a specific part.

Args: part_terminology_id: The part terminology ID.

Returns: List of attribute assignments with related attribute information."""
```
```python
    async def get_version(self) -> Optional[str]:
        """Get the current version of the PAdb database.

Returns: The version date as a string or None if no version is set."""
```
```python
    async def update_version(self, version_date) -> PAdbVersion:
        """Update the current version of the PAdb database.

Args: version_date: The new version date.

Returns: The updated version entity."""
```

```python
class PartAttributeRepository(BaseRepository[(PartAttribute, uuid.UUID)]):
    """Repository for PartAttribute entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the part attribute repository.  Args: db: The database session."""
```
```python
    async def get_by_pa_id(self, pa_id) -> Optional[PartAttribute]:
        """Get an attribute by its ID.

Args: pa_id: The attribute ID.

Returns: The attribute if found, None otherwise."""
```
```python
    async def search(self, search_term, page, page_size) -> Dict[(str, Any)]:
        """Search for attributes by name.

Args: search_term: The search term. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

```python
class ValidValueRepository(BaseRepository[(ValidValue, uuid.UUID)]):
    """Repository for ValidValue entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the valid value repository.  Args: db: The database session."""
```
```python
    async def get_by_valid_value_id(self, valid_value_id) -> Optional[ValidValue]:
        """Get a valid value by its ID.

Args: valid_value_id: The valid value ID.

Returns: The valid value if found, None otherwise."""
```
```python
    async def get_for_attribute_assignment(self, papt_id) -> List[ValidValue]:
        """Get valid values for a specific attribute assignment.

Args: papt_id: The part attribute assignment ID.

Returns: List of valid values for the specified assignment."""
```

####### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/padb/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
```

**Classes:**
```python
class AttributeSearchParameters(BaseModel):
    """Schema for attribute search parameters."""
```

```python
class AttributeSearchResponse(BaseModel):
    """Schema for paginated attribute search response."""
```

```python
class AttributeWithMetadata(BaseModel):
    """Schema for attribute with metadata and valid values."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class MeasurementGroup(BaseModel):
    """Schema for measurement group data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class MetaData(BaseModel):
    """Schema for attribute metadata."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class MetaUOMCode(BaseModel):
    """Schema for unit of measure code data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class PartAttribute(BaseModel):
    """Schema for part attribute data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class PartAttributeAssignment(BaseModel):
    """Schema for part attribute assignment data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class PartAttributeDetail(BaseModel):
    """Schema for detailed part attribute data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class PartAttributesResponse(BaseModel):
    """Schema for part attributes response."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ValidValue(BaseModel):
    """Schema for valid value data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

####### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/padb/service.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
from datetime import datetime
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import PAdbException
from app.domains.autocare.padb.repository import PAdbRepository
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.autocare.padb.service")
```

**Classes:**
```python
class PAdbService(object):
    """Service for PAdb operations.

Provides methods for importing, exporting, and querying parts attribute data."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the PAdb service.  Args: db: The database session."""
```
```python
    async def get_attribute_details(self, pa_id) -> Dict[(str, Any)]:
        """Get detailed information about a part attribute.

Args: pa_id: The part attribute ID.

Returns: Dict with detailed attribute information."""
```
```python
    async def get_part_attributes(self, part_terminology_id) -> Dict[(str, Any)]:
        """Get attributes for a specific part.

Args: part_terminology_id: The part terminology ID.

Returns: Dict with part attributes information."""
```
```python
    async def get_version(self) -> str:
        """Get the current version of the PAdb database.  Returns: The version date as a string."""
```
```python
    async def search_attributes(self, search_term, page, page_size) -> Dict[(str, Any)]:
        """Search for part attributes.

Args: search_term: The search term. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def update_database(self, file_path) -> Dict[(str, Any)]:
        """Update the PAdb database from a file.

Args: file_path: Path to the update file.

Returns: Dict with update results information."""
```

###### Package: pcdb
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/pcdb`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/pcdb/__init__.py`

####### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/pcdb/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from typing import Optional
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
```

**Global Variables:**
```python
parts_to_alias = parts_to_alias = Table(
    "autocare_parts_to_alias",
    Base.metadata,
    mapped_column(
        "part_terminology_id",
        Integer,
        ForeignKey("autocare_parts.part_terminology_id"),
        primary_key=True,
    ),
    mapped_column(
        "alias_id", Integer, ForeignKey("autocare_alias.alias_id"), primary_key=True
    ),
)
parts_to_use = parts_to_use = Table(
    "autocare_parts_to_use",
    Base.metadata,
    mapped_column(
        "part_terminology_id",
        Integer,
        ForeignKey("autocare_parts.part_terminology_id"),
        primary_key=True,
    ),
    mapped_column(
        "use_id", Integer, ForeignKey("autocare_use.use_id"), primary_key=True
    ),
)
```

**Classes:**
```python
class Alias(Base):
    """Model for part aliases."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_alias'
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class Category(Base):
    """Model for parts categories."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_category'
part_categories =     part_categories = relationship("PartCategory", back_populates="category")
code_masters =     code_masters = relationship("CodeMaster", back_populates="category")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class CodeMaster(Base):
    """Model for code master which links parts, categories, subcategories, and positions."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_code_master'
part =     part = relationship("Parts", foreign_keys=[part_terminology_id])
category =     category = relationship("Category", back_populates="code_masters")
subcategory =     subcategory = relationship("SubCategory", back_populates="code_masters")
position =     position = relationship("Position", back_populates="code_masters")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PCdbVersion(Base):
    """Model for PCdb version tracking."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_pcdb_version'
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PartCategory(Base):
    """Model for parts to category mapping."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_part_category'
part =     part = relationship("Parts", back_populates="categories")
subcategory =     subcategory = relationship("SubCategory", back_populates="part_categories")
category =     category = relationship("Category", back_populates="part_categories")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PartPosition(Base):
    """Model for parts to position mapping."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_part_position'
part =     part = relationship("Parts", back_populates="positions")
position =     position = relationship("Position", back_populates="part_positions")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class Parts(Base):
    """Model for parts terminology."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_parts'
description =     description = relationship("PartsDescription", back_populates="parts")
categories =     categories = relationship("PartCategory", back_populates="part")
positions =     positions = relationship("PartPosition", back_populates="part")
attributes =     attributes = relationship("PartAttributeAssignment", back_populates="part")
supersessions =     supersessions = relationship(
        "PartsSupersession",
        foreign_keys="[PartsSupersession.new_part_terminology_id]",
        primaryjoin="Parts.part_terminology_id==PartsSupersession.new_part_terminology_id",
        backref="new_part",
    )
superseded_by =     superseded_by = relationship(
        "PartsSupersession",
        foreign_keys="[PartsSupersession.old_part_terminology_id]",
        primaryjoin="Parts.part_terminology_id==PartsSupersession.old_part_terminology_id",
        backref="old_part",
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PartsDescription(Base):
    """Model for parts descriptions."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_parts_description'
parts =     parts = relationship("Parts", back_populates="description")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class PartsSupersession(Base):
    """Model for parts supersession."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_parts_supersession'
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class Position(Base):
    """Model for parts positions."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_position'
part_positions =     part_positions = relationship("PartPosition", back_populates="position")
code_masters =     code_masters = relationship("CodeMaster", back_populates="position")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class SubCategory(Base):
    """Model for parts subcategories."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_subcategory'
part_categories =     part_categories = relationship("PartCategory", back_populates="subcategory")
code_masters =     code_masters = relationship("CodeMaster", back_populates="subcategory")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class Use(Base):
    """Model for part uses."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_use'
```
*Methods:*
```python
    def __repr__(self) -> str:
```

####### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/pcdb/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.pcdb.models import Parts, Category, SubCategory, Position, PartCategory, PartPosition, PartsSupersession, PCdbVersion
```

**Classes:**
```python
class CategoryRepository(BaseRepository[(Category, uuid.UUID)]):
    """Repository for Category entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the category repository.  Args: db: The database session."""
```
```python
    async def get_all_categories(self) -> List[Category]:
        """Get all categories.  Returns: List of all categories."""
```
```python
    async def get_by_category_id(self, category_id) -> Optional[Category]:
        """Get a category by its ID.

Args: category_id: The category ID.

Returns: The category if found, None otherwise."""
```
```python
    async def search(self, search_term) -> List[Category]:
        """Search for categories by name.

Args: search_term: The search term.

Returns: List of matching categories."""
```

```python
class PCdbRepository(object):
    """Repository for PCdb entity operations.

Provides methods for querying PCdb data and managing database updates."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the PCdb repository.  Args: db: The database session."""
```
```python
    async def get_version(self) -> Optional[str]:
        """Get the current version of the PCdb database.

Returns: The version date as a string or None if no version is set."""
```
```python
    async def search_parts(self, search_term, categories, page, page_size) -> Dict[(str, Any)]:
        """Search for parts by term and optional category filters.

Args: search_term: The search term. categories: Optional list of category IDs to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def update_version(self, version_date) -> PCdbVersion:
        """Update the current version of the PCdb database.

Args: version_date: The new version date.

Returns: The updated version entity."""
```

```python
class PartsRepository(BaseRepository[(Parts, uuid.UUID)]):
    """Repository for Parts entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the parts repository.  Args: db: The database session."""
```
```python
    async def get_by_category(self, category_id, page, page_size) -> Dict[(str, Any)]:
        """Get parts by category.

Args: category_id: The category ID. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_terminology_id(self, part_terminology_id) -> Optional[Parts]:
        """Get a part by its terminology ID.

Args: part_terminology_id: The part terminology ID.

Returns: The part if found, None otherwise."""
```
```python
    async def get_supersessions(self, part_terminology_id) -> Dict[(str, List[Parts])]:
        """Get supersession information for a part.

Args: part_terminology_id: The part terminology ID.

Returns: Dict with superseded_by and supersedes lists."""
```
```python
    async def search(self, search_term, categories, page, page_size) -> Dict[(str, Any)]:
        """Search for parts by term and optional category filters.

Args: search_term: The search term. categories: Optional list of category IDs to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

```python
class PositionRepository(BaseRepository[(Position, uuid.UUID)]):
    """Repository for Position entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the position repository.  Args: db: The database session."""
```
```python
    async def get_all_positions(self) -> List[Position]:
        """Get all positions.  Returns: List of all positions."""
```
```python
    async def get_by_part(self, part_terminology_id) -> List[Position]:
        """Get positions for a specific part.

Args: part_terminology_id: The part terminology ID.

Returns: List of positions for the specified part."""
```
```python
    async def get_by_position_id(self, position_id) -> Optional[Position]:
        """Get a position by its ID.

Args: position_id: The position ID.

Returns: The position if found, None otherwise."""
```

```python
class SubCategoryRepository(BaseRepository[(SubCategory, uuid.UUID)]):
    """Repository for SubCategory entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the subcategory repository.  Args: db: The database session."""
```
```python
    async def get_by_category(self, category_id) -> List[SubCategory]:
        """Get subcategories by category.

Args: category_id: The category ID.

Returns: List of subcategories in the specified category."""
```
```python
    async def get_by_subcategory_id(self, subcategory_id) -> Optional[SubCategory]:
        """Get a subcategory by its ID.

Args: subcategory_id: The subcategory ID.

Returns: The subcategory if found, None otherwise."""
```

####### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/pcdb/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
```

**Classes:**
```python
class Category(BaseModel):
    """Schema for part category data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Part(BaseModel):
    """Schema for part data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class PartDetail(Part):
    """Schema for detailed part data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class PartSearchParameters(BaseModel):
    """Schema for part search parameters."""
```

```python
class PartSearchResponse(BaseModel):
    """Schema for paginated part search response."""
```

```python
class Position(BaseModel):
    """Schema for part position data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class SubCategory(BaseModel):
    """Schema for part subcategory data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

####### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/pcdb/service.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import PCdbException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.pcdb.repository import PCdbRepository
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.autocare.pcdb.service")
```

**Classes:**
```python
class PCdbService(object):
    """Service for PCdb operations.  Provides methods for importing, exporting, and querying parts data."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the PCdb service.  Args: db: The database session."""
```
```python
    async def get_categories(self) -> List[Dict[(str, Any)]]:
        """Get all parts categories.  Returns: List of categories with their IDs and names."""
```
```python
    async def get_part_details(self, part_terminology_id) -> Dict[(str, Any)]:
        """Get detailed information about a part.

Args: part_terminology_id: The part terminology ID.

Returns: Dict with detailed part information."""
```
```python
    async def get_subcategories_by_category(self, category_id) -> List[Dict[(str, Any)]]:
        """Get subcategories for a specific category.

Args: category_id: The category ID.

Returns: List of subcategories with their IDs and names."""
```
```python
    async def get_version(self) -> str:
        """Get the current version of the PCdb database.  Returns: The version date as a string."""
```
```python
    async def import_from_pies(self, file_path, params) -> Dict[(str, Any)]:
        """Import parts data from a PIES XML file.

Args: file_path: Path to the PIES XML file. params: Import parameters.

Returns: Dict with import results information."""
```
```python
    async def search_parts(self, search_term, categories, page, page_size) -> Dict[(str, Any)]:
        """Search for parts with optional category filters.

Args: search_term: The search term. categories: Optional list of category IDs to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def update_database(self, file_path) -> Dict[(str, Any)]:
        """Update the PCdb database from a file.

Args: file_path: Path to the update file.

Returns: Dict with update results information."""
```

###### Package: qdb
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/qdb`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/qdb/__init__.py`

####### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/qdb/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
```

**Classes:**
```python
class GroupNumber(Base):
    """Model for qualifier group numbers."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_group_number'
qualifier_groups =     qualifier_groups = relationship("QualifierGroup", back_populates="group_number")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class Language(Base):
    """Model for languages."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_language'
translations =     translations = relationship("QualifierTranslation", back_populates="language")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class QdbVersion(Base):
    """Model for Qdb version tracking."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_qdb_version'
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class Qualifier(Base):
    """Model for qualifiers."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_qualifier'
qualifier_type =     qualifier_type = relationship("QualifierType", back_populates="qualifiers")
translations =     translations = relationship("QualifierTranslation", back_populates="qualifier")
groups =     groups = relationship("QualifierGroup", back_populates="qualifier")
superseded_by =     superseded_by = relationship(
        "Qualifier",
        remote_side=[id],
        foreign_keys=[new_qualifier_id],
        backref="supersedes",
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class QualifierGroup(Base):
    """Model for qualifier groups."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_qualifier_group'
group_number =     group_number = relationship("GroupNumber", back_populates="qualifier_groups")
qualifier =     qualifier = relationship("Qualifier", back_populates="groups")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class QualifierTranslation(Base):
    """Model for qualifier translations."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_qualifier_translation'
qualifier =     qualifier = relationship("Qualifier", back_populates="translations")
language =     language = relationship("Language", back_populates="translations")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class QualifierType(Base):
    """Model for qualifier types."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_qualifier_type'
qualifiers =     qualifiers = relationship("Qualifier", back_populates="qualifier_type")
```
*Methods:*
```python
    def __repr__(self) -> str:
```

####### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/qdb/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.qdb.models import QualifierType, Qualifier, Language, QualifierTranslation, GroupNumber, QualifierGroup, QdbVersion
```

**Classes:**
```python
class GroupNumberRepository(BaseRepository[(GroupNumber, uuid.UUID)]):
    """Repository for GroupNumber entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the group number repository.  Args: db: The database session."""
```
```python
    async def get_all_groups(self) -> List[GroupNumber]:
        """Get all group numbers.  Returns: List of all group numbers."""
```
```python
    async def get_by_group_number_id(self, group_number_id) -> Optional[GroupNumber]:
        """Get a group number by its ID.

Args: group_number_id: The group number ID.

Returns: The group number if found, None otherwise."""
```
```python
    async def get_qualifiers_by_group(self, group_number_id, page, page_size) -> Dict[(str, Any)]:
        """Get qualifiers for a specific group.

Args: group_number_id: The group number ID. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

```python
class LanguageRepository(BaseRepository[(Language, uuid.UUID)]):
    """Repository for Language entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the language repository.  Args: db: The database session."""
```
```python
    async def get_all_languages(self) -> List[Language]:
        """Get all languages.  Returns: List of all languages."""
```
```python
    async def get_by_language_id(self, language_id) -> Optional[Language]:
        """Get a language by its ID.

Args: language_id: The language ID.

Returns: The language if found, None otherwise."""
```

```python
class QdbRepository(object):
    """Repository for Qdb entity operations.

Provides methods for querying Qdb data and managing database updates."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the Qdb repository.  Args: db: The database session."""
```
```python
    async def get_version(self) -> Optional[str]:
        """Get the current version of the Qdb database.

Returns: The version date as a string or None if no version is set."""
```
```python
    async def search_qualifiers(self, search_term, qualifier_type_id, language_id, page, page_size) -> Dict[(str, Any)]:
        """Search for qualifiers with optional filters.

Args: search_term: The search term. qualifier_type_id: Optional qualifier type ID to filter by. language_id: Optional language ID to search translations. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def update_version(self, version_date) -> QdbVersion:
        """Update the current version of the Qdb database.

Args: version_date: The new version date.

Returns: The updated version entity."""
```

```python
class QualifierRepository(BaseRepository[(Qualifier, uuid.UUID)]):
    """Repository for Qualifier entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the qualifier repository.  Args: db: The database session."""
```
```python
    async def get_by_qualifier_id(self, qualifier_id) -> Optional[Qualifier]:
        """Get a qualifier by its ID.

Args: qualifier_id: The qualifier ID.

Returns: The qualifier if found, None otherwise."""
```
```python
    async def get_groups(self, qualifier_id) -> List[Dict[(str, Any)]]:
        """Get groups for a qualifier.

Args: qualifier_id: The qualifier ID.

Returns: List of groups with group number info."""
```
```python
    async def get_translations(self, qualifier_id, language_id) -> List[QualifierTranslation]:
        """Get translations for a qualifier.

Args: qualifier_id: The qualifier ID. language_id: Optional language ID to filter by.

Returns: List of translations for the qualifier."""
```
```python
    async def search(self, search_term, qualifier_type_id, language_id, page, page_size) -> Dict[(str, Any)]:
        """Search for qualifiers with optional filters.

Args: search_term: The search term. qualifier_type_id: Optional qualifier type ID to filter by. language_id: Optional language ID to search translations. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

```python
class QualifierTypeRepository(BaseRepository[(QualifierType, uuid.UUID)]):
    """Repository for QualifierType entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the qualifier type repository.  Args: db: The database session."""
```
```python
    async def get_all_types(self) -> List[QualifierType]:
        """Get all qualifier types.  Returns: List of all qualifier types."""
```
```python
    async def get_by_qualifier_type_id(self, qualifier_type_id) -> Optional[QualifierType]:
        """Get a qualifier type by its ID.

Args: qualifier_type_id: The qualifier type ID.

Returns: The qualifier type if found, None otherwise."""
```

####### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/qdb/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
```

**Classes:**
```python
class GroupNumber(BaseModel):
    """Schema for group number data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Language(BaseModel):
    """Schema for language data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Qualifier(BaseModel):
    """Schema for qualifier data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class QualifierDetail(Qualifier):
    """Schema for detailed qualifier data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class QualifierGroup(BaseModel):
    """Schema for qualifier group data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class QualifierSearchParameters(BaseModel):
    """Schema for qualifier search parameters."""
```

```python
class QualifierSearchResponse(BaseModel):
    """Schema for paginated qualifier search response."""
```

```python
class QualifierTranslation(BaseModel):
    """Schema for qualifier translation data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class QualifierType(BaseModel):
    """Schema for qualifier type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

####### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/qdb/service.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import QdbException
from app.domains.autocare.qdb.repository import QdbRepository
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.autocare.qdb.service")
```

**Classes:**
```python
class QdbService(object):
    """Service for Qdb operations.

Provides methods for importing, exporting, and querying qualifier data."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the Qdb service.  Args: db: The database session."""
```
```python
    async def get_languages(self) -> List[Dict[(str, Any)]]:
        """Get all languages.  Returns: List of languages with their IDs and names."""
```
```python
    async def get_qualifier_details(self, qualifier_id) -> Dict[(str, Any)]:
        """Get detailed information about a qualifier.

Args: qualifier_id: The qualifier ID.

Returns: Dict with detailed qualifier information."""
```
```python
    async def get_qualifier_types(self) -> List[Dict[(str, Any)]]:
        """Get all qualifier types.  Returns: List of qualifier types with their IDs and names."""
```
```python
    async def get_version(self) -> str:
        """Get the current version of the Qdb database.  Returns: The version date as a string."""
```
```python
    async def search_qualifiers(self, search_term, qualifier_type_id, language_id, page, page_size) -> Dict[(str, Any)]:
        """Search for qualifiers with optional filters.

Args: search_term: The search term. qualifier_type_id: Optional qualifier type ID to filter by. language_id: Optional language ID to search translations. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def update_database(self, file_path) -> Dict[(str, Any)]:
        """Update the Qdb database from a file.

Args: file_path: Path to the update file.

Returns: Dict with update results information."""
```

###### Package: vcdb
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/vcdb`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/vcdb/__init__.py`

####### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/vcdb/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
```

**Global Variables:**
```python
vehicle_to_drive_type = vehicle_to_drive_type = Table(
    "autocare_vehicle_to_drive_type",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "drive_type_id",
        Integer,
        ForeignKey("autocare_drive_type.drive_type_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_brake_config = vehicle_to_brake_config = Table(
    "autocare_vehicle_to_brake_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "brake_config_id",
        Integer,
        ForeignKey("autocare_brake_config.brake_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_bed_config = vehicle_to_bed_config = Table(
    "autocare_vehicle_to_bed_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "bed_config_id",
        Integer,
        ForeignKey("autocare_bed_config.bed_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_body_style_config = vehicle_to_body_style_config = Table(
    "autocare_vehicle_to_body_style_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "body_style_config_id",
        Integer,
        ForeignKey("autocare_body_style_config.body_style_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_mfr_body_code = vehicle_to_mfr_body_code = Table(
    "autocare_vehicle_to_mfr_body_code",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "mfr_body_code_id",
        Integer,
        ForeignKey("autocare_mfr_body_code.mfr_body_code_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_engine_config = vehicle_to_engine_config = Table(
    "autocare_vehicle_to_engine_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "engine_config_id",
        Integer,
        ForeignKey("autocare_engine_config.engine_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_spring_type_config = vehicle_to_spring_type_config = Table(
    "autocare_vehicle_to_spring_type_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "spring_type_config_id",
        Integer,
        ForeignKey("autocare_spring_type_config.spring_type_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_steering_config = vehicle_to_steering_config = Table(
    "autocare_vehicle_to_steering_config",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "steering_config_id",
        Integer,
        ForeignKey("autocare_steering_config.steering_config_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_transmission = vehicle_to_transmission = Table(
    "autocare_vehicle_to_transmission",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "transmission_id",
        Integer,
        ForeignKey("autocare_transmission.transmission_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
vehicle_to_wheel_base = vehicle_to_wheel_base = Table(
    "autocare_vehicle_to_wheel_base",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "vehicle_id", Integer, ForeignKey("autocare_vehicle.vehicle_id"), nullable=False
    ),
    Column(
        "wheel_base_id",
        Integer,
        ForeignKey("autocare_wheel_base.wheel_base_id"),
        nullable=False,
    ),
    Column("source", String(10), nullable=True),
)
```

**Classes:**
```python
class Aspiration(Base):
    """Aspiration entity representing engine aspiration types.

Attributes: id: Primary key. aspiration_id: VCdb specific ID. name: Aspiration type name. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_aspiration'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="aspiration")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Aspiration instance.  Returns: String representation."""
```

```python
class BaseVehicle(Base):
    """BaseVehicle entity representing basic vehicle identification.

Attributes: id: Primary key. base_vehicle_id: VCdb specific ID. year_id: Reference to year. make_id: Reference to make. model_id: Reference to model. year: Relationship to year. make: Relationship to make. model: Relationship to model. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_base_vehicle'
year =     year = relationship("Year", back_populates="base_vehicles")
make =     make = relationship("Make", back_populates="base_vehicles")
model =     model = relationship("Model", back_populates="base_vehicles")
vehicles =     vehicles = relationship("Vehicle", back_populates="base_vehicle")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BaseVehicle instance.  Returns: String representation."""
```

```python
class BedConfig(Base):
    """BedConfig entity representing bed configurations.

Attributes: id: Primary key. bed_config_id: VCdb specific ID. bed_length_id: Reference to bed length. bed_type_id: Reference to bed type. bed_length: Relationship to bed length. bed_type: Relationship to bed type. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_bed_config'
bed_length =     bed_length = relationship("BedLength", back_populates="bed_configs")
bed_type =     bed_type = relationship("BedType", back_populates="bed_configs")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BedConfig instance.  Returns: String representation."""
```

```python
class BedLength(Base):
    """BedLength entity representing bed length measurements.

Attributes: id: Primary key. bed_length_id: VCdb specific ID. length: Bed length in imperial units. length_metric: Bed length in metric units. bed_configs: Relationship to bed configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_bed_length'
bed_configs =     bed_configs = relationship("BedConfig", back_populates="bed_length")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BedLength instance.  Returns: String representation."""
```

```python
class BedType(Base):
    """BedType entity representing types of vehicle beds.

Attributes: id: Primary key. bed_type_id: VCdb specific ID. name: Bed type name. bed_configs: Relationship to bed configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_bed_type'
bed_configs =     bed_configs = relationship("BedConfig", back_populates="bed_type")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BedType instance.  Returns: String representation."""
```

```python
class BodyNumDoors(Base):
    """BodyNumDoors entity representing number of doors.

Attributes: id: Primary key. body_num_doors_id: VCdb specific ID. num_doors: Number of doors string. body_style_configs: Relationship to body style configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_body_num_doors'
body_style_configs =     body_style_configs = relationship(
        "BodyStyleConfig", back_populates="body_num_doors"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BodyNumDoors instance.  Returns: String representation."""
```

```python
class BodyStyleConfig(Base):
    """BodyStyleConfig entity representing body style configurations.

Attributes: id: Primary key. body_style_config_id: VCdb specific ID. body_num_doors_id: Reference to body number of doors. body_type_id: Reference to body type. body_num_doors: Relationship to body number of doors. body_type: Relationship to body type. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_body_style_config'
body_num_doors =     body_num_doors = relationship("BodyNumDoors", back_populates="body_style_configs")
body_type =     body_type = relationship("BodyType", back_populates="body_style_configs")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BodyStyleConfig instance.  Returns: String representation."""
```

```python
class BodyType(Base):
    """BodyType entity representing types of vehicle bodies.

Attributes: id: Primary key. body_type_id: VCdb specific ID. name: Body type name. body_style_configs: Relationship to body style configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_body_type'
body_style_configs =     body_style_configs = relationship("BodyStyleConfig", back_populates="body_type")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BodyType instance.  Returns: String representation."""
```

```python
class BrakeABS(Base):
    """BrakeABS entity representing ABS configurations.

Attributes: id: Primary key. brake_abs_id: VCdb specific ID. name: ABS configuration name. brake_configs: Relationship to brake configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_brake_abs'
brake_configs =     brake_configs = relationship("BrakeConfig", back_populates="brake_abs")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BrakeABS instance.  Returns: String representation."""
```

```python
class BrakeConfig(Base):
    """BrakeConfig entity representing complete brake configurations.

Attributes: id: Primary key. brake_config_id: VCdb specific ID. front_brake_type_id: Reference to front brake type. rear_brake_type_id: Reference to rear brake type. brake_system_id: Reference to brake system. brake_abs_id: Reference to ABS configuration. front_brake_type: Relationship to front brake type. rear_brake_type: Relationship to rear brake type. brake_system: Relationship to brake system. brake_abs: Relationship to ABS configuration. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_brake_config'
front_brake_type =     front_brake_type = relationship(
        "BrakeType",
        foreign_keys=[front_brake_type_id],
        back_populates="front_brake_configs",
    )
rear_brake_type =     rear_brake_type = relationship(
        "BrakeType",
        foreign_keys=[rear_brake_type_id],
        back_populates="rear_brake_configs",
    )
brake_system =     brake_system = relationship("BrakeSystem", back_populates="brake_configs")
brake_abs =     brake_abs = relationship("BrakeABS", back_populates="brake_configs")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BrakeConfig instance.  Returns: String representation."""
```

```python
class BrakeSystem(Base):
    """BrakeSystem entity representing brake system configurations.

Attributes: id: Primary key. brake_system_id: VCdb specific ID. name: Brake system name. brake_configs: Relationship to brake configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_brake_system'
brake_configs =     brake_configs = relationship("BrakeConfig", back_populates="brake_system")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BrakeSystem instance.  Returns: String representation."""
```

```python
class BrakeType(Base):
    """BrakeType entity representing types of brake systems.

Attributes: id: Primary key. brake_type_id: VCdb specific ID. name: Brake type name. front_brake_configs: Relationship to brake configs (as front). rear_brake_configs: Relationship to brake configs (as rear)."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_brake_type'
front_brake_configs =     front_brake_configs = relationship(
        "BrakeConfig",
        foreign_keys="[BrakeConfig.front_brake_type_id]",
        back_populates="front_brake_type",
    )
rear_brake_configs =     rear_brake_configs = relationship(
        "BrakeConfig",
        foreign_keys="[BrakeConfig.rear_brake_type_id]",
        back_populates="rear_brake_type",
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of BrakeType instance.  Returns: String representation."""
```

```python
class CylinderHeadType(Base):
    """CylinderHeadType entity representing cylinder head types.

Attributes: id: Primary key. cylinder_head_type_id: VCdb specific ID. name: Cylinder head type name. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_cylinder_head_type'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="cylinder_head_type")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of CylinderHeadType instance.  Returns: String representation."""
```

```python
class DriveType(Base):
    """DriveType entity representing types of drive systems.

Attributes: id: Primary key. drive_type_id: VCdb specific ID. name: Drive type name. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_drive_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of DriveType instance.  Returns: String representation."""
```

```python
class ElecControlled(Base):
    """ElecControlled entity representing electronic controlled status.

Attributes: id: Primary key. elec_controlled_id: VCdb specific ID. value: Electronic controlled value. transmissions: Relationship to transmissions."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_elec_controlled'
transmissions =     transmissions = relationship("Transmission", back_populates="elec_controlled")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ElecControlled instance.  Returns: String representation."""
```

```python
class EngineBase(Base):
    """EngineBase entity representing base engine specifications.

Attributes: id: Primary key. engine_base_id: VCdb specific ID. engine_block_id: Reference to engine block. engine_bore_stroke_id: Reference to engine bore stroke. engine_block: Relationship to engine block. engine_bore_stroke: Relationship to engine bore stroke. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_engine_base'
engine_block =     engine_block = relationship("EngineBlock", back_populates="engine_bases")
engine_bore_stroke =     engine_bore_stroke = relationship("EngineBoreStroke", back_populates="engine_bases")
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="engine_base")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of EngineBase instance.  Returns: String representation."""
```

```python
class EngineBlock(Base):
    """EngineBlock entity representing engine block specifications.

Attributes: id: Primary key. engine_block_id: VCdb specific ID. liter: Engine size in liters. cc: Engine size in cubic centimeters. cid: Engine size in cubic inches displacement. cylinders: Number of cylinders. block_type: Engine block type. engine_bases: Relationship to engine bases."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_engine_block'
engine_bases =     engine_bases = relationship("EngineBase", back_populates="engine_block")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of EngineBlock instance.  Returns: String representation."""
```

```python
class EngineBoreStroke(Base):
    """EngineBoreStroke entity representing engine bore and stroke measurements.

Attributes: id: Primary key. engine_bore_stroke_id: VCdb specific ID. bore_in: Bore measurement in inches. bore_metric: Bore measurement in metric. stroke_in: Stroke measurement in inches. stroke_metric: Stroke measurement in metric. engine_bases: Relationship to engine bases."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_engine_bore_stroke'
engine_bases =     engine_bases = relationship("EngineBase", back_populates="engine_bore_stroke")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of EngineBoreStroke instance.  Returns: String representation."""
```

```python
class EngineConfig(Base):
    """EngineConfig entity representing complete engine configurations.

Attributes: id: Primary key. engine_config_id: VCdb specific ID. engine_base_id: Reference to engine base. engine_designation_id: Reference to engine designation. engine_vin_id: Reference to engine VIN. valves_id: Reference to valves. fuel_delivery_config_id: Reference to fuel delivery config. aspiration_id: Reference to aspiration. cylinder_head_type_id: Reference to cylinder head type. fuel_type_id: Reference to fuel type. ignition_system_type_id: Reference to ignition system type. engine_mfr_id: Reference to engine manufacturer. engine_version_id: Reference to engine version. power_output_id: Reference to power output. engine_base: Relationship to engine base. engine_designation: Relationship to engine designation. engine_vin: Relationship to engine VIN. valves: Relationship to valves. fuel_delivery_config: Relationship to fuel delivery config. aspiration: Relationship to aspiration. cylinder_head_type: Relationship to cylinder head type. fuel_type: Relationship to fuel type. ignition_system_type: Relationship to ignition system type. engine_mfr: Relationship to engine manufacturer. engine_version: Relationship to engine version. power_output: Relationship to power output. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_engine_config'
engine_base =     engine_base = relationship("EngineBase", back_populates="engine_configs")
engine_designation =     engine_designation = relationship(
        "EngineDesignation", back_populates="engine_configs"
    )
engine_vin =     engine_vin = relationship("EngineVIN", back_populates="engine_configs")
valves =     valves = relationship("Valves", back_populates="engine_configs")
fuel_delivery_config =     fuel_delivery_config = relationship(
        "FuelDeliveryConfig", back_populates="engine_configs"
    )
aspiration =     aspiration = relationship("Aspiration", back_populates="engine_configs")
cylinder_head_type =     cylinder_head_type = relationship(
        "CylinderHeadType", back_populates="engine_configs"
    )
fuel_type =     fuel_type = relationship("FuelType", back_populates="engine_configs")
ignition_system_type =     ignition_system_type = relationship(
        "IgnitionSystemType", back_populates="engine_configs"
    )
engine_mfr =     engine_mfr = relationship("Mfr", back_populates="engine_configs")
engine_version =     engine_version = relationship("EngineVersion", back_populates="engine_configs")
power_output =     power_output = relationship("PowerOutput", back_populates="engine_configs")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of EngineConfig instance.  Returns: String representation."""
```

```python
class EngineDesignation(Base):
    """EngineDesignation entity representing engine designation codes.

Attributes: id: Primary key. engine_designation_id: VCdb specific ID. name: Engine designation name. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_engine_designation'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="engine_designation")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of EngineDesignation instance.  Returns: String representation."""
```

```python
class EngineVIN(Base):
    """EngineVIN entity representing engine VIN codes.

Attributes: id: Primary key. engine_vin_id: VCdb specific ID. code: Engine VIN code. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_engine_vin'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="engine_vin")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of EngineVIN instance.  Returns: String representation."""
```

```python
class EngineVersion(Base):
    """EngineVersion entity representing engine versions.

Attributes: id: Primary key. engine_version_id: VCdb specific ID. version: Engine version value. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_engine_version'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="engine_version")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of EngineVersion instance.  Returns: String representation."""
```

```python
class FuelDeliveryConfig(Base):
    """FuelDeliveryConfig entity representing fuel delivery configurations.

Attributes: id: Primary key. fuel_delivery_config_id: VCdb specific ID. fuel_delivery_type_id: Reference to fuel delivery type. fuel_delivery_subtype_id: Reference to fuel delivery subtype. fuel_system_control_type_id: Reference to fuel system control type. fuel_system_design_id: Reference to fuel system design. fuel_delivery_type: Relationship to fuel delivery type. fuel_delivery_subtype: Relationship to fuel delivery subtype. fuel_system_control_type: Relationship to fuel system control type. fuel_system_design: Relationship to fuel system design. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_fuel_delivery_config'
fuel_delivery_type =     fuel_delivery_type = relationship(
        "FuelDeliveryType", back_populates="fuel_delivery_configs"
    )
fuel_delivery_subtype =     fuel_delivery_subtype = relationship(
        "FuelDeliverySubType", back_populates="fuel_delivery_configs"
    )
fuel_system_control_type =     fuel_system_control_type = relationship(
        "FuelSystemControlType", back_populates="fuel_delivery_configs"
    )
fuel_system_design =     fuel_system_design = relationship(
        "FuelSystemDesign", back_populates="fuel_delivery_configs"
    )
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="fuel_delivery_config")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of FuelDeliveryConfig instance.  Returns: String representation."""
```

```python
class FuelDeliverySubType(Base):
    """FuelDeliverySubType entity representing fuel delivery subtypes.

Attributes: id: Primary key. fuel_delivery_subtype_id: VCdb specific ID. name: Fuel delivery subtype name. fuel_delivery_configs: Relationship to fuel delivery configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_fuel_delivery_subtype'
fuel_delivery_configs =     fuel_delivery_configs = relationship(
        "FuelDeliveryConfig", back_populates="fuel_delivery_subtype"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of FuelDeliverySubType instance.  Returns: String representation."""
```

```python
class FuelDeliveryType(Base):
    """FuelDeliveryType entity representing fuel delivery types.

Attributes: id: Primary key. fuel_delivery_type_id: VCdb specific ID. name: Fuel delivery type name. fuel_delivery_configs: Relationship to fuel delivery configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_fuel_delivery_type'
fuel_delivery_configs =     fuel_delivery_configs = relationship(
        "FuelDeliveryConfig", back_populates="fuel_delivery_type"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of FuelDeliveryType instance.  Returns: String representation."""
```

```python
class FuelSystemControlType(Base):
    """FuelSystemControlType entity representing fuel system control types.

Attributes: id: Primary key. fuel_system_control_type_id: VCdb specific ID. name: Fuel system control type name. fuel_delivery_configs: Relationship to fuel delivery configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_fuel_system_control_type'
fuel_delivery_configs =     fuel_delivery_configs = relationship(
        "FuelDeliveryConfig", back_populates="fuel_system_control_type"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of FuelSystemControlType instance.  Returns: String representation."""
```

```python
class FuelSystemDesign(Base):
    """FuelSystemDesign entity representing fuel system design types.

Attributes: id: Primary key. fuel_system_design_id: VCdb specific ID. name: Fuel system design name. fuel_delivery_configs: Relationship to fuel delivery configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_fuel_system_design'
fuel_delivery_configs =     fuel_delivery_configs = relationship(
        "FuelDeliveryConfig", back_populates="fuel_system_design"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of FuelSystemDesign instance.  Returns: String representation."""
```

```python
class FuelType(Base):
    """FuelType entity representing fuel types.

Attributes: id: Primary key. fuel_type_id: VCdb specific ID. name: Fuel type name. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_fuel_type'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="fuel_type")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of FuelType instance.  Returns: String representation."""
```

```python
class IgnitionSystemType(Base):
    """IgnitionSystemType entity representing ignition system types.

Attributes: id: Primary key. ignition_system_type_id: VCdb specific ID. name: Ignition system type name. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_ignition_system_type'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="ignition_system_type")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of IgnitionSystemType instance.  Returns: String representation."""
```

```python
class Make(Base):
    """Make entity representing vehicle manufacturers.

Attributes: id: Primary key. make_id: VCdb specific ID. name: Make name. vehicles: Relationship to vehicles. base_vehicles: Relationship to base vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_make'
vehicles =     vehicles = relationship("Vehicle", back_populates="make")
base_vehicles =     base_vehicles = relationship("BaseVehicle", back_populates="make")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Make instance.  Returns: String representation."""
```

```python
class Mfr(Base):
    """Mfr entity representing manufacturers.

Attributes: id: Primary key. mfr_id: VCdb specific ID. name: Manufacturer name. engine_configs: Relationship to engine configs (as engine manufacturer). transmission_configs: Relationship to transmission configs (as transmission manufacturer)."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_mfr'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="engine_mfr")
transmission_configs =     transmission_configs = relationship(
        "Transmission", back_populates="transmission_mfr"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Mfr instance.  Returns: String representation."""
```

```python
class MfrBodyCode(Base):
    """MfrBodyCode entity representing manufacturer body codes.

Attributes: id: Primary key. mfr_body_code_id: VCdb specific ID. code: Body code value. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_mfr_body_code'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of MfrBodyCode instance.  Returns: String representation."""
```

```python
class Model(Base):
    """Model entity representing vehicle models.

Attributes: id: Primary key. model_id: VCdb specific ID. name: Model name. vehicle_type_id: Reference to vehicle type. base_vehicles: Relationship to base vehicles. vehicle_type: Relationship to vehicle type."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_model'
base_vehicles =     base_vehicles = relationship("BaseVehicle", back_populates="model")
vehicle_type =     vehicle_type = relationship("VehicleType", back_populates="models")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Model instance.  Returns: String representation."""
```

```python
class PowerOutput(Base):
    """PowerOutput entity representing engine power output measurements.

Attributes: id: Primary key. power_output_id: VCdb specific ID. horsepower: Horsepower value. kilowatt: Kilowatt value. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_power_output'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="power_output")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of PowerOutput instance.  Returns: String representation."""
```

```python
class PublicationStage(Base):
    """PublicationStage entity representing publication stages for vehicle data.

Attributes: id: Primary key. publication_stage_id: VCdb specific ID. name: Publication stage name. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_publication_stage'
vehicles =     vehicles = relationship("Vehicle", back_populates="publication_stage")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of PublicationStage instance.  Returns: String representation."""
```

```python
class Region(Base):
    """Region entity representing geographic regions.

Attributes: id: Primary key. region_id: VCdb specific ID. parent_id: Optional reference to parent region. abbr: Region abbreviation. name: Region name. children: Relationship to child regions. parent: Relationship to parent region. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_region'
children =     children = relationship("Region", back_populates="parent", remote_side=[region_id])
parent =     parent = relationship("Region", back_populates="children", remote_side=[id])
vehicles =     vehicles = relationship("Vehicle", back_populates="region")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Region instance.  Returns: String representation."""
```

```python
class SpringType(Base):
    """SpringType entity representing spring types.

Attributes: id: Primary key. spring_type_id: VCdb specific ID. name: Spring type name. front_spring_configs: Relationship to spring configs (as front). rear_spring_configs: Relationship to spring configs (as rear)."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_spring_type'
front_spring_configs =     front_spring_configs = relationship(
        "SpringTypeConfig",
        foreign_keys="[SpringTypeConfig.front_spring_type_id]",
        back_populates="front_spring_type",
    )
rear_spring_configs =     rear_spring_configs = relationship(
        "SpringTypeConfig",
        foreign_keys="[SpringTypeConfig.rear_spring_type_id]",
        back_populates="rear_spring_type",
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of SpringType instance.  Returns: String representation."""
```

```python
class SpringTypeConfig(Base):
    """SpringTypeConfig entity representing spring type configurations.

Attributes: id: Primary key. spring_type_config_id: VCdb specific ID. front_spring_type_id: Reference to front spring type. rear_spring_type_id: Reference to rear spring type. front_spring_type: Relationship to front spring type. rear_spring_type: Relationship to rear spring type. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_spring_type_config'
front_spring_type =     front_spring_type = relationship(
        "SpringType",
        foreign_keys=[front_spring_type_id],
        back_populates="front_spring_configs",
    )
rear_spring_type =     rear_spring_type = relationship(
        "SpringType",
        foreign_keys=[rear_spring_type_id],
        back_populates="rear_spring_configs",
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of SpringTypeConfig instance.  Returns: String representation."""
```

```python
class SteeringConfig(Base):
    """SteeringConfig entity representing steering configurations.

Attributes: id: Primary key. steering_config_id: VCdb specific ID. steering_type_id: Reference to steering type. steering_system_id: Reference to steering system. steering_type: Relationship to steering type. steering_system: Relationship to steering system. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_steering_config'
steering_type =     steering_type = relationship("SteeringType", back_populates="steering_configs")
steering_system =     steering_system = relationship("SteeringSystem", back_populates="steering_configs")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of SteeringConfig instance.  Returns: String representation."""
```

```python
class SteeringSystem(Base):
    """SteeringSystem entity representing steering systems.

Attributes: id: Primary key. steering_system_id: VCdb specific ID. name: Steering system name. steering_configs: Relationship to steering configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_steering_system'
steering_configs =     steering_configs = relationship("SteeringConfig", back_populates="steering_system")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of SteeringSystem instance.  Returns: String representation."""
```

```python
class SteeringType(Base):
    """SteeringType entity representing steering types.

Attributes: id: Primary key. steering_type_id: VCdb specific ID. name: Steering type name. steering_configs: Relationship to steering configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_steering_type'
steering_configs =     steering_configs = relationship("SteeringConfig", back_populates="steering_type")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of SteeringType instance.  Returns: String representation."""
```

```python
class SubModel(Base):
    """SubModel entity representing vehicle submodels.

Attributes: id: Primary key. submodel_id: VCdb specific ID. name: Submodel name. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_submodel'
vehicles =     vehicles = relationship("Vehicle", back_populates="submodel")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of SubModel instance.  Returns: String representation."""
```

```python
class Transmission(Base):
    """Transmission entity representing complete transmission configurations.

Attributes: id: Primary key. transmission_id: VCdb specific ID. transmission_base_id: Reference to transmission base. transmission_mfr_code_id: Reference to transmission manufacturer code. elec_controlled_id: Reference to electronic controlled status. transmission_mfr_id: Reference to transmission manufacturer. transmission_base: Relationship to transmission base. transmission_mfr_code: Relationship to transmission manufacturer code. elec_controlled: Relationship to electronic controlled status. transmission_mfr: Relationship to transmission manufacturer. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_transmission'
transmission_base =     transmission_base = relationship("TransmissionBase", back_populates="transmissions")
transmission_mfr_code =     transmission_mfr_code = relationship(
        "TransmissionMfrCode", back_populates="transmissions"
    )
elec_controlled =     elec_controlled = relationship("ElecControlled", back_populates="transmissions")
transmission_mfr =     transmission_mfr = relationship("Mfr", back_populates="transmission_configs")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Transmission instance.  Returns: String representation."""
```

```python
class TransmissionBase(Base):
    """TransmissionBase entity representing base transmission specifications.

Attributes: id: Primary key. transmission_base_id: VCdb specific ID. transmission_type_id: Reference to transmission type. transmission_num_speeds_id: Reference to transmission number of speeds. transmission_control_type_id: Reference to transmission control type. transmission_type: Relationship to transmission type. transmission_num_speeds: Relationship to transmission number of speeds. transmission_control_type: Relationship to transmission control type. transmissions: Relationship to transmissions."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_transmission_base'
transmission_type =     transmission_type = relationship(
        "TransmissionType", back_populates="transmission_bases"
    )
transmission_num_speeds =     transmission_num_speeds = relationship(
        "TransmissionNumSpeeds", back_populates="transmission_bases"
    )
transmission_control_type =     transmission_control_type = relationship(
        "TransmissionControlType", back_populates="transmission_bases"
    )
transmissions =     transmissions = relationship("Transmission", back_populates="transmission_base")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of TransmissionBase instance.  Returns: String representation."""
```

```python
class TransmissionControlType(Base):
    """TransmissionControlType entity representing transmission control types.

Attributes: id: Primary key. transmission_control_type_id: VCdb specific ID. name: Transmission control type name. transmission_bases: Relationship to transmission bases."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_transmission_control_type'
transmission_bases =     transmission_bases = relationship(
        "TransmissionBase", back_populates="transmission_control_type"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of TransmissionControlType instance.  Returns: String representation."""
```

```python
class TransmissionMfrCode(Base):
    """TransmissionMfrCode entity representing transmission manufacturer codes.

Attributes: id: Primary key. transmission_mfr_code_id: VCdb specific ID. code: Manufacturer code value. transmissions: Relationship to transmissions."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_transmission_mfr_code'
transmissions =     transmissions = relationship("Transmission", back_populates="transmission_mfr_code")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of TransmissionMfrCode instance.  Returns: String representation."""
```

```python
class TransmissionNumSpeeds(Base):
    """TransmissionNumSpeeds entity representing number of transmission speeds.

Attributes: id: Primary key. transmission_num_speeds_id: VCdb specific ID. num_speeds: Number of speeds value. transmission_bases: Relationship to transmission bases."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_transmission_num_speeds'
transmission_bases =     transmission_bases = relationship(
        "TransmissionBase", back_populates="transmission_num_speeds"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of TransmissionNumSpeeds instance.  Returns: String representation."""
```

```python
class TransmissionType(Base):
    """TransmissionType entity representing transmission types.

Attributes: id: Primary key. transmission_type_id: VCdb specific ID. name: Transmission type name. transmission_bases: Relationship to transmission bases."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_transmission_type'
transmission_bases =     transmission_bases = relationship(
        "TransmissionBase", back_populates="transmission_type"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of TransmissionType instance.  Returns: String representation."""
```

```python
class VCdbVersion(Base):
    """VCdbVersion entity representing VCdb version information.

Attributes: id: Primary key. version_date: Date of the version. is_current: Whether this is the current version."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_vcdb_version'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of VCdbVersion instance.  Returns: String representation."""
```

```python
class Valves(Base):
    """Valves entity representing number of engine valves.

Attributes: id: Primary key. valves_id: VCdb specific ID. valves_per_engine: Number of valves per engine. engine_configs: Relationship to engine configs."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_valves'
engine_configs =     engine_configs = relationship("EngineConfig", back_populates="valves")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Valves instance.  Returns: String representation."""
```

```python
class Vehicle(Base):
    """Vehicle entity representing specific vehicle configurations.

Attributes: id: Primary key. vehicle_id: VCdb specific ID. base_vehicle_id: Reference to base vehicle. submodel_id: Reference to submodel. region_id: Reference to region. source: Data source information. publication_stage_id: Reference to publication stage. publication_stage_source: Source of publication stage. publication_stage_date: Date of publication stage. base_vehicle: Relationship to base vehicle. submodel: Relationship to submodel. region: Relationship to region. publication_stage: Relationship to publication stage. make: Relationship to make (through base_vehicle). year: Year value (through base_vehicle.year). model: Model name (through base_vehicle.model)."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_vehicle'
base_vehicle =     base_vehicle = relationship("BaseVehicle", back_populates="vehicles")
submodel =     submodel = relationship("SubModel", back_populates="vehicles")
region =     region = relationship("Region", back_populates="vehicles")
publication_stage =     publication_stage = relationship("PublicationStage", back_populates="vehicles")
drive_types =     drive_types = relationship("DriveType", secondary="autocare_vehicle_to_drive_type")
brake_configs =     brake_configs = relationship(
        "BrakeConfig", secondary="autocare_vehicle_to_brake_config"
    )
bed_configs =     bed_configs = relationship("BedConfig", secondary="autocare_vehicle_to_bed_config")
body_style_configs =     body_style_configs = relationship(
        "BodyStyleConfig", secondary="autocare_vehicle_to_body_style_config"
    )
mfr_body_codes =     mfr_body_codes = relationship(
        "MfrBodyCode", secondary="autocare_vehicle_to_mfr_body_code"
    )
engine_configs =     engine_configs = relationship(
        "EngineConfig", secondary="autocare_vehicle_to_engine_config"
    )
spring_type_configs =     spring_type_configs = relationship(
        "SpringTypeConfig", secondary="autocare_vehicle_to_spring_type_config"
    )
steering_configs =     steering_configs = relationship(
        "SteeringConfig", secondary="autocare_vehicle_to_steering_config"
    )
transmissions =     transmissions = relationship(
        "Transmission", secondary="autocare_vehicle_to_transmission"
    )
wheel_bases =     wheel_bases = relationship("WheelBase", secondary="autocare_vehicle_to_wheel_base")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Vehicle instance.  Returns: String representation."""
```
```python
@property
    def make(self) -> Make:
        """Get the make of this vehicle.  Returns: Make object."""
```
```python
@property
    def model(self) -> str:
        """Get the model of this vehicle.  Returns: Model name."""
```
```python
@property
    def year(self) -> int:
        """Get the year of this vehicle.  Returns: Year value."""
```

```python
class VehicleType(Base):
    """VehicleType entity representing types of vehicles.

Attributes: id: Primary key. vehicle_type_id: VCdb specific ID. name: Vehicle type name. vehicle_type_group_id: Optional reference to vehicle type group. models: Relationship to models. vehicle_type_group: Relationship to vehicle type group."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_vehicle_type'
models =     models = relationship("Model", back_populates="vehicle_type")
vehicle_type_group =     vehicle_type_group = relationship(
        "VehicleTypeGroup", back_populates="vehicle_types"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of VehicleType instance.  Returns: String representation."""
```

```python
class VehicleTypeGroup(Base):
    """VehicleTypeGroup entity representing groups of vehicle types.

Attributes: id: Primary key. vehicle_type_group_id: VCdb specific ID. name: Vehicle type group name. vehicle_types: Relationship to vehicle types."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_vehicle_type_group'
vehicle_types =     vehicle_types = relationship("VehicleType", back_populates="vehicle_type_group")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of VehicleTypeGroup instance.  Returns: String representation."""
```

```python
class WheelBase(Base):
    """WheelBase entity representing wheelbase measurements.

Attributes: id: Primary key. wheel_base_id: VCdb specific ID. wheel_base: Wheelbase measurement in imperial units. wheel_base_metric: Wheelbase measurement in metric units. vehicles: Relationship to vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_wheel_base'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of WheelBase instance.  Returns: String representation."""
```

```python
class Year(Base):
    """Year entity representing vehicle model years.

Attributes: id: Primary key. year_id: VCdb specific ID. year: The actual year value. base_vehicles: Relationship to base vehicles."""
```
*Class attributes:*
```python
__tablename__ = 'autocare_year'
base_vehicles =     base_vehicles = relationship("BaseVehicle", back_populates="year")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Year instance.  Returns: String representation."""
```

####### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/vcdb/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.vcdb.models import Vehicle, BaseVehicle, Make, Model, Year, SubModel, VehicleType, Region, VCdbVersion, DriveType, BrakeType, BrakeSystem, BrakeABS, BrakeConfig, BodyType, BodyNumDoors, BodyStyleConfig, EngineBlock, EngineBoreStroke, EngineBase, Aspiration, FuelType, CylinderHeadType, FuelDeliveryType, FuelDeliverySubType, FuelSystemControlType, FuelSystemDesign, FuelDeliveryConfig, EngineDesignation, EngineVIN, EngineVersion, Valves, Mfr, IgnitionSystemType, PowerOutput, EngineConfig, TransmissionType, TransmissionNumSpeeds, TransmissionControlType, TransmissionBase, TransmissionMfrCode, ElecControlled, Transmission, WheelBase
```

**Classes:**
```python
class BaseVehicleRepository(BaseRepository[(BaseVehicle, uuid.UUID)]):
    """Repository for BaseVehicle entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the base vehicle repository.  Args: db: The database session."""
```
```python
    async def find_by_year_make_model(self, year_id, make_id, model_id) -> Optional[BaseVehicle]:
        """Find a base vehicle by year, make, and model IDs.

Args: year_id: Year ID. make_id: Make ID. model_id: Model ID.

Returns: The base vehicle if found, None otherwise."""
```
```python
    async def get_by_base_vehicle_id(self, base_vehicle_id) -> Optional[BaseVehicle]:
        """Get a base vehicle by its VCdb ID.

Args: base_vehicle_id: The base vehicle ID.

Returns: The base vehicle if found, None otherwise."""
```
```python
    async def search_by_criteria(self, year, make, model, page, page_size) -> Dict[(str, Any)]:
        """Search for base vehicles by various criteria.

Args: year: Optional year to filter by. make: Optional make name to filter by. model: Optional model name to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

```python
class BodyStyleConfigRepository(BaseRepository[(BodyStyleConfig, uuid.UUID)]):
    """Repository for BodyStyleConfig entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the body style config repository.  Args: db: The database session."""
```
```python
    async def get_by_body_style_config_id(self, body_style_config_id) -> Optional[BodyStyleConfig]:
        """Get a body style config by its VCdb ID.

Args: body_style_config_id: The body style config ID.

Returns: The body style config if found, None otherwise."""
```
```python
    async def get_by_body_type(self, body_type_id) -> List[BodyStyleConfig]:
        """Get body style configs by body type.

Args: body_type_id: The body type ID.

Returns: List of body style configs with the specified body type."""
```
```python
    async def get_full_body_style_details(self, body_style_config_id) -> Dict[(str, Any)]:
        """Get full details for a body style configuration.

Args: body_style_config_id: The body style config ID.

Returns: Dict with detailed body style information."""
```

```python
class BrakeConfigRepository(BaseRepository[(BrakeConfig, uuid.UUID)]):
    """Repository for BrakeConfig entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the brake config repository.  Args: db: The database session."""
```
```python
    async def get_by_brake_config_id(self, brake_config_id) -> Optional[BrakeConfig]:
        """Get a brake config by its VCdb ID.

Args: brake_config_id: The brake config ID.

Returns: The brake config if found, None otherwise."""
```
```python
    async def get_full_brake_config_details(self, brake_config_id) -> Dict[(str, Any)]:
        """Get full details for a brake configuration.

Args: brake_config_id: The brake config ID.

Returns: Dict with detailed brake configuration information."""
```

```python
class DriveTypeRepository(BaseRepository[(DriveType, uuid.UUID)]):
    """Repository for DriveType entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the drive type repository.  Args: db: The database session."""
```
```python
    async def get_all_drive_types(self) -> List[DriveType]:
        """Get all drive types.  Returns: List of all drive types."""
```
```python
    async def get_by_drive_type_id(self, drive_type_id) -> Optional[DriveType]:
        """Get a drive type by its VCdb ID.

Args: drive_type_id: The drive type ID.

Returns: The drive type if found, None otherwise."""
```

```python
class EngineConfigRepository(BaseRepository[(EngineConfig, uuid.UUID)]):
    """Repository for EngineConfig entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the engine config repository.  Args: db: The database session."""
```
```python
    async def get_by_criteria(self, engine_base_id, fuel_type_id, aspiration_id, page, page_size) -> Dict[(str, Any)]:
        """Get engine configurations by various criteria.

Args: engine_base_id: Optional engine base ID to filter by. fuel_type_id: Optional fuel type ID to filter by. aspiration_id: Optional aspiration ID to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_engine_config_id(self, engine_config_id) -> Optional[EngineConfig]:
        """Get an engine configuration by its VCdb ID.

Args: engine_config_id: The engine config ID.

Returns: The engine config if found, None otherwise."""
```
```python
    async def get_full_engine_details(self, engine_config_id) -> Dict[(str, Any)]:
        """Get full details for an engine configuration.

Args: engine_config_id: The engine config ID.

Returns: Dict with detailed engine information."""
```

```python
class MakeRepository(BaseRepository[(Make, uuid.UUID)]):
    """Repository for Make entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the make repository.  Args: db: The database session."""
```
```python
    async def get_all_makes(self) -> List[Make]:
        """Get all makes.  Returns: List of all makes."""
```
```python
    async def get_by_make_id(self, make_id) -> Optional[Make]:
        """Get a make by its VCdb ID.

Args: make_id: The make ID.

Returns: The make if found, None otherwise."""
```
```python
    async def get_by_year(self, year) -> List[Make]:
        """Get all makes available for a specific year.

Args: year: Vehicle year.

Returns: List of makes available for the year."""
```
```python
    async def search_by_name(self, name) -> List[Make]:
        """Search makes by name.

Args: name: The make name to search for.

Returns: List of makes matching the search."""
```

```python
class ModelRepository(BaseRepository[(Model, uuid.UUID)]):
    """Repository for Model entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the model repository.  Args: db: The database session."""
```
```python
    async def get_by_model_id(self, model_id) -> Optional[Model]:
        """Get a model by its VCdb ID.

Args: model_id: The model ID.

Returns: The model if found, None otherwise."""
```
```python
    async def get_by_vehicle_type(self, vehicle_type_id) -> List[Model]:
        """Get models for a specific vehicle type.

Args: vehicle_type_id: Vehicle type ID.

Returns: List of models for the vehicle type."""
```
```python
    async def get_by_year_make(self, year, make_id) -> List[Model]:
        """Get all models available for a specific year and make.

Args: year: Vehicle year. make_id: Make ID.

Returns: List of models available for the year and make."""
```
```python
    async def search_by_name(self, name) -> List[Model]:
        """Search models by name.

Args: name: The model name to search for.

Returns: List of models matching the search."""
```

```python
class RegionRepository(BaseRepository[(Region, uuid.UUID)]):
    """Repository for Region entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the region repository.  Args: db: The database session."""
```
```python
    async def get_all_top_level_regions(self) -> List[Region]:
        """Get all top-level regions (no parent).  Returns: List of all top-level regions."""
```
```python
    async def get_by_parent(self, parent_id) -> List[Region]:
        """Get regions by parent.

Args: parent_id: The parent region ID.

Returns: List of regions with the specified parent."""
```
```python
    async def get_by_region_id(self, region_id) -> Optional[Region]:
        """Get a region by its VCdb ID.

Args: region_id: The region ID.

Returns: The region if found, None otherwise."""
```

```python
class SubModelRepository(BaseRepository[(SubModel, uuid.UUID)]):
    """Repository for SubModel entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the submodel repository.  Args: db: The database session."""
```
```python
    async def get_all_submodels(self) -> List[SubModel]:
        """Get all submodels.  Returns: List of all submodels."""
```
```python
    async def get_by_submodel_id(self, submodel_id) -> Optional[SubModel]:
        """Get a submodel by its VCdb ID.

Args: submodel_id: The submodel ID.

Returns: The submodel if found, None otherwise."""
```
```python
    async def search_by_name(self, name) -> List[SubModel]:
        """Search submodels by name.

Args: name: The submodel name to search for.

Returns: List of submodels matching the search."""
```

```python
class TransmissionRepository(BaseRepository[(Transmission, uuid.UUID)]):
    """Repository for Transmission entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the transmission repository.  Args: db: The database session."""
```
```python
    async def get_by_criteria(self, transmission_type_id, transmission_num_speeds_id, transmission_control_type_id, page, page_size) -> Dict[(str, Any)]:
        """Get transmissions by various criteria.

Args: transmission_type_id: Optional transmission type ID to filter by. transmission_num_speeds_id: Optional number of speeds ID to filter by. transmission_control_type_id: Optional control type ID to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_transmission_id(self, transmission_id) -> Optional[Transmission]:
        """Get a transmission by its VCdb ID.

Args: transmission_id: The transmission ID.

Returns: The transmission if found, None otherwise."""
```
```python
    async def get_full_transmission_details(self, transmission_id) -> Dict[(str, Any)]:
        """Get full details for a transmission.

Args: transmission_id: The transmission ID.

Returns: Dict with detailed transmission information."""
```

```python
class VCdbRepository(object):
    """Repository for VCdb entity operations.

Provides methods for querying VCdb data and managing database updates."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the VCdb repository.  Args: db: The database session."""
```
```python
    async def get_version(self) -> Optional[str]:
        """Get the current version of the VCdb database.

Returns: The version date as a string or None if no version is set."""
```
```python
    async def update_version(self, version_date) -> VCdbVersion:
        """Update the current version of the VCdb database.

Args: version_date: The new version date.

Returns: The updated version entity."""
```

```python
class VehicleRepository(BaseRepository[(Vehicle, uuid.UUID)]):
    """Repository for Vehicle entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the vehicle repository.  Args: db: The database session."""
```
```python
    async def get_by_vehicle_id(self, vehicle_id) -> Optional[Vehicle]:
        """Get a vehicle by its VCdb ID.

Args: vehicle_id: The vehicle ID.

Returns: The vehicle if found, None otherwise."""
```
```python
    async def get_submodels_by_base_vehicle(self, base_vehicle_id) -> List[SubModel]:
        """Get submodels available for a specific base vehicle.

Args: base_vehicle_id: Base vehicle ID.

Returns: List of submodels for the base vehicle."""
```
```python
    async def get_vehicle_configurations(self, vehicle_id) -> Dict[(str, List[Any])]:
        """Get all configurations for a specific vehicle.

Args: vehicle_id: Vehicle ID.

Returns: Dict containing lists of configurations by type."""
```
```python
    async def search(self, year, make, model, submodel, body_type, engine_config, transmission_type, page, page_size) -> Dict[(str, Any)]:
        """Search for vehicles with optional filters.

Args: year: Optional vehicle year to filter by. make: Optional make name to filter by. model: Optional model name to filter by. submodel: Optional submodel name to filter by. body_type: Optional body type name to filter by. engine_config: Optional engine configuration ID to filter by. transmission_type: Optional transmission type ID to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

```python
class VehicleTypeRepository(BaseRepository[(VehicleType, uuid.UUID)]):
    """Repository for VehicleType entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the vehicle type repository.  Args: db: The database session."""
```
```python
    async def get_all_vehicle_types(self) -> List[VehicleType]:
        """Get all vehicle types.  Returns: List of all vehicle types."""
```
```python
    async def get_by_group(self, vehicle_type_group_id) -> List[VehicleType]:
        """Get vehicle types by group.

Args: vehicle_type_group_id: The vehicle type group ID.

Returns: List of vehicle types in the group."""
```
```python
    async def get_by_vehicle_type_id(self, vehicle_type_id) -> Optional[VehicleType]:
        """Get a vehicle type by its VCdb ID.

Args: vehicle_type_id: The vehicle type ID.

Returns: The vehicle type if found, None otherwise."""
```

```python
class WheelBaseRepository(BaseRepository[(WheelBase, uuid.UUID)]):
    """Repository for WheelBase entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the wheel base repository.  Args: db: The database session."""
```
```python
    async def get_all_wheel_bases(self) -> List[WheelBase]:
        """Get all wheel bases.  Returns: List of all wheel bases."""
```
```python
    async def get_by_wheel_base_id(self, wheel_base_id) -> Optional[WheelBase]:
        """Get a wheel base by its VCdb ID.

Args: wheel_base_id: The wheel base ID.

Returns: The wheel base if found, None otherwise."""
```

```python
class YearRepository(BaseRepository[(Year, uuid.UUID)]):
    """Repository for Year entity operations."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the year repository.  Args: db: The database session."""
```
```python
    async def get_all_years(self) -> List[Year]:
        """Get all available years.  Returns: List of all year entities."""
```
```python
    async def get_by_year(self, year) -> Optional[Year]:
        """Get a year entity by the year value.

Args: year: The year value.

Returns: The year entity if found, None otherwise."""
```
```python
    async def get_by_year_id(self, year_id) -> Optional[Year]:
        """Get a year by its VCdb ID.

Args: year_id: The year ID.

Returns: The year if found, None otherwise."""
```
```python
    async def get_year_range(self) -> Tuple[(int, int)]:
        """Get the minimum and maximum years in the database.  Returns: Tuple containing (min_year, max_year)."""
```

####### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/vcdb/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
```

**Classes:**
```python
class Aspiration(BaseModel):
    """Schema for aspiration data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BaseVehicle(BaseModel):
    """Schema for base vehicle data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BedConfig(BaseModel):
    """Schema for bed configuration data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BedLength(BaseModel):
    """Schema for bed length data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BedType(BaseModel):
    """Schema for bed type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BodyNumDoors(BaseModel):
    """Schema for body number of doors data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BodyStyleConfig(BaseModel):
    """Schema for body style configuration data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BodyType(BaseModel):
    """Schema for body type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BrakeABS(BaseModel):
    """Schema for brake ABS data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BrakeConfig(BaseModel):
    """Schema for brake configuration data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BrakeSystem(BaseModel):
    """Schema for brake system data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BrakeType(BaseModel):
    """Schema for brake type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class CylinderHeadType(BaseModel):
    """Schema for cylinder head type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class DriveType(BaseModel):
    """Schema for drive type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ElecControlled(BaseModel):
    """Schema for electrically controlled data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class EngineBase(BaseModel):
    """Schema for engine base data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class EngineBlock(BaseModel):
    """Schema for engine block data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class EngineBoreStroke(BaseModel):
    """Schema for engine bore and stroke data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class EngineConfig(BaseModel):
    """Schema for engine configuration data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class EngineDesignation(BaseModel):
    """Schema for engine designation data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class EngineVIN(BaseModel):
    """Schema for engine VIN data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class EngineVersion(BaseModel):
    """Schema for engine version data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FuelDeliveryConfig(BaseModel):
    """Schema for fuel delivery configuration data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FuelDeliverySubType(BaseModel):
    """Schema for fuel delivery subtype data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FuelDeliveryType(BaseModel):
    """Schema for fuel delivery type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FuelSystemControlType(BaseModel):
    """Schema for fuel system control type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FuelSystemDesign(BaseModel):
    """Schema for fuel system design data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FuelType(BaseModel):
    """Schema for fuel type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class IgnitionSystemType(BaseModel):
    """Schema for ignition system type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Make(BaseModel):
    """Schema for vehicle make data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Mfr(BaseModel):
    """Schema for manufacturer data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class MfrBodyCode(BaseModel):
    """Schema for manufacturer body code data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Model(BaseModel):
    """Schema for vehicle model data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class PowerOutput(BaseModel):
    """Schema for power output data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class PublicationStage(BaseModel):
    """Schema for publication stage data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Region(BaseModel):
    """Schema for region data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class SpringType(BaseModel):
    """Schema for spring type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class SpringTypeConfig(BaseModel):
    """Schema for spring type configuration data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class SteeringConfig(BaseModel):
    """Schema for steering configuration data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class SteeringSystem(BaseModel):
    """Schema for steering system data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class SteeringType(BaseModel):
    """Schema for steering type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class SubModel(BaseModel):
    """Schema for vehicle submodel data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Transmission(BaseModel):
    """Schema for transmission data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class TransmissionBase(BaseModel):
    """Schema for transmission base data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class TransmissionControlType(BaseModel):
    """Schema for transmission control type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class TransmissionMfrCode(BaseModel):
    """Schema for transmission manufacturer code data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class TransmissionNumSpeeds(BaseModel):
    """Schema for transmission number of speeds data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class TransmissionType(BaseModel):
    """Schema for transmission type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Valves(BaseModel):
    """Schema for valves data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Vehicle(BaseModel):
    """Schema for complete vehicle data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class VehicleDetail(Vehicle):
    """Schema for detailed vehicle data with configurations."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class VehicleSearchParameters(BaseModel):
    """Schema for vehicle search parameters."""
```

```python
class VehicleSearchResponse(BaseModel):
    """Schema for paginated vehicle search response."""
```

```python
class VehicleType(BaseModel):
    """Schema for vehicle type data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class VehicleTypeGroup(BaseModel):
    """Schema for vehicle type group data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class WheelBase(BaseModel):
    """Schema for wheel base data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Year(BaseModel):
    """Schema for vehicle year data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

####### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/autocare/vcdb/service.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import VCdbException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.vcdb.repository import VCdbRepository
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.autocare.vcdb.service")
```

**Classes:**
```python
class VCdbService(object):
    """Service for interacting with VCdb (Vehicle Component Database) data.

This service provides methods for querying, importing, and managing vehicle data and their components according to Auto Care standards."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the VCdb service.  Args: db: SQLAlchemy async session for database operations"""
```
```python
    async def find_base_vehicle(self, year_id, make_id, model_id) -> Optional[Dict[(str, Any)]]:
        """Find a base vehicle by its component IDs.

Args: year_id: The year ID make_id: The make ID model_id: The model ID

Returns: Dictionary containing base vehicle information or None if not found"""
```
```python
    async def get_all_submodels(self) -> List[Dict[(str, Any)]]:
        """Get all available submodels.  Returns: List of dictionaries containing submodel information"""
```
```python
    async def get_base_vehicle(self, base_vehicle_id) -> Dict[(str, Any)]:
        """Get a specific base vehicle by ID.

Args: base_vehicle_id: The base vehicle ID to retrieve

Returns: Dictionary containing base vehicle information

Raises: ResourceNotFoundException: If base vehicle with the specified ID is not found"""
```
```python
    async def get_body_style_config(self, body_style_config_id) -> Dict[(str, Any)]:
        """Get detailed information about a specific body style configuration.

Args: body_style_config_id: The body style configuration ID to retrieve

Returns: Dictionary containing detailed body style configuration information

Raises: ResourceNotFoundException: If body style configuration is not found"""
```
```python
    async def get_brake_config(self, brake_config_id) -> Dict[(str, Any)]:
        """Get detailed information about a specific brake configuration.

Args: brake_config_id: The brake configuration ID to retrieve

Returns: Dictionary containing detailed brake configuration information

Raises: ResourceNotFoundException: If brake configuration is not found"""
```
```python
    async def get_drive_types(self) -> List[Dict[(str, Any)]]:
        """Get all available drive types.  Returns: List of dictionaries containing drive type information"""
```
```python
    async def get_engine_config(self, engine_config_id) -> Dict[(str, Any)]:
        """Get detailed information about a specific engine configuration.

Args: engine_config_id: The engine configuration ID to retrieve

Returns: Dictionary containing detailed engine configuration information

Raises: ResourceNotFoundException: If engine configuration is not found"""
```
```python
    async def get_make_by_id(self, make_id) -> Dict[(str, Any)]:
        """Get a specific make by ID.

Args: make_id: The make ID to retrieve

Returns: Dictionary containing make information

Raises: ResourceNotFoundException: If make with the specified ID is not found"""
```
```python
    async def get_makes(self) -> List[Dict[(str, Any)]]:
        """Get all available vehicle makes.  Returns: List of dictionaries containing make information"""
```
```python
    async def get_makes_by_year(self, year) -> List[Dict[(str, Any)]]:
        """Get all makes available for a specific year.

Args: year: The vehicle year to filter by

Returns: List of dictionaries containing make information for the specified year"""
```
```python
    async def get_model_by_id(self, model_id) -> Dict[(str, Any)]:
        """Get a specific model by ID.

Args: model_id: The model ID to retrieve

Returns: Dictionary containing model information

Raises: ResourceNotFoundException: If model with the specified ID is not found"""
```
```python
    async def get_models_by_year_make(self, year, make_id) -> List[Dict[(str, Any)]]:
        """Get all models for a specific year and make.

Args: year: The vehicle year make_id: The make ID

Returns: List of dictionaries containing model information"""
```
```python
    async def get_regions(self) -> List[Dict[(str, Any)]]:
        """Get all top-level regions.  Returns: List of dictionaries containing region information"""
```
```python
    async def get_regions_by_parent(self, parent_id) -> List[Dict[(str, Any)]]:
        """Get all subregions for a parent region.

Args: parent_id: The parent region ID

Returns: List of dictionaries containing subregion information"""
```
```python
    async def get_submodels_by_base_vehicle(self, base_vehicle_id) -> List[Dict[(str, Any)]]:
        """Get all submodels for a specific base vehicle.

Args: base_vehicle_id: The base vehicle ID

Returns: List of dictionaries containing submodel information"""
```
```python
    async def get_transmission(self, transmission_id) -> Dict[(str, Any)]:
        """Get detailed information about a specific transmission.

Args: transmission_id: The transmission ID to retrieve

Returns: Dictionary containing detailed transmission information

Raises: ResourceNotFoundException: If transmission is not found"""
```
```python
    async def get_vehicle_by_id(self, vehicle_id) -> Dict[(str, Any)]:
        """Get a specific vehicle by ID.

Args: vehicle_id: The vehicle ID to retrieve

Returns: Dictionary containing basic vehicle information

Raises: ResourceNotFoundException: If vehicle with the specified ID is not found"""
```
```python
    async def get_vehicle_configurations(self, vehicle_id) -> Dict[(str, List[Dict[(str, Any)]])]:
        """Get all component configurations for a specific vehicle.

Args: vehicle_id: The vehicle ID to retrieve configurations for

Returns: Dictionary containing component configurations grouped by type

Raises: ResourceNotFoundException: If vehicle with the specified ID is not found"""
```
```python
    async def get_vehicle_details(self, vehicle_id) -> Dict[(str, Any)]:
        """Get detailed information about a specific vehicle.

Args: vehicle_id: The vehicle ID to retrieve

Returns: Dictionary containing detailed vehicle information including engines, transmissions, drive types, and body styles

Raises: ResourceNotFoundException: If vehicle with the specified ID is not found"""
```
```python
    async def get_vehicle_types(self) -> List[Dict[(str, Any)]]:
        """Get all available vehicle types.  Returns: List of dictionaries containing vehicle type information"""
```
```python
    async def get_vehicle_types_by_group(self, group_id) -> List[Dict[(str, Any)]]:
        """Get all vehicle types within a specific group.

Args: group_id: The vehicle type group ID

Returns: List of dictionaries containing vehicle type information"""
```
```python
    async def get_version(self) -> str:
        """Get the current VCdb database version.

Returns: String representation of the version date or a message indicating no version information is available"""
```
```python
    async def get_wheel_bases(self) -> List[Dict[(str, Any)]]:
        """Get all available wheel bases.  Returns: List of dictionaries containing wheel base information"""
```
```python
    async def get_year_range(self) -> Tuple[(int, int)]:
        """Get the range of available vehicle years.

Returns: Tuple containing the minimum and maximum years in the database"""
```
```python
    async def get_years(self) -> List[Dict[(str, Any)]]:
        """Get all available vehicle years.  Returns: List of dictionaries containing year information"""
```
```python
    async def import_from_aces(self, file_path, params) -> Dict[(str, Any)]:
        """Import vehicle data from an ACES XML file.

Args: file_path: Path to the ACES XML file params: Import parameters for controlling the import process

Returns: Dictionary with status information about the import operation

Raises: VCdbException: If the import operation fails"""
```
```python
    async def search_base_vehicles(self, year, make, model, page, page_size) -> Dict[(str, Any)]:
        """Search for base vehicles by criteria.

Args: year: Optional year to filter by make: Optional make name pattern to filter by model: Optional model name pattern to filter by page: Page number for pagination page_size: Number of items per page

Returns: Dictionary containing search results and pagination information"""
```
```python
    async def search_engine_configs(self, engine_base_id, fuel_type_id, aspiration_id, page, page_size) -> Dict[(str, Any)]:
        """Search for engine configurations by criteria.

Args: engine_base_id: Optional engine base ID to filter by fuel_type_id: Optional fuel type ID to filter by aspiration_id: Optional aspiration ID to filter by page: Page number for pagination page_size: Number of items per page

Returns: Dictionary containing search results and pagination information"""
```
```python
    async def search_makes(self, search_term) -> List[Dict[(str, Any)]]:
        """Search for makes by name.

Args: search_term: The search term to find in make names

Returns: List of dictionaries containing matching make information"""
```
```python
    async def search_models(self, search_term) -> List[Dict[(str, Any)]]:
        """Search for models by name.

Args: search_term: The search term to find in model names

Returns: List of dictionaries containing matching model information"""
```
```python
    async def search_submodels(self, search_term) -> List[Dict[(str, Any)]]:
        """Search for submodels by name.

Args: search_term: The search term to find in submodel names

Returns: List of dictionaries containing matching submodel information"""
```
```python
    async def search_transmissions(self, transmission_type_id, transmission_num_speeds_id, transmission_control_type_id, page, page_size) -> Dict[(str, Any)]:
        """Search for transmissions by criteria.

Args: transmission_type_id: Optional transmission type ID to filter by transmission_num_speeds_id: Optional number of speeds ID to filter by transmission_control_type_id: Optional control type ID to filter by page: Page number for pagination page_size: Number of items per page

Returns: Dictionary containing search results and pagination information"""
```
```python
    async def search_vehicles(self, year, make, model, submodel, body_type, engine_config, transmission_type, page, page_size) -> Dict[(str, Any)]:
        """Search for vehicles by criteria.

Args: year: Optional year to filter by make: Optional make name pattern to filter by model: Optional model name pattern to filter by submodel: Optional submodel name pattern to filter by body_type: Optional body type pattern to filter by engine_config: Optional engine configuration ID to filter by transmission_type: Optional transmission type ID to filter by page: Page number for pagination page_size: Number of items per page

Returns: Dictionary containing search results and pagination information"""
```
```python
    async def update_database(self, file_path) -> Dict[(str, Any)]:
        """Update the VCdb database from a file.

Args: file_path: Path to the file containing VCdb data

Returns: Dictionary with status information about the update operation

Raises: VCdbException: If the update operation fails"""
```

##### Package: chat
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/__init__.py`

###### Module: connection
*WebSocket connection management.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/connection.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import json
from typing import Dict, Optional, Set
from app.domains.chat.schemas import WebSocketCommand
from fastapi import WebSocket
from app.logging import get_logger
from app.utils.redis_manager import get_redis_pool
```

**Global Variables:**
```python
logger = logger = get_logger("app.chat.connection")
manager = manager = ConnectionManager()
redis_manager = redis_manager = RedisConnectionManager(manager)
```

**Classes:**
```python
class ConnectionManager(object):
    """WebSocket connection manager for the chat system.

This class handles: - Active WebSocket connections - Connection groups by room ID - Message broadcasting - Connection authentication"""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the connection manager."""
```
```python
    async def broadcast_to_room(self, message, room_id, exclude) -> None:
        """Broadcast a message to all connections in a room.

Args: message: The message data to send room_id: The room ID to broadcast to exclude: Optional connection ID to exclude from broadcast"""
```
```python
    async def broadcast_to_user(self, message, user_id) -> None:
        """Broadcast a message to all connections for a specific user.

Args: message: The message data to send user_id: The user ID to broadcast to"""
```
```python
    async def connect(self, websocket, connection_id, user_id) -> None:
        """Accept a WebSocket connection and register it.

Args: websocket: The WebSocket connection connection_id: Unique ID for this connection user_id: ID of the authenticated user"""
```
```python
    def disconnect(self, connection_id) -> None:
        """Remove a WebSocket connection.  Args: connection_id: The ID of the connection to remove"""
```
```python
    def get_connection_count(self) -> int:
        """Get the count of active connections.  Returns: int: Number of active connections"""
```
```python
    def get_room_connection_count(self, room_id) -> int:
        """Get the count of connections in a specific room.

Args: room_id: The room ID

Returns: int: Number of connections in the room"""
```
```python
    def get_user_connection_count(self, user_id) -> int:
        """Get the count of connections for a specific user.

Args: user_id: The user ID

Returns: int: Number of connections for the user"""
```
```python
    def join_room(self, connection_id, room_id) -> None:
        """Add a connection to a room group.

Args: connection_id: The connection ID room_id: The room ID to join"""
```
```python
    def leave_room(self, connection_id, room_id) -> None:
        """Remove a connection from a room group.

Args: connection_id: The connection ID room_id: The room ID to leave"""
```
```python
    async def send_personal_message(self, message, connection_id) -> None:
        """Send a message to a specific connection.

Args: message: The message data to send connection_id: The target connection ID"""
```

```python
class RedisConnectionManager(object):
    """Redis-based connection manager for multi-instance scaling.

This class extends the basic connection manager with Redis Pub/Sub to allow broadcasting messages across multiple application instances."""
```
*Methods:*
```python
    def __init__(self, local_manager) -> None:
        """Initialize the Redis connection manager.

Args: local_manager: The local connection manager instance"""
```
```python
    async def broadcast_to_room(self, message, room_id, exclude) -> None:
        """Broadcast a message to all connections in a room across all instances.

Args: message: The message data to send room_id: The room ID to broadcast to exclude: Optional connection ID to exclude from broadcast"""
```
```python
    async def broadcast_to_user(self, message, user_id) -> None:
        """Broadcast a message to all connections for a specific user across all instances.

Args: message: The message data to send user_id: The user ID to broadcast to"""
```
```python
    async def start_pubsub_listener(self) -> None:
        """Start the Redis Pub/Sub listener task."""
```

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/exceptions.py`

###### Module: handlers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/handlers.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, Boolean, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.utils.crypto import encrypt_message, decrypt_message
from app.domains.users.models import User
from app.domains.company.schemas import Company
```

**Classes:**
```python
class ChatMember(Base):
    """Chat member entity representing a user's membership in a chat room.

Attributes: id: Unique identifier. room_id: ID of the chat room. user_id: ID of the user. role: Member's role in the room. last_read_at: When the user last read messages in the room. is_active: Whether the membership is active. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'chat_member'
__table_args__ =     __table_args__ = (Index("idx_unique_room_user", "room_id", "user_id", unique=True),)
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ChatMember instance.

Returns: String representation including id, user ID, room ID, and role."""
```

```python
class ChatMemberRole(str, Enum):
    """Roles of chat room members.

Attributes: OWNER: Room owner with full control. ADMIN: Administrator with elevated permissions. MEMBER: Regular member. GUEST: Guest with limited permissions."""
```
*Class attributes:*
```python
OWNER = 'owner'
ADMIN = 'admin'
MEMBER = 'member'
GUEST = 'guest'
```

```python
class ChatMessage(Base):
    """Chat message entity representing a message in a chat room.

Attributes: id: Unique identifier. room_id: ID of the chat room. sender_id: ID of the user who sent the message. message_type: Type of message. content_encrypted: Encrypted message content. extra_metadata: Additional metadata about the message. is_deleted: Whether the message was deleted. deleted_at: When the message was deleted. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'chat_message'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ChatMessage instance.

Returns: String representation including id, message type, and room ID."""
```
```python
@content.setter
    def content(self, value) -> None:
        """Set the message content, encrypting it.  Args: value: Plain text message content to encrypt."""
```

```python
class ChatRoom(Base):
    """Chat room entity representing a conversation space.

Attributes: id: Unique identifier. name: Optional room name (might be null for direct chats). type: Type of chat room. company_id: ID of the associated company. is_active: Whether the room is active. extra_metadata: Additional metadata about the room. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'chat_room'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ChatRoom instance.

Returns: String representation including id, name, and type."""
```

```python
class ChatRoomType(str, Enum):
    """Types of chat rooms.

Attributes: DIRECT: One-to-one chat between two users. GROUP: Group chat with multiple users. COMPANY: Company-wide chat. SUPPORT: Support chat with customer service."""
```
*Class attributes:*
```python
DIRECT = 'direct'
GROUP = 'group'
COMPANY = 'company'
SUPPORT = 'support'
```

```python
class MessageReaction(Base):
    """Message reaction entity representing a user's reaction to a message.

Attributes: id: Unique identifier. message_id: ID of the message being reacted to. user_id: ID of the user who reacted. reaction: Reaction string (e.g., emoji). created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'message_reaction'
__table_args__ =     __table_args__ = (
        Index(
            "idx_unique_message_user_reaction",
            "message_id",
            "user_id",
            "reaction",
            unique=True,
        ),
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of MessageReaction instance.

Returns: String representation including id, reaction, and user ID."""
```

```python
class MessageType(str, Enum):
    """Types of chat messages.

Attributes: TEXT: Plain text message. IMAGE: Image message. FILE: File attachment message. SYSTEM: System notification message. ACTION: User action message."""
```
*Class attributes:*
```python
TEXT = 'text'
IMAGE = 'image'
FILE = 'file'
SYSTEM = 'system'
ACTION = 'action'
```

```python
class RateLimitLog(Base):
    """Rate limit log entity for tracking API rate limits.

Attributes: id: Unique identifier. user_id: ID of the user being rate limited. room_id: ID of the chat room (if applicable). event_type: Type of event being limited. timestamp: When the event occurred. count: Event count."""
```
*Class attributes:*
```python
__tablename__ = 'rate_limit_log'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of RateLimitLog instance.

Returns: String representation including id, user ID, event type, and count."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.chat.models import ChatRoom, ChatMember, ChatMessage, MessageReaction, RateLimitLog, ChatRoomType, ChatMemberRole, MessageType
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, BusinessException, PermissionDeniedException, RateLimitException
```

**Classes:**
```python
class ChatMemberRepository(BaseRepository[(ChatMember, uuid.UUID)]):
    """Repository for ChatMember entity operations.

Provides methods for querying, creating, updating, and deleting ChatMember entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the chat member repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, member_id) -> ChatMember:
        """Ensure a chat member exists by ID, raising an exception if not found.

Args: member_id: The chat member ID to check.

Returns: The chat member if found.

Raises: ResourceNotFoundException: If the chat member is not found."""
```
```python
    async def find_by_room_and_user(self, room_id, user_id) -> Optional[ChatMember]:
        """Find a chat membership for a specific room and user.

Args: room_id: The chat room ID. user_id: The user ID.

Returns: The chat member if found, None otherwise."""
```
```python
    async def get_by_room(self, room_id, active_only) -> List[ChatMember]:
        """Get all members of a chat room.

Args: room_id: The chat room ID. active_only: Whether to include only active members.

Returns: List of chat members in the room."""
```
```python
    async def get_by_user(self, user_id) -> List[ChatMember]:
        """Get all chat memberships for a user.

Args: user_id: The user ID.

Returns: List of chat memberships for the user."""
```
```python
    async def remove_member(self, room_id, user_id, removed_by_id) -> bool:
        """Remove a member from a chat room.

Args: room_id: The chat room ID. user_id: The user ID to remove. removed_by_id: ID of the user performing the removal.

Returns: True if the member was removed, False otherwise.

Raises: PermissionDeniedException: If the user doesn't have permission."""
```
```python
    async def update_last_read(self, room_id, user_id, timestamp) -> Optional[ChatMember]:
        """Update the last read timestamp for a member.

Args: room_id: The chat room ID. user_id: The user ID. timestamp: Optional custom timestamp (defaults to now).

Returns: The updated member if found, None otherwise."""
```
```python
    async def update_role(self, room_id, user_id, new_role, updated_by_id) -> Optional[ChatMember]:
        """Update the role of a chat member.

Args: room_id: The chat room ID. user_id: The user ID. new_role: The new role to assign. updated_by_id: ID of the user making the change.

Returns: The updated member if found, None otherwise.

Raises: PermissionDeniedException: If the user doesn't have permission."""
```

```python
class ChatMessageRepository(BaseRepository[(ChatMessage, uuid.UUID)]):
    """Repository for ChatMessage entity operations.

Provides methods for querying, creating, updating, and deleting ChatMessage entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the chat message repository.  Args: db: The database session."""
```
```python
    async def check_rate_limit(self, user_id, room_id, event_type, max_count, window_seconds) -> None:
        """Check if a user has exceeded rate limits for an event type.

Args: user_id: The user ID. room_id: The chat room ID. event_type: The event type being limited. max_count: Maximum allowed events in the time window. window_seconds: Time window in seconds.

Raises: RateLimitException: If the rate limit is exceeded."""
```
```python
    async def delete_message(self, message_id, deleted_by_id) -> Optional[ChatMessage]:
        """Delete a message.

Args: message_id: The message ID. deleted_by_id: ID of the user deleting the message.

Returns: The deleted message if found, None otherwise.

Raises: PermissionDeniedException: If the user doesn't have permission."""
```
```python
    async def edit_message(self, message_id, new_content, edited_by_id) -> Optional[ChatMessage]:
        """Edit a message.

Args: message_id: The message ID. new_content: The new message content. edited_by_id: ID of the user making the edit.

Returns: The updated message if found, None otherwise.

Raises: PermissionDeniedException: If the user doesn't have permission."""
```
```python
    async def ensure_exists(self, message_id) -> ChatMessage:
        """Ensure a chat message exists by ID, raising an exception if not found.

Args: message_id: The chat message ID to check.

Returns: The chat message if found.

Raises: ResourceNotFoundException: If the chat message is not found."""
```
```python
    async def get_room_messages(self, room_id, limit, before_id, include_deleted) -> List[ChatMessage]:
        """Get messages for a chat room.

Args: room_id: The chat room ID. limit: Maximum number of messages to return. before_id: Optional message ID to get messages before. include_deleted: Whether to include deleted messages.

Returns: List of chat messages."""
```
```python
    async def send_message(self, room_id, sender_id, content, message_type, extra_metadata) -> ChatMessage:
        """Send a message to a chat room.

Args: room_id: The chat room ID. sender_id: The sender user ID. content: The message content. message_type: The message type. extra_metadata: Optional message metadata.

Returns: The created message.

Raises: ResourceNotFoundException: If the room doesn't exist. PermissionDeniedException: If the user isn't a member of the room."""
```

```python
class ChatRoomRepository(BaseRepository[(ChatRoom, uuid.UUID)]):
    """Repository for ChatRoom entity operations.

Provides methods for querying, creating, updating, and deleting ChatRoom entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the chat room repository.  Args: db: The database session."""
```
```python
    async def add_members(self, room_id, user_ids, role, added_by_id) -> List[ChatMember]:
        """Add members to a chat room.

Args: room_id: ID of the chat room. user_ids: List of user IDs to add. role: Role to assign to the new members. added_by_id: ID of the user adding the members.

Returns: List of created member records.

Raises: ResourceNotFoundException: If the room doesn't exist. PermissionDeniedException: If the user doesn't have permission."""
```
```python
    async def create_direct_chat(self, user1_id, user2_id) -> Tuple[(ChatRoom, List[ChatMember])]:
        """Create a direct chat between two users.

Args: user1_id: First user ID. user2_id: Second user ID.

Returns: Tuple containing (chat room, list of members).

Raises: BusinessException: If a direct chat already exists between the users."""
```
```python
    async def create_group_chat(self, name, creator_id, member_ids, company_id) -> Tuple[(ChatRoom, List[ChatMember])]:
        """Create a group chat.

Args: name: Group chat name. creator_id: ID of the user creating the chat. member_ids: List of member user IDs. company_id: Optional company ID to associate with the chat.

Returns: Tuple containing (chat room, list of members).

Raises: BusinessException: If no members are provided."""
```
```python
    async def ensure_exists(self, room_id) -> ChatRoom:
        """Ensure a chat room exists by ID, raising an exception if not found.

Args: room_id: The chat room ID to check.

Returns: The chat room if found.

Raises: ResourceNotFoundException: If the chat room is not found."""
```
```python
    async def find_direct_chat(self, user1_id, user2_id) -> Optional[ChatRoom]:
        """Find a direct chat between two users.

Args: user1_id: First user ID. user2_id: Second user ID.

Returns: The direct chat room if found, None otherwise."""
```
```python
    async def get_company_rooms(self, company_id, page, page_size) -> Dict[(str, Any)]:
        """Get paginated list of chat rooms for a company.

Args: company_id: The company ID to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_rooms_for_user(self, user_id, room_type, page, page_size) -> Dict[(str, Any)]:
        """Get paginated list of chat rooms for a user.

Args: user_id: The user ID to filter by. room_type: Optional room type to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

```python
class MessageReactionRepository(BaseRepository[(MessageReaction, uuid.UUID)]):
    """Repository for MessageReaction entity operations.

Provides methods for querying, creating, updating, and deleting MessageReaction entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the message reaction repository.  Args: db: The database session."""
```
```python
    async def add_reaction(self, message_id, user_id, reaction) -> MessageReaction:
        """Add a reaction to a message.

Args: message_id: The message ID. user_id: The user ID. reaction: The reaction string.

Returns: The created or existing reaction.

Raises: ResourceNotFoundException: If the message doesn't exist. PermissionDeniedException: If the user isn't a member of the room."""
```
```python
    async def find_by_message_user_reaction(self, message_id, user_id, reaction) -> Optional[MessageReaction]:
        """Find a reaction by message, user, and reaction type.

Args: message_id: The message ID. user_id: The user ID. reaction: The reaction string.

Returns: The reaction if found, None otherwise."""
```
```python
    async def get_by_message(self, message_id) -> List[MessageReaction]:
        """Get all reactions for a message.

Args: message_id: The message ID.

Returns: List of reactions for the message."""
```
```python
    async def get_reaction_counts(self, message_id) -> Dict[(str, int)]:
        """Get counts of each reaction type for a message.

Args: message_id: The message ID.

Returns: Dictionary mapping reaction strings to counts."""
```
```python
    async def get_user_reactions(self, message_id, reaction) -> List[uuid.UUID]:
        """Get user IDs who reacted with a specific reaction to a message.

Args: message_id: The message ID. reaction: The reaction string.

Returns: List of user IDs."""
```
```python
    async def remove_reaction(self, message_id, user_id, reaction) -> bool:
        """Remove a reaction from a message.

Args: message_id: The message ID. user_id: The user ID. reaction: The reaction string.

Returns: True if the reaction was removed, False otherwise."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.chat.models import ChatRoomType, ChatMemberRole, MessageType
```

**Classes:**
```python
class ChatMember(ChatMemberInDB):
    """Schema for complete ChatMember data in API responses.

Includes related entities like user and room details."""
```

```python
class ChatMemberBase(BaseModel):
    """Base schema for ChatMember data.

Attributes: room_id: ID of the chat room. user_id: ID of the user. role: Member's role in the room. is_active: Whether the membership is active."""
```

```python
class ChatMemberCreate(ChatMemberBase):
    """Schema for creating a new ChatMember."""
```

```python
class ChatMemberInDB(ChatMemberBase):
    """Schema for ChatMember data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ChatMemberUpdate(BaseModel):
    """Schema for updating an existing ChatMember.  All fields are optional to allow partial updates."""
```

```python
class ChatMessage(ChatMessageInDB):
    """Schema for complete ChatMessage data in API responses.

Includes additional fields like sender information and reactions."""
```

```python
class ChatMessageBase(BaseModel):
    """Base schema for ChatMessage data.

Attributes: room_id: ID of the chat room. sender_id: ID of the message sender. message_type: Type of message. content: Message content. extra_metadata: Additional metadata about the message."""
```

```python
class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a new ChatMessage."""
```

```python
class ChatMessageInDB(ChatMessageBase):
    """Schema for ChatMessage data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ChatMessageUpdate(BaseModel):
    """Schema for updating an existing ChatMessage.  All fields are optional to allow partial updates."""
```

```python
class ChatRoom(ChatRoomInDB):
    """Schema for complete ChatRoom data in API responses.

Includes additional computed fields and related entities."""
```

```python
class ChatRoomBase(BaseModel):
    """Base schema for ChatRoom data.

Attributes: name: Room name (might be null for direct chats). type: Type of chat room. company_id: ID of the associated company. is_active: Whether the room is active. extra_metadata: Additional metadata about the room."""
```

```python
class ChatRoomCreate(ChatRoomBase):
    """Schema for creating a new ChatRoom."""
```

```python
class ChatRoomInDB(ChatRoomBase):
    """Schema for ChatRoom data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ChatRoomUpdate(BaseModel):
    """Schema for updating an existing ChatRoom.  All fields are optional to allow partial updates."""
```

```python
class CommandType(str, Enum):
    """Types of WebSocket commands.

Attributes: JOIN_ROOM: Join a chat room. LEAVE_ROOM: Leave a chat room. SEND_MESSAGE: Send a message to a room. READ_MESSAGES: Mark messages as read. TYPING_START: Indicate the user started typing. TYPING_STOP: Indicate the user stopped typing. FETCH_HISTORY: Request message history. ADD_REACTION: Add a reaction to a message. REMOVE_REACTION: Remove a reaction from a message. EDIT_MESSAGE: Edit a message. DELETE_MESSAGE: Delete a message."""
```
*Class attributes:*
```python
JOIN_ROOM = 'join_room'
LEAVE_ROOM = 'leave_room'
SEND_MESSAGE = 'send_message'
READ_MESSAGES = 'read_messages'
TYPING_START = 'typing_start'
TYPING_STOP = 'typing_stop'
FETCH_HISTORY = 'fetch_history'
ADD_REACTION = 'add_reaction'
REMOVE_REACTION = 'remove_reaction'
EDIT_MESSAGE = 'edit_message'
DELETE_MESSAGE = 'delete_message'
```

```python
class DeleteMessageCommand(BaseModel):
    """Schema for deleting a message.

Attributes: room_id: ID of the room. message_id: ID of the message to delete."""
```

```python
class EditMessageCommand(BaseModel):
    """Schema for editing a message.

Attributes: room_id: ID of the room. message_id: ID of the message to edit. content: New message content."""
```

```python
class FetchHistoryCommand(BaseModel):
    """Schema for fetching message history.

Attributes: room_id: ID of the room. before_id: ID to fetch messages before. limit: Maximum number of messages to fetch."""
```

```python
class JoinRoomCommand(BaseModel):
    """Schema for joining a chat room.  Attributes: room_id: ID of the room to join."""
```

```python
class LeaveRoomCommand(BaseModel):
    """Schema for leaving a chat room.  Attributes: room_id: ID of the room to leave."""
```

```python
class MessageReaction(MessageReactionInDB):
    """Schema for complete MessageReaction data in API responses.

Includes related entities like user details."""
```

```python
class MessageReactionBase(BaseModel):
    """Base schema for MessageReaction data.

Attributes: message_id: ID of the message. user_id: ID of the user. reaction: Reaction string (e.g., emoji)."""
```

```python
class MessageReactionCreate(MessageReactionBase):
    """Schema for creating a new MessageReaction."""
```

```python
class MessageReactionInDB(MessageReactionBase):
    """Schema for MessageReaction data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ReactionCommand(BaseModel):
    """Schema for message reactions.

Attributes: room_id: ID of the room. message_id: ID of the message. reaction: Reaction string (e.g., emoji)."""
```

```python
class ReadMessagesCommand(BaseModel):
    """Schema for marking messages as read.

Attributes: room_id: ID of the room. last_read_id: ID of the last read message."""
```

```python
class SendMessageCommand(BaseModel):
    """Schema for sending a message.

Attributes: room_id: ID of the room to send to. content: Message content. message_type: Type of message. extra_metadata: Additional message metadata."""
```

```python
class TypingCommand(BaseModel):
    """Schema for typing indicators.  Attributes: room_id: ID of the room."""
```

```python
class UserPresence(BaseModel):
    """Schema for user presence information.

Attributes: user_id: ID of the user. is_online: Whether the user is currently online. last_seen_at: When the user was last seen. status: Optional custom status message."""
```

```python
class WebSocketCommand(BaseModel):
    """Base schema for WebSocket commands.

Attributes: command: Type of command. room_id: ID of the chat room. data: Command-specific data."""
```

```python
class WebSocketResponse(BaseModel):
    """Schema for WebSocket responses.

Attributes: type: Response type. success: Whether the operation was successful. error: Error message if not successful. data: Response data."""
```

###### Module: service
*Module for chat functionality including rooms and messages.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/service.py`

**Imports:**
```python
from __future__ import annotations
import datetime
import uuid
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import and_, desc, func, or_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.core.exceptions import BusinessException, DatabaseException, ErrorCode, ResourceNotFoundException, ValidationException
from app.logging import get_logger
from app.domains.chat.models import ChatMember, ChatMemberRole, ChatMessage, ChatRoom, ChatRoomType, MessageReaction, MessageType
from app.domains.users.models import User
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.chat")
```

**Classes:**
```python
class ChatService(object):
    """Service for managing chat functionality including rooms, messages, and reactions.

This service handles all operations related to chat, including: - Creating and managing chat rooms - Sending and retrieving messages - User permissions within chat rooms - Message reactions - Read status tracking"""
```
*Methods:*
```python
    def __init__(self, db):
        """Initialize the ChatService.  Args: db: Database session for database operations"""
```
```python
    async def add_member(self, room_id, user_id, role) -> bool:
        """Add a member to a chat room.

Args: room_id: ID of the chat room user_id: ID of the user to add role: Role of the user in the room

Returns: True if successful, False otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def add_reaction(self, message_id, user_id, reaction) -> bool:
        """Add a reaction to a message.

Args: message_id: ID of the message user_id: ID of the user adding the reaction reaction: Reaction string/emoji

Returns: True if successful, False otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def check_message_permission(self, message_id, user_id, require_admin) -> bool:
        """Check if a user has permission to modify a message.

Args: message_id: ID of the message user_id: ID of the user require_admin: Whether to require admin privileges

Returns: True if the user has permission, False otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def check_room_access(self, user_id, room_id) -> bool:
        """Check if a user has access to a chat room.

Args: user_id: ID of the user room_id: ID of the room

Returns: True if the user has access, False otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def create_direct_chat(self, user_id1, user_id2) -> str:
        """Create a direct chat room between two users or return existing one.

Args: user_id1: ID of the first user user_id2: ID of the second user

Returns: ID of the created/existing direct chat room

Raises: ValidationException: If the input data is invalid DatabaseException: If a database error occurs BusinessException: If there's a logical error creating the room"""
```
```python
    async def create_message(self, room_id, sender_id, content, message_type, metadata) -> ChatMessage:
        """Create a new message in a chat room.

Args: room_id: ID of the chat room sender_id: ID of the message sender content: Message content message_type: Type of message (default: "text") metadata: Optional metadata for the message

Returns: The created ChatMessage instance

Raises: ValidationException: If the input data is invalid DatabaseException: If a database error occurs BusinessException: If there's a logical error creating the message"""
```
```python
    async def create_room(self, name, room_type, creator_id, company_id, members) -> ChatRoom:
        """Create a new chat room.

Args: name: Optional name for the chat room room_type: Type of chat room (DIRECT, GROUP, COMPANY, SUPPORT) creator_id: User ID of the room creator company_id: Optional company ID for company rooms members: Optional list of initial members for the room

Returns: The newly created ChatRoom instance

Raises: ValidationException: If the input data is invalid DatabaseException: If a database error occurs BusinessException: If there's a logical error creating the room"""
```
```python
    async def delete_message(self, message_id) -> bool:
        """Soft delete a message.

Args: message_id: ID of the message to delete

Returns: True if the operation was successful, False otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def edit_message(self, message_id, content) -> Tuple[(bool, Optional[ChatMessage])]:
        """Edit an existing message.

Args: message_id: ID of the message to edit content: New content for the message

Returns: Tuple of (success status, updated message if successful)

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def find_direct_chat(self, user_id1, user_id2) -> Optional[str]:
        """Find a direct chat room between two users.

Args: user_id1: ID of the first user user_id2: ID of the second user

Returns: Room ID if found, None otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def get_message_history(self, room_id, before_id, limit) -> List[Dict[(str, Any)]]:
        """Get message history for a chat room.

Args: room_id: ID of the chat room before_id: Optional ID of message to get history before limit: Maximum number of messages to return

Returns: List of formatted message dictionaries

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def get_room(self, room_id) -> Optional[ChatRoom]:
        """Get a chat room by ID.

Args: room_id: The ID of the room to retrieve

Returns: The ChatRoom instance if found, None otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def get_room_info(self, room_id) -> Dict[(str, Any)]:
        """Get detailed information about a chat room.

Args: room_id: The ID of the room

Returns: Dictionary with room information and members

Raises: ResourceNotFoundException: If the room doesn't exist DatabaseException: If a database error occurs"""
```
```python
    async def get_room_with_members(self, room_id) -> Optional[ChatRoom]:
        """Get a chat room by ID with its members loaded.

Args: room_id: The ID of the room to retrieve

Returns: The ChatRoom instance with members if found, None otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def get_unread_count(self, room_id, user_id, last_read_at) -> int:
        """Get count of unread messages for a user in a room.

Args: room_id: ID of the chat room user_id: ID of the user last_read_at: Optional timestamp of last read message

Returns: Count of unread messages

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def get_user_rooms(self, user_id) -> List[Dict[(str, Any)]]:
        """Get all chat rooms for a user.

Args: user_id: The ID of the user

Returns: List of chat room data dictionaries with metadata

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def mark_as_read(self, user_id, room_id, last_read_id) -> bool:
        """Mark messages in a room as read up to a specific message.

Args: user_id: ID of the user room_id: ID of the chat room last_read_id: ID of the last read message

Returns: True if successful, False otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
@classmethod
    def register(cls) -> None:
        """Register this service with the service registry."""
```
```python
    async def remove_member(self, room_id, user_id) -> bool:
        """Remove a member from a chat room.

Args: room_id: ID of the chat room user_id: ID of the user to remove

Returns: True if successful, False otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def remove_reaction(self, message_id, user_id, reaction) -> bool:
        """Remove a reaction from a message.

Args: message_id: ID of the message user_id: ID of the user removing the reaction reaction: Reaction string/emoji

Returns: True if successful, False otherwise

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def update_member_role(self, room_id, user_id, role) -> bool:
        """Update a member's role in a chat room.

Args: room_id: ID of the chat room user_id: ID of the user role: New role for the user

Returns: True if successful, False otherwise

Raises: DatabaseException: If a database error occurs"""
```

###### Module: service_DUPLICATEMAYBE
*Chat service for managing chat rooms, messages, and members.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/service_DUPLICATEMAYBE.py`

**Imports:**
```python
from __future__ import annotations
import datetime
import uuid
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import and_, desc, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.core.cache.decorators import cached
from app.core.exceptions import BusinessException, ValidationException, ErrorCode
from app.logging import get_logger
from app.domains.chat.models import ChatMember, ChatMemberRole, ChatMessage, ChatRoom, ChatRoomType, MessageReaction, MessageType
from app.domains.users.models import User
from app.utils.crypto import decrypt_message, encrypt_message
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.chat")
```

**Classes:**
```python
class ChatService(object):
    """Service for managing chat rooms and messages."""
```
*Methods:*
```python
    def __init__(self, db):
        """Initialize the chat service.  Args: db: Database session for database operations."""
```
```python
    async def check_message_permission(self, message_id, user_id, require_admin) -> bool:
        """Check if a user has permission to manage a message.

Args: message_id: The message ID. user_id: The user ID. require_admin: Whether to require admin role.

Returns: True if the user has permission, False otherwise.

Raises: BusinessException: If there's an error checking permission."""
```
```python
    async def check_room_access(self, user_id, room_id) -> bool:
        """Check if a user has access to a chat room.

Args: user_id: The user ID. room_id: The chat room ID.

Returns: True if the user has access, False otherwise.

Raises: BusinessException: If there's an error checking access."""
```
```python
    async def create_message(self, room_id, sender_id, content, message_type, metadata) -> ChatMessage:
        """Create a new chat message.

Args: room_id: The chat room ID. sender_id: The sender user ID. content: Message content. message_type: Type of message. metadata: Additional message metadata.

Returns: The created chat message.

Raises: ValidationException: If the message type is invalid. BusinessException: If there's an error creating the message."""
```
```python
    async def create_room(self, name, room_type, creator_id, company_id, members) -> ChatRoom:
        """Create a new chat room.

Args: name: Room name. room_type: Type of chat room. creator_id: ID of the user creating the room. company_id: ID of the company if this is a company room. members: List of member data to add to the room.

Returns: The newly created chat room.

Raises: ValidationException: If the room type or member data is invalid. BusinessException: If there's an error creating the room."""
```
```python
    async def delete_message(self, message_id) -> bool:
        """Delete a chat message (soft delete).

Args: message_id: The message ID.

Returns: True if successful, False otherwise.

Raises: BusinessException: If there's an error deleting the message."""
```
```python
    async def edit_message(self, message_id, content) -> Tuple[(bool, Optional[ChatMessage])]:
        """Edit a chat message.

Args: message_id: The message ID. content: New message content.

Returns: Tuple of (success, updated_message).

Raises: BusinessException: If there's an error editing the message."""
```
```python
@cached(prefix='chat:messages', ttl=60, backend='redis')
    async def get_message_history(self, room_id, before_id, limit) -> List[Dict[(str, Any)]]:
        """Get chat message history for a room.

Args: room_id: The chat room ID. before_id: Get messages before this message ID. limit: Maximum number of messages to return.

Returns: List of formatted message dictionaries.

Raises: BusinessException: If there's an error retrieving messages."""
```
```python
@cached(prefix='chat:room', ttl=300, backend='redis')
    async def get_room(self, room_id) -> Optional[ChatRoom]:
        """Get a chat room by ID.

Args: room_id: The chat room ID.

Returns: The chat room, or None if not found.

Raises: BusinessException: If there's an error retrieving the room."""
```
```python
    async def get_room_with_members(self, room_id) -> Optional[ChatRoom]:
        """Get a chat room with its members.

Args: room_id: The chat room ID.

Returns: The chat room with members loaded, or None if not found.

Raises: BusinessException: If there's an error retrieving the room."""
```
```python
@classmethod
    def register(cls) -> None:
        """Register this service with the service registry."""
```

###### Module: tasks
*Celery worker for background tasks.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/tasks.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List
from celery import Celery
from app.core.config import settings
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.tasks.chat_tasks")
celery_app = celery_app = Celery(
    "worker",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/2",
)
```

**Functions:**
```python
@celery_app.task(bind=True, name='analyze_chat_activity')
def analyze_chat_activity(self, room_id, time_period) -> Dict[(str, Any)]:
    """Analyze chat activity for a room.

Args: room_id: The room ID time_period: Time period for analysis ("day", "week", "month")

Returns: dict: Analysis results"""
```

```python
@celery_app.task(bind=True, name='moderate_message_content')
def moderate_message_content(self, message_id, content, sender_id, room_id) -> Dict[(str, Any)]:
    """Moderate message content for prohibited content.

Args: message_id: The message ID content: Message content to moderate sender_id: ID of the message sender room_id: The room ID

Returns: dict: Moderation results"""
```

```python
@celery_app.task(bind=True, name='process_message_notifications')
def process_message_notifications(self, message_id, room_id, sender_id, recipients, message_preview) -> Dict[(str, Any)]:
    """Process and send message notifications.

Args: message_id: The message ID room_id: The room ID sender_id: ID of the message sender recipients: List of recipient user IDs message_preview: Preview text for notification

Returns: dict: Task result information"""
```

```python
@celery_app.task(bind=True, name='update_user_presence')
def update_user_presence(self) -> Dict[(str, Any)]:
    """Update user presence status based on activity.

This task runs periodically to update user online status based on their last activity.

Returns: dict: Task result information"""
```

###### Module: websocket
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/chat/websocket.py`

**Imports:**
```python
from __future__ import annotations
import datetime
import json
import uuid
from typing import cast
from app.chat.schemas import ChatMessageSchema, CommandType, MessageType, WebSocketCommand, WebSocketResponse
from app.core.service_registry import get_service
from app.domains.audit.service_service import AuditEventType, AuditLogLevel, AuditService
from app.services.metrics_service import MetricsService
from app.services.validation_service import ValidationService
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user_ws, get_db
from app.core.exceptions import BusinessLogicException, ErrorCode, PermissionDeniedException, ValidationException
from app.logging import get_logger
from app.core.security import sanitize_input, moderate_content
from app.domains.chat.connection import manager, redis_manager
from app.domains.chat.service import ChatService
from app.domains.users.models import User
from app.utils.redis_manager import rate_limit_check
```

**Global Variables:**
```python
logger = logger = get_logger("app.chat.websocket")
router = router = APIRouter()
```

**Functions:**
```python
async def get_audit_service() -> AuditService:
    """Get the audit service instance."""
```

```python
async def get_metrics_service() -> MetricsService:
    """Get the metrics service instance."""
```

```python
async def get_validation_service() -> ValidationService:
    """Get the validation service instance."""
```

```python
async def process_command(command, websocket, connection_id, user, chat_service, audit_service) -> None:
    """Process a WebSocket command.

Args: command: The command to process websocket: The WebSocket connection connection_id: Unique connection identifier user: The authenticated user chat_service: Chat service for chat operations audit_service: Audit service for logging events

Raises: ValidationException: If the command data is invalid PermissionDeniedException: If the user lacks permission ResourceNotFoundException: If a required resource isn't found BusinessLogicException: If there's a logical error processing the command"""
```

```python
@router.websocket('/ws/chat')
async def websocket_endpoint(websocket, db, current_user):
    """WebSocket endpoint for chat functionality.

This endpoint manages the WebSocket connection for chat clients, handling commands for joining/leaving rooms, sending/receiving messages, and more.

Args: websocket: The WebSocket connection db: Database session for database operations current_user: The authenticated user"""
```

##### Package: company
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/company`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/company/__init__.py`

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/company/exceptions.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/company/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.chat.models import ChatRoom
from app.domains.audit.models import AuditLog
from app.domains.location.models import Address
from app.domains.users.models import User
from app.domains.audit.models import AuditLog
from app.domains.products.models import Brand
```

**Classes:**
```python
class Company(Base):
    """Company entity representing a business organization.

Attributes: id: Unique identifier. name: Company name. headquarters_address_id: ID of the headquarters address. billing_address_id: ID of the billing address. shipping_address_id: ID of the shipping address. account_number: Unique account identifier. account_type: Type of account (client, supplier, etc). industry: Industry sector. is_active: Whether the company is active. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'company'
headquarters_address =     headquarters_address = relationship(
        "Address", foreign_keys=[headquarters_address_id]
    )
billing_address =     billing_address = relationship("Address", foreign_keys=[billing_address_id])
shipping_address =     shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Company instance.

Returns: String representation including name and account type."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/company/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.company.schemas import Company
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

**Classes:**
```python
class CompanyRepository(BaseRepository[(Company, uuid.UUID)]):
    """Repository for Company entity operations.

Provides methods for querying, creating, updating, and deleting Company entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the company repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, company_id) -> Company:
        """Ensure a company exists by ID, raising an exception if not found.

Args: company_id: The company ID to check.

Returns: The company if found.

Raises: ResourceNotFoundException: If the company is not found."""
```
```python
    async def find_by_account_number(self, account_number) -> Optional[Company]:
        """Find a company by its account number.

Args: account_number: The account number to search for.

Returns: The company if found, None otherwise."""
```
```python
    async def find_by_industry(self, industry) -> List[Company]:
        """Find companies by industry.

Args: industry: The industry to filter by.

Returns: List of companies in the specified industry."""
```
```python
    async def find_by_name(self, name) -> Optional[Company]:
        """Find a company by its name.

Args: name: The company name to search for.

Returns: The company if found, None otherwise."""
```
```python
    async def get_active_companies(self, page, page_size) -> Dict[(str, Any)]:
        """Get paginated list of active companies.

Args: page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/company/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.location.schemas import Address
```

**Classes:**
```python
class Company(CompanyInDB):
    """Schema for complete company data in API responses.  Includes related entities like addresses."""
```

```python
class CompanyBase(BaseModel):
    """Base schema for company data.

Attributes: name: Company name. account_number: Optional unique account identifier. account_type: Type of account. industry: Optional industry sector. is_active: Whether the company is active."""
```

```python
class CompanyCreate(CompanyBase):
    """Schema for creating a new company."""
```

```python
class CompanyInDB(CompanyBase):
    """Schema for company data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class CompanyUpdate(BaseModel):
    """Schema for updating an existing company.  All fields are optional to allow partial updates."""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/company/service.py`

##### Package: compliance
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/compliance`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/compliance/__init__.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/compliance/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, Date, DateTime, Enum as SQLAEnum, ForeignKey
from sqlalchemy import Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.products.models import Product
from app.domains.users.models import User
```

**Classes:**
```python
class ApprovalStatus(str, Enum):
    """Status of regulatory approvals.

Attributes: APPROVED: Fully approved. PENDING: Approval pending. REVOKED: Approval revoked. NOT_REQUIRED: Approval not required."""
```
*Class attributes:*
```python
APPROVED = 'Approved'
PENDING = 'Pending'
REVOKED = 'Revoked'
NOT_REQUIRED = 'Not Required'
```

```python
class ChemicalType(str, Enum):
    """Types of chemicals for regulatory compliance.

Attributes: CARCINOGEN: Cancer-causing chemicals. REPRODUCTIVE_TOXICANT: Chemicals harmful to reproduction. BOTH: Chemicals that are both carcinogenic and reproductive toxicants."""
```
*Class attributes:*
```python
CARCINOGEN = 'Carcinogen'
REPRODUCTIVE_TOXICANT = 'Reproductive Toxicant'
BOTH = 'Both'
```

```python
class ExposureScenario(str, Enum):
    """Scenarios for potential chemical exposure.

Attributes: CONSUMER: Exposure to general consumers. OCCUPATIONAL: Exposure in occupational settings. ENVIRONMENTAL: Environmental exposure."""
```
*Class attributes:*
```python
CONSUMER = 'Consumer'
OCCUPATIONAL = 'Occupational'
ENVIRONMENTAL = 'Environmental'
```

```python
class HazardousMaterial(Base):
    """Hazardous material information entity for products.

Attributes: id: Unique identifier. product_id: ID of the hazardous product. un_number: UN number for hazardous material. hazard_class: DOT hazard class. packing_group: Packing group (I, II, III). handling_instructions: Special handling instructions. restricted_transport: Transport restrictions. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'hazardous_material'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of HazardousMaterial instance.

Returns: String representation including product ID."""
```

```python
class ProductChemical(Base):
    """Product-chemical association entity.

Attributes: id: Unique identifier. product_id: ID of the product containing the chemical. chemical_id: ID of the chemical in the product. exposure_scenario: Type of exposure scenario. warning_required: Whether a warning label is required. warning_label: Text of the required warning label if applicable."""
```
*Class attributes:*
```python
__tablename__ = 'product_chemical'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductChemical instance.

Returns: String representation including product ID and chemical ID."""
```

```python
class ProductDOTApproval(Base):
    """Department of Transportation approval entity for products.

Attributes: id: Unique identifier. product_id: ID of the approved product. approval_status: Status of the approval. approval_number: DOT approval number if applicable. approved_by: Name of the approver. approval_date: Date of approval. expiration_date: Expiration date of the approval. reason: Reason for the approval status. changed_by_id: ID of the user who last changed the approval. changed_at: When the approval was last changed."""
```
*Class attributes:*
```python
__tablename__ = 'product_dot_approval'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductDOTApproval instance.

Returns: String representation including product ID and approval status."""
```

```python
class Prop65Chemical(Base):
    """California Proposition 65 chemical entity.

Attributes: id: Unique identifier. name: Chemical name. cas_number: CAS Registry Number (unique chemical identifier). type: Type of chemical hazard. exposure_limit: Safe harbor exposure limit if applicable. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'prop65_chemical'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Prop65Chemical instance.

Returns: String representation including name and CAS number."""
```

```python
class TransportRestriction(str, Enum):
    """Restrictions on product transportation methods.

Attributes: NONE: No restrictions. AIR: Air transport restricted. GROUND: Ground transport restricted. SEA: Sea transport restricted. ALL: All transport methods restricted."""
```
*Class attributes:*
```python
NONE = 'NONE'
AIR = 'AIR'
GROUND = 'GROUND'
SEA = 'SEA'
ALL = 'ALL'
```

```python
class Warning(Base):
    """Warning entity for products containing regulated chemicals.

Attributes: id: Unique identifier. product_id: ID of the product requiring the warning. chemical_id: ID of the chemical in the warning. warning_text: Text of the warning label. last_updated: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'warning'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Warning instance.

Returns: String representation including product ID and chemical ID."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/compliance/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.compliance.models import Prop65Chemical, Warning, ProductChemical, ProductDOTApproval, HazardousMaterial, ApprovalStatus, ChemicalType, ExposureScenario
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

**Classes:**
```python
class HazardousMaterialRepository(BaseRepository[(HazardousMaterial, uuid.UUID)]):
    """Repository for HazardousMaterial entity operations.

Provides methods for querying, creating, updating, and deleting HazardousMaterial entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the HazardousMaterial repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, hazmat_id) -> HazardousMaterial:
        """Ensure hazardous material information exists by ID, raising an exception if not found.

Args: hazmat_id: The hazardous material ID to check.

Returns: The hazardous material information if found.

Raises: ResourceNotFoundException: If the information is not found."""
```
```python
    async def find_by_product(self, product_id) -> Optional[HazardousMaterial]:
        """Find hazardous material information for a specific product.

Args: product_id: The product ID.

Returns: The hazardous material information if found, None otherwise."""
```
```python
    async def find_by_un_number(self, un_number) -> List[HazardousMaterial]:
        """Find hazardous materials by UN number.

Args: un_number: The UN number to search for.

Returns: List of hazardous materials with the specified UN number."""
```
```python
    async def get_by_hazard_class(self, hazard_class) -> List[HazardousMaterial]:
        """Get hazardous materials with a specific hazard class.

Args: hazard_class: The hazard class to filter by.

Returns: List of hazardous materials with the specified hazard class."""
```

```python
class ProductChemicalRepository(BaseRepository[(ProductChemical, uuid.UUID)]):
    """Repository for ProductChemical entity operations.

Provides methods for querying, creating, updating, and deleting ProductChemical entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the ProductChemical repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, association_id) -> ProductChemical:
        """Ensure a product chemical association exists by ID, raising an exception if not found.

Args: association_id: The association ID to check.

Returns: The product chemical association if found.

Raises: ResourceNotFoundException: If the association is not found."""
```
```python
    async def find_by_product_and_chemical(self, product_id, chemical_id) -> Optional[ProductChemical]:
        """Find a product chemical association by product and chemical IDs.

Args: product_id: The product ID. chemical_id: The chemical ID.

Returns: The product chemical association if found, None otherwise."""
```
```python
    async def get_by_exposure_scenario(self, scenario) -> List[ProductChemical]:
        """Get product chemical associations with a specific exposure scenario.

Args: scenario: The exposure scenario to filter by.

Returns: List of product chemical associations with the specified scenario."""
```
```python
    async def get_by_product(self, product_id) -> List[ProductChemical]:
        """Get chemical associations for a specific product.

Args: product_id: The product ID to filter by.

Returns: List of product chemical associations for the product."""
```
```python
    async def get_products_with_warnings(self) -> List[uuid.UUID]:
        """Get IDs of products that require warnings.  Returns: List of product IDs that require warnings."""
```

```python
class ProductDOTApprovalRepository(BaseRepository[(ProductDOTApproval, uuid.UUID)]):
    """Repository for ProductDOTApproval entity operations.

Provides methods for querying, creating, updating, and deleting ProductDOTApproval entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the ProductDOTApproval repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, approval_id) -> ProductDOTApproval:
        """Ensure a DOT approval exists by ID, raising an exception if not found.

Args: approval_id: The approval ID to check.

Returns: The DOT approval if found.

Raises: ResourceNotFoundException: If the approval is not found."""
```
```python
    async def find_by_approval_number(self, approval_number) -> Optional[ProductDOTApproval]:
        """Find a DOT approval by approval number.

Args: approval_number: The approval number to search for.

Returns: The DOT approval if found, None otherwise."""
```
```python
    async def find_by_product(self, product_id) -> Optional[ProductDOTApproval]:
        """Find a DOT approval for a specific product.

Args: product_id: The product ID.

Returns: The DOT approval if found, None otherwise."""
```
```python
    async def get_by_status(self, status) -> List[ProductDOTApproval]:
        """Get DOT approvals with a specific status.

Args: status: The approval status to filter by.

Returns: List of DOT approvals with the specified status."""
```
```python
    async def get_expiring_soon(self, days) -> List[ProductDOTApproval]:
        """Get DOT approvals that are expiring soon.

Args: days: Number of days to consider "soon".

Returns: List of DOT approvals expiring within the specified number of days."""
```

```python
class Prop65ChemicalRepository(BaseRepository[(Prop65Chemical, uuid.UUID)]):
    """Repository for Prop65Chemical entity operations.

Provides methods for querying, creating, updating, and deleting Prop65Chemical entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the Prop65Chemical repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, chemical_id) -> Prop65Chemical:
        """Ensure a chemical exists by ID, raising an exception if not found.

Args: chemical_id: The chemical ID to check.

Returns: The chemical if found.

Raises: ResourceNotFoundException: If the chemical is not found."""
```
```python
    async def find_by_cas_number(self, cas_number) -> Optional[Prop65Chemical]:
        """Find a chemical by its CAS number.

Args: cas_number: The CAS number to search for.

Returns: The chemical if found, None otherwise."""
```
```python
    async def find_by_name(self, name) -> List[Prop65Chemical]:
        """Find chemicals by name (partial match).

Args: name: The chemical name to search for.

Returns: List of chemicals with matching names."""
```
```python
    async def get_by_type(self, chemical_type) -> List[Prop65Chemical]:
        """Get chemicals of a specific type.

Args: chemical_type: The chemical type to filter by.

Returns: List of chemicals of the specified type."""
```

```python
class WarningRepository(BaseRepository[(Warning, uuid.UUID)]):
    """Repository for Warning entity operations.

Provides methods for querying, creating, updating, and deleting Warning entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the Warning repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, warning_id) -> Warning:
        """Ensure a warning exists by ID, raising an exception if not found.

Args: warning_id: The warning ID to check.

Returns: The warning if found.

Raises: ResourceNotFoundException: If the warning is not found."""
```
```python
    async def get_by_chemical(self, chemical_id) -> List[Warning]:
        """Get warnings for a specific chemical.

Args: chemical_id: The chemical ID to filter by.

Returns: List of warnings for the chemical."""
```
```python
    async def get_by_product(self, product_id) -> List[Warning]:
        """Get warnings for a specific product.

Args: product_id: The product ID to filter by.

Returns: List of warnings for the product."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/compliance/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.compliance.models import ChemicalType, ExposureScenario, ApprovalStatus, TransportRestriction
```

**Classes:**
```python
class HazardousMaterial(HazardousMaterialInDB):
    """Schema for complete HazardousMaterial data in API responses.

Includes related entities like product details."""
```

```python
class HazardousMaterialBase(BaseModel):
    """Base schema for HazardousMaterial data.

Attributes: product_id: ID of the hazardous product. un_number: UN number for hazardous material. hazard_class: DOT hazard class. packing_group: Packing group (I, II, III). handling_instructions: Special handling instructions. restricted_transport: Transport restrictions."""
```

```python
class HazardousMaterialCreate(HazardousMaterialBase):
    """Schema for creating a new HazardousMaterial."""
```

```python
class HazardousMaterialInDB(HazardousMaterialBase):
    """Schema for HazardousMaterial data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class HazardousMaterialUpdate(BaseModel):
    """Schema for updating an existing HazardousMaterial.

All fields are optional to allow partial updates."""
```

```python
class ProductChemical(ProductChemicalInDB):
    """Schema for complete ProductChemical data in API responses.

Includes related entities like chemical and product details."""
```

```python
class ProductChemicalBase(BaseModel):
    """Base schema for ProductChemical data.

Attributes: product_id: ID of the product containing the chemical. chemical_id: ID of the chemical in the product. exposure_scenario: Type of exposure scenario. warning_required: Whether a warning label is required. warning_label: Text of the required warning label if applicable."""
```

```python
class ProductChemicalCreate(ProductChemicalBase):
    """Schema for creating a new ProductChemical."""
```

```python
class ProductChemicalInDB(ProductChemicalBase):
    """Schema for ProductChemical data as stored in the database.

Includes database-specific fields like ID."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductChemicalUpdate(BaseModel):
    """Schema for updating an existing ProductChemical.  All fields are optional to allow partial updates."""
```

```python
class ProductDOTApproval(ProductDOTApprovalInDB):
    """Schema for complete ProductDOTApproval data in API responses.

Includes related entities like product and user details."""
```

```python
class ProductDOTApprovalBase(BaseModel):
    """Base schema for ProductDOTApproval data.

Attributes: product_id: ID of the approved product. approval_status: Status of the approval. approval_number: DOT approval number if applicable. approved_by: Name of the approver. approval_date: Date of approval. expiration_date: Expiration date of the approval. reason: Reason for the approval status."""
```

```python
class ProductDOTApprovalCreate(ProductDOTApprovalBase):
    """Schema for creating a new ProductDOTApproval."""
```

```python
class ProductDOTApprovalInDB(ProductDOTApprovalBase):
    """Schema for ProductDOTApproval data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductDOTApprovalUpdate(BaseModel):
    """Schema for updating an existing ProductDOTApproval.

All fields are optional to allow partial updates."""
```

```python
class Prop65Chemical(Prop65ChemicalInDB):
    """Schema for complete Prop65Chemical data in API responses."""
```

```python
class Prop65ChemicalBase(BaseModel):
    """Base schema for Prop65Chemical data.

Attributes: name: Chemical name. cas_number: CAS Registry Number (unique chemical identifier). type: Type of chemical hazard. exposure_limit: Safe harbor exposure limit if applicable."""
```

```python
class Prop65ChemicalCreate(Prop65ChemicalBase):
    """Schema for creating a new Prop65Chemical."""
```

```python
class Prop65ChemicalInDB(Prop65ChemicalBase):
    """Schema for Prop65Chemical data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class Prop65ChemicalUpdate(BaseModel):
    """Schema for updating an existing Prop65Chemical.  All fields are optional to allow partial updates."""
```

```python
class Warning(WarningInDB):
    """Schema for complete Warning data in API responses.

Includes related entities like chemical and product details."""
```

```python
class WarningBase(BaseModel):
    """Base schema for Warning data.

Attributes: product_id: ID of the product requiring the warning. chemical_id: ID of the chemical in the warning. warning_text: Text of the warning label."""
```

```python
class WarningCreate(WarningBase):
    """Schema for creating a new Warning."""
```

```python
class WarningInDB(WarningBase):
    """Schema for Warning data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class WarningUpdate(BaseModel):
    """Schema for updating an existing Warning.  All fields are optional to allow partial updates."""
```

##### Package: currency
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/currency`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/currency/__init__.py`

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/currency/exceptions.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/currency/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
```

**Classes:**
```python
class Currency(Base):
    """Currency entity representing a monetary currency.

Attributes: id: Unique identifier. code: ISO 4217 currency code. name: Currency name. symbol: Currency symbol. is_active: Whether the currency is active. is_base: Whether this is the base currency. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'currency'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Currency instance.

Returns: String representation including code and name."""
```

```python
class ExchangeRate(Base):
    """Exchange rate between two currencies.

Attributes: id: Unique identifier. source_currency_id: ID of the source currency. target_currency_id: ID of the target currency. rate: Exchange rate value. effective_date: When the rate became effective. fetched_at: When the rate was fetched. data_source: API or source that provided the rate. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'exchange_rate'
__table_args__ =     __table_args__ = (
        UniqueConstraint(
            "source_currency_id",
            "target_currency_id",
            "effective_date",
            name="uix_exchange_rate_source_target_date",
        ),
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ExchangeRate instance.

Returns: String representation including source, target, and rate."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/currency/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.currency.models import Currency, ExchangeRate
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, BusinessException
```

**Classes:**
```python
class CurrencyRepository(BaseRepository[(Currency, uuid.UUID)]):
    """Repository for Currency entity operations.

Provides methods for querying, creating, updating, and deleting Currency entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the currency repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, currency_id) -> Currency:
        """Ensure a currency exists by ID, raising an exception if not found.

Args: currency_id: The currency ID to check.

Returns: The currency if found.

Raises: ResourceNotFoundException: If the currency is not found."""
```
```python
    async def find_by_code(self, code) -> Optional[Currency]:
        """Find a currency by its ISO code.

Args: code: The ISO 4217 currency code.

Returns: The currency if found, None otherwise."""
```
```python
    async def get_active_currencies(self) -> List[Currency]:
        """Get all active currencies.  Returns: List of active currencies sorted by code."""
```
```python
    async def get_base_currency(self) -> Optional[Currency]:
        """Get the base currency of the system.  Returns: The base currency if found, None otherwise."""
```
```python
    async def set_as_base(self, currency_id) -> Currency:
        """Set a currency as the base currency.

This will unset any existing base currency.

Args: currency_id: The ID of the currency to set as base.

Returns: The updated currency.

Raises: ResourceNotFoundException: If the currency is not found. BusinessException: If the currency is not active."""
```

```python
class ExchangeRateRepository(BaseRepository[(ExchangeRate, uuid.UUID)]):
    """Repository for ExchangeRate entity operations.

Provides methods for querying, creating, updating, and deleting ExchangeRate entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the exchange rate repository.  Args: db: The database session."""
```
```python
    async def convert(self, source_currency_code, target_currency_code, amount) -> Tuple[(float, float, datetime)]:
        """Convert an amount between two currencies using the latest exchange rate.

Args: source_currency_code: The source currency code. target_currency_code: The target currency code. amount: The amount to convert.

Returns: Tuple containing (converted amount, exchange rate, timestamp).

Raises: ResourceNotFoundException: If either currency is not found. BusinessException: If no exchange rate is found."""
```
```python
    async def find_latest_rate(self, source_currency_id, target_currency_id) -> Optional[ExchangeRate]:
        """Find the latest exchange rate between two currencies.

Args: source_currency_id: The source currency ID. target_currency_id: The target currency ID.

Returns: The latest exchange rate if found, None otherwise."""
```
```python
    async def find_rate_at_date(self, source_currency_id, target_currency_id, date) -> Optional[ExchangeRate]:
        """Find the exchange rate between two currencies at a specific date.

Args: source_currency_id: The source currency ID. target_currency_id: The target currency ID. date: The date to find the rate for.

Returns: The exchange rate if found, None otherwise."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/currency/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

**Classes:**
```python
class ConversionRequest(BaseModel):
    """Schema for currency conversion request.

Attributes: source_currency: Source currency code. target_currency: Target currency code. amount: Amount to convert."""
```
*Methods:*
```python
@field_validator('source_currency', 'target_currency')
@classmethod
    def validate_currency_code(cls, v) -> str:
        """Validate and normalize currency codes.

Args: v: The currency code to validate.

Returns: Uppercase version of the currency code."""
```

```python
class ConversionResponse(BaseModel):
    """Schema for currency conversion response.

Attributes: source_currency: Source currency code. target_currency: Target currency code. source_amount: Original amount. converted_amount: Converted amount. exchange_rate: Exchange rate used. timestamp: Conversion timestamp."""
```

```python
class CurrencyBase(BaseModel):
    """Base schema for currency data.

Attributes: code: ISO 4217 currency code. name: Currency name. symbol: Currency symbol. is_active: Whether the currency is active. is_base: Whether this is the base currency."""
```

```python
class CurrencyCreate(CurrencyBase):
    """Schema for creating a new currency."""
```

```python
class CurrencyRead(CurrencyBase):
    """Schema for currency data in API responses.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class CurrencyUpdate(BaseModel):
    """Schema for updating an existing currency.  All fields are optional to allow partial updates."""
```

```python
class ExchangeRateBase(BaseModel):
    """Base schema for exchange rate data.

Attributes: source_currency_id: ID of the source currency. target_currency_id: ID of the target currency. rate: Exchange rate value. effective_date: When the rate became effective. data_source: API or source that provided the rate."""
```

```python
class ExchangeRateCreate(ExchangeRateBase):
    """Schema for creating a new exchange rate."""
```

```python
class ExchangeRateRead(ExchangeRateBase):
    """Schema for exchange rate data in API responses.

Includes database-specific fields and related currencies."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

###### Module: service
*Currency service for fetching and managing exchange rates.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/currency/service.py`

**Imports:**
```python
from __future__ import annotations
import datetime
from typing import Dict, Optional
import httpx
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.cache.decorators import cached
from app.core.config import settings
from app.logging import get_logger
from app.domains.currency.models import Currency, ExchangeRate
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.currency_service")
```

**Classes:**
```python
class ExchangeRateService(object):
    """Service for fetching and managing currency exchange rates."""
```
*Class attributes:*
```python
API_URL = 'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
DATA_SOURCE = 'exchangerate-api.com'
```
*Methods:*
```python
@classmethod
    async def convert_amount(cls, db, amount, source_code, target_code) -> Optional[float]:
        """Convert an amount from one currency to another.

Args: db: Database session amount: Amount to convert source_code: Source currency code target_code: Target currency code

Returns: Optional[float]: Converted amount or None if rate not found"""
```
```python
@classmethod
    async def fetch_latest_rates(cls, db, base_currency) -> Dict[(str, float)]:
        """Fetch the latest exchange rates from the API.

Args: db: Database session base_currency: Base currency code (default: USD)

Returns: Dict[str, float]: Dictionary of currency codes to rates

Raises: ValueError: If API key is missing or invalid httpx.RequestError: If request fails httpx.HTTPStatusError: If API returns error status"""
```
```python
@classmethod
@cached(prefix='currency', ttl=3600, backend='redis')
    async def get_latest_exchange_rate(cls, db, source_code, target_code) -> Optional[float]:
        """Get the latest exchange rate between two currencies.

Args: db: Database session source_code: Source currency code target_code: Target currency code

Returns: Optional[float]: Exchange rate or None if not found"""
```
```python
@classmethod
    async def update_exchange_rates(cls, db, force) -> int:
        """Update exchange rates in the database.

Args: db: Database session force: Force update even if not due yet

Returns: int: Number of rates updated

Raises: ValueError: If API returns invalid data SQLAlchemyError: If database operations fail"""
```

###### Module: tasks
*Celery tasks for currency operations.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/currency/tasks.py`

**Imports:**
```python
from __future__ import annotations
from typing import Dict, Optional
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from sqlalchemy.exc import SQLAlchemyError
from app.logging import get_logger
from app.db.session import get_db_context
from app.domains.currency.service import ExchangeRateService
```

**Global Variables:**
```python
logger = logger = get_logger("app.tasks.currency_tasks")
```

**Functions:**
```python
@shared_task
def init_currencies() -> Dict[(str, Optional[int])]:
    """Initialize currencies in the database.  Returns: Dict[str, Optional[int]]: Result of the operation"""
```

```python
@shared_task(bind=True, max_retries=3, default_retry_delay=300, autoretry_for=(Exception), retry_backoff=True)
def update_exchange_rates(self) -> Dict[(str, Optional[int])]:
    """Update exchange rates from the API.  Returns: Dict[str, Optional[int]]: Result of the operation"""
```

##### Package: fitment
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/fitment`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/fitment/__init__.py`

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/fitment/exceptions.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/fitment/models.py`

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/fitment/repository.py`

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/fitment/schemas.py`

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/fitment/service.py`

##### Package: inventory
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/inventory`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/inventory/__init__.py`

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/inventory/exceptions.py`

###### Module: handlers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/inventory/handlers.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/inventory/models.py`

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/inventory/repository.py`

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/inventory/schemas.py`

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/inventory/service.py`

##### Package: location
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/location`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/location/__init__.py`

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/location/exceptions.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/location/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.domains.reference.models import Warehouse, TariffCode
from app.domains.products.models import Manufacturer
from app.domains.company.schemas import Company
```

**Classes:**
```python
class Address(Base):
    """Address entity representing a physical location.

Attributes: id: Unique identifier. street: Street address. city: City name. state: State or province. postal_code: Postal or ZIP code. country_id: ID of the associated country. latitude: Geographic latitude. longitude: Geographic longitude. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'address'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Address instance.

Returns: String representation including street, city, and postal code."""
```

```python
class Country(Base):
    """Country entity representing a geographic country or territory.

Attributes: id: Unique identifier. name: Country name. iso_alpha_2: ISO 3166-1 alpha-2 code (2 letters). iso_alpha_3: ISO 3166-1 alpha-3 code (3 letters). iso_numeric: ISO 3166-1 numeric code (3 digits). region: Geographic region. subregion: Geographic subregion. currency: ISO 4217 currency code. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'country'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Country instance.

Returns: String representation including name and ISO code."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/location/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.location.models import Country, Address
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

**Classes:**
```python
class AddressRepository(BaseRepository[(Address, uuid.UUID)]):
    """Repository for Address entity operations.

Provides methods for querying, creating, updating, and deleting Address entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the address repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, address_id) -> Address:
        """Ensure an address exists by ID, raising an exception if not found.

Args: address_id: The address ID to check.

Returns: The address if found.

Raises: ResourceNotFoundException: If the address is not found."""
```
```python
    async def find_by_city(self, city, country_id) -> List[Address]:
        """Find addresses by city.

Args: city: The city name to search for. country_id: Optional country ID to restrict search.

Returns: List of addresses in the specified city."""
```
```python
    async def find_by_postal_code(self, postal_code, country_id) -> List[Address]:
        """Find addresses by postal code.

Args: postal_code: The postal code to search for. country_id: Optional country ID to restrict search.

Returns: List of addresses with matching postal code."""
```
```python
    async def search(self, search_term, page, page_size) -> Dict[(str, Any)]:
        """Search addresses by various fields.

Args: search_term: The term to search for. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

```python
class CountryRepository(BaseRepository[(Country, uuid.UUID)]):
    """Repository for Country entity operations.

Provides methods for querying, creating, updating, and deleting Country entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the country repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, country_id) -> Country:
        """Ensure a country exists by ID, raising an exception if not found.

Args: country_id: The country ID to check.

Returns: The country if found.

Raises: ResourceNotFoundException: If the country is not found."""
```
```python
    async def find_by_iso_code(self, iso_code) -> Optional[Country]:
        """Find a country by ISO code (alpha-2 or alpha-3).

Args: iso_code: The ISO code to search for.

Returns: The country if found, None otherwise."""
```
```python
    async def find_by_name(self, name) -> List[Country]:
        """Find countries by name (partial match).

Args: name: The country name to search for.

Returns: List of countries with matching names."""
```
```python
    async def get_by_currency(self, currency_code) -> List[Country]:
        """Get countries using a specific currency.

Args: currency_code: The ISO 4217 currency code.

Returns: List of countries using the specified currency."""
```
```python
    async def get_by_region(self, region) -> List[Country]:
        """Get countries in a specific region.

Args: region: The region to filter by.

Returns: List of countries in the specified region."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/location/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

**Classes:**
```python
class Address(AddressInDB):
    """Schema for complete Address data in API responses.  Includes related entities like country details."""
```

```python
class AddressBase(BaseModel):
    """Base schema for Address data.

Attributes: street: Street address. city: City name. state: State or province. postal_code: Postal or ZIP code. country_id: ID of the associated country. latitude: Geographic latitude. longitude: Geographic longitude."""
```
*Methods:*
```python
@field_validator('latitude')
@classmethod
    def validate_latitude(cls, v) -> Optional[float]:
        """Validate latitude value if provided.

Args: v: The latitude to validate or None.

Returns: Validated latitude or None.

Raises: ValueError: If the latitude is outside valid range."""
```
```python
@field_validator('longitude')
@classmethod
    def validate_longitude(cls, v) -> Optional[float]:
        """Validate longitude value if provided.

Args: v: The longitude to validate or None.

Returns: Validated longitude or None.

Raises: ValueError: If the longitude is outside valid range."""
```

```python
class AddressCreate(AddressBase):
    """Schema for creating a new Address."""
```

```python
class AddressInDB(AddressBase):
    """Schema for Address data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class AddressUpdate(BaseModel):
    """Schema for updating an existing Address.  All fields are optional to allow partial updates."""
```
*Methods:*
```python
@field_validator('latitude')
@classmethod
    def validate_latitude(cls, v) -> Optional[float]:
        """Validate latitude value if provided.

Args: v: The latitude to validate or None.

Returns: Validated latitude or None.

Raises: ValueError: If the latitude is outside valid range."""
```
```python
@field_validator('longitude')
@classmethod
    def validate_longitude(cls, v) -> Optional[float]:
        """Validate longitude value if provided.

Args: v: The longitude to validate or None.

Returns: Validated longitude or None.

Raises: ValueError: If the longitude is outside valid range."""
```

```python
class Country(CountryInDB):
    """Schema for complete Country data in API responses."""
```

```python
class CountryBase(BaseModel):
    """Base schema for Country data.

Attributes: name: Country name. iso_alpha_2: ISO 3166-1 alpha-2 code (2 letters). iso_alpha_3: ISO 3166-1 alpha-3 code (3 letters). iso_numeric: ISO 3166-1 numeric code (3 digits). region: Geographic region. subregion: Geographic subregion. currency: ISO 4217 currency code."""
```
*Methods:*
```python
@field_validator('iso_alpha_2', 'iso_alpha_3', 'currency', mode='before')
@classmethod
    def uppercase_codes(cls, v) -> Optional[str]:
        """Convert codes to uppercase if provided.

Args: v: The code to convert or None.

Returns: Uppercase code or None."""
```

```python
class CountryCreate(CountryBase):
    """Schema for creating a new Country."""
```

```python
class CountryInDB(CountryBase):
    """Schema for Country data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class CountryUpdate(BaseModel):
    """Schema for updating an existing Country.  All fields are optional to allow partial updates."""
```
*Methods:*
```python
@field_validator('iso_alpha_2', 'iso_alpha_3', 'currency', mode='before')
@classmethod
    def uppercase_codes(cls, v) -> Optional[str]:
        """Convert codes to uppercase if provided.

Args: v: The code to convert or None.

Returns: Uppercase code or None."""
```

```python
class GeocodeRequest(BaseModel):
    """Schema for geocoding request.

Attributes: address: Full address string to geocode. street: Street address component. city: City component. state: State or province component. postal_code: Postal or ZIP code component. country: Country component."""
```

```python
class GeocodeResult(BaseModel):
    """Schema for geocoding result.

Attributes: latitude: Geographic latitude. longitude: Geographic longitude. formatted_address: Formatted address string. confidence: Confidence score (0-100). components: Address components."""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/location/service.py`

##### Package: media
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/__init__.py`

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/exceptions.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, Enum as SQLAEnum, ForeignKey, Integer, String, func, text, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.products.models import Product
from app.models.associations import product_media_association
```

**Classes:**
```python
class Media(Base):
    """Media entity representing a stored file.

Attributes: id: Unique identifier filename: Original file name file_path: Path to the stored file file_size: File size in bytes media_type: Type of media mime_type: MIME type of the file visibility: Visibility setting file_metadata: Additional metadata about the file uploaded_by_id: ID of the user who uploaded the file is_approved: Whether the media has been approved approved_by_id: ID of the user who approved the media approved_at: When the media was approved created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'media'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Media instance.

Returns: String representation including filename and media type."""
```
```python
@property
    def extension(self) -> str:
        """Get the file extension.  Returns: The file extension or empty string if none."""
```
```python
@property
    def has_thumbnail(self) -> bool:
        """Check if this media has a thumbnail.

Returns: True if the media is an image (which have thumbnails), False otherwise."""
```
```python
@property
    def is_image(self) -> bool:
        """Check if this media is an image.  Returns: True if media_type is IMAGE, False otherwise."""
```

```python
class MediaType(str, Enum):
    """Types of media that can be stored in the system.

Attributes: IMAGE: Image files (jpg, png, etc.) DOCUMENT: Document files (pdf, doc, etc.) VIDEO: Video files (mp4, etc.) MSDS: Material Safety Data Sheets DOT_APPROVAL: Department of Transportation approval documents OTHER: Other media types"""
```
*Class attributes:*
```python
IMAGE = 'image'
DOCUMENT = 'document'
VIDEO = 'video'
MSDS = 'msds'
DOT_APPROVAL = 'dot_approval'
OTHER = 'other'
```

```python
class MediaVisibility(str, Enum):
    """Visibility settings for media files.

Attributes: PUBLIC: Accessible to anyone PRIVATE: Only accessible to authorized users RESTRICTED: Limited access based on specific rules"""
```
*Class attributes:*
```python
PUBLIC = 'public'
PRIVATE = 'private'
RESTRICTED = 'restricted'
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.media.models import Media, MediaType, MediaVisibility
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

**Classes:**
```python
class MediaRepository(BaseRepository[(Media, uuid.UUID)]):
    """Repository for Media entity operations.

Provides methods for querying, creating, updating, and deleting Media entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the media repository.  Args: db: The database session."""
```
```python
    async def approve(self, media_id, approver_id) -> Optional[Media]:
        """Approve a media item.

Args: media_id: ID of the media to approve. approver_id: ID of the user approving the media.

Returns: Updated media if found, None otherwise."""
```
```python
    async def ensure_exists(self, media_id) -> Media:
        """Ensure a media exists by ID, raising an exception if not found.

Args: media_id: The media ID to check.

Returns: The media if found.

Raises: ResourceNotFoundException: If the media is not found."""
```
```python
    async def find_by_filename(self, filename) -> List[Media]:
        """Find media by filename.

Args: filename: The filename to search for.

Returns: List of media with matching filename."""
```
```python
    async def find_by_media_type(self, media_type) -> List[Media]:
        """Find media by type.

Args: media_type: The media type to filter by.

Returns: List of media of the specified type."""
```
```python
    async def get_by_product(self, product_id, page, page_size) -> Dict[(str, Any)]:
        """Get paginated list of media for a specific product.

Args: product_id: The product ID to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_visibility(self, visibility, page, page_size) -> Dict[(str, Any)]:
        """Get paginated list of media with specified visibility.

Args: visibility: The visibility to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.media.models import MediaType, MediaVisibility
from app.core.config import settings
```

**Classes:**
```python
class FileUploadError(BaseModel):
    """Schema for file upload error.

Attributes: error: Error message. detail: Detailed error information."""
```

```python
class FileUploadResponse(BaseModel):
    """Schema for file upload response.

Attributes: media: Media object for the uploaded file. message: Success message."""
```

```python
class Media(MediaInDB):
    """Schema for complete media data in API responses.

Includes derived fields like URLs.

Attributes: url: URL to access the file. thumbnail_url: URL to access the thumbnail if available."""
```
*Methods:*
```python
    def model_post_init(self, __context) -> None:
        """Post-initialization hook to set URLs.  Args: __context: Initialization context (unused)."""
```

```python
class MediaBase(BaseModel):
    """Base schema for media data.

Attributes: filename: Original name of the file. media_type: Type of media. visibility: Visibility setting. file_metadata: Additional metadata about the file."""
```

```python
class MediaCreate(BaseModel):
    """Schema for creating new media.  Note: Filename is handled by the file upload process."""
```

```python
class MediaInDB(MediaBase):
    """Schema for media data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class MediaListResponse(BaseModel):
    """Schema for paginated list of media.

Attributes: items: List of media items. total: Total number of items. page: Current page number. page_size: Number of items per page. pages: Total number of pages."""
```

```python
class MediaUpdate(BaseModel):
    """Schema for updating existing media.  All fields are optional to allow partial updates."""
```

###### Package: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/service`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/service/__init__.py`

**Imports:**
```python
from typing import Optional
from app.domains.media.service.service import MediaService
```

**Functions:**
```python
async def get_media_service(storage_type) -> MediaService:
    """Get or create an initialized MediaService instance.

Args: storage_type: Optional storage type

Returns: An initialized MediaService instance"""
```

```python
def get_media_service_factory(storage_type) -> MediaService:
    """Get or create a MediaService instance without initialization.

Args: storage_type: Optional storage type

Returns: A non-initialized MediaService instance"""
```

####### Module: base
*Base interfaces and types for the media storage system.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/service/base.py`

**Imports:**
```python
from __future__ import annotations
from enum import Enum
from typing import BinaryIO, Optional, Protocol, TypedDict, Union
from fastapi import UploadFile
```

**Classes:**
```python
class FileMetadata(TypedDict):
    """File metadata type definition."""
```

```python
class FileNotFoundError(MediaStorageError):
    """Exception raised when a file is not found."""
```

```python
class MediaStorageBackend(Protocol):
    """Protocol defining media storage backend interface."""
```
*Methods:*
```python
    async def delete_file(self, file_path) -> bool:
        """Delete a file from storage.

Args: file_path: Relative path to the file

Returns: bool: True if file was successfully deleted, False otherwise

Raises: MediaStorageError: If deletion fails"""
```
```python
    async def file_exists(self, file_path) -> bool:
        """Check if a file exists in storage.

Args: file_path: Relative path to the file

Returns: bool: True if file exists, False otherwise"""
```
```python
    async def generate_thumbnail(self, file_path, width, height) -> Optional[str]:
        """Generate a thumbnail for an image file.

Args: file_path: Relative path to the original image width: Desired thumbnail width height: Desired thumbnail height

Returns: Optional[str]: Path to the thumbnail if successful, None otherwise

Raises: MediaStorageError: If thumbnail generation fails"""
```
```python
    async def get_file_url(self, file_path) -> str:
        """Get the URL for accessing a file.

Args: file_path: Relative path to the file

Returns: str: Public URL to access the file"""
```
```python
    async def initialize(self) -> None:
        """Initialize storage backend connection."""
```
```python
    async def save_file(self, file, destination, media_type, content_type) -> str:
        """Save a file to storage and return its public URL.

Args: file: The file to upload (UploadFile, file-like object, or bytes) destination: Relative path where the file should be stored media_type: Type of media being stored content_type: Optional content type override

Returns: str: Public URL to access the file

Raises: MediaStorageError: If saving fails"""
```

```python
class MediaStorageError(Exception):
    """Base exception for media storage errors."""
```

```python
class StorageBackendType(str, Enum):
    """Enumeration of supported storage backend types."""
```
*Class attributes:*
```python
LOCAL = 'local'
S3 = 's3'
AZURE = 'azure'
```

```python
class StorageConnectionError(MediaStorageError):
    """Exception raised when connection to storage fails."""
```

####### Module: factory
*Factory module for creating media storage backends.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/service/factory.py`

**Imports:**
```python
from __future__ import annotations
from typing import Optional
from app.domains.media.service.base import MediaStorageBackend, StorageBackendType
from app.domains.media.service.local import LocalMediaStorage
from app.domains.media.service.s3 import S3MediaStorage
from app.core.config import settings
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.media.service.factory")
```

**Classes:**
```python
class StorageBackendFactory(object):
    """Factory for creating media storage backends."""
```
*Methods:*
```python
@staticmethod
    def get_backend(backend_type) -> MediaStorageBackend:
        """Get a storage backend instance based on type.

Args: backend_type: The type of backend to create. If None, will use the value from settings.MEDIA_STORAGE_TYPE.

Returns: An instance of MediaStorageBackend.

Raises: ValueError: If an unsupported backend type is specified."""
```

####### Module: local
*Local filesystem storage backend implementation.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/service/local.py`

**Imports:**
```python
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO, Dict, Optional, Set, Tuple, Union
import aiofiles
from app.domains.media.service.base import FileNotFoundError, MediaStorageError
from app.domains.media.service.thumbnails import ThumbnailGenerator
from fastapi import UploadFile
from app.core.config import settings
from app.logging import get_logger
from app.domains.media.models import MediaType
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.media.service.local")
```

**Classes:**
```python
@dataclass
class LocalMediaStorage(object):
    """Local filesystem storage backend for development."""
```
*Methods:*
```python
    def __post_init__(self) -> None:
        """Ensure media directories exist."""
```
```python
    async def delete_file(self, file_path) -> bool:
        """Delete file from local storage asynchronously.

Args: file_path: Relative path to the file

Returns: bool: True if file was successfully deleted, False otherwise

Raises: FileNotFoundError: If the file doesn't exist MediaStorageError: If deletion fails"""
```
```python
    async def file_exists(self, file_path) -> bool:
        """Check if a file exists in storage asynchronously.

Args: file_path: Relative path to the file

Returns: bool: True if file exists, False otherwise"""
```
```python
    async def generate_thumbnail(self, file_path, width, height) -> Optional[str]:
        """Generate a thumbnail for an image file asynchronously.

Args: file_path: Relative path to the original image width: Desired thumbnail width height: Desired thumbnail height

Returns: Optional[str]: Path to the thumbnail if successful, None otherwise

Raises: MediaStorageError: If thumbnail generation fails FileNotFoundError: If the original file doesn't exist"""
```
```python
    async def get_file_url(self, file_path) -> str:
        """Get URL for local file.

Args: file_path: Relative path to the file

Returns: str: Public URL to access the file"""
```
```python
    async def initialize(self) -> None:
        """Initialize storage backend connection.

For local storage, this is a no-op as directories are created in __post_init__."""
```
```python
    async def save_file(self, file, destination, media_type, content_type) -> str:
        """Save file to local storage asynchronously.

Args: file: The file to upload (UploadFile, file-like object, or bytes) destination: Relative path where the file should be stored media_type: Type of media being stored content_type: Optional content type override

Returns: str: URL to access the saved file

Raises: MediaStorageError: If file saving fails ValueError: If invalid file type or format"""
```

####### Module: s3
*Amazon S3 storage backend implementation.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/service/s3.py`

**Imports:**
```python
from __future__ import annotations
import tempfile
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncGenerator, BinaryIO, Dict, Optional, Set, Union
import aioboto3
import aiofiles
from app.domains.media.service.base import FileNotFoundError, MediaStorageError, StorageConnectionError
from app.domains.media.service.thumbnails import ThumbnailGenerator
from fastapi import UploadFile
from app.core.config import settings
from app.logging import get_logger
from app.domains.media.models import MediaType
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.media.service.s3")
```

**Classes:**
```python
@dataclass
class S3MediaStorage(object):
    """Amazon S3 storage backend for production."""
```
*Methods:*
```python
    async def delete_file(self, file_path) -> bool:
        """Delete file from S3 storage.

Args: file_path: Relative path to the file

Returns: bool: True if file was successfully deleted, False otherwise

Raises: MediaStorageError: If deletion fails"""
```
```python
    async def file_exists(self, file_path) -> bool:
        """Check if a file exists in S3 storage.

Args: file_path: Relative path to the file

Returns: bool: True if file exists, False otherwise"""
```
```python
    async def generate_thumbnail(self, file_path, width, height) -> Optional[str]:
        """Generate a thumbnail for an image file in S3.

This implementation downloads the file, generates the thumbnail locally, then uploads it back to S3. In a production environment, you might want to use a service like AWS Lambda or a dedicated image processing service.

Args: file_path: Relative path to the original image width: Desired thumbnail width height: Desired thumbnail height

Returns: Optional[str]: Path to the thumbnail if successful, None otherwise

Raises: MediaStorageError: If thumbnail generation fails"""
```
```python
    async def get_file_url(self, file_path) -> str:
        """Get URL for S3 file.

Args: file_path: Relative path to the file

Returns: str: Public URL to access the file"""
```
```python
    async def initialize(self) -> None:
        """Initialize S3 client and create bucket if it doesn't exist.

Raises: StorageConnectionError: If connection to S3 fails"""
```
```python
    async def save_file(self, file, destination, media_type, content_type) -> str:
        """Save file to S3 storage.

Args: file: The file to upload (UploadFile, file-like object, or bytes) destination: Relative path where the file should be stored media_type: Type of media being stored content_type: Optional content type override

Returns: str: URL to access the saved file

Raises: MediaStorageError: If file saving fails ValueError: If invalid file type or format"""
```

####### Module: service
*Main media service implementation.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/service/service.py`

**Imports:**
```python
from __future__ import annotations
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from app.domains.media.service.base import FileNotFoundError, MediaStorageBackend, MediaStorageError, StorageBackendType
from app.domains.media.service.factory import StorageBackendFactory
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings
from app.logging import get_logger
from app.domains.media.models import MediaType, MediaVisibility
from app.services.interfaces import ServiceInterface
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.media.service.service")
```

**Classes:**
```python
class MediaService(ServiceInterface):
    """Service for handling media file operations with configurable storage backends."""
```
*Methods:*
```python
    def __init__(self, storage_type):
        """Initialize the media service.

Args: storage_type: Optional storage backend type. If None, uses the value from settings."""
```
```python
    async def delete_file(self, file_url) -> bool:
        """Delete a file from storage with improved error handling.

Args: file_url: URL of the file to delete

Returns: bool: True if file was successfully deleted

Raises: HTTPException: If deletion fails"""
```
```python
    async def ensure_initialized(self) -> None:
        """Ensure the service is initialized."""
```
```python
    async def initialize(self) -> None:
        """Initialize the media service and storage backend.

This must be called before using any other methods.

Raises: MediaStorageError: If storage initialization fails"""
```
```python
    async def shutdown(self) -> None:
        """Release resources during service shutdown."""
```
```python
    async def upload_file(self, file, media_type, product_id, filename, visibility, generate_thumbnail) -> Tuple[(str, Dict[(str, Any)], Optional[str])]:
        """Upload a file to storage with improved error handling.

Args: file: The uploaded file media_type: Type of media being uploaded product_id: Optional product ID to associate with the file filename: Optional filename override visibility: Visibility level for the file generate_thumbnail: Whether to generate a thumbnail for images

Returns: Tuple[str, Dict[str, Any], Optional[str]]: Tuple of (file URL, metadata, thumbnail URL or None)

Raises: HTTPException: If the file type is invalid or upload fails"""
```

####### Module: thumbnails
*Thumbnail generation utilities.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/media/service/thumbnails.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
from pathlib import Path
from typing import Tuple
from app.domains.media.service.base import FileNotFoundError, MediaStorageError
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.media.service.thumbnails")
```

**Classes:**
```python
class ThumbnailGenerator(object):
    """Utility class for generating thumbnails from images."""
```
*Methods:*
```python
@staticmethod
    def can_generate_thumbnail(file_path) -> bool:
        """Check if a thumbnail can be generated for a file based on its extension.

Args: file_path: Path to the file

Returns: bool: True if a thumbnail can be generated, False otherwise"""
```
```python
@staticmethod
    async def generate_thumbnail(file_path, output_path, width, height, quality) -> None:
        """Generate a thumbnail for an image file.

Args: file_path: Path to the original image output_path: Path where the thumbnail should be saved width: Desired thumbnail width height: Desired thumbnail height quality: JPEG quality (1-100)

Raises: FileNotFoundError: If the original file doesn't exist MediaStorageError: If thumbnail generation fails"""
```
```python
@staticmethod
    def get_supported_formats() -> Tuple[(str, Ellipsis)]:
        """Get a list of supported image formats for thumbnail generation.

Returns: Tuple of supported file extensions (lowercase, with dot)"""
```
```python
@staticmethod
    def get_thumbnail_path(original_path, width, height, thumbnails_dir) -> str:
        """Get the path where a thumbnail should be stored.

Args: original_path: Path to the original image width: Thumbnail width height: Thumbnail height thumbnails_dir: Directory for storing thumbnails

Returns: str: Path to the thumbnail"""
```

##### Package: model_mapping
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/model_mapping`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/model_mapping/__init__.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/model_mapping/models.py`

**Imports:**
```python
from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base
```

**Classes:**
```python
class ModelMapping(Base):
    """Model mapping entity for vehicle model translation.

Attributes: id: Unique auto-incrementing identifier. pattern: Pattern to match in vehicle text. mapping: Mapping in format 'Make|VehicleCode|Model'. priority: Priority for mapping (higher values are processed first). active: Whether this mapping is active. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'model_mapping'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ModelMapping instance.

Returns: String representation including id, pattern, and mapping."""
```
```python
@property
    def make(self) -> str:
        """Get the make part of the mapping.  Returns: The make value or empty string if not available."""
```
```python
@property
    def model(self) -> str:
        """Get the model part of the mapping.  Returns: The model value or empty string if not available."""
```
```python
@property
    def vehicle_code(self) -> str:
        """Get the vehicle code part of the mapping.

Returns: The vehicle code value or empty string if not available."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/model_mapping/repository.py`

**Imports:**
```python
from __future__ import annotations
import re
from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.model_mapping.models import ModelMapping
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

**Classes:**
```python
class ModelMappingRepository(BaseRepository[(ModelMapping, int)]):
    """Repository for ModelMapping entity operations.

Provides methods for querying, creating, updating, and deleting ModelMapping entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the model mapping repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, mapping_id) -> ModelMapping:
        """Ensure a model mapping exists by ID, raising an exception if not found.

Args: mapping_id: The model mapping ID to check.

Returns: The model mapping if found.

Raises: ResourceNotFoundException: If the model mapping is not found."""
```
```python
    async def find_by_make_model(self, make, model) -> List[ModelMapping]:
        """Find model mappings by make and model.

Args: make: The make to search for. model: The model to search for.

Returns: List of model mappings for the make and model."""
```
```python
    async def find_by_pattern(self, pattern) -> List[ModelMapping]:
        """Find model mappings by pattern.

Args: pattern: The pattern to search for.

Returns: List of model mappings matching the pattern."""
```
```python
    async def get_active_mappings(self, page, page_size) -> Dict[(str, Any)]:
        """Get paginated list of active model mappings.

Args: page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_make(self, make) -> List[ModelMapping]:
        """Get model mappings for a specific make.

Args: make: The make to filter by.

Returns: List of model mappings for the make."""
```
```python
    async def match_vehicle_string(self, vehicle_string) -> Optional[Dict[(str, str)]]:
        """Match a vehicle string against patterns to find the correct mapping.

Args: vehicle_string: The vehicle string to match.

Returns: Dictionary with make, code, and model if matched, None otherwise."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/model_mapping/schemas.py`

**Imports:**
```python
from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

**Classes:**
```python
class ModelMapping(ModelMappingInDB):
    """Schema for complete ModelMapping data in API responses.  Includes additional computed properties."""
```
*Methods:*
```python
@property
    def make(self) -> str:
        """Get the make part of the mapping.  Returns: The make value or empty string if not available."""
```
```python
@property
    def model(self) -> str:
        """Get the model part of the mapping.  Returns: The model value or empty string if not available."""
```
```python
@property
    def vehicle_code(self) -> str:
        """Get the vehicle code part of the mapping.

Returns: The vehicle code value or empty string if not available."""
```

```python
class ModelMappingBase(BaseModel):
    """Base schema for ModelMapping data.

Attributes: pattern: Pattern to match in vehicle text. mapping: Mapping in format 'Make|VehicleCode|Model'. priority: Priority for mapping (higher values are processed first). active: Whether this mapping is active."""
```
*Methods:*
```python
@field_validator('mapping')
@classmethod
    def validate_mapping_format(cls, v) -> str:
        """Validate mapping format.

Args: v: The mapping string to validate.

Returns: Validated mapping string.

Raises: ValueError: If the mapping format is invalid."""
```

```python
class ModelMappingCreate(ModelMappingBase):
    """Schema for creating a new ModelMapping."""
```

```python
class ModelMappingInDB(ModelMappingBase):
    """Schema for ModelMapping data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ModelMappingPaginatedResponse(BaseModel):
    """Schema for paginated model mapping data.

Attributes: items: List of model mappings. total: Total number of items. page: Current page number. page_size: Number of items per page. pages: Total number of pages."""
```

```python
class ModelMappingUpdate(BaseModel):
    """Schema for updating an existing ModelMapping.  All fields are optional to allow partial updates."""
```
*Methods:*
```python
@field_validator('mapping')
@classmethod
    def validate_mapping_format(cls, v) -> Optional[str]:
        """Validate mapping format if provided.

Args: v: The mapping string to validate or None.

Returns: Validated mapping string or None.

Raises: ValueError: If the mapping format is invalid."""
```

```python
class VehicleMatchRequest(BaseModel):
    """Schema for vehicle matching request.

Attributes: vehicle_string: Vehicle string to match against patterns."""
```

```python
class VehicleMatchResponse(BaseModel):
    """Schema for vehicle matching response.

Attributes: matched: Whether a match was found. make: Make value if matched. code: Vehicle code value if matched. model: Model value if matched. pattern: Pattern that matched. mapping: Original mapping string."""
```

##### Package: products
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/products`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/products/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.domains.products.models import Product, Brand, ProductDescription
from app.domains.products.schemas import ProductCreate, ProductUpdate, Product as ProductSchema, Brand as BrandSchema
from app.domains.products.service import ProductService
from app.domains.products.exceptions import ProductNotFoundException, DuplicatePartNumberException, ProductInactiveException
from app.domains.products import handlers
```

**Global Variables:**
```python
__all__ = __all__ = [
    # Models
    "Product",
    "Brand",
    "ProductDescription",
    # Schemas
    "ProductCreate",
    "ProductUpdate",
    "ProductSchema",
    "BrandSchema",
    # Services
    "ProductService",
    # Exceptions
    "ProductNotFoundException",
    "DuplicatePartNumberException",
    "ProductInactiveException",
]
```

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/products/exceptions.py`

**Imports:**
```python
from __future__ import annotations
from app.core.exceptions import BusinessException, ResourceNotFoundException
```

**Classes:**
```python
class BrandNotFoundException(ResourceNotFoundException):
    """Raised when a brand cannot be found."""
```
*Methods:*
```python
    def __init__(self, brand_id) -> None:
        """Initialize the exception.  Args: brand_id: ID of the brand that wasn't found"""
```

```python
class DuplicateBrandNameException(BusinessException):
    """Raised when attempting to create a brand with an existing name."""
```
*Methods:*
```python
    def __init__(self, name) -> None:
        """Initialize the exception.  Args: name: The duplicate brand name"""
```

```python
class DuplicatePartNumberException(BusinessException):
    """Raised when attempting to create a product with an existing part number."""
```
*Methods:*
```python
    def __init__(self, part_number) -> None:
        """Initialize the exception.  Args: part_number: The duplicate part number"""
```

```python
class ProductInactiveException(BusinessException):
    """Raised when attempting operations on an inactive product."""
```
*Methods:*
```python
    def __init__(self, product_id) -> None:
        """Initialize the exception.  Args: product_id: ID of the inactive product"""
```

```python
class ProductNotFoundException(ResourceNotFoundException):
    """Raised when a product cannot be found."""
```
*Methods:*
```python
    def __init__(self, product_id) -> None:
        """Initialize the exception.  Args: product_id: ID of the product that wasn't found"""
```

###### Module: handlers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/products/handlers.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
from typing import Any, Dict
from uuid import UUID
from app.core.events import subscribe_to_event
from app.db.session import get_db
from app.domains.products.repository import ProductRepository
```

**Global Variables:**
```python
logger = logger = get_logger("app.domains.products.handlers")
```

**Functions:**
```python
@subscribe_to_event('inventory.stock_level_critical')
async def handle_critical_stock_level(payload) -> None:
    """Mark products as out of stock when inventory is critically low.

Args: payload: Event data containing stock information"""
```

```python
@subscribe_to_event('pricing.price_update')
async def handle_price_update(payload) -> None:
    """Update product prices when pricing information changes.

Args: payload: Event data containing pricing information"""
```

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/products/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy import UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.media.models import Media
from app.domains.reference.models import Color, ConstructionType, Hardware, PackagingType, TariffCode, Texture, UnspscCode
from app.domains.location.models import Country
from app.models.associations import product_color_association, product_construction_type_association, product_country_origin_association, product_fitment_association, product_hardware_association, product_media_association, product_packaging_association, product_tariff_code_association, product_texture_association, product_unspsc_association
```

**Classes:**
```python
class AttributeDefinition(Base):
    """Attribute definition entity representing a product attribute type.

Attributes: id: Unique identifier. name: Attribute name. code: Attribute code (unique). description: Attribute description. data_type: Data type (e.g., string, number, boolean, etc.). is_required: Whether the attribute is required. default_value: Default value for the attribute. validation_regex: Regex for validation of string values. min_value: Minimum allowed value for numeric attributes. max_value: Maximum allowed value for numeric attributes. options: Available options for enum-like attributes. display_order: Display order position. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'attribute_definition'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of AttributeDefinition instance.

Returns: String representation including code."""
```

```python
class Brand(Base):
    """Brand entity representing a product brand.

Attributes: id: Unique identifier. name: Brand name. parent_company_id: ID of the parent company. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'brand'
parent_company =     parent_company = relationship("Company", foreign_keys=[parent_company_id])
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Brand instance.  Returns: String representation including name."""
```

```python
class Fitment(Base):
    """Fitment entity representing vehicle compatibility for a product.

Attributes: id: Unique identifier. year: Vehicle year. make: Vehicle make. model: Vehicle model. engine: Engine specification. transmission: Transmission specification. attributes: Additional fitment attributes. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'fitment'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Fitment instance.

Returns: String representation including year, make, and model."""
```

```python
class Manufacturer(Base):
    """Manufacturer entity representing a product manufacturer.

Attributes: id: Unique identifier. name: Manufacturer name. company_id: ID of the associated company. address_id: ID of the primary address. billing_address_id: ID of the billing address. shipping_address_id: ID of the shipping address. country_id: ID of the country of origin. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'manufacturer'
company =     company = relationship("Company", foreign_keys=[company_id])
address =     address = relationship("Address", foreign_keys=[address_id])
billing_address =     billing_address = relationship("Address", foreign_keys=[billing_address_id])
shipping_address =     shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
country =     country = relationship("Country", foreign_keys=[country_id])
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Manufacturer instance.

Returns: String representation including name."""
```

```python
class PriceType(Base):
    """Price type entity representing a type of pricing (e.g., retail, wholesale, etc.).

Attributes: id: Unique identifier. name: Price type name. description: Price type description. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'price_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of PriceType instance.  Returns: String representation including name."""
```

```python
class Product(Base):
    """Product entity representing a sellable item.

Attributes: id: Unique identifier. part_number: Product part number (unique). part_number_stripped: Normalized version of part number for searching. application: Product application or use case description. vintage: Whether the product is for vintage vehicles. late_model: Whether the product is for late model vehicles. soft: Whether the product is soft (e.g., fabric vs metal). universal: Whether the product is universal (fits multiple applications). search_vector: Full-text search vector. is_active: Whether the product is active in the catalog. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'product'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Product instance.

Returns: String representation including part number."""
```

```python
class ProductActivity(Base):
    """Product activity entity representing status changes for a product.

Attributes: id: Unique identifier. product_id: ID of the associated product. status: Product status (e.g., active, inactive, discontinued, etc.). reason: Reason for the status change. changed_by_id: ID of the user who made the change. changed_at: When the change was made."""
```
*Class attributes:*
```python
__tablename__ = 'product_activity'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductActivity instance.

Returns: String representation including status and product ID."""
```

```python
class ProductAttribute(Base):
    """Product attribute entity representing a specific attribute value for a product.

Attributes: id: Unique identifier. product_id: ID of the associated product. attribute_id: ID of the attribute definition. value_string: String value. value_number: Numeric value. value_boolean: Boolean value. value_date: Date value. value_json: JSON value. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'product_attribute'
__table_args__ =     __table_args__ = (
        UniqueConstraint("product_id", "attribute_id", name="uix_product_attribute"),
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductAttribute instance.

Returns: String representation including product ID and attribute ID."""
```

```python
class ProductBrandHistory(Base):
    """Product brand history entity representing brand changes for a product.

Attributes: id: Unique identifier. product_id: ID of the associated product. old_brand_id: ID of the previous brand. new_brand_id: ID of the new brand. changed_by_id: ID of the user who made the change. changed_at: When the change was made."""
```
*Class attributes:*
```python
__tablename__ = 'product_brand_history'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductBrandHistory instance.

Returns: String representation including product ID and brand change."""
```

```python
class ProductDescription(Base):
    """Product description entity representing a textual description of a product.

Attributes: id: Unique identifier. product_id: ID of the associated product. description_type: Type of description (e.g., short, long, etc.). description: The actual description text. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'product_description'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductDescription instance.

Returns: String representation including description type and product ID."""
```

```python
class ProductMarketing(Base):
    """Product marketing entity representing marketing content for a product.

Attributes: id: Unique identifier. product_id: ID of the associated product. marketing_type: Type of marketing content (e.g., bullet point, ad copy, etc.). content: The actual marketing content. position: Display order position. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'product_marketing'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductMarketing instance.

Returns: String representation including marketing type and product ID."""
```

```python
class ProductMeasurement(Base):
    """Product measurement entity representing physical measurements of a product.

Attributes: id: Unique identifier. product_id: ID of the associated product. manufacturer_id: ID of the manufacturer who provided the measurements. length: Length measurement. width: Width measurement. height: Height measurement. weight: Weight measurement. volume: Volume measurement. dimensional_weight: Dimensional weight for shipping calculations. effective_date: When the measurements became effective."""
```
*Class attributes:*
```python
__tablename__ = 'product_measurement'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductMeasurement instance.

Returns: String representation including product ID."""
```

```python
class ProductPricing(Base):
    """Product pricing entity representing a price for a product.

Attributes: id: Unique identifier. product_id: ID of the associated product. pricing_type_id: ID of the price type. manufacturer_id: ID of the manufacturer. price: Price value. currency: Currency code. last_updated: When the price was last updated."""
```
*Class attributes:*
```python
__tablename__ = 'product_pricing'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductPricing instance.

Returns: String representation including product ID, pricing type, and price."""
```

```python
class ProductStock(Base):
    """Product stock entity representing inventory levels for a product.

Attributes: id: Unique identifier. product_id: ID of the associated product. warehouse_id: ID of the warehouse. quantity: Stock quantity. last_updated: When the stock level was last updated."""
```
*Class attributes:*
```python
__tablename__ = 'product_stock'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductStock instance.

Returns: String representation including product ID, warehouse ID, and quantity."""
```

```python
class ProductSupersession(Base):
    """Product supersession entity representing when one product replaces another.

Attributes: id: Unique identifier. old_product_id: ID of the product being replaced. new_product_id: ID of the replacement product. reason: Reason for the supersession. changed_at: When the supersession was created."""
```
*Class attributes:*
```python
__tablename__ = 'product_supersession'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ProductSupersession instance.

Returns: String representation including old and new product IDs."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/products/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.products.models import Product, Brand, Fitment, ProductActivity, ProductSupersession
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, BusinessException
```

**Classes:**
```python
class BrandRepository(BaseRepository[(Brand, uuid.UUID)]):
    """Repository for Brand entity operations.

Provides methods for querying, creating, updating, and deleting Brand entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the brand repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, brand_id) -> Brand:
        """Ensure a brand exists by ID, raising an exception if not found.

Args: brand_id: The brand ID to check.

Returns: The brand if found.

Raises: ResourceNotFoundException: If the brand is not found."""
```
```python
    async def find_by_name(self, name) -> Optional[Brand]:
        """Find a brand by exact name.

Args: name: The brand name to search for.

Returns: The brand if found, None otherwise."""
```
```python
    async def find_by_name_partial(self, name) -> List[Brand]:
        """Find brands by partial name match.

Args: name: The brand name to search for.

Returns: List of brands with matching names."""
```
```python
    async def get_by_company(self, company_id) -> List[Brand]:
        """Get brands owned by a specific company.

Args: company_id: The company ID to filter by.

Returns: List of brands owned by the specified company."""
```

```python
class FitmentRepository(BaseRepository[(Fitment, uuid.UUID)]):
    """Repository for Fitment entity operations.

Provides methods for querying, creating, updating, and deleting Fitment entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the fitment repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, fitment_id) -> Fitment:
        """Ensure a fitment exists by ID, raising an exception if not found.

Args: fitment_id: The fitment ID to check.

Returns: The fitment if found.

Raises: ResourceNotFoundException: If the fitment is not found."""
```
```python
    async def find_by_vehicle(self, year, make, model, engine, transmission) -> List[Fitment]:
        """Find fitments matching a specific vehicle.

Args: year: Vehicle year. make: Vehicle make. model: Vehicle model. engine: Optional engine specification. transmission: Optional transmission specification.

Returns: List of matching fitments."""
```
```python
    async def get_makes_by_year(self, year) -> List[str]:
        """Get all makes available for a specific year.

Args: year: Vehicle year.

Returns: List of unique make names."""
```
```python
    async def get_models_by_year_make(self, year, make) -> List[str]:
        """Get all models available for a specific year and make.

Args: year: Vehicle year. make: Vehicle make.

Returns: List of unique model names."""
```
```python
    async def get_years_range(self) -> Tuple[(int, int)]:
        """Get the minimum and maximum years in the fitment data.

Returns: Tuple containing (min_year, max_year)."""
```

```python
class ProductRepository(BaseRepository[(Product, uuid.UUID)]):
    """Repository for Product entity operations.

Provides methods for querying, creating, updating, and deleting Product entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the product repository.  Args: db: The database session."""
```
```python
    async def create_supersession(self, old_product_id, new_product_id, reason) -> ProductSupersession:
        """Create a product supersession (one product replacing another).

Args: old_product_id: ID of the product being replaced. new_product_id: ID of the replacement product. reason: Optional reason for the supersession.

Returns: The created supersession record.

Raises: ResourceNotFoundException: If either product is not found. BusinessException: If trying to supersede a product with itself."""
```
```python
    async def ensure_exists(self, product_id) -> Product:
        """Ensure a product exists by ID, raising an exception if not found.

Args: product_id: The product ID to check.

Returns: The product if found.

Raises: ResourceNotFoundException: If the product is not found."""
```
```python
    async def find_by_part_number(self, part_number) -> Optional[Product]:
        """Find a product by exact part number.

Args: part_number: The part number to search for.

Returns: The product if found, None otherwise."""
```
```python
    async def find_by_part_number_stripped(self, part_number) -> List[Product]:
        """Find products by normalized part number.

Args: part_number: The part number to search for.

Returns: List of products with matching normalized part number."""
```
```python
    async def get_active_products(self, page, page_size) -> Dict[(str, Any)]:
        """Get paginated list of active products.

Args: page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_fitment(self, year, make, model, engine, transmission, page, page_size) -> Dict[(str, Any)]:
        """Get products compatible with a specific vehicle fitment.

Args: year: Vehicle year. make: Vehicle make. model: Vehicle model. engine: Optional engine specification. transmission: Optional transmission specification. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def search(self, search_term, page, page_size) -> Dict[(str, Any)]:
        """Search products by various fields.

Args: search_term: The term to search for. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def update_status(self, product_id, status, reason, user_id) -> Tuple[(Product, ProductActivity)]:
        """Update a product's status and create an activity record.

Args: product_id: ID of the product to update. status: New status value. reason: Optional reason for the status change. user_id: Optional ID of the user making the change.

Returns: Tuple containing (updated product, activity record).

Raises: ResourceNotFoundException: If the product is not found."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/products/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
```

**Classes:**
```python
class Brand(BrandInDB):
    """Schema for complete Brand data in API responses.

Includes related entities like parent company details."""
```

```python
class BrandBase(BaseModel):
    """Base schema for Brand data.

Attributes: name: Brand name. parent_company_id: ID of the parent company."""
```

```python
class BrandCreate(BrandBase):
    """Schema for creating a new Brand."""
```

```python
class BrandInDB(BrandBase):
    """Schema for Brand data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BrandUpdate(BaseModel):
    """Schema for updating an existing Brand.  All fields are optional to allow partial updates."""
```

```python
class DescriptionType(str, Enum):
    """Types of product descriptions.

Attributes: SHORT: Brief product description. LONG: Detailed product description. KEYWORDS: Keywords for search. SLANG: Colloquial terms for the product. NOTES: Internal notes about the product."""
```
*Class attributes:*
```python
SHORT = 'Short'
LONG = 'Long'
KEYWORDS = 'Keywords'
SLANG = 'Slang'
NOTES = 'Notes'
```

```python
class Fitment(FitmentInDB):
    """Schema for complete Fitment data in API responses."""
```

```python
class FitmentBase(BaseModel):
    """Base schema for Fitment data.

Attributes: year: Vehicle year. make: Vehicle make. model: Vehicle model. engine: Engine specification. transmission: Transmission specification. attributes: Additional fitment attributes."""
```
*Methods:*
```python
@field_validator('year')
@classmethod
    def validate_year(cls, v) -> int:
        """Validate vehicle year.

Args: v: The year to validate.

Returns: Validated year.

Raises: ValueError: If the year is outside valid range."""
```

```python
class FitmentCreate(FitmentBase):
    """Schema for creating a new Fitment."""
```

```python
class FitmentInDB(FitmentBase):
    """Schema for Fitment data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FitmentListResponse(PaginatedResponse):
    """Schema for paginated fitment response.  Overrides items type to be specifically List[Fitment]."""
```

```python
class FitmentUpdate(BaseModel):
    """Schema for updating an existing Fitment.  All fields are optional to allow partial updates."""
```
*Methods:*
```python
@field_validator('year')
@classmethod
    def validate_year(cls, v) -> Optional[int]:
        """Validate vehicle year if provided.

Args: v: The year to validate or None.

Returns: Validated year or None.

Raises: ValueError: If the year is outside valid range."""
```

```python
class MarketingType(str, Enum):
    """Types of product marketing content.

Attributes: BULLET_POINT: Bullet point features. AD_COPY: Advertising copy."""
```
*Class attributes:*
```python
BULLET_POINT = 'Bullet Point'
AD_COPY = 'Ad Copy'
```

```python
class PaginatedResponse(BaseModel):
    """Base schema for paginated responses.

Attributes: items: List of items. total: Total number of items. page: Current page number. page_size: Number of items per page. pages: Total number of pages."""
```

```python
class Product(ProductInDB):
    """Schema for complete Product data in API responses.

Includes related entities like descriptions, marketing, etc."""
```

```python
class ProductActivity(ProductActivityInDB):
    """Schema for complete ProductActivity data in API responses.

Includes related entities like user details."""
```

```python
class ProductActivityBase(BaseModel):
    """Base schema for ProductActivity data.

Attributes: status: Product status. reason: Reason for the status change."""
```

```python
class ProductActivityCreate(ProductActivityBase):
    """Schema for creating a new ProductActivity."""
```

```python
class ProductActivityInDB(ProductActivityBase):
    """Schema for ProductActivity data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductBase(BaseModel):
    """Base schema for Product data.

Attributes: part_number: Product part number. part_number_stripped: Normalized version of part number for searching. application: Product application or use case description. vintage: Whether the product is for vintage vehicles. late_model: Whether the product is for late model vehicles. soft: Whether the product is soft (e.g., fabric vs metal). universal: Whether the product is universal (fits multiple applications). is_active: Whether the product is active in the catalog."""
```
*Methods:*
```python
@model_validator(mode='after')
    def generate_part_number_stripped(self) -> 'ProductBase':
        """Generate normalized part number if not provided.  Returns: Self with normalized part number."""
```

```python
class ProductCreate(ProductBase):
    """Schema for creating a new Product.  Includes nested creation of related entities."""
```

```python
class ProductDescription(ProductDescriptionInDB):
    """Schema for complete ProductDescription data in API responses."""
```

```python
class ProductDescriptionBase(BaseModel):
    """Base schema for ProductDescription data.

Attributes: description_type: Type of description. description: The description text."""
```

```python
class ProductDescriptionCreate(ProductDescriptionBase):
    """Schema for creating a new ProductDescription."""
```

```python
class ProductDescriptionInDB(ProductDescriptionBase):
    """Schema for ProductDescription data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductDescriptionUpdate(BaseModel):
    """Schema for updating an existing ProductDescription.

All fields are optional to allow partial updates."""
```

```python
class ProductInDB(ProductBase):
    """Schema for Product data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductListResponse(PaginatedResponse):
    """Schema for paginated product response.  Overrides items type to be specifically List[Product]."""
```

```python
class ProductMarketing(ProductMarketingInDB):
    """Schema for complete ProductMarketing data in API responses."""
```

```python
class ProductMarketingBase(BaseModel):
    """Base schema for ProductMarketing data.

Attributes: marketing_type: Type of marketing content. content: The marketing content. position: Display order position."""
```

```python
class ProductMarketingCreate(ProductMarketingBase):
    """Schema for creating a new ProductMarketing."""
```

```python
class ProductMarketingInDB(ProductMarketingBase):
    """Schema for ProductMarketing data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductMarketingUpdate(BaseModel):
    """Schema for updating an existing ProductMarketing.

All fields are optional to allow partial updates."""
```

```python
class ProductMeasurement(ProductMeasurementInDB):
    """Schema for complete ProductMeasurement data in API responses.

Includes related entities like manufacturer details."""
```

```python
class ProductMeasurementBase(BaseModel):
    """Base schema for ProductMeasurement data.

Attributes: manufacturer_id: ID of the manufacturer. length: Length measurement. width: Width measurement. height: Height measurement. weight: Weight measurement. volume: Volume measurement. dimensional_weight: Dimensional weight for shipping calculations."""
```

```python
class ProductMeasurementCreate(ProductMeasurementBase):
    """Schema for creating a new ProductMeasurement."""
```

```python
class ProductMeasurementInDB(ProductMeasurementBase):
    """Schema for ProductMeasurement data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductMeasurementUpdate(ProductMeasurementBase):
    """Schema for updating an existing ProductMeasurement.

All fields are optional to allow partial updates."""
```

```python
class ProductStatus(str, Enum):
    """Product status values.

Attributes: ACTIVE: Product is active and available. INACTIVE: Product is temporarily inactive. DISCONTINUED: Product is permanently discontinued. OUT_OF_STOCK: Product is out of stock. PENDING: Product is pending approval or release."""
```
*Class attributes:*
```python
ACTIVE = 'active'
INACTIVE = 'inactive'
DISCONTINUED = 'discontinued'
OUT_OF_STOCK = 'out_of_stock'
PENDING = 'pending'
```

```python
class ProductStock(ProductStockInDB):
    """Schema for complete ProductStock data in API responses.

Includes related entities like warehouse details."""
```

```python
class ProductStockBase(BaseModel):
    """Base schema for ProductStock data.

Attributes: warehouse_id: ID of the warehouse. quantity: Stock quantity."""
```

```python
class ProductStockCreate(ProductStockBase):
    """Schema for creating new ProductStock."""
```

```python
class ProductStockInDB(ProductStockBase):
    """Schema for ProductStock data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductStockUpdate(BaseModel):
    """Schema for updating an existing ProductStock.  All fields are optional to allow partial updates."""
```

```python
class ProductSupersession(ProductSupersessionInDB):
    """Schema for complete ProductSupersession data in API responses.

Includes related entities like product details."""
```

```python
class ProductSupersessionBase(BaseModel):
    """Base schema for ProductSupersession data.

Attributes: old_product_id: ID of the product being replaced. new_product_id: ID of the replacement product. reason: Reason for the supersession."""
```

```python
class ProductSupersessionCreate(ProductSupersessionBase):
    """Schema for creating a new ProductSupersession."""
```

```python
class ProductSupersessionInDB(ProductSupersessionBase):
    """Schema for ProductSupersession data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductSupersessionUpdate(BaseModel):
    """Schema for updating an existing ProductSupersession.

All fields are optional to allow partial updates."""
```

```python
class ProductUpdate(BaseModel):
    """Schema for updating an existing Product.  All fields are optional to allow partial updates."""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/products/service.py`

**Imports:**
```python
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import get_dependency
from app.domains.products.models import Product
from app.domains.products.schemas import ProductCreate
```

**Classes:**
```python
class ProductService(object):
    """Service for product operations."""
```
*Methods:*
```python
    def __init__(self, db):
```
```python
    async def create_product(self, data) -> Product:
        """Create a new product."""
```
```python
    async def get_product(self, product_id) -> Product:
        """Get product by ID."""
```

##### Package: reference
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/reference`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/reference/__init__.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/reference/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.domains.products.models import ProductStock
from app.domains.location.models import Address
```

**Classes:**
```python
class Color(Base):
    """Color entity representing a product color.

Attributes: id: Unique identifier. name: Color name. hex_code: Hexadecimal color code. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'color'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Color instance.

Returns: String representation including name and hex code."""
```

```python
class ConstructionType(Base):
    """Construction type entity representing a product construction method.

Attributes: id: Unique identifier. name: Construction type name. description: Description of the construction type. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'construction_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of ConstructionType instance.

Returns: String representation including name."""
```

```python
class Hardware(Base):
    """Hardware item entity representing hardware used with products.

Attributes: id: Unique identifier. name: Hardware item name. description: Description of the hardware item. part_number: Manufacturer part number. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'hardware_item'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Hardware instance.  Returns: String representation including name."""
```

```python
class PackagingType(Base):
    """Packaging type entity representing a product packaging method.

Attributes: id: Unique identifier. pies_code: PIES standard code. name: Packaging type name. description: Description of the packaging type. source: Source of the packaging type data. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'packaging_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of PackagingType instance.

Returns: String representation including name."""
```

```python
class TariffCode(Base):
    """Tariff code entity representing a product tariff classification.

Attributes: id: Unique identifier. code: Tariff code number. description: Description of the tariff code. country_id: ID of the country this tariff applies to. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'tariff_code'
country =     country = relationship("Country", back_populates="tariff_codes")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of TariffCode instance.

Returns: String representation including code."""
```

```python
class Texture(Base):
    """Texture entity representing a product texture.

Attributes: id: Unique identifier. name: Texture name. description: Description of the texture. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'texture'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Texture instance.  Returns: String representation including name."""
```

```python
class UnspscCode(Base):
    """UNSPSC code entity for product classification.

Attributes: id: Unique identifier. code: UNSPSC code number. description: Description of the code. segment: Segment description. family: Family description. class_: Class description. commodity: Commodity description. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'unspsc_code'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of UnspscCode instance.

Returns: String representation including code and description."""
```

```python
class Warehouse(Base):
    """Warehouse entity representing a storage location.

Attributes: id: Unique identifier. name: Warehouse name. address_id: ID of the warehouse address. is_active: Whether the warehouse is active. created_at: Creation timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'warehouse'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of Warehouse instance.  Returns: String representation including name."""
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/reference/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.reference.models import Color, TariffCode, UnspscCode, Warehouse
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
```

**Classes:**
```python
class ColorRepository(BaseRepository[(Color, uuid.UUID)]):
    """Repository for Color entity operations.

Provides methods for querying, creating, updating, and deleting Color entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the color repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, color_id) -> Color:
        """Ensure a color exists by ID, raising an exception if not found.

Args: color_id: The color ID to check.

Returns: The color if found.

Raises: ResourceNotFoundException: If the color is not found."""
```
```python
    async def find_by_hex(self, hex_code) -> Optional[Color]:
        """Find a color by hex code.

Args: hex_code: The hex code to search for.

Returns: The color if found, None otherwise."""
```
```python
    async def find_by_name(self, name) -> Optional[Color]:
        """Find a color by name.

Args: name: The color name to search for.

Returns: The color if found, None otherwise."""
```

```python
class TariffCodeRepository(BaseRepository[(TariffCode, uuid.UUID)]):
    """Repository for TariffCode entity operations.

Provides methods for querying, creating, updating, and deleting TariffCode entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the tariff code repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, tariff_code_id) -> TariffCode:
        """Ensure a tariff code exists by ID, raising an exception if not found.

Args: tariff_code_id: The tariff code ID to check.

Returns: The tariff code if found.

Raises: ResourceNotFoundException: If the tariff code is not found."""
```
```python
    async def find_by_code(self, code) -> List[TariffCode]:
        """Find tariff codes by code string.

Args: code: The tariff code to search for.

Returns: List of matching tariff codes."""
```
```python
    async def get_by_country(self, country_id) -> List[TariffCode]:
        """Get tariff codes for a specific country.

Args: country_id: The country ID to filter by.

Returns: List of tariff codes for the country."""
```

```python
class UnspscCodeRepository(BaseRepository[(UnspscCode, uuid.UUID)]):
    """Repository for UnspscCode entity operations.

Provides methods for querying, creating, updating, and deleting UnspscCode entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the UNSPSC code repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, unspsc_code_id) -> UnspscCode:
        """Ensure a UNSPSC code exists by ID, raising an exception if not found.

Args: unspsc_code_id: The UNSPSC code ID to check.

Returns: The UNSPSC code if found.

Raises: ResourceNotFoundException: If the UNSPSC code is not found."""
```
```python
    async def find_by_code(self, code) -> Optional[UnspscCode]:
        """Find a UNSPSC code by exact code.

Args: code: The UNSPSC code to search for.

Returns: The UNSPSC code if found, None otherwise."""
```
```python
    async def find_by_description(self, description) -> List[UnspscCode]:
        """Find UNSPSC codes by description (partial match).

Args: description: The description text to search for.

Returns: List of UNSPSC codes with matching descriptions."""
```
```python
    async def find_by_segment(self, segment) -> List[UnspscCode]:
        """Find UNSPSC codes by segment.

Args: segment: The segment to filter by.

Returns: List of UNSPSC codes in the segment."""
```

```python
class WarehouseRepository(BaseRepository[(Warehouse, uuid.UUID)]):
    """Repository for Warehouse entity operations.

Provides methods for querying, creating, updating, and deleting Warehouse entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the warehouse repository.  Args: db: The database session."""
```
```python
    async def ensure_exists(self, warehouse_id) -> Warehouse:
        """Ensure a warehouse exists by ID, raising an exception if not found.

Args: warehouse_id: The warehouse ID to check.

Returns: The warehouse if found.

Raises: ResourceNotFoundException: If the warehouse is not found."""
```
```python
    async def find_by_name(self, name) -> Optional[Warehouse]:
        """Find a warehouse by name.

Args: name: The warehouse name to search for.

Returns: The warehouse if found, None otherwise."""
```
```python
    async def get_active_warehouses(self) -> List[Warehouse]:
        """Get all active warehouses.  Returns: List of active warehouses."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/reference/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

**Classes:**
```python
class Color(ColorInDB):
    """Schema for complete Color data in API responses."""
```

```python
class ColorBase(BaseModel):
    """Base schema for Color data.  Attributes: name: Color name. hex_code: Hexadecimal color code."""
```
*Methods:*
```python
@field_validator('hex_code')
@classmethod
    def validate_hex_code(cls, v) -> Optional[str]:
        """Validate hex code format.

Args: v: The hex code to validate or None.

Returns: Validated hex code or None.

Raises: ValueError: If the hex code format is invalid."""
```

```python
class ColorCreate(ColorBase):
    """Schema for creating a new Color."""
```

```python
class ColorInDB(ColorBase):
    """Schema for Color data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ColorUpdate(BaseModel):
    """Schema for updating an existing Color.  All fields are optional to allow partial updates."""
```
*Methods:*
```python
@field_validator('hex_code')
@classmethod
    def validate_hex_code(cls, v) -> Optional[str]:
        """Validate hex code format if provided.

Args: v: The hex code to validate or None.

Returns: Validated hex code or None.

Raises: ValueError: If the hex code format is invalid."""
```

```python
class ConstructionType(ConstructionTypeInDB):
    """Schema for complete ConstructionType data in API responses."""
```

```python
class ConstructionTypeBase(BaseModel):
    """Base schema for ConstructionType data.

Attributes: name: Construction type name. description: Description of the construction type."""
```

```python
class ConstructionTypeCreate(ConstructionTypeBase):
    """Schema for creating a new ConstructionType."""
```

```python
class ConstructionTypeInDB(ConstructionTypeBase):
    """Schema for ConstructionType data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ConstructionTypeUpdate(BaseModel):
    """Schema for updating an existing ConstructionType.

All fields are optional to allow partial updates."""
```

```python
class Hardware(HardwareInDB):
    """Schema for complete Hardware data in API responses."""
```

```python
class HardwareBase(BaseModel):
    """Base schema for Hardware data.

Attributes: name: Hardware item name. description: Description of the hardware item. part_number: Manufacturer part number."""
```

```python
class HardwareCreate(HardwareBase):
    """Schema for creating a new Hardware."""
```

```python
class HardwareInDB(HardwareBase):
    """Schema for Hardware data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class HardwareUpdate(BaseModel):
    """Schema for updating an existing Hardware.  All fields are optional to allow partial updates."""
```

```python
class PackagingType(PackagingTypeInDB):
    """Schema for complete PackagingType data in API responses."""
```

```python
class PackagingTypeBase(BaseModel):
    """Base schema for PackagingType data.

Attributes: name: Packaging type name. pies_code: PIES standard code. description: Description of the packaging type. source: Source of the packaging type data."""
```

```python
class PackagingTypeCreate(PackagingTypeBase):
    """Schema for creating a new PackagingType."""
```

```python
class PackagingTypeInDB(PackagingTypeBase):
    """Schema for PackagingType data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class PackagingTypeUpdate(BaseModel):
    """Schema for updating an existing PackagingType.  All fields are optional to allow partial updates."""
```

```python
class TariffCode(TariffCodeInDB):
    """Schema for complete TariffCode data in API responses.

Includes related entities like country details."""
```

```python
class TariffCodeBase(BaseModel):
    """Base schema for TariffCode data.

Attributes: code: Tariff code number. description: Description of the tariff code. country_id: ID of the country this tariff applies to."""
```

```python
class TariffCodeCreate(TariffCodeBase):
    """Schema for creating a new TariffCode."""
```

```python
class TariffCodeInDB(TariffCodeBase):
    """Schema for TariffCode data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class TariffCodeUpdate(BaseModel):
    """Schema for updating an existing TariffCode.  All fields are optional to allow partial updates."""
```

```python
class Texture(TextureInDB):
    """Schema for complete Texture data in API responses."""
```

```python
class TextureBase(BaseModel):
    """Base schema for Texture data.

Attributes: name: Texture name. description: Description of the texture."""
```

```python
class TextureCreate(TextureBase):
    """Schema for creating a new Texture."""
```

```python
class TextureInDB(TextureBase):
    """Schema for Texture data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class TextureUpdate(BaseModel):
    """Schema for updating an existing Texture.  All fields are optional to allow partial updates."""
```

```python
class UnspscCode(UnspscCodeInDB):
    """Schema for complete UnspscCode data in API responses."""
```

```python
class UnspscCodeBase(BaseModel):
    """Base schema for UnspscCode data.

Attributes: code: UNSPSC code number. description: Description of the code. segment: Segment description. family: Family description. class_: Class description. commodity: Commodity description."""
```

```python
class UnspscCodeCreate(UnspscCodeBase):
    """Schema for creating a new UnspscCode."""
```

```python
class UnspscCodeInDB(UnspscCodeBase):
    """Schema for UnspscCode data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class UnspscCodeUpdate(BaseModel):
    """Schema for updating an existing UnspscCode.  All fields are optional to allow partial updates."""
```

```python
class Warehouse(WarehouseInDB):
    """Schema for complete Warehouse data in API responses.

Includes related entities like address details."""
```

```python
class WarehouseBase(BaseModel):
    """Base schema for Warehouse data.

Attributes: name: Warehouse name. address_id: ID of the warehouse address. is_active: Whether the warehouse is active."""
```

```python
class WarehouseCreate(WarehouseBase):
    """Schema for creating a new Warehouse."""
```

```python
class WarehouseInDB(WarehouseBase):
    """Schema for Warehouse data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class WarehouseUpdate(BaseModel):
    """Schema for updating an existing Warehouse.  All fields are optional to allow partial updates."""
```

##### Package: security
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/security`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/security/__init__.py`

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/security/exceptions.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/security/models.py`

###### Module: passwords
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/security/passwords.py`

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/security/repository.py`

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/security/schemas.py`

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/security/service.py`

###### Module: tokens
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/security/tokens.py`

##### Package: sync_history
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/sync_history`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/sync_history/__init__.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/sync_history/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
```

**Classes:**
```python
class SyncEntityType(str, Enum):
    """Types of entities that can be synchronized."""
```
*Class attributes:*
```python
PRODUCT = 'product'
MEASUREMENT = 'measurement'
STOCK = 'stock'
PRICING = 'pricing'
MANUFACTURER = 'manufacturer'
CUSTOMER = 'customer'
ORDER = 'order'
```

```python
class SyncEvent(Base):
    """Events during synchronization operations."""
```
*Class attributes:*
```python
__tablename__ = 'sync_event'
```
*Methods:*
```python
    def __repr__(self) -> str:
```

```python
class SyncHistory(Base):
    """History of synchronization operations."""
```
*Class attributes:*
```python
__tablename__ = 'sync_history'
triggered_by =     triggered_by = relationship("User", foreign_keys=[triggered_by_id])
__table_args__ =     __table_args__ = (
        Index("ix_sync_history_status_started_at", status, started_at.desc()),
        Index("ix_sync_history_entity_source", entity_type, source),
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
```
```python
    def add_event(self, event_type, message, details) -> 'SyncEvent':
        """Add an event to this sync operation.

Args: event_type: Type of event message: Event message details: Additional details

Returns: Created event"""
```
```python
    def complete(self, status, records_processed, records_created, records_updated, records_failed, error_message, details) -> None:
        """Mark the sync as complete with results.

Args: status: Final status records_processed: Number of records processed records_created: Number of records created records_updated: Number of records updated records_failed: Number of records that failed error_message: Error message if any details: Additional details"""
```

```python
class SyncSource(str, Enum):
    """Source systems for synchronization."""
```
*Class attributes:*
```python
AS400 = 'as400'
FILEMAKER = 'filemaker'
API = 'api'
EXTERNAL = 'external'
```

```python
class SyncStatus(str, Enum):
    """Status of synchronization operations."""
```
*Class attributes:*
```python
PENDING = 'pending'
RUNNING = 'running'
COMPLETED = 'completed'
FAILED = 'failed'
CANCELLED = 'cancelled'
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/sync_history/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from sqlalchemy import select, desc, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.logging import get_logger
from app.domains.sync_history.models import SyncHistory, SyncEvent, SyncStatus, SyncEntityType, SyncSource
from app.repositories.base import BaseRepository
```

**Global Variables:**
```python
logger = logger = get_logger("app.repositories.sync_history_repository")
```

**Classes:**
```python
class SyncEventRepository(BaseRepository[(SyncEvent, uuid.UUID)]):
    """Repository for sync events."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the repository.  Args: db: SQLAlchemy async session"""
```
```python
    async def get_events_by_type(self, event_type, sync_id, limit) -> List[SyncEvent]:
        """Get events by type.

Args: event_type: Event type sync_id: Optional sync ID to filter by limit: Maximum number of events to return

Returns: List of sync events"""
```

```python
class SyncHistoryRepository(BaseRepository[(SyncHistory, uuid.UUID)]):
    """Repository for sync history records."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the repository.  Args: db: SQLAlchemy async session"""
```
```python
    async def add_sync_event(self, sync_id, event_type, message, details) -> SyncEvent:
        """Add an event to a sync operation.

Args: sync_id: ID of sync history record event_type: Type of event message: Event message details: Additional details

Returns: Created sync event

Raises: ResourceNotFoundException: If sync record not found"""
```
```python
    async def cancel_active_syncs(self, entity_type, source, cancelled_by_id) -> int:
        """Cancel active sync operations.

Args: entity_type: Filter by entity type source: Filter by source cancelled_by_id: ID of user cancelling the syncs

Returns: Number of syncs cancelled"""
```
```python
    async def create_sync(self, entity_type, source, triggered_by_id, details) -> SyncHistory:
        """Create a new sync history record.

Args: entity_type: Type of entity being synced source: Source system triggered_by_id: ID of user who triggered the sync details: Additional details

Returns: Created sync history record"""
```
```python
    async def get_active_syncs(self, entity_type, source) -> List[SyncHistory]:
        """Get currently active sync operations.

Args: entity_type: Filter by entity type source: Filter by source

Returns: List of active sync history records"""
```
```python
    async def get_latest_syncs(self, entity_type, source, status, limit) -> List[SyncHistory]:
        """Get the latest sync operations.

Args: entity_type: Filter by entity type source: Filter by source status: Filter by status limit: Maximum number of records to return

Returns: List of sync history records"""
```
```python
    async def get_sync_events(self, sync_id, limit) -> List[SyncEvent]:
        """Get events for a sync operation.

Args: sync_id: ID of sync history record limit: Maximum number of events to return

Returns: List of sync events"""
```
```python
    async def get_sync_stats(self, days, entity_type, source) -> Dict[(str, Any)]:
        """Get statistics for sync operations.

Args: days: Number of days to analyze entity_type: Filter by entity type source: Filter by source

Returns: Dictionary with sync statistics"""
```
```python
    async def update_sync_status(self, sync_id, status, records_processed, records_created, records_updated, records_failed, error_message, details) -> SyncHistory:
        """Update the status of a sync operation.

Args: sync_id: ID of sync history record status: New status records_processed: Number of records processed records_created: Number of records created records_updated: Number of records updated records_failed: Number of records failed error_message: Error message if any details: Additional details

Returns: Updated sync history record

Raises: ResourceNotFoundException: If sync record not found"""
```

##### Package: users
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/users`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/users/__init__.py`

###### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/users/exceptions.py`

###### Module: handlers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/users/handlers.py`

###### Module: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/users/models.py`

**Imports:**
```python
from __future__ import annotations
import uuid
import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from jose import jwt
from passlib.context import CryptContext
import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.core.config import settings
from app.db.base_class import Base
from app.domains.company.models import Company
from app.domains.api_key.models import ApiKey
from app.domains.media.models import Media
from app.domains.chat.models import ChatMember
```

**Global Variables:**
```python
pwd_context = pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**Functions:**
```python
def create_access_token(subject, role, expires_delta) -> str:
    """Create a JWT access token for a user.

Args: subject: The subject (user ID) for the token. role: The user's role. expires_delta: Optional custom expiration time delta.

Returns: The encoded JWT token string."""
```

```python
def get_password_hash(password) -> str:
    """Generate a hash from a plain-text password.

Args: password: The plain-text password to hash.

Returns: The hashed password."""
```

```python
def verify_password(plain_password, hashed_password) -> bool:
    """Verify if a plain password matches a hash.

Args: plain_password: The plain-text password to verify. hashed_password: The hashed password to compare against.

Returns: True if the password matches, False otherwise."""
```

**Classes:**
```python
class User(Base):
    """User entity representing a system user.

Attributes: id: Unique identifier. email: User's email address (unique). hashed_password: Securely hashed password. full_name: User's full name. role: User's role in the system. is_active: Whether the user account is active. company_id: ID of the associated company. created_at: Creation timestamp. updated_at: Last update timestamp."""
```
*Class attributes:*
```python
__tablename__ = 'user'
uploaded_media =     uploaded_media = relationship(
        "Media", foreign_keys="[Media.uploaded_by_id]", back_populates="uploaded_by"
    )
approved_media =     approved_media = relationship(
        "Media", foreign_keys="[Media.approved_by_id]", back_populates="approved_by"
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of User instance.

Returns: String representation including email and role."""
```

```python
class UserRole(str, Enum):
    """Enumeration of user roles in the system.

Attributes: ADMIN: Administrator role with full system access. MANAGER: Manager role with elevated permissions. CLIENT: Standard client user. DISTRIBUTOR: Distributor with specific permissions. READ_ONLY: User with read-only access."""
```
*Class attributes:*
```python
ADMIN = 'admin'
MANAGER = 'manager'
CLIENT = 'client'
DISTRIBUTOR = 'distributor'
READ_ONLY = 'read_only'
```

###### Module: repository
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/users/repository.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.users.models import User, UserRole
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, AuthenticationException
```

**Classes:**
```python
class UserRepository(BaseRepository[(User, uuid.UUID)]):
    """Repository for User entity operations.

Provides methods for querying, creating, updating, and deleting User entities, extending the generic BaseRepository."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the user repository.  Args: db: The database session."""
```
```python
    async def authenticate(self, email, password) -> User:
        """Authenticate a user by email and password.

Args: email: The user's email. password: The plaintext password.

Returns: The authenticated user.

Raises: AuthenticationException: If authentication fails."""
```
```python
    async def ensure_exists(self, user_id) -> User:
        """Ensure a user exists by ID, raising an exception if not found.

Args: user_id: The user ID to check.

Returns: The user if found.

Raises: ResourceNotFoundException: If the user is not found."""
```
```python
    async def find_by_email(self, email) -> Optional[User]:
        """Find a user by email address.

Args: email: The email address to search for.

Returns: The user if found, None otherwise."""
```
```python
    async def get_by_company(self, company_id, page, page_size) -> Dict[(str, Any)]:
        """Get paginated list of users for a specific company.

Args: company_id: The company ID to filter by. page: The page number. page_size: The number of items per page.

Returns: Dict containing items, total count, and pagination info."""
```
```python
    async def get_by_role(self, role) -> List[User]:
        """Get all users with a specific role.

Args: role: The role to filter by.

Returns: List of users with the specified role."""
```

###### Module: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/users/schemas.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.domains.company.schemas import Company
```

**Classes:**
```python
class Token(BaseModel):
    """Schema for authentication tokens.

Attributes: access_token: The JWT access token. token_type: The token type (typically "bearer")."""
```

```python
class TokenPayload(BaseModel):
    """Schema for JWT token payload.

Attributes: sub: Subject (typically user ID). exp: Expiration timestamp. role: User role. iat: Issued at timestamp."""
```

```python
class User(UserInDB):
    """Schema for complete user data in API responses.  Includes related entities like company details."""
```

```python
class UserBase(BaseModel):
    """Base schema for user data.

Attributes: email: User's email address. full_name: User's full name. role: User's role in the system. is_active: Whether the user account is active. company_id: ID of the associated company."""
```

```python
class UserCreate(UserBase):
    """Schema for creating a new user.

Extends UserBase to include password.

Attributes: password: User's plain-text password (will be hashed)."""
```
*Methods:*
```python
@field_validator('password')
@classmethod
    def password_strength(cls, v) -> str:
        """Validate password strength.

Args: v: The password to validate.

Returns: The password if valid.

Raises: ValueError: If the password doesn't meet strength requirements."""
```

```python
class UserInDB(UserBase):
    """Schema for user data as stored in the database.

Includes database-specific fields like ID and timestamps."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class UserRole(str, Enum):
    """Enumeration of user roles in the system.

Attributes: ADMIN: Administrator role with full system access. MANAGER: Manager role with elevated permissions. CLIENT: Standard client user. DISTRIBUTOR: Distributor with specific permissions. READ_ONLY: User with read-only access."""
```
*Class attributes:*
```python
ADMIN = 'admin'
MANAGER = 'manager'
CLIENT = 'client'
DISTRIBUTOR = 'distributor'
READ_ONLY = 'read_only'
```

```python
class UserUpdate(BaseModel):
    """Schema for updating an existing user.  All fields are optional to allow partial updates."""
```
*Methods:*
```python
@field_validator('password')
@classmethod
    def password_strength(cls, v) -> Optional[str]:
        """Validate password strength if provided.

Args: v: The password to validate or None.

Returns: The password if valid or None if not provided.

Raises: ValueError: If the password doesn't meet strength requirements."""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/domains/users/service.py`

#### Package: fitment
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/__init__.py`

##### Module: api
*API endpoints for fitment functionality.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/api.py`

**Imports:**
```python
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, Query, UploadFile, status
from pydantic import BaseModel, Field
from app.logging import get_logger
from app.domains.model_mapping.schemas import ModelMapping as ModelMappingSchema
from app.domains.model_mapping.schemas import ModelMappingCreate, ModelMappingUpdate
from exceptions import ConfigurationError, FitmentError
from mapper import FitmentMappingEngine
from models import ValidationStatus
```

**Global Variables:**
```python
logger = logger = get_logger("app.fitment.api")
router = router = APIRouter(prefix="/api/v1/fitment", tags=["fitment"])
```

**Functions:**
```python
@router.post('/model-mappings', response_model=ModelMappingSchema, status_code=status.HTTP_201_CREATED)
async def create_model_mapping(mapping_data, mapping_engine):
    """Create a new model mapping.

Args: mapping_data: Mapping data mapping_engine: Mapping engine instance

Returns: Created mapping

Raises: HTTPException: If creation fails"""
```

```python
@router.delete('/model-mappings/{mapping_id}', status_code=status.HTTP_200_OK)
async def delete_model_mapping(mapping_id, mapping_engine):
    """Delete a model mapping.

Args: mapping_id: ID of the mapping to delete mapping_engine: Mapping engine instance

Returns: Success message

Raises: HTTPException: If deletion fails"""
```

```python
def get_mapping_engine():
    """Get an instance of the mapping engine.

This is a FastAPI dependency for endpoints that need the mapping engine."""
```

```python
@router.get('/pcdb-positions/{terminology_id}', response_model=List[Dict[(str, Any)]])
async def get_pcdb_positions(terminology_id, mapping_engine):
    """Get PCDB positions for a part terminology.

Args: terminology_id: Part terminology ID mapping_engine: Mapping engine instance

Returns: List of PCDB positions

Raises: HTTPException: If retrieval fails"""
```

```python
@router.get('/model-mappings', response_model=ModelMappingsListResponse)
async def list_model_mappings(mapping_engine, skip, limit, pattern, sort_by, sort_order):
    """List model mappings from database.

Args: mapping_engine: Mapping engine instance skip: Number of items to skip (for pagination) limit: Maximum number of items to return (for pagination) pattern: Optional pattern to filter by sort_by: Field to sort by (pattern, mapping, priority, active) sort_order: Sort order (asc, desc)

Returns: List of model mappings with pagination information

Raises: HTTPException: If retrieval fails"""
```

```python
@router.post('/parse-application', response_model=Dict[(str, Any)])
async def parse_application(application_text, mapping_engine):
    """Parse a part application text.

Args: application_text: Raw part application text mapping_engine: Mapping engine instance

Returns: Parsed application components

Raises: HTTPException: If parsing fails"""
```

```python
@router.post('/process', response_model=ProcessFitmentResponse)
async def process_fitment(request, mapping_engine):
    """Process fitment application texts.

Args: request: Request body with application texts and part terminology ID mapping_engine: Mapping engine instance

Returns: Processing results

Raises: HTTPException: If processing fails"""
```

```python
@router.post('/refresh-mappings', status_code=status.HTTP_200_OK)
async def refresh_mappings(mapping_engine):
    """Refresh model mappings from the database.

This allows for updating mappings without restarting the server.

Args: mapping_engine: Mapping engine instance

Returns: Success message

Raises: HTTPException: If refresh fails"""
```

```python
@router.put('/model-mappings/{mapping_id}', response_model=ModelMappingSchema)
async def update_model_mapping(mapping_id, mapping_data, mapping_engine):
    """Update an existing model mapping.

Args: mapping_id: ID of the mapping to update mapping_data: Updated mapping data mapping_engine: Mapping engine instance

Returns: Updated mapping

Raises: HTTPException: If update fails"""
```

```python
@router.post('/upload-model-mappings', response_model=UploadModelMappingsResponse)
async def upload_model_mappings(file, mapping_engine):
    """Upload model mappings JSON file.

Args: file: JSON file with model mappings mapping_engine: Mapping engine instance

Returns: Upload result

Raises: HTTPException: If upload fails"""
```

**Classes:**
```python
class FitmentValidationResponse(BaseModel):
    """Response model for fitment validation results."""
```

```python
class ModelMappingRequest(BaseModel):
    """Request for creating or updating a model mapping."""
```

```python
class ModelMappingResponse(BaseModel):
    """Response for a model mapping."""
```

```python
class ModelMappingsListResponse(BaseModel):
    """Response for listing model mappings."""
```

```python
class ProcessFitmentRequest(BaseModel):
    """Request body for processing fitment applications."""
```

```python
class ProcessFitmentResponse(BaseModel):
    """Response body for processing fitment applications."""
```

```python
class UploadModelMappingsResponse(BaseModel):
    """Response for model mappings upload."""
```

##### Module: config
*Configuration for the fitment module.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/config.py`

**Imports:**
```python
from __future__ import annotations
import os
from functools import lru_cache
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Functions:**
```python
@lru_cache(maxsize=1)
def get_settings() -> FitmentSettings:
    """Get the fitment settings.  Returns: FitmentSettings instance"""
```

**Classes:**
```python
class FitmentSettings(BaseSettings):
    """Settings for the fitment module."""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_prefix="FITMENT_", case_sensitive=False, extra="ignore"
    )
```
*Methods:*
```python
@validator('vcdb_path', 'pcdb_path')
    def validate_file_path(self, v) -> str:
        """Validate that a file path exists."""
```
```python
@validator('model_mappings_path')
    def validate_optional_file_path(self, v) -> Optional[str]:
        """Validate that an optional file path exists if provided."""
```

##### Module: db
*Database access for fitment data.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/db.py`

**Imports:**
```python
from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple
import pyodbc
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.logging import get_logger
from exceptions import DatabaseError
from models import PCDBPosition, PartTerminology, VCDBVehicle
```

**Global Variables:**
```python
logger = logger = get_logger("app.fitment.db")
```

**Classes:**
```python
class AccessDBClient(object):
    """Client for Microsoft Access databases (VCDB and PCDB)."""
```
*Methods:*
```python
    def __init__(self, db_path) -> None:
        """Initialize the Access DB client.  Args: db_path: Path to the MS Access database file"""
```
```python
    def connect(self) -> pyodbc.Connection:
        """Connect to the Access database.

Returns: ODBC connection to the database

Raises: DatabaseError: If connection fails"""
```
```python
    def query(self, sql, params) -> List[Dict[(str, Any)]]:
        """Execute a SQL query on the Access database.

Args: sql: SQL query to execute params: Optional parameters for the query

Returns: List of dictionaries representing the query results

Raises: DatabaseError: If query execution fails"""
```

```python
class FitmentDBService(object):
    """Service for database operations related to fitment data."""
```
*Methods:*
```python
    def __init__(self, vcdb_path, pcdb_path, sqlalchemy_url) -> None:
        """Initialize the fitment database service.

Args: vcdb_path: Path to the VCDB MS Access database pcdb_path: Path to the PCDB MS Access database sqlalchemy_url: Optional SQLAlchemy URL for async database"""
```
```python
    async def add_model_mapping(self, pattern, mapping, priority) -> int:
        """Add a new model mapping to the database.

Args: pattern: Pattern to match in vehicle text mapping: Mapping string in format "Make|VehicleCode|Model" priority: Optional priority for matching (higher values are processed first)

Returns: ID of the new mapping

Raises: DatabaseError: If insert fails"""
```
```python
    async def delete_model_mapping(self, mapping_id) -> bool:
        """Delete a model mapping.

Args: mapping_id: ID of the mapping to delete

Returns: True if successful

Raises: DatabaseError: If delete fails"""
```
```python
    async def get_model_mappings(self) -> Dict[(str, List[str])]:
        """Get model mappings from the database.

Returns: Dictionary of model mappings where keys are patterns and values are lists of mapping strings

Raises: DatabaseError: If query fails"""
```
```python
    def get_pcdb_part_terminology(self, terminology_id) -> PartTerminology:
        """Get part terminology information from PCDB.

Args: terminology_id: ID of the part terminology

Returns: PartTerminology object

Raises: DatabaseError: If query fails or part terminology not found"""
```
```python
    def get_pcdb_positions(self, position_ids) -> List[PCDBPosition]:
        """Get position information from PCDB.

Args: position_ids: Optional list of position IDs to filter by

Returns: List of PCDBPosition objects

Raises: DatabaseError: If query fails"""
```
```python
@asynccontextmanager
    async def get_session(self) -> AsyncGenerator[(AsyncSession, None)]:
        """Get an async session for database operations.

Yields: AsyncSession object

Raises: DatabaseError: If async database is not configured"""
```
```python
    def get_vcdb_vehicles(self, year, make, model) -> List[VCDBVehicle]:
        """Get vehicles from VCDB matching the specified criteria.

Args: year: Optional year to filter by make: Optional make to filter by model: Optional model to filter by

Returns: List of VCDBVehicle objects

Raises: DatabaseError: If query fails"""
```
```python
    async def import_mappings_from_json(self, json_data) -> int:
        """Import mappings from a JSON dictionary.

Args: json_data: Dictionary where keys are patterns and values are lists of mappings

Returns: Number of mappings imported

Raises: DatabaseError: If import fails"""
```
```python
    def load_model_mappings_from_json(self, json_path) -> Dict[(str, List[str])]:
        """Load model mappings from a JSON file.

Args: json_path: Path to the JSON file

Returns: Dictionary of model mappings

Raises: DatabaseError: If loading fails"""
```
```python
    async def save_fitment_results(self, product_id, fitments) -> bool:
        """Save fitment results to the database.

Args: product_id: ID of the product fitments: List of fitment dictionaries

Returns: True if successful

Raises: DatabaseError: If saving fails"""
```
```python
    async def update_model_mapping(self, mapping_id, **kwargs) -> bool:
        """Update an existing model mapping.

Args: mapping_id: ID of the mapping to update **kwargs: Fields to update (pattern, mapping, priority, active)

Returns: True if successful

Raises: DatabaseError: If update fails"""
```

##### Module: dependencies
*Dependencies for the fitment module.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/dependencies.py`

**Imports:**
```python
from __future__ import annotations
import os
from functools import lru_cache
from app.core.config import settings as app_settings
from db import FitmentDBService
from exceptions import ConfigurationError
from mapper import FitmentMappingEngine
```

**Functions:**
```python
@lru_cache(maxsize=1)
def get_fitment_db_service() -> FitmentDBService:
    """Get a singleton instance of the FitmentDBService.

Returns: FitmentDBService instance

Raises: ConfigurationError: If required configuration is missing"""
```

```python
@lru_cache(maxsize=1)
def get_fitment_mapping_engine() -> FitmentMappingEngine:
    """Get a singleton instance of the FitmentMappingEngine.

Returns: FitmentMappingEngine instance

Raises: ConfigurationError: If required configuration is missing"""
```

```python
async def initialize_mapping_engine() -> None:
    """Initialize the mapping engine with database mappings.

This should be called during application startup."""
```

##### Module: exceptions
*Custom exceptions for the fitment module.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/exceptions.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Optional
```

**Classes:**
```python
class ConfigurationError(FitmentError):
    """Exception raised when configuration is invalid or missing."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize a configuration error.

Args: message: Error message details: Optional dictionary with additional error details"""
```

```python
class DatabaseError(FitmentError):
    """Exception raised when a database operation fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize a database error.

Args: message: Error message details: Optional dictionary with additional error details"""
```

```python
class FitmentError(Exception):
    """Base class for all fitment module exceptions."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize a fitment error.

Args: message: Error message details: Optional dictionary with additional error details"""
```

```python
class MappingError(FitmentError):
    """Exception raised when mapping a fitment fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize a mapping error.

Args: message: Error message details: Optional dictionary with additional error details"""
```

```python
class ParsingError(FitmentError):
    """Exception raised when parsing a fitment string fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize a parsing error.

Args: message: Error message details: Optional dictionary with additional error details"""
```

```python
class ValidationError(FitmentError):
    """Exception raised when validating a fitment fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """Initialize a validation error.

Args: message: Error message details: Optional dictionary with additional error details"""
```

##### Module: mapper
*Mapper for fitment data.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/mapper.py`

**Imports:**
```python
from __future__ import annotations
from functools import lru_cache
from typing import Any, Dict, List, Optional
from app.logging import get_logger
from db import FitmentDBService
from exceptions import MappingError
from models import PartTerminology, PCDBPosition, ValidationResult, ValidationStatus, VCDBVehicle
from parser import FitmentParser
from validator import FitmentValidator
```

**Global Variables:**
```python
logger = logger = get_logger("app.fitment.mapper")
```

**Classes:**
```python
class FitmentMappingEngine(object):
    """Engine for mapping fitment data to VCDB and PCDB records."""
```
*Methods:*
```python
    def __init__(self, db_service) -> None:
        """Initialize the mapping engine.  Args: db_service: Database service for fitment data"""
```
```python
    def batch_process_applications(self, application_texts, terminology_id) -> Dict[(str, List[ValidationResult])]:
        """Process a batch of part application strings.

Args: application_texts: List of raw part application texts terminology_id: ID of the part terminology

Returns: Dictionary mapping application text to validation results

Raises: MappingError: If processing fails"""
```
```python
    def configure(self, model_mappings_path) -> None:
        """Configure the mapping engine with model mappings.

Args: model_mappings_path: Path to the model mappings Excel file"""
```
```python
    async def configure_from_database(self) -> None:
        """Configure the mapping engine with model mappings from the database.

This allows for dynamic updates to mappings without server restarts."""
```
```python
    def configure_from_file(self, model_mappings_path) -> None:
        """Configure the mapping engine with model mappings from a file.

Args: model_mappings_path: Path to the model mappings JSON file"""
```
```python
@lru_cache(maxsize=100)
    def get_part_terminology(self, terminology_id) -> PartTerminology:
        """Get part terminology information by ID.

Args: terminology_id: ID of the part terminology

Returns: PartTerminology object

Raises: MappingError: If part terminology not found"""
```
```python
@lru_cache(maxsize=100)
    def get_pcdb_positions(self, terminology_id) -> List[PCDBPosition]:
        """Get PCDB positions for a part terminology.

Args: terminology_id: ID of the part terminology

Returns: List of PCDBPosition objects

Raises: MappingError: If positions not found"""
```
```python
    def get_vcdb_vehicles(self, year, make, model) -> List[VCDBVehicle]:
        """Get VCDB vehicles matching criteria.

Args: year: Optional year filter make: Optional make filter model: Optional model filter

Returns: List of VCDBVehicle objects

Raises: MappingError: If query fails"""
```
```python
    def process_application(self, application_text, terminology_id) -> List[ValidationResult]:
        """Process a part application string and validate against databases.

Args: application_text: Raw part application text terminology_id: ID of the part terminology

Returns: List of ValidationResult objects

Raises: MappingError: If processing fails"""
```
```python
    async def refresh_mappings(self) -> None:
        """Refresh model mappings from the database.

This allows for reloading mappings without restarting the server."""
```
```python
    async def save_mapping_results(self, product_id, results) -> bool:
        """Save mapping results to the database.

Args: product_id: ID of the product results: List of ValidationResult objects

Returns: True if successful

Raises: MappingError: If saving fails"""
```
```python
    def serialize_validation_results(self, results) -> List[Dict[(str, Any)]]:
        """Serialize validation results to JSON-compatible dictionaries.

Args: results: List of ValidationResult objects

Returns: List of dictionaries"""
```

##### Module: models
*Fitment data models for the Crown Nexus platform.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/models.py`

**Imports:**
```python
from __future__ import annotations
import re
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
```

**Classes:**
```python
class MappingRule(BaseModel):
    """Rule for mapping vehicle model text to structured data."""
```

```python
class ModelMapping(BaseModel):
    """Database model mapping rule."""
```
*Methods:*
```python
@property
    def make(self) -> str:
        """Extract make from mapping string."""
```
```python
@property
    def model(self) -> str:
        """Extract model from mapping string."""
```
```python
@property
    def vehicle_code(self) -> str:
        """Extract vehicle code from mapping string."""
```

```python
class PCDBPosition(BaseModel):
    """PCDB position information."""
```

```python
class PartApplication(BaseModel):
    """Raw part application string with parsing capabilities."""
```
*Methods:*
```python
@model_validator(mode='after')
    def parse_application(self) -> 'PartApplication':
        """Parse the raw application text into structured components."""
```

```python
class PartFitment(BaseModel):
    """Represents a vehicle fitment for a specific part."""
```

```python
class PartTerminology(BaseModel):
    """PCDB part terminology information."""
```

```python
class Position(str, Enum):
    """Automotive part position enumeration."""
```
*Class attributes:*
```python
FRONT = 'Front'
REAR = 'Rear'
LEFT = 'Left'
RIGHT = 'Right'
UPPER = 'Upper'
LOWER = 'Lower'
INNER = 'Inner'
OUTER = 'Outer'
CENTER = 'Center'
NA = 'N/A'
VARIES = 'Varies with Application'
```

```python
class PositionGroup(BaseModel):
    """Group of positions for a part."""
```

```python
class VCDBVehicle(BaseModel):
    """VCDB vehicle information."""
```

```python
class ValidationResult(BaseModel):
    """Result of validating a part fitment."""
```

```python
class ValidationStatus(Enum):
    """Status of a validation result."""
```
*Class attributes:*
```python
VALID =     VALID = auto()
WARNING =     WARNING = auto()
ERROR =     ERROR = auto()
```

```python
class Vehicle(BaseModel):
    """Vehicle information model."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(populate_by_name=True)
```
*Methods:*
```python
@property
    def full_name(self) -> str:
        """Generate a complete vehicle description."""
```

##### Module: parser
*Parser for fitment application strings.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/parser.py`

**Imports:**
```python
from __future__ import annotations
import re
from typing import Dict, List, Tuple
from exceptions import ParsingError
from models import PartApplication, PartFitment, Position, PositionGroup, Vehicle
```

**Classes:**
```python
class FitmentParser(object):
    """Parser for fitment strings with configurable rules."""
```
*Methods:*
```python
    def __init__(self, model_mappings) -> None:
        """Initialize the parser with model mappings.

Args: model_mappings: Dictionary mapping vehicle model text to structured make/model data"""
```
```python
    def expand_year_range(self, start_year, end_year) -> List[int]:
        """Expand a year range into a list of individual years.

Args: start_year: First year in range end_year: Last year in range

Returns: List of all years in the range (inclusive)"""
```
```python
    def extract_positions(self, position_text) -> List[PositionGroup]:
        """Extract position information from the position text.

Args: position_text: Text describing position (e.g., "Left or Right Front Upper")

Returns: List of PositionGroup objects representing all position combinations"""
```
```python
    def extract_year_range(self, year_text) -> Tuple[(int, int)]:
        """Extract start and end years from a year range string.

Args: year_text: Year range text (e.g., "2005-2010")

Returns: Tuple of (start_year, end_year)

Raises: ParsingError: If the year range cannot be parsed"""
```
```python
    def find_model_mapping(self, vehicle_text) -> List[Dict[(str, str)]]:
        """Find the appropriate model mapping for the vehicle text.

Args: vehicle_text: Text describing the vehicle model

Returns: List of dictionaries with make, model mappings

Raises: ParsingError: If no mapping is found"""
```
```python
    def parse_application(self, application_text) -> PartApplication:
        """Parse a raw part application text into a structured PartApplication object.

Args: application_text: Raw application text string

Returns: PartApplication with extracted components

Raises: ParsingError: If the application text cannot be parsed"""
```
```python
    def process_application(self, part_app) -> List[PartFitment]:
        """Process a part application into a list of specific part fitments.

Args: part_app: Parsed part application

Returns: List of expanded PartFitment objects

Raises: ParsingError: If processing fails"""
```

##### Module: validator
*Validator for fitment data.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/validator.py`

**Imports:**
```python
from __future__ import annotations
from app.logging import get_logger
from typing import Dict, List, Set
from models import PartFitment, PCDBPosition, Position, ValidationResult, ValidationStatus, VCDBVehicle
```

**Global Variables:**
```python
logger = logger = get_logger("app.fitment.validator")
```

**Classes:**
```python
class FitmentValidator(object):
    """Validator for fitment data against VCDB and PCDB databases."""
```
*Methods:*
```python
    def __init__(self, part_terminology_id, pcdb_positions) -> None:
        """Initialize the validator.

Args: part_terminology_id: ID of the part terminology pcdb_positions: List of valid PCDB positions for this part"""
```
```python
    def validate_fitment(self, fitment, available_vehicles) -> ValidationResult:
        """Validate a fitment against VCDB and PCDB data.

Args: fitment: The fitment to validate available_vehicles: List of available VCDB vehicles

Returns: ValidationResult with status and messages"""
```

#### Package: logging
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/logging`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/logging/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.logging.config import get_logger, initialize_logging, reinitialize_logging, shutdown_logging
from app.logging.context import clear_user_id, log_execution_time, log_execution_time_async, request_context, set_user_id
```

**Global Variables:**
```python
__all__ = __all__ = [
    "initialize_logging",
    "reinitialize_logging",
    "shutdown_logging",
    "get_logger",
    "request_context",
    "set_user_id",
    "clear_user_id",
    "log_execution_time",
    "log_execution_time_async",
]
```

##### Module: config
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/logging/config.py`

**Imports:**
```python
from __future__ import annotations
import datetime
import logging
import logging.config
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import pythonjsonlogger.jsonlogger as pythonjsonlogger
import structlog
from structlog.stdlib import BoundLogger, LoggerFactory
from structlog.types import EventDict, Processor, WrappedLogger
import threading
```

**Global Variables:**
```python
DEFAULT_LOG_LEVEL = 'INFO'
```

**Functions:**
```python
def add_request_id_processor(logger, method_name, event_dict) -> EventDict:
    """Add request ID to structured log event."""
```

```python
def add_service_info_processor(logger, method_name, event_dict) -> EventDict:
    """Add service information to structured log event."""
```

```python
def add_timestamp_processor(logger, method_name, event_dict) -> EventDict:
    """Add ISO format timestamp to structured log event."""
```

```python
def add_user_id_processor(logger, method_name, event_dict) -> EventDict:
    """Add user ID to structured log event."""
```

```python
def configure_std_logging() -> None:
    """Configure standard Python logging."""
```

```python
def configure_structlog() -> None:
    """Configure structlog for structured logging."""
```

```python
def get_environment() -> str:
    """Get the application environment with fallback logic.  Returns: The environment as a string"""
```

```python
def get_log_level() -> str:
    """Get the configured log level with fallback logic.

This isolates the settings dependency and provides a fallback.

Returns: The log level as a string"""
```

```python
def get_logger(name) -> BoundLogger:
    """Get a structured logger for the given name.

Args: name: The name for the logger

Returns: A structured logger instance"""
```

```python
def initialize_logging() -> None:
    """Initialize the logging system at import time."""
```

```python
async def reinitialize_logging() -> None:
    """Reinitialize the logging system asynchronously.

This can be called from the lifespan to update logging configuration or reload settings if needed."""
```

```python
async def shutdown_logging() -> None:
    """Shut down the logging system asynchronously."""
```

**Classes:**
```python
class ConsoleRendererWithLineNumbers(structlog.dev.ConsoleRenderer):
    """Custom renderer that includes line numbers in colorized output."""
```
*Methods:*
```python
    def __call__(self, logger, name, event_dict) -> str:
        """Format the event dict with line numbers included."""
```

```python
class RequestIdFilter(logging.Filter):
    """Filter for adding request ID to log records."""
```
*Methods:*
```python
    def filter(self, record) -> bool:
        """Add request ID to log record.

Args: record: The log record to process

Returns: bool: Always True to include the record"""
```

```python
class UserIdFilter(logging.Filter):
    """Filter for adding user ID to log records."""
```
*Methods:*
```python
    def filter(self, record) -> bool:
        """Add user ID to log record.

Args: record: The log record to process

Returns: bool: Always True to include the record"""
```

##### Module: context
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/logging/context.py`

**Imports:**
```python
from __future__ import annotations
import datetime
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, cast
import structlog
from structlog.stdlib import BoundLogger
from app.logging.config import _request_context, get_logger
```

**Global Variables:**
```python
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
```

**Functions:**
```python
def clear_user_id() -> None:
    """Clear the user ID from the current context."""
```

```python
def log_execution_time(logger, level):
    """Decorator to log function execution time.

Args: logger: Optional logger to use (defaults to module logger) level: Log level to use

Returns: Decorated function"""
```

```python
def log_execution_time_async(logger, level):
    """Decorator to log async function execution time.

Args: logger: Optional logger to use (defaults to module logger) level: Log level to use

Returns: Decorated async function"""
```

```python
@contextmanager
def request_context(request_id, user_id):
    """Context manager for tracking request information.

Args: request_id: Optional request ID (generated if not provided) user_id: Optional user ID

Yields: The request ID being used"""
```

```python
def set_user_id(user_id) -> None:
    """Set the user ID for the current context.  Args: user_id: The user ID to set"""
```

#### Package: middleware
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/middleware`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/middleware/__init__.py`

##### Module: error_handler
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/middleware/error_handler.py`

**Imports:**
```python
from __future__ import annotations
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.error import handle_exception
from app.core.exceptions import AppException, app_exception_handler, generic_exception_handler
from app.logging.context import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.middleware.error_handler")
```

**Classes:**
```python
class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling exceptions and converting them to standardized responses.

This middleware catches all exceptions, logs them, and passes them to the appropriate exception handler for creating consistent error responses."""
```
*Methods:*
```python
    async def dispatch(self, request, call_next) -> Response:
        """Process the request and handle any exceptions.

Args: request: The incoming request call_next: The next middleware in the chain

Returns: Either the response from downstream middleware or an error response"""
```

##### Module: logging
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/middleware/logging.py`

**Imports:**
```python
from __future__ import annotations
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.context import get_logger, request_context
```

**Global Variables:**
```python
logger = logger = get_logger("app.middleware.logging")
```

**Classes:**
```python
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and setting up request context.

This middleware generates a request ID for each incoming request, logs request and response information, and sets up the thread-local request context for use by other components."""
```
*Methods:*
```python
    def __init__(self, app):
        """Initialize the middleware.  Args: app: The FastAPI application"""
```
```python
    async def dispatch(self, request, call_next) -> Response:
        """Process the request, setting up context and logging information.

Args: request: The incoming request call_next: The next middleware in the chain

Returns: The response from downstream middleware"""
```

##### Module: metrics
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/middleware/metrics.py`

**Imports:**
```python
from __future__ import annotations
import time
from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Route, Match
from app.logging import get_logger
from app.core.metrics import track_request, set_gauge, MetricName, MetricTag
```

**Global Variables:**
```python
logger = logger = get_logger("app.middleware.metrics")
```

**Classes:**
```python
class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting request metrics.

Automatically tracks HTTP request metrics such as request count, duration, and errors."""
```
*Methods:*
```python
    def __init__(self, app) -> None:
        """Initialize the metrics middleware.  Args: app: FastAPI application"""
```
```python
    async def dispatch(self, request, call_next) -> Response:
```

##### Module: rate_limiting
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/middleware/rate_limiting.py`

**Imports:**
```python
from __future__ import annotations
import time
from typing import Any, Callable, Dict, List, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import RateLimitException
from app.logging import get_logger
from app.core.rate_limiting.limiter import RateLimiter
from app.core.rate_limiting.models import RateLimitRule
from app.core.rate_limiting.exceptions import RateLimitExceededException
from app.core.dependency_manager import get_dependency
```

**Global Variables:**
```python
logger = logger = get_logger("app.middleware.rate_limiting")
HAS_METRICS = False
```

**Classes:**
```python
class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware that applies rate limiting to incoming requests.

This middleware checks requests against configured rate limit rules and rejects requests that exceed the limits."""
```
*Methods:*
```python
    def __init__(self, app, rules, use_redis, enable_headers, block_exceeding_requests) -> None:
        """Initialize the rate limit middleware.

Args: app: The FastAPI application. rules: List of rate limit rules to apply. If None, a default rule will be used. use_redis: Whether to use Redis for rate limiting. enable_headers: Whether to include rate limit headers in responses. block_exceeding_requests: Whether to block requests that exceed the rate limit."""
```
```python
    async def dispatch(self, request, call_next) -> Response:
        """Process the request and apply rate limiting.

Args: request: The incoming request. call_next: The next middleware or route handler.

Returns: The response from the next middleware or route handler, or a 429 response if the rate limit is exceeded.

Raises: RateLimitException: If the rate limit is exceeded and block_exceeding_requests is True."""
```

##### Module: request_context
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/middleware/request_context.py`

**Imports:**
```python
from __future__ import annotations
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.context import get_logger, request_context
```

**Global Variables:**
```python
logger = logger = get_logger("app.middleware.request_context")
```

**Classes:**
```python
class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware for setting up request context and logging request information.

This middleware generates a request ID for each incoming request, logs request and response information, and sets up the thread-local request context for use by other components."""
```
*Methods:*
```python
    async def dispatch(self, request, call_next) -> Response:
        """Process the request, setting up context and logging information.

Args: request: The incoming request call_next: The next middleware in the chain

Returns: The response from downstream middleware"""
```

##### Module: response_formatter
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/middleware/response_formatter.py`

**Imports:**
```python
from __future__ import annotations
import datetime
import json
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.middleware.response_formatter")
```

**Classes:**
```python
class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    """Middleware for formatting API responses.

This middleware ensures all API responses follow a consistent format, with success flag, data, and metadata. It also adds timestamps and request IDs to responses."""
```
*Methods:*
```python
    async def dispatch(self, request, call_next) -> Response:
        """Process the request and format the response.

Args: request: FastAPI request call_next: Next middleware or route handler

Returns: Response: Formatted response"""
```

##### Module: security
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/middleware/security.py`

**Imports:**
```python
from __future__ import annotations
from typing import Callable, Optional
from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.exceptions import SecurityException
from app.logging.context import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.middleware.security")
```

**Classes:**
```python
class SecureRequestMiddleware(BaseHTTPMiddleware):
    """Middleware for blocking suspicious requests.

This middleware checks incoming requests for suspicious patterns and blocks them if detected."""
```
*Methods:*
```python
    def __init__(self, app, block_suspicious_requests) -> None:
        """Initialize the middleware.

Args: app: The FastAPI application block_suspicious_requests: Whether to block suspicious requests"""
```
```python
    async def dispatch(self, request, call_next) -> Response:
        """Process the request, checking for suspicious patterns.

Args: request: The incoming request call_next: The next middleware in the chain

Returns: The response if the request is not suspicious

Raises: SecurityException: If the request is suspicious and blocking is enabled"""
```

```python
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers to responses.

This middleware adds headers such as Content-Security-Policy, X-Frame-Options, and other security-related headers to responses."""
```
*Methods:*
```python
    def __init__(self, app, content_security_policy, permissions_policy, expect_ct) -> None:
        """Initialize the middleware.

Args: app: The FastAPI application content_security_policy: Optional CSP header value permissions_policy: Optional permissions policy header value expect_ct: Optional Expect-CT header value"""
```
```python
    async def dispatch(self, request, call_next) -> Response:
        """Process the request, adding security headers to the response.

Args: request: The incoming request call_next: The next middleware in the chain

Returns: The response with added security headers"""
```

#### Package: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models`

**__init__.py:**
*Models package.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/__init__.py`

##### Module: associations
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/associations.py`

**Imports:**
```python
from __future__ import annotations
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
```

**Global Variables:**
```python
product_fitment_association = product_fitment_association = Table(
    "product_fitment",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "fitment_id",
        UUID(as_uuid=True),
        ForeignKey("fitment.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)
product_media_association = product_media_association = Table(
    "product_media",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "media_id",
        UUID(as_uuid=True),
        ForeignKey("media.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("display_order", Integer, nullable=False, default=0),
    Column("is_primary", Integer, nullable=False, default=0),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)
product_tariff_code_association = product_tariff_code_association = Table(
    "product_tariff_code",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tariff_code_id",
        UUID(as_uuid=True),
        ForeignKey("tariff_code.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "assigned_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)
product_unspsc_association = product_unspsc_association = Table(
    "product_unspsc",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "unspsc_code_id",
        UUID(as_uuid=True),
        ForeignKey("unspsc_code.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "assigned_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)
product_country_origin_association = product_country_origin_association = Table(
    "product_country_origin",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "country_id",
        UUID(as_uuid=True),
        ForeignKey("country.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "manufacturer_id",
        UUID(as_uuid=True),
        ForeignKey("manufacturer.id", ondelete="SET NULL"),
        nullable=True,
    ),
    Column("origin_type", Integer, nullable=False, default=0),
    Column("origin_order", Integer, nullable=False, default=0),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint("product_id", "country_id", name="uix_product_country"),
)
product_hardware_association = product_hardware_association = Table(
    "product_hardware",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "hardware_id",
        UUID(as_uuid=True),
        ForeignKey("hardware_item.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("quantity", Integer, nullable=False, default=1),
    Column("is_optional", Integer, nullable=False, default=0),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint("product_id", "hardware_id", name="uix_product_hardware"),
)
product_interchange_association = product_interchange_association = Table(
    "product_interchange",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("interchange_number", Integer, nullable=False),
    Column(
        "brand_id",
        UUID(as_uuid=True),
        ForeignKey("brand.id", ondelete="SET NULL"),
        nullable=True,
    ),
    # CORRECTION: Changed from Integer to Text for notes
    Column("notes", Text, nullable=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint(
        "product_id", "interchange_number", "brand_id", name="uix_product_interchange"
    ),
)
product_packaging_association = product_packaging_association = Table(
    "product_packaging",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "packaging_type_id",
        UUID(as_uuid=True),
        ForeignKey("packaging_type.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)
product_color_association = product_color_association = Table(
    "product_color",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "color_id",
        UUID(as_uuid=True),
        ForeignKey("color.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)
product_construction_type_association = product_construction_type_association = Table(
    "product_construction_type",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "construction_type_id",
        UUID(as_uuid=True),
        ForeignKey("construction_type.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)
product_texture_association = product_texture_association = Table(
    "product_texture",
    Base.metadata,
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "texture_id",
        UUID(as_uuid=True),
        ForeignKey("texture.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
)
```

#### Package: repositories
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/repositories`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/repositories/__init__.py`

##### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/repositories/base.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseException
from app.logging import get_logger
from app.db.base_class import Base
from app.db.utils import bulk_create, count_query, create_object, delete_object, get_by_id, get_by_ids, paginate, update_object, upsert
```

**Global Variables:**
```python
logger = logger = get_logger("app.repositories.base")
T = T = TypeVar("T", bound=Base)
ID = ID = TypeVar("ID")
```

**Classes:**
```python
class BaseRepository(Generic[(T, ID)]):
    """Generic repository for database operations.

This class provides a standard interface for database operations, implementing the repository pattern for clean architecture.

Attributes: model: SQLAlchemy model class db: Database session"""
```
*Methods:*
```python
    def __init__(self, model, db) -> None:
        """Initialize the repository.  Args: model: SQLAlchemy model class db: Database session"""
```
```python
    async def bulk_create(self, items) -> List[T]:
        """Create multiple entities.

Args: items: List of entity data

Returns: List[T]: Created entities

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def count(self, filters) -> int:
        """Count entities matching filters.

Args: filters: Dictionary of field:value pairs for filtering

Returns: int: Count of matching entities

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def create(self, data) -> T:
        """Create a new entity.

Args: data: Entity data

Returns: T: Created entity

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def delete(self, id_value, user_id, hard_delete) -> bool:
        """Delete an entity.

Args: id_value: Entity ID user_id: ID of the user performing the deletion hard_delete: Whether to permanently delete

Returns: bool: True if deleted, False if not found

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def exists(self, filters) -> bool:
        """Check if an entity exists with the given filters.

Args: filters: Filters to apply

Returns: bool: True if entity exists

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def find_one_by(self, filters) -> Optional[T]:
        """Find a single entity by filters.

Args: filters: Filters to apply

Returns: Optional[T]: Entity or None if not found

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def get_all(self, page, page_size, order_by, filters) -> Dict[(str, Any)]:
        """Get all entities with pagination.

Args: page: Page number page_size: Page size order_by: Field to order by (prefix with - for descending) filters: Dictionary of field:value pairs for filtering

Returns: Dict[str, Any]: Paginated results

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def get_by_id(self, id_value) -> Optional[T]:
        """Get entity by ID.

Args: id_value: Entity ID

Returns: Optional[T]: Entity or None if not found

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def get_by_ids(self, ids) -> List[T]:
        """Get entities by IDs.

Args: ids: List of entity IDs

Returns: List[T]: List of found entities

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def update(self, id_value, data, user_id) -> Optional[T]:
        """Update an entity.

Args: id_value: Entity ID data: Updated data user_id: ID of the user making the update

Returns: Optional[T]: Updated entity or None if not found

Raises: DatabaseException: If a database error occurs"""
```
```python
    async def upsert(self, data, unique_fields) -> T:
        """Insert or update an entity based on unique fields.

Args: data: Entity data unique_fields: Fields to use for uniqueness check

Returns: T: Created or updated entity

Raises: DatabaseException: If a database error occurs"""
```

#### Package: schemas
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas/__init__.py`

#### Package: services
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/__init__.py`

##### Module: as400_sync_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/as400_sync_service.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config.integrations.as400 import as400_settings, get_as400_connector_config
from app.core.exceptions import ConfigurationException
from app.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
from app.data_import.pipeline.as400_pipeline import AS400Pipeline
from app.db.session import get_db_context
from app.domains.products.models import Product
from app.domains.reference.models import Warehouse
from app.domains.products.schemas import ProductCreate, ProductMeasurementCreate, ProductStock as ProductStockSchema
from app.data_import.processors.as400_processor import AS400ProcessorConfig, ProductAS400Processor
from app.data_import.importers.as400_importers import ProductAS400Importer, ProductMeasurementImporter, ProductStockImporter
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.as400_sync_service")
as400_sync_service = as400_sync_service = AS400SyncService.get_instance()
```

**Classes:**
```python
class AS400SyncService(object):
    """Service for managing AS400 data synchronization.

This service orchestrates the synchronization of data from AS400 to the application database, handling scheduling, execution, and monitoring."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the AS400 sync service."""
```
```python
@classmethod
    def get_instance(cls) -> AS400SyncService:
        """Get the singleton instance of AS400SyncService.  Returns: The singleton instance"""
```
```python
    async def get_sync_status(self, entity_type) -> Dict[(str, Any)]:
        """Get the status of all or a specific sync operation.

Args: entity_type: Optional entity type to get status for

Returns: Dictionary with sync status"""
```
```python
    async def initialize(self) -> None:
        """Initialize the sync service.  This method should be called during application startup."""
```
```python
    async def run_sync(self, entity_type, force) -> Dict[(str, Any)]:
        """Run a synchronization operation.

Args: entity_type: Type of entity to sync force: Whether to force sync regardless of schedule

Returns: Dictionary with sync results"""
```
```python
    async def schedule_sync(self, entity_type, delay_seconds) -> None:
        """Schedule a sync for a specific entity type.

Args: entity_type: Type of entity to sync delay_seconds: Delay before executing sync"""
```
```python
    async def shutdown(self) -> None:
        """Shut down the sync service.  This method should be called during application shutdown."""
```

```python
class SyncEntityType(str, Enum):
    """Types of entities that can be synchronized from AS400."""
```
*Class attributes:*
```python
PRODUCT = 'product'
MEASUREMENT = 'measurement'
STOCK = 'stock'
PRICING = 'pricing'
MANUFACTURER = 'manufacturer'
CUSTOMER = 'customer'
ORDER = 'order'
```

```python
class SyncLog(object):
    """Log entry for a synchronization operation."""
```
*Methods:*
```python
    def __init__(self, entity_type, status, records_processed, records_created, records_updated, records_failed, started_at, completed_at, error_message) -> None:
        """Initialize a sync log entry.

Args: entity_type: Type of entity being synchronized status: Current status of the sync records_processed: Number of records processed records_created: Number of records created records_updated: Number of records updated records_failed: Number of records that failed started_at: When the sync started completed_at: When the sync completed error_message: Error message if any"""
```
```python
    def complete(self, status, records_processed, records_created, records_updated, records_failed, error_message) -> None:
        """Mark the sync as complete.

Args: status: Final status records_processed: Number of records processed records_created: Number of records created records_updated: Number of records updated records_failed: Number of records that failed error_message: Error message if any"""
```

```python
class SyncStatus(str, Enum):
    """Status of synchronization operations."""
```
*Class attributes:*
```python
PENDING = 'pending'
RUNNING = 'running'
COMPLETED = 'completed'
FAILED = 'failed'
CANCELLED = 'cancelled'
```

##### Module: interfaces
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/interfaces.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar
```

**Global Variables:**
```python
T = T = TypeVar("T")  # Entity type
ID = ID = TypeVar("ID")  # ID type
C = C = TypeVar("C")  # Create schema type
U = U = TypeVar("U")  # Update schema type
R = R = TypeVar("R")  # Response schema type
```

**Classes:**
```python
class CrudServiceInterface(ServiceInterface[(T, ID)], Generic[(T, ID, C, U, R)]):
    """Extended interface for CRUD services with schema validation.

This interface extends the base service interface with methods that use Pydantic models for validation."""
```
*Methods:*
```python
    async def create_with_schema(self, schema, user_id) -> T:
        """Create a new entity using a Pydantic schema.

Args: schema: Create schema user_id: Optional user ID for permission checks

Returns: T: The created entity"""
```
```python
    async def to_response(self, entity) -> R:
        """Convert entity to response schema.  Args: entity: Entity to convert  Returns: R: Response schema"""
```
```python
    async def to_response_multi(self, entities) -> List[R]:
        """Convert entities to response schemas.

Args: entities: Entities to convert

Returns: List[R]: Response schemas"""
```
```python
    async def update_with_schema(self, id, schema, user_id) -> Optional[T]:
        """Update an existing entity using a Pydantic schema.

Args: id: Entity ID schema: Update schema user_id: Optional user ID for permission checks

Returns: Optional[T]: The updated entity if found, None otherwise"""
```

```python
class ReadOnlyServiceInterface(ServiceInterface[(T, ID)], Generic[(T, ID, R)]):
    """Interface for read-only services.

This interface provides only read operations, useful for services that don't need to modify data."""
```
*Methods:*
```python
    async def to_response(self, entity) -> R:
        """Convert entity to response schema.  Args: entity: Entity to convert  Returns: R: Response schema"""
```
```python
    async def to_response_multi(self, entities) -> List[R]:
        """Convert entities to response schemas.

Args: entities: Entities to convert

Returns: List[R]: Response schemas"""
```

```python
class ServiceInterface(Protocol, Generic[(T, ID)]):
    """Base protocol for all services.

This protocol defines the standard interface that all services must implement."""
```
*Methods:*
```python
    async def create(self, data, user_id) -> T:
        """Create a new entity.

Args: data: Entity data user_id: Optional user ID for permission checks

Returns: T: The created entity"""
```
```python
    async def delete(self, id, user_id) -> bool:
        """Delete an entity.

Args: id: Entity ID user_id: Optional user ID for permission checks

Returns: bool: True if the entity was deleted, False otherwise"""
```
```python
    async def get_all(self, page, page_size, filters, user_id) -> Dict[(str, Any)]:
        """Get all entities with pagination.

Args: page: Page number (1-indexed) page_size: Number of items per page filters: Optional filters to apply user_id: Optional user ID for permission checks

Returns: Dict[str, Any]: Paginated results"""
```
```python
    async def get_by_id(self, id, user_id) -> Optional[T]:
        """Get entity by ID.

Args: id: Entity ID user_id: Optional user ID for permission checks

Returns: Optional[T]: The entity if found, None otherwise"""
```
```python
    async def initialize(self) -> None:
        """Initialize service resources.

This method should be called during application startup to initialize any resources needed by the service."""
```
```python
    async def shutdown(self) -> None:
        """Release service resources.

This method should be called during application shutdown to release any resources held by the service."""
```
```python
    async def update(self, id, data, user_id) -> Optional[T]:
        """Update an existing entity.

Args: id: Entity ID data: Updated entity data user_id: Optional user ID for permission checks

Returns: Optional[T]: The updated entity if found, None otherwise"""
```

##### Module: test_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/test_service.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Generic, List, Optional, Type, TypeVar
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.test_service")
T = T = TypeVar("T")
```

**Classes:**
```python
class TestService(Generic[T]):
    """Service for test-related functionality.

This service provides methods for setting up and tearing down test data, creating test fixtures, and validating test results."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the test service."""
```
```python
    async def create_test_token(self, user_id, role, expires_in) -> str:
        """Create a test JWT token.

Args: user_id: User ID to include in the token role: User role to include in the token expires_in: Token expiration time in seconds

Returns: str: JWT token"""
```
```python
    async def setup_test_data(self, model_class, count) -> List[T]:
        """Set up test data for a model.

Args: model_class: Model class to create instances of count: Number of instances to create

Returns: List[T]: List of created model instances"""
```
```python
    async def teardown_test_data(self, model_class, instances) -> None:
        """Clean up test data.

Args: model_class: Model class of the instances instances: List of model instances to clean up"""
```
```python
    async def validate_test_result(self, actual, expected, ignore_fields) -> bool:
        """Validate that a test result matches the expected value.

Args: actual: Actual result from the test expected: Expected result ignore_fields: Fields to ignore during comparison

Returns: bool: True if the actual result matches the expected result"""
```

##### Module: vehicle
*Vehicle data service for managing vehicle information and fitment data.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/vehicle.py`

**Imports:**
```python
from __future__ import annotations
import re
from typing import Dict, List, Optional, Any
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.cache.decorators import cached
from app.core.exceptions import DatabaseException, ErrorCode, ValidationException
from app.logging import get_logger
from app.domains.products.models import Fitment
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.vehicle")
```

**Functions:**
```python
async def get_vehicle_service(db) -> VehicleDataService:
    """Dependency for getting the vehicle service.

Args: db: Database session.

Returns: VehicleDataService instance."""
```

**Classes:**
```python
class VehicleDataService(object):
    """Service for managing vehicle data and fitment information."""
```
*Methods:*
```python
    def __init__(self, db):
        """Initialize the vehicle data service.  Args: db: Database session for database operations."""
```
```python
@cached(ttl=86400, backend='redis')
    async def decode_vin(self, vin) -> Optional[Dict[(str, Any)]]:
        """Decode a Vehicle Identification Number (VIN).

Args: vin: The 17-character VIN to decode.

Returns: Dict containing vehicle information, or None if invalid VIN.

Raises: ValidationException: If the VIN format is invalid. ExternalServiceException: If an external VIN decoding service fails."""
```
```python
@cached(prefix='vehicle:engines', ttl=3600, backend='redis')
    async def get_engines(self, make, model, year) -> List[str]:
        """Get vehicle engines, optionally filtered by make, model, and/or year.

Args: make: Optional make filter. model: Optional model filter. year: Optional year filter.

Returns: List[str]: A list of engines in alphabetical order.

Raises: DatabaseException: If there's an error executing the database query."""
```
```python
@cached(ttl=3600, backend='redis', prefix='vehicle:makes')
    async def get_makes(self, year) -> List[str]:
        """Get vehicle makes, optionally filtered by year.

Args: year: Optional year filter.

Returns: List[str]: A list of makes in alphabetical order.

Raises: DatabaseException: If there's an error executing the database query."""
```
```python
@cached(prefix='vehicle:models', ttl=3600, backend='redis')
    async def get_models(self, make, year) -> List[str]:
        """Get vehicle models, optionally filtered by make and/or year.

Args: make: Optional make filter. year: Optional year filter.

Returns: List[str]: A list of models in alphabetical order.

Raises: DatabaseException: If there's an error executing the database query."""
```
```python
@cached(prefix='vehicle:transmissions', ttl=3600, backend='redis')
    async def get_transmissions(self, make, model, year, engine) -> List[str]:
        """Get vehicle transmissions, optionally filtered by make, model, year, and/or engine.

Args: make: Optional make filter. model: Optional model filter. year: Optional year filter. engine: Optional engine filter.

Returns: List[str]: A list of transmissions in alphabetical order.

Raises: DatabaseException: If there's an error executing the database query."""
```
```python
@cached(prefix='vehicle:years', ttl=3600, backend='redis')
    async def get_years(self) -> List[int]:
        """Get all available vehicle years.

Returns: List[int]: A list of years in descending order.

Raises: DatabaseException: If there's an error executing the database query."""
```
```python
@classmethod
    def register(cls) -> None:
        """Register this service with the service registry."""
```
```python
@cached(ttl=3600, backend='redis')
    async def standardize_make(self, make) -> str:
        """Standardize a vehicle make name.

Args: make: The make name to standardize.

Returns: Standardized make name."""
```
```python
@cached(ttl=3600, backend='redis')
    async def validate_fitment(self, year, make, model, engine, transmission) -> bool:
        """Validate if a specific vehicle fitment exists.

Args: year: Vehicle year. make: Vehicle make. model: Vehicle model. engine: Optional engine type. transmission: Optional transmission type.

Returns: bool: True if the fitment exists, False otherwise.

Raises: DatabaseException: If there's an error executing the database query."""
```

##### Package: base_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base_service`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base_service/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.services.base_service.contracts import BaseServiceProtocol
from app.services.base_service.permissions import PermissionHelper
from app.services.base_service.service import BaseService
```

**Global Variables:**
```python
__all__ = __all__ = ["BaseService", "BaseServiceProtocol", "PermissionHelper"]
```

###### Module: contracts
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base_service/contracts.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel
from app.db.base_class import Base
from app.services.interfaces import CrudServiceInterface
```

**Global Variables:**
```python
T = T = TypeVar("T", bound=Base)  # SQLAlchemy model type
C = C = TypeVar("C", bound=BaseModel)  # Create schema type
U = U = TypeVar("U", bound=BaseModel)  # Update schema type
R = R = TypeVar("R", bound=BaseModel)  # Response schema type
ID = ID = TypeVar("ID")  # ID type
```

**Classes:**
```python
class BaseServiceProtocol(CrudServiceInterface[(T, ID, C, U, R)], Generic[(T, ID, C, U, R)]):
    """Protocol defining the interface for base service functionality."""
```
*Methods:*
```python
    async def after_create(self, entity, user_id) -> None:
        """Hook after entity creation.  Args: entity: Created entity user_id: Current user ID"""
```
```python
    async def after_delete(self, entity, user_id) -> None:
        """Hook after entity deletion.  Args: entity: Deleted entity user_id: Current user ID"""
```
```python
    async def after_update(self, updated_entity, original_entity, user_id) -> None:
        """Hook after entity update.

Args: updated_entity: Updated entity original_entity: Original entity before update user_id: Current user ID"""
```
```python
    async def before_create(self, data, user_id) -> None:
        """Hook before entity creation.  Args: data: Entity data user_id: Current user ID"""
```
```python
    async def before_delete(self, entity, user_id) -> None:
        """Hook before entity deletion.  Args: entity: Entity to delete user_id: Current user ID"""
```
```python
    async def before_update(self, entity, data, user_id) -> None:
        """Hook before entity update.

Args: entity: Existing entity data: Updated data user_id: Current user ID"""
```
```python
    async def validate_create(self, data, user_id) -> None:
        """Validate data before creation.

Args: data: Entity data user_id: Current user ID

Raises: ValidationException: If validation fails"""
```
```python
    async def validate_delete(self, entity, user_id) -> None:
        """Validate before deletion.

Args: entity: Entity to delete user_id: Current user ID

Raises: ValidationException: If validation fails"""
```
```python
    async def validate_update(self, entity, data, user_id) -> None:
        """Validate data before update.

Args: entity: Existing entity data: Updated data user_id: Current user ID

Raises: ValidationException: If validation fails"""
```

###### Module: permissions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base_service/permissions.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Optional, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AuthenticationException, ErrorCode
from app.logging import get_logger
from app.domains.users.models import User
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.base_service.permissions")
```

**Classes:**
```python
class PermissionHelper(object):
    """Helper for permission-related operations."""
```
*Methods:*
```python
@staticmethod
    def check_owner_permission(user_id, entity_user_id, owner_field) -> bool:
        """Check if a user is the owner of an entity.

Args: user_id: User ID to check entity_user_id: User ID from the entity owner_field: Field name containing the owner ID

Returns: bool: True if user is the owner, False otherwise"""
```
```python
@staticmethod
    async def get_user(db, user_id) -> User:
        """Get user by ID.

Args: db: Database session user_id: User ID

Returns: User: User model

Raises: AuthenticationException: If user not found"""
```
```python
@staticmethod
    def has_all_permissions(user, permissions) -> bool:
        """Check if a user has all specified permissions.

Args: user: User to check permissions for permissions: List of permissions to check

Returns: bool: True if user has all permissions, False otherwise"""
```
```python
@staticmethod
    def has_any_permission(user, permissions) -> bool:
        """Check if a user has any of the specified permissions.

Args: user: User to check permissions for permissions: List of permissions to check

Returns: bool: True if user has any permission, False otherwise"""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base_service/service.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
from app.core.permissions import Permission
from app.db.base_class import Base
from app.repositories.base import BaseRepository
from app.schemas.pagination import CursorPaginationParams, OffsetPaginationParams, PaginationResult
from app.services.base_service.contracts import BaseServiceProtocol
from app.services.base_service.operations import CreateUpdateOperations, ReadDeleteOperations
from app.services.base_service.permissions import PermissionHelper
from app.services.pagination.service import PaginationService
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.base_service.service")
T = T = TypeVar("T", bound=Base)  # SQLAlchemy model type
C = C = TypeVar("C", bound=BaseModel)  # Create schema type
U = U = TypeVar("U", bound=BaseModel)  # Update schema type
R = R = TypeVar("R", bound=BaseModel)  # Response schema type
ID = ID = TypeVar("ID")  # ID type
```

**Classes:**
```python
class BaseService(Generic[(T, C, U, R, ID)], BaseServiceProtocol[(T, ID, C, U, R)]):
    """Base service for CRUD operations on entities.

This service provides standardized CRUD operations with: - Integrated permissions checking - Transaction management - Error handling - Validation - Event dispatching - Logging

Attributes: db: AsyncSession for database operations model: SQLAlchemy model class repository: Repository for database operations create_schema: Pydantic model for create operations update_schema: Pydantic model for update operations response_schema: Pydantic model for responses required_create_permission: Permission required for create operations required_read_permission: Permission required for read operations required_update_permission: Permission required for update operations required_delete_permission: Permission required for delete operations"""
```
*Methods:*
```python
    def __init__(self, db, model_class, create_schema, update_schema, response_schema, repository_class) -> None:
        """Initialize the service.

Args: db: Database session model_class: SQLAlchemy model class create_schema: Pydantic model for create operations update_schema: Pydantic model for update operations response_schema: Pydantic model for responses repository_class: Repository class for database operations"""
```
```python
    async def after_create(self, entity, user_id) -> None:
        """Hook after entity creation.  Args: entity: Created entity user_id: Current user ID"""
```
```python
    async def after_delete(self, entity, user_id) -> None:
        """Hook after entity deletion.  Args: entity: Deleted entity user_id: Current user ID"""
```
```python
    async def after_update(self, updated_entity, original_entity, user_id) -> None:
        """Hook after entity update.

Args: updated_entity: Updated entity original_entity: Original entity before update user_id: Current user ID"""
```
```python
    async def apply_filters(self, filters, user_id) -> Dict[(str, Any)]:
        """Apply custom filters based on business logic.

This method can be overridden in subclasses to add additional filters based on the user, entity type, or other business rules.

Args: filters: Base filters to apply user_id: Current user ID

Returns: Dict[str, Any]: Updated filters"""
```
```python
    async def before_create(self, data, user_id) -> None:
        """Hook before entity creation.  Args: data: Entity data user_id: Current user ID"""
```
```python
    async def before_delete(self, entity, user_id) -> None:
        """Hook before entity deletion.  Args: entity: Entity to delete user_id: Current user ID"""
```
```python
    async def before_update(self, entity, data, user_id) -> None:
        """Hook before entity update.

Args: entity: Existing entity data: Updated data user_id: Current user ID"""
```
```python
    async def create(self, data, user_id) -> T:
        """Create new entity.

Args: data: Entity data user_id: Current user ID

Returns: T: Created entity

Raises: ValidationException: If validation fails PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def create_with_schema(self, schema, user_id) -> T:
        """Create a new entity using a Pydantic schema.

Args: schema: Create schema user_id: Optional user ID for permission checks

Returns: T: The created entity"""
```
```python
    async def delete(self, id, user_id, hard_delete) -> bool:
        """Delete entity.

Args: id: Entity ID user_id: Current user ID hard_delete: Whether to permanently delete

Returns: bool: True if deleted

Raises: ResourceNotFoundException: If entity not found PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def get(self, id, user_id) -> T:
        """Get entity by ID with permission check.

Args: id: Entity ID user_id: Current user ID

Returns: T: Entity

Raises: ResourceNotFoundException: If entity not found PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def get_all(self, page, page_size, filters, user_id) -> Dict[(str, Any)]:
        """Get all entities with pagination.

Args: page: Page number (1-indexed) page_size: Number of items per page filters: Optional filters to apply user_id: Optional user ID for permission checks

Returns: Dict[str, Any]: Paginated results"""
```
```python
    async def get_by_id(self, id, user_id) -> Optional[T]:
        """Get entity by ID without raising exceptions.

Args: id: Entity ID user_id: Current user ID

Returns: Optional[T]: Entity or None if not found"""
```
```python
    async def get_multi(self, user_id, page, page_size, filters, order_by) -> Dict[(str, Any)]:
        """Get multiple entities with pagination.

Args: user_id: Current user ID page: Page number page_size: Items per page filters: Filters to apply order_by: Field to order by

Returns: Dict[str, Any]: Paginated results

Raises: PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def get_paginated(self, user_id, params, filters) -> PaginationResult[R]:
        """Get paginated entities using offset-based pagination.

Args: user_id: Current user ID params: Pagination parameters filters: Filters to apply

Returns: PaginationResult[R]: Paginated results

Raises: PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def get_paginated_with_cursor(self, user_id, params, filters) -> PaginationResult[R]:
        """Get paginated entities using cursor-based pagination.

Args: user_id: Current user ID params: Pagination parameters filters: Filters to apply

Returns: PaginationResult[R]: Paginated results

Raises: PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def initialize(self) -> None:
        """Initialize service resources."""
```
```python
    async def shutdown(self) -> None:
        """Release service resources."""
```
```python
    async def to_response(self, entity) -> R:
        """Convert entity to response model.  Args: entity: Entity to convert  Returns: R: Response model"""
```
```python
    async def to_response_multi(self, entities) -> List[R]:
        """Convert multiple entities to response models.

Args: entities: Entities to convert

Returns: List[R]: Response models"""
```
```python
    async def update(self, id, data, user_id) -> T:
        """Update entity.

Args: id: Entity ID data: Updated data user_id: Current user ID

Returns: T: Updated entity

Raises: ResourceNotFoundException: If entity not found ValidationException: If validation fails PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def update_with_schema(self, id, schema, user_id) -> Optional[T]:
        """Update an existing entity using a Pydantic schema.

Args: id: Entity ID schema: Update schema user_id: Optional user ID for permission checks

Returns: Optional[T]: The updated entity if found, None otherwise"""
```
```python
    async def validate_create(self, data, user_id) -> None:
        """Validate data before creation.

Args: data: Entity data user_id: Current user ID

Raises: ValidationException: If validation fails"""
```
```python
    async def validate_delete(self, entity, user_id) -> None:
        """Validate before deletion.

Args: entity: Entity to delete user_id: Current user ID

Raises: ValidationException: If validation fails"""
```
```python
    async def validate_update(self, entity, data, user_id) -> None:
        """Validate data before update.

Args: entity: Existing entity data: Updated data user_id: Current user ID

Raises: ValidationException: If validation fails"""
```

###### Package: operations
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base_service/operations`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base_service/operations/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.services.base_service.operations.create_update import CreateUpdateOperations
from app.services.base_service.operations.read_delete import ReadDeleteOperations
```

**Global Variables:**
```python
__all__ = __all__ = ["CreateUpdateOperations", "ReadDeleteOperations"]
```

####### Module: create_update
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base_service/operations/create_update.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ErrorCode, PermissionDeniedException, ResourceNotFoundException
from app.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import transactional
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.base_service.operations.create_update")
T = T = TypeVar("T", bound=Base)  # SQLAlchemy model type
C = C = TypeVar("C", bound=BaseModel)  # Create schema type
U = U = TypeVar("U", bound=BaseModel)  # Update schema type
ID = ID = TypeVar("ID")  # ID type
```

**Classes:**
```python
class CreateUpdateOperations(Generic[(T, C, U, ID)]):
    """Operations for creating and updating entities."""
```
*Methods:*
```python
@transactional
    async def create(self, db, repository, data, user_id, required_permission, validate_func, before_func, after_func, get_user_func) -> T:
        """Create new entity.

Args: db: Database session repository: Repository for database operations data: Entity data user_id: Current user ID required_permission: Required permission for this operation validate_func: Function for validating the data before_func: Function to call before creation after_func: Function to call after creation get_user_func: Function to get user by ID

Returns: T: Created entity

Raises: ValidationException: If validation fails PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def create_with_schema(self, db, repository, schema, user_id, required_permission, validate_func, before_func, after_func, get_user_func) -> T:
        """Create a new entity using a Pydantic schema.

Args: db: Database session repository: Repository for database operations schema: Create schema user_id: Optional user ID for permission checks required_permission: Required permission for this operation validate_func: Function for validating the data before_func: Function to call before creation after_func: Function to call after creation get_user_func: Function to get user by ID

Returns: T: The created entity"""
```
```python
@transactional
    async def update(self, db, repository, id, data, user_id, required_permission, validate_func, before_func, after_func, get_user_func) -> T:
        """Update entity.

Args: db: Database session repository: Repository for database operations id: Entity ID data: Updated data user_id: Current user ID required_permission: Required permission for this operation validate_func: Function for validating the data before_func: Function to call before update after_func: Function to call after update get_user_func: Function to get user by ID

Returns: T: Updated entity

Raises: ResourceNotFoundException: If entity not found ValidationException: If validation fails PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def update_with_schema(self, db, repository, id, schema, user_id, required_permission, validate_func, before_func, after_func, get_user_func) -> Optional[T]:
        """Update an existing entity using a Pydantic schema.

Args: db: Database session repository: Repository for database operations id: Entity ID schema: Update schema user_id: Optional user ID for permission checks required_permission: Required permission for this operation validate_func: Function for validating the data before_func: Function to call before update after_func: Function to call after update get_user_func: Function to get user by ID

Returns: Optional[T]: The updated entity if found, None otherwise"""
```

####### Module: read_delete
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base_service/operations/read_delete.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ErrorCode, PermissionDeniedException, ResourceNotFoundException
from app.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import transactional
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.base_service.operations.read_delete")
T = T = TypeVar("T", bound=Base)  # SQLAlchemy model type
R = R = TypeVar("R", bound=BaseModel)  # Response schema type
ID = ID = TypeVar("ID")  # ID type
```

**Classes:**
```python
class ReadDeleteOperations(Generic[(T, R, ID)]):
    """Operations for reading and deleting entities."""
```
*Methods:*
```python
@transactional
    async def delete(self, db, repository, id, user_id, hard_delete, required_permission, validate_func, before_func, after_func, get_user_func) -> bool:
        """Delete entity.

Args: db: Database session repository: Repository for database operations id: Entity ID user_id: Current user ID hard_delete: Whether to permanently delete required_permission: Required permission for this operation validate_func: Function for validating the deletion before_func: Function to call before deletion after_func: Function to call after deletion get_user_func: Function to get user by ID

Returns: bool: True if deleted

Raises: ResourceNotFoundException: If entity not found PermissionDeniedException: If user doesn't have permission"""
```
```python
@transactional
    async def get(self, db, repository, id, user_id, required_permission, get_user_func) -> T:
        """Get entity by ID with permission check.

Args: db: Database session repository: Repository for database operations id: Entity ID user_id: Current user ID required_permission: Required permission for this operation get_user_func: Function to get user by ID

Returns: T: Entity

Raises: ResourceNotFoundException: If entity not found PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def get_all(self, db, repository, page, page_size, filters, user_id, required_permission, get_user_func, apply_filters_func) -> Dict[(str, Any)]:
        """Get all entities with pagination.

Args: db: Database session repository: Repository for database operations page: Page number (1-indexed) page_size: Number of items per page filters: Optional filters to apply user_id: Optional user ID for permission checks required_permission: Required permission for this operation get_user_func: Function to get user by ID apply_filters_func: Function to apply custom filters

Returns: Dict[str, Any]: Paginated results"""
```
```python
    async def get_by_id(self, db, repository, id, user_id, required_permission, get_user_func) -> Optional[T]:
        """Get entity by ID without raising exceptions.

Args: db: Database session repository: Repository for database operations id: Entity ID user_id: Current user ID required_permission: Required permission for this operation get_user_func: Function to get user by ID

Returns: Optional[T]: Entity or None if not found"""
```
```python
@transactional
    async def get_multi(self, db, repository, user_id, page, page_size, filters, order_by, required_permission, get_user_func, apply_filters_func) -> Dict[(str, Any)]:
        """Get multiple entities with pagination.

Args: db: Database session repository: Repository for database operations user_id: Current user ID page: Page number page_size: Items per page filters: Filters to apply order_by: Field to order by required_permission: Required permission for this operation get_user_func: Function to get user by ID apply_filters_func: Function to apply custom filters

Returns: Dict[str, Any]: Paginated results

Raises: PermissionDeniedException: If user doesn't have permission"""
```
```python
    async def to_response(self, entity, response_model) -> R:
        """Convert entity to response model.

Args: entity: Entity to convert response_model: Response model class

Returns: R: Response model"""
```
```python
    async def to_response_multi(self, entities, response_model) -> List[R]:
        """Convert multiple entities to response models.

Args: entities: Entities to convert response_model: Response model class

Returns: List[R]: Response models"""
```

##### Package: search
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.services.search.service import SearchService
```

**Global Variables:**
```python
__all__ = __all__ = ["get_search_service", "SearchService"]
```

**Functions:**
```python
def get_search_service(db):
    """Factory function to get SearchService  Args: db: Database session  Returns: SearchService instance"""
```

###### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search/base.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Optional, Protocol, TypeVar
```

**Global Variables:**
```python
T = T = TypeVar("T")  # Entity type
```

**Classes:**
```python
class SearchProvider(Protocol):
    """Protocol for search providers."""
```
*Methods:*
```python
    async def initialize(self) -> None:
        """Initialize the search provider."""
```
```python
    async def search(self, search_term, filters, page, page_size, **kwargs) -> Dict[(str, Any)]:
        """Search for entities matching the criteria.

Args: search_term: Text to search for filters: Filters to apply page: Page number (1-indexed) page_size: Number of items per page **kwargs: Additional search parameters

Returns: Dict containing search results and pagination info"""
```
```python
    async def shutdown(self) -> None:
        """Shutdown the search provider."""
```

```python
class SearchResult(Dict[(str, Any)]):
    """Type for search results."""
```

###### Module: factory
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search/factory.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.core.config import settings
from app.logging import get_logger
from app.domains.products.models import Fitment, Product
from app.services.search.base import SearchProvider
from app.services.search.providers import DatabaseSearchProvider, ElasticsearchSearchProvider
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.search.factory")
```

**Classes:**
```python
class SearchProviderFactory(object):
    """Factory for creating search provider instances."""
```
*Methods:*
```python
@classmethod
    async def create_default_provider(cls, db, model_class) -> SearchProvider:
        """Create the default search provider for a model.

Args: db: Database session model_class: SQLAlchemy model class to search

Returns: SearchProvider: The default provider for the model"""
```
```python
@classmethod
    async def create_provider(cls, provider_type, db, model_class, **kwargs) -> SearchProvider:
        """Create a search provider of the specified type.

Args: provider_type: The type of provider to create ('database', 'elasticsearch') db: Database session model_class: SQLAlchemy model class to search **kwargs: Additional provider configuration

Returns: SearchProvider: The created provider

Raises: ValueError: If provider type is unsupported"""
```
```python
@classmethod
    async def shutdown_all(cls) -> None:
        """Shutdown all cached providers."""
```

###### Module: service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search/service.py`

**Imports:**
```python
from __future__ import annotations
from app.core.cache.decorators import cached
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import get_dependency
from app.core.exceptions import DatabaseException, ErrorCode
from app.logging import get_logger
from app.domains.products.models import Fitment, Product
from app.services.interfaces import ServiceInterface
from app.services.search.factory import SearchProviderFactory
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.search.service")
```

**Classes:**
```python
class SearchService(ServiceInterface):
    """Service for searching various entity types."""
```
*Methods:*
```python
    def __init__(self, db) -> None:
        """Initialize the search service.  Args: db: Database session"""
```
```python
    async def global_search(self, search_term, entity_types, page, page_size) -> Dict[(str, Any)]:
        """Search across multiple entity types.

Args: search_term: Text to search for entity_types: Types of entities to search page: Page number for pagination page_size: Items per page

Returns: Dict containing search results for each entity type"""
```
```python
    async def initialize(self) -> None:
        """Initialize the search service."""
```
```python
@cached(prefix='search:fitments', ttl=300, backend='redis')
    async def search_fitments(self, search_term, year, make, model, engine, transmission, page, page_size, use_elasticsearch) -> Dict[(str, Any)]:
        """Search for fitments matching the given criteria.

Args: search_term: Text to search for year: Filter by year make: Filter by make model: Filter by model engine: Filter by engine transmission: Filter by transmission page: Page number for pagination page_size: Items per page use_elasticsearch: Whether to use Elasticsearch or database search

Returns: Dict containing search results and pagination info

Raises: DatabaseException: If the search operation fails"""
```
```python
@cached(prefix='search:products', ttl=300, backend='redis')
    async def search_products(self, search_term, attributes, is_active, page, page_size, use_elasticsearch) -> Dict[(str, Any)]:
        """Search for products matching the given criteria.

Args: search_term: Text to search for in product name, description, etc. attributes: Product attributes to filter by is_active: Filter by active status page: Page number for pagination page_size: Items per page use_elasticsearch: Whether to use Elasticsearch or database search

Returns: Dict containing search results and pagination info

Raises: DatabaseException: If the search operation fails"""
```
```python
    async def shutdown(self) -> None:
        """Shutdown the search service."""
```

###### Package: providers
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search/providers`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search/providers/__init__.py`

**Imports:**
```python
from __future__ import annotations
from app.services.search.providers.database import DatabaseSearchProvider
from app.services.search.providers.elasticsearch import ElasticsearchSearchProvider
```

**Global Variables:**
```python
__all__ = __all__ = ["DatabaseSearchProvider", "ElasticsearchSearchProvider"]
```

####### Module: database
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search/providers/database.py`

**Imports:**
```python
from __future__ import annotations
from app.core.pagination import paginate_with_offset, OffsetPaginationParams
from typing import Any, Dict, List, Optional, Type, cast
from sqlalchemy import func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.core.exceptions import DatabaseException, ErrorCode
from app.logging import get_logger
from app.domains.products.models import Fitment, Product
from app.services.search.base import SearchProvider, SearchResult
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.search.providers.database")
```

**Classes:**
```python
class DatabaseSearchProvider(SearchProvider):
    """Search provider that queries the database directly."""
```
*Methods:*
```python
    def __init__(self, db, model_class) -> None:
        """Initialize the database search provider.

Args: db: Database session model_class: SQLAlchemy model class to search"""
```
```python
    async def initialize(self) -> None:
        """Initialize the database search provider."""
```
```python
    async def search(self, search_term, filters, page, page_size, **kwargs) -> SearchResult:
        """Search for entities in the database.

Args: search_term: Text to search for filters: Filters to apply page: Page number (1-indexed) page_size: Number of items per page **kwargs: Additional search parameters

Returns: Dict containing search results and pagination info

Raises: DatabaseException: If the database search fails"""
```
```python
    async def shutdown(self) -> None:
        """Shutdown the database search provider."""
```

####### Module: elasticsearch
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search/providers/elasticsearch.py`

**Imports:**
```python
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, Type
from elasticsearch import AsyncElasticsearch
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from app.core.config import settings
from app.core.exceptions import DatabaseException, ErrorCode, ServiceException
from app.logging import get_logger
from app.services.search.base import SearchProvider, SearchResult
from app.utils.retry import async_retry_on_network_errors
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.search.providers.elasticsearch")
```

**Classes:**
```python
class ElasticsearchSearchProvider(SearchProvider):
    """Search provider that uses Elasticsearch."""
```
*Methods:*
```python
    def __init__(self, db, model_class, index_name) -> None:
        """Initialize the Elasticsearch search provider.

Args: db: Database session model_class: SQLAlchemy model class to search index_name: Elasticsearch index name (defaults to lowercase model name)"""
```
```python
    async def initialize(self) -> None:
        """Initialize the Elasticsearch search provider."""
```
```python
@async_retry_on_network_errors(retries=2, delay=0.5)
    async def search(self, search_term, filters, page, page_size, **kwargs) -> SearchResult:
        """Search for entities using Elasticsearch.

Args: search_term: Text to search for filters: Filters to apply page: Page number (1-indexed) page_size: Number of items per page **kwargs: Additional search parameters

Returns: Dict containing search results and pagination info

Raises: ServiceException: If the Elasticsearch query fails DatabaseException: If fetching entities from database fails"""
```
```python
    async def shutdown(self) -> None:
        """Shutdown the Elasticsearch search provider."""
```

#### Package: tasks
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/tasks`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/tasks/__init__.py`

#### Package: utils
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/__init__.py`

##### Module: circuit_breaker
*Circuit breaker implementation for preventing cascading failures.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/circuit_breaker.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import enum
import functools
import time
from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, cast
from app.core.exceptions import ServiceException, ErrorCode
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.utils.circuit_breaker")
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
```

**Functions:**
```python
def circuit_breaker(name, failure_threshold, success_threshold, timeout, exception_types, fallback) -> Callable[([F], F)]:
    """Decorator factory for applying circuit breaker pattern.

Args: name: Unique name for the circuit breaker failure_threshold: Number of failures before opening circuit success_threshold: Number of successes before closing circuit timeout: Seconds before trying again after circuit opens exception_types: List of exception types to count as failures fallback: Function to call when circuit is open

Returns: Callable: Decorator function

Examples: @circuit_breaker("payment_service", failure_threshold=3) def process_payment(order_id): ...

@circuit_breaker("user_service", fallback=get_cached_user) async def get_user(user_id): ..."""
```

**Classes:**
```python
class CircuitBreaker(object):
    """Circuit breaker implementation to prevent cascading failures."""
```
*Methods:*
```python
    def __call__(self, func) -> F:
        """Decorate function with circuit breaker (synchronous version).

Args: func: The function to wrap with circuit breaker

Returns: F: Wrapped function"""
```
```python
    def __init__(self, name, config) -> None:
        """Initialize a new circuit breaker.

Args: name: Unique name for this circuit breaker config: Configuration options, or None for defaults"""
```
```python
    def async_call(self, func) -> F:
        """Decorate async function with circuit breaker.

Args: func: The async function to wrap with circuit breaker

Returns: F: Wrapped async function"""
```
```python
    def check_state(self) -> None:
        """Check if circuit state should change based on time elapsed.

If in OPEN state and timeout has elapsed, transitions to HALF_OPEN."""
```
```python
@classmethod
    def get(cls, name) -> CircuitBreaker:
        """Get an existing circuit breaker by name.

Args: name: Name of the circuit breaker

Returns: CircuitBreaker: The named circuit breaker

Raises: ValueError: If no circuit breaker with that name exists"""
```
```python
@classmethod
    def get_all_states(cls) -> Dict[(str, CircuitState)]:
        """Get the current state of all circuit breakers.

Returns: Dict[str, CircuitState]: Map of circuit breaker names to states"""
```
```python
@classmethod
    def get_or_create(cls, name, config) -> CircuitBreaker:
        """Get an existing circuit breaker or create a new one.

Args: name: Name of the circuit breaker config: Configuration options for new breaker, or None for defaults

Returns: CircuitBreaker: The named circuit breaker"""
```
```python
    def reset(self) -> None:
        """Reset this circuit breaker to CLOSED state."""
```
```python
@classmethod
    def reset_all(cls) -> None:
        """Reset all circuit breakers to CLOSED state."""
```

```python
@dataclass
class CircuitBreakerConfig(object):
    """Configuration options for circuit breaker behavior."""
```

```python
class CircuitState(enum.Enum):
    """Possible states of a circuit breaker."""
```
*Class attributes:*
```python
CLOSED = 'closed'
OPEN = 'open'
HALF_OPEN = 'half_open'
```

##### Module: crypto
*Cryptography utility module for handling secure encryption, decryption, and token generation.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/crypto.py`

**Imports:**
```python
from __future__ import annotations
import base64
import os
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings
from app.core.exceptions import ConfigurationException, SecurityException, ErrorCode
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.utils.crypto")
```

**Functions:**
```python
def decrypt_message(encrypted_message) -> str:
    """Decrypt a Fernet-encrypted message.

Args: encrypted_message: Base64-encoded encrypted message

Returns: str: Decrypted plaintext message

Raises: CryptoError: If decryption fails or token is invalid"""
```

```python
def encrypt_message(message) -> str:
    """Encrypt a message using Fernet symmetric encryption.

Args: message: Plaintext message to encrypt

Returns: str: Base64-encoded encrypted message

Raises: CryptoError: If encryption fails"""
```

```python
def generate_secure_token(length) -> str:
    """Generate a cryptographically secure random token.

Args: length: Length of the token in bytes (resulting hex string will be twice this length)

Returns: str: Hexadecimal string representation of the random token

Raises: CryptoError: If token generation fails ValueError: If length is less than 16"""
```

**Classes:**
```python
class CryptoError(SecurityException):
    """Exception raised for cryptographic operations failures."""
```
*Methods:*
```python
    def __init__(self, message, code, details, original_exception) -> None:
        """Initialize CryptoError.

Args: message: Human-readable error description code: Error code from ErrorCode enum details: Additional error context original_exception: Original exception that caused this error"""
```

##### Module: file
*File handling utilities for secure file operations and validation.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/file.py`

**Imports:**
```python
from __future__ import annotations
import os
import secrets
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Protocol, Set, Tuple, Union
from PIL import Image, UnidentifiedImageError
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings
from app.core.exceptions import ErrorCode, SecurityException, ValidationException
from app.logging import get_logger
from app.domains.media.models import MediaType
```

**Global Variables:**
```python
logger = logger = get_logger("app.utils.file")
MediaConstraints = MediaConstraints = Dict[MediaType, Set[str]]
SizeConstraints = SizeConstraints = Dict[MediaType, int]
DimensionsTuple = DimensionsTuple = Tuple[int, int]
```

**Functions:**
```python
def get_file_extension(filename) -> str:
    """Extract file extension from filename.

Args: filename: Name of the file

Returns: str: Extension without dot or empty string if none"""
```

```python
def get_file_path(file_path) -> Path:
    """Convert URL or relative path to absolute file path.

Args: file_path: URL, absolute, or relative file path

Returns: Path: Absolute path to the file"""
```

```python
def get_file_url(file_path) -> str:
    """Get public URL for a file path.

Args: file_path: Path to the file

Returns: str: URL to access the file"""
```

```python
def get_media_type_from_mime(mime_type) -> MediaType:
    """Determine media type from MIME type.

Args: mime_type: MIME type string (e.g., 'image/jpeg')

Returns: MediaType: Appropriate MediaType enum value"""
```

```python
def get_thumbnail_path(file_path) -> Optional[Path]:
    """Get thumbnail path for a given file path.

Args: file_path: Path to the original file

Returns: Optional[Path]: Path to thumbnail if exists, None otherwise"""
```

```python
def is_safe_filename(filename) -> bool:
    """Check if filename is safe (no path traversal).

Args: filename: Name of the file to check

Returns: bool: True if filename is safe, False otherwise"""
```

```python
def sanitize_filename(filename) -> str:
    """Sanitize filename to remove unsafe characters.

Args: filename: Original filename

Returns: str: Sanitized filename"""
```

```python
def save_upload_file(file, media_id, media_type, is_image) -> Tuple[(str, int, str)]:
    """Save uploaded file to disk with secure naming.

Args: file: FastAPI UploadFile object media_id: UUID for the media record media_type: MediaType enum value is_image: Whether the file is an image

Returns: Tuple containing: - str: Relative path to saved file - int: File size in bytes - str: Generated media hash

Raises: HTTPException: If file saving fails"""
```

```python
def validate_file(file, allowed_types) -> Tuple[(MediaType, bool)]:
    """Validate file type, size, and content.

Performs comprehensive validation on the uploaded file including: - Filename validation - Size limits checking - MIME type verification - For images: additional image content validation

Args: file: FastAPI UploadFile object allowed_types: Set of allowed MediaType values, if None all types are allowed

Returns: Tuple containing: - MediaType: Detected media type - bool: True if file is an image, False otherwise

Raises: FileValidationError: If validation fails"""
```

**Classes:**
```python
class FileSecurityError(SecurityException):
    """Exception raised for file security validation failures."""
```
*Methods:*
```python
    def __init__(self, message, code, details) -> None:
        """Initialize FileSecurityError.

Args: message: Human-readable error description code: Error code from ErrorCode enum details: Additional error context"""
```

```python
class FileValidationError(ValidationException):
    """Exception raised for file validation failures."""
```
*Methods:*
```python
    def __init__(self, message, code, details) -> None:
        """Initialize FileValidationError.

Args: message: Human-readable error description code: Error code from ErrorCode enum details: Additional error context"""
```

```python
class ImageProcessor(Protocol):
    """Protocol defining interface for image processing operations."""
```
*Methods:*
```python
    def open(self, path) -> 'Image.Image':
        """Open an image file.  Args: path: Path to the image file  Returns: Image object"""
```

##### Module: redis_manager
*Core Redis utility functions with proper error handling and structured logging.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/redis_manager.py`

**Imports:**
```python
from __future__ import annotations
import json
from typing import Any, Dict, Optional, TypeVar, cast
import redis.asyncio as redis
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from app.core.config import settings
from app.core.exceptions import ServiceException, ErrorCode
from app.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.utils.redis_manager")
T = T = TypeVar("T")
```

**Functions:**
```python
async def cache_get_or_set(key, callback, ttl, force_refresh) -> Any:
    """Get a value from Redis or set it using the callback.

Args: key: Redis key. callback: Async function to call if key doesn't exist. ttl: TTL in seconds. force_refresh: Force refresh the cache.

Returns: The cached or newly computed value."""
```

```python
async def delete_key(key) -> bool:
    """Delete a key from Redis.

Args: key: The Redis key.

Returns: bool: True if key was deleted, False otherwise."""
```

```python
async def get_key(key, default) -> Optional[T]:
    """Get a key from Redis.

Args: key: The Redis key. default: Default value if key doesn't exist.

Returns: The stored value or default."""
```

```python
async def get_redis_client() -> Redis:
    """Get a Redis client from the connection pool.

Returns: Redis: A Redis client instance.

Raises: ServiceException: If unable to connect to Redis."""
```

```python
async def get_redis_pool() -> ConnectionPool:
    """Get or create a Redis connection pool.

Returns: ConnectionPool: A Redis connection pool instance.

Raises: ServiceException: If unable to connect to Redis."""
```

```python
async def increment_counter(key, amount, ttl) -> Optional[int]:
    """Increment a counter in Redis.

Args: key: The Redis key. amount: Amount to increment by. ttl: Optional TTL in seconds.

Returns: int: New counter value, or None if operation failed."""
```

```python
async def publish_message(channel, message) -> bool:
    """Publish a message to a Redis channel.

Args: channel: Redis channel name. message: Message to publish (will be JSON serialized).

Returns: bool: True if message was published to at least one subscriber."""
```

```python
async def rate_limit_check(key, limit, window) -> tuple[(bool, int)]:
    """Check if a rate limit has been exceeded.

Args: key: The rate limit key. limit: Maximum number of operations in the window. window: Time window in seconds.

Returns: tuple: (is_limited, current_count)"""
```

```python
async def set_key(key, value, ttl) -> bool:
    """Set a key in Redis with optional TTL.

Args: key: The Redis key. value: The value to store (will be JSON serialized). ttl: Optional TTL in seconds.

Returns: bool: True if successful, False otherwise."""
```

##### Module: retry
*Retry utilities for improving resilience of external service calls.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/retry.py`

**Imports:**
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

**Global Variables:**
```python
logger = logger = get_logger("app.utils.retry")
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
```

**Functions:**
```python
async def async_retry(func, retries=None, delay, backoff_factor, jitter, exceptions) -> Union[(Callable[([F], F)], F)]:
    """Decorator to retry asynchronous functions with exponential backoff.

Args: func: Function to decorate (for direct use) retries: Maximum number of retry attempts delay: Initial delay between retries in seconds backoff_factor: Multiplier for delay after each retry jitter: Whether to add randomness to delay timing exceptions: Exception type(s) to catch and retry on

Returns: Callable: Decorated async function that will retry on failure

Examples: # As decorator with default settings @async_retry async def fetch_data(): ...

# As decorator with custom settings @async_retry(retries=5, delay=0.5, exceptions=[ConnectionError, TimeoutError]) async def fetch_data(): ..."""
```

```python
def async_retry_on_network_errors(retries, delay, backoff_factor, jitter) -> Callable[([F], F)]:
    """Decorator to retry async functions specifically on network-related errors.

This is a convenience wrapper around async_retry() with pre-configured exception types for common network errors.

Args: retries: Maximum number of retry attempts delay: Initial delay between retries in seconds backoff_factor: Multiplier for delay after each retry jitter: Whether to add randomness to delay timing

Returns: Callable: Decorator function"""
```

```python
async def async_retry_with_timeout(retries, delay, timeout, backoff_factor, jitter, exceptions) -> Callable[([F], F)]:
    """Decorator to retry async functions with timeout.

Combines timeout functionality with retry logic for async functions.

Args: retries: Maximum number of retry attempts delay: Initial delay between retries in seconds timeout: Maximum execution time in seconds backoff_factor: Multiplier for delay after each retry jitter: Whether to add randomness to delay timing exceptions: Exception type(s) to catch and retry on

Returns: Callable: Decorator function"""
```

```python
def retry(func, retries=None, delay, backoff_factor, jitter, exceptions) -> Union[(Callable[([F], F)], F)]:
    """Decorator to retry synchronous functions with exponential backoff.

Args: func: Function to decorate (for direct use) retries: Maximum number of retry attempts delay: Initial delay between retries in seconds backoff_factor: Multiplier for delay after each retry jitter: Whether to add randomness to delay timing exceptions: Exception type(s) to catch and retry on

Returns: Callable: Decorated function that will retry on failure

Examples: # As decorator with default settings @retry def fetch_data(): ...

# As decorator with custom settings @retry(retries=5, delay=0.5, exceptions=[ConnectionError, TimeoutError]) def fetch_data(): ..."""
```

```python
def retry_on_network_errors(retries, delay, backoff_factor, jitter) -> Callable[([F], F)]:
    """Decorator to retry functions specifically on network-related errors.

This is a convenience wrapper around retry() with pre-configured exception types for common network errors.

Args: retries: Maximum number of retry attempts delay: Initial delay between retries in seconds backoff_factor: Multiplier for delay after each retry jitter: Whether to add randomness to delay timing

Returns: Callable: Decorator function"""
```

```python
def retry_with_timeout(retries, delay, timeout, backoff_factor, jitter, exceptions) -> Callable[([F], F)]:
    """Decorator to retry functions with timeout.

Combines timeout functionality with retry logic.

Args: retries: Maximum number of retry attempts delay: Initial delay between retries in seconds timeout: Maximum execution time in seconds backoff_factor: Multiplier for delay after each retry jitter: Whether to add randomness to delay timing exceptions: Exception type(s) to catch and retry on

Returns: Callable: Decorator function"""
```

**Classes:**
```python
class RetryableError(Protocol):
    """Protocol defining retryable error behaviors."""
```
*Methods:*
```python
    def is_retryable(self) -> bool:
        """Determine if exception should trigger retry."""
```

### Package: tests
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/__init__.py`

#### Module: conftest
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/conftest.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import uuid
from typing import AsyncGenerator, Dict, Generator
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_token
from app.db.base_class import Base
from app.domains.products.models import Brand, Fitment, Product
from app.domains.users.models import Company, User, UserRole, get_password_hash
from app.main import app
```

**Global Variables:**
```python
TEST_DATABASE_URL = TEST_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI).replace(
    settings.POSTGRES_DB, f"{settings.POSTGRES_DB}_test"
)
test_engine = test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)
TestingSessionLocal = TestingSessionLocal = sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)
```

**Functions:**
```python
@pytest_asyncio.fixture(scope='function')
async def admin_headers(admin_token) -> Dict[(str, str)]:
    """Create headers with admin authentication token.

This fixture creates headers with the admin JWT token for authenticated requests.

Args: admin_token: Admin JWT token

Returns: Dict[str, str]: Headers with admin authentication token"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def admin_token(admin_user) -> str:
    """Create an authentication token for admin user.

This fixture generates a valid JWT token for the admin user to use in authenticated API requests.

Args: admin_user: Admin user fixture

Returns: str: JWT token for admin user"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def admin_user(db) -> User:
    """Create a test admin user.

This fixture provides an admin user for testing endpoints that require admin privileges.

Args: db: Database session fixture

Returns: User: Admin user model instance"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def auth_headers(user_token) -> Dict[(str, str)]:
    """Create headers with authentication token.

This fixture creates headers with the JWT token for authenticated requests.

Args: user_token: User JWT token

Returns: Dict[str, str]: Headers with authentication token"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def client(db) -> AsyncGenerator[(AsyncClient, None)]:
    """Create a test client with the database session.

This fixture overrides the database dependency to use the test database session and provides an async HTTP client for testing API endpoints.

Args: db: Database session fixture

Yields: AsyncClient: Test client for async API requests"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def db(setup_db) -> AsyncGenerator[(AsyncSession, None)]:
    """Create a fresh database session for a test.

This fixture provides an isolated database session for each test with proper transaction management and cleanup.

Args: setup_db: Ensures database tables are created

Yields: AsyncSession: Database session"""
```

```python
@pytest.fixture(scope='session')
def event_loop() -> Generator[(asyncio.AbstractEventLoop, None, None)]:
    """Create an instance of the default event loop for each test case.

This fixture is required for pytest-asyncio to work properly.

Yields: asyncio.AbstractEventLoop: Event loop for async tests"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def normal_user(db) -> User:
    """Create a test normal user.

This fixture provides a regular user for testing endpoints that require authentication but not admin privileges.

Args: db: Database session fixture

Returns: User: Normal user model instance"""
```

```python
@pytest_asyncio.fixture(scope='session')
async def setup_db() -> AsyncGenerator[(None, None)]:
    """Set up test database tables.

This fixture creates all tables for testing and drops them after all tests are complete. It runs only once per test session.

Yields: None"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def test_brand(db) -> Brand:
    """Create a test brand.

This fixture provides a brand for testing brand-related functionality.

Args: db: Database session fixture

Returns: Brand: Brand model instance"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def test_company(db) -> Company:
    """Create a test company.

This fixture provides a company for testing company-related functionality.

Args: db: Database session fixture

Returns: Company: Company model instance"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def test_fitment(db) -> Fitment:
    """Create a test fitment.

This fixture provides a fitment for testing fitment-related functionality.

Args: db: Database session fixture

Returns: Fitment: Fitment model instance"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def test_product(db, test_brand) -> Product:
    """Create a test product.

This fixture provides a product for testing product-related functionality.

Args: db: Database session fixture test_brand: Brand fixture

Returns: Product: Product model instance"""
```

```python
@pytest_asyncio.fixture(scope='function')
async def user_token(normal_user) -> str:
    """Create an authentication token for normal user.

This fixture generates a valid JWT token for the normal user to use in authenticated API requests.

Args: normal_user: Normal user fixture

Returns: str: JWT token for normal user"""
```

#### Module: utils
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/utils.py`

**Imports:**
```python
from __future__ import annotations
import random
import string
from typing import Any, Dict, List, Optional, Type, TypeVar
from httpx import AsyncClient
from pydantic import BaseModel
```

**Global Variables:**
```python
M = M = TypeVar("M", bound=BaseModel)
```

**Functions:**
```python
def assert_model_data_matches(model, data) -> None:
    """Assert that a model instance data matches the provided data.

Args: model: Model instance data: Expected data

Raises: AssertionError: If model data doesn't match expected data"""
```

```python
def create_random_email() -> str:
    """Create a random email for test data.  Returns: str: Random email address"""
```

```python
def create_random_string(length) -> str:
    """Create a random string for test data.

Args: length: Length of the string to generate, defaults to 10

Returns: str: Random string"""
```

```python
async def make_authenticated_request(client, method, url, token, **kwargs) -> Any:
    """Make an authenticated request to the API.

Args: client: HTTPX AsyncClient method: HTTP method (get, post, put, delete) url: API endpoint URL token: JWT token for authentication **kwargs: Additional arguments to pass to the client method

Returns: Any: API response

Raises: ValueError: If invalid HTTP method is provided"""
```

```python
def validate_model_response(response_data, model_type, exclude_fields) -> M:
    """Validate that an API response matches a model schema.

Args: response_data: API response data model_type: Pydantic model class to validate against exclude_fields: Fields to exclude from validation, defaults to None

Returns: M: Validated model instance

Raises: ValueError: If response doesn't match model schema"""
```

#### Package: api
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/api`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/api/__init__.py`

##### Package: v1
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/api/v1`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/api/v1/__init__.py`

###### Module: test_auth
*Tests for authentication endpoints.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/api/v1/test_auth.py`

**Imports:**
```python
from __future__ import annotations
from httpx import AsyncClient
from app.domains.users.models import User
from tests.utils import make_authenticated_request
```

**Functions:**
```python
async def test_get_current_user(client, normal_user, user_token) -> None:
    """Test retrieving the current user profile.

Args: client: Test client normal_user: Test user fixture user_token: User authentication token"""
```

```python
async def test_get_current_user_unauthorized(client) -> None:
    """Test retrieving user profile without authentication.  Args: client: Test client"""
```

```python
async def test_login_invalid_credentials(client, normal_user) -> None:
    """Test login with invalid credentials.  Args: client: Test client normal_user: Test user fixture"""
```

```python
async def test_login_success(client, normal_user) -> None:
    """Test successful login with valid credentials.

Args: client: Test client normal_user: Test user fixture"""
```

###### Module: test_products
*Tests for product management endpoints.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/api/v1/test_products.py`

**Imports:**
```python
from __future__ import annotations
import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.products.models import Product
from app.domains.users.models import User
from tests.utils import make_authenticated_request, create_random_string
```

**Functions:**
```python
@pytest.mark.asyncio
async def test_create_product_admin(client, admin_token) -> None:
    """Test creating a product as admin.  Args: client: Test client admin_token: Admin token"""
```

```python
@pytest.mark.asyncio
async def test_create_product_duplicate_sku(client, admin_token, test_product) -> None:
    """Test creating a product with a duplicate SKU.

Args: client: Test client admin_token: Admin token test_product: Test product fixture"""
```

```python
@pytest.mark.asyncio
async def test_create_product_non_admin(client, user_token) -> None:
    """Test that non-admin users cannot create products.  Args: client: Test client user_token: User token"""
```

```python
@pytest.mark.asyncio
async def test_delete_product_admin(client, admin_token, db) -> None:
    """Test deleting a product as admin.

Args: client: Test client admin_token: Admin token db: Database session"""
```

```python
@pytest.mark.asyncio
async def test_delete_product_non_admin(client, user_token, test_product) -> None:
    """Test that non-admin users cannot delete products.

Args: client: Test client user_token: User token test_product: Test product fixture"""
```

```python
@pytest.mark.asyncio
async def test_read_product(client, user_token, test_product) -> None:
    """Test retrieving a single product.

Args: client: Test client user_token: User token test_product: Test product fixture"""
```

```python
@pytest.mark.asyncio
async def test_read_product_not_found(client, user_token) -> None:
    """Test retrieving a non-existent product.  Args: client: Test client user_token: User token"""
```

```python
@pytest.mark.asyncio
async def test_read_products(client, normal_user, user_token, test_product) -> None:
    """Test retrieving a list of products.

Args: client: Test client normal_user: Regular user user_token: User token test_product: Test product fixture"""
```

```python
@pytest.mark.asyncio
async def test_read_products_with_filters(client, admin_token, test_product) -> None:
    """Test retrieving products with filters.

Args: client: Test client admin_token: Admin token test_product: Test product fixture"""
```

```python
@pytest.mark.asyncio
async def test_update_product_admin(client, admin_token, test_product) -> None:
    """Test updating a product as admin.

Args: client: Test client admin_token: Admin token test_product: Test product fixture"""
```

```python
@pytest.mark.asyncio
async def test_update_product_non_admin(client, user_token, test_product) -> None:
    """Test that non-admin users cannot update products.

Args: client: Test client user_token: User token test_product: Test product fixture"""
```

###### Module: test_users
*Tests for user management endpoints.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/api/v1/test_users.py`

**Imports:**
```python
from __future__ import annotations
from httpx import AsyncClient
from app.domains.users.models import User, UserRole
from tests.utils import create_random_email, make_authenticated_request
```

**Functions:**
```python
async def test_create_user_admin(client, admin_token) -> None:
    """Test user creation by admin.  Args: client: Test client admin_token: Admin authentication token"""
```

```python
async def test_delete_user_admin(client, admin_token, normal_user) -> None:
    """Test deleting a user as admin.

Args: client: Test client admin_token: Admin authentication token normal_user: User to delete"""
```

```python
async def test_read_user_by_id_admin(client, admin_token, normal_user) -> None:
    """Test retrieving a user by ID as admin.

Args: client: Test client admin_token: Admin authentication token normal_user: User to retrieve"""
```

```python
async def test_read_users_admin(client, admin_user, admin_token, normal_user) -> None:
    """Test that admin users can list all users.

Args: client: Test client admin_user: Admin user fixture admin_token: Admin authentication token normal_user: Regular user fixture"""
```

```python
async def test_read_users_non_admin(client, normal_user, user_token) -> None:
    """Test that non-admin users cannot list all users.

Args: client: Test client normal_user: Regular user fixture user_token: User authentication token"""
```

```python
async def test_update_user_admin(client, admin_token, normal_user) -> None:
    """Test updating a user as admin.

Args: client: Test client admin_token: Admin authentication token normal_user: User to update"""
```

