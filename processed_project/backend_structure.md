# backend Project Structure
Generated on 2025-03-16 13:13:05

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
│   │   └── deps.py
│   ├── chat/
│   │   ├── connection.py
│   │   ├── service.py
│   │   └── websocket.py
│   ├── commands/
│   │   ├── __init__.py
│   │   └── init_currencies.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── celeryconfig.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── base_class.py
│   │   └── session.py
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
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── currency.py
│   │   ├── media.py
│   │   ├── model_mapping.py
│   │   ├── product.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── currency_service.py
│   │   ├── media_service.py
│   │   ├── search.py
│   │   └── vehicle.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── chat_tasks.py
│   │   └── currency_tasks.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── crypto.py
│   │   ├── db.py
│   │   ├── file.py
│   │   └── redis_manager.py
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
│   ├── __init__.py
│   ├── conftest.py
│   └── utils.py
├── README.md
├── alembic.ini
├── backend.iml
├── pyproject.toml
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
*FastAPI application entry point.*
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
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.api.deps import get_current_user
from app.api.v1.router import api_router
from app.core.config import Environment, settings
from app.core.logging import setup_logging, get_logger, request_context, set_user_id
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
media_path =     media_path = Path(settings.MEDIA_ROOT).resolve()
host = '0.0.0.0'
port = 8000
```

**Functions:**
```python
@app.get('/health')
async def health_check() -> dict:
    """
    Health check endpoint.

    This endpoint allows monitoring systems to check if the application..."""
```

```python
@asynccontextmanager
async def lifespan(app) -> AsyncGenerator[(None, None)]:
    """
    FastAPI lifespan event handler.

    This context manager handles application startup and shutd..."""
```

```python
async def log_current_user(current_user) -> Optional[User]:
    """
    Log the current user ID in the request context.
    
    Args:
        current_user: Current au..."""
```

**Classes:**
```python
class RequestContextMiddleware(object):
    """
    Middleware that sets up logging request context.
    
    This middleware ensures each request ..."""
```
*Methods:*
```python
    async def __call__(self, request, call_next) -> Response:
        """
        Process the request and set up logging context.
        
        Args:
            request:..."""
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
*API dependency providers.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/deps.py`

**Imports:**
```python
from __future__ import annotations
from datetime import datetime
from typing import Annotated, Dict, Optional, Union
from fastapi import Depends, HTTPException, Query, WebSocket, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect
from app.core.config import settings
from app.core.logging import get_logger, set_user_id
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import TokenPayload
```

**Global Variables:**
```python
logger = logger = get_logger("app.api.deps")
oauth2_scheme = oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)
PaginationParams = PaginationParams = Dict[str, Union[int, float]]
```

**Functions:**
```python
async def get_admin_user(current_user) -> User:
    """
    Get the current active admin user.

    This dependency builds on get_current_active_user and e..."""
```

```python
async def get_current_active_user(current_user) -> User:
    """
    Get the current active user.

    This dependency builds on get_current_user and ensures the us..."""
```

```python
async def get_current_user(db, token) -> User:
    """
    Get the current authenticated user.

    This dependency validates the JWT token, decodes it, a..."""
```

```python
async def get_current_user_ws(websocket, db) -> User:
    """
    Get the current authenticated user from WebSocket connection.
    
    This dependency extracts..."""
```

```python
async def get_manager_user(current_user) -> User:
    """
    Get the current active manager or admin user.

    This dependency builds on get_current_active..."""
```

```python
async def get_optional_user(db, token) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise None.

    This dependency is useful for endpo..."""
```

```python
def get_pagination(page, page_size) -> PaginationParams:
    """
    Get pagination parameters.

    This dependency generates pagination parameters based on page n..."""
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
    """
    OAuth2 compatible token login endpoint.

    This endpoint authenticates a user and provides a ..."""
```

```python
@router.get('/me', response_model=UserSchema)
async def read_users_me(current_user) -> Any:
    """
    Get current user information.

    This endpoint returns information about the currently
    au..."""
```

```python
@router.get('/validate-token')
async def validate_token(token) -> dict:
    """
    Validate a JWT token.

    This endpoint verifies if a token is valid and active.
    It's usef..."""
```

####### Module: chat
*Chat system REST API endpoints.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/api/v1/endpoints/chat.py`

**Imports:**
```python
from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, validator
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.chat.schemas import ChatRoomSchema, ChatMessageSchema, ChatMemberSchema
from app.chat.service import ChatService
from app.db.session import get_db_context
from app.models.chat import ChatRoom, ChatMember, ChatMemberRole, ChatRoomType
from app.models.user import User
```

**Global Variables:**
```python
router = router = APIRouter()
logger = logger = logging.getLogger(__name__)
```

**Functions:**
```python
@router.post('/rooms/{room_id}/members')
async def add_room_member(room_id, request, db, current_user) -> Dict[(str, Any)]:
    """
    Add a member to a room.
    
    Args:
        room_id: Room ID
        request: Member additio..."""
```

```python
@router.post('/direct-chats')
async def create_direct_chat(request, db, current_user) -> Dict[(str, Any)]:
    """
    Create or get a direct chat with another user.
    
    Args:
        request: Direct chat crea..."""
```

```python
@router.post('/rooms', status_code=status.HTTP_201_CREATED)
async def create_room(request, db, current_user) -> Dict[(str, Any)]:
    """
    Create a new chat room.
    
    Args:
        request: Room creation request
        db: Datab..."""
```

```python
@router.get('/rooms/{room_id}')
async def get_room(room_id, db, current_user) -> Dict[(str, Any)]:
    """
    Get information about a specific room.
    
    Args:
        room_id: Room ID
        db: Data..."""
```

```python
@router.get('/rooms/{room_id}/messages')
async def get_room_messages(room_id, before_id, limit, db, current_user) -> Dict[(str, Any)]:
    """
    Get messages from a room.
    
    Args:
        room_id: Room ID
        before_id: Get messag..."""
```

```python
@router.get('/rooms')
async def get_rooms(db, current_user) -> Dict[(str, Any)]:
    """
    Get all rooms for the current user.
    
    Args:
        db: Database session
        current..."""
```

```python
@router.delete('/rooms/{room_id}/members/{user_id}')
async def remove_room_member(room_id, user_id, db, current_user) -> Dict[(str, Any)]:
    """
    Remove a member from a room.
    
    Args:
        room_id: Room ID
        user_id: User ID
 ..."""
```

```python
@router.put('/rooms/{room_id}/members/{user_id}')
async def update_room_member(room_id, user_id, request, db, current_user) -> Dict[(str, Any)]:
    """
    Update a member's role in a room.
    
    Args:
        room_id: Room ID
        user_id: User..."""
```

**Classes:**
```python
class AddMemberRequest(BaseModel):
    """Request model for adding a member to a room."""
```
*Methods:*
```python
@validator('role')
    def validate_role(cls, v) -> str:
        """Validate member role."""
```

```python
class CreateDirectChatRequest(BaseModel):
    """Request model for creating a direct chat."""
```

```python
class CreateRoomRequest(BaseModel):
    """Request model for creating a room."""
```
*Methods:*
```python
@validator('type')
    def validate_type(cls, v) -> str:
        """Validate room type."""
```

```python
class UpdateMemberRequest(BaseModel):
    """Request model for updating a member in a room."""
```
*Methods:*
```python
@validator('role')
    def validate_role(cls, v) -> str:
        """Validate member role."""
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
    """
    Convert an amount between currencies.

    Args:
        conversion: Conversion request paramet..."""
```

```python
@router.get('/', response_model=List[CurrencyRead])
async def read_currencies(db, current_user, active_only) -> Any:
    """
    Get list of available currencies.

    Args:
        db: Database session
        current_user:..."""
```

```python
@router.get('/rates', response_model=List[ExchangeRateRead])
async def read_exchange_rates(db, current_user, source_code, target_code, limit) -> Any:
    """
    Get exchange rates with optional filtering.

    Args:
        db: Database session
        cur..."""
```

```python
@router.post('/update', status_code=status.HTTP_202_ACCEPTED)
async def trigger_exchange_rate_update(background_tasks, db, current_user, async_update) -> Dict[(str, Any)]:
    """
    Trigger an update of exchange rates.

    Args:
        background_tasks: Background tasks
    ..."""
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
    """
    Associate a product with a fitment.

    Args:
        fitment_id: Fitment ID
        product_i..."""
```

```python
@router.post('/', response_model=FitmentSchema, status_code=status.HTTP_201_CREATED)
async def create_fitment(db, fitment_in, current_user) -> Any:
    """
    Create new fitment.

    Args:
        db: Database session
        fitment_in: Fitment data
  ..."""
```

```python
@router.delete('/{fitment_id}')
async def delete_fitment(fitment_id, db, current_user) -> dict:
    """
    Delete a fitment.

    Args:
        fitment_id: Fitment ID
        db: Database session
      ..."""
```

```python
@router.get('/{fitment_id}', response_model=FitmentSchema)
async def read_fitment(fitment_id, db, current_user) -> Any:
    """
    Get fitment by ID.

    Args:
        fitment_id: Fitment ID
        db: Database session
     ..."""
```

```python
@router.get('/{fitment_id}/products', response_model=List[ProductSchema])
async def read_fitment_products(fitment_id, db, current_user, skip, limit) -> Any:
    """
    Get products associated with a fitment.

    Args:
        fitment_id: Fitment ID
        db: D..."""
```

```python
@router.get('/', response_model=FitmentListResponse)
async def read_fitments(db, current_user, year, make, model, engine, transmission, page, page_size) -> Any:
    """
    Retrieve fitments with filtering options.

    Args:
        db: Database session
        curre..."""
```

```python
@router.delete('/{fitment_id}/products/{product_id}')
async def remove_product_from_fitment(fitment_id, product_id, db, current_user) -> dict:
    """
    Remove association between a product and a fitment.

    Args:
        fitment_id: Fitment ID
 ..."""
```

```python
@router.put('/{fitment_id}', response_model=FitmentSchema)
async def update_fitment(fitment_id, fitment_in, db, current_user) -> Any:
    """
    Update a fitment.

    Args:
        fitment_id: Fitment ID
        fitment_in: Updated fitment..."""
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
    """
    Get the current locale based on the request.
    
    Args:
        locale: Current locale from..."""
```

```python
@router.get('/messages/{locale}')
async def get_messages(locale) -> Dict[(str, Dict[(str, str)])]:
    """
    Get all translation messages for a specific locale.
    
    Args:
        locale: Locale code ..."""
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
    """
    Associate media with a product.

    Args:
        media_id: Media ID
        product_id: Produ..."""
```

```python
@router.delete('/{media_id}')
async def delete_media(media_id, db, current_user) -> dict:
    """
    Delete media.

    Args:
        media_id: Media ID
        db: Database session
        curren..."""
```

