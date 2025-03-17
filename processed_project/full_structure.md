# backend Project Structure
Generated on 2025-03-17 01:36:47

## Table of Contents
1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Packages and Modules](#packages-and-modules)

## Project Overview
- Project Name: backend
- Root Path: /home/runner/work/Crown-Nexus/Crown-Nexus/backend
- Packages: 3
- Top-level Modules: 1

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
│   ├── chat/
│   │   ├── connection.py
│   │   ├── service.py
│   │   └── websocket.py
│   ├── commands/
│   │   ├── __init__.py
│   │   └── init_currencies.py
│   ├── core/
│   │   ├── cache/
│   │   │   ├── base.py
│   │   │   ├── decorators.py
│   │   │   ├── keys.py
│   │   │   ├── manager.py
│   │   │   ├── memory.py
│   │   │   └── redis.py
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── celeryconfig.py
│   │   ├── config.py
│   │   ├── dependency_manager.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   ├── permissions.py
│   │   ├── security.py
│   │   └── service_registry.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── base_class.py
│   │   ├── session.py
│   │   └── utils.py
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
│   ├── middleware/
│   │   ├── error_handler.py
│   │   └── response_formatter.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── associations.py
│   │   ├── chat.py
│   │   ├── compliance.py
│   │   ├── currency.py
│   │   ├── location.py
│   │   ├── media.py
│   │   ├── model_mapping.py
│   │   ├── product.py
│   │   ├── reference.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── currency.py
│   │   ├── media.py
│   │   ├── model_mapping.py
│   │   ├── pagination.py
│   │   ├── product.py
│   │   ├── responses.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── cache_service.py
│   │   ├── chat.py
│   │   ├── currency_service.py
│   │   ├── error_handling_service.py
│   │   ├── interfaces.py
│   │   ├── logging_service.py
│   │   ├── media_service.py
│   │   ├── metrics_service.py
│   │   ├── pagination.py
│   │   ├── search.py
│   │   ├── test_service.py
│   │   ├── validation_service.py
│   │   └── vehicle.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── chat_tasks.py
│   │   └── currency_tasks.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── circuit_breaker.py
│   │   ├── crypto.py
│   │   ├── db.py
│   │   ├── errors.py
│   │   ├── file.py
│   │   ├── redis_manager.py
│   │   └── retry.py
│   ├── __init__.py
│   └── main.py
├── examples/
│   ├── __init__.py
│   └── process_fitment.py
├── migrations/
│   └── model_mappings_table.sql
├── scripts/
│   ├── auto_translate.py
│   ├── bootstrap_countries.py
│   ├── check_alembic_version_table.py
│   ├── check_tables.py
│   ├── create_admin.py
│   ├── create_tables_directly.py
│   ├── database_bootstrap.py
│   ├── database_connection_info_check.py
│   ├── debug_database.py
│   ├── extract_messages.py
│   ├── init_db.py
│   ├── reset_db.py
│   ├── test_fixed_config.py
│   └── test_tables.py
├── tests/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_products.py
│   │   │   └── test_users.py
│   │   └── __init__.py
│   ├── integration/
│   │   └── test_api/
│   │       ├── test_auth.py
│   │       └── test_products.py
│   ├── unit/
│   │   ├── test_config.py
│   │   └── test_db.py
│   ├── utils/
│   │   └── factories.py
│   ├── __init__.py
│   ├── conftest.py
│   └── utils.py
├── README.md
├── alembic.ini
├── backend.iml
├── pyproject.toml
├── pytest.ini
├── requirements-dev.in
├── requirements-dev.txt
├── requirements.in
├── requirements.txt
└── test_db.py
```

## Packages and Modules
### Top-level Modules
### Module: test_db
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/test_db.py`

**Imports:**
```python
import asyncio
import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
```

**Functions:**
```python
async def test_connection():
```


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
import logging
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Callable, Optional
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import AppException, app_exception_handler, validation_exception_handler, http_exception_handler, generic_exception_handler
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.response_formatter import ResponseFormatterMiddleware
from app.api.deps import get_current_user
from app.api.v1.router import api_router
from app.core.config import Environment, settings
from app.core.logging import get_logger, request_context, set_user_id
from app.core.service_registry import register_services, initialize_services, shutdown_services
from app.core.cache.manager import initialize_cache
from app.fitment.api import router as fitment_router
from app.fitment.dependencies import initialize_mapping_engine
from app.models.user import User
import uvicorn
```

**Global Variables:**
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

**Functions:**
```python
@app.get('/health')
async def health_check() -> dict:
    """Health check endpoint.

This endpoint allows monitoring systems to check if the application is running and responding to requests.

Returns: dict: Health status information"""
```

```python
@asynccontextmanager
async def lifespan(app) -> AsyncGenerator[(None, None)]:
    """FastAPI lifespan event handler.

This context manager handles application startup and shutdown events. It's responsible for initializing and cleaning up resources.

Args: app: FastAPI application instance

Yields: None"""
```

```python
async def log_current_user(current_user) -> Optional[User]:
    """Log the current user ID in the request context.

Args: current_user: Current authenticated user from token

Returns: The current user unchanged"""
```

**Classes:**
```python
class RequestContextMiddleware(object):
    """Middleware that sets up logging request context.

This middleware ensures each request has a unique ID and tracks execution time, both stored in the logging context."""
```
*Methods:*
```python
    async def __call__(self, request, call_next) -> Response:
        """Process the request and set up logging context.

Args: request: The incoming request call_next: The next middleware or route handler

Returns: Response: The processed response"""
```
```python
    def __init__(self, app) -> None:
        """Initialize middleware with the FastAPI app."""
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
from datetime import datetime
from typing import Annotated, Dict, List, Optional, Union
from fastapi import Depends, HTTPException, Query, WebSocket, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect
from app.core.config import settings
from app.core.exceptions import AuthenticationException, ErrorCode, PermissionDeniedException
from app.core.logging import get_logger, set_user_id
from app.core.permissions import Permission, PermissionChecker
from app.core.security import TokenData, decode_token, oauth2_scheme
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.utils.errors import ensure_not_none
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
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.schemas.responses import Response, PaginatedResponse
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
from datetime import datetime, timedelta
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db
from app.core.config import settings
from app.models.user import User, UserRole, create_access_token, verify_password
from app.schemas.user import Token, TokenPayload, User as UserSchema
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
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, validator
from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.api.responses import created_response, error_response, success_response
from app.core.exceptions import AuthenticationException, BusinessLogicException, PermissionDeniedException, ResourceAlreadyExistsException, ResourceNotFoundException, ValidationException
from app.core.logging import get_logger, log_execution_time
from app.db.session import AsyncSession
from app.models.chat import ChatMember, ChatMemberRole, ChatRoom, ChatRoomType, MessageType
from app.models.user import User
from app.services import get_chat_service
from app.schemas.responses import Response
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
    def validate_role(cls, v) -> str:
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
    def validate_message_type(cls, v) -> str:
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
    def validate_type(cls, v) -> str:
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
    def validate_role(cls, v) -> str:
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
from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.models.currency import Currency, ExchangeRate
from app.models.user import User
from app.schemas.currency import ConversionRequest, ConversionResponse, CurrencyCreate, CurrencyRead, CurrencyUpdate, ExchangeRateRead
from app.services.currency_service import ExchangeRateService
from app.tasks.currency_tasks import update_exchange_rates
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
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.models.product import Fitment, Product, product_fitment_association
from app.models.user import User
from app.schemas.product import Fitment as FitmentSchema, FitmentCreate, FitmentListResponse, FitmentUpdate, Product as ProductSchema
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
from typing import Annotated, Dict, Any
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
from typing import Annotated, Any, List, Optional, Set
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, Response, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination, get_optional_user
from app.core.config import settings
from app.models.media import Media, MediaType, MediaVisibility
from app.models.product import Product, product_media_association
from app.models.user import User
from app.schemas.media import FileUploadResponse, Media as MediaSchema, MediaCreate, MediaListResponse, MediaUpdate
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
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.models.product import Brand, Fitment, Product, ProductActivity, ProductBrandHistory, ProductDescription, ProductMarketing, ProductMeasurement, ProductStock, ProductSupersession
from app.models.reference import Warehouse
from app.models.user import User
from app.schemas.product import Brand as BrandSchema, BrandCreate, BrandUpdate, Fitment as FitmentSchema, FitmentCreate, FitmentUpdate, Product as ProductSchema, ProductCreate, ProductDescription as ProductDescriptionSchema, ProductDescriptionCreate, ProductDescriptionUpdate, ProductListResponse, ProductMarketing as ProductMarketingSchema, ProductMarketingCreate, ProductMarketingUpdate, ProductMeasurement as ProductMeasurementSchema, ProductMeasurementCreate, ProductMeasurementUpdate, ProductStatus, ProductStock as ProductStockSchema, ProductStockCreate, ProductStockUpdate, ProductSupersession as ProductSupersessionSchema, ProductSupersessionCreate, ProductUpdate
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
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db
from app.models.user import User
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
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.models.user import Company, User, UserRole, get_password_hash
from app.schemas.user import Company as CompanySchema, CompanyCreate, CompanyUpdate, User as UserSchema, UserCreate, UserUpdate
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
import sys
import typer
from typing import List, Optional
from sqlalchemy import select
from app.core.config import settings
from app.db.session import get_db_context
from app.models.currency import Currency
from app.tasks.currency_tasks import init_currencies as init_currencies_task
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
from app.core.config import settings
import app.tasks.currency_tasks
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

##### Module: config
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/config.py`

**Imports:**
```python
from __future__ import annotations
import os
import secrets
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, DirectoryPath, Field, PostgresDsn, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Global Variables:**
```python
settings = settings = get_settings()
```

**Functions:**
```python
@lru_cache
def get_settings() -> Settings:
    """Get application settings with caching.

This function is cached to avoid loading settings multiple times.

Returns: Application settings"""
```

**Classes:**
```python
class CORSSettings(BaseSettings):
    """CORS settings.  Attributes: BACKEND_CORS_ORIGINS: List of allowed origins for CORS"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```
*Methods:*
```python
@field_validator('BACKEND_CORS_ORIGINS', mode='before')
@classmethod
    def assemble_cors_origins(cls, v) -> List[str]:
        """Parse CORS origins from string or list.

Args: v: CORS origins as string or list

Returns: List of CORS origin strings"""
```

```python
class CelerySettings(BaseSettings):
    """Celery worker settings.

Attributes: CELERY_BROKER_URL: URL for Celery broker CELERY_RESULT_BACKEND: URL for Celery result backend"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```

```python
class ChatSettings(BaseSettings):
    """Chat system settings.

Attributes: CHAT_ENCRYPTION_SALT: Salt for chat message encryption CHAT_MESSAGE_LIMIT: Default message limit for fetching history CHAT_RATE_LIMIT_PER_MINUTE: Maximum messages per minute per user CHAT_WEBSOCKET_KEEPALIVE: Keepalive interval in seconds CHAT_MAX_MESSAGE_LENGTH: Maximum message length in characters"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```

```python
class CurrencySettings(BaseSettings):
    """Currency and exchange rate settings.

Attributes: EXCHANGE_RATE_API_KEY: API key for exchange rate service EXCHANGE_RATE_UPDATE_FREQUENCY: Update frequency in hours STORE_INVERSE_RATES: Whether to store inverse rates"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```

```python
class DatabaseSettings(BaseSettings):
    """Database connection settings.

Attributes: POSTGRES_SERVER: PostgreSQL server hostname POSTGRES_USER: PostgreSQL username POSTGRES_PASSWORD: PostgreSQL password POSTGRES_DB: PostgreSQL database name POSTGRES_PORT: PostgreSQL server port SQLALCHEMY_DATABASE_URI: Constructed database URI"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```
*Methods:*
```python
@model_validator(mode='after')
    def assemble_db_connection(self) -> 'DatabaseSettings':
        """Assemble database URI from components.  Returns: Self with SQLALCHEMY_DATABASE_URI set"""
```

```python
class ElasticsearchSettings(BaseSettings):
    """Elasticsearch connection settings.

Attributes: ELASTICSEARCH_HOST: Elasticsearch server hostname ELASTICSEARCH_PORT: Elasticsearch server port ELASTICSEARCH_USE_SSL: Whether to use SSL for connection ELASTICSEARCH_USERNAME: Elasticsearch username (optional) ELASTICSEARCH_PASSWORD: Elasticsearch password (optional)"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```
*Methods:*
```python
@property
    def uri(self) -> str:
        """Get Elasticsearch URI.  Returns: Elasticsearch connection URI"""
```

```python
class Environment(str, Enum):
    """Application environment enumeration.

Attributes: DEVELOPMENT: Development environment STAGING: Staging/testing environment PRODUCTION: Production environment"""
```
*Class attributes:*
```python
DEVELOPMENT = 'development'
STAGING = 'staging'
PRODUCTION = 'production'
```

```python
class FitmentSettings(BaseSettings):
    """Fitment system settings.

Attributes: VCDB_PATH: Path to VCDB Access database PCDB_PATH: Path to PCDB Access database MODEL_MAPPINGS_PATH: Path to model mappings file (optional) FITMENT_DB_URL: Database URL for fitment data (optional) FITMENT_LOG_LEVEL: Log level for fitment system FITMENT_CACHE_SIZE: Size of fitment cache"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```
*Methods:*
```python
@model_validator(mode='after')
    def validate_file_paths(self) -> 'FitmentSettings':
        """Validate that required file paths exist.

Returns: Self with validated paths

Raises: ValueError: If required paths don't exist"""
```

```python
class LocaleSettings(BaseSettings):
    """Internationalization and localization settings.

Attributes: DEFAULT_LOCALE: Default locale AVAILABLE_LOCALES: List of available locales"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```

```python
class LogLevel(str, Enum):
    """Log level enumeration.

Attributes: DEBUG: Debug level logging INFO: Info level logging WARNING: Warning level logging ERROR: Error level logging CRITICAL: Critical level logging"""
```
*Class attributes:*
```python
DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'
```

```python
class LoggingSettings(BaseSettings):
    """Logging configuration settings.

Attributes: LOG_LEVEL: Default log level LOG_FORMAT: Log format (json or text)"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```

```python
class MediaSettings(BaseSettings):
    """Media handling settings.

Attributes: MEDIA_ROOT: Root directory for media files MEDIA_URL: URL prefix for media files MEDIA_STORAGE_TYPE: Storage type (local, s3, etc.) MEDIA_CDN_URL: CDN URL for media files (optional)"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```
*Methods:*
```python
@field_validator('MEDIA_ROOT', mode='before')
@classmethod
    def create_media_directories(cls, v) -> str:
        """Create media directories if they don't exist.  Args: v: Media root path  Returns: Media root path"""
```
```python
@property
    def media_base_url(self) -> str:
        """Get the base URL for media files.

Returns: Base URL for media files (CDN URL in production, local path otherwise)"""
```

```python
class RedisSettings(BaseSettings):
    """Redis connection settings.

Attributes: REDIS_HOST: Redis server hostname REDIS_PORT: Redis server port REDIS_PASSWORD: Redis password (optional) REDIS_DB: Redis database number"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```
*Methods:*
```python
@property
    def uri(self) -> str:
        """Get Redis URI.  Returns: Redis connection URI"""
```

```python
class SecuritySettings(BaseSettings):
    """Security settings.

Attributes: SECRET_KEY: Secret key for token signing ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration time in minutes ALGORITHM: JWT signing algorithm"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```

```python
class Settings(BaseSettings):
    """Main application settings combining all subsystems.

Attributes: PROJECT_NAME: Name of the project DESCRIPTION: Project description VERSION: Application version ENVIRONMENT: Current environment API_V1_STR: API v1 prefix BASE_DIR: Base directory for the application

# Subsystem settings included as properties"""
```
*Class attributes:*
```python
model_config =     model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
```
*Methods:*
```python
@field_validator('BACKEND_CORS_ORIGINS', mode='before')
@classmethod
    def assemble_cors_origins(cls, v) -> List[str]:
        """Parse CORS origins from string or list.

Args: v: CORS origins as string or list

Returns: List of CORS origin strings"""
```
```python
@model_validator(mode='after')
    def assemble_db_connection(self) -> 'Settings':
        """Assemble database URI from components.  Returns: Self with SQLALCHEMY_DATABASE_URI set"""
```
```python
@property
    def chat(self) -> ChatSettings:
        """Get chat settings."""
```
```python
@field_validator('MEDIA_ROOT', mode='before')
@classmethod
    def create_media_directories(cls, v) -> str:
        """Create media directories if they don't exist.  Args: v: Media root path  Returns: Media root path"""
```
```python
@property
    def currency(self) -> CurrencySettings:
        """Get currency settings."""
```
```python
@property
    def db(self) -> DatabaseSettings:
        """Get database settings."""
```
```python
@property
    def elasticsearch(self) -> ElasticsearchSettings:
        """Get Elasticsearch settings."""
```
```python
@property
    def fitment(self) -> FitmentSettings:
        """Get fitment settings."""
```
```python
@property
    def locale(self) -> LocaleSettings:
        """Get locale settings."""
```
```python
@property
    def media(self) -> MediaSettings:
        """Get media settings."""
```
```python
@property
    def media_base_url(self) -> str:
        """Get the base URL for media files.

Returns: Base URL for media files (CDN URL in production, local path otherwise)"""
```
```python
@property
    def redis(self) -> RedisSettings:
        """Get Redis settings."""
```
```python
@property
    def security(self) -> SecuritySettings:
        """Get security settings."""
```

##### Module: dependency_manager
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/dependency_manager.py`

**Imports:**
```python
from __future__ import annotations
import inspect
import logging
from typing import Any, Callable, Dict, Optional, Type, TypeVar, cast
```

**Global Variables:**
```python
T = T = TypeVar('T')
dependency_manager = dependency_manager = DependencyManager()
```

**Functions:**
```python
def get_dependency(name, **kwargs) -> Any:
    """Get a dependency instance.

This is a convenience function for getting a dependency instance.

Args: name: Dependency name **kwargs: Arguments to pass to the factory function

Returns: Any: Dependency instance"""
```

```python
def inject_dependency(dependency_name) -> Callable:
    """Decorator for injecting dependencies.

This decorator injects a dependency into a function or method.

Args: dependency_name: Name of the dependency to inject

Returns: Callable: Decorated function or method"""
```

**Classes:**
```python
class DependencyManager(object):
    """Manager for application dependencies.

This class provides a central registry for all dependencies in the application, allowing for better organization, testing, and dependency injection."""
```
*Methods:*
```python
    def __new__(cls) -> DependencyManager:
        """Create a singleton instance of the dependency manager.

Returns: DependencyManager: The singleton instance"""
```
```python
    def clear(self) -> None:
        """Clear all registered dependencies.  This is useful for testing to ensure a clean state."""
```
```python
    def clear_instance(self, name) -> None:
        """Clear a specific dependency instance.  Args: name: Dependency name"""
```
```python
    def get(self, name, **kwargs) -> Any:
        """Get a dependency instance.

If the dependency is not already registered, it will be created using the registered factory function.

Args: name: Dependency name **kwargs: Arguments to pass to the factory function

Returns: Any: Dependency instance

Raises: ValueError: If dependency is not registered"""
```
```python
    def get_instance(self, cls, **kwargs) -> T:
        """Get a dependency instance by class.

Args: cls: Dependency class **kwargs: Arguments to pass to the factory function

Returns: T: Dependency instance

Raises: ValueError: If dependency is not registered"""
```
```python
    def register_dependency(self, name, instance) -> None:
        """Register a dependency instance.  Args: name: Dependency name instance: Dependency instance"""
```
```python
    def register_factory(self, name, factory) -> None:
        """Register a factory function for creating dependencies.

Args: name: Dependency name factory: Factory function"""
```

##### Module: exceptions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/exceptions.py`

**Imports:**
```python
from __future__ import annotations
import logging
import sys
import traceback
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union, cast
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from app.core.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.exceptions")
```

**Functions:**
```python
async def app_exception_handler(request, exc) -> JSONResponse:
    """Handle AppException instances.

Args: request: FastAPI request exc: AppException instance

Returns: JSONResponse: JSON response with error details"""
```

```python
async def generic_exception_handler(request, exc) -> JSONResponse:
    """Handle unhandled exceptions.

Args: request: FastAPI request exc: Unhandled exception

Returns: JSONResponse: JSON response with error details"""
```

```python
async def http_exception_handler(request, exc) -> JSONResponse:
    """Handle FastAPI's HTTPException.

Args: request: FastAPI request exc: HTTPException instance

Returns: JSONResponse: JSON response with error details"""
```

```python
async def validation_exception_handler(request, exc) -> JSONResponse:
    """Handle FastAPI's RequestValidationError.

Args: request: FastAPI request exc: RequestValidationError instance

Returns: JSONResponse: JSON response with validation error details"""
```

**Classes:**
```python
class AppException(Exception):
    """Base exception for all application-specific exceptions.

This class provides the foundation for a structured exception hierarchy, with standardized error codes, messages, and HTTP status codes."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, severity, category, original_exception) -> None:
        """Initialize the exception with customizable properties.

Args: message: Human-readable error message code: Error code details: Detailed error information status_code: HTTP status code severity: Error severity level category: Error category original_exception: Original exception that caused this error"""
```
```python
    def log(self, request_id) -> None:
        """Log the exception with appropriate severity level.  Args: request_id: Request ID for tracking"""
```
```python
    def to_response(self, request_id) -> ErrorResponse:
        """Convert exception to a standardized error response.

Args: request_id: Request ID for tracking

Returns: ErrorResponse: Standardized error response"""
```

```python
class AuthenticationException(AppException):
    """Exception raised for authentication errors.  This exception is used when authentication fails."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the authentication exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class BadRequestException(AppException):
    """Exception raised for bad requests.  This exception is used when a request is malformed or invalid."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the bad request exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class BusinessLogicException(AppException):
    """Exception raised for business logic errors.

This exception is used when a business rule is violated."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the business logic exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class ConfigurationException(AppException):
    """Exception raised for configuration errors.

This exception is used when there's an issue with application configuration."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the configuration exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class DataIntegrityException(DatabaseException):
    """Exception raised for data integrity errors.

This exception is used when a database constraint is violated."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the data integrity exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class DatabaseException(AppException):
    """Exception raised for database errors.  This exception is used when a database operation fails."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the database exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class ErrorCategory(str, Enum):
    """Categories for errors.  These categories help group errors by their source or nature."""
```
*Class attributes:*
```python
VALIDATION = 'validation'
AUTHENTICATION = 'authentication'
AUTHORIZATION = 'authorization'
RESOURCE = 'resource'
DATABASE = 'database'
NETWORK = 'network'
EXTERNAL = 'external'
BUSINESS = 'business'
SECURITY = 'security'
DATA = 'data'
SYSTEM = 'system'
UNKNOWN = 'unknown'
```

```python
class ErrorCode(str, Enum):
    """Error codes for standardized error responses.

These codes provide standardized identifiers for error types, allowing clients to handle errors consistently."""
```
*Class attributes:*
```python
UNKNOWN_ERROR = 'UNKNOWN_ERROR'
VALIDATION_ERROR = 'VALIDATION_ERROR'
PERMISSION_DENIED = 'PERMISSION_DENIED'
RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND'
RESOURCE_ALREADY_EXISTS = 'RESOURCE_ALREADY_EXISTS'
BAD_REQUEST = 'BAD_REQUEST'
AUTHENTICATION_FAILED = 'AUTHENTICATION_FAILED'
TOKEN_EXPIRED = 'TOKEN_EXPIRED'
INVALID_TOKEN = 'INVALID_TOKEN'
USER_NOT_ACTIVE = 'USER_NOT_ACTIVE'
DATABASE_ERROR = 'DATABASE_ERROR'
TRANSACTION_FAILED = 'TRANSACTION_FAILED'
DATA_INTEGRITY_ERROR = 'DATA_INTEGRITY_ERROR'
NETWORK_ERROR = 'NETWORK_ERROR'
TIMEOUT_ERROR = 'TIMEOUT_ERROR'
CONNECTION_ERROR = 'CONNECTION_ERROR'
EXTERNAL_SERVICE_ERROR = 'EXTERNAL_SERVICE_ERROR'
RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED'
SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE'
EXTERNAL_DEPENDENCY_ERROR = 'EXTERNAL_DEPENDENCY_ERROR'
BUSINESS_LOGIC_ERROR = 'BUSINESS_LOGIC_ERROR'
INVALID_STATE_ERROR = 'INVALID_STATE_ERROR'
OPERATION_NOT_ALLOWED = 'OPERATION_NOT_ALLOWED'
SECURITY_ERROR = 'SECURITY_ERROR'
ACCESS_DENIED = 'ACCESS_DENIED'
CSRF_ERROR = 'CSRF_ERROR'
DATA_ERROR = 'DATA_ERROR'
SERIALIZATION_ERROR = 'SERIALIZATION_ERROR'
DESERIALIZATION_ERROR = 'DESERIALIZATION_ERROR'
SYSTEM_ERROR = 'SYSTEM_ERROR'
CONFIGURATION_ERROR = 'CONFIGURATION_ERROR'
DEPENDENCY_ERROR = 'DEPENDENCY_ERROR'
```

```python
class ErrorDetail(BaseModel):
    """Detailed error information for API responses.

This model provides structured error details, including location, message, and error type."""
```

```python
class ErrorResponse(BaseModel):
    """Standardized error response model.

This model defines the structure of error responses returned by the API, providing consistent error information to clients."""
```
*Methods:*
```python
@validator('details', pre=True)
    def validate_details(cls, v) -> List[ErrorDetail]:
        """Validate and convert error details to proper format."""
```

```python
class ErrorSeverity(str, Enum):
    """Severity levels for errors.  These levels help categorize errors by their impact and urgency."""
```
*Class attributes:*
```python
DEBUG = 'debug'
INFO = 'info'
WARNING = 'warning'
ERROR = 'error'
CRITICAL = 'critical'
```

```python
class ExternalServiceException(AppException):
    """Exception raised for external service errors.

This exception is used when an external service call fails."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the external service exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class InvalidStateException(BusinessLogicException):
    """Exception raised for invalid state errors.

This exception is used when an operation is attempted in an invalid state."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the invalid state exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class NetworkException(AppException):
    """Exception raised for network errors.  This exception is used when a network operation fails."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the network exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class OperationNotAllowedException(BusinessLogicException):
    """Exception raised when an operation is not allowed.

This exception is used when an operation is not allowed due to business rules."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the operation not allowed exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class PermissionDeniedException(AppException):
    """Exception raised for permission errors.

This exception is used when a user doesn't have permission to perform an action."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the permission denied exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class RateLimitException(ExternalServiceException):
    """Exception raised for rate limit errors.

This exception is used when an external service rate limit is exceeded."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the rate limit exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class ResourceAlreadyExistsException(AppException):
    """Exception raised when a resource already exists.

This exception is used when attempting to create a resource that already exists."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the resource already exists exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class ResourceNotFoundException(AppException):
    """Exception raised when a resource is not found.

This exception is used when a requested resource doesn't exist."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the resource not found exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class ServiceUnavailableException(ExternalServiceException):
    """Exception raised when an external service is unavailable.

This exception is used when an external service is temporarily unavailable."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the service unavailable exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class TimeoutException(NetworkException):
    """Exception raised for timeout errors.  This exception is used when a network operation times out."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the timeout exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class TransactionException(DatabaseException):
    """Exception raised for transaction errors.  This exception is used when a database transaction fails."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the transaction exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

```python
class ValidationException(AppException):
    """Exception raised for validation errors.

This exception is used when input data fails validation checks."""
```
*Methods:*
```python
    def __init__(self, message, code, details, status_code, original_exception) -> None:
        """Initialize the validation exception.

Args: message: Error message code: Error code details: Additional error details status_code: HTTP status code original_exception: Original exception"""
```

##### Module: logging
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/logging.py`

**Imports:**
```python
from __future__ import annotations
import logging
import logging.config
import sys
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, Union
import structlog
from pythonjsonlogger import jsonlogger
from structlog.stdlib import BoundLogger
from structlog.types import EventDict, Processor, WrappedLogger
from app.core.config import Environment, LogLevel, settings
```

**Global Variables:**
```python
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
```

**Functions:**
```python
def add_request_id_processor(logger, method_name, event_dict) -> EventDict:
    """Structlog processor that adds request_id from thread-local storage.

Args: logger: Logger instance method_name: Method name being called event_dict: Event dictionary to modify

Returns: Modified event dictionary"""
```

```python
def add_service_info_processor(logger, method_name, event_dict) -> EventDict:
    """Structlog processor that adds service information to log events.

Args: logger: Logger instance method_name: Method name being called event_dict: Event dictionary to modify

Returns: Modified event dictionary"""
```

```python
def add_timestamp_processor(logger, method_name, event_dict) -> EventDict:
    """Structlog processor that adds timestamp to log events.

Args: logger: Logger instance method_name: Method name being called event_dict: Event dictionary to modify

Returns: Modified event dictionary"""
```

```python
def add_user_id_processor(logger, method_name, event_dict) -> EventDict:
    """Structlog processor that adds user_id from thread-local storage.

Args: logger: Logger instance method_name: Method name being called event_dict: Event dictionary to modify

Returns: Modified event dictionary"""
```

```python
def clear_user_id() -> None:
    """Clear the current user ID from the logging context."""
```

```python
def configure_std_logging() -> None:
    """Configure standard library logging with appropriate handlers and formatters.

This sets up log handlers based on environment and configuration settings."""
```

```python
def configure_structlog() -> None:
    """Configure structlog with processors and renderers.

This sets up structlog to work alongside the standard library logging, with consistent formatting and context handling."""
```

```python
def get_logger(name) -> BoundLogger:
    """Get a structlog logger instance.

Args: name: Logger name (typically __name__)

Returns: Structured logger instance"""
```

```python
def log_execution_time(logger, level):
    """Decorator to log function execution time.

Args: logger: Logger to use (created from function name if not provided) level: Log level to use ("debug", "info", etc.)

Returns: Decorated function"""
```

```python
def log_execution_time_async(logger, level):
    """Decorator to log async function execution time.

Args: logger: Logger to use (created from function name if not provided) level: Log level to use ("debug", "info", etc.)

Returns: Decorated async function"""
```

```python
@contextmanager
def request_context(request_id, user_id):
    """Context manager for tracking request context in logs.

Args: request_id: Request ID (generated if not provided) user_id: User ID (optional)

Yields: The request_id"""
```

```python
def set_user_id(user_id) -> None:
    """Set the current user ID in the logging context.  Args: user_id: User ID to set"""
```

```python
def setup_logging() -> None:
    """Set up the logging system.

This function should be called early in the application startup process to configure all logging components."""
```

**Classes:**
```python
class RequestIdFilter(logging.Filter):
    """Log filter that adds request_id from thread-local storage.

This filter adds the current request ID to log records if available."""
```
*Methods:*
```python
    def filter(self, record) -> bool:
        """Add request_id to log record if available.

Args: record: Log record to modify

Returns: True to include the record"""
```

```python
class UserIdFilter(logging.Filter):
    """Log filter that adds user_id from thread-local storage.

This filter adds the current user ID to log records if available."""
```
*Methods:*
```python
    def filter(self, record) -> bool:
        """Add user_id to log record if available.

Args: record: Log record to modify

Returns: True to include the record"""
```

##### Module: permissions
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/permissions.py`

**Imports:**
```python
from __future__ import annotations
import enum
from typing import Any, Callable, Dict, List, Optional, Set, Type, TypeVar, Union, cast
from fastapi import Depends, HTTPException, Request, status
from pydantic import BaseModel
from app.core.exceptions import PermissionDeniedException
from app.core.logging import get_logger
from app.models.user import User, UserRole
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.permissions")
T = T = TypeVar("T", bound=Callable[..., Any])
ROLE_PERMISSIONS = ROLE_PERMISSIONS = {
    UserRole.ADMIN: {
        # Admin has all permissions
        p for p in Permission
    },
    UserRole.MANAGER: {
        # Managers have most permissions except for system administration
        Permission.USER_READ,
        Permission.USER_CREATE,
        Permission.USER_UPDATE,
        
        Permission.PRODUCT_READ,
        Permission.PRODUCT_CREATE,
        Permission.PRODUCT_UPDATE,
        Permission.PRODUCT_DELETE,
        Permission.PRODUCT_ADMIN,
        
        Permission.MEDIA_READ,
        Permission.MEDIA_CREATE,
        Permission.MEDIA_UPDATE,
        Permission.MEDIA_DELETE,
        Permission.MEDIA_ADMIN,
        
        Permission.FITMENT_READ,
        Permission.FITMENT_CREATE,
        Permission.FITMENT_UPDATE,
        Permission.FITMENT_DELETE,
        Permission.FITMENT_ADMIN,
        
        Permission.COMPANY_READ,
    },
    UserRole.CLIENT: {
        # Clients have basic read permissions and can manage their own data
        Permission.PRODUCT_READ,
        Permission.FITMENT_READ,
        Permission.MEDIA_READ,
        Permission.COMPANY_READ,
    },
    UserRole.DISTRIBUTOR: {
        # Distributors have slightly more permissions than regular clients
        Permission.PRODUCT_READ,
        Permission.FITMENT_READ,
        Permission.MEDIA_READ,
        Permission.MEDIA_CREATE,
        Permission.COMPANY_READ,
    },
    UserRole.READ_ONLY: {
        # Read-only users can only read data
        Permission.PRODUCT_READ,
        Permission.FITMENT_READ,
        Permission.MEDIA_READ,
        Permission.COMPANY_READ,
    },
}
permissions = permissions = PermissionChecker()
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
```python
@staticmethod
    def require_admin() -> Callable[([T], T)]:
        """Decorator to require admin role.  Returns: Callable: Decorator function"""
```
```python
@staticmethod
    def require_permission(permission) -> Callable[([T], T)]:
        """Decorator to require a specific permission.

Args: permission: Required permission

Returns: Callable: Decorator function"""
```
```python
@staticmethod
    def require_permissions(permissions, require_all) -> Callable[([T], T)]:
        """Decorator to require multiple permissions.

Args: permissions: Required permissions require_all: Whether all permissions are required (AND) or any (OR)

Returns: Callable: Decorator function"""
```

##### Module: security
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/security.py`

**Imports:**
```python
from __future__ import annotations
import secrets
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, ValidationError
from app.core.config import settings
from app.core.exceptions import AuthenticationException, ErrorCode
from app.core.logging import get_logger
from app.utils.redis_manager import delete_key, get_key, set_key
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.security")
pwd_context = pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)
```

**Functions:**
```python
async def add_token_to_blacklist(token_jti, expires_at) -> None:
    """Add a token to the blacklist in Redis.

Args: token_jti: JWT ID to blacklist expires_at: When the token expires"""
```

```python
def create_token(subject, token_type, expires_delta, role, user_data) -> str:
    """Create a JWT token.

Args: subject: Subject (user ID) token_type: Token type (access or refresh) expires_delta: Token expiration time role: User role user_data: Additional user data to include in token

Returns: str: JWT token"""
```

```python
def create_token_pair(user_id, role, user_data) -> TokenPair:
    """Create an access and refresh token pair.

Args: user_id: User ID role: User role user_data: Additional user data to include in tokens

Returns: TokenPair: Access and refresh token pair"""
```

```python
async def decode_token(token) -> TokenData:
    """Decode and validate a JWT token.

Args: token: JWT token

Returns: TokenData: Decoded token data

Raises: AuthenticationException: If token is invalid or expired"""
```

```python
def generate_random_token(length) -> str:
    """Generate a secure random token.

Args: length: Length of the token in bytes

Returns: str: Secure random token"""
```

```python
def generate_token_jti() -> str:
    """Generate a unique JWT ID for token tracking.  Returns: str: Unique token identifier"""
