# Module: app.api.v1.endpoints.chat

**Path:** `app/api/v1/endpoints/chat.py`

[Back to Project Index](../../../../../index.md)

## Imports
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

## Global Variables
```python
router = router = APIRouter()
logger = logger = get_logger("app.api.v1.endpoints.chat")
```

## Functions

| Function | Description |
| --- | --- |
| `add_reaction` |  |
| `add_room_member` |  |
| `create_direct_chat` |  |
| `create_message` |  |
| `create_room` |  |
| `delete_message` |  |
| `edit_message` |  |
| `get_room` |  |
| `get_room_messages` |  |
| `get_rooms` |  |
| `remove_reaction` |  |
| `remove_room_member` |  |
| `update_room_member` |  |

### `add_reaction`
```python
@router.post('/rooms/{room_id}/messages/{message_id}/reactions')
@log_execution_time(logger)
async def add_reaction(room_id, message_id, request, db, current_user) -> Response:
```

### `add_room_member`
```python
@router.post('/rooms/{room_id}/members')
@log_execution_time(logger)
async def add_room_member(room_id, request, db, current_user) -> Response:
```

### `create_direct_chat`
```python
@router.post('/direct-chats')
@log_execution_time(logger)
async def create_direct_chat(request, db, current_user) -> Response:
```

### `create_message`
```python
@router.post('/rooms/{room_id}/messages')
@log_execution_time(logger)
async def create_message(room_id, request, db, current_user) -> Response:
```

### `create_room`
```python
@router.post('/rooms', status_code=status.HTTP_201_CREATED)
@log_execution_time(logger)
async def create_room(request, db, current_user) -> Response:
```

### `delete_message`
```python
@router.delete('/rooms/{room_id}/messages/{message_id}')
@log_execution_time(logger)
async def delete_message(room_id, message_id, db, current_user) -> Response:
```

### `edit_message`
```python
@router.put('/rooms/{room_id}/messages/{message_id}')
@log_execution_time(logger)
async def edit_message(room_id, message_id, request, db, current_user) -> Response:
```

### `get_room`
```python
@router.get('/rooms/{room_id}')
@log_execution_time(logger)
async def get_room(room_id, db, current_user) -> Response:
```

### `get_room_messages`
```python
@router.get('/rooms/{room_id}/messages')
@log_execution_time(logger)
async def get_room_messages(room_id, before_id, limit, db, current_user) -> Response:
```

### `get_rooms`
```python
@router.get('/rooms')
@log_execution_time(logger)
async def get_rooms(db, current_user) -> Response:
```

### `remove_reaction`
```python
@router.delete('/rooms/{room_id}/messages/{message_id}/reactions/{reaction}')
@log_execution_time(logger)
async def remove_reaction(room_id, message_id, reaction, db, current_user) -> Response:
```

### `remove_room_member`
```python
@router.delete('/rooms/{room_id}/members/{user_id}')
@log_execution_time(logger)
async def remove_room_member(room_id, user_id, db, current_user) -> Response:
```

### `update_room_member`
```python
@router.put('/rooms/{room_id}/members/{user_id}')
@log_execution_time(logger)
async def update_room_member(room_id, user_id, request, db, current_user) -> Response:
```

## Classes

| Class | Description |
| --- | --- |
| `AddMemberRequest` |  |
| `CreateDirectChatRequest` |  |
| `CreateMessageRequest` |  |
| `CreateRoomRequest` |  |
| `EditMessageRequest` |  |
| `ReactionRequest` |  |
| `UpdateMemberRequest` |  |

### Class: `AddMemberRequest`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_role` |  |

##### `validate_role`
```python
@validator('role')
def validate_role(self, v) -> str:
```

### Class: `CreateDirectChatRequest`
**Inherits from:** BaseModel

### Class: `CreateMessageRequest`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_message_type` |  |

##### `validate_message_type`
```python
@validator('message_type')
def validate_message_type(self, v) -> str:
```

### Class: `CreateRoomRequest`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_type` |  |

##### `validate_type`
```python
@validator('type')
def validate_type(self, v) -> str:
```

### Class: `EditMessageRequest`
**Inherits from:** BaseModel

### Class: `ReactionRequest`
**Inherits from:** BaseModel

### Class: `UpdateMemberRequest`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `validate_role` |  |

##### `validate_role`
```python
@validator('role')
def validate_role(self, v) -> str:
```
