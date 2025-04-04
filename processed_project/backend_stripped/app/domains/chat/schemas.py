from __future__ import annotations
import uuid
'Chat schema definitions.\n\nThis module defines Pydantic schemas for chat-related objects,\nincluding commands, messages, and responses.\n'
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.chat.models import ChatRoomType, ChatMemberRole, MessageType
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
class WebSocketCommand(BaseModel):
    command: CommandType = Field(..., description='Command type')
    room_id: Optional[str] = Field(None, description='Chat room ID')
    data: Dict[str, Any] = Field(default_factory=dict, description='Command data')
class JoinRoomCommand(BaseModel):
    room_id: str = Field(..., description='Room ID to join')
class LeaveRoomCommand(BaseModel):
    room_id: str = Field(..., description='Room ID to leave')
class SendMessageCommand(BaseModel):
    room_id: str = Field(..., description='Room ID to send to')
    content: str = Field(..., description='Message content')
    message_type: MessageType = Field(MessageType.TEXT, description='Message type')
    extra_metadata: Dict[str, Any] = Field(default_factory=dict, description='Additional metadata')
class ReadMessagesCommand(BaseModel):
    room_id: str = Field(..., description='Room ID')
    last_read_id: str = Field(..., description='Last read message ID')
class TypingCommand(BaseModel):
    room_id: str = Field(..., description='Room ID')
class FetchHistoryCommand(BaseModel):
    room_id: str = Field(..., description='Room ID')
    before_id: Optional[str] = Field(None, description='Fetch messages before this ID')
    limit: int = Field(50, description='Maximum number of messages to fetch')
class ReactionCommand(BaseModel):
    room_id: str = Field(..., description='Room ID')
    message_id: str = Field(..., description='Message ID')
    reaction: str = Field(..., description='Reaction string (e.g., emoji)')
class EditMessageCommand(BaseModel):
    room_id: str = Field(..., description='Room ID')
    message_id: str = Field(..., description='Message ID to edit')
    content: str = Field(..., description='New message content')
class DeleteMessageCommand(BaseModel):
    room_id: str = Field(..., description='Room ID')
    message_id: str = Field(..., description='Message ID to delete')
class WebSocketResponse(BaseModel):
    type: str = Field(..., description='Response type')
    success: bool = Field(True, description='Whether the operation was successful')
    error: Optional[str] = Field(None, description='Error message if not successful')
    data: Dict[str, Any] = Field(default_factory=dict, description='Response data')
class ChatRoomBase(BaseModel):
    name: Optional[str] = Field(None, description='Room name')
    type: ChatRoomType = Field(..., description='Room type')
    company_id: Optional[uuid.UUID] = Field(None, description='Associated company ID')
    is_active: bool = Field(True, description='Whether the room is active')
    extra_metadata: Dict[str, Any] = Field(default_factory=dict, description='Additional metadata')
class ChatRoomCreate(ChatRoomBase):
    pass
class ChatRoomUpdate(BaseModel):
    name: Optional[str] = Field(None, description='Room name')
    is_active: Optional[bool] = Field(None, description='Whether the room is active')
    extra_metadata: Optional[Dict[str, Any]] = Field(None, description='Additional metadata')
class ChatRoomInDB(ChatRoomBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class ChatRoom(ChatRoomInDB):
    member_count: int = Field(0, description='Number of members in the room')
    last_message: Optional[Dict[str, Any]] = Field(None, description='Last message in the room')
    company: Optional[Dict[str, Any]] = Field(None, description='Associated company details')
class ChatMemberBase(BaseModel):
    room_id: uuid.UUID = Field(..., description='Chat room ID')
    user_id: uuid.UUID = Field(..., description='User ID')
    role: ChatMemberRole = Field(ChatMemberRole.MEMBER, description='Member role')
    is_active: bool = Field(True, description='Whether the membership is active')
class ChatMemberCreate(ChatMemberBase):
    pass
class ChatMemberUpdate(BaseModel):
    role: Optional[ChatMemberRole] = Field(None, description='Member role')
    is_active: Optional[bool] = Field(None, description='Whether the membership is active')
    last_read_at: Optional[datetime] = Field(None, description='Last read timestamp')
class ChatMemberInDB(ChatMemberBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    last_read_at: Optional[datetime] = Field(None, description='Last read timestamp')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class ChatMember(ChatMemberInDB):
    user: Optional[Dict[str, Any]] = Field(None, description='User details')
    room: Optional[Dict[str, Any]] = Field(None, description='Room details')
class ChatMessageBase(BaseModel):
    room_id: uuid.UUID = Field(..., description='Chat room ID')
    sender_id: Optional[uuid.UUID] = Field(None, description='Sender user ID')
    message_type: MessageType = Field(MessageType.TEXT, description='Message type')
    content: str = Field(..., description='Message content')
    extra_metadata: Dict[str, Any] = Field(default_factory=dict, description='Additional metadata')
class ChatMessageCreate(ChatMessageBase):
    pass
class ChatMessageUpdate(BaseModel):
    content: Optional[str] = Field(None, description='Message content')
    extra_metadata: Optional[Dict[str, Any]] = Field(None, description='Additional metadata')
class ChatMessageInDB(ChatMessageBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    is_deleted: bool = Field(False, description='Whether the message is deleted')
    deleted_at: Optional[datetime] = Field(None, description='When the message was deleted')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class ChatMessage(ChatMessageInDB):
    sender_name: Optional[str] = Field(None, description='Sender name')
    reactions: Dict[str, List[str]] = Field(default_factory=dict, description='Message reactions')
    is_edited: bool = Field(False, description='Whether the message has been edited')
    room: Optional[Dict[str, Any]] = Field(None, description='Room details')
    sender: Optional[Dict[str, Any]] = Field(None, description='Sender details')
class MessageReactionBase(BaseModel):
    message_id: uuid.UUID = Field(..., description='Message ID')
    user_id: uuid.UUID = Field(..., description='User ID')
    reaction: str = Field(..., description='Reaction string (e.g., emoji)')
class MessageReactionCreate(MessageReactionBase):
    pass
class MessageReactionInDB(MessageReactionBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    created_at: datetime = Field(..., description='Creation timestamp')
    model_config = ConfigDict(from_attributes=True)
class MessageReaction(MessageReactionInDB):
    user: Optional[Dict[str, Any]] = Field(None, description='User details')
    message: Optional[Dict[str, Any]] = Field(None, description='Message details')
class UserPresence(BaseModel):
    user_id: str = Field(..., description='User ID')
    is_online: bool = Field(..., description='Whether the user is online')
    last_seen_at: Optional[datetime] = Field(None, description='When the user was last seen')
    status: Optional[str] = Field(None, description='Custom status message')