```python
@router.get('/file/{media_id}')
async def get_media_file(media_id, db, current_user) -> Any:
    """
    Get the file for media.

    Args:
        media_id: Media ID
        db: Database session
    ..."""
```

```python
@router.get('/thumbnail/{media_id}')
async def get_media_thumbnail(media_id, db, current_user) -> Any:
    """
    Get the thumbnail for an image.

    Args:
        media_id: Media ID
        db: Database sess..."""
```

```python
@router.get('/products/{product_id}', response_model=List[MediaSchema])
async def get_product_media(product_id, db, current_user, media_type) -> Any:
    """
    Get media associated with a product.

    Args:
        product_id: Product ID
        db: Data..."""
```

```python
@router.get('/', response_model=MediaListResponse)
async def read_media(db, current_user, media_type, visibility, is_approved, product_id, page, page_size) -> Any:
    """
    Retrieve media with filtering options.

    Args:
        db: Database session
        current_..."""
```

```python
@router.get('/{media_id}', response_model=MediaSchema)
async def read_media_item(media_id, db, current_user) -> Any:
    """
    Get media by ID.

    Args:
        media_id: Media ID
        db: Database session
        cur..."""
```

```python
@router.delete('/{media_id}/products/{product_id}')
async def remove_media_from_product(media_id, product_id, db, current_user) -> dict:
    """
    Remove association between media and a product.

    Args:
        media_id: Media ID
        p..."""
```

```python
@router.put('/{media_id}', response_model=MediaSchema)
async def update_media(media_id, media_in, db, current_user) -> Any:
    """
    Update media metadata.

    Args:
        media_id: Media ID
        media_in: Updated media da..."""
```

```python
@router.post('/upload', response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(background_tasks, db, current_user, file, media_type, visibility, metadata, product_id) -> Any:
    """
    Upload a new file.

    Args:
        background_tasks: Background tasks
        db: Database s..."""
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
    """
    Create new brand.

    Args:
        db: Database session
        brand_in: Brand data
        ..."""
```

```python
@router.post('/', response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(db, product_in, current_user) -> Any:
    """
    Create new product.

    Args:
        db: Database session
        product_in: Product data
  ..."""
```

```python
@router.post('/{product_id}/descriptions', response_model=ProductDescriptionSchema)
async def create_product_description(product_id, description_in, db, current_user) -> Any:
    """
    Add a description to a product.

    Args:
        product_id: Product ID
        description_i..."""
```

```python
@router.post('/{product_id}/marketing', response_model=ProductMarketingSchema)
async def create_product_marketing(product_id, marketing_in, db, current_user) -> Any:
    """
    Add marketing content to a product.

    Args:
        product_id: Product ID
        marketing..."""
```

```python
@router.post('/{product_id}/measurements', response_model=ProductMeasurementSchema)
async def create_product_measurement(product_id, measurement_in, db, current_user) -> Any:
    """
    Add measurements to a product.

    Args:
        product_id: Product ID
        measurement_in..."""
```

```python
@router.post('/{product_id}/stock', response_model=ProductStockSchema)
async def create_product_stock(product_id, stock_in, db, current_user) -> Any:
    """
    Add stock information to a product.

    Args:
        product_id: Product ID
        stock_in:..."""
```

```python
@router.post('/{product_id}/supersessions', response_model=ProductSupersessionSchema)
async def create_product_supersession(product_id, supersession_in, db, current_user) -> Any:
    """
    Create a product supersession.

    Args:
        product_id: Product ID
        supersession_i..."""
```

```python
@router.delete('/brands/{brand_id}')
async def delete_brand(brand_id, db, current_user) -> dict:
    """
    Delete a brand.

    Args:
        brand_id: Brand ID
        db: Database session
        curr..."""
```

```python
@router.delete('/{product_id}')
async def delete_product(product_id, db, current_user) -> dict:
    """
    Delete a product.

    Args:
        product_id: Product ID
        db: Database session
      ..."""
```

```python
@router.delete('/{product_id}/descriptions/{description_id}')
async def delete_product_description(product_id, description_id, db, current_user) -> dict:
    """
    Delete a product description.

    Args:
        product_id: Product ID
        description_id:..."""
```

```python
@router.delete('/{product_id}/marketing/{marketing_id}')
async def delete_product_marketing(product_id, marketing_id, db, current_user) -> dict:
    """
    Delete product marketing content.

    Args:
        product_id: Product ID
        marketing_i..."""
```

```python
@router.delete('/{product_id}/stock/{stock_id}')
async def delete_product_stock(product_id, stock_id, db, current_user) -> dict:
    """
    Delete product stock information.

    Args:
        product_id: Product ID
        stock_id: S..."""
```

```python
@router.delete('/{product_id}/supersessions/{supersession_id}')
async def delete_product_supersession(product_id, supersession_id, db, current_user) -> dict:
    """
    Delete a product supersession.

    Args:
        product_id: Product ID
        supersession_i..."""
```

```python
@router.get('/brands/{brand_id}', response_model=BrandSchema)
async def read_brand(brand_id, db, current_user) -> Any:
    """
    Get brand by ID.

    Args:
        brand_id: Brand ID
        db: Database session
        cur..."""
```

```python
@router.get('/brands/', response_model=List[BrandSchema])
async def read_brands(db, current_user, skip, limit) -> Any:
    """
    Retrieve brands.

    Args:
        db: Database session
        current_user: Current authenti..."""
```

```python
@router.get('/{product_id}', response_model=ProductSchema)
async def read_product(product_id, db, current_user) -> Any:
    """
    Get product by ID.

    Args:
        product_id: Product ID
        db: Database session
     ..."""
```

```python
@router.get('/', response_model=ProductListResponse)
async def read_products(db, current_user, search, vintage, late_model, soft, universal, is_active, skip, limit, page, page_size) -> Any:
    """
    Retrieve products with filtering.

    Args:
        db: Database session
        current_user:..."""
```

```python
@router.put('/brands/{brand_id}', response_model=BrandSchema)
async def update_brand(brand_id, brand_in, db, current_user) -> Any:
    """
    Update a brand.

    Args:
        brand_id: Brand ID
        brand_in: Updated brand data
    ..."""
```

```python
@router.put('/{product_id}', response_model=ProductSchema)
async def update_product(product_id, product_in, db, current_user) -> Any:
    """
    Update a product.

    Args:
        product_id: Product ID
        product_in: Updated product..."""
```

```python
@router.put('/{product_id}/descriptions/{description_id}', response_model=ProductDescriptionSchema)
async def update_product_description(product_id, description_id, description_in, db, current_user) -> Any:
    """
    Update a product description.

    Args:
        product_id: Product ID
        description_id:..."""
```

```python
@router.put('/{product_id}/marketing/{marketing_id}', response_model=ProductMarketingSchema)
async def update_product_marketing(product_id, marketing_id, marketing_in, db, current_user) -> Any:
    """
    Update product marketing content.

    Args:
        product_id: Product ID
        marketing_i..."""
```

```python
@router.put('/{product_id}/stock/{stock_id}', response_model=ProductStockSchema)
async def update_product_stock(product_id, stock_id, stock_in, db, current_user) -> Any:
    """
    Update product stock information.

    Args:
        product_id: Product ID
        stock_id: S..."""
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
    """
    Decode a Vehicle Identification Number (VIN).

    Args:
        vin: Vehicle Identification Nu..."""
```

```python
@router.get('/vehicle-data/engines')
async def get_vehicle_engines(db, current_user, vehicle_service, make, model, year) -> List[str]:
    """
    Get all available vehicle engines.

    Args:
        db: Database session
        current_user..."""
```

```python
@router.get('/vehicle-data/makes')
async def get_vehicle_makes(db, current_user, vehicle_service, year) -> List[str]:
    """
    Get all available vehicle makes.

    Args:
        db: Database session
        current_user: ..."""
```

```python
@router.get('/vehicle-data/models')
async def get_vehicle_models(db, current_user, vehicle_service, make, year) -> List[str]:
    """
    Get all available vehicle models.

    Args:
        db: Database session
        current_user:..."""
```

```python
@router.get('/vehicle-data/transmissions')
async def get_vehicle_transmissions(db, current_user, vehicle_service, make, model, year, engine) -> List[str]:
    """
    Get all available vehicle transmissions.

    Args:
        db: Database session
        curren..."""
```

```python
@router.get('/vehicle-data/years')
async def get_vehicle_years(db, current_user, vehicle_service) -> List[int]:
    """
    Get all available vehicle years.

    Args:
        db: Database session
        current_user: ..."""
```

```python
@router.get('/')
async def global_search(db, current_user, search_service, q, entity_types, page, page_size) -> Any:
    """
    Perform a global search across multiple entity types.

    Args:
        db: Database session
 ..."""
```

```python
@router.get('/fitments')
async def search_fitments(db, current_user, search_service, q, year, make, model, engine, transmission, page, page_size) -> Any:
    """
    Search for fitments with filtering.

    Args:
        db: Database session
        current_use..."""
```

```python
@router.get('/products')
async def search_products(db, current_user, search_service, q, is_active, page, page_size, use_elasticsearch) -> Any:
    """
    Search for products with filtering.

    Args:
        db: Database session
        current_use..."""
```

```python
@router.post('/vehicle-data/validate-fitment')
async def validate_vehicle_fitment(db, current_user, vehicle_service, year, make, model, engine, transmission) -> dict:
    """
    Validate if a fitment combination exists.

    Args:
        db: Database session
        curre..."""
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
    """
    Create new company.

    Args:
        company_in: Company data
        db: Database session
  ..."""
```

```python
@router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_in, db, current_user) -> Any:
    """
    Create new user.

    Args:
        user_in: User data
        db: Database session
        cur..."""
```

```python
@router.delete('/companies/{company_id}')
async def delete_company(company_id, db, current_user) -> dict:
    """
    Delete a company.

    Args:
        company_id: Company ID
        db: Database session
      ..."""
```

```python
@router.delete('/{user_id}')
async def delete_user(user_id, db, current_user) -> dict:
    """
    Delete a user.

    Args:
        user_id: User ID
        db: Database session
        current..."""
```

```python
@router.get('/companies/', response_model=List[CompanySchema])
async def read_companies(db, current_user, skip, limit, is_active) -> Any:
    """
    Retrieve companies with filtering options.

    Args:
        db: Database session
        curr..."""
```

```python
@router.get('/companies/{company_id}', response_model=CompanySchema)
async def read_company(company_id, db, current_user) -> Any:
    """
    Get company by ID.

    Args:
        company_id: Company ID
        db: Database session
     ..."""
```

```python
@router.get('/{user_id}', response_model=UserSchema)
async def read_user(user_id, db, current_user) -> Any:
    """
    Get user by ID.

    Args:
        user_id: User ID
        db: Database session
        curren..."""
```

