# backend/app/schemas/chat.py
"""
Chat system Pydantic schemas.

This module defines the Pydantic models for chat data validation:
- WebSocket commands and responses
- Chat room data
- Message formats
- User presence and status

These schemas ensure consistent data structures throughout the chat system.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CommandType(str, Enum):
    """WebSocket command types."""
    JOIN_ROOM = "join_room"
    LEAVE_ROOM = "leave_room"
    SEND_MESSAGE = "send_message"
    READ_MESSAGES = "read_messages"
    TYPING_START = "typing_start"
    TYPING_STOP = "typing_stop"
    FETCH_HISTORY = "fetch_history"
    ADD_REACTION = "add_reaction"
    REMOVE_REACTION = "remove_reaction"
    EDIT_MESSAGE = "edit_message"
    DELETE_MESSAGE = "delete_message"


class MessageType(str, Enum):
    """Message content types."""
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"
    ACTION = "action"


class WebSocketCommand(BaseModel):
    """
    Base WebSocket command structure.

    This model defines the common structure for all WebSocket commands:
    - Command type to identify the action
    - Optional room identifier
    - Command data with type-specific content
    """
    command: CommandType
    room_id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)


class JoinRoomCommand(BaseModel):
    """
    Command to join a chat room.

    Attributes:
        room_id: Room identifier
    """
    room_id: str


class LeaveRoomCommand(BaseModel):
    """
    Command to leave a chat room.

    Attributes:
        room_id: Room identifier
    """
    room_id: str


class SendMessageCommand(BaseModel):
    """
    Command to send a message.

    Attributes:
        room_id: Room identifier
        content: Message content
        message_type: Type of message (text, image, etc.)
        metadata: Additional message data
    """
    room_id: str
    content: str
    message_type: MessageType = MessageType.TEXT
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ReadMessagesCommand(BaseModel):
    """
    Command to mark messages as read.

    Attributes:
        room_id: Room identifier
        last_read_id: ID of the last read message
    """
    room_id: str
    last_read_id: str


class TypingCommand(BaseModel):
    """
    Command for typing indicators.

    Attributes:
        room_id: Room identifier
    """
    room_id: str


class FetchHistoryCommand(BaseModel):
    """
    Command to fetch message history.

    Attributes:
        room_id: Room identifier
        before_id: Fetch messages before this ID
        limit: Maximum number of messages to return
    """
    room_id: str
    before_id: Optional[str] = None
    limit: int = 50


class ReactionCommand(BaseModel):
    """
    Command for message reactions.

    Attributes:
        room_id: Room identifier
        message_id: Message identifier
        reaction: Reaction content
    """
    room_id: str
    message_id: str
    reaction: str


class EditMessageCommand(BaseModel):
    """
    Command to edit a message.

    Attributes:
        room_id: Room identifier
        message_id: Message identifier
        content: New message content
    """
    room_id: str
    message_id: str
    content: str


class DeleteMessageCommand(BaseModel):
    """
    Command to delete a message.

    Attributes:
        room_id: Room identifier
        message_id: Message identifier
    """
    room_id: str
    message_id: str


class WebSocketResponse(BaseModel):
    """
    Base WebSocket response structure.

    This model defines the common structure for all WebSocket responses:
    - Response type for client handling
    - Optional error information
    - Response data with type-specific content
    """
    type: str
    success: bool = True
    error: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)


class ChatRoomSchema(BaseModel):
    """
    Chat room information schema.

    Attributes:
        id: Room identifier
        name: Room name
        type: Room type
        created_at: Creation timestamp
        member_count: Number of members in the room
        last_message: Last message information (optional)
    """
    id: str
    name: Optional[str] = None
    type: str
    created_at: datetime
    member_count: int
    last_message: Optional[Dict[str, Any]] = None


class ChatMessageSchema(BaseModel):
    """
    Chat message schema.

    Attributes:
        id: Message identifier
        room_id: Room identifier
        sender_id: Sender user identifier
        sender_name: Sender display name
        message_type: Type of message
        content: Message content
        reactions: Message reactions
        created_at: Creation timestamp
        updated_at: Last update timestamp
        is_edited: Whether the message has been edited
        is_deleted: Whether the message has been deleted
    """
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
    """
    Chat room member schema.

    Attributes:
        user_id: User identifier
        user_name: User display name
        role: Member role in the room
        is_online: Whether the user is currently online
        last_seen_at: When the user was last active
    """
    user_id: str
    user_name: str
    role: str
    is_online: bool
    last_seen_at: Optional[datetime] = None


class UserPresenceSchema(BaseModel):
    """
    User presence information schema.

    Attributes:
        user_id: User identifier
        is_online: Whether the user is currently online
        last_seen_at: When the user was last active
        status: Custom status message
    """
    user_id: str
    is_online: bool
    last_seen_at: Optional[datetime] = None
    status: Optional[str] = None
