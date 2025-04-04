# Module: app.domains.chat.repository

**Path:** `app/domains/chat/repository.py`

[Back to Project Index](../../../../index.md)

## Imports
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

## Classes

| Class | Description |
| --- | --- |
| `ChatMemberRepository` |  |
| `ChatMessageRepository` |  |
| `ChatRoomRepository` |  |
| `MessageReactionRepository` |  |

### Class: `ChatMemberRepository`
**Inherits from:** BaseRepository[(ChatMember, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `ensure_exists` `async` |  |
| `find_by_room_and_user` `async` |  |
| `get_by_room` `async` |  |
| `get_by_user` `async` |  |
| `remove_member` `async` |  |
| `update_last_read` `async` |  |
| `update_role` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `ensure_exists`
```python
async def ensure_exists(self, member_id) -> ChatMember:
```

##### `find_by_room_and_user`
```python
async def find_by_room_and_user(self, room_id, user_id) -> Optional[ChatMember]:
```

##### `get_by_room`
```python
async def get_by_room(self, room_id, active_only) -> List[ChatMember]:
```

##### `get_by_user`
```python
async def get_by_user(self, user_id) -> List[ChatMember]:
```

##### `remove_member`
```python
async def remove_member(self, room_id, user_id, removed_by_id) -> bool:
```

##### `update_last_read`
```python
async def update_last_read(self, room_id, user_id, timestamp) -> Optional[ChatMember]:
```

##### `update_role`
```python
async def update_role(self, room_id, user_id, new_role, updated_by_id) -> Optional[ChatMember]:
```

### Class: `ChatMessageRepository`
**Inherits from:** BaseRepository[(ChatMessage, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `check_rate_limit` `async` |  |
| `delete_message` `async` |  |
| `edit_message` `async` |  |
| `ensure_exists` `async` |  |
| `get_room_messages` `async` |  |
| `send_message` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `check_rate_limit`
```python
async def check_rate_limit(self, user_id, room_id, event_type, max_count, window_seconds) -> None:
```

##### `delete_message`
```python
async def delete_message(self, message_id, deleted_by_id) -> Optional[ChatMessage]:
```

##### `edit_message`
```python
async def edit_message(self, message_id, new_content, edited_by_id) -> Optional[ChatMessage]:
```

##### `ensure_exists`
```python
async def ensure_exists(self, message_id) -> ChatMessage:
```

##### `get_room_messages`
```python
async def get_room_messages(self, room_id, limit, before_id, include_deleted) -> List[ChatMessage]:
```

##### `send_message`
```python
async def send_message(self, room_id, sender_id, content, message_type, extra_metadata) -> ChatMessage:
```

### Class: `ChatRoomRepository`
**Inherits from:** BaseRepository[(ChatRoom, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `add_members` `async` |  |
| `create_direct_chat` `async` |  |
| `create_group_chat` `async` |  |
| `ensure_exists` `async` |  |
| `find_direct_chat` `async` |  |
| `get_company_rooms` `async` |  |
| `get_rooms_for_user` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `add_members`
```python
async def add_members(self, room_id, user_ids, role, added_by_id) -> List[ChatMember]:
```

##### `create_direct_chat`
```python
async def create_direct_chat(self, user1_id, user2_id) -> Tuple[(ChatRoom, List[ChatMember])]:
```

##### `create_group_chat`
```python
async def create_group_chat(self, name, creator_id, member_ids, company_id) -> Tuple[(ChatRoom, List[ChatMember])]:
```

##### `ensure_exists`
```python
async def ensure_exists(self, room_id) -> ChatRoom:
```

##### `find_direct_chat`
```python
async def find_direct_chat(self, user1_id, user2_id) -> Optional[ChatRoom]:
```

##### `get_company_rooms`
```python
async def get_company_rooms(self, company_id, page, page_size) -> Dict[(str, Any)]:
```

##### `get_rooms_for_user`
```python
async def get_rooms_for_user(self, user_id, room_type, page, page_size) -> Dict[(str, Any)]:
```

### Class: `MessageReactionRepository`
**Inherits from:** BaseRepository[(MessageReaction, uuid.UUID)]

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `add_reaction` `async` |  |
| `find_by_message_user_reaction` `async` |  |
| `get_by_message` `async` |  |
| `get_reaction_counts` `async` |  |
| `get_user_reactions` `async` |  |
| `remove_reaction` `async` |  |

##### `__init__`
```python
def __init__(self, db) -> None:
```

##### `add_reaction`
```python
async def add_reaction(self, message_id, user_id, reaction) -> MessageReaction:
```

##### `find_by_message_user_reaction`
```python
async def find_by_message_user_reaction(self, message_id, user_id, reaction) -> Optional[MessageReaction]:
```

##### `get_by_message`
```python
async def get_by_message(self, message_id) -> List[MessageReaction]:
```

##### `get_reaction_counts`
```python
async def get_reaction_counts(self, message_id) -> Dict[(str, int)]:
```

##### `get_user_reactions`
```python
async def get_user_reactions(self, message_id, reaction) -> List[uuid.UUID]:
```

##### `remove_reaction`
```python
async def remove_reaction(self, message_id, user_id, reaction) -> bool:
```