```python
@router.get('/me', response_model=UserSchema)
async def read_user_me(current_user, db) -> Any:
    """
    Get current user.

    Args:
        current_user: Current authenticated user
        db: Datab..."""
```

```python
@router.get('/', response_model=List[UserSchema])
async def read_users(db, current_user, skip, limit, role, company_id, is_active) -> Any:
    """
    Retrieve users with filtering options.

    Args:
        db: Database session
        current_..."""
```

```python
@router.put('/companies/{company_id}', response_model=CompanySchema)
async def update_company(company_id, company_in, db, current_user) -> Any:
    """
    Update a company.

    Args:
        company_id: Company ID
        company_in: Updated company..."""
```

```python
@router.put('/{user_id}', response_model=UserSchema)
async def update_user(user_id, user_in, db, current_user) -> Any:
    """
    Update a user.

    Args:
        user_id: User ID
        user_in: Updated user data
        d..."""
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
    """
    Get application settings with caching.
    
    This function is cached to avoid loading settin..."""
```

**Classes:**
```python
class CORSSettings(BaseSettings):
    """
    CORS settings.
    
    Attributes:
        BACKEND_CORS_ORIGINS: List of allowed origins for C..."""
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
        """
        Parse CORS origins from string or list.
        
        Args:
            v: CORS origins ..."""
```

```python
class CelerySettings(BaseSettings):
    """
    Celery worker settings.
    
    Attributes:
        CELERY_BROKER_URL: URL for Celery broker
 ..."""
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
    """
    Chat system settings.
    
    Attributes:
        CHAT_ENCRYPTION_SALT: Salt for chat message ..."""
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
    """
    Currency and exchange rate settings.
    
    Attributes:
        EXCHANGE_RATE_API_KEY: API ke..."""
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
    """
    Database connection settings.
    
    Attributes:
        POSTGRES_SERVER: PostgreSQL server h..."""
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
        """
        Assemble database URI from components.
        
        Returns:
            Self with SQLA..."""
```

```python
class ElasticsearchSettings(BaseSettings):
    """
    Elasticsearch connection settings.
    
    Attributes:
        ELASTICSEARCH_HOST: Elasticsear..."""
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
        """
        Get Elasticsearch URI.
        
        Returns:
            Elasticsearch connection URI
 ..."""
```

```python
class Environment(str, Enum):
    """
    Application environment enumeration.
    
    Attributes:
        DEVELOPMENT: Development envi..."""
```
*Class attributes:*
```python
DEVELOPMENT = 'development'
STAGING = 'staging'
PRODUCTION = 'production'
```

```python
class FitmentSettings(BaseSettings):
    """
    Fitment system settings.
    
    Attributes:
        VCDB_PATH: Path to VCDB Access database
 ..."""
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
        """
        Validate that required file paths exist.
        
        Returns:
            Self with va..."""
```

```python
class LocaleSettings(BaseSettings):
    """
    Internationalization and localization settings.
    
    Attributes:
        DEFAULT_LOCALE: De..."""
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
    """
    Log level enumeration.
    
    Attributes:
        DEBUG: Debug level logging
        INFO: In..."""
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
    """
    Logging configuration settings.
    
    Attributes:
        LOG_LEVEL: Default log level
     ..."""
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
    """
    Media handling settings.
    
    Attributes:
        MEDIA_ROOT: Root directory for media file..."""
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
        """
        Create media directories if they don't exist.
        
        Args:
            v: Media r..."""
```
```python
@property
    def media_base_url(self) -> str:
        """
        Get the base URL for media files.
        
        Returns:
            Base URL for media ..."""
```

```python
class RedisSettings(BaseSettings):
    """
    Redis connection settings.
    
    Attributes:
        REDIS_HOST: Redis server hostname
     ..."""
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
        """
        Get Redis URI.
        
        Returns:
            Redis connection URI
        """
```

```python
class SecuritySettings(BaseSettings):
    """
    Security settings.
    
    Attributes:
        SECRET_KEY: Secret key for token signing
      ..."""
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
    """
    Main application settings combining all subsystems.
    
    Attributes:
        PROJECT_NAME: ..."""
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
        """
        Parse CORS origins from string or list.
        
        Args:
            v: CORS origins ..."""
```
```python
@model_validator(mode='after')
    def assemble_db_connection(self) -> 'Settings':
        """
        Assemble database URI from components.
        
        Returns:
            Self with SQLA..."""
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
        """
        Create media directories if they don't exist.
        
        Args:
            v: Media r..."""
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
        """
        Get the base URL for media files.
        
        Returns:
            Base URL for media ..."""
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
    """
    Structlog processor that adds request_id from thread-local storage.
    
    Args:
        logg..."""
```

```python
def add_service_info_processor(logger, method_name, event_dict) -> EventDict:
    """
    Structlog processor that adds service information to log events.
    
    Args:
        logger:..."""
```

```python
def add_timestamp_processor(logger, method_name, event_dict) -> EventDict:
    """
    Structlog processor that adds timestamp to log events.
    
    Args:
        logger: Logger in..."""
```

```python
def add_user_id_processor(logger, method_name, event_dict) -> EventDict:
    """
    Structlog processor that adds user_id from thread-local storage.
    
    Args:
        logger:..."""
```

```python
def clear_user_id() -> None:
    """Clear the current user ID from the logging context."""
```

```python
def configure_std_logging() -> None:
    """
    Configure standard library logging with appropriate handlers and formatters.
    
    This sets..."""
```

```python
def configure_structlog() -> None:
    """
    Configure structlog with processors and renderers.
    
    This sets up structlog to work alon..."""
```

```python
def get_logger(name) -> BoundLogger:
    """
    Get a structlog logger instance.
    
    Args:
        name: Logger name (typically __name__)
..."""
```

```python
def log_execution_time(logger, level):
    """
    Decorator to log function execution time.
    
    Args:
        logger: Logger to use (created..."""
```

```python
def log_execution_time_async(logger, level):
    """
    Decorator to log async function execution time.
    
    Args:
        logger: Logger to use (c..."""
```

```python
@contextmanager
def request_context(request_id, user_id):
    """
    Context manager for tracking request context in logs.
    
    Args:
        request_id: Reques..."""
```

```python
def set_user_id(user_id) -> None:
    """
    Set the current user ID in the logging context.
    
    Args:
        user_id: User ID to set
..."""
```

```python
def setup_logging() -> None:
    """
    Set up the logging system.
    
    This function should be called early in the application sta..."""
```

**Classes:**
```python
class RequestIdFilter(logging.Filter):
    """
    Log filter that adds request_id from thread-local storage.
    
    This filter adds the curren..."""
```
*Methods:*
```python
    def filter(self, record) -> bool:
        """
        Add request_id to log record if available.
        
        Args:
            record: Log r..."""
```

```python
class UserIdFilter(logging.Filter):
    """
    Log filter that adds user_id from thread-local storage.
    
    This filter adds the current u..."""
```
*Methods:*
```python
    def filter(self, record) -> bool:
        """
        Add user_id to log record if available.
        
        Args:
            record: Log reco..."""
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
*SQLAlchemy base model class.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/db/base_class.py`

**Imports:**
```python
from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar
from sqlalchemy import Column, DateTime, inspect, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.expression import Select
```

**Global Variables:**
```python
T = T = TypeVar('T', bound='Base')
```

**Classes:**
```python
class Base(DeclarativeBase):
    """
    Base class for all database models.

    This class provides common functionality for all model..."""
```
*Methods:*
```python
@declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name automatically from class name.

        The generated name is the lower..."""
```
```python
    def dict(self) -> Dict[(str, Any)]:
        """
        Convert model instance to dictionary.

        This method is useful for API responses and ..."""
```
```python
@classmethod
    def filter_by_id(cls, id) -> Select:
        """
        Create a query to filter by id.

        Args:
            id: UUID primary key to filter b..."""
```
```python
    def update(self, **kwargs) -> None:
        """
        Update model attributes from keyword arguments.

        Args:
            **kwargs: Attrib..."""
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
    """
    Get a database session.

    This dependency provides an async database session that automatica..."""
```

```python
@contextlib.asynccontextmanager
async def get_db_context() -> AsyncGenerator[(AsyncSession, None)]:
    """
    Context manager for database sessions.

    This is useful for scripts that need to handle thei..."""
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
    """
    Create a new model mapping.

    Args:
        mapping_data: Mapping data
        mapping_engin..."""
```

```python
@router.delete('/model-mappings/{mapping_id}', status_code=status.HTTP_200_OK)
async def delete_model_mapping(mapping_id, mapping_engine):
    """
    Delete a model mapping.

    Args:
        mapping_id: ID of the mapping to delete
        mapp..."""
```

```python
def get_mapping_engine():
    """
    Get an instance of the mapping engine.

    This is a FastAPI dependency for endpoints that nee..."""
```

```python
@router.get('/pcdb-positions/{terminology_id}', response_model=List[Dict[(str, Any)]])
async def get_pcdb_positions(terminology_id, mapping_engine):
    """
    Get PCDB positions for a part terminology.

    Args:
        terminology_id: Part terminology ..."""
```

```python
@router.get('/model-mappings', response_model=ModelMappingList)
async def list_model_mappings(mapping_engine, skip, limit, pattern, sort_by, sort_order):
    """
    List model mappings from database.

    Args:
        mapping_engine: Mapping engine instance
 ..."""
```

```python
@router.post('/parse-application', response_model=Dict[(str, Any)])
async def parse_application(application_text, mapping_engine):
    """
    Parse a part application text.

    Args:
        application_text: Raw part application text
 ..."""
```

```python
@router.post('/process', response_model=ProcessFitmentResponse)
async def process_fitment(request, mapping_engine):
    """
    Process fitment application texts.

    Args:
        request: Request body with application te..."""
```

```python
@router.post('/refresh-mappings', status_code=status.HTTP_200_OK)
async def refresh_mappings(mapping_engine):
    """
    Refresh model mappings from the database.

    This allows for updating mappings without restar..."""
```

```python
@router.put('/model-mappings/{mapping_id}', response_model=ModelMappingSchema)
async def update_model_mapping(mapping_id, mapping_data, mapping_engine):
    """
    Update an existing model mapping.

    Args:
        mapping_id: ID of the mapping to update
  ..."""
```

```python
@router.post('/upload-model-mappings', response_model=UploadModelMappingsResponse)
async def upload_model_mappings(file, mapping_engine):
    """
    Upload model mappings JSON file.

    Args:
        file: JSON file with model mappings
       ..."""
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
    """
    Get the fitment settings.

    Returns:
        FitmentSettings instance
    """
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
        """
        Initialize the Access DB client.

        Args:
            db_path: Path to the MS Access ..."""
```
```python
    def connect(self) -> pyodbc.Connection:
        """
        Connect to the Access database.

        Returns:
            ODBC connection to the databa..."""
```
```python
    def query(self, sql, params) -> List[Dict[(str, Any)]]:
        """
        Execute a SQL query on the Access database.

        Args:
            sql: SQL query to ex..."""
```

