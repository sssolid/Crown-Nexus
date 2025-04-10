# Module: app.domains.chat.schemas

**Path:** `app/domains/chat/schemas.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.chat.models import ChatRoomType, ChatMemberRole, MessageType
```

## Classes

| Class | Description |
| --- | --- |
| `ChatMember` |  |
| `ChatMemberBase` |  |
| `ChatMemberCreate` |  |
| `ChatMemberInDB` |  |
| `ChatMemberUpdate` |  |
| `ChatMessage` |  |
| `ChatMessageBase` |  |
| `ChatMessageCreate` |  |
| `ChatMessageInDB` |  |
| `ChatMessageUpdate` |  |
| `ChatRoom` |  |
| `ChatRoomBase` |  |
| `ChatRoomCreate` |  |
| `ChatRoomInDB` |  |
| `ChatRoomUpdate` |  |
| `CommandType` |  |
| `DeleteMessageCommand` |  |
| `EditMessageCommand` |  |
| `FetchHistoryCommand` |  |
| `JoinRoomCommand` |  |
| `LeaveRoomCommand` |  |
| `MessageReaction` |  |
| `MessageReactionBase` |  |
| `MessageReactionCreate` |  |
| `MessageReactionInDB` |  |
| `ReactionCommand` |  |
| `ReadMessagesCommand` |  |
| `SendMessageCommand` |  |
| `TypingCommand` |  |
| `UserPresence` |  |
| `WebSocketCommand` |  |
| `WebSocketResponse` |  |

### Class: `ChatMember`
**Inherits from:** ChatMemberInDB

### Class: `ChatMemberBase`
**Inherits from:** BaseModel

### Class: `ChatMemberCreate`
**Inherits from:** ChatMemberBase

### Class: `ChatMemberInDB`
**Inherits from:** ChatMemberBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ChatMemberUpdate`
**Inherits from:** BaseModel

### Class: `ChatMessage`
**Inherits from:** ChatMessageInDB

### Class: `ChatMessageBase`
**Inherits from:** BaseModel

### Class: `ChatMessageCreate`
**Inherits from:** ChatMessageBase

### Class: `ChatMessageInDB`
**Inherits from:** ChatMessageBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ChatMessageUpdate`
**Inherits from:** BaseModel

### Class: `ChatRoom`
**Inherits from:** ChatRoomInDB

### Class: `ChatRoomBase`
**Inherits from:** BaseModel

### Class: `ChatRoomCreate`
**Inherits from:** ChatRoomBase

### Class: `ChatRoomInDB`
**Inherits from:** ChatRoomBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ChatRoomUpdate`
**Inherits from:** BaseModel

### Class: `CommandType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `JOIN_ROOM` | `'join_room'` |
| `LEAVE_ROOM` | `'leave_room'` |
| `SEND_MESSAGE` | `'send_message'` |
| `READ_MESSAGES` | `'read_messages'` |
| `TYPING_START` | `'typing_start'` |
| `TYPING_STOP` | `'typing_stop'` |
| `FETCH_HISTORY` | `'fetch_history'` |
| `ADD_REACTION` | `'add_reaction'` |
| `REMOVE_REACTION` | `'remove_reaction'` |
| `EDIT_MESSAGE` | `'edit_message'` |
| `DELETE_MESSAGE` | `'delete_message'` |

### Class: `DeleteMessageCommand`
**Inherits from:** BaseModel

### Class: `EditMessageCommand`
**Inherits from:** BaseModel

### Class: `FetchHistoryCommand`
**Inherits from:** BaseModel

### Class: `JoinRoomCommand`
**Inherits from:** BaseModel

### Class: `LeaveRoomCommand`
**Inherits from:** BaseModel

### Class: `MessageReaction`
**Inherits from:** MessageReactionInDB

### Class: `MessageReactionBase`
**Inherits from:** BaseModel

### Class: `MessageReactionCreate`
**Inherits from:** MessageReactionBase

### Class: `MessageReactionInDB`
**Inherits from:** MessageReactionBase

#### Attributes

| Name | Value |
| --- | --- |
| `model_config` | `    model_config = ConfigDict(from_attributes=True)` |

### Class: `ReactionCommand`
**Inherits from:** BaseModel

### Class: `ReadMessagesCommand`
**Inherits from:** BaseModel

### Class: `SendMessageCommand`
**Inherits from:** BaseModel

### Class: `TypingCommand`
**Inherits from:** BaseModel

### Class: `UserPresence`
**Inherits from:** BaseModel

### Class: `WebSocketCommand`
**Inherits from:** BaseModel

### Class: `WebSocketResponse`
**Inherits from:** BaseModel
