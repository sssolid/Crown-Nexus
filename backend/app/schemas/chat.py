from __future__ import annotations

import uuid

"""Chat schema definitions.

This module defines Pydantic schemas for chat-related objects,
including commands, messages, and responses.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.chat import ChatRoomType, ChatMemberRole, MessageType


class CommandType(str, Enum):
    """Types of WebSocket commands.

    Attributes:
        JOIN_ROOM: Join a chat room.
        LEAVE_ROOM: Leave a chat room.
        SEND_MESSAGE: Send a message to a room.
        READ_MESSAGES: Mark messages as read.
        TYPING_START: Indicate the user started typing.
        TYPING_STOP: Indicate the user stopped typing.
        FETCH_HISTORY: Request message history.
        ADD_REACTION: Add a reaction to a message.
        REMOVE_REACTION: Remove a reaction from a message.
        EDIT_MESSAGE: Edit a message.
        DELETE_MESSAGE: Delete a message.
    """

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


class WebSocketCommand(BaseModel):
    """Base schema for WebSocket commands.

    Attributes:
        command: Type of command.
        room_id: ID of the chat room.
        data: Command-specific data.
    """

    command: CommandType = Field(..., description="Command type")
    room_id: Optional[str] = Field(None, description="Chat room ID")
    data: Dict[str, Any] = Field(default_factory=dict, description="Command data")


class JoinRoomCommand(BaseModel):
    """Schema for joining a chat room.

    Attributes:
        room_id: ID of the room to join.
    """

    room_id: str = Field(..., description="Room ID to join")


class LeaveRoomCommand(BaseModel):
    """Schema for leaving a chat room.

    Attributes:
        room_id: ID of the room to leave.
    """

    room_id: str = Field(..., description="Room ID to leave")


class SendMessageCommand(BaseModel):
    """Schema for sending a message.

    Attributes:
        room_id: ID of the room to send to.
        content: Message content.
        message_type: Type of message.
        extra_metadata: Additional message metadata.
    """

    room_id: str = Field(..., description="Room ID to send to")
    content: str = Field(..., description="Message content")
    message_type: MessageType = Field(MessageType.TEXT, description="Message type")
    extra_metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class ReadMessagesCommand(BaseModel):
    """Schema for marking messages as read.

    Attributes:
        room_id: ID of the room.
        last_read_id: ID of the last read message.
    """

    room_id: str = Field(..., description="Room ID")
    last_read_id: str = Field(..., description="Last read message ID")


class TypingCommand(BaseModel):
    """Schema for typing indicators.

    Attributes:
        room_id: ID of the room.
    """

    room_id: str = Field(..., description="Room ID")


class FetchHistoryCommand(BaseModel):
    """Schema for fetching message history.

    Attributes:
        room_id: ID of the room.
        before_id: ID to fetch messages before.
        limit: Maximum number of messages to fetch.
    """

    room_id: str = Field(..., description="Room ID")
    before_id: Optional[str] = Field(None, description="Fetch messages before this ID")
    limit: int = Field(50, description="Maximum number of messages to fetch")


class ReactionCommand(BaseModel):
    """Schema for message reactions.

    Attributes:
        room_id: ID of the room.
        message_id: ID of the message.
        reaction: Reaction string (e.g., emoji).
    """

    room_id: str = Field(..., description="Room ID")
    message_id: str = Field(..., description="Message ID")
    reaction: str = Field(..., description="Reaction string (e.g., emoji)")


class EditMessageCommand(BaseModel):
    """Schema for editing a message.

    Attributes:
        room_id: ID of the room.
        message_id: ID of the message to edit.
        content: New message content.
    """

    room_id: str = Field(..., description="Room ID")
    message_id: str = Field(..., description="Message ID to edit")
    content: str = Field(..., description="New message content")


class DeleteMessageCommand(BaseModel):
    """Schema for deleting a message.

    Attributes:
        room_id: ID of the room.
        message_id: ID of the message to delete.
    """

    room_id: str = Field(..., description="Room ID")
    message_id: str = Field(..., description="Message ID to delete")


class WebSocketResponse(BaseModel):
    """Schema for WebSocket responses.

    Attributes:
        type: Response type.
        success: Whether the operation was successful.
        error: Error message if not successful.
        data: Response data.
    """

    type: str = Field(..., description="Response type")
    success: bool = Field(True, description="Whether the operation was successful")
    error: Optional[str] = Field(None, description="Error message if not successful")
    data: Dict[str, Any] = Field(default_factory=dict, description="Response data")


class ChatRoomBase(BaseModel):
    """Base schema for ChatRoom data.

    Attributes:
        name: Room name (might be null for direct chats).
        type: Type of chat room.
        company_id: ID of the associated company.
        is_active: Whether the room is active.
        extra_metadata: Additional metadata about the room.
    """

    name: Optional[str] = Field(None, description="Room name")
    type: ChatRoomType = Field(..., description="Room type")
    company_id: Optional[uuid.UUID] = Field(None, description="Associated company ID")
    is_active: bool = Field(True, description="Whether the room is active")
    extra_metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class ChatRoomCreate(ChatRoomBase):
    """Schema for creating a new ChatRoom."""

    pass


class ChatRoomUpdate(BaseModel):
    """Schema for updating an existing ChatRoom.

    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Room name")
    is_active: Optional[bool] = Field(None, description="Whether the room is active")
    extra_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata"
    )


