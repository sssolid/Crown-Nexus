# Module: app.domains.chat.models

**Path:** `app/domains/chat/models.py`

[Back to Project Index](../../../../index.md)

## Imports
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

## Classes

| Class | Description |
| --- | --- |
| `ChatMember` |  |
| `ChatMemberRole` |  |
| `ChatMessage` |  |
| `ChatRoom` |  |
| `ChatRoomType` |  |
| `MessageReaction` |  |
| `MessageType` |  |
| `RateLimitLog` |  |

### Class: `ChatMember`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'chat_member'` |
| `__table_args__` | `    __table_args__ = (Index("idx_unique_room_user", "room_id", "user_id", unique=True),)` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ChatMemberRole`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `OWNER` | `'owner'` |
| `ADMIN` | `'admin'` |
| `MEMBER` | `'member'` |
| `GUEST` | `'guest'` |

### Class: `ChatMessage`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'chat_message'` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |
| `content` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

##### `content`
```python
@content.setter
def content(self, value) -> None:
```

### Class: `ChatRoom`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'chat_room'` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `ChatRoomType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `DIRECT` | `'direct'` |
| `GROUP` | `'group'` |
| `COMPANY` | `'company'` |
| `SUPPORT` | `'support'` |

### Class: `MessageReaction`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'message_reaction'` |
| `__table_args__` | `    __table_args__ = (
        Index(
            "idx_unique_message_user_reaction",
            "message_id",
            "user_id",
            "reaction",
            unique=True,
        ),
    )` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```

### Class: `MessageType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `TEXT` | `'text'` |
| `IMAGE` | `'image'` |
| `FILE` | `'file'` |
| `SYSTEM` | `'system'` |
| `ACTION` | `'action'` |

### Class: `RateLimitLog`
**Inherits from:** Base

#### Attributes

| Name | Value |
| --- | --- |
| `__tablename__` | `'rate_limit_log'` |

#### Methods

| Method | Description |
| --- | --- |
| `__repr__` |  |

##### `__repr__`
```python
def __repr__(self) -> str:
```