```python
class FitmentDBService(object):
    """Service for database operations related to fitment data."""
```
*Methods:*
```python
    def __init__(self, vcdb_path, pcdb_path, sqlalchemy_url) -> None:
        """
        Initialize the fitment database service.

        Args:
            vcdb_path: Path to the ..."""
```
```python
    async def add_model_mapping(self, pattern, mapping, priority) -> int:
        """
        Add a new model mapping to the database.

        Args:
            pattern: Pattern to mat..."""
```
```python
    async def delete_model_mapping(self, mapping_id) -> bool:
        """
        Delete a model mapping.

        Args:
            mapping_id: ID of the mapping to delete
..."""
```
```python
    async def get_model_mappings(self) -> Dict[(str, List[str])]:
        """
        Get model mappings from the database.

        Returns:
            Dictionary of model map..."""
```
```python
    def get_pcdb_part_terminology(self, terminology_id) -> PartTerminology:
        """
        Get part terminology information from PCDB.

        Args:
            terminology_id: ID o..."""
```
```python
    def get_pcdb_positions(self, position_ids) -> List[PCDBPosition]:
        """
        Get position information from PCDB.

        Args:
            position_ids: Optional list ..."""
```
```python
@asynccontextmanager
    async def get_session(self) -> AsyncGenerator[(AsyncSession, None)]:
        """
        Get an async session for database operations.

        Yields:
            AsyncSession obj..."""
```
```python
    def get_vcdb_vehicles(self, year, make, model) -> List[VCDBVehicle]:
        """
        Get vehicles from VCDB matching the specified criteria.

        Args:
            year: Op..."""
```
```python
    async def import_mappings_from_json(self, json_data) -> int:
        """
        Import mappings from a JSON dictionary.

        Args:
            json_data: Dictionary wh..."""
```
```python
    def load_model_mappings_from_json(self, json_path) -> Dict[(str, List[str])]:
        """
        Load model mappings from a JSON file.

        Args:
            json_path: Path to the JSO..."""
```
```python
    async def save_fitment_results(self, product_id, fitments) -> bool:
        """
        Save fitment results to the database.

        Args:
            product_id: ID of the prod..."""
```
```python
    async def update_model_mapping(self, mapping_id, **kwargs) -> bool:
        """
        Update an existing model mapping.

        Args:
            mapping_id: ID of the mapping ..."""
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
    """
    Get a singleton instance of the FitmentDBService.

    Returns:
        FitmentDBService instan..."""
```

```python
@lru_cache(maxsize=1)
def get_fitment_mapping_engine() -> FitmentMappingEngine:
    """
    Get a singleton instance of the FitmentMappingEngine.

    Returns:
        FitmentMappingEngin..."""
```

```python
async def initialize_mapping_engine() -> None:
    """
    Initialize the mapping engine with database mappings.

    This should be called during applica..."""
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
        """
        Initialize a configuration error.

        Args:
            message: Error message
       ..."""
```

```python
class DatabaseError(FitmentError):
    """Exception raised when a database operation fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """
        Initialize a database error.

        Args:
            message: Error message
            ..."""
```

```python
class FitmentError(Exception):
    """Base class for all fitment module exceptions."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """
        Initialize a fitment error.

        Args:
            message: Error message
            d..."""
```

```python
class MappingError(FitmentError):
    """Exception raised when mapping a fitment fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """
        Initialize a mapping error.

        Args:
            message: Error message
            d..."""
```

```python
class ParsingError(FitmentError):
    """Exception raised when parsing a fitment string fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """
        Initialize a parsing error.

        Args:
            message: Error message
            d..."""
```

```python
class ValidationError(FitmentError):
    """Exception raised when validating a fitment fails."""
```
*Methods:*
```python
    def __init__(self, message, details) -> None:
        """
        Initialize a validation error.

        Args:
            message: Error message
          ..."""
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
        """
        Initialize the mapping engine.

        Args:
            db_service: Database service for ..."""
```
```python
    def batch_process_applications(self, application_texts, terminology_id) -> Dict[(str, List[ValidationResult])]:
        """
        Process a batch of part application strings.

        Args:
            application_texts: ..."""
```
```python
    def configure(self, model_mappings_path) -> None:
        """
        Configure the mapping engine with model mappings.

        Args:
            model_mappings..."""
```
```python
    async def configure_from_database(self) -> None:
        """
        Configure the mapping engine with model mappings from the database.

        This allows fo..."""
```
```python
    def configure_from_file(self, model_mappings_path) -> None:
        """
        Configure the mapping engine with model mappings from a file.

        Args:
            mo..."""
```
```python
@lru_cache(maxsize=100)
    def get_part_terminology(self, terminology_id) -> PartTerminology:
        """
        Get part terminology information by ID.

        Args:
            terminology_id: ID of th..."""
```
```python
@lru_cache(maxsize=100)
    def get_pcdb_positions(self, terminology_id) -> List[PCDBPosition]:
        """
        Get PCDB positions for a part terminology.

        Args:
            terminology_id: ID of..."""
```
```python
    def get_vcdb_vehicles(self, year, make, model) -> List[VCDBVehicle]:
        """
        Get VCDB vehicles matching criteria.

        Args:
            year: Optional year filter
..."""
```
```python
    def process_application(self, application_text, terminology_id) -> List[ValidationResult]:
        """
        Process a part application string and validate against databases.

        Args:
          ..."""
```
```python
    async def refresh_mappings(self) -> None:
        """
        Refresh model mappings from the database.

        This allows for reloading mappings witho..."""
```
```python
    async def save_mapping_results(self, product_id, results) -> bool:
        """
        Save mapping results to the database.

        Args:
            product_id: ID of the prod..."""
```
```python
    def serialize_validation_results(self, results) -> List[Dict[(str, Any)]]:
        """
        Serialize validation results to JSON-compatible dictionaries.

        Args:
            re..."""
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
        """
        Initialize the parser with model mappings.

        Args:
            model_mappings: Dicti..."""
```
```python
    def expand_year_range(self, start_year, end_year) -> List[int]:
        """
        Expand a year range into a list of individual years.

        Args:
            start_year:..."""
```
```python
    def extract_positions(self, position_text) -> List[PositionGroup]:
        """
        Extract position information from the position text.

        Args:
            position_te..."""
```
```python
    def extract_year_range(self, year_text) -> Tuple[(int, int)]:
        """
        Extract start and end years from a year range string.

        Args:
            year_text:..."""
```
```python
    def find_model_mapping(self, vehicle_text) -> List[Dict[(str, str)]]:
        """
        Find the appropriate model mapping for the vehicle text.

        Args:
            vehicle..."""
```
```python
    def parse_application(self, application_text) -> PartApplication:
        """
        Parse a raw part application text into a structured PartApplication object.

        Args:
..."""
```
```python
    def process_application(self, part_app) -> List[PartFitment]:
        """
        Process a part application into a list of specific part fitments.

        Args:
          ..."""
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
        """
        Initialize the validator.

        Args:
            part_terminology_id: ID of the part te..."""
```
```python
    def validate_fitment(self, fitment, available_vehicles) -> ValidationResult:
        """
        Validate a fitment against VCDB and PCDB data.

        Args:
            fitment: The fitm..."""
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
    """
    Chat room member model.
    
    This model tracks users' membership in chat rooms:
    - Each ..."""
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
    """
    Roles of chat room members.
    
    Defines the possible roles a user can have in a chat room:..."""
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
    """
    Chat message model.
    
    This model represents individual messages in chat rooms:
    - Mes..."""
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
    """
    Chat room model representing a conversation space.
    
    This model defines a chat room wher..."""
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
    """
    Types of chat rooms supported by the system.
    
    Defines the possible chat room configurat..."""
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
    """
    Message reaction model.
    
    This model tracks reactions to messages (like emoji reactions)..."""
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
    """
    Types of messages supported by the chat system.
    
    Defines the possible message types:
  ..."""
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
    """
    Rate limiting log model.
    
    This model tracks rate limiting for users to prevent spam:
  ..."""
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
    """
    Statuses for regulatory approvals.

    Defines the possible states of a regulatory approval.
 ..."""
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
    """
    Types of chemical hazards under Proposition 65.

    Defines the categories of chemical hazards..."""
```
*Class attributes:*
```python
CARCINOGEN = 'Carcinogen'
REPRODUCTIVE_TOXICANT = 'Reproductive Toxicant'
BOTH = 'Both'
```

```python
class ExposureScenario(str, Enum):
    """
    Types of exposure scenarios for chemicals.

    Defines the different contexts in which chemica..."""
```
*Class attributes:*
```python
CONSUMER = 'Consumer'
OCCUPATIONAL = 'Occupational'
ENVIRONMENTAL = 'Environmental'
```

```python
class HazardousMaterial(Base):
    """
    Hazardous material model.

    Represents hazardous material information for products.

    Att..."""
```
*Class attributes:*
```python
__tablename__ = 'hazardous_material'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the hazardous material.

        Returns:
            str: Hazardo..."""
```

```python
class ProductChemical(Base):
    """
    Product chemical association model.

    Represents relationships between products and chemical..."""
```
*Class attributes:*
```python
__tablename__ = 'product_chemical'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product chemical association.

        Returns:
            st..."""
```

```python
class ProductDOTApproval(Base):
    """
    Product DOT approval model.

    Represents Department of Transportation approvals for products..."""
```
*Class attributes:*
```python
__tablename__ = 'product_dot_approval'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the DOT approval.

        Returns:
            str: DOT approval ..."""
```

```python
class Prop65Chemical(Base):
    """
    Proposition 65 chemical model.

    Represents chemicals listed under California's Proposition ..."""
```
*Class attributes:*
```python
__tablename__ = 'prop65_chemical'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the chemical.

        Returns:
            str: Chemical represen..."""
```

```python
class TransportRestriction(str, Enum):
    """
    Types of transportation restrictions.

    Defines the possible transportation restrictions for..."""
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
    """
    Warning model.

    Represents warning text for chemicals in products.

    Attributes:
       ..."""
```
*Class attributes:*
```python
__tablename__ = 'warning'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the warning.

        Returns:
            str: Warning representa..."""
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
    """
    Currency model.

    Represents currency information:
    - ISO codes
    - Name
    - Symbol
 ..."""
```
*Class attributes:*
```python
__tablename__ = 'currency'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the currency.

        Returns:
            str: Currency represen..."""
```

```python
class ExchangeRate(Base):
    """
    Exchange rate model.

    Tracks historical exchange rates between currencies:
    - Source and..."""
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
        """
        String representation of the exchange rate.

        Returns:
            str: Exchange rat..."""
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
    """
    Address model.

    Represents physical addresses for companies, warehouses, etc.

    Attribut..."""
```
*Class attributes:*
```python
__tablename__ = 'address'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the address.

        Returns:
            str: Address representa..."""
```

