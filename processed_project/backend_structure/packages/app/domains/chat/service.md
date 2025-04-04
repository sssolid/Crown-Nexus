# Module: app.domains.chat.service

**Path:** `app/domains/chat/service.py`

[Back to Project Index](../../../../index.md)

## Imports
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
| `add_member` `async` |  |
| `add_reaction` `async` |  |
| `check_message_permission` `async` |  |
| `check_room_access` `async` |  |
| `create_direct_chat` `async` |  |
| `create_message` `async` |  |
| `create_room` `async` |  |
| `delete_message` `async` |  |
| `edit_message` `async` |  |
| `find_direct_chat` `async` |  |
| `get_message_history` `async` |  |
| `get_room` `async` |  |
| `get_room_info` `async` |  |
| `get_room_with_members` `async` |  |
| `get_unread_count` `async` |  |
| `get_user_rooms` `async` |  |
| `mark_as_read` `async` |  |
| `register` |  |
| `remove_member` `async` |  |
| `remove_reaction` `async` |  |
| `update_member_role` `async` |  |

##### `__init__`
```python
def __init__(self, db):
```

##### `add_member`
```python
async def add_member(self, room_id, user_id, role) -> bool:
```

##### `add_reaction`
```python
async def add_reaction(self, message_id, user_id, reaction) -> bool:
```

##### `check_message_permission`
```python
async def check_message_permission(self, message_id, user_id, require_admin) -> bool:
```

##### `check_room_access`
```python
async def check_room_access(self, user_id, room_id) -> bool:
```

##### `create_direct_chat`
```python
async def create_direct_chat(self, user_id1, user_id2) -> str:
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

##### `find_direct_chat`
```python
async def find_direct_chat(self, user_id1, user_id2) -> Optional[str]:
```

##### `get_message_history`
```python
async def get_message_history(self, room_id, before_id, limit) -> List[Dict[(str, Any)]]:
```

##### `get_room`
```python
async def get_room(self, room_id) -> Optional[ChatRoom]:
```

##### `get_room_info`
```python
async def get_room_info(self, room_id) -> Dict[(str, Any)]:
```

##### `get_room_with_members`
```python
async def get_room_with_members(self, room_id) -> Optional[ChatRoom]:
```

##### `get_unread_count`
```python
async def get_unread_count(self, room_id, user_id, last_read_at) -> int:
```

##### `get_user_rooms`
```python
async def get_user_rooms(self, user_id) -> List[Dict[(str, Any)]]:
```

##### `mark_as_read`
```python
async def mark_as_read(self, user_id, room_id, last_read_id) -> bool:
```

##### `register`
```python
@classmethod
def register(cls) -> None:
```

##### `remove_member`
```python
async def remove_member(self, room_id, user_id) -> bool:
```

##### `remove_reaction`
```python
async def remove_reaction(self, message_id, user_id, reaction) -> bool:
```

##### `update_member_role`
```python
async def update_member_role(self, room_id, user_id, role) -> bool:
```