```

```python
def get_password_hash(password) -> str:
    """Hash a password using bcrypt.  Args: password: Plain text password  Returns: str: Hashed password"""
```

```python
async def is_token_blacklisted(token_jti) -> bool:
    """Check if a token is blacklisted.

Args: token_jti: JWT ID to check

Returns: bool: True if token is blacklisted"""
```

```python
async def refresh_tokens(refresh_token) -> TokenPair:
    """Generate new token pair using a refresh token.

Args: refresh_token: JWT refresh token

Returns: TokenPair: New access and refresh token pair

Raises: AuthenticationException: If refresh token is invalid"""
```

```python
async def revoke_token(token) -> None:
    """Revoke a token by adding it to the blacklist.

Args: token: JWT token to revoke

Raises: AuthenticationException: If token is invalid"""
```

```python
def verify_password(plain_password, hashed_password) -> bool:
    """Verify a password against a hash.

Args: plain_password: Plain text password hashed_password: Hashed password

Returns: bool: True if password matches"""
```

**Classes:**
```python
class TokenData(BaseModel):
    """Token payload data."""
```

```python
class TokenPair(BaseModel):
    """Access and refresh token pair."""
```

```python
class TokenType(str):
    """Token type constants."""
```
*Class attributes:*
```python
ACCESS = 'access'
REFRESH = 'refresh'
```

##### Module: service_registry
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/core/service_registry.py`

**Imports:**
```python
from __future__ import annotations
import inspect
from typing import Any, Dict, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import dependency_manager
from app.core.logging import get_logger
from app.services.error_handling_service import ErrorHandlingService
from app.services.logging_service import LoggingService
from app.services.metrics_service import MetricsService
from app.services.validation_service import ValidationService
from app.services.cache_service import CacheService
```

**Global Variables:**
```python
logger = logger = get_logger("app.core.service_registry")
```

**Functions:**
```python
def get_service(service_name, db) -> Any:
    """Get a service instance by name.

Args: service_name: Name of the service db: Optional database session

Returns: Any: Service instance"""
```

```python
async def initialize_services() -> None:
    """Initialize all registered services.

This function should be called during application startup to initialize all registered services."""
```

```python
def register_services() -> None:
    """Register all services in the dependency manager.

This function should be called during application startup to register all services in the dependency manager."""
```

```python
async def shutdown_services() -> None:
    """Shutdown all registered services.

This function should be called during application shutdown to release resources held by services."""
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
from app.models.user import Company, User, UserRole
from app.models.associations import product_fitment_association, product_media_association, product_tariff_code_association, product_unspsc_association, product_country_origin_association, product_hardware_association, product_interchange_association, product_packaging_association, product_color_association, product_construction_type_association, product_texture_association
from app.models.location import Address, Country
from app.models.reference import Color, ConstructionType, Hardware, PackagingType, TariffCode, Texture, UnspscCode, Warehouse
from app.models.product import AttributeDefinition, Brand, Fitment, Manufacturer, PriceType, Product, ProductActivity, ProductAttribute, ProductBrandHistory, ProductDescription, ProductMarketing, ProductMeasurement, ProductPricing, ProductStock, ProductSupersession
from app.models.media import Media, MediaType, MediaVisibility
from app.models.compliance import Prop65Chemical, ProductChemical
```

##### Module: base_class
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/db/base_class.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, cast, ClassVar, get_args, get_origin, get_type_hints
from sqlalchemy import Column, DateTime, Boolean, String, inspect, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from sqlalchemy.sql.expression import Select
from app.core.logging import get_logger
```

**Global Variables:**
```python
logger = logger = get_logger("app.db.base_class")
T = T = TypeVar('T', bound='Base')
```

**Classes:**
```python
@as_declarative()
class Base(DeclarativeBase):
    """Enhanced base class for all database models.

This class provides common functionality for all models, including: - Automatic table name generation - Audit fields (created_at, updated_at, created_by_id, updated_by_id) - Soft deletion support - JSON serialization via the to_dict() method - Helper methods for common query operations"""
```
*Methods:*
```python
@declared_attr
    def __tablename__(cls) -> str:
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
from sqlalchemy.pool import NullPool
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
import contextlib
import functools
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Sequence, Type, TypeVar, Union, cast, overload
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import Delete, Insert, Update
from app.core.exceptions import DatabaseException
from app.core.logging import get_logger
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
    """Create multiple model instances in a single transaction.

Args: db: Database session model: Model class objects: List of object data

Returns: List[T]: List of created instances

Raises: DatabaseException: If a database error occurs"""
```

```python
async def bulk_update(db, model, id_field, objects) -> int:
    """Update multiple model instances in a single transaction.

Args: db: Database session model: Model class id_field: Field name to use for identifying records (usually 'id') objects: List of object data (must include id_field)

Returns: int: Number of updated instances

Raises: DatabaseException: If a database error occurs"""
```

```python
async def count_query(db, query) -> int:
    """Count results of a query.

Args: db: Database session query: Base query

Returns: int: Count of matching records

Raises: DatabaseException: If a database error occurs"""
```

```python
async def create_object(db, model, obj_in) -> T:
    """Create a new model instance.

Args: db: Database session model: Model class obj_in: Object data

Returns: T: Created instance

Raises: DatabaseException: If a database error occurs"""
```

```python
async def delete_object(db, model, id_value, user_id, hard_delete) -> bool:
    """Delete a model instance by ID.

By default, performs a soft delete unless hard_delete is True.

Args: db: Database session model: Model class id_value: ID value to look up user_id: ID of the user performing the deletion hard_delete: Whether to permanently delete the record

Returns: bool: True if deleted, False if not found

Raises: DatabaseException: If a database error occurs"""
```

```python
async def execute_query(db, query) -> Any:
    """Execute a SQLAlchemy query with error handling.

Args: db: Database session query: SQLAlchemy query to execute

Returns: Any: Query result

Raises: DatabaseException: If a database error occurs"""
```

```python
async def get_by_id(db, model, id_value) -> Optional[T]:
    """Get a model instance by ID with proper error handling.

Args: db: Database session model: Model class id_value: ID value to look up

Returns: Optional[T]: Found instance or None

Raises: DatabaseException: If a database error occurs"""
```

```python
async def get_by_ids(db, model, ids) -> List[T]:
    """Get multiple model instances by their IDs.

Args: db: Database session model: Model class ids: List of IDs to look up

Returns: List[T]: List of found instances

Raises: DatabaseException: If a database error occurs"""
```

```python
async def paginate(db, query, page, page_size, load_items) -> Dict[(str, Any)]:
    """Paginate a query.

Args: db: Database session query: Base query page: Page number (1-indexed) page_size: Number of items per page load_items: Whether to load the items or just return metadata

Returns: Dict[str, Any]: Pagination result with items, total, page, page_size, and pages

Raises: DatabaseException: If a database error occurs"""
```

```python
@contextlib.asynccontextmanager
async def transaction(db) -> AsyncGenerator[(AsyncSession, None)]:
    """Context manager for database transactions.

This ensures that operations within the context are committed together or rolled back on error, simplifying transaction management.

Args: db: Database session

Yields: AsyncSession: Database session with transaction

Raises: DatabaseException: If a database error occurs"""
```

```python
def transactional(func) -> F:
    """Decorator for managing transactions in service methods.

Ensures the method runs within a transaction and properly handles errors.

Args: func: Function to decorate

Returns: Decorated function with transaction management"""
```

```python
async def update_object(db, model, id_value, obj_in, user_id) -> Optional[T]:
    """Update a model instance by ID.

Args: db: Database session model: Model class id_value: ID value to look up obj_in: New data to update user_id: ID of the user making the update

Returns: Optional[T]: Updated instance or None if not found

Raises: DatabaseException: If a database error occurs"""
```

```python
async def upsert(db, model, data, unique_fields) -> T:
    """Insert a record or update it if it already exists.

Args: db: Database session model: Model class data: Object data unique_fields: Fields to use for uniqueness check

Returns: T: Created or updated instance

Raises: DatabaseException: If a database error occurs"""
```

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
import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.schemas.model_mapping import ModelMapping as ModelMappingSchema
from app.schemas.model_mapping import ModelMappingCreate, ModelMappingList, ModelMappingUpdate
from exceptions import ConfigurationError, DatabaseError, FitmentError, MappingError, ParsingError, ValidationError
from mapper import FitmentMappingEngine
from models import ValidationStatus
```

**Global Variables:**
```python
logger = logger = logging.getLogger(__name__)
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
@router.get('/model-mappings', response_model=ModelMappingList)
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
import logging
import os
from functools import lru_cache
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
```

**Functions:**
```python
def configure_logging() -> None:
    """Configure logging for the fitment module."""
```

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
        env_prefix="FITMENT_",
        case_sensitive=False,
        extra="ignore"
    )
```
*Methods:*
```python
@validator('vcdb_path', 'pcdb_path')
    def validate_file_path(cls, v) -> str:
        """Validate that a file path exists."""
```
```python
@validator('model_mappings_path')
    def validate_optional_file_path(cls, v) -> Optional[str]:
        """Validate that an optional file path exists if provided."""
```

##### Module: db
*Database access for fitment data.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/fitment/db.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple, Union
import pandas as pd
import pyodbc
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from models import PCDBPosition, PartTerminology, VCDBVehicle
from exceptions import DatabaseError
```

**Global Variables:**
```python
logger = logger = logging.getLogger(__name__)
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
from typing import Optional
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
import json
import logging
from dataclasses import asdict
from functools import lru_cache
from typing import Any, Dict, List, Optional, Set, Tuple, Union, cast
from db import FitmentDBService
from exceptions import MappingError
from models import PartApplication, PartFitment, PartTerminology, PCDBPosition, ValidationResult, ValidationStatus, VCDBVehicle
from parser import FitmentParser
from validator import FitmentValidator
```

**Global Variables:**
```python
logger = logger = logging.getLogger(__name__)
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
from typing import Dict, List, Optional, Set, Union, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo
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
from typing import Dict, List, Optional, Set, Tuple
from models import PartApplication, PartFitment, Position, PositionGroup, ValidationResult, ValidationStatus, Vehicle
from exceptions import ParsingError
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
import logging
from typing import Dict, List, Optional, Set, Tuple
from models import PartFitment, PartTerminology, PCDBPosition, Position, ValidationResult, ValidationStatus, VCDBVehicle
from exceptions import ValidationError
```

**Global Variables:**
```python
logger = logger = logging.getLogger(__name__)
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

#### Package: models
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/__init__.py`

**Imports:**
```python
from app.models.product import Fitment, Product, product_fitment_association
from app.models.user import Company, User, UserRole
from app.models.media import Media, MediaType, MediaVisibility, product_media_association
```

