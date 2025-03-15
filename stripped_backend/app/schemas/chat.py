from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
class CommandType(str, Enum):
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
class MessageType(str, Enum):
    TEXT = 'text'
    IMAGE = 'image'
    FILE = 'file'
    SYSTEM = 'system'
    ACTION = 'action'
class WebSocketCommand(BaseModel):
    command: CommandType
    room_id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
class JoinRoomCommand(BaseModel):
    room_id: str
class LeaveRoomCommand(BaseModel):
    room_id: str
class SendMessageCommand(BaseModel):
    room_id: str
    content: str
    message_type: MessageType = MessageType.TEXT
    metadata: Dict[str, Any] = Field(default_factory=dict)
class ReadMessagesCommand(BaseModel):
    room_id: str
    last_read_id: str
class TypingCommand(BaseModel):
    room_id: str
class FetchHistoryCommand(BaseModel):
    room_id: str
    before_id: Optional[str] = None
    limit: int = 50
class ReactionCommand(BaseModel):
    room_id: str
    message_id: str
    reaction: str
class EditMessageCommand(BaseModel):
    room_id: str
    message_id: str
    content: str
class DeleteMessageCommand(BaseModel):
    room_id: str
    message_id: str
class WebSocketResponse(BaseModel):
    type: str
    success: bool = True
    error: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
class ChatRoomSchema(BaseModel):
    id: str
    name: Optional[str] = None
    type: str
    created_at: datetime
    member_count: int
    last_message: Optional[Dict[str, Any]] = None
class ChatMessageSchema(BaseModel):
    id: str
    room_id: str
    sender_id: Optional[str] = None
    sender_name: Optional[str] = None
    message_type: str
    content: str
    reactions: Dict[str, List[str]] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    is_edited: bool = False
    is_deleted: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
class ChatMemberSchema(BaseModel):
    user_id: str
    user_name: str
    role: str
    is_online: bool
    last_seen_at: Optional[datetime] = None
class UserPresenceSchema(BaseModel):
    user_id: str
    is_online: bool
    last_seen_at: Optional[datetime] = None
    status: Optional[str] = None