```python
class Country(Base):
    """
    Country model.

    Represents countries with ISO codes and related information.

    Attribute..."""
```
*Class attributes:*
```python
__tablename__ = 'country'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the country.

        Returns:
            str: Country representa..."""
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
    """
    Media model for storing file metadata.

    This model tracks uploaded files and their metadata..."""
```
*Class attributes:*
```python
__tablename__ = 'media'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the media.

        Returns:
            str: Media representation..."""
```
```python
@property
    def extension(self) -> str:
        """
        Get the file extension from the filename.

        Returns:
            str: File extension..."""
```
```python
@property
    def has_thumbnail(self) -> bool:
        """
        Check if the media should have a thumbnail.

        Returns:
            bool: True if med..."""
```
```python
@property
    def is_image(self) -> bool:
        """
        Check if the media is an image.

        Returns:
            bool: True if media_type is I..."""
```

```python
class MediaType(str, Enum):
    """
    Types of media files supported by the system.

    Defines the different categories of files th..."""
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
    """
    Visibility levels for media files.

    Controls who can access the media files:
    - PUBLIC: ..."""
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
    """
    Model mapping database model.

    This model stores mappings between part application text pat..."""
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
    """
    Attribute definition model.

    Defines flexible product attributes.

    Attributes:
        ..."""
```
*Class attributes:*
```python
__tablename__ = 'attribute_definition'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the attribute definition.

        Returns:
            str: Attri..."""
```

```python
class Brand(Base):
    """
    Brand model.

    Represents product brands.

    Attributes:
        id: Primary key UUID
    ..."""
```
*Class attributes:*
```python
__tablename__ = 'brand'
parent_company =     parent_company = relationship("Company", foreign_keys=[parent_company_id])
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the brand.

        Returns:
            str: Brand representation..."""
```

```python
class Fitment(Base):
    """
    Fitment model representing vehicle compatibility information.

    This model stores informatio..."""
```
*Class attributes:*
```python
__tablename__ = 'fitment'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the fitment.

        Returns:
            str: Fitment representa..."""
```

```python
class Manufacturer(Base):
    """
    Manufacturer model.

    Represents product manufacturers.

    Attributes:
        id: Primary..."""
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
        """
        String representation of the manufacturer.

        Returns:
            str: Manufacturer ..."""
```

```python
class PriceType(Base):
    """
    Price type model.

    Defines types of prices.

    Attributes:
        id: Primary key UUID
 ..."""
```
*Class attributes:*
```python
__tablename__ = 'price_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the price type.

        Returns:
            str: Price type repr..."""
```

```python
class Product(Base):
    """
    Product model representing automotive parts and accessories.

    This model stores core inform..."""
```
*Class attributes:*
```python
__tablename__ = 'product'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product.

        Returns:
            str: Product representa..."""
```

```python
class ProductActivity(Base):
    """
    Product activity model.

    Tracks status changes for products.

    Attributes:
        id: P..."""
```
*Class attributes:*
```python
__tablename__ = 'product_activity'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product activity.

        Returns:
            str: Product a..."""
```

```python
class ProductAttribute(Base):
    """
    Product attribute model.

    Stores flexible attribute values for products.

    Attributes:
 ..."""
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
        """
        String representation of the product attribute.

        Returns:
            str: Product ..."""
```

```python
class ProductBrandHistory(Base):
    """
    Product brand history model.

    Tracks brand changes for products.

    Attributes:
        i..."""
```
*Class attributes:*
```python
__tablename__ = 'product_brand_history'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product brand history.

        Returns:
            str: Prod..."""
```

```python
class ProductDescription(Base):
    """
    Product description model.

    Stores different types of descriptions for products.

    Attri..."""
```
*Class attributes:*
```python
__tablename__ = 'product_description'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product description.

        Returns:
            str: Produc..."""
```

```python
class ProductMarketing(Base):
    """
    Product marketing model.

    Stores marketing content for products.

    Attributes:
        i..."""
```
*Class attributes:*
```python
__tablename__ = 'product_marketing'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product marketing.

        Returns:
            str: Product ..."""
```

```python
class ProductMeasurement(Base):
    """
    Product measurement model.

    Stores dimensional information for products.

    Attributes:
 ..."""
```
*Class attributes:*
```python
__tablename__ = 'product_measurement'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product measurement.

        Returns:
            str: Produc..."""
```

```python
class ProductPricing(Base):
    """
    Product pricing model.

    Stores pricing information for products.

    Attributes:
        i..."""
```
*Class attributes:*
```python
__tablename__ = 'product_pricing'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product pricing.

        Returns:
            str: Product pr..."""
```

```python
class ProductStock(Base):
    """
    Product stock model.

    Tracks inventory levels for products.

    Attributes:
        id: Pr..."""
```
*Class attributes:*
```python
__tablename__ = 'product_stock'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product stock.

        Returns:
            str: Product stoc..."""
```

```python
class ProductSupersession(Base):
    """
    Product supersession model.

    Tracks product replacements.

    Attributes:
        id: Prim..."""
```
*Class attributes:*
```python
__tablename__ = 'product_supersession'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the product supersession.

        Returns:
            str: Produ..."""
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
    """
    Color model.

    Represents standard color names and their hex codes.

    Attributes:
       ..."""
```
*Class attributes:*
```python
__tablename__ = 'color'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the color.

        Returns:
            str: Color representation..."""
```

```python
class ConstructionType(Base):
    """
    Construction type model.

    Represents materials used in product construction.

    Attribute..."""
```
*Class attributes:*
```python
__tablename__ = 'construction_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the construction type.

        Returns:
            str: Construc..."""
```

```python
class Hardware(Base):
    """
    Hardware item model.

    Represents hardware items included with products.

    Attributes:
  ..."""
```
*Class attributes:*
```python
__tablename__ = 'hardware_item'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the hardware item.

        Returns:
            str: Hardware ite..."""
```

```python
class PackagingType(Base):
    """
    Packaging type model.

    Represents types of product packaging.

    Attributes:
        id: ..."""
```
*Class attributes:*
```python
__tablename__ = 'packaging_type'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the packaging type.

        Returns:
            str: Packaging t..."""
```

```python
class TariffCode(Base):
    """
    Tariff code model.

    Represents HS, HTS, or other tariff codes.

    Attributes:
        id:..."""
```
*Class attributes:*
```python
__tablename__ = 'tariff_code'
country =     country = relationship("Country")
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the tariff code.

        Returns:
            str: Tariff code re..."""
```

```python
class Texture(Base):
    """
    Texture model.

    Represents surface textures of products.

    Attributes:
        id: Prima..."""
```
*Class attributes:*
```python
__tablename__ = 'texture'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the texture.

        Returns:
            str: Texture representa..."""
```

```python
class UnspscCode(Base):
    """
    UNSPSC code model.

    Represents United Nations Standard Products and Services Code.

    Att..."""
```
*Class attributes:*
```python
__tablename__ = 'unspsc_code'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the UNSPSC code.

        Returns:
            str: UNSPSC code re..."""
```

```python
class Warehouse(Base):
    """
    Warehouse model.

    Represents product storage locations.

    Attributes:
        id: Primar..."""
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
        """
        String representation of the warehouse.

        Returns:
            str: Warehouse repres..."""
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
    """
    Create a JWT access token.

    Args:
        subject: Subject (usually user ID) to include in ..."""
```

```python
def get_password_hash(password) -> str:
    """
    Hash a password using Bcrypt.

    Args:
        password: Plain text password

    Returns:
  ..."""
```

```python
def verify_password(plain_password, hashed_password) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password: Plain text password
      ..."""
```

**Classes:**
```python
class Company(Base):
    """
    Company model for B2B customers and distributors.

    This model stores information about clie..."""
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
        """
        String representation of the company.

        Returns:
            str: Company representa..."""
```

```python
class User(Base):
    """
    User model for authentication and authorization.

    This model stores user information, crede..."""
```
*Class attributes:*
```python
__tablename__ = 'user'
```
*Methods:*
```python
    def __repr__(self) -> str:
        """
        String representation of the user.

        Returns:
            str: User representation w..."""
```

```python
class UserRole(str, Enum):
    """
    User role enumeration for authorization.

    These roles define different permission levels in..."""
```
*Class attributes:*
```python
ADMIN = 'admin'
MANAGER = 'manager'
CLIENT = 'client'
DISTRIBUTOR = 'distributor'
READ_ONLY = 'read_only'
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
    """
    Chat room member schema.
    
    Attributes:
        user_id: User identifier
        user_nam..."""
```

```python
class ChatMessageSchema(BaseModel):
    """
    Chat message schema.
    
    Attributes:
        id: Message identifier
        room_id: Room ..."""
```

```python
class ChatRoomSchema(BaseModel):
    """
    Chat room information schema.
    
    Attributes:
        id: Room identifier
        name: Ro..."""
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
    """
    Command to delete a message.
    
    Attributes:
        room_id: Room identifier
        mess..."""
```

```python
class EditMessageCommand(BaseModel):
    """
    Command to edit a message.
    
    Attributes:
        room_id: Room identifier
        messag..."""
```

```python
class FetchHistoryCommand(BaseModel):
    """
    Command to fetch message history.
    
    Attributes:
        room_id: Room identifier
       ..."""
```

```python
class JoinRoomCommand(BaseModel):
    """
    Command to join a chat room.
    
    Attributes:
        room_id: Room identifier
    """
```

```python
class LeaveRoomCommand(BaseModel):
    """
    Command to leave a chat room.
    
    Attributes:
        room_id: Room identifier
    """
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
    """
    Command for message reactions.
    
    Attributes:
        room_id: Room identifier
        me..."""
```

```python
class ReadMessagesCommand(BaseModel):
    """
    Command to mark messages as read.
    
    Attributes:
        room_id: Room identifier
       ..."""
```

```python
class SendMessageCommand(BaseModel):
    """
    Command to send a message.
    
    Attributes:
        room_id: Room identifier
        conten..."""
```

```python
class TypingCommand(BaseModel):
    """
    Command for typing indicators.
    
    Attributes:
        room_id: Room identifier
    """
```

```python
class UserPresenceSchema(BaseModel):
    """
    User presence information schema.
    
    Attributes:
        user_id: User identifier
       ..."""
```

```python
class WebSocketCommand(BaseModel):
    """
    Base WebSocket command structure.
    
    This model defines the common structure for all WebS..."""
```

```python
class WebSocketResponse(BaseModel):
    """
    Base WebSocket response structure.
    
    This model defines the common structure for all Web..."""
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
    """
    Error response for file upload.

    This schema defines the structure of error responses for f..."""
```

```python
class FileUploadResponse(BaseModel):
    """
    Response after file upload.

    This schema defines the structure of responses to file uploads..."""
```