class ChatRoomInDB(ChatRoomBase):
    """Schema for ChatRoom data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class ChatRoom(ChatRoomInDB):
    """Schema for complete ChatRoom data in API responses.

    Includes additional computed fields and related entities.
    """

    member_count: int = Field(0, description="Number of members in the room")
    last_message: Optional[Dict[str, Any]] = Field(
        None, description="Last message in the room"
    )
    company: Optional[Dict[str, Any]] = Field(
        None, description="Associated company details"
    )


class ChatMemberBase(BaseModel):
    """Base schema for ChatMember data.

    Attributes:
        room_id: ID of the chat room.
        user_id: ID of the user.
        role: Member's role in the room.
        is_active: Whether the membership is active.
    """

    room_id: uuid.UUID = Field(..., description="Chat room ID")
    user_id: uuid.UUID = Field(..., description="User ID")
    role: ChatMemberRole = Field(ChatMemberRole.MEMBER, description="Member role")
    is_active: bool = Field(True, description="Whether the membership is active")


class ChatMemberCreate(ChatMemberBase):
    """Schema for creating a new ChatMember."""

    pass


class ChatMemberUpdate(BaseModel):
    """Schema for updating an existing ChatMember.

    All fields are optional to allow partial updates.
    """

    role: Optional[ChatMemberRole] = Field(None, description="Member role")
    is_active: Optional[bool] = Field(
        None, description="Whether the membership is active"
    )
    last_read_at: Optional[datetime] = Field(None, description="Last read timestamp")


class ChatMemberInDB(ChatMemberBase):
    """Schema for ChatMember data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    last_read_at: Optional[datetime] = Field(None, description="Last read timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class ChatMember(ChatMemberInDB):
    """Schema for complete ChatMember data in API responses.

    Includes related entities like user and room details.
    """

    user: Optional[Dict[str, Any]] = Field(None, description="User details")
    room: Optional[Dict[str, Any]] = Field(None, description="Room details")


class ChatMessageBase(BaseModel):
    """Base schema for ChatMessage data.

    Attributes:
        room_id: ID of the chat room.
        sender_id: ID of the message sender.
        message_type: Type of message.
        content: Message content.
        extra_metadata: Additional metadata about the message.
    """

    room_id: uuid.UUID = Field(..., description="Chat room ID")
    sender_id: Optional[uuid.UUID] = Field(None, description="Sender user ID")
    message_type: MessageType = Field(MessageType.TEXT, description="Message type")
    content: str = Field(..., description="Message content")
    extra_metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a new ChatMessage."""

    pass


class ChatMessageUpdate(BaseModel):
    """Schema for updating an existing ChatMessage.

    All fields are optional to allow partial updates.
    """

    content: Optional[str] = Field(None, description="Message content")
    extra_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata"
    )


class ChatMessageInDB(ChatMessageBase):
    """Schema for ChatMessage data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    is_deleted: bool = Field(False, description="Whether the message is deleted")
    deleted_at: Optional[datetime] = Field(
        None, description="When the message was deleted"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class ChatMessage(ChatMessageInDB):
    """Schema for complete ChatMessage data in API responses.

    Includes additional fields like sender information and reactions.
    """

    sender_name: Optional[str] = Field(None, description="Sender name")
    reactions: Dict[str, List[str]] = Field(
        default_factory=dict, description="Message reactions"
    )
    is_edited: bool = Field(False, description="Whether the message has been edited")
    room: Optional[Dict[str, Any]] = Field(None, description="Room details")
    sender: Optional[Dict[str, Any]] = Field(None, description="Sender details")


class MessageReactionBase(BaseModel):
    """Base schema for MessageReaction data.

    Attributes:
        message_id: ID of the message.
        user_id: ID of the user.
        reaction: Reaction string (e.g., emoji).
    """

    message_id: uuid.UUID = Field(..., description="Message ID")
    user_id: uuid.UUID = Field(..., description="User ID")
    reaction: str = Field(..., description="Reaction string (e.g., emoji)")


class MessageReactionCreate(MessageReactionBase):
    """Schema for creating a new MessageReaction."""

    pass


class MessageReactionInDB(MessageReactionBase):
    """Schema for MessageReaction data as stored in the database.

    Includes database-specific fields like ID and timestamps.
    """

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)


class MessageReaction(MessageReactionInDB):
    """Schema for complete MessageReaction data in API responses.

    Includes related entities like user details.
    """

    user: Optional[Dict[str, Any]] = Field(None, description="User details")
    message: Optional[Dict[str, Any]] = Field(None, description="Message details")


class UserPresence(BaseModel):
    """Schema for user presence information.

    Attributes:
        user_id: ID of the user.
        is_online: Whether the user is currently online.
        last_seen_at: When the user was last seen.
        status: Optional custom status message.
    """

    user_id: str = Field(..., description="User ID")
    is_online: bool = Field(..., description="Whether the user is online")
    last_seen_at: Optional[datetime] = Field(
        None, description="When the user was last seen"
    )
    status: Optional[str] = Field(None, description="Custom status message")