##### Module: associations
*Association tables for many-to-many relationships.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/associations.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
```

**Global Variables:**
```python
product_fitment_association = product_fitment_association = Table(
    "product_fitment",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("fitment_id", UUID(as_uuid=True), ForeignKey("fitment.id", ondelete="CASCADE"), primary_key=True),
    # Metadata
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
product_media_association = product_media_association = Table(
    "product_media",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("media_id", UUID(as_uuid=True), ForeignKey("media.id", ondelete="CASCADE"), primary_key=True),
    # Optional sequence for ordering media items
    Column("display_order", Integer, nullable=False, default=0),
    # Is this the primary/featured media for the product
    Column("is_primary", Integer, nullable=False, default=0),
    # Metadata
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
product_tariff_code_association = product_tariff_code_association = Table(
    "product_tariff_code",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("tariff_code_id", UUID(as_uuid=True), ForeignKey("tariff_code.id", ondelete="CASCADE"), primary_key=True),
    # Metadata
    Column("assigned_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
product_unspsc_association = product_unspsc_association = Table(
    "product_unspsc",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("unspsc_code_id", UUID(as_uuid=True), ForeignKey("unspsc_code.id", ondelete="CASCADE"), primary_key=True),
    # Metadata
    Column("assigned_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
product_country_origin_association = product_country_origin_association = Table(
    "product_country_origin",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("country_id", UUID(as_uuid=True), ForeignKey("country.id", ondelete="CASCADE"), primary_key=True),
    Column("manufacturer_id", UUID(as_uuid=True), ForeignKey("manufacturer.id", ondelete="SET NULL"), nullable=True),
    # Type of origin (Origin, Assembly, etc.)
    Column("origin_type", Integer, nullable=False, default=0),
    # Order for organizing countries
    Column("origin_order", Integer, nullable=False, default=0),
    # Metadata
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    # Add a unique constraint for product_id and country_id
    UniqueConstraint("product_id", "country_id", name="uix_product_country"),
)
product_hardware_association = product_hardware_association = Table(
    "product_hardware",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("hardware_id", UUID(as_uuid=True), ForeignKey("hardware_item.id", ondelete="CASCADE"), primary_key=True),
    # Number of hardware pieces included
    Column("quantity", Integer, nullable=False, default=1),
    # Is the hardware required
    Column("is_optional", Integer, nullable=False, default=0),
    # Metadata
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    # Add a unique constraint for product_id and hardware_id
    UniqueConstraint("product_id", "hardware_id", name="uix_product_hardware"),
)
product_interchange_association = product_interchange_association = Table(
    "product_interchange",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    # Interchange number (part number from another brand/supplier)
    Column("interchange_number", Integer, nullable=False),
    # Optional brand reference
    Column("brand_id", UUID(as_uuid=True), ForeignKey("brand.id", ondelete="SET NULL"), nullable=True),
    # Optional compatibility notes
    Column("notes", Integer, nullable=True),
    # Metadata
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    # Primary key is product_id and interchange_number
    UniqueConstraint("product_id", "interchange_number", "brand_id", name="uix_product_interchange"),
)
product_packaging_association = product_packaging_association = Table(
    "product_packaging",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("packaging_type_id", UUID(as_uuid=True), ForeignKey("packaging_type.id", ondelete="CASCADE"), primary_key=True),
    # Metadata
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
product_color_association = product_color_association = Table(
    "product_color",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("color_id", UUID(as_uuid=True), ForeignKey("color.id", ondelete="CASCADE"), primary_key=True),
    # Metadata
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
product_construction_type_association = product_construction_type_association = Table(
    "product_construction_type",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("construction_type_id", UUID(as_uuid=True), ForeignKey("construction_type.id", ondelete="CASCADE"), primary_key=True),
    # Metadata
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
product_texture_association = product_texture_association = Table(
    "product_texture",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("texture_id", UUID(as_uuid=True), ForeignKey("texture.id", ondelete="CASCADE"), primary_key=True),
    # Metadata
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
```

##### Module: chat
*Chat system models.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/chat.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text, Boolean, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.utils.crypto import encrypt_message, decrypt_message
from app.models.user import User, Company
```

**Classes:**
```python
class ChatMember(Base):
    """Chat room member model.

This model tracks users' membership in chat rooms: - Each member has a role (owner, admin, etc.) - Tracks when the user last read messages - Records membership status

Attributes: id: Primary key UUID room_id: Reference to chat room user_id: Reference to user role: Member role (owner, admin, member, guest) last_read_at: When the user last read messages is_active: Whether the membership is active created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'chat_member'
__table_args__ =     __table_args__ = (
        Index('idx_unique_room_user', 'room_id', 'user_id', unique=True),
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the chat member."""
```

```python
class ChatMemberRole(str, Enum):
    """Roles of chat room members.

Defines the possible roles a user can have in a chat room: - OWNER: Creator/owner with full permissions - ADMIN: Administrator with moderation rights - MEMBER: Regular participant - GUEST: Temporary participant with limited rights"""
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
    """Chat message model.

This model represents individual messages in chat rooms: - Messages support various types (text, image, etc.) - Content is encrypted for security - Tracks message status (sent, delivered, read)

Attributes: id: Primary key UUID room_id: Reference to chat room sender_id: Reference to sender user message_type: Type of message (text, image, file, system, action) content_encrypted: Encrypted message content metadata: Additional message metadata as JSON is_deleted: Whether the message has been deleted deleted_at: When the message was deleted created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'chat_message'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the chat message."""
```
```python
@content.setter
    def content(self, value) -> None:
        """Encrypt and store the message content."""
```

```python
class ChatRoom(Base):
    """Chat room model representing a conversation space.

This model defines a chat room where users can exchange messages: - Each room has a type (direct, group, etc.) - Rooms can be associated with a company - Messages are linked to rooms - Members track participants in the room

Attributes: id: Primary key UUID name: Room name (optional for direct chats) type: Room type (direct, group, company, support) company_id: Associated company (optional) is_active: Whether the room is active metadata: Additional room data as JSON created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'chat_room'
company =     company = relationship("Company", back_populates="chat_rooms")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the chat room."""
```

```python
class ChatRoomType(str, Enum):
    """Types of chat rooms supported by the system.

Defines the possible chat room configurations: - DIRECT: One-to-one chat between two users - GROUP: Group chat for multiple users - COMPANY: Company-wide chat room - SUPPORT: Customer support chat"""
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
    """Message reaction model.

This model tracks reactions to messages (like emoji reactions): - Each reaction is associated with a specific message - Users can react with emoji or predefined reactions - Multiple users can add the same reaction

Attributes: id: Primary key UUID message_id: Reference to chat message user_id: Reference to user who reacted reaction: Reaction content (emoji or predefined reaction) created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'message_reaction'
__table_args__ =     __table_args__ = (
        Index('idx_unique_message_user_reaction', 'message_id', 'user_id', 'reaction', unique=True),
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the message reaction."""
```

```python
class MessageType(str, Enum):
    """Types of messages supported by the chat system.

Defines the possible message types: - TEXT: Regular text message - IMAGE: Image attachment - FILE: File attachment - SYSTEM: System-generated message - ACTION: User action notification"""
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
    """Rate limiting log model.

This model tracks rate limiting for users to prevent spam: - Records user's message sending attempts - Used to enforce rate limits on messaging - Supports both global and room-specific limits

Attributes: id: Primary key UUID user_id: Reference to user room_id: Reference to chat room (optional) event_type: Type of event being rate limited timestamp: When the event occurred count: Number of events in the current period"""
```
*Class attributes:*
```python
__tablename__ = 'rate_limit_log'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the rate limit log."""
```

##### Module: compliance
*Compliance models.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/compliance.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, Date, DateTime, Enum as SQLAEnum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.models.product import Product
from app.models.user import User
```

**Classes:**
```python
class ApprovalStatus(str, Enum):
    """Statuses for regulatory approvals.  Defines the possible states of a regulatory approval."""
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
    """Types of chemical hazards under Proposition 65.

Defines the categories of chemical hazards recognized by California's Proposition 65."""
```
*Class attributes:*
```python
CARCINOGEN = 'Carcinogen'
REPRODUCTIVE_TOXICANT = 'Reproductive Toxicant'
BOTH = 'Both'
```

```python
class ExposureScenario(str, Enum):
    """Types of exposure scenarios for chemicals.

Defines the different contexts in which chemical exposure might occur."""
```
*Class attributes:*
```python
CONSUMER = 'Consumer'
OCCUPATIONAL = 'Occupational'
ENVIRONMENTAL = 'Environmental'
```

```python
class HazardousMaterial(Base):
    """Hazardous material model.

Represents hazardous material information for products.

Attributes: id: Primary key UUID product_id: Reference to product un_number: UN/NA Number (e.g., 1993 for flammable liquids) hazard_class: Hazard Classification (e.g., Flammable Liquid) packing_group: Packing Group (I, II, III) handling_instructions: Storage or transport precautions restricted_transport: Restrictions (Air, Ground, Sea, None) created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'hazardous_material'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the hazardous material.  Returns: str: Hazardous material representation"""
```

```python
class ProductChemical(Base):
    """Product chemical association model.

Represents relationships between products and chemicals, including exposure scenarios and warning requirements.

Attributes: id: Primary key UUID product_id: Reference to product chemical_id: Reference to chemical exposure_scenario: Scenario (Consumer, Occupational, Environmental) warning_required: Whether a warning is required warning_label: Warning text for label"""
```
*Class attributes:*
```python
__tablename__ = 'product_chemical'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product chemical association.

Returns: str: Product chemical association representation"""
```

```python
class ProductDOTApproval(Base):
    """Product DOT approval model.

Represents Department of Transportation approvals for products.

Attributes: id: Primary key UUID product_id: Reference to product approval_status: Status (Approved, Pending, Revoked, Not Required) approval_number: Official DOT approval number approved_by: Entity or agency that approved the product approval_date: When the product was approved expiration_date: If the approval has an expiration date reason: If revoked or pending, store reason changed_by_id: User who made the change changed_at: When the change occurred"""
```
*Class attributes:*
```python
__tablename__ = 'product_dot_approval'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the DOT approval.  Returns: str: DOT approval representation"""
```

```python
class Prop65Chemical(Base):
    """Proposition 65 chemical model.

Represents chemicals listed under California's Proposition 65.

Attributes: id: Primary key UUID name: Chemical name cas_number: Chemical Abstracts Service (CAS) Number type: Type of hazard (Carcinogen, Reproductive Toxicant, Both) exposure_limit: Exposure limit if applicable updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'prop65_chemical'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the chemical.  Returns: str: Chemical representation"""
```

```python
class TransportRestriction(str, Enum):
    """Types of transportation restrictions.

Defines the possible transportation restrictions for hazardous materials."""
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
    """Warning model.

Represents warning text for chemicals in products.

Attributes: id: Primary key UUID product_id: Reference to product chemical_id: Reference to chemical warning_text: Warning text last_updated: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'warning'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the warning.  Returns: str: Warning representation"""
```

##### Module: currency
*Currency models.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/currency.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
```

**Classes:**
```python
class Currency(Base):
    """Currency model.

Represents currency information: - ISO codes - Name - Symbol - Active status

Attributes: id: Primary key UUID code: ISO 4217 currency code (USD, EUR, etc.) name: Currency name symbol: Currency symbol is_active: Whether the currency is active is_base: Whether this is the base currency for the system created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'currency'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the currency.  Returns: str: Currency representation"""
```

```python
class ExchangeRate(Base):
    """Exchange rate model.

Tracks historical exchange rates between currencies: - Source and target currencies - Rate value - Effective date

Attributes: id: Primary key UUID source_currency_id: Reference to source currency target_currency_id: Reference to target currency rate: Exchange rate value effective_date: When the rate became effective fetched_at: When the rate was fetched from the API data_source: API or source that provided the rate created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'exchange_rate'
__table_args__ =     __table_args__ = (
        UniqueConstraint(
            'source_currency_id', 'target_currency_id', 'effective_date',
            name='uix_exchange_rate_source_target_date'
        ),
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the exchange rate.  Returns: str: Exchange rate representation"""
```

##### Module: location
*Location models.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/location.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, DateTime, ForeignKey, String, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.models.reference import Warehouse, TariffCode
from app.models.product import Manufacturer
from app.models.user import Company
```

**Classes:**
```python
class Address(Base):
    """Address model.

Represents physical addresses for companies, warehouses, etc.

Attributes: id: Primary key UUID street: Street address city: City name state: State or province postal_code: Postal or ZIP code country_id: Reference to country latitude: Geographical latitude longitude: Geographical longitude created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'address'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the address.  Returns: str: Address representation"""
```

```python
class Country(Base):
    """Country model.

Represents countries with ISO codes and related information.

Attributes: id: Primary key UUID name: Full country name iso_alpha_2: 2-letter country code (US, etc.) iso_alpha_3: 3-letter country code (USA, etc.) iso_numeric: Numeric country code (840, etc.) region: Region name (North America, etc.) subregion: Subregion name (Northern America, etc.) currency: Currency code (USD, etc.) created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'country'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the country.  Returns: str: Country representation"""
```

##### Module: media
*Media asset models.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/media.py`

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
from app.models.associations import product_media_association
from app.models.product import Product
from app.models.user import User
```

**Classes:**
```python
class Media(Base):
    """Media model for storing file metadata.

This model tracks uploaded files and their metadata: - Basic file information (name, path, size, type) - Access control via visibility settings - Ownership tracking - Approval workflow status - Product associations

Attributes: id: Primary key UUID filename: Original filename file_path: Path to the stored file file_size: Size of the file in bytes media_type: Type of media (image, document, video, other) mime_type: MIME type of the file visibility: Visibility level file_metadata: Additional metadata as JSON uploaded_by_id: Reference to the user who uploaded the file is_approved: Whether the file has been approved for use approved_by_id: Reference to the user who approved the file approved_at: When the file was approved products: Associated products created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'media'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the media.  Returns: str: Media representation with filename and type"""
```
```python
@property
    def extension(self) -> str:
        """Get the file extension from the filename.

Returns: str: File extension (lowercase, without leading period)"""
```
```python
@property
    def has_thumbnail(self) -> bool:
        """Check if the media should have a thumbnail.

Returns: bool: True if media is an image and should have a thumbnail"""
```
```python
@property
    def is_image(self) -> bool:
        """Check if the media is an image.  Returns: bool: True if media_type is IMAGE"""
```

```python
class MediaType(str, Enum):
    """Types of media files supported by the system.

Defines the different categories of files that can be uploaded and helps determine appropriate handling and validation rules."""
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
    """Visibility levels for media files.

Controls who can access the media files: - PUBLIC: Accessible without authentication - PRIVATE: Requires authentication - RESTRICTED: Requires specific permissions"""
```
*Class attributes:*
```python
PUBLIC = 'public'
PRIVATE = 'private'
RESTRICTED = 'restricted'
```

##### Module: model_mapping
*Model mapping database model.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/model_mapping.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
```

**Classes:**
```python
class ModelMapping(Base):
    """Model mapping database model.

This model stores mappings between part application text patterns and structured make/model data in the format "Make|VehicleCode|Model"."""
```
*Class attributes:*
```python
__tablename__ = 'model_mappings'
id =     id = Column(Integer, primary_key=True, autoincrement=True)
pattern =     pattern = Column(String(255), nullable=False, index=True)
mapping =     mapping = Column(String(255), nullable=False)
priority =     priority = Column(Integer, nullable=False, default=0)
active =     active = Column(Boolean, nullable=False, default=True)
created_at =     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
updated_at =     updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
```
*Methods:*
```python
    def __repr__(self) -> str:
        """Return string representation of model mapping."""
```
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

##### Module: product
*Product catalog models.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/product.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.models.associations import product_fitment_association, product_media_association
from app.models.media import Media
from app.models.user import User
```

**Classes:**
```python
class AttributeDefinition(Base):
    """Attribute definition model.

Defines flexible product attributes.

Attributes: id: Primary key UUID name: Attribute name code: Code for the attribute description: Description of the attribute data_type: Data type is_required: Whether the attribute is required default_value: Default value for the attribute validation_regex: Regular expression for validation min_value: Minimum value max_value: Maximum value options: For picklist values display_order: Order for displaying attributes created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'attribute_definition'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the attribute definition.

Returns: str: Attribute definition representation"""
```

```python
class Brand(Base):
    """Brand model.

Represents product brands.

Attributes: id: Primary key UUID name: Brand name parent_company_id: Reference to parent company created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'brand'
parent_company =     parent_company = relationship("Company", foreign_keys=[parent_company_id])
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the brand.  Returns: str: Brand representation"""
```

```python
class Fitment(Base):
    """Fitment model representing vehicle compatibility information.

This model stores information about vehicle compatibility for products: - Year/Make/Model data for basic vehicle identification - Engine and transmission details for specific applications - Flexible JSON attributes for additional fitment criteria

Attributes: id: Primary key UUID year: Vehicle model year make: Vehicle manufacturer model: Vehicle model name engine: Engine specification transmission: Transmission type attributes: JSON field for additional fitment attributes products: Associated products for this fitment created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'fitment'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the fitment.

Returns: str: Fitment representation with year, make, and model"""
```

```python
class Manufacturer(Base):
    """Manufacturer model.

Represents product manufacturers.

Attributes: id: Primary key UUID name: Manufacturer name company_id: Parent company if applicable address_id: Reference to address billing_address_id: Reference to billing address shipping_address_id: Reference to shipping address country_id: Manufacturing location created_at: Creation timestamp"""
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
        """String representation of the manufacturer.  Returns: str: Manufacturer representation"""
```

```python
class PriceType(Base):
    """Price type model.

Defines types of prices.

Attributes: id: Primary key UUID name: Price type name description: Description of price type created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'price_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the price type.  Returns: str: Price type representation"""
```

```python
class Product(Base):
    """Product model representing automotive parts and accessories.

This model stores core information about products including: - Basic product details (part number, application) - Product flags (vintage, late_model, soft, universal) - Search capabilities via search_vector - Relationships to descriptions, marketing, activities, etc.

Attributes: id: Primary key UUID part_number: Unique identifier for the product part_number_stripped: Alphanumeric version of part_number application: Unformatted data for vehicle fitment applications vintage: Vintage fitments flag late_model: Late model fitments flag soft: Soft good flag universal: Universal fit flag search_vector: Full-text search vector created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'product'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product.  Returns: str: Product representation with part number"""
```

```python
class ProductActivity(Base):
    """Product activity model.

Tracks status changes for products.

Attributes: id: Primary key UUID product_id: Reference to product status: Product status (active, inactive) reason: Reason for status change changed_by: User who made the change changed_at: When the change occurred"""
```
*Class attributes:*
```python
__tablename__ = 'product_activity'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product activity.  Returns: str: Product activity representation"""
```

```python
class ProductAttribute(Base):
    """Product attribute model.

Stores flexible attribute values for products.

Attributes: id: Primary key UUID product_id: Reference to product attribute_id: Reference to attribute definition value_string: String value value_number: Numeric value value_boolean: Boolean value value_date: Date value value_json: JSON value created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'product_attribute'
__table_args__ =     __table_args__ = (
        # Ensure a product can't have the same attribute twice
        UniqueConstraint('product_id', 'attribute_id', name='uix_product_attribute'),
    )
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product attribute.  Returns: str: Product attribute representation"""
```

```python
class ProductBrandHistory(Base):
    """Product brand history model.

Tracks brand changes for products.

Attributes: id: Primary key UUID product_id: Reference to product old_brand_id: Previous brand new_brand_id: New brand changed_by_id: User who made the change changed_at: When the change occurred"""
```
*Class attributes:*
```python
__tablename__ = 'product_brand_history'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product brand history.

Returns: str: Product brand history representation"""
```

```python
class ProductDescription(Base):
    """Product description model.

Stores different types of descriptions for products.

Attributes: id: Primary key UUID product_id: Reference to product description_type: Type of description (Short, Long, Keywords, etc.) description: Description content created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'product_description'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product description.  Returns: str: Product description representation"""
```

```python
class ProductMarketing(Base):
    """Product marketing model.

Stores marketing content for products.

Attributes: id: Primary key UUID product_id: Reference to product marketing_type: Type of marketing content (Bullet Point, Ad Copy) content: Marketing content position: Order for display created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'product_marketing'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product marketing.  Returns: str: Product marketing representation"""
```

```python
class ProductMeasurement(Base):
    """Product measurement model.

Stores dimensional information for products.

Attributes: id: Primary key UUID product_id: Reference to product manufacturer_id: Optional manufacturer reference length: Length in inches width: Width in inches height: Height in inches weight: Weight in pounds volume: Volume in cubic inches dimensional_weight: DIM weight calculation effective_date: When measurements become effective"""
```
*Class attributes:*
```python
__tablename__ = 'product_measurement'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product measurement.  Returns: str: Product measurement representation"""
```

```python
class ProductPricing(Base):
    """Product pricing model.

Stores pricing information for products.

Attributes: id: Primary key UUID product_id: Reference to product pricing_type_id: Reference to price type manufacturer_id: Optional manufacturer reference price: The current price currency: Currency code last_updated: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'product_pricing'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product pricing.  Returns: str: Product pricing representation"""
```

```python
class ProductStock(Base):
    """Product stock model.

Tracks inventory levels for products.

Attributes: id: Primary key UUID product_id: Reference to product warehouse_id: Reference to warehouse quantity: Quantity in stock last_updated: Last stock update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'product_stock'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product stock.  Returns: str: Product stock representation"""
```

```python
class ProductSupersession(Base):
    """Product supersession model.

Tracks product replacements.

Attributes: id: Primary key UUID old_product_id: Product being replaced new_product_id: Replacement product reason: Explanation of why the product was superseded changed_at: When the change occurred"""
```
*Class attributes:*
```python
__tablename__ = 'product_supersession'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the product supersession.

Returns: str: Product supersession representation"""
```

##### Module: reference
*Reference data models.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/reference.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.models.product import Product
```

**Classes:**
```python
class Color(Base):
    """Color model.

Represents standard color names and their hex codes.

Attributes: id: Primary key UUID name: Standard color name hex_code: Hex code for digital representation (optional) created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'color'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the color.  Returns: str: Color representation"""
```

```python
class ConstructionType(Base):
    """Construction type model.

Represents materials used in product construction.

Attributes: id: Primary key UUID name: Material name description: Optional description created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'construction_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the construction type.  Returns: str: Construction type representation"""
```

```python
class Hardware(Base):
    """Hardware item model.

Represents hardware items included with products.

Attributes: id: Primary key UUID name: Name of the hardware item description: Optional details part_number: Optional part number for the hardware item created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'hardware_item'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the hardware item.  Returns: str: Hardware item representation"""
```

```python
class PackagingType(Base):
    """Packaging type model.

Represents types of product packaging.

Attributes: id: Primary key UUID pies_code: AutoCare PCdb PIES Code (optional) name: Packaging type name description: Optional description source: Source of the data created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'packaging_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the packaging type.  Returns: str: Packaging type representation"""
```

```python
class TariffCode(Base):
    """Tariff code model.

Represents HS, HTS, or other tariff codes.

Attributes: id: Primary key UUID code: Tariff code description: Description of the code country_id: Country this code applies to (optional) created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'tariff_code'
country =     country = relationship("Country")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the tariff code.  Returns: str: Tariff code representation"""
```

```python
class Texture(Base):
    """Texture model.

Represents surface textures of products.

Attributes: id: Primary key UUID name: Texture name description: Optional description created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'texture'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the texture.  Returns: str: Texture representation"""
```

```python
class UnspscCode(Base):
    """UNSPSC code model.

Represents United Nations Standard Products and Services Code.

Attributes: id: Primary key UUID code: 8- or 10-digit UNSPSC code description: UNSPSC category description segment: High-level category family: Sub-category class: Product class commodity: Specific commodity category created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'unspsc_code'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the UNSPSC code.  Returns: str: UNSPSC code representation"""
```

```python
class Warehouse(Base):
    """Warehouse model.

Represents product storage locations.

Attributes: id: Primary key UUID name: Warehouse name address_id: Reference to address (optional) is_active: Whether the warehouse is active created_at: Creation timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'warehouse'
address =     address = relationship("Address")
stock =     stock = relationship("ProductStock", back_populates="warehouse")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the warehouse.  Returns: str: Warehouse representation"""
```

##### Module: user
*User model and authentication utilities.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/models/user.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Optional, Union
from jose import jwt
from passlib.context import CryptContext
import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.core.config import settings
from app.db.base_class import Base
```

**Global Variables:**
```python
pwd_context = pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**Functions:**
```python
def create_access_token(subject, role, expires_delta) -> str:
    """Create a JWT access token.

Args: subject: Subject (usually user ID) to include in the token role: User role to include in the token expires_delta: Token expiration time delta (optional)

Returns: str: JWT token string"""
```

```python
def get_password_hash(password) -> str:
    """Hash a password using Bcrypt.  Args: password: Plain text password  Returns: str: Hashed password"""
```

```python
def verify_password(plain_password, hashed_password) -> bool:
    """Verify a password against a hash.

Args: plain_password: Plain text password hashed_password: Bcrypt hashed password

Returns: bool: True if password matches, False otherwise"""
```

**Classes:**
```python
class Company(Base):
    """Company model for B2B customers and distributors.

This model stores information about client companies and distributors. It supports: - Account number tracking for integration with external systems - Different account types (distributor, jobber, etc.) - Address information for headquarters, billing, and shipping - Industry classification - Status tracking

Attributes: id: Primary key UUID name: Company name headquarters_address_id: Reference to headquarters address billing_address_id: Reference to billing address shipping_address_id: Reference to shipping address account_number: External account number (e.g., from iSeries) account_type: Type of account (distributor, jobber, etc.) industry: Industry sector (Automotive, Electronics, etc.) is_active: Whether the company account is active created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'company'
headquarters_address =     headquarters_address = relationship("Address", foreign_keys=[headquarters_address_id])
billing_address =     billing_address = relationship("Address", foreign_keys=[billing_address_id])
shipping_address =     shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the company.

Returns: str: Company representation with name and account type"""
```

```python
class User(Base):
    """User model for authentication and authorization.

This model stores user information, credentials, and permissions. It supports: - Email-based authentication - Role-based access control - Company association for B2B users - Account status tracking

Attributes: id: Primary key UUID email: User's email address (used for login) hashed_password: Bcrypt-hashed password full_name: User's full name role: User's role in the system is_active: Whether the user account is active company_id: Reference to associated company (optional) company: Relationship to Company model created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
__tablename__ = 'user'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """String representation of the user.  Returns: str: User representation with email and role"""
```

```python
class UserRole(str, Enum):
    """User role enumeration for authorization.

These roles define different permission levels in the system: - ADMIN: Full system access and management capabilities - MANAGER: Product and user management, approvals - CLIENT: Regular customer access - DISTRIBUTOR: B2B partner access - READ_ONLY: Limited view-only access"""
```
*Class attributes:*
```python
ADMIN = 'admin'
MANAGER = 'manager'
CLIENT = 'client'
DISTRIBUTOR = 'distributor'
READ_ONLY = 'read_only'
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
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseException
from app.core.logging import get_logger
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

**Imports:**
```python
from app.schemas.product import Fitment, FitmentCreate, FitmentInDB, FitmentListResponse, FitmentUpdate, PaginatedResponse, Product, ProductCreate, ProductInDB, ProductListResponse, ProductUpdate
from app.schemas.user import Company, CompanyCreate, CompanyInDB, CompanyUpdate, Token, TokenPayload, User, UserCreate, UserInDB, UserRole, UserUpdate
```

##### Module: chat
*Chat system Pydantic schemas.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas/chat.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
```

**Classes:**
```python
class ChatMemberSchema(BaseModel):
    """Chat room member schema.

Attributes: user_id: User identifier user_name: User display name role: Member role in the room is_online: Whether the user is currently online last_seen_at: When the user was last active"""
```

```python
class ChatMessageSchema(BaseModel):
    """Chat message schema.

Attributes: id: Message identifier room_id: Room identifier sender_id: Sender user identifier sender_name: Sender display name message_type: Type of message content: Message content reactions: Message reactions created_at: Creation timestamp updated_at: Last update timestamp is_edited: Whether the message has been edited is_deleted: Whether the message has been deleted"""
```

```python
class ChatRoomSchema(BaseModel):
    """Chat room information schema.

Attributes: id: Room identifier name: Room name type: Room type created_at: Creation timestamp member_count: Number of members in the room last_message: Last message information (optional)"""
```

```python
class CommandType(str, Enum):
    """WebSocket command types."""
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
    """Command to delete a message.  Attributes: room_id: Room identifier message_id: Message identifier"""
```

```python
class EditMessageCommand(BaseModel):
    """Command to edit a message.

Attributes: room_id: Room identifier message_id: Message identifier content: New message content"""
```

```python
class FetchHistoryCommand(BaseModel):
    """Command to fetch message history.

Attributes: room_id: Room identifier before_id: Fetch messages before this ID limit: Maximum number of messages to return"""
```

```python
class JoinRoomCommand(BaseModel):
    """Command to join a chat room.  Attributes: room_id: Room identifier"""
```

```python
class LeaveRoomCommand(BaseModel):
    """Command to leave a chat room.  Attributes: room_id: Room identifier"""
```

```python
class MessageType(str, Enum):
    """Message content types."""
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
class ReactionCommand(BaseModel):
    """Command for message reactions.

Attributes: room_id: Room identifier message_id: Message identifier reaction: Reaction content"""
```

```python
class ReadMessagesCommand(BaseModel):
    """Command to mark messages as read.

Attributes: room_id: Room identifier last_read_id: ID of the last read message"""
```

```python
class SendMessageCommand(BaseModel):
    """Command to send a message.

Attributes: room_id: Room identifier content: Message content message_type: Type of message (text, image, etc.) metadata: Additional message data"""
```

```python
class TypingCommand(BaseModel):
    """Command for typing indicators.  Attributes: room_id: Room identifier"""
```

```python
class UserPresenceSchema(BaseModel):
    """User presence information schema.

Attributes: user_id: User identifier is_online: Whether the user is currently online last_seen_at: When the user was last active status: Custom status message"""
```

```python
class WebSocketCommand(BaseModel):
    """Base WebSocket command structure.

This model defines the common structure for all WebSocket commands: - Command type to identify the action - Optional room identifier - Command data with type-specific content"""
```

```python
class WebSocketResponse(BaseModel):
    """Base WebSocket response structure.

This model defines the common structure for all WebSocket responses: - Response type for client handling - Optional error information - Response data with type-specific content"""
```

##### Module: currency
*Currency schemas.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas/currency.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
```

**Classes:**
```python
class ConversionRequest(BaseModel):
    """Schema for currency conversion requests."""
```
*Methods:*
```python
@field_validator('source_currency', 'target_currency')
@classmethod
    def validate_currency_code(cls, v) -> str:
        """Validate currency code format."""
```

```python
class ConversionResponse(BaseModel):
    """Schema for currency conversion responses."""
```

```python
class CurrencyBase(BaseModel):
    """Base model for currency data."""
```

```python
class CurrencyCreate(CurrencyBase):
    """Schema for creating a new currency."""
```

```python
class CurrencyRead(CurrencyBase):
    """Schema for reading currency data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class CurrencyUpdate(BaseModel):
    """Schema for updating a currency."""
```

```python
class ExchangeRateBase(BaseModel):
    """Base model for exchange rate data."""
```

```python
class ExchangeRateCreate(ExchangeRateBase):
    """Schema for creating a new exchange rate."""
```

```python
class ExchangeRateRead(ExchangeRateBase):
    """Schema for reading exchange rate data."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

##### Module: media
*Media asset schemas.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas/media.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.config import settings
from app.models.media import MediaType, MediaVisibility
```

**Classes:**
```python
class FileUploadError(BaseModel):
    """Error response for file upload.

This schema defines the structure of error responses for file uploads.

Attributes: error: Error type detail: Detailed error information (optional)"""
```

```python
class FileUploadResponse(BaseModel):
    """Response after file upload.

This schema defines the structure of responses to file uploads.

Attributes: media: Media information message: Success message"""
```

```python
class Media(MediaInDB):
    """Schema for Media responses.

This schema is used for API responses returning media data. It extends the database schema with URLs for frontend use.

Attributes: url: URL to access the file thumbnail_url: URL to access the thumbnail (optional)"""
```
*Methods:*
```python
    def model_post_init(self, __context) -> None:
        """Post initialization hook to set URLs.

This method runs after the model is initialized, allowing us to set the URL fields based on the media properties.

Args: __context: Context information (not used)"""
```

```python
class MediaBase(BaseModel):
    """Base schema for Media data.

Defines common fields used across media-related schemas.

Attributes: filename: Original file name media_type: Type of media (image, document, video, other) visibility: Visibility level file_metadata: Additional file metadata"""
```

```python
class MediaCreate(BaseModel):
    """Schema for creating new Media (separate from file upload).

This schema is used for the form data part of media uploads, separate from the actual file data.

Attributes: media_type: Type of media visibility: Visibility level file_metadata: Additional file metadata"""
```

```python
class MediaInDB(MediaBase):
    """Schema for Media as stored in the database.

Extends the base media schema with database-specific fields.

Attributes: id: Media UUID file_path: Path to the stored file file_size: Size of the file in bytes mime_type: MIME type of the file uploaded_by_id: Reference to user who uploaded the file is_approved: Whether the media is approved approved_by_id: Reference to user who approved the media (optional) approved_at: Approval timestamp (optional) created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class MediaListResponse(BaseModel):
    """Paginated response for media listings.

This schema provides a structure for paginated media list responses.

Attributes: items: List of media items total: Total number of items page: Current page number page_size: Number of items per page pages: Total number of pages"""
```

```python
class MediaUpdate(BaseModel):
    """Schema for updating existing Media.

Defines fields that can be updated on a media asset, with all fields being optional to allow partial updates.

Attributes: filename: Original file name (optional) media_type: Type of media (optional) visibility: Visibility level (optional) file_metadata: Additional file metadata (optional) is_approved: Whether the media is approved (optional)"""
```

##### Module: model_mapping
*Model mapping schemas for API input/output.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas/model_mapping.py`

**Imports:**
```python
from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
```

**Classes:**
```python
class Config(object):
    """Pydantic configuration."""
```
*Class attributes:*
```python
from_attributes = True
```

```python
class ModelMapping(ModelMappingBase):
    """Schema for a model mapping response."""
```

```python
class ModelMappingBase(BaseModel):
    """Base model mapping schema."""
```
*Methods:*
```python
@field_validator('mapping')
    def validate_mapping_format(cls, v) -> str:
        """Validate that mapping has the correct format (Make|VehicleCode|Model)."""
```

```python
class ModelMappingCreate(ModelMappingBase):
    """Schema for creating a new model mapping."""
```

```python
class ModelMappingList(BaseModel):
    """Schema for a list of model mappings."""
```

```python
class ModelMappingUpdate(BaseModel):
    """Schema for updating an existing model mapping."""
```
*Methods:*
```python
@field_validator('mapping')
    def validate_mapping_format(cls, v) -> Optional[str]:
        """Validate that mapping has the correct format if provided."""
```

##### Module: pagination
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas/pagination.py`

**Imports:**
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from fastapi import Query
from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel
```

**Global Variables:**
```python
T = T = TypeVar("T")
```

**Functions:**
```python
def cursor_pagination_params(cursor, limit, sort) -> CursorPaginationParams:
    """FastAPI dependency for cursor-based pagination parameters.

Args: cursor: Pagination cursor limit: Maximum number of items to return sort: Sort fields

Returns: CursorPaginationParams: Parsed pagination parameters"""
```

```python
def offset_pagination_params(page, page_size, sort) -> OffsetPaginationParams:
    """FastAPI dependency for offset-based pagination parameters.

Args: page: Page number page_size: Number of items per page sort: Sort fields

Returns: OffsetPaginationParams: Parsed pagination parameters"""
```

**Classes:**
```python
class CursorPaginationParams(BaseModel):
    """Cursor-based pagination parameters.

Attributes: cursor: Cursor for pagination limit: Maximum number of items to return sort: Fields to sort by"""
```
*Methods:*
```python
@validator('sort', pre=True)
    def parse_sort(cls, value) -> Optional[List[SortField]]:
        """Parse sort parameter from various input formats.

Same behavior as in OffsetPaginationParams.

Args: value: Sort parameter in various formats

Returns: Optional[List[SortField]]: Parsed sort fields"""
```

```python
class OffsetPaginationParams(BaseModel):
    """Offset-based pagination parameters.

Attributes: page: Page number (1-indexed) page_size: Number of items per page sort: Fields to sort by"""
```
*Methods:*
```python
@validator('sort', pre=True)
    def parse_sort(cls, value) -> Optional[List[SortField]]:
        """Parse sort parameter from various input formats.

Supports: - Single string: "field" or "field:asc" - List of strings: ["field1", "field2:desc"] - Already parsed list of SortField

Args: value: Sort parameter in various formats

Returns: Optional[List[SortField]]: Parsed sort fields"""
```

```python
class PaginationResult(GenericModel, Generic[T]):
    """Result of a paginated query.

Attributes: items: Items in the current page total: Total number of items page: Current page number (for offset pagination) page_size: Items per page (for offset pagination) pages: Total number of pages (for offset pagination) next_cursor: Cursor for next page (for cursor pagination) prev_cursor: Cursor for previous page (for cursor pagination) has_next: Whether there are more items has_prev: Whether there are previous items"""
```

```python
class SortDirection(str, Enum):
    """Sort direction for query results."""
```
*Class attributes:*
```python
ASC = 'asc'
DESC = 'desc'
```

```python
class SortField(BaseModel):
    """Sort field configuration.  Attributes: field: Field name to sort by direction: Sort direction"""
```
*Methods:*
```python
@classmethod
    def from_string(cls, sort_string) -> 'SortField':
        """Create a sort field from a string.

The string format is: field_name[:asc|desc] If direction is not specified, it defaults to ASC.

Args: sort_string: String representing sort field and direction

Returns: SortField: Sort field configuration"""
```

##### Module: product
*Product catalog schemas.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas/product.py`

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
    """Schema for Brand responses.

This schema is used for API responses returning brand data.

Attributes: parent_company: Parent company information (optional)"""
```

```python
class BrandBase(BaseModel):
    """Base schema for Brand data.

Defines common fields used across brand schemas.

Attributes: name: Brand name parent_company_id: Parent company ID (optional)"""
```

```python
class BrandCreate(BrandBase):
    """Schema for creating a new Brand.  Extends the base brand schema for creation requests."""
```

```python
class BrandInDB(BrandBase):
    """Schema for Brand as stored in the database.

Extends the base brand schema with database-specific fields.

Attributes: id: Brand UUID created_at: Creation timestamp"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BrandUpdate(BaseModel):
    """Schema for updating an existing Brand.

Defines fields that can be updated on a brand.

Attributes: name: Brand name (optional) parent_company_id: Parent company ID (optional)"""
```

```python
class DescriptionType(str, Enum):
    """Types of product descriptions.

Defines the different categories of descriptions that can be associated with a product."""
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
    """Schema for Fitment responses.  This schema is used for API responses returning fitment data."""
```

```python
class FitmentBase(BaseModel):
    """Base schema for Fitment data.

Defines common fields used across fitment-related schemas.

Attributes: year: Vehicle model year make: Vehicle manufacturer model: Vehicle model name engine: Engine specification (optional) transmission: Transmission type (optional) attributes: Additional fitment attributes"""
```
*Methods:*
```python
@field_validator('year')
@classmethod
    def validate_year(cls, v) -> int:
        """Validate the year is within a reasonable range.

Args: v: Year value

Returns: int: Validated year

Raises: ValueError: If year is outside reasonable range"""
```

```python
class FitmentCreate(FitmentBase):
    """Schema for creating a new Fitment.  Extends the base fitment schema for creation requests."""
```

```python
class FitmentInDB(FitmentBase):
    """Schema for Fitment as stored in the database.

Extends the base fitment schema with database-specific fields.

Attributes: id: Fitment UUID created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FitmentListResponse(PaginatedResponse):
    """Paginated response for fitment listings.

This schema specializes the generic paginated response for fitment listings.

Attributes: items: List of fitments"""
```

```python
class FitmentUpdate(BaseModel):
    """Schema for updating an existing Fitment.

Defines fields that can be updated on a fitment, with all fields being optional to allow partial updates.

Attributes: year: Vehicle model year (optional) make: Vehicle manufacturer (optional) model: Vehicle model name (optional) engine: Engine specification (optional) transmission: Transmission type (optional) attributes: Additional fitment attributes (optional)"""
```
*Methods:*
```python
@field_validator('year')
@classmethod
    def validate_year(cls, v) -> Optional[int]:
        """Validate the year is within a reasonable range if provided.

Args: v: Year value (optional)

Returns: Optional[int]: Validated year

Raises: ValueError: If year is outside reasonable range"""
```

```python
class MarketingType(str, Enum):
    """Types of product marketing content.

Defines the different categories of marketing content that can be associated with a product."""
```
*Class attributes:*
```python
BULLET_POINT = 'Bullet Point'
AD_COPY = 'Ad Copy'
```

```python
class PaginatedResponse(BaseModel):
    """Generic paginated response schema.

This schema provides a structure for paginated list responses, including metadata about the pagination.

Attributes: items: List of items total: Total number of items page: Current page number page_size: Number of items per page pages: Total number of pages"""
```

```python
class Product(ProductInDB):
    """Schema for Product responses.

This schema is used for API responses returning product data. It extends the database schema with related entities.

Attributes: descriptions: List of product descriptions marketing: List of marketing content activities: List of product activities superseded_by: List of products this product is superseded by supersedes: List of products this product supersedes measurements: List of product measurements stock: List of product stock information"""
```

```python
class ProductActivity(ProductActivityInDB):
    """Schema for Product Activity responses.

This schema is used for API responses returning product activity data.

Attributes: changed_by: User who made the change (optional)"""
```

```python
class ProductActivityBase(BaseModel):
    """Base schema for Product Activity data.

Defines common fields used across product activity schemas.

Attributes: status: Product status reason: Reason for status change (optional)"""
```

```python
class ProductActivityCreate(ProductActivityBase):
    """Schema for creating a new Product Activity.

Extends the base product activity schema for creation requests."""
```

```python
class ProductActivityInDB(ProductActivityBase):
    """Schema for Product Activity as stored in the database.

Extends the base product activity schema with database-specific fields.

Attributes: id: Activity UUID product_id: Product UUID changed_by_id: User UUID who made the change (optional) changed_at: When the change occurred"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductBase(BaseModel):
    """Base schema for Product data.

Defines common fields used across product schemas.

Attributes: part_number: Unique identifier for the product part_number_stripped: Alphanumeric version of part_number (auto-generated) application: Unformatted data for vehicle fitment applications (optional) vintage: Vintage fitments flag late_model: Late model fitments flag soft: Soft good flag universal: Universal fit flag is_active: Whether the product is active"""
```
*Methods:*
```python
@model_validator(mode='after')
    def generate_part_number_stripped(self) -> 'ProductBase':
        """Generate the stripped part number if not provided.  Returns: ProductBase: Validated model instance"""
```

```python
class ProductCreate(ProductBase):
    """Schema for creating a new Product.

Extends the base product schema for creation requests.

Attributes: descriptions: List of product descriptions (optional) marketing: List of marketing content (optional)"""
```

```python
class ProductDescription(ProductDescriptionInDB):
    """Schema for Product Description responses.

This schema is used for API responses returning product description data."""
```

```python
class ProductDescriptionBase(BaseModel):
    """Base schema for Product Description data.

Defines common fields used across product description schemas.

Attributes: description_type: Type of description description: Description content"""
```

```python
class ProductDescriptionCreate(ProductDescriptionBase):
    """Schema for creating a new Product Description.

Extends the base product description schema for creation requests."""
```

```python
class ProductDescriptionInDB(ProductDescriptionBase):
    """Schema for Product Description as stored in the database.

Extends the base product description schema with database-specific fields.

Attributes: id: Description UUID product_id: Product UUID created_at: Creation timestamp"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductDescriptionUpdate(BaseModel):
    """Schema for updating an existing Product Description.

Defines fields that can be updated on a product description.

Attributes: description_type: Type of description (optional) description: Description content (optional)"""
```

```python
class ProductInDB(ProductBase):
    """Schema for Product as stored in the database.

Extends the base product schema with database-specific fields.

Attributes: id: Product UUID created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductListResponse(PaginatedResponse):
    """Paginated response for product listings.

This schema specializes the generic paginated response for product listings.

Attributes: items: List of products"""
```

```python
class ProductMarketing(ProductMarketingInDB):
    """Schema for Product Marketing responses.

This schema is used for API responses returning product marketing data."""
```

```python
class ProductMarketingBase(BaseModel):
    """Base schema for Product Marketing data.

Defines common fields used across product marketing schemas.

Attributes: marketing_type: Type of marketing content content: Marketing content position: Order for display (optional)"""
```

```python
class ProductMarketingCreate(ProductMarketingBase):
    """Schema for creating a new Product Marketing.

Extends the base product marketing schema for creation requests."""
```

```python
class ProductMarketingInDB(ProductMarketingBase):
    """Schema for Product Marketing as stored in the database.

Extends the base product marketing schema with database-specific fields.

Attributes: id: Marketing UUID product_id: Product UUID created_at: Creation timestamp"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductMarketingUpdate(BaseModel):
    """Schema for updating an existing Product Marketing.

Defines fields that can be updated on product marketing content.

Attributes: marketing_type: Type of marketing content (optional) content: Marketing content (optional) position: Order for display (optional)"""
```

```python
class ProductMeasurement(ProductMeasurementInDB):
    """Schema for Product Measurement responses.

This schema is used for API responses returning product measurement data.

Attributes: manufacturer: Manufacturer information (optional)"""
```

```python
class ProductMeasurementBase(BaseModel):
    """Base schema for Product Measurement data.

Defines common fields used across product measurement schemas.

Attributes: manufacturer_id: Manufacturer UUID (optional) length: Length in inches (optional) width: Width in inches (optional) height: Height in inches (optional) weight: Weight in pounds (optional) volume: Volume in cubic inches (optional) dimensional_weight: DIM weight calculation (optional)"""
```

```python
class ProductMeasurementCreate(ProductMeasurementBase):
    """Schema for creating a new Product Measurement.

Extends the base product measurement schema for creation requests."""
```

```python
class ProductMeasurementInDB(ProductMeasurementBase):
    """Schema for Product Measurement as stored in the database.

Extends the base product measurement schema with database-specific fields.

Attributes: id: Measurement UUID product_id: Product UUID effective_date: When measurements become effective"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductMeasurementUpdate(ProductMeasurementBase):
    """Schema for updating an existing Product Measurement.

Fields are the same as the base schema since all are optional."""
```

```python
class ProductStatus(str, Enum):
    """Product status options.  Defines the possible status values for product activities."""
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
    """Schema for Product Stock responses.

This schema is used for API responses returning product stock data.

Attributes: warehouse: Warehouse information"""
```

```python
class ProductStockBase(BaseModel):
    """Base schema for Product Stock data.

Defines common fields used across product stock schemas.

Attributes: warehouse_id: Warehouse UUID quantity: Quantity in stock"""
```

```python
class ProductStockCreate(ProductStockBase):
    """Schema for creating a new Product Stock.

Extends the base product stock schema for creation requests."""
```

```python
class ProductStockInDB(ProductStockBase):
    """Schema for Product Stock as stored in the database.

Extends the base product stock schema with database-specific fields.

Attributes: id: Stock UUID product_id: Product UUID last_updated: Last stock update timestamp"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductStockUpdate(BaseModel):
    """Schema for updating an existing Product Stock.

Defines fields that can be updated on product stock.

Attributes: quantity: Quantity in stock (optional)"""
```

```python
class ProductSupersession(ProductSupersessionInDB):
    """Schema for Product Supersession responses.

This schema is used for API responses returning product supersession data.

Attributes: old_product: Basic information about the product being replaced new_product: Basic information about the replacement product"""
```

```python
class ProductSupersessionBase(BaseModel):
    """Base schema for Product Supersession data.

Defines common fields used across product supersession schemas.

Attributes: old_product_id: Product being replaced new_product_id: Replacement product reason: Explanation of why the product was superseded (optional)"""
```

```python
class ProductSupersessionCreate(ProductSupersessionBase):
    """Schema for creating a new Product Supersession.

Extends the base product supersession schema for creation requests."""
```

```python
class ProductSupersessionInDB(ProductSupersessionBase):
    """Schema for Product Supersession as stored in the database.

Extends the base product supersession schema with database-specific fields.

Attributes: id: Supersession UUID changed_at: When the change occurred"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductSupersessionUpdate(BaseModel):
    """Schema for updating an existing Product Supersession.

Defines fields that can be updated on a product supersession.

Attributes: reason: Explanation of why the product was superseded (optional)"""
```

```python
class ProductUpdate(BaseModel):
    """Schema for updating an existing Product.

Defines fields that can be updated on a product, with all fields being optional to allow partial updates.

Attributes: part_number: Unique identifier for the product (optional) application: Unformatted data for vehicle fitment applications (optional) vintage: Vintage fitments flag (optional) late_model: Late model fitments flag (optional) soft: Soft good flag (optional) universal: Universal fit flag (optional) is_active: Whether the product is active (optional)"""
```

##### Module: responses
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas/responses.py`

**Imports:**
```python
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
```

**Global Variables:**
```python
T = T = TypeVar("T")
```

**Classes:**
```python
class MetaData(BaseModel):
    """Response metadata.

Attributes: pagination: Pagination metadata request_id: Request ID for tracking extra: Additional metadata"""
```

```python
class PaginatedResponse(Response, Generic[T]):
    """Paginated API response.

This is a specialized response model for paginated results.

Attributes: data: List of items meta: Response metadata with pagination"""
```
*Methods:*
```python
@classmethod
    def from_pagination_result(cls, items, pagination, message, code, meta, request_id) -> 'PaginatedResponse[T]':
        """Create a paginated response from pagination result.

Args: items: List of items pagination: Pagination metadata message: Success message code: HTTP status code meta: Additional metadata request_id: Request ID for tracking

Returns: PaginatedResponse[T]: Paginated response"""
```

```python
class PaginationMeta(BaseModel):
    """Pagination metadata.

Attributes: page: Current page number page_size: Number of items per page total_items: Total number of items total_pages: Total number of pages has_next: Whether there are more pages has_prev: Whether there are previous pages"""
```
*Methods:*
```python
@classmethod
    def from_pagination_result(cls, result) -> 'PaginationMeta':
        """Create pagination metadata from pagination result.

Args: result: Pagination result from service

Returns: PaginationMeta: Pagination metadata"""
```

```python
class Response(GenericModel, Generic[T]):
    """Standard API response envelope.

All API responses are wrapped in this model to ensure a consistent format.

Attributes: status: Response status information data: Response data meta: Response metadata"""
```
*Methods:*
```python
@classmethod
    def error(cls, message, code, data, meta, request_id) -> 'Response[T]':
        """Create an error response.

Args: message: Error message code: HTTP status code data: Error data meta: Additional metadata request_id: Request ID for tracking

Returns: Response[T]: Error response"""
```
```python
@classmethod
    def success(cls, data, message, code, meta, pagination, request_id) -> 'Response[T]':
        """Create a success response.

Args: data: Response data message: Success message code: HTTP status code meta: Additional metadata pagination: Pagination metadata request_id: Request ID for tracking

Returns: Response[T]: Success response"""
```

```python
class ResponseStatus(BaseModel):
    """Response status information.

Attributes: success: Whether the request was successful code: HTTP status code message: Status message timestamp: Response timestamp"""
```

##### Module: user
*User data schemas.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/schemas/user.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
```

**Classes:**
```python
class Company(CompanyInDB):
    """Schema for Company responses.

This schema is used for API responses returning company data. It extends the database schema with any additional computed fields."""
```

```python
class CompanyBase(BaseModel):
    """Base schema for Company data.

Defines common fields used across company-related schemas.

Attributes: name: Company name account_number: External account number (optional) account_type: Type of account is_active: Whether the account is active"""
```

```python
class CompanyCreate(CompanyBase):
    """Schema for creating a new Company.  Extends the base company schema for creation requests."""
```

```python
class CompanyInDB(CompanyBase):
    """Schema for Company as stored in the database.

Extends the base company schema with database-specific fields.

Attributes: id: Company UUID created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class CompanyUpdate(BaseModel):
    """Schema for updating an existing Company.

Defines fields that can be updated on a company, with all fields being optional to allow partial updates.

Attributes: name: Company name (optional) account_number: External account number (optional) account_type: Type of account (optional) is_active: Whether the account is active (optional)"""
```

```python
class Token(BaseModel):
    """Token schema for authentication responses.

This schema defines the structure of token responses sent to clients after successful authentication.

Attributes: access_token: JWT access token token_type: Token type (usually "bearer")"""
```

```python
class TokenPayload(BaseModel):
    """Token payload schema.

This schema defines the structure of the JWT token payload for validation and extraction of token data.

Attributes: sub: User ID (subject) exp: Expiration timestamp role: User role iat: Issued at timestamp (optional)"""
```

```python
class User(UserInDB):
    """Schema for User responses.

This schema is used for API responses returning user data. It extends the database schema with the associated company.

Attributes: company: Associated company information (optional)"""
```

```python
class UserBase(BaseModel):
    """Base schema for User data.

Defines common fields used across user-related schemas.

Attributes: email: User email address full_name: User's full name role: User role is_active: Whether the user account is active company_id: Reference to associated company (optional)"""
```

```python
class UserCreate(UserBase):
    """Schema for creating a new User.

Extends the base user schema with password field for user creation.

Attributes: password: User password (min length: 8)"""
```

```python
class UserInDB(UserBase):
    """Schema for User as stored in the database.

Extends the base user schema with database-specific fields.

Attributes: id: User UUID created_at: Creation timestamp updated_at: Last update timestamp"""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class UserRole(str, Enum):
    """User role enumeration.

Defines the possible roles a user can have in the system, determining their access privileges."""
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
    """Schema for updating an existing User.

Defines fields that can be updated on a user, with all fields being optional to allow partial updates.

Attributes: email: User email address (optional) full_name: User's full name (optional) password: User password (optional, min length: 8) role: User role (optional) is_active: Whether the user account is active (optional) company_id: Reference to associated company (optional, can be set to None)"""
```
*Methods:*
```python
@validator('password')
    def password_strength(cls, v) -> Optional[str]:
        """Validate password strength.

Args: v: Password value

Returns: Optional[str]: Validated password

Raises: ValueError: If password doesn't meet strength requirements"""
```

#### Package: services
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services`

**__init__.py:**
*Service layer for the application.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/__init__.py`

**Imports:**
```python
from __future__ import annotations
import logging
from typing import Any, Dict, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import get_logger
from app.services.test_service import TestService
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.services.chat import ChatService
```

**Global Variables:**
```python
logger = logger = get_logger('app.services')
service_registry = service_registry = ServiceRegistry()
```

**Functions:**
```python
def get_chat_service(db) -> ChatService:
    """Get a ChatService instance.

This factory function provides a clean way to get a ChatService instance without directly depending on the ChatService implementation.

Args: db: Database session to pass to the ChatService constructor

Returns: ChatService: A new ChatService instance

Raises: ValueError: If the ChatService is not registered in the ServiceRegistry"""
```

```python
def get_test_service() -> TestService:
    """Get a TestService instance.  Returns: TestService: A new TestService instance"""
```

**Classes:**
```python
class ServiceRegistry(object):
    """Registry for application services.

This class implements the Singleton pattern to provide a central registry for all services in the application. Services can be registered and retrieved by name."""
```
*Methods:*
```python
    def __new__(cls, *args, **kwargs):
        """Create a singleton instance of the ServiceRegistry.

Returns: ServiceRegistry: The singleton instance"""
```
```python
@classmethod
    def get(cls, name, db) -> Any:
        """Get a service instance by name.

Args: name: Name of the service to retrieve db: Database session to pass to the service constructor

Returns: An instance of the requested service

Raises: ValueError: If the service name is not found in the registry"""
```
```python
@classmethod
    def get_all(cls, db) -> Dict[(str, Any)]:
        """Get instances of all registered services.

Args: db: Database session to pass to the service constructors

Returns: Dictionary mapping service names to service instances"""
```
```python
@classmethod
    def register(cls, service_class, name) -> None:
        """Register a service class.

Args: service_class: The service class to register name: Optional name for the service. If not provided, the class name is used."""
```

##### Module: base
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/base.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, cast
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import BusinessLogicException, DatabaseException, ErrorCode, PermissionDeniedException, ResourceAlreadyExistsException, ResourceNotFoundException, ValidationException
from app.core.logging import get_logger
from app.core.permissions import Permission, PermissionChecker
from app.db.base_class import Base
from app.db.utils import count_query, transaction, transactional
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.pagination import CursorPaginationParams, OffsetPaginationParams, PaginationResult
from app.services.interfaces import CrudServiceInterface
from app.services.pagination import PaginationService
from app.utils.errors import ensure_not_none, resource_already_exists, resource_not_found, validation_error
```

**Global Variables:**
```python
T = T = TypeVar("T", bound=Base)  # SQLAlchemy model
C = C = TypeVar("C", bound=BaseModel)  # Create schema
U = U = TypeVar("U", bound=BaseModel)  # Update schema
R = R = TypeVar("R", bound=BaseModel)  # Response schema
ID = ID = TypeVar("ID")  # ID type
logger = logger = get_logger("app.services.base")
```

**Classes:**
```python
class BaseService(Generic[(T, C, U, R, ID)], CrudServiceInterface[(T, ID, C, U, R)]):
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
@transactional
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
@transactional
    async def delete(self, id, user_id, hard_delete) -> bool:
        """Delete entity.

Args: id: Entity ID user_id: Current user ID hard_delete: Whether to permanently delete

Returns: bool: True if deleted

Raises: ResourceNotFoundException: If entity not found PermissionDeniedException: If user doesn't have permission"""
```
```python
@transactional
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
@transactional
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
@transactional
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

##### Module: cache_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/cache_service.py`

**Imports:**
```python
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, TypeVar
from app.core.cache.decorators import cache_aside, cached, invalidate_cache, memoize
from app.core.cache.keys import generate_cache_key, generate_list_key, generate_model_key, generate_query_key
from app.core.cache.manager import cache_manager
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
```

**Global Variables:**
```python
T = T = TypeVar('T')
logger = logger = get_logger("app.services.cache_service")
```

**Classes:**
```python
class CacheService(object):
    """Service for caching operations.

This service provides a high-level interface for caching operations, with support for model caching, query caching, and more."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the cache service."""
```
```python
    async def get_model(self, model_name, model_id, backend) -> Optional[Dict[(str, Any)]]:
        """Get a model instance from the cache.

Args: model_name: Model name model_id: Model ID backend: Cache backend to use

Returns: Optional[Dict[str, Any]]: Cached model instance or None if not found"""
```
```python
    async def get_model_list(self, model_name, filters, backend) -> Optional[List[Dict[(str, Any)]]]:
        """Get a list of model instances from the cache.

Args: model_name: Model name filters: Optional filters backend: Cache backend to use

Returns: Optional[List[Dict[str, Any]]]: Cached list or None if not found"""
```
```python
    async def get_or_set(self, key, default_factory, ttl, backend) -> Any:
        """Get a value from the cache or set it if not found.

Args: key: Cache key default_factory: Function to call to get default value ttl: Time-to-live in seconds backend: Cache backend to use

Returns: Any: Cached value or default value"""
```
```python
    async def get_or_set_async(self, key, default_factory, ttl, backend) -> Any:
        """Get a value from the cache or set it if not found (async version).

Args: key: Cache key default_factory: Async function to call to get default value ttl: Time-to-live in seconds backend: Cache backend to use

Returns: Any: Cached value or default value"""
```
```python
    async def get_query(self, query_name, params, backend) -> Optional[Any]:
        """Get a query result from the cache.

Args: query_name: Query name params: Optional query parameters backend: Cache backend to use

Returns: Optional[Any]: Cached query result or None if not found"""
```
```python
    async def initialize(self) -> None:
        """Initialize service resources."""
```
```python
    async def invalidate_model(self, model_name, model_id, backend) -> bool:
        """Invalidate a model instance in the cache.

Args: model_name: Model name model_id: Model ID backend: Cache backend to use

Returns: bool: True if successful, False otherwise"""
```
```python
    async def invalidate_model_list(self, model_name, backend) -> int:
        """Invalidate all lists of a model in the cache.

Args: model_name: Model name backend: Cache backend to use

Returns: int: Number of keys invalidated"""
```
```python
    async def invalidate_query(self, query_name, backend) -> int:
        """Invalidate all results of a query in the cache.

Args: query_name: Query name backend: Cache backend to use

Returns: int: Number of keys invalidated"""
```
```python
    async def set_model(self, model_name, model_id, data, ttl, backend) -> bool:
        """Set a model instance in the cache.

Args: model_name: Model name model_id: Model ID data: Model data ttl: Time-to-live in seconds backend: Cache backend to use

Returns: bool: True if successful, False otherwise"""
```
```python
    async def set_model_list(self, model_name, data, filters, ttl, backend) -> bool:
        """Set a list of model instances in the cache.

Args: model_name: Model name data: List data filters: Optional filters ttl: Time-to-live in seconds backend: Cache backend to use

Returns: bool: True if successful, False otherwise"""
```
```python
    async def set_query(self, query_name, data, params, ttl, backend) -> bool:
        """Set a query result in the cache.

Args: query_name: Query name data: Query result params: Optional query parameters ttl: Time-to-live in seconds backend: Cache backend to use

Returns: bool: True if successful, False otherwise"""
```
```python
    async def shutdown(self) -> None:
        """Release service resources."""
```

##### Module: chat
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/chat.py`

**Imports:**
```python
from __future__ import annotations
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from sqlalchemy import and_, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.core.exceptions import AuthenticationException, BusinessLogicException, ResourceNotFoundException, ValidationException
from app.core.logging import get_logger
from app.db.session import get_db_context
from app.models.chat import ChatMember, ChatMemberRole, ChatMessage, ChatRoom, ChatRoomType, MessageReaction, MessageType
from app.models.user import User
from app.utils.crypto import decrypt_message, encrypt_message
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.chat")
```

**Classes:**
```python
class ChatService(object):
    """Service for chat-related operations.

This service handles all chat operations including: - Chat rooms (create, update, delete) - Chat messages (create, update, delete) - Chat members (add, remove, update roles) - Reactions (add, remove) - Reading status (mark as read, get unread count)"""
```
*Methods:*
```python
    def __init__(self, db):
        """Initialize the chat service.  Args: db: AsyncSession for database operations"""
```
```python
    async def check_message_permission(self, message_id, user_id, require_admin) -> bool:
        """Check if a user has permission to modify a message.

Args: message_id: ID of the message user_id: ID of the user require_admin: Whether to require admin permissions

Returns: True if the user has permission, False otherwise"""
```
```python
    async def check_room_access(self, user_id, room_id) -> bool:
        """Check if a user has access to a room.

Args: user_id: ID of the user room_id: ID of the room

Returns: True if the user has access, False otherwise"""
```
```python
    async def create_message(self, room_id, sender_id, content, message_type, metadata) -> ChatMessage:
        """Create a new chat message.

Args: room_id: ID of the chat room sender_id: ID of the message sender content: Message content message_type: Type of message (text, image, file, etc.) metadata: Additional metadata for the message

Returns: The created message

Raises: ValidationException: If message parameters are invalid BusinessLogicException: If message creation fails"""
```
```python
    async def create_room(self, name, room_type, creator_id, company_id, members) -> ChatRoom:
        """Create a new chat room.

Args: name: Name of the chat room room_type: Type of chat room (direct, group, company) creator_id: ID of the user creating the room company_id: Optional company ID for company rooms members: Optional list of members to add (with user_id and role)

Returns: The newly created chat room

Raises: ValidationException: If room parameters are invalid"""
```
```python
    async def delete_message(self, message_id) -> bool:
        """Delete a chat message.

Args: message_id: ID of the message to delete

Returns: True if successful, False otherwise

Raises: BusinessLogicException: If message deletion fails"""
```
```python
    async def edit_message(self, message_id, content) -> Tuple[(bool, Optional[ChatMessage])]:
        """Edit an existing chat message.

Args: message_id: ID of the message to edit content: New content for the message

Returns: Tuple of (success, updated message or None)

Raises: BusinessLogicException: If message editing fails"""
```
```python
    async def get_message_history(self, room_id, before_id, limit) -> List[Dict[(str, Any)]]:
        """Get message history for a room.

Args: room_id: ID of the room before_id: Get messages before this ID (for pagination) limit: Maximum number of messages to return

Returns: List of message data dictionaries

Raises: BusinessLogicException: If retrieving message history fails"""
```
```python
    async def get_room(self, room_id) -> Optional[ChatRoom]:
        """Get a chat room by ID.

Args: room_id: ID of the chat room

Returns: The chat room if found, None otherwise"""
```
```python
    async def get_room_with_members(self, room_id) -> Optional[ChatRoom]:
        """Get a chat room with its members.

Args: room_id: ID of the chat room

Returns: The chat room with members if found, None otherwise"""
```
```python
@classmethod
    def register(cls) -> None:
        """Register this service with the service registry."""
```

##### Module: currency_service
*Currency service for fetching and managing exchange rates.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/currency_service.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import httpx
from sqlalchemy import desc, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.session import get_db_context
from app.models.currency import Currency, ExchangeRate
from app.utils.cache import redis_cache
```

**Global Variables:**
```python
logger = logger = logging.getLogger(__name__)
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
@redis_cache(prefix='currency', ttl=3600)
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

##### Module: error_handling_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/error_handling_service.py`

**Imports:**
```python
from __future__ import annotations
import traceback
from typing import Any, Dict, Optional, Type, cast
from app.core.exceptions import AppException, BusinessLogicException, DatabaseException, ErrorCode, ErrorResponse, ValidationException
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.error_handling_service")
```

**Classes:**
```python
class ErrorHandlingService(object):
    """Service for centralized error handling.

This service provides standardized error handling across the application, with consistent error responses and logging."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the error handling service."""
```
```python
    def create_business_logic_error(self, message, details) -> BusinessLogicException:
        """Create a business logic error exception.

Args: message: Error message details: Additional error details

Returns: BusinessLogicException: Business logic error exception"""
```
```python
    def create_database_error(self, message, original_error, details) -> DatabaseException:
        """Create a database error exception.

Args: message: Error message original_error: Original exception details: Additional error details

Returns: DatabaseException: Database error exception"""
```
```python
    def create_validation_error(self, field, message, error_type) -> ValidationException:
        """Create a validation error exception.

Args: field: Field with the error message: Error message error_type: Type of error

Returns: ValidationException: Validation error exception"""
```
```python
    def handle_exception(self, exception, request_id) -> ErrorResponse:
        """Handle an exception and return a standardized error response.

Args: exception: The exception to handle request_id: Request ID for logging and tracking

Returns: ErrorResponse: Standardized error response"""
```
```python
    async def initialize(self) -> None:
        """Initialize service resources."""
```
```python
    async def shutdown(self) -> None:
        """Release service resources."""
```

##### Module: interfaces
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/interfaces.py`

**Imports:**
```python
from __future__ import annotations
import abc
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Protocol, Type, TypeVar, Union
```

**Global Variables:**
```python
T = T = TypeVar('T')  # Entity type
ID = ID = TypeVar('ID')  # ID type
C = C = TypeVar('C')  # Create schema type
U = U = TypeVar('U')  # Update schema type
R = R = TypeVar('R')  # Response schema type
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

##### Module: logging_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/logging_service.py`

**Imports:**
```python
from __future__ import annotations
import json
import logging
import sys
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional, TypeVar, cast
import structlog
from pythonjsonlogger import jsonlogger
from structlog.stdlib import BoundLogger
from structlog.types import EventDict, Processor, WrappedLogger
from app.core.config import Environment, LogLevel, settings
from app.services.interfaces import ServiceInterface
```

**Global Variables:**
```python
F = F = TypeVar("F", bound=Callable[..., Any])
T = T = TypeVar("T")
```

**Classes:**
```python
class LoggingService(object):
    """Service for centralized logging functionality.

This service provides standardized logging across the application, with support for structured logging, correlation IDs, and context tracking."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the logging service."""
```
```python
    def add_context_processor(self, logger, method_name, event_dict) -> EventDict:
        """Add context data to log events.

Args: logger: Logger instance method_name: Method name being called event_dict: Event dictionary to modify

Returns: EventDict: Modified event dictionary"""
```
```python
    def clear_context(self) -> None:
        """Clear context data for the current thread."""
```
```python
    def configure_logging(self) -> None:
        """Configure logging with appropriate handlers and formatters."""
```
```python
    def configure_std_logging(self) -> None:
        """Configure standard library logging.

Sets up log handlers based on environment and configuration settings."""
```
```python
    def configure_structlog(self) -> None:
        """Configure structlog with processors and renderers.

Sets up structlog to work alongside standard library logging, with consistent formatting and context handling."""
```
```python
    def get_logger(self, name) -> BoundLogger:
        """Get a structlog logger instance.

Args: name: Logger name (typically __name__)

Returns: BoundLogger: Structured logger instance"""
```
```python
    async def initialize(self) -> None:
        """Initialize service resources."""
```
```python
    def log_execution_time(self, logger, level) -> Callable[([F], F)]:
        """Decorator to log function execution time.

Args: logger: Logger to use level: Log level to use

Returns: Callable: Decorated function"""
```
```python
    async def log_execution_time_async(self, logger, level) -> Callable[([F], F)]:
        """Decorator to log async function execution time.

Args: logger: Logger to use level: Log level to use

Returns: Callable: Decorated async function"""
```
```python
@contextmanager
    def request_context(self, request_id, user_id) -> Generator[(str, None, None)]:
        """Context manager for tracking request context in logs.

Args: request_id: Request ID (generated if not provided) user_id: User ID (optional)

Yields: str: Request ID"""
```
```python
    def set_context(self, request_id, user_id, **kwargs) -> None:
        """Set context data for the current thread.

Args: request_id: Request ID for correlation user_id: User ID for tracking **kwargs: Additional context data"""
```
```python
    async def shutdown(self) -> None:
        """Release service resources."""
```

##### Module: media_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/media_service.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, AsyncGenerator, BinaryIO, Dict, List, Literal, Optional, Protocol, Set, Tuple, TypedDict, Union
import aiofiles
import aioboto3
from fastapi import HTTPException, UploadFile, status
from pydantic import BaseModel, Field, ValidationError
from app.core.config import Environment, settings
from app.models.media import MediaType, MediaVisibility
import structlog
```

**Global Variables:**
```python
logger = logger = structlog.get_logger(__name__)
media_service = media_service = MediaService()
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

```python
@dataclass
class MediaService(object):
    """Improved media service with better error handling and async support."""
```
*Methods:*
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
    async def upload_file(self, file, media_type, product_id, filename, visibility, generate_thumbnail) -> Tuple[(str, Dict[(str, Any)], Optional[str])]:
        """Upload a file to storage with improved error handling.

Args: file: The uploaded file media_type: Type of media being uploaded product_id: Optional product ID to associate with the file filename: Optional filename override visibility: Visibility level for the file generate_thumbnail: Whether to generate a thumbnail for images

Returns: Tuple[str, Dict[str, Any], Optional[str]]: Tuple of (file URL, metadata, thumbnail URL or None)

Raises: HTTPException: If the file type is invalid or upload fails"""
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

##### Module: metrics_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/metrics_service.py`

**Imports:**
```python
from __future__ import annotations
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, Generator, List, Optional, TypeVar, cast
from prometheus_client import Counter, Gauge, Histogram, Summary
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
```

**Global Variables:**
```python
F = F = TypeVar("F", bound=Callable[..., Any])
logger = logger = get_logger("app.services.metrics_service")
```

**Classes:**
```python
@dataclass
class MetricsConfig(object):
    """Configuration for metrics."""
```

```python
class MetricsService(object):
    """Service for collecting and exporting metrics.

This service provides standardized metrics collection across the application, with support for counters, gauges, histograms, and summaries."""
```
*Methods:*
```python
    def __init__(self, config) -> None:
        """Initialize the metrics service.  Args: config: Metrics configuration"""
```
```python
    def create_counter(self, name, description, labelnames, namespace, subsystem) -> Counter:
        """Create a counter metric.

Args: name: Metric name description: Metric description labelnames: Label names namespace: Metric namespace subsystem: Metric subsystem

Returns: Counter: Created counter"""
```
```python
    def create_gauge(self, name, description, labelnames, namespace, subsystem) -> Gauge:
        """Create a gauge metric.

Args: name: Metric name description: Metric description labelnames: Label names namespace: Metric namespace subsystem: Metric subsystem

Returns: Gauge: Created gauge"""
```
```python
    def create_histogram(self, name, description, labelnames, buckets, namespace, subsystem) -> Histogram:
        """Create a histogram metric.

Args: name: Metric name description: Metric description labelnames: Label names buckets: Histogram buckets namespace: Metric namespace subsystem: Metric subsystem

Returns: Histogram: Created histogram"""
```
```python
    def create_summary(self, name, description, labelnames, namespace, subsystem) -> Summary:
        """Create a summary metric.

Args: name: Metric name description: Metric description labelnames: Label names namespace: Metric namespace subsystem: Metric subsystem

Returns: Summary: Created summary"""
```
```python
    def increment_counter(self, name, amount, labels) -> None:
        """Increment a counter metric.

Args: name: Metric name amount: Amount to increment by labels: Metric labels"""
```
```python
    async def initialize(self) -> None:
        """Initialize service resources."""
```
```python
    def observe_histogram(self, name, value, labels) -> None:
        """Observe a histogram metric value.

Args: name: Metric name value: Observation value labels: Metric labels"""
```
```python
    def observe_summary(self, name, value, labels) -> None:
        """Observe a summary metric value.

Args: name: Metric name value: Observation value labels: Metric labels"""
```
```python
    def set_gauge(self, name, value, labels) -> None:
        """Set a gauge metric value.  Args: name: Metric name value: Gauge value labels: Metric labels"""
```
```python
    async def shutdown(self) -> None:
        """Release service resources."""
```
```python
@contextmanager
    def timer(self, metric_type, name, labels) -> Generator[(None, None, None)]:
        """Context manager for timing operations.

Args: metric_type: Type of metric (histogram or summary) name: Metric name labels: Metric labels

Yields: None"""
```
```python
    def timing_decorator(self, metric_type, name, labels_func) -> Callable[([F], F)]:
        """Decorator for timing function execution.

Args: metric_type: Type of metric (histogram or summary) name: Metric name labels_func: Function to extract labels from function arguments

Returns: Callable: Decorated function"""
```
```python
    async def timing_decorator_async(self, metric_type, name, labels_func) -> Callable[([F], F)]:
        """Decorator for timing async function execution.

Args: metric_type: Type of metric (histogram or summary) name: Metric name labels_func: Function to extract labels from function arguments

Returns: Callable: Decorated async function"""
```

##### Module: pagination
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/pagination.py`

**Imports:**
```python
from __future__ import annotations
import base64
import json
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union, cast
from fastapi import HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import Column, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import ClauseElement
from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.db.base_class import Base
from app.db.utils import count_query, execute_query
from app.schemas.pagination import CursorPaginationParams, OffsetPaginationParams, PaginationResult, SortDirection, SortField
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.pagination")
T = T = TypeVar("T", bound=Base)
R = R = TypeVar("R", bound=BaseModel)
```

**Classes:**
```python
class PaginationService(Generic[(T, R)]):
    """Service for handling pagination.

This service supports both offset-based and cursor-based pagination.

Attributes: db: Database session model: SQLAlchemy model class response_model: Pydantic response model"""
```
*Methods:*
```python
    def __init__(self, db, model, response_model) -> None:
        """Initialize the pagination service.

Args: db: Database session model: SQLAlchemy model class response_model: Pydantic response model"""
```
```python
    async def paginate_with_cursor(self, query, params, transform_func) -> PaginationResult[R]:
        """Paginate query results using cursor-based pagination.

Args: query: SQLAlchemy query params: Pagination parameters transform_func: Function to transform items

Returns: PaginationResult[R]: Paginated results

Raises: ValidationException: If pagination parameters are invalid"""
```
```python
    async def paginate_with_offset(self, query, params, transform_func) -> PaginationResult[R]:
        """Paginate query results using offset-based pagination.

Args: query: SQLAlchemy query params: Pagination parameters transform_func: Function to transform items

Returns: PaginationResult[R]: Paginated results

Raises: ValidationException: If pagination parameters are invalid"""
```

##### Module: search
*Search service.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/search.py`

**Imports:**
```python
from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.config import settings
from app.models.product import Fitment, Product
from app.utils.db import paginate
```

**Functions:**
```python
async def get_search_service(db) -> SearchService:
    """Get search service instance.  Args: db: Database session  Returns: SearchService: Search service"""
```

**Classes:**
```python
class SearchService(object):
    """Service for search functionality.

This service provides methods for searching across different entities in the application, with support for text search, filtering, and pagination."""
```
*Methods:*
```python
    def __init__(self, db):
        """Initialize the search service.  Args: db: Database session"""
```
```python
    async def get_es_client(self) -> Optional[AsyncElasticsearch]:
        """Get Elasticsearch client instance.

Returns: Optional[AsyncElasticsearch]: Elasticsearch client or None if not configured"""
```
```python
    async def global_search(self, search_term, entity_types, page, page_size) -> Dict[(str, Any)]:
        """Search across multiple entity types.

Args: search_term: Text to search for entity_types: List of entity types to search (products, fitments, categories) page: Page number page_size: Items per page

Returns: Dict[str, Any]: Search results grouped by entity type"""
```
```python
    async def search_fitments(self, search_term, year, make, model, engine, transmission, page, page_size) -> Dict[(str, Any)]:
        """Search for fitments with filtering and pagination.

Args: search_term: Text to search for year: Filter by year make: Filter by make model: Filter by model engine: Filter by engine transmission: Filter by transmission page: Page number page_size: Items per page

Returns: Dict[str, Any]: Search results with pagination"""
```
```python
    async def search_products(self, search_term, attributes, is_active, page, page_size, use_elasticsearch) -> Dict[(str, Any)]:
        """Search for products with filtering and pagination.

Args: search_term: Text to search for attributes: Filter by product attributes is_active: Filter by active status page: Page number page_size: Items per page use_elasticsearch: Whether to use Elasticsearch (if available)

Returns: Dict[str, Any]: Search results with pagination"""
```

##### Module: test_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/test_service.py`

**Imports:**
```python
from __future__ import annotations
import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, cast
from app.core.logging import get_logger
from app.services.base import BaseService
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.test_service")
T = T = TypeVar('T')
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

##### Module: validation_service
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/validation_service.py`

**Imports:**
```python
from __future__ import annotations
import re
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Type, Union, cast
from pydantic import BaseModel, Field, ValidationError, root_validator, validator
from app.core.exceptions import ValidationException
from app.core.logging import get_logger
from app.services.interfaces import ServiceInterface
```

**Global Variables:**
```python
logger = logger = get_logger("app.services.validation_service")
```

**Classes:**
```python
class ValidationService(object):
    """Service for validating data.

This service provides standardized validation across the application, with support for common validation patterns."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize the validation service."""
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
    def validate_data(self, data, schema_class) -> BaseModel:
        """Validate data against a Pydantic schema.

Args: data: Data to validate schema_class: Pydantic schema class

Returns: BaseModel: Validated schema

Raises: ValidationException: If validation fails"""
```
```python
    def validate_date(self, value, min_date, max_date, format_str) -> bool:
        """Validate a date.

Args: value: Date to validate min_date: Minimum allowed date max_date: Maximum allowed date format_str: Date format string for string dates

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_email(self, email) -> bool:
        """Validate an email address.

Args: email: Email address to validate

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_length(self, value, min_length, max_length) -> bool:
        """Validate string length.

Args: value: String to validate min_length: Minimum allowed length max_length: Maximum allowed length

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_phone(self, phone) -> bool:
        """Validate a phone number.

Args: phone: Phone number to validate

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_range(self, value, min_value, max_value) -> bool:
        """Validate a numeric value within a range.

Args: value: Numeric value to validate min_value: Minimum allowed value max_value: Maximum allowed value

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_regex(self, value, pattern) -> bool:
        """Validate a string against a regex pattern.

Args: value: String to validate pattern: Regex pattern

Returns: bool: True if valid, False otherwise"""
```
```python
    def validate_required(self, value) -> bool:
        """Validate that a value is not None or empty.

Args: value: Value to validate

Returns: bool: True if valid, False otherwise"""
```
```python
    async def validate_unique(self, field, value, model, db, exclude_id) -> bool:
        """Validate that a field value is unique.

Args: field: Field name value: Field value model: SQLAlchemy model db: Database session exclude_id: ID to exclude from the check

Returns: bool: True if valid, False otherwise"""
```

##### Module: vehicle
*Vehicle data lookup service.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/vehicle.py`

**Imports:**
```python
from __future__ import annotations
import re
from typing import Dict, List, Optional, Set, Tuple
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.models.product import Fitment
from app.utils.cache import memory_cache, redis_cache
```

**Functions:**
```python
async def get_vehicle_service(db) -> VehicleDataService:
    """Get vehicle data service instance.

Args: db: Database session

Returns: VehicleDataService: Vehicle data service"""
```

**Classes:**
```python
class VehicleDataService(object):
    """Service for vehicle data lookups and validation.

This service provides methods for working with vehicle data, including lookups, validation, and standardization."""
```
*Methods:*
```python
    def __init__(self, db):
        """Initialize the vehicle data service.  Args: db: Database session"""
```
```python
@memory_cache(maxsize=1000, ttl=86400)
    async def decode_vin(self, vin) -> Optional[Dict[(str, Any)]]:
        """Decode a Vehicle Identification Number (VIN).

This method could integrate with an external VIN decoding service or use internal logic to parse VIN information.

Args: vin: Vehicle Identification Number

Returns: Optional[Dict[str, Any]]: Decoded vehicle data or None if invalid"""
```
```python
@redis_cache(prefix='vehicle:engines', ttl=3600)
    async def get_engines(self, make, model, year) -> List[str]:
        """Get all available engines, optionally filtered by make, model, and year.

Args: make: Filter by make model: Filter by model year: Filter by year

Returns: List[str]: Sorted list of engines"""
```
```python
@redis_cache(prefix='vehicle:makes', ttl=3600)
    async def get_makes(self, year) -> List[str]:
        """Get all available makes, optionally filtered by year.

Args: year: Filter by year

Returns: List[str]: Sorted list of makes"""
```
```python
@redis_cache(prefix='vehicle:models', ttl=3600)
    async def get_models(self, make, year) -> List[str]:
        """Get all available models, optionally filtered by make and year.

Args: make: Filter by make year: Filter by year

Returns: List[str]: Sorted list of models"""
```
```python
@redis_cache(prefix='vehicle:transmissions', ttl=3600)
    async def get_transmissions(self, make, model, year, engine) -> List[str]:
        """Get all available transmissions, optionally filtered.

Args: make: Filter by make model: Filter by model year: Filter by year engine: Filter by engine

Returns: List[str]: Sorted list of transmissions"""
```
```python
@redis_cache(prefix='vehicle:years', ttl=3600)
    async def get_years(self) -> List[int]:
        """Get all available years from fitment data.  Returns: List[int]: Sorted list of years"""
```
```python
@memory_cache(maxsize=100, ttl=3600)
    async def standardize_make(self, make) -> str:
        """Standardize vehicle make to ensure consistent naming.

Args: make: Vehicle make

Returns: str: Standardized make name"""
```
```python
@memory_cache(maxsize=100, ttl=3600)
    async def validate_fitment(self, year, make, model, engine, transmission) -> bool:
        """Validate if a fitment combination exists.

Args: year: Vehicle year make: Vehicle make model: Vehicle model engine: Vehicle engine transmission: Vehicle transmission

Returns: bool: True if fitment exists"""
```

#### Package: tasks
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/tasks`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/tasks/__init__.py`

##### Module: chat_tasks
*Celery worker for background tasks.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/tasks/chat_tasks.py`

**Imports:**
```python
from __future__ import annotations
import logging
import os
from typing import Any, Dict, List, Optional
from celery import Celery
from app.core.config import settings
```

**Global Variables:**
```python
logger = logger = logging.getLogger(__name__)
celery_app = celery_app = Celery(
    "worker",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/2"
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

##### Module: currency_tasks
*Celery tasks for currency operations.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/tasks/currency_tasks.py`

**Imports:**
```python
from __future__ import annotations
import logging
from typing import Dict, Optional, List
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db_context
from app.services.currency_service import ExchangeRateService
```

**Global Variables:**
```python
logger = logger = logging.getLogger(__name__)
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

#### Package: utils
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/__init__.py`

##### Module: cache
*Caching utility functions.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/cache.py`

**Imports:**
```python
from __future__ import annotations
import functools
import hashlib
import inspect
import json
import pickle
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, cast
import redis.asyncio as redis
from fastapi import Depends, Request
from app.core.config import settings
```

**Global Variables:**
```python
F = F = TypeVar('F', bound=Callable[..., Any])
RT = RT = TypeVar('RT')  # Return type
```

**Functions:**
```python
def generate_cache_key(prefix, func, args, kwargs) -> str:
    """Generate a cache key for a function call.

Args: prefix: Key prefix func: Function args: Function arguments kwargs: Function keyword arguments

Returns: str: Cache key"""
```

```python
async def get_redis() -> redis.Redis:
    """Get Redis client instance.

Creates a new connection if one doesn't exist.

Returns: redis.Redis: Redis client"""
```

```python
def get_request_cache(request) -> RequestCache:
    """Get or create a RequestCache instance for the current request.

Args: request: FastAPI request

Returns: RequestCache: Request cache"""
```

```python
async def invalidate_cache(prefix, pattern, redis_conn) -> int:
    """Invalidate cache keys matching a pattern.

Args: prefix: Cache key prefix pattern: Key pattern redis_conn: Redis client

Returns: int: Number of keys deleted"""
```

```python
def memory_cache(maxsize, ttl) -> Callable[([F], F)]:
    """Decorator for in-memory caching with TTL.

Args: maxsize: Maximum cache size ttl: Time-to-live in seconds

Returns: Callable: Decorator function"""
```

```python
def redis_cache(prefix, ttl, skip_args) -> Callable[([F], F)]:
    """Decorator for Redis caching.

Args: prefix: Cache key prefix ttl: Time-to-live in seconds skip_args: List of argument names to skip when generating cache key

Returns: Callable: Decorator function"""
```

**Classes:**
```python
class RequestCache(object):
    """Cache for the current request lifecycle.

This class provides a way to cache data during a single request, which can be useful for repeated database queries or expensive computations within the same request."""
```
*Methods:*
```python
    def __init__(self) -> None:
        """Initialize an empty cache."""
```
```python
    def clear(self) -> None:
        """Clear all cached values."""
```
```python
    def delete(self, key) -> None:
        """Delete value from cache.  Args: key: Cache key"""
```
```python
    def get(self, key) -> Optional[Any]:
        """Get value from cache.  Args: key: Cache key  Returns: Optional[Any]: Cached value or None"""
```
```python
    def set(self, key, value) -> None:
        """Set value in cache.  Args: key: Cache key value: Value to cache"""
```

##### Module: circuit_breaker
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/circuit_breaker.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import enum
import functools
import logging
import time
from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast
from app.core.exceptions import ServiceUnavailableException
from app.core.logging import get_logger
```

**Global Variables:**
```python
F = F = TypeVar('F', bound=Callable[..., Any])
logger = logger = get_logger("app.utils.circuit_breaker")
```

**Functions:**
```python
def circuit_breaker(name, failure_threshold, success_threshold, timeout, exception_types, fallback) -> Callable[([F], F)]:
    """Circuit breaker decorator.

This decorator applies the circuit breaker pattern to a function.

Args: name: Circuit breaker name failure_threshold: Number of failures before opening the circuit success_threshold: Number of successes before closing the circuit timeout: Time in seconds to wait before transitioning from OPEN to HALF_OPEN exception_types: Types of exceptions that increment the failure counter fallback: Optional fallback function to call when the circuit is open

Returns: Callable: Function decorator"""
```

**Classes:**
```python
class CircuitBreaker(object):
    """Circuit breaker implementation.

This class implements the circuit breaker pattern, which prevents an application from repeatedly trying to execute an operation that's likely to fail, allowing it to continue without waiting for the fault to be fixed or wasting resources while the fault is being fixed.

Attributes: name: Unique name for this circuit breaker config: Circuit breaker configuration state: Current circuit state failure_count: Count of consecutive failures success_count: Count of consecutive successes last_failure_time: Time of last failure last_state_change_time: Time of last state change"""
```
*Methods:*
```python
    def __call__(self, func) -> F:
        """Decorate a function with circuit breaker.

Args: func: Function to decorate

Returns: F: Decorated function"""
```
```python
    def __init__(self, name, config) -> None:
        """Initialize the circuit breaker.

Args: name: Unique name for this circuit breaker config: Circuit breaker configuration"""
```
```python
    def async_call(self, func) -> F:
        """Decorate an async function with circuit breaker.

Args: func: Async function to decorate

Returns: F: Decorated async function"""
```
```python
    def check_state(self) -> None:
        """Check and update the circuit breaker state.

This method checks if the circuit breaker should transition to a new state based on its current state and the elapsed time since the last state change."""
```
```python
@classmethod
    def get(cls, name) -> CircuitBreaker:
        """Get a circuit breaker by name.

Args: name: Circuit breaker name

Returns: CircuitBreaker: Circuit breaker instance

Raises: ValueError: If circuit breaker not found"""
```
```python
@classmethod
    def get_all_states(cls) -> Dict[(str, CircuitState)]:
        """Get the states of all circuit breakers.

Returns: Dict[str, CircuitState]: Dictionary of circuit breaker names and states"""
```
```python
@classmethod
    def get_or_create(cls, name, config) -> CircuitBreaker:
        """Get a circuit breaker by name or create it if it doesn't exist.

Args: name: Circuit breaker name config: Circuit breaker configuration

Returns: CircuitBreaker: Circuit breaker instance"""
```
```python
    def reset(self) -> None:
        """Reset the circuit breaker to its initial state."""
```
```python
@classmethod
    def reset_all(cls) -> None:
        """Reset all circuit breakers."""
```

```python
@dataclass
class CircuitBreakerConfig(object):
    """Circuit breaker configuration.

This class holds the configuration for a circuit breaker.

Attributes: failure_threshold: Number of failures before opening the circuit success_threshold: Number of successes before closing the circuit timeout: Time in seconds to wait before transitioning from OPEN to HALF_OPEN exception_types: Types of exceptions that increment the failure counter fallback: Optional fallback function to call when the circuit is open"""
```

```python
class CircuitState(enum.Enum):
    """Circuit breaker states.

The circuit breaker can be in one of three states: - CLOSED: Normal operation, requests are allowed - OPEN: Circuit is broken, all requests fail immediately - HALF_OPEN: Allowing a limited number of test requests to check if the service is back"""
```
*Class attributes:*
```python
CLOSED = 'closed'
OPEN = 'open'
HALF_OPEN = 'half_open'
```

##### Module: crypto
*Cryptography utilities.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/crypto.py`

**Imports:**
```python
from __future__ import annotations
import base64
import os
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from app.core.config import settings
```

**Functions:**
```python
def decrypt_message(encrypted_message) -> str:
    """Decrypt a Fernet-encrypted message.

Args: encrypted_message: The encrypted message as a base64-encoded string

Returns: str: The decrypted plaintext message

Raises: cryptography.fernet.InvalidToken: If the message is invalid or corrupted"""
```

```python
def encrypt_message(message) -> str:
    """Encrypt a message using Fernet symmetric encryption.

Args: message: The plaintext message to encrypt

Returns: str: The encrypted message as a base64-encoded string"""
```

```python
def generate_secure_token(length) -> str:
    """Generate a cryptographically secure random token.

Args: length: The desired length of the token in bytes

Returns: str: A secure random token as a hex string"""
```

##### Module: db
*Database utility functions.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/db.py`

**Imports:**
```python
from __future__ import annotations
import contextlib
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Sequence, Type, TypeVar
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Delete, Insert, Select, Update
from app.db.base_class import Base
```

**Global Variables:**
```python
T = T = TypeVar('T', bound=Base)
```

**Functions:**
```python
async def bulk_create(db, model, objects) -> List[T]:
    """Create multiple model instances in a single transaction.

This is more efficient than creating objects one at a time.

Args: db: Database session model: Model class objects: List of object data

Returns: List[T]: List of created model instances"""
```

```python
async def create_object(db, model, obj_in) -> T:
    """Create a model instance.

Args: db: Database session model: Model class obj_in: Object data

Returns: T: Created model instance"""
```

```python
async def delete_object(db, model, id) -> bool:
    """Delete a model instance by ID.

Args: db: Database session model: Model class id: Instance ID

Returns: bool: True if deleted, False if not found"""
```

```python
async def execute_query(db, query) -> Any:
    """Execute a SQLAlchemy query.

Args: db: Database session query: SQLAlchemy query

Returns: Any: Query result"""
```

```python
async def get_by_id(db, model, id) -> Optional[T]:
    """Get a model instance by ID.

Args: db: Database session model: Model class id: Instance ID

Returns: Optional[T]: Model instance or None if not found"""
```

```python
async def paginate(db, query, page, page_size) -> Dict[(str, Any)]:
    """Paginate a query.

Args: db: Database session query: Base query page: Page number (starting from 1) page_size: Number of items per page

Returns: Dict[str, Any]: Pagination result with items, total, page, page_size, and pages"""
```

```python
@contextlib.asynccontextmanager
async def transaction(db) -> AsyncGenerator[(AsyncSession, None)]:
    """Context manager for database transactions.

This ensures that all operations within the context are committed together or rolled back on error.

Args: db: Database session

Yields: AsyncSession: Database session"""
```

```python
async def update_object(db, model, id, obj_in) -> Optional[T]:
    """Update a model instance by ID.

Args: db: Database session model: Model class id: Instance ID obj_in: Object data

Returns: Optional[T]: Updated model instance or None if not found"""
```

##### Module: errors
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/errors.py`

**Imports:**
```python
from __future__ import annotations
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from app.core.exceptions import AppException, BadRequestException, BusinessLogicException, DatabaseException, ErrorCode, ErrorDetail, PermissionDeniedException, ResourceAlreadyExistsException, ResourceNotFoundException, ValidationException
```

**Global Variables:**
```python
T = T = TypeVar("T")
```

**Functions:**
```python
def bad_request(message) -> BadRequestException:
    """Create a BadRequestException with the provided message.

Args: message: Error message

Returns: BadRequestException with the provided message"""
```

```python
def business_logic_error(message) -> BusinessLogicException:
    """Create a BusinessLogicException with the provided message.

Args: message: Error message

Returns: BusinessLogicException with the provided message"""
```

```python
def create_error_details(loc, msg, type_str) -> ErrorDetail:
    """Create an error detail object.

Args: loc: Location of the error (e.g., ["body", "username"]) msg: Error message type_str: Error type string

Returns: ErrorDetail object"""
```

```python
def database_error(message, original_error) -> DatabaseException:
    """Create a DatabaseException with the provided message.

Args: message: Error message original_error: Original exception that was caught

Returns: DatabaseException with the provided message"""
```

```python
def ensure_not_none(value, resource_type, resource_id) -> T:
    """Ensure a value is not None, raising ResourceNotFoundException if it is.

Args: value: Value to check resource_type: Type of resource for error message resource_id: ID of the resource for error message

Returns: The value if it's not None

Raises: ResourceNotFoundException: If the value is None"""
```

```python
def permission_denied(action, resource_type) -> PermissionDeniedException:
    """Create a PermissionDeniedException with standard formatting.

Args: action: Action attempted (e.g., "create", "update") resource_type: Type of resource (e.g., "User", "Product")

Returns: PermissionDeniedException with a standardized message"""
```

```python
def resource_already_exists(resource_type, identifier) -> ResourceAlreadyExistsException:
    """Create a ResourceAlreadyExistsException with standard formatting.

Args: resource_type: Type of resource (e.g., "User", "Product") identifier: Identifier(s) that caused the conflict

Returns: ResourceAlreadyExistsException with a standardized message"""
```

```python
def resource_not_found(resource_type, resource_id) -> ResourceNotFoundException:
    """Create a ResourceNotFoundException with standard formatting.

Args: resource_type: Type of resource (e.g., "User", "Product") resource_id: ID of the resource that wasn't found

Returns: ResourceNotFoundException with a standardized message"""
```

```python
def validation_error(field, message) -> ValidationException:
    """Create a ValidationException for a specific field.

Args: field: Field name or path message: Error message

Returns: ValidationException with details for the specified field"""
```

##### Module: file
*File handling utilities.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/file.py`

**Imports:**
```python
from __future__ import annotations
import os
import secrets
import uuid
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Dict, List, Optional, Set, Tuple, Union
from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from app.core.config import Environment, settings
from app.models.media import MediaType
```

**Functions:**
```python
def get_file_extension(filename) -> str:
    """Get the file extension from a filename.

Args: filename: Filename to extract extension from

Returns: str: File extension (lowercase, without leading period)"""
```

```python
def get_file_path(file_path) -> Path:
    """Get the absolute path of a file.

Args: file_path: Relative path from media root or full URL

Returns: Path: Absolute path to the file"""
```

```python
def get_file_url(file_path) -> str:
    """Get the URL for a file path, taking environment into account.

Args: file_path: Relative path from media root

Returns: str: Full URL to access the file"""
```

```python
def get_media_type_from_mime(mime_type) -> MediaType:
    """Determine the media type from MIME type.

Args: mime_type: MIME type of the file

Returns: MediaType: Determined media type"""
```

```python
def get_thumbnail_path(file_path) -> Optional[Path]:
    """Get the thumbnail path for an image.

Args: file_path: Relative path from media root or full URL

Returns: Optional[Path]: Absolute path to the thumbnail, or None if not found"""
```

```python
def is_safe_filename(filename) -> bool:
    """Check if a filename is safe to use.

Validates that the filename doesn't contain any potentially dangerous characters or path traversal attempts.

Args: filename: Filename to check

Returns: bool: True if filename is safe, False otherwise"""
```

```python
def sanitize_filename(filename) -> str:
    """Sanitize a filename to be safe for storage.

Args: filename: Original filename

Returns: str: Sanitized filename"""
```

```python
def save_upload_file(file, media_id, media_type, is_image) -> Tuple[(str, int, str)]:
    """Save an uploaded file to disk.

Handles saving the file to the appropriate directory and creating thumbnails for images.

Args: file: Uploaded file media_id: ID of the media record media_type: Type of media is_image: Whether the file is an image

Returns: Tuple[str, int, str]: File path, file size, and media hash

Raises: IOError: If file saving fails"""
```

```python
def validate_file(file, allowed_types) -> Tuple[(MediaType, bool)]:
    """Validate a file for upload.

Performs various validations on the uploaded file: - Filename presence - File size within limits - MIME type allowed for the media type - Image validity for image files

Args: file: Uploaded file allowed_types: Set of allowed media types (if None, all types are allowed)

Returns: Tuple[MediaType, bool]: Media type and whether the file is an image

Raises: HTTPException: If file is invalid"""
```

##### Module: redis_manager
*Redis connection manager.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/redis_manager.py`

**Imports:**
```python
from __future__ import annotations
import json
import logging
from typing import Any, Dict, List, Optional, TypeVar, cast
import redis.asyncio as redis
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from app.core.config import settings
```

**Global Variables:**
```python
logger = logger = logging.getLogger(__name__)
T = T = TypeVar('T')
```

**Functions:**
```python
async def cache_get_or_set(key, callback, ttl, force_refresh) -> Any:
    """Get a value from cache or compute and store it.

Args: key: Cache key callback: Function to compute the value if not cached ttl: Time-to-live in seconds force_refresh: Force cache refresh

Returns: Any: Cached or computed value"""
```

```python
async def delete_key(key) -> bool:
    """Delete a key from Redis.  Args: key: Redis key  Returns: bool: Success status"""
```

```python
async def get_key(key, default) -> Optional[T]:
    """Get a value from Redis.

Args: key: Redis key default: Default value if key doesn't exist

Returns: Any: Deserialized value or default"""
```

```python
async def get_redis_client() -> Redis:
    """Get a Redis client using the connection pool.  Returns: Redis: Redis client"""
```

```python
async def get_redis_pool() -> ConnectionPool:
    """Get or create the Redis connection pool.  Returns: ConnectionPool: Redis connection pool"""
```

```python
async def increment_counter(key, amount, ttl) -> Optional[int]:
    """Increment a counter in Redis.

Args: key: Redis key amount: Amount to increment by ttl: Time-to-live in seconds (optional)

Returns: Optional[int]: New counter value or None on error"""
```

```python
async def publish_message(channel, message) -> bool:
    """Publish a message to a Redis channel.

Args: channel: Redis channel name message: Message data to publish

Returns: bool: Success status"""
```

```python
async def rate_limit_check(key, limit, window) -> tuple[(bool, int)]:
    """Check if a rate limit has been exceeded.

Args: key: Redis key for the rate limit limit: Maximum number of operations window: Time window in seconds

Returns: tuple[bool, int]: (is_limited, current_count)"""
```

```python
async def set_key(key, value, ttl) -> bool:
    """Set a value in Redis.

Args: key: Redis key value: Value to store (will be JSON serialized) ttl: Time-to-live in seconds (optional)

Returns: bool: Success status"""
```

##### Module: retry
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/utils/retry.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
import functools
import logging
import random
import time
from typing import Any, Callable, List, Optional, Type, TypeVar, Union, cast
from app.core.exceptions import NetworkException, RateLimitException, ServiceUnavailableException, TimeoutException
from app.core.logging import get_logger
```

**Global Variables:**
```python
F = F = TypeVar('F', bound=Callable[..., Any])
T = T = TypeVar('T')
logger = logger = get_logger("app.utils.retry")
```

**Functions:**
```python
async def async_retry(retries, delay, backoff_factor, jitter, exceptions) -> Callable[([F], F)]:
    """Retry decorator for asynchronous functions.

This decorator retries an async function when it raises specified exceptions, with exponential backoff and optional jitter.

Args: retries: Maximum number of retries delay: Initial delay between retries in seconds backoff_factor: Backoff multiplier (how much to increase delay each retry) jitter: Whether to add random jitter to delay exceptions: Exception types to catch and retry

Returns: Callable: Decorated async function"""
```

```python
async def async_retry_on_network_errors(retries, delay, backoff_factor, jitter) -> Callable[([F], F)]:
    """Async retry decorator for functions that may encounter network errors.

This decorator is specialized for network-related errors in async functions and uses appropriate exception types.

Args: retries: Maximum number of retries delay: Initial delay between retries in seconds backoff_factor: Backoff multiplier (how much to increase delay each retry) jitter: Whether to add random jitter to delay

Returns: Callable: Decorated async function"""
```

```python
async def async_retry_with_timeout(retries, delay, timeout, backoff_factor, jitter, exceptions) -> Callable[([F], F)]:
    """Retry decorator with timeout for asynchronous functions.

This decorator combines retry logic with a timeout for each attempt.

Args: retries: Maximum number of retries delay: Initial delay between retries in seconds timeout: Timeout for each attempt in seconds backoff_factor: Backoff multiplier (how much to increase delay each retry) jitter: Whether to add random jitter to delay exceptions: Exception types to catch and retry

Returns: Callable: Decorated async function"""
```

```python
def retry(retries, delay, backoff_factor, jitter, exceptions) -> Callable[([F], F)]:
    """Retry decorator for synchronous functions.

This decorator retries a function when it raises specified exceptions, with exponential backoff and optional jitter.

Args: retries: Maximum number of retries delay: Initial delay between retries in seconds backoff_factor: Backoff multiplier (how much to increase delay each retry) jitter: Whether to add random jitter to delay exceptions: Exception types to catch and retry

Returns: Callable: Decorated function"""
```

```python
def retry_on_network_errors(retries, delay, backoff_factor, jitter) -> Callable[([F], F)]:
    """Retry decorator for functions that may encounter network errors.

This decorator is specialized for network-related errors and uses appropriate exception types.

Args: retries: Maximum number of retries delay: Initial delay between retries in seconds backoff_factor: Backoff multiplier (how much to increase delay each retry) jitter: Whether to add random jitter to delay

Returns: Callable: Decorated function"""
```

```python
def retry_with_timeout(retries, delay, timeout, backoff_factor, jitter, exceptions) -> Callable[([F], F)]:
    """Retry decorator with timeout for synchronous functions.

This decorator combines retry logic with a timeout for each attempt.

Args: retries: Maximum number of retries delay: Initial delay between retries in seconds timeout: Timeout for each attempt in seconds backoff_factor: Backoff multiplier (how much to increase delay each retry) jitter: Whether to add random jitter to delay exceptions: Exception types to catch and retry

Returns: Callable: Decorated function"""
```

### Package: examples
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/examples`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/examples/__init__.py`

#### Module: process_fitment
*Example script for processing fitment data.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/examples/process_fitment.py`

**Imports:**
```python
import asyncio
import json
import os
import sys
from typing import Dict, List
from app.fitment.config import FitmentSettings, configure_logging
from app.fitment.db import FitmentDBService
from app.fitment.mapper import FitmentMappingEngine
from app.fitment.models import ValidationStatus
```

**Functions:**
```python
async def main():
    """Run the example script."""
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
import os
import uuid
from datetime import datetime
from typing import Any, AsyncGenerator, Callable, Dict, Generator, List, Optional, Type, TypeVar
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import Environment, settings
from app.core.security import create_access_token
from app.db.base import Base
from app.main import app
from app.models.user import Company, User, UserRole, get_password_hash
from app.models.product import Brand, Fitment, Product
from app.api.deps import get_db
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
import json
import random
import string
import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar, cast
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from pydantic import BaseModel
```

**Global Variables:**
```python
M = M = TypeVar('M', bound=BaseModel)
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
import pytest
from httpx import AsyncClient
from app.models.user import User
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
from typing import Dict, Any
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.models.user import User
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
import pytest
from httpx import AsyncClient
from app.models.user import User, UserRole
from tests.utils import create_random_email, create_random_string, make_authenticated_request
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

# frontend Frontend Structure
Generated on 2025-03-17 01:36:48

## Project Overview
- Project Name: frontend
- Project Type: Vue 3
- Root Path: /home/runner/work/Crown-Nexus/Crown-Nexus/frontend

### Dependencies
**Production Dependencies:**
- @mdi/font: ^7.4.47
- axios: ^1.8.1
- date-fns: ^4.1.0
- package.json: ^2.0.1
- pinia: ^2.3.1
- vue: ^3.5.13
- vue-i18n: ^10.0.6
- vue-router: ^4.5.0
- vuetify: ^3.7.15

**Development Dependencies:**
- @types/node: ^22.13.9
- @vitejs/plugin-vue: ^5.2.1
- @vitejs/plugin-vue-jsx: ^4.1.1
- @vue/test-utils: ^2.4.6
- @vue/tsconfig: ^0.7.0
- jsdom: ^26.0.0
- typescript: ~5.7.2
- vite: ^6.2.0
- vitest: ^3.0.7
- vue-tsc: ^2.2.4

## Directory Structure
```
frontend/
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   │   ├── brand_identity/
│   │   │   ├── brand_pattern_background.png
│   │   │   ├── brand_pattern_background2.png
│   │   │   ├── icon.png
│   │   │   ├── icon2.png
│   │   │   ├── logo.png
│   │   │   └── logo2.png
│   │   ├── dashboard_ui/
│   │   │   ├── dashboard_welcome_banner.png
│   │   │   ├── dashboard_welcome_banner2.png
│   │   │   ├── empty_state_charts.png
│   │   │   ├── empty_state_charts2.png
│   │   │   ├── widget_card_header_fitments.png
│   │   │   ├── widget_card_header_fitments2.png
│   │   │   ├── widget_card_header_order_sales.png
│   │   │   ├── widget_card_header_order_sales2.png
│   │   │   ├── widget_card_header_products.png
│   │   │   ├── widget_card_header_products2.png
│   │   │   └── widget_card_header_user_account.png
│   │   ├── documentation_help/
│   │   │   ├── database_relationship_diagram.png
│   │   │   ├── database_relationship_diagram2.png
│   │   │   ├── fitment_association_workflow.png
│   │   │   ├── import_export_workflow.png
│   │   │   ├── import_export_workflow2.png
│   │   │   ├── order_processing_workflow.png
│   │   │   ├── order_processing_workflow2.png
│   │   │   ├── product_creation_workflow.png
│   │   │   ├── product_creation_workflow2.png
│   │   │   ├── tutorial_screenshots.png
│   │   │   ├── tutorial_screenshots2.png
│   │   │   ├── user_permission_management.png
│   │   │   └── user_permission_management2.png
│   │   ├── email_notification/
│   │   │   ├── account_alerts.png
│   │   │   ├── account_alerts2.png
│   │   │   ├── email_header.png
│   │   │   ├── email_header2.png
│   │   │   ├── newsletter_updates.png
│   │   │   ├── newsletter_updates2.png
│   │   │   ├── order_confirmation.png
│   │   │   ├── order_confirmation2.png
│   │   │   ├── password_reset_security.png
│   │   │   ├── password_reset_security2.png
│   │   │   └── welcome_onboarding.png
│   │   ├── fitment_related/
│   │   │   ├── fitment_compatibility.png
│   │   │   ├── fitment_compatibility2.png
│   │   │   ├── vehicle_make_icons.png
│   │   │   ├── vehicle_make_icons2.png
│   │   │   ├── vehicle_position_diagrams.png
│   │   │   └── vehicle_position_diagrams2.png
│   │   ├── marketing_landing/
│   │   │   ├── analytics_reporting.png
│   │   │   ├── catalog_management.png
│   │   │   ├── catalog_management2.png
│   │   │   ├── fitment_compatibility.png
│   │   │   ├── fitment_compatibility2.png
│   │   │   ├── home_page_hero_banner.png
│   │   │   ├── home_page_hero_banner2.png
│   │   │   ├── order_processing.png
│   │   │   ├── order_processing2.png
│   │   │   ├── testimonial_background.png
│   │   │   └── testimonial_background2.png
│   │   ├── mobile_responsive/
│   │   │   ├── header_collapsed.png
│   │   │   ├── header_collapsed2.png
│   │   │   ├── menu_button_states.png
│   │   │   ├── menu_button_states2.png
│   │   │   └── simplified_illustration.png
│   │   ├── navigation_ui/
│   │   │   ├── action_button_icons.png
│   │   │   ├── action_button_icons2.png
│   │   │   ├── main_navigation_icons.png
│   │   │   └── main_navigation_icons2.png
│   │   ├── product_catalog/
│   │   │   ├── brake_systems.png
│   │   │   ├── brake_systems2.png
│   │   │   ├── detail_gallery.png
│   │   │   ├── detail_gallery2.png
│   │   │   ├── electrical_systems.png
│   │   │   ├── electrical_systems2.png
│   │   │   ├── engine_components.png
│   │   │   ├── engine_components2.png
│   │   │   ├── exterior_accessories.png
│   │   │   ├── exterior_accessories2.png
│   │   │   ├── interior_accessories.png
│   │   │   ├── interior_accessories2.png
│   │   │   ├── maintenance_items.png
│   │   │   ├── maintenance_items2.png
│   │   │   ├── no_image_available.png
│   │   │   ├── no_image_available2.png
│   │   │   ├── performance_parts.png
│   │   │   ├── performance_parts2.png
│   │   │   ├── suspension_parts.png
│   │   │   ├── suspension_parts2.png
│   │   │   ├── thumbnail_template.png
│   │   │   └── thumbnail_template2.png
│   │   ├── status_notification/
│   │   │   ├── empty_fitment_catalog.png
│   │   │   ├── empty_fitment_catalog2.png
│   │   │   ├── empty_product_list.png
│   │   │   ├── empty_product_list2.png
│   │   │   ├── no_notifications.png
│   │   │   ├── no_order_history.png
│   │   │   ├── no_order_history2.png
│   │   │   ├── no_search_results.png
│   │   │   ├── status_icons.png
│   │   │   └── status_icons2.png
│   │   ├── testimonials/
│   │   │   ├── auto_repair.jpg
│   │   │   ├── citywide.jpg
│   │   │   ├── gt_performance.jpg
│   │   │   ├── midwest_auto.jpg
│   │   │   ├── pacific_auto.jpg
│   │   │   └── velocity_performance.jpg
│   │   └── vue.svg
│   ├── components/
│   │   ├── chat/
│   │   │   ├── AddMemberDialog.vue
│   │   │   ├── ChatContainer.vue
│   │   │   ├── ChatHeader.vue
│   │   │   ├── ChatInput.vue
│   │   │   ├── ChatMembers.vue
│   │   │   ├── ChatMessage.vue
│   │   │   ├── ChatMessages.vue
│   │   │   ├── ChatRoomDialog.vue
│   │   │   └── ChatRoomItem.vue
│   │   ├── common/
│   │   │   ├── ConfirmDialog.vue
│   │   │   └── NotificationSystem.vue
│   │   ├── faq/
│   │   │   └── FaqAccordion.vue
│   │   ├── layout/
│   │   │   ├── BlankLayout.vue
│   │   │   ├── DashboardFooter.vue
│   │   │   ├── DashboardLayout.vue
│   │   │   ├── MainFooter.vue
│   │   │   └── PublicLayout.vue
│   │   ├── HelloWorld.vue
│   │   └── LanguageSwitcher.vue
│   ├── i18n/
│   │   ├── locales/
│   │   │   └── en.json
│   │   └── index.ts
│   ├── router/
│   │   └── index.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── chat.ts
│   │   ├── fitment.ts
│   │   ├── fitmentProcessing.ts
│   │   ├── media.ts
│   │   ├── modelMapping.ts
│   │   ├── product.ts
│   │   └── user.ts
│   ├── stores/
│   │   └── auth.ts
│   ├── types/
│   │   ├── chat.ts
│   │   ├── fitment.ts
│   │   ├── media.ts
│   │   ├── product.ts
│   │   └── user.ts
│   ├── utils/
│   │   ├── error-handler.ts
│   │   ├── formatters.ts
│   │   └── notification.ts
│   ├── views/
│   │   ├── AboutPage.vue
│   │   ├── AccountDashboard.vue
│   │   ├── Blog.vue
│   │   ├── Careers.vue
│   │   ├── ChatPage.vue
│   │   ├── ContactPage.vue
│   │   ├── Dashboard.vue
│   │   ├── FAQ.vue
│   │   ├── FitmentCatalog.vue
│   │   ├── FitmentDetail.vue
│   │   ├── FitmentForm.vue
│   │   ├── LandingPage.vue
│   │   ├── Login.vue
│   │   ├── MediaLibrary.vue
│   │   ├── ModelMappingsManager.vue
│   │   ├── NotFound.vue
│   │   ├── OrderHistory.vue
│   │   ├── Partners.vue
│   │   ├── Pricing.vue
│   │   ├── PrivacyPolicy.vue
│   │   ├── ProductCatalog.vue
│   │   ├── ProductDetail.vue
│   │   ├── ProductFitments.vue
│   │   ├── ProductForm.vue
│   │   ├── ProductMedia.vue
│   │   ├── ResourcesPage.vue
│   │   ├── SavedLists.vue
│   │   ├── ServicesPage.vue
│   │   ├── Settings.vue
│   │   ├── ShippingReturns.vue
│   │   ├── TermsOfService.vue
│   │   ├── Testimonials.vue
│   │   ├── Unauthorized.vue
│   │   ├── UserDetail.vue
│   │   ├── UserForm.vue
│   │   ├── UserManagement.vue
│   │   └── UserProfile.vue
│   ├── App.vue
│   ├── main.ts
│   ├── style.css
│   └── vite-env.d.ts
├── README.md
├── index.html
├── package-lock.json
├── package.json
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

## Components
### AboutPage
**Path:** `src/views/AboutPage.vue`
**Type:** Composition API (script setup)

### AccountDashboard
**Path:** `src/views/AccountDashboard.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `accountMenu`: [
      { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/account/dashboard' },
      { title: 'Profile', icon: 'mdi-account', to: '/account/profile' },
      { title: 'Company Information', icon: 'mdi-domain', to: '/account/company' },
      { title: 'Payment Methods', icon: 'mdi-credit-card', to: '/account/payment-methods' },
      { title: 'Shipping Addresses', icon: 'mdi-map-marker', to: '/account/shipping-addresses' },
      { title: 'Team Members', icon: 'mdi-account-group', to: '/account/team' }
    ]
- `loading`: true
- `orderMenu`: [
      { title: 'Order History', icon: 'mdi-history', to: '/account/orders' },
      { title: 'Saved Lists', icon: 'mdi-format-list-bulleted', to: '/account/saved-lists' },
      { title: 'Quick Order', icon: 'mdi-flash', to: '/account/quick-order' },
      { title: 'Quotes & Estimates', icon: 'mdi-file-document-outline', to: '/account/quotes' },
      { title: 'Returns', icon: 'mdi-keyboard-return', to: '/account/returns' }
    ]
- `quickActions`: [
      { title: 'New Order', icon: 'mdi-cart-plus', to: '/products', color: 'primary' },
      { title: 'Quick Order', icon: 'mdi-flash', to: '/account/quick-order', color: 'secondary' },
      { title: 'Track Orders', icon: 'mdi-truck-delivery', to: '/account/orders', color: 'info' },
      { title: 'Support', icon: 'mdi-lifebuoy', to: '/account/support-tickets', color: 'error' },
      { title: 'Reorder', icon: 'mdi-refresh', to: '/account/orders?filter=reorder', color: 'success' },
      { title: 'Returns', icon: 'mdi-keyboard-return', to: '/account/returns', color: 'warning' }
    ]
- `quickStats`: [
      { title: 'Orders', value: '24', icon: 'mdi-package-variant', color: 'primary-lighten-5' },
      { title: 'Pending', value: '3', icon: 'mdi-clock-outline', color: 'warning-lighten-5' },
      { title: 'Returns', value: '1', icon: 'mdi-keyboard-return', color: 'error-lighten-5' },
      { title: 'Lists', value: '5', icon: 'mdi-format-list-bulleted', color: 'success-lighten-5' }
    ]
- `supportMenu`: [
      { title: 'Support Tickets', icon: 'mdi-lifebuoy', to: '/account/support-tickets' },
      { title: 'Downloads', icon: 'mdi-download', to: '/account/downloads' },
      { title: 'Settings', icon: 'mdi-cog', to: '/account/settings' }
    ]

#### Computed Properties
- `user`

#### Methods
- `async fetchAccountData()`
- `getOrderStatusColor()`
- `getUserInitials()`
- `isActiveRoute()`
- `logout()`
- `markAsRead()`

### AddMemberDialog
**Path:** `src/components/chat/AddMemberDialog.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| modelValue | boolean | Yes | - |
| roomId | string | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |
| role | - |
| update | - |
| userId | - |
| value | - |

#### Reactive State
**Refs:**
- `isSubmitting`: false
- `loadingUsers`: false
- `selectedRole`: ChatMemberRole.MEMBER

#### Methods
- `closeDialog()`
- `async loadUsers()`
- `resetForm()`
- `async submitForm()`

#### Watchers
- `() => props.modelValue`

#### Lifecycle Hooks
- `mounted`

### App
**Path:** `src/App.vue`
**Type:** Composition API

#### Computed Properties
- `layout`

### BlankLayout
**Path:** `src/components/layout/BlankLayout.vue`
**Type:** Options API

### Blog
**Path:** `src/views/Blog.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `categories`: [
      'Industry News',
      'Product Updates',
      'Technical Tips',
      'Case Studies',
      'Market Trends',
      'Company News'
    ]
- `deleteDialog`: false
- `deleteLoading`: false
- `email`: ''
- `itemsPerPage`: 5
- `loading`: true
- `page`: 1
- `privacyConsent`: false
- `searchQuery`: ''
- `sortOptions`: [
      { title: 'Newest First', value: 'newest' },
      { title: 'Oldest First', value: 'oldest' },
      { title: 'Most Popular', value: 'popular' },
      { title: 'Alphabetical', value: 'alphabetical' }
    ]
- `sortOrder`: 'newest'
- `subscribeDialog`: false
- `subscribing`: false
- `totalItems`: 0

#### Computed Properties
- `isAdmin`

#### Methods
- `applyFilters()`
- `clearSearch()`
- `confirmDelete()`
- `async deletePost()`
- `async fetchPosts()`
- `filterPosts()`
- `getCategoryCount()`
- `resetFilters()`
- `searchPosts()`
- `async subscribeNewsletter()`

### Careers
**Path:** `src/views/Careers.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `benefits`: [
      {
        title: 'Innovate & Make an Impact',
        icon: 'lightbulb',
        description: 'Work on cutting-edge technology that\'s transforming an entire industry. Your contributions will directly impact thousands of businesses and help shape the future of automotive commerce.'
      },
      {
        title: 'Collaborative & Inclusive Culture',
        icon: 'account-group',
        description: 'Join a diverse team that values different perspectives and fosters collaboration. We believe the best solutions come from combining our unique strengths and experiences.'
      },
      {
        title: 'Grow Your Career',
        icon: 'chart-line',
        description: 'We\'re committed to your professional development with clear career paths, mentorship programs, continuous learning opportunities, and regular feedback to help you reach your goals.'
      },
      {
        title: 'Work-Life Balance',
        icon: 'balance-scale',
        description: 'We believe in sustainable performance. Enjoy flexible work arrangements, generous PTO, and a culture that respects boundaries to ensure you can perform at your best.'
      },
      {
        title: 'Be Part of Something Bigger',
        icon: 'earth',
        description: 'Our platform helps reduce waste, optimize supply chains, and improve efficiency across the automotive aftermarket. Your work will contribute to more sustainable practices in a major global industry.'
      },
      {
        title: 'Competitive Compensation',
        icon: 'cash-multiple',
        description: 'We offer competitive salaries, performance bonuses, equity options for eligible positions, and a comprehensive benefits package designed to support your health and financial wellbeing.'
      }
    ]
- `companyStats`: [
      { value: '5,000+', label: 'Business Customers' },
      { value: '120+', label: 'Team Members' },
      { value: '4', label: 'Office Locations' },
      { value: '25+', label: 'Countries Served' }
    ]
- `galleryDialog`: false
- `galleryIndex`: 0
- `loading`: true
- `perks`: [
      { title: 'Health Insurance', icon: 'heart-pulse' },
      { title: 'Dental & Vision', icon: 'eye' },
      { title: '401(k

#### Computed Properties
- `departments`
- `filteredJobs`

#### Methods
- `async fetchJobs()`
- `nextImage()`
- `openGallery()`
- `prevImage()`
- `scrollToJobs()`

### ChatContainer
**Path:** `src/components/chat/ChatContainer.vue`
**Type:** Composition API (script setup)

#### Reactive State
**Refs:**
- `searchQuery`: ''
- `showAddMemberDialog`: false
- `showCreateRoomDialog`: false
- `showMembersPanel`: false
- `showRemoveMemberDialog`: false
- `sidebarCollapsed`: false

#### Computed Properties
- `activeRoomId`
- `currentUserId`

#### Methods
- `async addMember(userId: string, role: string)`
- `confirmRemoveMember(member: ChatMember)`
- `async createRoom(name: string, type: ChatRoomType, members: any[])`
- `deleteMessage(messageId: string)`
- `editMessage(messageId: string, content: string)`
- `handleReaction(messageId: string, reaction: string, isAdding: boolean)`
- `handleTyping(isTyping: boolean)`
- `joinRoom(roomId: string)`
- `loadMoreMessages(beforeId: string)`
- `async removeMemberConfirmed()`
- `sendMessage(content: string)`
- `toggleSidebar()`
- `async updateMemberRole(userId: string, role: string)`

#### Watchers
- `() => router.currentRoute.value.query.room`

#### Lifecycle Hooks
- `mounted`

### ChatHeader
**Path:** `src/components/chat/ChatHeader.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| onlineCount | number | Yes | - |
| room | ChatRoom | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |

#### Reactive State
**Refs:**
- `notificationLevel`: 'all'
- `showLeaveDialog`: false
- `showNotificationSettings`: false
- `showRoomInfo`: false

#### Computed Properties
- `avatarText`
- `canLeaveRoom`
- `displayName`
- `roomTypeDisplay`
- `statusText`

#### Methods
- `confirmLeaveRoom()`
- `formatDate(dateStr: string)`
- `async leaveRoom()`
- `async saveNotificationSettings()`

### ChatInput
**Path:** `src/components/chat/ChatInput.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| roomId | string | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| content | - |
| e | - |
| isTyping | - |

#### Reactive State
**Refs:**
- `isTyping`: false
- `messageText`: ''

#### Computed Properties
- `canSend`
- `fileIcon`
- `typingText`
- `typingUsers`

#### Methods
- `clearAttachment()`
- `formatFileSize(bytes: number)`
- `getMessageType(file: File)`
- `handleBlur()`
- `handleFileSelected(event: Event)`
- `handleFocus()`
- `handleInput()`
- `handleKeydown(event: KeyboardEvent)`
- `sendMessage()`
- `startTyping()`
- `stopTyping()`

#### Lifecycle Hooks
- `beforeunmount`

### ChatMembers
**Path:** `src/components/chat/ChatMembers.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| currentUserId | string | Yes | - |
| members | ChatMember[] | Yes | - |
| room | ChatRoom | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |
| member | - |
| role | - |
| userId | - |

#### Reactive State
**Refs:**
- `searchQuery`: ''
- `showMenu`: false

#### Computed Properties
- `currentUserRole`
- `filteredMembers`
- `offlineMembers`
- `onlineMembers`

#### Methods
- `canManageUser(member: ChatMember)`
- `getMemberInitials(name: string)`
- `getMemberRoleDisplay(role: string)`
- `isCurrentUser(member: ChatMember)`
- `removeMember(member: ChatMember)`
- `updateMemberRole(userId: string, role: string)`

### ChatMessage
**Path:** `src/components/chat/ChatMessage.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| isOwnMessage | boolean | Yes | - |
| message | ChatMessage | Yes | - |
| showSender | boolean | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| content | - |
| e | - |
| isAdding | - |
| messageId | - |
| reaction | - |

#### Reactive State
**Refs:**
- `editContent`: ''
- `isEditing`: false
- `showDeleteDialog`: false
- `showReactionMenu`: false

#### Computed Properties
- `canDelete`
- `canEdit`
- `currentUserId`
- `hasReactions`

#### Methods
- `addReaction(reaction: string)`
- `cancelEdit()`
- `confirmDelete()`
- `deleteMessage()`
- `formatTime(dateStr: string)`
- `saveEdit()`
- `startEdit()`
- `toggleReaction(reaction: string, users: string[])`

### ChatMessages
**Path:** `src/components/chat/ChatMessages.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| currentUserId | string | Yes | - |
| messages | ChatMessage[] | Yes | - |
| roomId | string | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| beforeId | - |
| content | - |
| e | - |
| isAdding | - |
| messageId | - |
| reaction | - |

#### Reactive State
**Refs:**
- `hasReachedTop`: false
- `isLoadingMore`: false
- `lastHeight`: 0
- `lastScrollTop`: 0
- `shouldScrollToBottom`: true

#### Computed Properties
- `canLoadMore`
- `typingText`
- `typingUsers`

#### Methods
- `formatDateSeparator(dateStr: string)`
- `handleDelete(messageId: string)`
- `handleEdit(messageId: string, content: string)`
- `handleReaction(messageId: string, reaction: string, isAdding: boolean)`
- `handleScroll()`
- `loadMore()`
- `restoreScrollPosition()`
- `scrollToBottom()`
- `shouldShowDateSeparator(message: ChatMessage, index: number)`
- `shouldShowSender(message: ChatMessage, index: number)`

#### Lifecycle Hooks
- `mounted`
- `updated`

### ChatPage
**Path:** `src/views/ChatPage.vue`
**Type:** Composition API (script setup)

#### Lifecycle Hooks
- `beforeunmount`
- `mounted`

### ChatRoomDialog
**Path:** `src/components/chat/ChatRoomDialog.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| modelValue | boolean | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |
| members | - |
| name | - |
| type | - |
| update | - |
| value | - |

#### Reactive State
**Refs:**
- `isSubmitting`: false
- `loadingUsers`: false
- `roomName`: ''
- `roomType`: ChatRoomType.GROUP

#### Methods
- `closeDialog()`
- `async loadUsers()`
- `resetForm()`
- `async submitForm()`

#### Watchers
- `() => props.modelValue`

#### Lifecycle Hooks
- `mounted`

### ChatRoomItem
**Path:** `src/components/chat/ChatRoomItem.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| active | boolean | Yes | - |
| room | ChatRoom | Yes | - |

#### Computed Properties
- `avatarText`
- `displayName`
- `formattedTime`
- `messagePreview`

#### Methods
- `getOtherUserName()`

### ConfirmDialog
**Path:** `src/components/common/ConfirmDialog.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| Boolean | Any | No | - |
| String | Any | No | - |
| cancelText | String | No | 'Cancel' |
| dangerConfirm | Boolean | No | false |
| message | String | No | 'Are you sure you want to proceed?' |
| modelValue | Boolean | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |
| update | - |
| value | - |

#### Reactive State
**Refs:**
- `isLoading`: false

#### Methods
- `cancel()`
- `confirm()`

#### Watchers
- `() => props.dangerConfirm`

### ContactPage
**Path:** `src/views/ContactPage.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `formSubmitting`: false
- `formValid`: false
- `newsletterEmail`: ''
- `newsletterSubmitting`: false
- `referenceNumber`: ''
- `showSuccessDialog`: false

**Reactive Objects:**
- `formData`: {
      company: '',
      businessType: '',
      name: '',
      title: '',
      email: '',
      phone: '',
      inquiryType: '',
      message: ''
    }

#### Methods
- `async submitForm()`
- `async subscribeNewsletter()`

### Dashboard
**Path:** `src/views/Dashboard.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activities`: [
      {
        title: 'New product added: Brake Pads X500',
        timestamp: new Date(Date.now(
- `loading`: false
- `quickActions`: [
      {
        title: 'Add Product',
        icon: 'mdi-plus-circle',
        link: '/products/new'
      },
      {
        title: 'Add Fitment',
        icon: 'mdi-car-plus',
        link: '/fitments/new'
      },
      {
        title: 'Upload Media',
        icon: 'mdi-cloud-upload',
        link: '/media/upload'
      },
      {
        title: 'Search',
        icon: 'mdi-magnify',
        link: '/search'
      },
      {
        title: 'Reports',
        icon: 'mdi-chart-bar',
        link: '/reports'
      },
      {
        title: 'Settings',
        icon: 'mdi-cog',
        link: '/settings'
      }
    ]
- `stats`: [
      {
        title: 'Products',
        subtitle: 'Total products in catalog',
        value: '0',
        icon: 'mdi-package-variant-closed',
        color: 'primary',
        link: '/products'
      },
      {
        title: 'Fitments',
        subtitle: 'Vehicle compatibility',
        value: '0',
        icon: 'mdi-car',
        color: 'success',
        link: '/fitments'
      },
      {
        title: 'Media',
        subtitle: 'Images and documents',
        value: '0',
        icon: 'mdi-image-multiple',
        color: 'info',
        link: '/media'
      },
      {
        title: 'Users',
        subtitle: 'Active accounts',
        value: '0',
        icon: 'mdi-account-group',
        color: 'warning',
        link: '/users'
      }
    ]

#### Methods
- `async fetchDashboardData()`
- `refreshData()`

### DashboardFooter
**Path:** `src/components/layout/DashboardFooter.vue`
**Type:** Composition API

### DashboardLayout
**Path:** `src/components/layout/DashboardLayout.vue`
**Type:** Composition API

#### Methods
- `async initializeAuth()`
- `logout()`

### FAQ
**Path:** `src/views/FAQ.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeTab`: 'all'
- `loading`: true
- `searchQuery`: ''

#### Computed Properties
- `isAdmin`

#### Methods
- `async fetchFaqs()`
- `getFaqsByCategory()`
- `openLiveChat()`
- `searchFaqs()`

### FaqAccordion
**Path:** `src/components/faq/FaqAccordion.vue`
**Type:** Composition API

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| faqs | Array | Yes | - |

#### Reactive State
**Refs:**
- `deleteDialog`: false
- `deleteLoading`: false

#### Methods
- `confirmDelete()`
- `async copyLink()`
- `async deleteFaq()`
- `formatAnswer()`
- `async submitFeedback()`

### FitmentCatalog
**Path:** `src/views/FitmentCatalog.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `deleteDialog`: false
- `deleteLoading`: false
- `itemsPerPage`: 10
- `loading`: false
- `page`: 1
- `totalItems`: 0
- `totalPages`: 1

#### Computed Properties
- `isAdmin`

#### Methods
- `confirmDelete()`
- `async deleteFitment()`
- `async fetchFitments()`
- `resetFilters()`

### FitmentDetail
**Path:** `src/views/FitmentDetail.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `addProductLoading`: false
- `deleteDialog`: false
- `deleteLoading`: false
- `loading`: true
- `productsLoading`: false
- `removeProductDialog`: false
- `removeProductLoading`: false
- `showAddProductDialog`: false

#### Computed Properties
- `isAdmin`

#### Methods
- `async addProduct()`
- `confirmDelete()`
- `confirmRemoveProduct()`
- `async deleteFitment()`
- `async fetchAvailableProducts()`
- `async fetchFitment()`
- `async fetchProducts()`
- `async fetchSimilarFitments()`
- `async removeProductAssociation()`

### FitmentForm
**Path:** `src/views/FitmentForm.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `formDirty`: false
- `formError`: ''
- `initialLoading`: false
- `isFormValid`: false
- `loading`: false
- `partApplications`: ''
- `processingApplications`: false
- `productId`: ''
- `showProcessingInfo`: false
- `showUnsavedDialog`: false

#### Methods
- `addAttribute()`
- `clearError()`
- `discardChanges()`
- `async fetchAssociatedProducts()`
- `async fetchFitment()`
- `navigationGuard()`
- `objectToAttributes()`
- `async processPartApplications()`
- `removeAttribute()`
- `async submitForm()`

### HelloWorld
**Path:** `src/components/HelloWorld.vue`
**Type:** Composition API (script setup)

#### Reactive State
**Refs:**
- `count`: 0

### LandingPage
**Path:** `src/views/LandingPage.vue`
**Type:** Composition API (script setup)

#### Methods
- `goToCategory()`

### LanguageSwitcher
**Path:** `src/components/LanguageSwitcher.vue`
**Type:** Composition API (script setup)

#### Reactive State
**Refs:**
- `currentLocale`: locale.value

#### Methods
- `async changeLocale()`

#### Lifecycle Hooks
- `mounted`

### Login
**Path:** `src/views/Login.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `password`: ''
- `rememberMe`: true
- `showPassword`: false
- `username`: ''

#### Computed Properties
- `loading`

#### Methods
- `async login()`

### MainFooter
**Path:** `src/components/layout/MainFooter.vue`
**Type:** Composition API

### MediaLibrary
**Path:** `src/views/MediaLibrary.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `associateForm`: {
      product_id: null as string | null
    }
- `associateLoading`: false
- `batchDeleteLoading`: false
- `dateMenu`: false
- `deleteLoading`: false
- `editForm`: {
      filename: '',
      alt_text: '',
      description: '',
      product_id: null as string | null
    }
- `editLoading`: false
- `fileTypeOptions`: [
      { title: 'All Files', value: 'all' },
      { title: 'Images', value: 'image' },
      { title: 'Documents', value: 'document' }
    ]
- `headers`: [
      { title: 'Filename', key: 'filename', sortable: true },
      { title: 'Type', key: 'mime_type', sortable: true },
      { title: 'Size', key: 'size', sortable: true },
      { title: 'Uploaded', key: 'created_at', sortable: true },
      { title: 'Product', key: 'product', sortable: false },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]
- `isDragging`: false
- `isEditFormValid`: true
- `loading`: true
- `page`: 1
- `pageSize`: 20
- `search`: ''
- `showAdvancedFilters`: false
- `showAssociateDialog`: false
- `showBatchDeleteDialog`: false
- `showDeleteDialog`: false
- `showEditDialog`: false
- `showPreviewDialog`: false
- `showUploadDialog`: false
- `sortOption`: 'newest'
- `sortOptions`: [
      { title: 'Newest First', value: 'newest' },
      { title: 'Oldest First', value: 'oldest' },
      { title: 'Name A-Z', value: 'name_asc' },
      { title: 'Name Z-A', value: 'name_desc' },
      { title: 'Size (Largest
- `totalPages`: 1
- `uploadForm`: {
      product_id: null as string | null
    }
- `uploadProgress`: 0
- `uploading`: false

#### Computed Properties
- `dateRangeText`
- `documentCount`
- `hasSelectedWithProducts`
- `imageCount`
- `totalSize`

#### Methods
- `addFileToUpload()`
- `applyClientSideFilters()`
- `applyFilters()`
- `associateWithProduct()`
- `batchAssociateProduct()`
- `async batchDeleteMedia()`
- `bulkDownload()`
- `cancelUpload()`
- `clearDateRange()`
- `async confirmAssociate()`
- `confirmBatchDelete()`
- `confirmDeleteFromPreview()`
- `confirmDeleteMedia()`
- `async deleteMedia()`
- `downloadMedia()`
- `editFromPreview()`
- `editMedia()`
- `async fetchMedia()`
- `async fetchProductOptions()`
- `async fetchRecentUploads()`
- `handleFileDrop()`
- `handleFileSelect()`
- `openMediaPreview()`
- `removeFileFromUpload()`
- `resetFilters()`
- `async saveMediaEdit()`
- `toggleSelect()`
- `async uploadFiles()`

### ModelMappingsManager
**Path:** `src/views/ModelMappingsManager.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `currentPage`: 1
- `debug`: true
- `deleteDialog`: false
- `deletingMapping`: false
- `editMode`: false
- `filters`: {
      pattern: '',
    }
- `initialLoading`: true
- `itemsPerPage`: 10
- `loading`: false
- `mappingDialog`: false
- `savingMapping`: false
- `totalMappings`: 0
- `uploading`: false

#### Methods
- `applyFilter()`
- `confirmDelete()`
- `async deleteMapping()`
- `editMapping()`
- `async loadMappings()`
- `async refreshMappings()`
- `async saveMapping()`
- `saveMappingForm()`
- `showAddMappingDialog()`
- `async toggleActive()`
- `async uploadMappings()`

### NotFound
**Path:** `src/views/NotFound.vue`
**Type:** Composition API (script setup)

#### Methods
- `goBack()`

### NotificationSystem
**Path:** `src/components/common/NotificationSystem.vue`
**Type:** Composition API

#### Computed Properties
- `notifications`

#### Methods
- `closeNotification()`
- `getVariant()`

### OrderHistory
**Path:** `src/views/OrderHistory.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `cancellationReasons`: [
      'Ordered by mistake',
      'Found better price elsewhere',
      'Taking too long to ship',
      'Changed my mind',
      'Incorrect item(s
- `dateRange`: {
      from: '',
      to: ''
    }
- `itemsPerPage`: 10
- `loading`: true
- `orderStatuses`: [
      'Pending',
      'Processing',
      'Shipped',
      'Delivered',
      'Cancelled',
      'On Hold',
      'Backordered'
    ]
- `orderTypes`: [
      'Standard',
      'Rush',
      'Dropship',
      'Backorder',
      'Will Call'
    ]
- `page`: 1
- `paymentMethods`: [
      'Credit Card',
      'Purchase Order',
      'Net 30',
      'ACH Transfer',
      'Wire Transfer'
    ]
- `search`: ''
- `showAdvancedFilters`: false
- `tableHeaders`: [
      { title: 'Order #', key: 'order_number', sortable: true },
      { title: 'Date', key: 'order_date', sortable: true },
      { title: 'Total', key: 'total', sortable: true },
      { title: 'Status', key: 'status', sortable: true },
      { title: 'Shipping', key: 'shipping', sortable: false },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]

#### Computed Properties
- `filteredOrders`
- `paginatedMobileOrders`

#### Methods
- `applyFilters()`
- `canCancel()`
- `canReturn()`
- `cancelOrder()`
- `async confirmCancelOrder()`
- `downloadInvoice()`
- `exportToExcel()`
- `exportToPdf()`
- `async fetchOrders()`
- `getStatusColor()`
- `getTrackingUrl()`
- `printOrders()`
- `async reorder()`
- `resetFilters()`

### Partners
**Path:** `src/views/Partners.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeTab`: 'manufacturers'
- `techTab`: 'all'

#### Methods
- `filteredTechPartners()`

### Pricing
**Path:** `src/views/Pricing.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `additionalServices`: [
      {
        title: 'Data Migration & Setup',
        description: 'Our team will help migrate your existing product data, customer information, and historical orders into Crown Nexus to ensure a smooth transition.',
        image: 'https://via.placeholder.com/600x400?text=Data+Migration',
        link: '/services/data-migration'
      },
      {
        title: 'Custom Integration Development',
        description: 'Need to connect Crown Nexus with your ERP, CRM, or other business systems? Our developers can build custom integrations tailored to your specific requirements.',
        image: 'https://via.placeholder.com/600x400?text=Custom+Integration',
        link: '/services/custom-integration'
      },
      {
        title: 'Training & Implementation',
        description: 'Comprehensive training for your team to ensure everyone knows how to leverage Crown Nexus effectively. Includes personalized implementation support.',
        image: 'https://via.placeholder.com/600x400?text=Training',
        link: '/services/training'
      }
    ]
- `billingPeriod`: 'monthly'
- `faqs`: [
      {
        question: 'Can I upgrade or downgrade my plan later?',
        answer: 'Yes, you can upgrade your plan at any time, and the new pricing will be prorated for the remainder of your billing cycle. Downgrades take effect at the start of your next billing cycle.'
      },
      {
        question: 'What happens if I exceed my plan limits?',
        answer: 'If you exceed your plan limits (such as number of users or SKUs
- `growthDistributorBenefits`: [
      {
        icon: 'mdi-chart-line',
        title: 'Scalable Pricing',
        description: 'Pricing that grows with your business with predictable costs'
      },
      {
        icon: 'mdi-book-open-variant',
        title: 'Training & Onboarding',
        description: 'Comprehensive training program to get your team up to speed quickly'
      },
      {
        icon: 'mdi-tools',
        title: 'Business Development Tools',
        description: 'Access to tools and resources designed to help you grow your customer base'
      },
      {
        icon: 'mdi-account-group',
        title: 'Community Access',
        description: 'Join our distributor community for networking and knowledge sharing'
      },
      {
        icon: 'mdi-star',
        title: 'Pathway to Partner Program',
        description: 'Clear criteria and support to advance to our Partner Distributor Program'
      }
    ]
- `partnerDistributorBenefits`: [
      {
        icon: 'mdi-cash-multiple',
        title: 'Preferential Pricing',
        description: 'Access to wholesale pricing with volume-based discounts'
      },
      {
        icon: 'mdi-database',
        title: 'Enhanced Product Data',
        description: 'Premium access to comprehensive fitment data and rich product content'
      },
      {
        icon: 'mdi-api',
        title: 'Integration APIs',
        description: 'Enterprise-level API access for seamless integration with your existing systems'
      },
      {
        icon: 'mdi-account-tie',
        title: 'Dedicated Account Manager',
        description: 'Personal support from a dedicated account manager for your business'
      },
      {
        icon: 'mdi-handshake',
        title: 'Co-Marketing Opportunities',
        description: 'Joint marketing initiatives and promotional opportunities'
      }
    ]
- `plans`: [
      {
        id: 'starter',
        name: 'Starter',
        subtitle: 'For small businesses and startups',
        monthlyPrice: 249,
        annualPrice: 212, // 15% discount
        buttonText: 'Get Started',
        highlighted: false,
        features: [
          { text: 'Up to 3 users', included: true },
          { text: 'Product catalog management', included: true },
          { text: 'Basic fitment data', included: true },
          { text: '5,000 SKUs', included: true },
          { text: 'Standard support', included: true },
          { text: 'Inventory management', included: true },
          { text: 'Order processing', included: true },
          { text: 'Customer management', included: true },
          { text: 'Advanced analytics', included: false },
          { text: 'API access', included: false },
          { text: 'Custom branding', included: false },
          { text: 'Dedicated account manager', included: false }
        ]
      },
      {
        id: 'professional',
        name: 'Professional',
        subtitle: 'For growing businesses',
        monthlyPrice: 499,
        annualPrice: 424, // 15% discount
        buttonText: 'Get Started',
        highlighted: true,
        features: [
          { text: 'Up to 10 users', included: true },
          { text: 'Product catalog management', included: true },
          { text: 'Premium fitment data', included: true },
          { text: '25,000 SKUs', included: true },
          { text: 'Priority support', included: true },
          { text: 'Inventory management', included: true },
          { text: 'Order processing', included: true },
          { text: 'Customer management', included: true },
          { text: 'Advanced analytics', included: true },
          { text: 'API access', included: true },
          { text: 'Custom branding', included: true },
          { text: 'Dedicated account manager', included: false }
        ]
      },
      {
        id: 'enterprise',
        name: 'Enterprise',
        subtitle: 'For large organizations',
        monthlyPrice: 999,
        annualPrice: 849, // 15% discount
        buttonText: 'Contact Sales',
        highlighted: false,
        features: [
          { text: 'Unlimited users', included: true },
          { text: 'Product catalog management', included: true },
          { text: 'Premium fitment data', included: true },
          { text: 'Unlimited SKUs', included: true },
          { text: '24/7 premium support', included: true },
          { text: 'Inventory management', included: true },
          { text: 'Order processing', included: true },
          { text: 'Customer management', included: true },
          { text: 'Advanced analytics', included: true },
          { text: 'API access', included: true },
          { text: 'Custom branding', included: true },
          { text: 'Dedicated account manager', included: true }
        ]
      }
    ]
- `volumeTiers`: [
      {
        volume: '1-500 transactions/month',
        standardRate: '$2.50 per transaction',
        discount: '0%',
        discountedRate: '$2.50 per transaction'
      },
      {
        volume: '501-2,000 transactions/month',
        standardRate: '$2.50 per transaction',
        discount: '10%',
        discountedRate: '$2.25 per transaction'
      },
      {
        volume: '2,001-5,000 transactions/month',
        standardRate: '$2.50 per transaction',
        discount: '20%',
        discountedRate: '$2.00 per transaction'
      },
      {
        volume: '5,001-10,000 transactions/month',
        standardRate: '$2.50 per transaction',
        discount: '30%',
        discountedRate: '$1.75 per transaction'
      },
      {
        volume: '10,001+ transactions/month',
        standardRate: '$2.50 per transaction',
        discount: 'Custom',
        discountedRate: 'Contact Sales'
      }
    ]

#### Computed Properties
- `isMobile`

### PrivacyPolicy
**Path:** `src/views/PrivacyPolicy.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `sections`: [
      {
        id: 'introduction',
        title: '1. Introduction',
        content: `
          <p>Crown Nexus ("we," "our," or "us"

#### Methods
- `printPolicy()`
- `scrollToSection()`

### ProductCatalog
**Path:** `src/views/ProductCatalog.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `attributeFilter`: ''
- `deleteDialog`: false
- `deleteLoading`: false
- `itemsPerPage`: 10
- `loading`: false
- `page`: 1
- `search`: ''
- `showAdvancedFilters`: false
- `totalItems`: 0
- `totalPages`: 1

#### Computed Properties
- `isAdmin`

#### Methods
- `confirmDelete()`
- `async deleteProduct()`
- `async fetchCategories()`
- `async fetchProducts()`
- `resetFilters()`

### ProductDetail
**Path:** `src/views/ProductDetail.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `currentMediaIndex`: 0
- `deleteDialog`: false
- `deleteLoading`: false
- `loading`: true
- `mediaDialog`: false

#### Computed Properties
- `isAdmin`
- `productId`

#### Methods
- `confirmDelete()`
- `async deleteProduct()`
- `async fetchFitments()`
- `async fetchMedia()`
- `async fetchProduct()`
- `openMediaDialog()`

### ProductFitments
**Path:** `src/views/ProductFitments.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `addFilters`: {
      year: null as number | null,
      make: null as string | null,
      model: null as string | null,
      search: ''
    }
- `bulkLoading`: false
- `initialLoading`: true
- `loading`: false
- `page`: 1
- `pageSize`: 10
- `removeLoading`: false
- `removeMultipleLoading`: false
- `search`: ''
- `searchLoading`: false
- `searchPerformed`: false
- `showAddDialog`: false
- `showBulkDialog`: false
- `showRemoveDialog`: false
- `showRemoveMultipleDialog`: false
- `totalPages`: 1

#### Computed Properties
- `availableYears`
- `estimatedBulkCount`
- `productId`
- `totalFitments`
- `uniqueModels`
- `yearRange`

#### Methods
- `async addFitment()`
- `async bulkAddFitments()`
- `confirmRemoveSelected()`
- `confirmRemoveSingle()`
- `async fetchAvailableMakes()`
- `async fetchAvailableModels()`
- `async fetchAvailableYears()`
- `async fetchFitments()`
- `async fetchProduct()`
- `filterFitments()`
- `paginate()`
- `async removeFitment()`
- `async removeSelectedFitments()`
- `async searchFitments()`

### ProductForm
**Path:** `src/views/ProductForm.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `formDirty`: false
- `formError`: ''
- `initialLoading`: false
- `isFormValid`: false
- `loading`: false
- `showUnsavedDialog`: false

#### Methods
- `addAttribute()`
- `clearError()`
- `discardChanges()`
- `async fetchCategories()`
- `async fetchProduct()`
- `navigationGuard()`
- `objectToAttributes()`
- `removeAttribute()`
- `async submitForm()`

### ProductMedia
**Path:** `src/views/ProductMedia.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `deleteLoading`: false
- `editForm`: {
      filename: '',
      alt_text: '',
      description: ''
    }
- `editLoading`: false
- `initialLoading`: true
- `isDragging`: false
- `isEditFormValid`: true
- `reorderLoading`: false
- `showDeleteDialog`: false
- `showEditDialog`: false
- `showPreviewDialog`: false
- `showReorderDialog`: false
- `showUploadDialog`: false
- `uploadProgress`: 0
- `uploading`: false

#### Computed Properties
- `documentCount`
- `primaryMedia`
- `productId`

#### Methods
- `addFileToUpload()`
- `cancelUpload()`
- `confirmDeleteMedia()`
- `async deleteMedia()`
- `editMedia()`
- `async fetchMedia()`
- `async fetchProduct()`
- `handleFileDrop()`
- `handleFileSelect()`
- `openMediaPreview()`
- `removeFileFromUpload()`
- `async saveMediaEdit()`
- `async saveMediaOrder()`
- `async setPrimaryMedia()`
- `async uploadFiles()`

### PublicLayout
**Path:** `src/components/layout/PublicLayout.vue`
**Type:** Options API

### ResourcesPage
**Path:** `src/views/ResourcesPage.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeTab`: 'installation'
- `currentCategory`: 'all'
- `dateFilter`: ''
- `resourceTypeFilter`: ''
- `searchQuery`: ''
- `subscribeEmail`: ''
- `subscribeLoading`: false

#### Computed Properties
- `filteredResources`
- `getCurrentCategory`

#### Methods
- `downloadResource()`
- `getTechLibDocs()`
- `navigateTo()`
- `resetFilters()`
- `searchResources()`
- `subscribeToResources()`
- `viewDocument()`

### SavedLists
**Path:** `src/views/SavedLists.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `listLoading`: false
- `listTypes`: [
      'Standard',
      'Favorites',
      'Reorder',
      'Wishlist',
      'Seasonal',
      'Regular Stock'
    ]
- `loading`: true
- `permissionLevels`: [
      'View',
      'Edit',
      'Full Access'
    ]
- `productSearch`: ''
- `productSearchHeaders`: [
      { title: 'Product', key: 'product', sortable: false },
      { title: 'Price', key: 'price', sortable: true },
      { title: 'Quantity', key: 'quantity', sortable: false },
      { title: 'Availability', key: 'in_stock', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]
- `quickOrderHeaders`: [
      { title: 'Product', key: 'product_name', sortable: false },
      { title: 'Price', key: 'price', sortable: true },
      { title: 'Quantity', key: 'quantity', sortable: false },
      { title: 'Subtotal', key: 'subtotal', sortable: true },
      { title: 'Status', key: 'status', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]
- `quickOrderLoading`: false
- `quickOrderText`: ''
- `searchLoading`: false
- `showAddProductsDialog`: false
- `tableHeaders`: [
      { title: 'Product', key: 'product', sortable: false },
      { title: 'Price', key: 'price', sortable: true },
      { title: 'Quantity', key: 'quantity', sortable: false },
      { title: 'Subtotal', key: 'subtotal', sortable: true },
      { title: 'Status', key: 'in_stock', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]

#### Computed Properties
- `hasSelectedProducts`
- `hasValidQuickOrderItems`
- `isShareButtonDisabled`

#### Methods
- `async addAllQuickOrderToCart()`
- `async addAllToCart()`
- `async addProductToList()`
- `addSelectedProducts()`
- `async addToCart()`
- `calculateListTotal()`
- `confirmDeleteList()`
- `async copyShareLink()`
- `createNewList()`
- `async deleteList()`
- `async exportList()`
- `async fetchSavedLists()`
- `getListTypeColor()`
- `getStatusColor()`
- `getStatusText()`
- `async processQuickOrder()`
- `async removeFromList()`
- `renameList()`
- `async saveList()`
- `saveQuickOrderAsList()`
- `async saveQuickOrderList()`
- `async searchProducts()`
- `shareList()`
- `async submitShare()`
- `async toggleFavorite()`
- `async updateQuantity()`
- `viewList()`

### ServicesPage
**Path:** `src/views/ServicesPage.vue`
**Type:** Composition API

### Settings
**Path:** `src/views/Settings.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeIntegrationTab`: 'api'
- `activeSection`: 'general'
- `clearingCache`: false
- `creatingBackup`: false
- `emailSettings`: {
      smtp_host: 'smtp.example.com',
      smtp_port: 587,
      smtp_username: 'username',
      smtp_password: 'password',
      smtp_encryption: true,
      from_email: 'noreply@crownnexus.com',
      from_name: 'Crown Nexus',
      email_template: 'default'
    }
- `generalSettings`: {
      company_name: 'Crown Nexus',
      currency: 'USD',
      date_format: 'MM/DD/YYYY',
      timezone: 'America/New_York',
      language: 'en',
      items_per_page: 20
    }
- `integrationSettings`: {
      api_enabled: true,
      api_url: 'https://api.crownnexus.com/v1',
      api_rate_limit: 100,
      api_key: 'sk_live_example123456789abcdef',
      webhooks_enabled: false,
      crm_provider: 'none' as 'none' | 'salesforce' | 'hubspot' | 'zoho' | 'dynamics',
      crm_api_key: '',
      crm_instance_url: '',
      crm_sync_customers: false,
      crm_sync_products: false
    }
- `isEmailFormValid`: true
- `isGeneralFormValid`: true
- `isUserSettingsFormValid`: true
- `rebuildingSearch`: false
- `savingEmail`: false
- `savingGeneral`: false
- `savingIntegration`: false
- `savingSystem`: false
- `savingTheme`: false
- `savingUserSettings`: false
- `sendingTestEmail`: false
- `systemInfo`: {
      version: '1.5.2',
      last_updated: new Date(Date.now(
- `systemSettings`: {
      maintenance_mode: false,
      maintenance_message: 'The system is currently undergoing scheduled maintenance. Please check back later.',
      log_level: 'info' as 'debug' | 'info' | 'warning' | 'error' | 'critical',
      auto_backup: true,
      backup_frequency: 'daily' as 'daily' | 'weekly' | 'monthly',
      backup_retention: 30
    }
- `testEmailAddress`: ''
- `testingCrm`: false
- `themeSettings`: {
      mode: 'light' as 'light' | 'dark' | 'system',
      primary_color: '#1976D2',
      secondary_color: '#424242'
    }
- `userSettings`: {
      require_strong_password: true,
      password_expiry_days: 90,
      enable_2fa: false,
      session_timeout: 30,
      registration_mode: 'closed' as 'closed' | 'approval' | 'open',
      default_role: UserRole.CLIENT
    }

#### Methods
- `addWebhook()`
- `async clearSystemCache()`
- `copyApiKey()`
- `async createBackup()`
- `downloadLogs()`
- `goToApiKeyManager()`
- `async rebuildSearch()`
- `async regenerateApiKey()`
- `removeWebhook()`
- `async saveEmailSettings()`
- `async saveGeneralSettings()`
- `async saveIntegrationSettings()`
- `async saveSystemSettings()`
- `async saveThemeSettings()`
- `async saveUserSettings()`
- `async sendTestEmail()`
- `async testCrmConnection()`
- `async testWebhook()`

### ShippingReturns
**Path:** `src/views/ShippingReturns.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeTab`: 'shipping'
- `carriers`: [
      { name: 'FedEx', logo: 'https://via.placeholder.com/150x80?text=FedEx' },
      { name: 'UPS', logo: 'https://via.placeholder.com/150x80?text=UPS' },
      { name: 'USPS', logo: 'https://via.placeholder.com/150x80?text=USPS' },
      { name: 'DHL', logo: 'https://via.placeholder.com/150x80?text=DHL' },
      { name: 'XPO Logistics', logo: 'https://via.placeholder.com/150x80?text=XPO' },
      { name: 'Old Dominion', logo: 'https://via.placeholder.com/150x80?text=Old+Dominion' },
      { name: 'R+L Carriers', logo: 'https://via.placeholder.com/150x80?text=R%2BL' },
      { name: 'YRC Freight', logo: 'https://via.placeholder.com/150x80?text=YRC' }
    ]
- `commonQuestions`: [
      {
        question: 'How can I track my shipment?',
        answer: 'You can track your shipment in several ways:<br><br>1. Log into your Crown Nexus account and go to the "Orders" section<br>2. Click on the specific order to view tracking information<br>3. Click the tracking number to be redirected to the carrier\'s tracking page<br><br>You will also receive automated email updates with tracking information when your order ships and at key points during transit.'
      },
      {
        question: 'What if my shipment is damaged or items are missing?',
        answer: 'If you receive a damaged shipment or discover missing items:<br><br>1. Document the damage with photos before unpacking further<br>2. Note any damage on the delivery receipt when signing for the package<br>3. Contact our customer service team within 24 hours at 1-800-987-6543<br>4. Keep all original packaging materials until the claim is resolved<br><br>For missing items, please verify against the packing slip and contact customer service with the order number and details of the missing items.'
      },
      {
        question: 'Can I change my shipping address after placing an order?',
        answer: 'Address changes may be possible if the order has not yet been processed for shipping:<br><br>1. Log into your account and check your order status<br>2. If the status is "Processing" or earlier, contact customer service immediately<br>3. For orders already shipped, we cannot change the destination address<br>4. In some cases, we may be able to recall a package, but additional fees will apply<br><br>To avoid delivery issues, always verify your shipping address before completing your order.'
      },
      {
        question: 'What is your policy for partial shipments?',
        answer: 'Crown Nexus may split large orders into multiple shipments to ensure you receive available items as quickly as possible:<br><br>• You will not be charged extra shipping for partial shipments<br>• Each shipment will have its own tracking number<br>• You\'ll receive notification emails for each partial shipment<br>• Backordered items will ship as they become available<br><br>If you prefer to receive all items in a single shipment, please specify "Ship Complete" in the order notes during checkout or contact customer service.'
      },
      {
        question: 'How do I request a return for an incorrect item?',
        answer: 'If you received an incorrect item:<br><br>1. Contact customer service within 5 business days of receipt<br>2. Provide your order number and details about the incorrect item<br>3. We will issue an RMA and return shipping label at no cost to you<br>4. The correct item will be shipped as soon as possible<br>5. You are not responsible for restocking fees when we ship incorrect items<br><br>Please do not return items without an RMA number as this will delay processing and resolution.'
      }
    ]
- `customSolutions`: [
      {
        title: 'Dedicated Freight Program',
        subtitle: 'For high-volume customers with regular shipping needs',
        icon: 'truck-check'
      },
      {
        title: 'Cross-Dock Services',
        subtitle: 'Consolidate multiple shipments for more efficient delivery',
        icon: 'forklift'
      },
      {
        title: 'Just-In-Time Delivery',
        subtitle: 'Scheduled deliveries to support lean inventory management',
        icon: 'clock-time-five'
      },
      {
        title: 'Customized Packaging',
        subtitle: 'Special packaging solutions for unique product requirements',
        icon: 'package-variant'
      },
      {
        title: 'Managed Transportation',
        subtitle: 'Let our logistics team manage your entire shipping process',
        icon: 'truck-delivery'
      }
    ]
- `customsDocuments`: [
      {
        name: 'Commercial Invoice',
        description: 'Official document that details the sale transaction between seller and buyer, including item descriptions, quantities, and values.',
        requiredFor: 'All international shipments'
      },
      {
        name: 'Packing List',
        description: 'Detailed list of all items in the shipment, including quantities, weights, and dimensions.',
        requiredFor: 'All international shipments'
      },
      {
        name: 'Certificate of Origin',
        description: 'Document certifying the country where the goods were manufactured or produced.',
        requiredFor: 'Shipments to countries with preferential trade agreements'
      },
      {
        name: 'Shipper\'s Letter of Instruction',
        description: 'Detailed instructions from the shipper to the carrier about how to handle the shipment.',
        requiredFor: 'Most international shipments'
      },
      {
        name: 'Dangerous Goods Declaration',
        description: 'Document required for shipping hazardous materials, detailing the nature of the goods and safety precautions.',
        requiredFor: 'Shipments containing hazardous materials'
      },
      {
        name: 'Import License',
        description: 'Government-issued permit allowing the importation of specific goods into the destination country.',
        requiredFor: 'Certain restricted items in specific countries'
      }
    ]
- `expeditedOptions`: [
      {
        title: 'Same-Day Delivery',
        timing: 'Delivery within hours',
        color: 'error',
        icon: 'clock-fast',
        description: 'For critical parts needs, we offer same-day delivery service in select metro areas. Orders must be placed before 10 AM local time.',
        details: [
          { icon: 'mdi-map-marker', text: 'Available in major metro areas' },
          { icon: 'mdi-currency-usd', text: 'Premium pricing applies' },
          { icon: 'mdi-truck-fast', text: 'Direct courier delivery' },
          { icon: 'mdi-phone', text: 'Call for availability' }
        ]
      },
      {
        title: 'Next-Day Air',
        timing: 'Delivery by 10:30 AM next business day',
        color: 'warning',
        icon: 'airplane',
        description: 'Our premium overnight service guarantees delivery by 10:30 AM the next business day to most locations in the continental US.',
        details: [
          { icon: 'mdi-calendar-clock', text: 'Order by 4 PM EST for next-day delivery' },
          { icon: 'mdi-map', text: 'Available to most US locations' },
          { icon: 'mdi-truck-check', text: 'Full tracking and delivery confirmation' },
          { icon: 'mdi-account-check', text: 'Signature required on delivery' }
        ]
      }
    ]
- `freightGuidelines`: [
      'Orders over 150 lbs typically ship via freight',
      'Standard delivery is dock-to-dock',
      'Inside delivery available for additional fee',
      'Lift gate service available for locations without loading docks',
      'Freight shipments require a delivery appointment',
      'Inspection required at time of delivery'
    ]
- `internationalRegions`: [
      {
        name: 'North America',
        icon: 'earth',
        countries: ['Canada', 'Mexico']
      },
      {
        name: 'Latin America',
        icon: 'earth',
        countries: ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru', 'Panama']
      },
      {
        name: 'Europe',
        icon: 'earth',
        countries: ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands', 'Sweden']
      },
      {
        name: 'Asia Pacific',
        icon: 'earth',
        countries: ['Australia', 'Japan', 'South Korea', 'Singapore', 'Thailand', 'New Zealand']
      },
      {
        name: 'Middle East',
        icon: 'earth',
        countries: ['United Arab Emirates', 'Saudi Arabia', 'Qatar']
      },
      {
        name: 'Africa',
        icon: 'earth',
        countries: ['South Africa', 'Egypt', 'Morocco']
      }
    ]
- `internationalReturns`: [
      {
        title: 'International Return Process',
        description: 'Our international returns process is designed to make cross-border returns as smooth as possible:',
        points: [
          'Standard 30-day return window applies to international orders',
          'Return shipping costs are the responsibility of the customer unless the item is defective',
          'All returns require an RMA number before shipping',
          'Return shipping method should match or be slower than the original shipping method',
          'Customer is responsible for all duties and taxes on return shipments'
        ]
      },
      {
        title: 'Customs Documentation for Returns',
        description: 'Proper documentation is crucial for international returns to clear customs efficiently:',
        points: [
          'Mark packages as "Return of Goods" or "Warranty Return" as appropriate',
          'Include commercial invoice stating "No Commercial Value - Returned Goods"',
          'Reference the original order number and RMA number on all documents',
          'Include copy of original commercial invoice if available',
          'Declare actual value for customs purposes (even for warranty returns
- `internationalShippingMethods`: [
      {
        name: 'Economy International',
        delivery: '7-14 business days',
        bestFor: 'Non-urgent shipments and budget-conscious customers',
        tracking: true
      },
      {
        name: 'Standard International',
        delivery: '5-10 business days',
        bestFor: 'Regular international shipments with balanced cost and speed',
        tracking: true
      },
      {
        name: 'Expedited International',
        delivery: '3-5 business days',
        bestFor: 'Time-sensitive shipments needing faster delivery',
        tracking: true
      },
      {
        name: 'Priority International',
        delivery: '2-3 business days',
        bestFor: 'Urgent shipments requiring quick delivery',
        tracking: true
      },
      {
        name: 'International Air Freight',
        delivery: '5-7 business days',
        bestFor: 'Large volume shipments too heavy for standard service',
        tracking: true
      },
      {
        name: 'International Ocean Freight',
        delivery: '30-45 days',
        bestFor: 'Very large shipments where time is not critical',
        tracking: true
      }
    ]
- `ltlRequirements`: [
      'Proper packaging for freight handling',
      'Items must be palletized or crated',
      'Accurate dimensions and weight required',
      'Hazardous materials must be declared',
      'Commercial address with loading dock preferred',
      'Delivery contact information required'
    ]
- `orderProcessingSteps`: [
      {
        title: 'Order Placement',
        timing: 'Day 0',
        description: 'Order is submitted through website, EDI, or phone',
        color: 'primary'
      },
      {
        title: 'Order Verification',
        timing: 'Within 30 minutes',
        description: 'Order is checked for accuracy and availability',
        color: 'primary'
      },
      {
        title: 'Payment Processing',
        timing: 'Within 1 hour',
        description: 'Payment method is verified or terms are applied',
        color: 'primary'
      },
      {
        title: 'Picking & Packing',
        timing: 'Same day for orders before 2 PM',
        description: 'Items are picked from warehouse and packaged',
        color: 'secondary'
      },
      {
        title: 'Shipping',
        timing: 'Same day for orders before cutoff',
        description: 'Order is handed off to carrier with tracking',
        color: 'info'
      },
      {
        title: 'Delivery',
        timing: 'Based on shipping method',
        description: 'Carrier delivers to specified address',
        color: 'success'
      }
    ]
- `packagingPractices`: [
      {
        title: 'Multiple Box Sizes',
        icon: 'package-variant-closed',
        description: 'We use the appropriate box size for each order to minimize shipping costs and environmental impact while ensuring product protection.'
      },
      {
        title: 'Eco-Friendly Materials',
        icon: 'leaf',
        description: 'Whenever possible, we use recyclable and biodegradable packaging materials, including recycled cardboard and paper-based void fill.'
      },
      {
        title: 'Part-Specific Protection',
        icon: 'shield',
        description: 'Delicate parts receive additional protection with custom inserts, bubble wrap, or foam padding to prevent damage during transit.'
      },
      {
        title: 'Consolidation',
        icon: 'package-variant',
        description: 'Multiple items in a single order are consolidated whenever possible to reduce packaging materials and shipping costs.'
      }
    ]
- `returnPolicies`: [
      {
        title: 'Standard Returns',
        description: 'Our standard return policy for most products:',
        points: [
          '30-day return window from delivery date',
          'Items must be in original condition and packaging',
          'Return shipping paid by customer for non-defective items',
          'Restocking fee may apply (typically 15%
- `returnsProcess`: [
      {
        title: 'Request Return Authorization',
        description: 'Submit a return request through your account dashboard or by contacting customer service with your order number and reason for return.',
        icon: 'file-document-edit',
        color: 'primary'
      },
      {
        title: 'Receive RMA and Instructions',
        description: 'Once approved, you\'ll receive a Return Merchandise Authorization (RMA
- `returnsResources`: [
      {
        title: 'Returns Portal',
        icon: 'laptop',
        description: 'Manage all your returns online through our self-service returns portal. Request RMAs, print shipping labels, and track return status.',
        link: '/account/returns',
        buttonText: 'Access Portal',
        image: 'https://via.placeholder.com/400x200?text=Returns+Portal'
      },
      {
        title: 'RMA Generator',
        icon: 'note-text',
        description: 'Quickly generate return merchandise authorizations for multiple items or orders with our easy-to-use RMA tool.',
        link: '/tools/rma-generator',
        buttonText: 'Generate RMA',
        image: 'https://via.placeholder.com/400x200?text=RMA+Generator'
      },
      {
        title: 'Returns Guide',
        icon: 'book-open-variant',
        description: 'Download our comprehensive returns guide with step-by-step instructions, packaging requirements, and tips for efficient returns processing.',
        link: '/resources/returns-guide',
        buttonText: 'Download Guide',
        image: 'https://via.placeholder.com/400x200?text=Returns+Guide'
      }
    ]
- `shippingMethods`: [
      {
        name: 'Standard Ground',
        delivery: '3-5 business days',
        availability: 'Continental US & Canada',
        bestFor: 'Regular restocking orders'
      },
      {
        name: 'Expedited Ground',
        delivery: '2-3 business days',
        availability: 'Continental US & Canada',
        bestFor: 'Time-sensitive orders'
      },
      {
        name: 'Priority Overnight',
        delivery: 'Next business day',
        availability: 'Continental US & Canada',
        bestFor: 'Emergency parts needs'
      },
      {
        name: 'LTL Freight',
        delivery: '3-7 business days',
        availability: 'Continental US & Canada',
        bestFor: 'Large or heavy shipments'
      },
      {
        name: 'Will Call',
        delivery: 'Same day pickup',
        availability: 'Distribution center locations',
        bestFor: 'Local customers needing immediate parts'
      }
    ]
- `shippingPolicies`: [
      {
        title: 'Order Processing Times',
        content: 'Crown Nexus processes orders according to the following schedule:<br><br>• Orders received before 2 PM EST on business days are processed the same day<br>• Orders received after 2 PM EST are processed the next business day<br>• Processing time does not include weekends or holidays<br><br>Orders are processed in the sequence they are received, with priority given to emergency orders and expedited shipping requests.'
      },
      {
        title: 'Shipping Cutoff Times',
        content: 'To ensure your order ships on the same day, please place your order before these cutoff times:',
        bulletPoints: [
          'Standard Ground: 2 PM EST',
          'Expedited Ground: 2 PM EST',
          'Priority Overnight: 3 PM EST (may vary by location
- `shippingTools`: [
      {
        name: 'Shipping Rate Calculator',
        description: 'Calculate shipping costs based on weight, dimensions, and destination',
        icon: 'calculator',
        link: '/tools/shipping-calculator'
      },
      {
        name: 'Transit Time Estimator',
        description: 'Get estimated delivery times for any shipping method to your location',
        icon: 'clock-outline',
        link: '/tools/transit-estimator'
      },
      {
        name: 'Order Tracking Portal',
        description: 'Track all your shipments in one place with real-time updates',
        icon: 'map-marker-path',
        link: '/account/order-tracking'
      },
      {
        name: 'Shipping Documentation Generator',
        description: 'Generate shipping labels, packing slips, and customs forms',
        icon: 'file-document-outline',
        link: '/tools/documentation'
      }
    ]
- `warrantyInformation`: [
      {
        title: 'Manufacturer Warranties',
        description: 'All products sold through Crown Nexus come with the original manufacturer warranty. Warranty terms vary by manufacturer and product category.',
        coverage: [
          { category: 'Brake Components', standard: '12 months / 12,000 miles', extended: '24 months / 24,000 miles' },
          { category: 'Engine Parts', standard: '12 months / 12,000 miles', extended: '36 months / 36,000 miles' },
          { category: 'Suspension Components', standard: '24 months / 24,000 miles', extended: 'Lifetime (limited

### TermsOfService
**Path:** `src/views/TermsOfService.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `sections`: [
      {
        id: 'acceptance',
        title: '1. Acceptance of Terms',
        content: `
          <p>These Terms of Service ("Terms"

#### Methods
- `printTerms()`
- `scrollToSection()`

### Testimonials
**Path:** `src/views/Testimonials.vue`
**Type:** Composition API (script setup)

#### Reactive State
**Refs:**
- `industryOptions`: [
  'Auto Repair Shop',
  'Parts Retailer',
  'Distributor',
  'Dealership',
  'Fleet Service',
  'Performance Shop'
]
- `itemsPerPage`: 9
- `loading`: true
- `page`: 1
- `ratingOptions`: [
  { title: '5 Stars', value: 5 },
  { title: '4+ Stars', value: 4 },
  { title: '3+ Stars', value: 3 }
]
- `totalItems`: 0

#### Computed Properties
- `isAdmin`

#### Methods
- `async fetchTestimonials()`
- `filterTestimonials()`
- `resetFilters()`

#### Lifecycle Hooks
- `mounted`

### Unauthorized
**Path:** `src/views/Unauthorized.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `errorMessage`: ''
- `showContactDialog`: false

#### Computed Properties
- `isLoggedIn`

#### Methods
- `goBack()`

### UserDetail
**Path:** `src/views/UserDetail.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activityLoading`: false
- `activityPage`: 1
- `activityPageSize`: 10
- `deleteDialog`: false
- `deleteLoading`: false
- `hasMoreActivity`: false
- `impersonateDialog`: false
- `impersonateLoading`: false
- `loading`: true
- `resetDialog`: false
- `resetLoading`: false
- `statusDialog`: false
- `statusLoading`: false

#### Computed Properties
- `userId`

#### Methods
- `confirmDelete()`
- `confirmImpersonateUser()`
- `confirmPasswordReset()`
- `confirmToggleStatus()`
- `async deleteUser()`
- `async fetchActivityLog()`
- `async fetchUser()`
- `async impersonateUser()`
- `loadMoreActivity()`
- `refreshActivityLog()`
- `async sendPasswordReset()`
- `async toggleUserStatus()`

### UserForm
**Path:** `src/views/UserForm.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `confirmPassword`: ''
- `formDirty`: false
- `formError`: ''
- `initialLoading`: false
- `isFormValid`: false
- `loading`: false
- `showPassword`: false
- `showPasswordFields`: false
- `showUnsavedDialog`: false

#### Computed Properties
- `currentUser`
- `passwordRules`

#### Methods
- `clearError()`
- `discardChanges()`
- `async fetchCompanies()`
- `async fetchUser()`
- `navigationGuard()`
- `async submitForm()`

### UserManagement
**Path:** `src/views/UserManagement.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `deleteDialog`: false
- `deleteLoading`: false
- `itemsPerPage`: 10
- `loading`: false
- `page`: 1
- `search`: ''
- `totalItems`: 0
- `totalPages`: 1

#### Computed Properties
- `currentUserId`

#### Methods
- `confirmDelete()`
- `async deleteUser()`
- `async fetchUsers()`
- `resetFilters()`

### UserProfile
**Path:** `src/views/UserProfile.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `apiKeyForm`: {
      name: '',
      expiration: '90d'
    }
- `apiKeyLoading`: false
- `disableTwoFactorPassword`: ''
- `editingProfile`: false
- `isApiKeyFormValid`: false
- `isPasswordFormValid`: false
- `isProfileFormValid`: false
- `loading`: true
- `newApiKey`: ''
- `passwordForm`: {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
- `passwordFormError`: ''
- `passwordLastChanged`: new Date(Date.now(
- `preferences`: {
      theme: 'light' as 'light' | 'dark' | 'system',
      language: 'en',
      timezone: 'America/New_York',
      notifications_enabled: true,
      dashboard_widgets: ['recent_activity', 'product_stats', 'quick_actions']
    }
- `profileForm`: {
      full_name: '',
      email: ''
    }
- `profileFormError`: ''
- `revokeKeyLoading`: false
- `showActivityDialog`: false
- `showApiKeyDialog`: false
- `showCurrentPassword`: false
- `showNewPassword`: false
- `showRevokeKeyDialog`: false
- `showTwoFactorDialog`: false
- `twoFactorCode`: ''
- `twoFactorEnabled`: false
- `twoFactorLoading`: false
- `updatingPassword`: false
- `updatingPreferences`: false
- `updatingProfile`: false

#### Methods
- `cancelApiKeyDialog()`
- `cancelEditingProfile()`
- `async changePassword()`
- `clearPasswordError()`
- `clearProfileError()`
- `confirmRevokeKey()`
- `copyApiKey()`
- `async disableTwoFactor()`
- `async enableTwoFactor()`
- `async generateApiKey()`
- `async revokeApiKey()`
- `startEditingProfile()`
- `async updatePreferences()`
- `async updateProfile()`

## TypeScript Types
### api
**Path:** `src/services/api.ts`

#### Interface: `ApiError`
| Property | Type |
| -------- | ---- |
| detail | string |
| status | number |
| title | string |
| type | string |

### auth
**Path:** `src/stores/auth.ts`

#### Interface: `AuthState`
| Property | Type |
| -------- | ---- |
| error | string | null |
| isAuthenticated | boolean |
| loading | boolean |
| token | string | null |
| tokenExpiration | number | null |
| user | User | null |

#### Interface: `LoginCredentials`
| Property | Type |
| -------- | ---- |
| password | string |
| rememberMe | boolean |
| username | string |

#### Interface: `LoginResponse`
| Property | Type |
| -------- | ---- |
| access_token | string |
| token_type | string |

#### Interface: `TokenPayload`
| Property | Type |
| -------- | ---- |
| exp | number |
| role | UserRole |
| sub | string |

### chat
**Path:** `src/types/chat.ts`

#### Interface: `ChatMember`
| Property | Type |
| -------- | ---- |
| is_online | boolean |
| last_read_at | string | null |
| role | ChatMemberRole |
| user_id | string |
| user_name | string |

#### Enum: `ChatMemberRole`
| Property | Type |
| -------- | ---- |
| ADMIN | 'admin' |
| GUEST | 'guest' |
| MEMBER | 'member' |
| OWNER | 'owner' |

#### Interface: `ChatMessage`
| Property | Type |
| -------- | ---- |
| content | string |
| created_at | string |
| id | string |
| is_deleted | boolean |
| is_edited | boolean |
| message_type | MessageType |
| metadata | Record<string, any> |
| reactions | Record<string, string[]> |
| room_id | string |
| sender_id | string | null |
| sender_name | string | null |
| updated_at | string |

#### Interface: `ChatNotification`
| Property | Type |
| -------- | ---- |
| content | string |
| created_at | string |
| id | string |
| is_read | boolean |
| message_id | string |
| room_id | string |
| type | string |

#### Interface: `ChatRoom`
| Property | Type |
| -------- | ---- |
| company_id | string | null |
| created_at | string |
| id | string |
| last_message | ChatMessage | null |
| member_count | number |
| metadata | Record<string, any> |
| name | string | null |
| type | ChatRoomType |
| unread_count | number |
| user_role | ChatMemberRole |

#### Enum: `ChatRoomType`
| Property | Type |
| -------- | ---- |
| COMPANY | 'company' |
| DIRECT | 'direct' |
| GROUP | 'group' |
| SUPPORT | 'support' |

#### Interface: `ChatServiceState`
| Property | Type |
| -------- | ---- |
| activeRoom | ChatRoom | null |
| activeRoomId | string | null |
| activeRoomMembers | ChatMember[] |
| activeRoomMessages | ChatMessage[] |
| chatRooms | Record<string, ChatRoom> |
| typingUsers | Record<string, TypingIndicator[]> |

#### Enum: `MessageType`
| Property | Type |
| -------- | ---- |
| ACTION | 'action' |
| FILE | 'file' |
| IMAGE | 'image' |
| SYSTEM | 'system' |
| TEXT | 'text' |

#### Interface: `TypingIndicator`
| Property | Type |
| -------- | ---- |
| room_id | string |
| timestamp | number |
| user_id | string |
| user_name | string |

#### Interface: `UserPresence`
| Property | Type |
| -------- | ---- |
| is_online | boolean |
| last_seen_at | string | null |
| status | string | null |
| user_id | string |

#### Interface: `WebSocketCommand`
| Property | Type |
| -------- | ---- |
| command | string |
| data | Record<string, any> |
| room_id | string |

#### Interface: `WebSocketResponse`
| Property | Type |
| -------- | ---- |
| data | Record<string, any> |
| error | string |
| success | boolean |
| type | string |

### error-handler
**Path:** `src/utils/error-handler.ts`

#### Interface: `ErrorInfo`
| Property | Type |
| -------- | ---- |
| code | string |
| details | string | Record<string, any> |
| field | string |
| message | string |
| severity | ErrorSeverity |

#### Enum: `ErrorSeverity`
| Property | Type |
| -------- | ---- |
| CRITICAL | 'critical' |
| ERROR | 'error' |
| INFO | 'info' |
| WARNING | 'warning' |

### fitment
**Path:** `src/types/fitment.ts`

#### Interface: `Fitment`
| Property | Type |
| -------- | ---- |
| attributes | Record<string, any> |
| created_at | string |
| engine | string |
| id | string |
| make | string |
| model | string |
| transmission | string |
| updated_at | string |
| year | number |

#### Interface: `FitmentFilters`
| Property | Type |
| -------- | ---- |
| attributes | Record<string, any> |
| engine | string |
| make | string |
| model | string |
| page | number |
| page_size | number |
| transmission | string |
| year | number |

#### Interface: `FitmentListResponse`
| Property | Type |
| -------- | ---- |
| items | Fitment[] |
| page | number |
| page_size | number |
| pages | number |
| total | number |

### fitmentProcessing
**Path:** `src/services/fitmentProcessing.ts`

#### Interface: `FitmentValidationResult`
| Property | Type |
| -------- | ---- |
| attributes | Record<string, any> |
| engine | string |
| fitment | {
    vehicle: {
      year: number |
| make | string |
| message | string |
| model | string |
| original_text | string |
| status | string |
| submodel | string |
| suggestions | string[] |
| transmission | string |

#### Interface: `ProcessFitmentResponse`
| Property | Type |
| -------- | ---- |
| error_count | number |
| results | Record<string, FitmentValidationResult[]> |
| valid_count | number |
| warning_count | number |

### index
**Path:** `src/router/index.ts`

#### Interface: `RouteMeta`
| Property | Type |
| -------- | ---- |
| layout | string |
| requiresAdmin | boolean |
| requiresAuth | boolean |
| title | string |

### media
**Path:** `src/types/media.ts`

#### Interface: `Media`
| Property | Type |
| -------- | ---- |
| alt_text | string |
| created_at | string |
| description | string |
| filename | string |
| id | string |
| media_type | string |
| mime_type | string |
| product | any |
| size | number |
| thumbnail_url | string |
| updated_at | string |
| url | string |

### modelMapping
**Path:** `src/services/modelMapping.ts`

#### Interface: `ModelMapping`
| Property | Type |
| -------- | ---- |
| active | boolean |
| created_at | string |
| id | number |
| mapping | string |
| pattern | string |
| priority | number |
| updated_at | string |

#### Interface: `ModelMappingListResponse`
| Property | Type |
| -------- | ---- |
| items | ModelMapping[] |
| total | number |

#### Interface: `ModelMappingRequest`
| Property | Type |
| -------- | ---- |
| active | boolean |
| mapping | string |
| pattern | string |
| priority | number |

### notification
**Path:** `src/utils/notification.ts`

#### Interface: `Notification`
| Property | Type |
| -------- | ---- |
| closeable | boolean |
| id | number |
| message | string |
| position | 'top' | 'bottom' |
| timeout | number |
| type | NotificationType |

#### Enum: `NotificationType`
| Property | Type |
| -------- | ---- |
| ERROR | 'error' |
| INFO | 'info' |
| SUCCESS | 'success' |
| WARNING | 'warning' |

### product
**Path:** `src/types/product.ts`

#### Interface: `Brand`
| Property | Type |
| -------- | ---- |
| created_at | string |
| id | string |
| name | string |
| parent_company | any |
| parent_company_id | string |

#### Interface: `BrandCreateDTO`
| Property | Type |
| -------- | ---- |
| name | string |
| parent_company_id | string |

#### Interface: `BrandUpdateDTO`
| Property | Type |
| -------- | ---- |
| name | string |
| parent_company_id | string | null |

#### Enum: `DescriptionType`
| Property | Type |
| -------- | ---- |
| KEYWORDS | "Keywords" |
| LONG | "Long" |
| NOTES | "Notes" |
| SHORT | "Short" |
| SLANG | "Slang" |

#### Enum: `MarketingType`
| Property | Type |
| -------- | ---- |
| AD_COPY | "Ad Copy" |
| BULLET_POINT | "Bullet Point" |

#### Interface: `Product`
| Property | Type |
| -------- | ---- |
| activities | ProductActivity[] |
| application | string |
| created_at | string |
| descriptions | ProductDescription[] |
| id | string |
| is_active | boolean |
| late_model | boolean |
| marketing | ProductMarketing[] |
| measurements | ProductMeasurement[] |
| part_number | string |
| part_number_stripped | string |
| soft | boolean |
| stock | ProductStock[] |
| superseded_by | ProductSupersession[] |
| supersedes | ProductSupersession[] |
| universal | boolean |
| updated_at | string |
| vintage | boolean |

#### Interface: `ProductActivity`
| Property | Type |
| -------- | ---- |
| changed_at | string |
| changed_by | any |
| changed_by_id | string |
| id | string |
| product_id | string |
| reason | string |
| status | ProductStatus |

#### Interface: `ProductCreateDTO`
| Property | Type |
| -------- | ---- |
| application | string |
| descriptions | ProductDescriptionCreateDTO[] |
| is_active | boolean |
| late_model | boolean |
| marketing | ProductMarketingCreateDTO[] |
| part_number | string |
| part_number_stripped | string |
| soft | boolean |
| universal | boolean |
| vintage | boolean |

#### Interface: `ProductDescription`
| Property | Type |
| -------- | ---- |
| created_at | string |
| description | string |
| description_type | DescriptionType |
| id | string |
| product_id | string |

#### Interface: `ProductDescriptionCreateDTO`
| Property | Type |
| -------- | ---- |
| description | string |
| description_type | DescriptionType |

#### Interface: `ProductDescriptionUpdateDTO`
| Property | Type |
| -------- | ---- |
| description | string |
| description_type | DescriptionType |

#### Interface: `ProductFilters`
| Property | Type |
| -------- | ---- |
| is_active | boolean |
| late_model | boolean |
| page | number |
| page_size | number |
| search | string |
| soft | boolean |
| universal | boolean |
| vintage | boolean |

#### Interface: `ProductListResponse`
| Property | Type |
| -------- | ---- |
| items | Product[] |
| page | number |
| page_size | number |
| pages | number |
| total | number |

#### Interface: `ProductMarketing`
| Property | Type |
| -------- | ---- |
| content | string |
| created_at | string |
| id | string |
| marketing_type | MarketingType |
| position | number |
| product_id | string |

#### Interface: `ProductMarketingCreateDTO`
| Property | Type |
| -------- | ---- |
| content | string |
| marketing_type | MarketingType |
| position | number |

#### Interface: `ProductMarketingUpdateDTO`
| Property | Type |
| -------- | ---- |
| content | string |
| marketing_type | MarketingType |
| position | number |

#### Interface: `ProductMeasurement`
| Property | Type |
| -------- | ---- |
| dimensional_weight | number |
| effective_date | string |
| height | number |
| id | string |
| length | number |
| manufacturer | any |
| manufacturer_id | string |
| product_id | string |
| volume | number |
| weight | number |
| width | number |

#### Interface: `ProductMeasurementCreateDTO`
| Property | Type |
| -------- | ---- |
| dimensional_weight | number |
| height | number |
| length | number |
| manufacturer_id | string |
| volume | number |
| weight | number |
| width | number |

#### Enum: `ProductStatus`
| Property | Type |
| -------- | ---- |
| ACTIVE | "active" |
| DISCONTINUED | "discontinued" |
| INACTIVE | "inactive" |
| OUT_OF_STOCK | "out_of_stock" |
| PENDING | "pending" |

#### Interface: `ProductStock`
| Property | Type |
| -------- | ---- |
| id | string |
| last_updated | string |
| product_id | string |
| quantity | number |
| warehouse | any |
| warehouse_id | string |

#### Interface: `ProductStockCreateDTO`
| Property | Type |
| -------- | ---- |
| quantity | number |
| warehouse_id | string |

#### Interface: `ProductStockUpdateDTO`
| Property | Type |
| -------- | ---- |
| quantity | number |

#### Interface: `ProductSupersession`
| Property | Type |
| -------- | ---- |
| changed_at | string |
| id | string |
| new_product | any |
| new_product_id | string |
| old_product | any |
| old_product_id | string |
| reason | string |

#### Interface: `ProductSupersessionCreateDTO`
| Property | Type |
| -------- | ---- |
| new_product_id | string |
| old_product_id | string |
| reason | string |

#### Interface: `ProductUpdateDTO`
| Property | Type |
| -------- | ---- |
| application | string |
| is_active | boolean |
| late_model | boolean |
| part_number | string |
| soft | boolean |
| universal | boolean |
| vintage | boolean |

### user
**Path:** `src/types/user.ts`

#### Interface: `User`
| Property | Type |
| -------- | ---- |
| account_number | string |
| account_type | string |
| company | {
    id: string |
| created_at | string |
| email | string |
| full_name | string |
| id | string |
| is_active | boolean |
| is_admin | boolean |
| name | string |
| role | UserRole |
| updated_at | string |

#### Enum: `UserRole`
| Property | Type |
| -------- | ---- |
| ADMIN | 'admin' |
| CLIENT | 'client' |
| DISTRIBUTOR | 'distributor' |
| MANAGER | 'manager' |
| READ_ONLY | 'read_only' |

## Utility Functions
### api
**Path:** `src/services/api.ts`

#### Function: `handleApiError(error: any) → void`

### auth
**Path:** `src/stores/auth.ts`

#### Function: `getTokenExpiration(token: string | null) → number | null`

### error-handler
**Path:** `src/utils/error-handler.ts`

#### Function: `createErrorInfo(error: any, defaultMessage: string = 'An error occurred') → ErrorInfo`

#### Function: `getErrorMessage(error: any) → string`

#### Function: `isAxiosError(error: any) → error is AxiosError`

#### Function: `parseValidationErrors(error: any) → Record<string, string>`

### formatters
**Path:** `src/utils/formatters.ts`

#### Function: `formatCurrency(amount: number, currency: string = 'USD', locale: string = 'en-US') → string`

#### Function: `formatDate(dateInput: string | Date | number, format: 'short' | 'medium' | 'long' | 'full' = 'medium') → string`

#### Function: `formatDateTime(dateInput: string | Date | number, format: 'short' | 'medium' | 'long' | 'full' = 'medium') → string`

#### Function: `formatFileSize(bytes: number, decimals: number = 2) → string`

#### Function: `formatNumber(num: number, decimals: number = 0) → string`

#### Function: `toTitleCase(text: string) → string`

#### Function: `truncateText(text: string, maxLength: number = 50) → string`

### notification
**Path:** `src/utils/notification.ts`

#### Function: `createNotification(type: NotificationType, message: string, timeout: number = DEFAULT_TIMEOUT, closeable: boolean = true, position: 'top' | 'bottom' = DEFAULT_POSITION) → number`

#### Function: `error(message: string, timeout?: number) → number`

#### Function: `getNotifications() → Notification[]`

#### Function: `info(message: string, timeout?: number) → number`

#### Function: `removeNotification(id: number) → void`

#### Function: `success(message: string, timeout?: number) → number`

#### Function: `warning(message: string, timeout?: number) → number`
