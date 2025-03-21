# Module: app.services.chat

**Path:** `app/services/chat.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from sqlalchemy import and_, desc, func, or_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.core.cache.decorators import cached
from app.core.exceptions import AuthenticationException, BusinessException, ResourceNotFoundException, ValidationException, ErrorCode
from app.core.logging import get_logger
from app.db.session import get_db_context
from app.models.chat import ChatMember, ChatMemberRole, ChatMessage, ChatRoom, ChatRoomType, MessageReaction, MessageType
from app.models.user import User
from app.utils.crypto import decrypt_message, encrypt_message
```

## Global Variables
```python
logger = logger = get_logger("app.services.chat")
```

## Classes

| Class | Description |
| --- | --- |
| `ChatService` |  |

### Class: `ChatService`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `check_message_permission` `async` |  |
| `check_room_access` `async` |  |
| `create_message` `async` |  |
| `create_room` `async` |  |
| `delete_message` `async` |  |
| `edit_message` `async` |  |
| `get_message_history` `async` |  |
| `get_room` `async` |  |
| `get_room_with_members` `async` |  |
| `register` |  |

##### `__init__`
```python
def __init__(self, db):
```

##### `check_message_permission`
```python
async def check_message_permission(self, message_id, user_id, require_admin) -> bool:
```

##### `check_room_access`
```python
async def check_room_access(self, user_id, room_id) -> bool:
```

##### `create_message`
```python
async def create_message(self, room_id, sender_id, content, message_type, metadata) -> ChatMessage:
```

##### `create_room`
```python
async def create_room(self, name, room_type, creator_id, company_id, members) -> ChatRoom:
```

##### `delete_message`
```python
async def delete_message(self, message_id) -> bool:
```

##### `edit_message`
```python
async def edit_message(self, message_id, content) -> Tuple[(bool, Optional[ChatMessage])]:
```

##### `get_message_history`
```python
@cached(prefix='chat:messages', ttl=60, backend='redis')
async def get_message_history(self, room_id, before_id, limit) -> List[Dict[(str, Any)]]:
```

##### `get_room`
```python
@cached(prefix='chat:room', ttl=300, backend='redis')
async def get_room(self, room_id) -> Optional[ChatRoom]:
```

##### `get_room_with_members`
```python
async def get_room_with_members(self, room_id) -> Optional[ChatRoom]:
```

##### `register`
```python
@classmethod
def register(cls) -> None:
```