```python
class Media(MediaInDB):
    """
    Schema for Media responses.

    This schema is used for API responses returning media data.
  ..."""
```
*Methods:*
```python
    def model_post_init(self, __context) -> None:
        """
        Post initialization hook to set URLs.

        This method runs after the model is initiali..."""
```

```python
class MediaBase(BaseModel):
    """
    Base schema for Media data.

    Defines common fields used across media-related schemas.

    ..."""
```

```python
class MediaCreate(BaseModel):
    """
    Schema for creating new Media (separate from file upload).

    This schema is used for the for..."""
```

```python
class MediaInDB(MediaBase):
    """
    Schema for Media as stored in the database.

    Extends the base media schema with database-sp..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class MediaListResponse(BaseModel):
    """
    Paginated response for media listings.

    This schema provides a structure for paginated medi..."""
```

```python
class MediaUpdate(BaseModel):
    """
    Schema for updating existing Media.

    Defines fields that can be updated on a media asset, w..."""
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
    """
    Schema for Brand responses.

    This schema is used for API responses returning brand data.

 ..."""
```

```python
class BrandBase(BaseModel):
    """
    Base schema for Brand data.

    Defines common fields used across brand schemas.

    Attribut..."""
```

```python
class BrandCreate(BrandBase):
    """
    Schema for creating a new Brand.

    Extends the base brand schema for creation requests.
    """
```

```python
class BrandInDB(BrandBase):
    """
    Schema for Brand as stored in the database.

    Extends the base brand schema with database-sp..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class BrandUpdate(BaseModel):
    """
    Schema for updating an existing Brand.

    Defines fields that can be updated on a brand.

   ..."""
```

```python
class DescriptionType(str, Enum):
    """
    Types of product descriptions.

    Defines the different categories of descriptions that can b..."""
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
    """
    Schema for Fitment responses.

    This schema is used for API responses returning fitment data..."""
```

```python
class FitmentBase(BaseModel):
    """
    Base schema for Fitment data.

    Defines common fields used across fitment-related schemas.

..."""
```
*Methods:*
```python
@field_validator('year')
@classmethod
    def validate_year(cls, v) -> int:
        """
        Validate the year is within a reasonable range.

        Args:
            v: Year value

 ..."""
```

```python
class FitmentCreate(FitmentBase):
    """
    Schema for creating a new Fitment.

    Extends the base fitment schema for creation requests.
..."""
```

```python
class FitmentInDB(FitmentBase):
    """
    Schema for Fitment as stored in the database.

    Extends the base fitment schema with databas..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class FitmentListResponse(PaginatedResponse):
    """
    Paginated response for fitment listings.

    This schema specializes the generic paginated res..."""
```

```python
class FitmentUpdate(BaseModel):
    """
    Schema for updating an existing Fitment.

    Defines fields that can be updated on a fitment, ..."""
```
*Methods:*
```python
@field_validator('year')
@classmethod
    def validate_year(cls, v) -> Optional[int]:
        """
        Validate the year is within a reasonable range if provided.

        Args:
            v: Y..."""
```

```python
class MarketingType(str, Enum):
    """
    Types of product marketing content.

    Defines the different categories of marketing content ..."""
```
*Class attributes:*
```python
BULLET_POINT = 'Bullet Point'
AD_COPY = 'Ad Copy'
```

```python
class PaginatedResponse(BaseModel):
    """
    Generic paginated response schema.

    This schema provides a structure for paginated list res..."""
```

```python
class Product(ProductInDB):
    """
    Schema for Product responses.

    This schema is used for API responses returning product data..."""
```

```python
class ProductActivity(ProductActivityInDB):
    """
    Schema for Product Activity responses.

    This schema is used for API responses returning pro..."""
```

```python
class ProductActivityBase(BaseModel):
    """
    Base schema for Product Activity data.

    Defines common fields used across product activity ..."""
```

```python
class ProductActivityCreate(ProductActivityBase):
    """
    Schema for creating a new Product Activity.

    Extends the base product activity schema for c..."""
```

```python
class ProductActivityInDB(ProductActivityBase):
    """
    Schema for Product Activity as stored in the database.

    Extends the base product activity s..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductBase(BaseModel):
    """
    Base schema for Product data.

    Defines common fields used across product schemas.

    Attr..."""
```
*Methods:*
```python
@model_validator(mode='after')
    def generate_part_number_stripped(self) -> 'ProductBase':
        """
        Generate the stripped part number if not provided.

        Returns:
            ProductBas..."""
```

```python
class ProductCreate(ProductBase):
    """
    Schema for creating a new Product.

    Extends the base product schema for creation requests.
..."""
```

```python
class ProductDescription(ProductDescriptionInDB):
    """
    Schema for Product Description responses.

    This schema is used for API responses returning ..."""
```

```python
class ProductDescriptionBase(BaseModel):
    """
    Base schema for Product Description data.

    Defines common fields used across product descri..."""
```

```python
class ProductDescriptionCreate(ProductDescriptionBase):
    """
    Schema for creating a new Product Description.

    Extends the base product description schema..."""
```

```python
class ProductDescriptionInDB(ProductDescriptionBase):
    """
    Schema for Product Description as stored in the database.

    Extends the base product descrip..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductDescriptionUpdate(BaseModel):
    """
    Schema for updating an existing Product Description.

    Defines fields that can be updated on..."""
```

```python
class ProductInDB(ProductBase):
    """
    Schema for Product as stored in the database.

    Extends the base product schema with databas..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductListResponse(PaginatedResponse):
    """
    Paginated response for product listings.

    This schema specializes the generic paginated res..."""
```

```python
class ProductMarketing(ProductMarketingInDB):
    """
    Schema for Product Marketing responses.

    This schema is used for API responses returning pr..."""
```

```python
class ProductMarketingBase(BaseModel):
    """
    Base schema for Product Marketing data.

    Defines common fields used across product marketin..."""
```

```python
class ProductMarketingCreate(ProductMarketingBase):
    """
    Schema for creating a new Product Marketing.

    Extends the base product marketing schema for..."""
```

```python
class ProductMarketingInDB(ProductMarketingBase):
    """
    Schema for Product Marketing as stored in the database.

    Extends the base product marketing..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductMarketingUpdate(BaseModel):
    """
    Schema for updating an existing Product Marketing.

    Defines fields that can be updated on p..."""
```

```python
class ProductMeasurement(ProductMeasurementInDB):
    """
    Schema for Product Measurement responses.

    This schema is used for API responses returning ..."""
```

```python
class ProductMeasurementBase(BaseModel):
    """
    Base schema for Product Measurement data.

    Defines common fields used across product measur..."""
```

```python
class ProductMeasurementCreate(ProductMeasurementBase):
    """
    Schema for creating a new Product Measurement.

    Extends the base product measurement schema..."""
```

```python
class ProductMeasurementInDB(ProductMeasurementBase):
    """
    Schema for Product Measurement as stored in the database.

    Extends the base product measure..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductMeasurementUpdate(ProductMeasurementBase):
    """
    Schema for updating an existing Product Measurement.

    Fields are the same as the base schem..."""
```

```python
class ProductStatus(str, Enum):
    """
    Product status options.

    Defines the possible status values for product activities.
    """
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
    """
    Schema for Product Stock responses.

    This schema is used for API responses returning produc..."""
```

```python
class ProductStockBase(BaseModel):
    """
    Base schema for Product Stock data.

    Defines common fields used across product stock schema..."""
```

```python
class ProductStockCreate(ProductStockBase):
    """
    Schema for creating a new Product Stock.

    Extends the base product stock schema for creatio..."""
```

```python
class ProductStockInDB(ProductStockBase):
    """
    Schema for Product Stock as stored in the database.

    Extends the base product stock schema ..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductStockUpdate(BaseModel):
    """
    Schema for updating an existing Product Stock.

    Defines fields that can be updated on produ..."""
```

```python
class ProductSupersession(ProductSupersessionInDB):
    """
    Schema for Product Supersession responses.

    This schema is used for API responses returning..."""
```

```python
class ProductSupersessionBase(BaseModel):
    """
    Base schema for Product Supersession data.

    Defines common fields used across product super..."""
```

```python
class ProductSupersessionCreate(ProductSupersessionBase):
    """
    Schema for creating a new Product Supersession.

    Extends the base product supersession sche..."""
```

```python
class ProductSupersessionInDB(ProductSupersessionBase):
    """
    Schema for Product Supersession as stored in the database.

    Extends the base product supers..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class ProductSupersessionUpdate(BaseModel):
    """
    Schema for updating an existing Product Supersession.

    Defines fields that can be updated o..."""
```

```python
class ProductUpdate(BaseModel):
    """
    Schema for updating an existing Product.

    Defines fields that can be updated on a product, ..."""
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
    """
    Schema for Company responses.

    This schema is used for API responses returning company data..."""
```

```python
class CompanyBase(BaseModel):
    """
    Base schema for Company data.

    Defines common fields used across company-related schemas.

..."""
```

```python
class CompanyCreate(CompanyBase):
    """
    Schema for creating a new Company.

    Extends the base company schema for creation requests.
..."""
```

```python
class CompanyInDB(CompanyBase):
    """
    Schema for Company as stored in the database.

    Extends the base company schema with databas..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class CompanyUpdate(BaseModel):
    """
    Schema for updating an existing Company.

    Defines fields that can be updated on a company, ..."""
```

```python
class Token(BaseModel):
    """
    Token schema for authentication responses.

    This schema defines the structure of token resp..."""
```

```python
class TokenPayload(BaseModel):
    """
    Token payload schema.

    This schema defines the structure of the JWT token payload
    for v..."""
```

```python
class User(UserInDB):
    """
    Schema for User responses.

    This schema is used for API responses returning user data.
    ..."""
```

```python
class UserBase(BaseModel):
    """
    Base schema for User data.

    Defines common fields used across user-related schemas.

    At..."""
```

```python
class UserCreate(UserBase):
    """
    Schema for creating a new User.

    Extends the base user schema with password field for user ..."""
```

```python
class UserInDB(UserBase):
    """
    Schema for User as stored in the database.

    Extends the base user schema with database-spec..."""
```
*Class attributes:*
```python
model_config =     model_config = ConfigDict(from_attributes=True)
```

```python
class UserRole(str, Enum):
    """
    User role enumeration.

    Defines the possible roles a user can have in the system,
    deter..."""
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
    """
    Schema for updating an existing User.

    Defines fields that can be updated on a user, with a..."""
```
*Methods:*
```python
@validator('password')
    def password_strength(cls, v) -> Optional[str]:
        """
        Validate password strength.

        Args:
            v: Password value

        Returns:
..."""
```

#### Package: services
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services`

**__init__.py:**
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/app/services/__init__.py`

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
        """
        Convert an amount from one currency to another.

        Args:
            db: Database ses..."""
```
```python
@classmethod
    async def fetch_latest_rates(cls, db, base_currency) -> Dict[(str, float)]:
        """
        Fetch the latest exchange rates from the API.

        Args:
            db: Database sessi..."""
```
```python
@classmethod
@redis_cache(prefix='currency', ttl=3600)
    async def get_latest_exchange_rate(cls, db, source_code, target_code) -> Optional[float]:
        """
        Get the latest exchange rate between two currencies.

        Args:
            db: Databas..."""
```
```python
@classmethod
    async def update_exchange_rates(cls, db, force) -> int:
        """
        Update exchange rates in the database.

        Args:
            db: Database session
    ..."""
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
        """
        Delete file from local storage asynchronously.

        Args:
            file_path: Relati..."""
```
```python
    async def file_exists(self, file_path) -> bool:
        """
        Check if a file exists in storage asynchronously.

        Args:
            file_path: Rel..."""
```
```python
    async def generate_thumbnail(self, file_path, width, height) -> Optional[str]:
        """
        Generate a thumbnail for an image file asynchronously.

        Args:
            file_path..."""
```
```python
    async def get_file_url(self, file_path) -> str:
        """
        Get URL for local file.

        Args:
            file_path: Relative path to the file

  ..."""
```
```python
    async def initialize(self) -> None:
        """
        Initialize storage backend connection.

        For local storage, this is a no-op as direc..."""
```
```python
    async def save_file(self, file, destination, media_type, content_type) -> str:
        """
        Save file to local storage asynchronously.

        Args:
            file: The file to upl..."""
```

```python
@dataclass
class MediaService(object):
    """Improved media service with better error handling and async support."""
```
*Methods:*
```python
    async def delete_file(self, file_url) -> bool:
        """
        Delete a file from storage with improved error handling.

        Args:
            file_ur..."""
```
```python
    async def ensure_initialized(self) -> None:
        """Ensure the service is initialized."""
```
```python
    async def initialize(self) -> None:
        """
        Initialize the media service and storage backend.

        This must be called before using..."""
```
```python
    async def upload_file(self, file, media_type, product_id, filename, visibility, generate_thumbnail) -> Tuple[(str, Dict[(str, Any)], Optional[str])]:
        """
        Upload a file to storage with improved error handling.

        Args:
            file: The..."""
```

```python
class MediaStorageBackend(Protocol):
    """Protocol defining media storage backend interface."""
```
*Methods:*
```python
    async def delete_file(self, file_path) -> bool:
        """
        Delete a file from storage.

        Args:
            file_path: Relative path to the file..."""
```
```python
    async def file_exists(self, file_path) -> bool:
        """
        Check if a file exists in storage.

        Args:
            file_path: Relative path to t..."""
```
```python
    async def generate_thumbnail(self, file_path, width, height) -> Optional[str]:
        """
        Generate a thumbnail for an image file.

        Args:
            file_path: Relative path..."""
```
```python
    async def get_file_url(self, file_path) -> str:
        """
        Get the URL for accessing a file.

        Args:
            file_path: Relative path to th..."""
```
```python
    async def initialize(self) -> None:
        """Initialize storage backend connection."""
```
```python
    async def save_file(self, file, destination, media_type, content_type) -> str:
        """
        Save a file to storage and return its public URL.

        Args:
            file: The file..."""
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
        """
        Delete file from S3 storage.

        Args:
            file_path: Relative path to the fil..."""
```
```python
    async def file_exists(self, file_path) -> bool:
        """
        Check if a file exists in S3 storage.

        Args:
            file_path: Relative path t..."""
```
```python
    async def generate_thumbnail(self, file_path, width, height) -> Optional[str]:
        """
        Generate a thumbnail for an image file in S3.

        This implementation downloads the fi..."""
```
```python
    async def get_file_url(self, file_path) -> str:
        """
        Get URL for S3 file.

        Args:
            file_path: Relative path to the file

     ..."""
```
```python
    async def initialize(self) -> None:
        """
        Initialize S3 client and create bucket if it doesn't exist.

        Raises:
            St..."""
```
```python
    async def save_file(self, file, destination, media_type, content_type) -> str:
        """
        Save file to S3 storage.

        Args:
            file: The file to upload (UploadFile, f..."""
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
    """
    Get search service instance.

    Args:
        db: Database session

    Returns:
        Sear..."""
```

**Classes:**
```python
class SearchService(object):
    """
    Service for search functionality.

    This service provides methods for searching across diffe..."""
```
*Methods:*
```python
    def __init__(self, db):
        """
        Initialize the search service.

        Args:
            db: Database session
        """
```
```python
    async def get_es_client(self) -> Optional[AsyncElasticsearch]:
        """
        Get Elasticsearch client instance.

        Returns:
            Optional[AsyncElasticsearc..."""
```
```python
    async def global_search(self, search_term, entity_types, page, page_size) -> Dict[(str, Any)]:
        """
        Search across multiple entity types.

        Args:
            search_term: Text to search..."""
```
```python
    async def search_fitments(self, search_term, year, make, model, engine, transmission, page, page_size) -> Dict[(str, Any)]:
        """
        Search for fitments with filtering and pagination.

        Args:
            search_term: ..."""
```
```python
    async def search_products(self, search_term, attributes, is_active, page, page_size, use_elasticsearch) -> Dict[(str, Any)]:
        """
        Search for products with filtering and pagination.

        Args:
            search_term: ..."""
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
    """
    Get vehicle data service instance.

    Args:
        db: Database session

    Returns:
      ..."""
```

**Classes:**
```python
class VehicleDataService(object):
    """
    Service for vehicle data lookups and validation.

    This service provides methods for working..."""
```
*Methods:*
```python
    def __init__(self, db):
        """
        Initialize the vehicle data service.

        Args:
            db: Database session
      ..."""
```
```python
@memory_cache(maxsize=1000, ttl=86400)
    async def decode_vin(self, vin) -> Optional[Dict[(str, Any)]]:
        """
        Decode a Vehicle Identification Number (VIN).

        This method could integrate with an ..."""
```
```python
@redis_cache(prefix='vehicle:engines', ttl=3600)
    async def get_engines(self, make, model, year) -> List[str]:
        """
        Get all available engines, optionally filtered by make, model, and year.

        Args:
   ..."""
```
```python
@redis_cache(prefix='vehicle:makes', ttl=3600)
    async def get_makes(self, year) -> List[str]:
        """
        Get all available makes, optionally filtered by year.

        Args:
            year: Filt..."""
```
```python
@redis_cache(prefix='vehicle:models', ttl=3600)
    async def get_models(self, make, year) -> List[str]:
        """
        Get all available models, optionally filtered by make and year.

        Args:
            ..."""
```
```python
@redis_cache(prefix='vehicle:transmissions', ttl=3600)
    async def get_transmissions(self, make, model, year, engine) -> List[str]:
        """
        Get all available transmissions, optionally filtered.

        Args:
            make: Filt..."""
```
```python
@redis_cache(prefix='vehicle:years', ttl=3600)
    async def get_years(self) -> List[int]:
        """
        Get all available years from fitment data.

        Returns:
            List[int]: Sorted ..."""
```
```python
@memory_cache(maxsize=100, ttl=3600)
    async def standardize_make(self, make) -> str:
        """
        Standardize vehicle make to ensure consistent naming.

        Args:
            make: Vehi..."""
```
```python
@memory_cache(maxsize=100, ttl=3600)
    async def validate_fitment(self, year, make, model, engine, transmission) -> bool:
        """
        Validate if a fitment combination exists.

        Args:
            year: Vehicle year
   ..."""
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
    """
    Analyze chat activity for a room.
    
    Args:
        room_id: The room ID
        time_peri..."""
```

```python
@celery_app.task(bind=True, name='moderate_message_content')
def moderate_message_content(self, message_id, content, sender_id, room_id) -> Dict[(str, Any)]:
    """
    Moderate message content for prohibited content.
    
    Args:
        message_id: The message..."""
```

```python
@celery_app.task(bind=True, name='process_message_notifications')
def process_message_notifications(self, message_id, room_id, sender_id, recipients, message_preview) -> Dict[(str, Any)]:
    """
    Process and send message notifications.
    
    Args:
        message_id: The message ID
     ..."""
```

```python
@celery_app.task(bind=True, name='update_user_presence')
def update_user_presence(self) -> Dict[(str, Any)]:
    """
    Update user presence status based on activity.
    
    This task runs periodically to update u..."""
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
    """
    Initialize currencies in the database.

    Returns:
        Dict[str, Optional[int]]: Result o..."""
```

```python
@shared_task(bind=True, max_retries=3, default_retry_delay=300, autoretry_for=(Exception), retry_backoff=True)
def update_exchange_rates(self) -> Dict[(str, Optional[int])]:
    """
    Update exchange rates from the API.

    Returns:
        Dict[str, Optional[int]]: Result of t..."""
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
    """
    Generate a cache key for a function call.

    Args:
        prefix: Key prefix
        func: F..."""
```

```python
async def get_redis() -> redis.Redis:
    """
    Get Redis client instance.

    Creates a new connection if one doesn't exist.

    Returns:
  ..."""
```

```python
def get_request_cache(request) -> RequestCache:
    """
    Get or create a RequestCache instance for the current request.

    Args:
        request: Fast..."""
```

```python
async def invalidate_cache(prefix, pattern, redis_conn) -> int:
    """
    Invalidate cache keys matching a pattern.

    Args:
        prefix: Cache key prefix
        p..."""
```

```python
def memory_cache(maxsize, ttl) -> Callable[([F], F)]:
    """
    Decorator for in-memory caching with TTL.

    Args:
        maxsize: Maximum cache size
      ..."""
```

```python
def redis_cache(prefix, ttl, skip_args) -> Callable[([F], F)]:
    """
    Decorator for Redis caching.

    Args:
        prefix: Cache key prefix
        ttl: Time-to-l..."""
```

**Classes:**
```python
class RequestCache(object):
    """
    Cache for the current request lifecycle.

    This class provides a way to cache data during a ..."""
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
        """
        Delete value from cache.

        Args:
            key: Cache key
        """
```
```python
    def get(self, key) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
         ..."""
```
```python
    def set(self, key, value) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to c..."""
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
    """
    Decrypt a Fernet-encrypted message.
    
    Args:
        encrypted_message: The encrypted mes..."""
```

```python
def encrypt_message(message) -> str:
    """
    Encrypt a message using Fernet symmetric encryption.
    
    Args:
        message: The plaint..."""
```

```python
def generate_secure_token(length) -> str:
    """
    Generate a cryptographically secure random token.
    
    Args:
        length: The desired le..."""
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
    """
    Create multiple model instances in a single transaction.

    This is more efficient than creat..."""
```

```python
async def create_object(db, model, obj_in) -> T:
    """
    Create a model instance.

    Args:
        db: Database session
        model: Model class
   ..."""
```

```python
async def delete_object(db, model, id) -> bool:
    """
    Delete a model instance by ID.

    Args:
        db: Database session
        model: Model cla..."""
```

```python
async def execute_query(db, query) -> Any:
    """
    Execute a SQLAlchemy query.

    Args:
        db: Database session
        query: SQLAlchemy q..."""
```

```python
async def get_by_id(db, model, id) -> Optional[T]:
    """
    Get a model instance by ID.

    Args:
        db: Database session
        model: Model class
..."""
```

```python
async def paginate(db, query, page, page_size) -> Dict[(str, Any)]:
    """
    Paginate a query.

    Args:
        db: Database session
        query: Base query
        pag..."""
```

```python
@contextlib.asynccontextmanager
async def transaction(db) -> AsyncGenerator[(AsyncSession, None)]:
    """
    Context manager for database transactions.

    This ensures that all operations within the con..."""
```

```python
async def update_object(db, model, id, obj_in) -> Optional[T]:
    """
    Update a model instance by ID.

    Args:
        db: Database session
        model: Model cla..."""
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
    """
    Get the file extension from a filename.

    Args:
        filename: Filename to extract extens..."""
```

```python
def get_file_path(file_path) -> Path:
    """
    Get the absolute path of a file.

    Args:
        file_path: Relative path from media root or..."""
```

```python
def get_file_url(file_path) -> str:
    """
    Get the URL for a file path, taking environment into account.

    Args:
        file_path: Rel..."""
```

```python
def get_media_type_from_mime(mime_type) -> MediaType:
    """
    Determine the media type from MIME type.

    Args:
        mime_type: MIME type of the file

 ..."""
```

```python
def get_thumbnail_path(file_path) -> Optional[Path]:
    """
    Get the thumbnail path for an image.

    Args:
        file_path: Relative path from media roo..."""
```

```python
def is_safe_filename(filename) -> bool:
    """
    Check if a filename is safe to use.

    Validates that the filename doesn't contain any potent..."""
```

```python
def sanitize_filename(filename) -> str:
    """
    Sanitize a filename to be safe for storage.

    Args:
        filename: Original filename

   ..."""
```

```python
def save_upload_file(file, media_id, media_type, is_image) -> Tuple[(str, int, str)]:
    """
    Save an uploaded file to disk.

    Handles saving the file to the appropriate directory and cr..."""
```

```python
def validate_file(file, allowed_types) -> Tuple[(MediaType, bool)]:
    """
    Validate a file for upload.

    Performs various validations on the uploaded file:
    - Filen..."""
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
    """
    Get a value from cache or compute and store it.
    
    Args:
        key: Cache key
        c..."""
```

```python
async def delete_key(key) -> bool:
    """
    Delete a key from Redis.
    
    Args:
        key: Redis key
        
    Returns:
        bo..."""
```

```python
async def get_key(key, default) -> Optional[T]:
    """
    Get a value from Redis.
    
    Args:
        key: Redis key
        default: Default value if..."""
```

```python
async def get_redis_client() -> Redis:
    """
    Get a Redis client using the connection pool.
    
    Returns:
        Redis: Redis client
   ..."""
```

```python
async def get_redis_pool() -> ConnectionPool:
    """
    Get or create the Redis connection pool.
    
    Returns:
        ConnectionPool: Redis connec..."""
```

```python
async def increment_counter(key, amount, ttl) -> Optional[int]:
    """
    Increment a counter in Redis.
    
    Args:
        key: Redis key
        amount: Amount to i..."""
```

```python
async def publish_message(channel, message) -> bool:
    """
    Publish a message to a Redis channel.
    
    Args:
        channel: Redis channel name
      ..."""
```

```python
async def rate_limit_check(key, limit, window) -> tuple[(bool, int)]:
    """
    Check if a rate limit has been exceeded.
    
    Args:
        key: Redis key for the rate lim..."""
```

```python
async def set_key(key, value, ttl) -> bool:
    """
    Set a value in Redis.
    
    Args:
        key: Redis key
        value: Value to store (will..."""
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
*Test configuration and fixtures for pytest.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/conftest.py`

**Imports:**
```python
from __future__ import annotations
import asyncio
from typing import Any, AsyncGenerator, Callable, Dict, Generator, List
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.models.user import User, UserRole, get_password_hash
from app.api.deps import get_db
from app.models.product import Fitment, Product
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
async def admin_token(admin_user) -> str:
    """
    Create an authentication token for admin user.

    This fixture generates a valid JWT token fo..."""
```

```python
@pytest_asyncio.fixture(scope='function')
async def admin_user(db) -> User:
    """
    Create a test admin user.

    This fixture provides an admin user for testing endpoints
    th..."""
```

```python
@pytest_asyncio.fixture(scope='function')
async def client(db) -> AsyncGenerator[(AsyncClient, None)]:
    """
    Create a test client with the database session.

    This fixture overrides the database depend..."""
```

```python
@pytest_asyncio.fixture(scope='function')
async def db(setup_db) -> AsyncGenerator[(AsyncSession, None)]:
    """
    Create a fresh database session for a test.

    This fixture provides an isolated database ses..."""
```

```python
@pytest.fixture(scope='session')
def event_loop() -> Generator[(asyncio.AbstractEventLoop, None, None)]:
    """
    Create an instance of the default event loop for each test case.

    This fixture is required ..."""
```

```python
@pytest_asyncio.fixture(scope='function')
async def normal_user(db) -> User:
    """
    Create a test normal user.

    This fixture provides a regular user for testing endpoints
    ..."""
```

```python
@pytest_asyncio.fixture(scope='session')
async def setup_db() -> AsyncGenerator[(None, None)]:
    """
    Set up test database tables.

    This fixture creates all tables for testing and drops them af..."""
```

```python
@pytest_asyncio.fixture(scope='function')
async def test_fitment(db) -> Fitment:
    """
    Create a test fitment.

    This fixture provides a fitment for testing fitment-related
    fun..."""
```

```python
@pytest_asyncio.fixture(scope='function')
async def test_product(db) -> Product:
    """
    Create a test product.

    This fixture provides a product for testing product-related
    fun..."""
```

```python
@pytest_asyncio.fixture(scope='function')
async def user_token(normal_user) -> str:
    """
    Create an authentication token for normal user.

    This fixture generates a valid JWT token f..."""
```

#### Module: utils
*Testing utilities and helpers.*
Path: `/home/runner/work/Crown-Nexus/Crown-Nexus/backend/tests/utils.py`

**Imports:**
```python
from __future__ import annotations
import json
import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar
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
    """
    Assert that a model instance data matches the provided data.

    Args:
        model: Model in..."""
```

```python
def create_random_email() -> str:
    """
    Create a random email for test data.

    Returns:
        str: Random email address
    """
```

```python
def create_random_string(length) -> str:
    """
    Create a random string for test data.

    Args:
        length: Length of the string to genera..."""
```

```python
async def make_authenticated_request(client, method, url, token, **kwargs) -> Any:
    """
    Make an authenticated request to the API.

    Args:
        client: HTTPX AsyncClient
        ..."""
```

```python
def validate_model_response(response_data, model_type, exclude_fields) -> M:
    """
    Validate that an API response matches a model schema.

    Args:
        response_data: API res..."""
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
    """
    Test retrieving the current user profile.

    Args:
        client: Test client
        normal..."""
```

```python
async def test_get_current_user_unauthorized(client) -> None:
    """
    Test retrieving user profile without authentication.

    Args:
        client: Test client
   ..."""
```

```python
async def test_login_invalid_credentials(client, normal_user) -> None:
    """
    Test login with invalid credentials.

    Args:
        client: Test client
        normal_user..."""
```

```python
async def test_login_success(client, normal_user) -> None:
    """
    Test successful login with valid credentials.

    Args:
        client: Test client
        no..."""
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
    """
    Test creating a product as admin.

    Args:
        client: Test client
        admin_token: A..."""
```

```python
@pytest.mark.asyncio
async def test_create_product_duplicate_sku(client, admin_token, test_product) -> None:
    """
    Test creating a product with a duplicate SKU.

    Args:
        client: Test client
        ad..."""
```

```python
@pytest.mark.asyncio
async def test_create_product_non_admin(client, user_token) -> None:
    """
    Test that non-admin users cannot create products.

    Args:
        client: Test client
      ..."""
```

```python
@pytest.mark.asyncio
async def test_delete_product_admin(client, admin_token, db) -> None:
    """
    Test deleting a product as admin.

    Args:
        client: Test client
        admin_token: A..."""
```

```python
@pytest.mark.asyncio
async def test_delete_product_non_admin(client, user_token, test_product) -> None:
    """
    Test that non-admin users cannot delete products.

    Args:
        client: Test client
      ..."""
```

```python
@pytest.mark.asyncio
async def test_read_product(client, user_token, test_product) -> None:
    """
    Test retrieving a single product.

    Args:
        client: Test client
        user_token: Us..."""
```

```python
@pytest.mark.asyncio
async def test_read_product_not_found(client, user_token) -> None:
    """
    Test retrieving a non-existent product.

    Args:
        client: Test client
        user_tok..."""
```

```python
@pytest.mark.asyncio
async def test_read_products(client, normal_user, user_token, test_product) -> None:
    """
    Test retrieving a list of products.

    Args:
        client: Test client
        normal_user:..."""
```

```python
@pytest.mark.asyncio
async def test_read_products_with_filters(client, admin_token, test_product) -> None:
    """
    Test retrieving products with filters.

    Args:
        client: Test client
        admin_tok..."""
```

```python
@pytest.mark.asyncio
async def test_update_product_admin(client, admin_token, test_product) -> None:
    """
    Test updating a product as admin.

    Args:
        client: Test client
        admin_token: A..."""
```

```python
@pytest.mark.asyncio
async def test_update_product_non_admin(client, user_token, test_product) -> None:
    """
    Test that non-admin users cannot update products.

    Args:
        client: Test client
      ..."""
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
    """
    Test user creation by admin.

    Args:
        client: Test client
        admin_token: Admin ..."""
```

```python
async def test_delete_user_admin(client, admin_token, normal_user) -> None:
    """
    Test deleting a user as admin.

    Args:
        client: Test client
        admin_token: Admi..."""
```

```python
async def test_read_user_by_id_admin(client, admin_token, normal_user) -> None:
    """
    Test retrieving a user by ID as admin.

    Args:
        client: Test client
        admin_tok..."""
```

```python
async def test_read_users_admin(client, admin_user, admin_token, normal_user) -> None:
    """
    Test that admin users can list all users.

    Args:
        client: Test client
        admin_..."""
```

```python
async def test_read_users_non_admin(client, normal_user, user_token) -> None:
    """
    Test that non-admin users cannot list all users.

    Args:
        client: Test client
       ..."""
```

```python
async def test_update_user_admin(client, admin_token, normal_user) -> None:
    """
    Test updating a user as admin.

    Args:
        client: Test client
        admin_token: Admi..."""
```

