# backend/app/models/chat.py
"""
Chat system models.

This module defines the models for the real-time chat system:
- Chat rooms
- Chat messages with encryption
- Chat members and permissions
- Rate limiting data

These models provide a comprehensive structure for secure, real-time
messaging within the B2B platform.
"""

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

# For type hints only, not runtime imports
if TYPE_CHECKING:
    from app.models.user import User


class ChatRoomType(str, Enum):
    """
    Types of chat rooms supported by the system.

    Defines the possible chat room configurations:
    - DIRECT: One-to-one chat between two users
    - GROUP: Group chat for multiple users
    - COMPANY: Company-wide chat room
    - SUPPORT: Customer support chat
    """

    DIRECT = "direct"
    GROUP = "group"
    COMPANY = "company"
    SUPPORT = "support"


class ChatRoom(Base):
    """
    Chat room model representing a conversation space.

    This model defines a chat room where users can exchange messages:
    - Each room has a type (direct, group, etc.)
    - Rooms can be associated with a company
    - Messages are linked to rooms
    - Members track participants in the room

    Attributes:
        id: Primary key UUID
        name: Room name (optional for direct chats)
        type: Room type (direct, group, company, support)
        company_id: Associated company (optional)
        is_active: Whether the room is active
        metadata: Additional room data as JSON
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "chat_room"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    type: Mapped[ChatRoomType] = mapped_column(String(20), nullable=False, index=True)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id"), nullable=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true(), nullable=False
    )
    metadata: Mapped[Dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=expression.text("'{}'::jsonb"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    company = relationship("Company", back_populates="chat_rooms")
    messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="room", cascade="all, delete-orphan"
    )
    members: Mapped[List["ChatMember"]] = relationship(
        "ChatMember", back_populates="room", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of the chat room."""
        return f"<ChatRoom {self.id}: {self.name or '(Direct)'} ({self.type})>"


class ChatMemberRole(str, Enum):
    """
    Roles of chat room members.

    Defines the possible roles a user can have in a chat room:
    - OWNER: Creator/owner with full permissions
    - ADMIN: Administrator with moderation rights
    - MEMBER: Regular participant
    - GUEST: Temporary participant with limited rights
    """

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


class ChatMember(Base):
    """
    Chat room member model.

    This model tracks users' membership in chat rooms:
    - Each member has a role (owner, admin, etc.)
    - Tracks when the user last read messages
    - Records membership status

    Attributes:
        id: Primary key UUID
        room_id: Reference to chat room
        user_id: Reference to user
        role: Member role (owner, admin, member, guest)
        last_read_at: When the user last read messages
        is_active: Whether the membership is active
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "chat_member"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chat_room.id"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True
    )
    role: Mapped[ChatMemberRole] = mapped_column(
        String(20), nullable=False, default=ChatMemberRole.MEMBER
    )
    last_read_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    room: Mapped["ChatRoom"] = relationship("ChatRoom", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="chat_memberships")

    # Ensure a user can only be a member of a specific room once
    __table_args__ = (Index("idx_unique_room_user", "room_id", "user_id", unique=True),)

    def __repr__(self) -> str:
        """String representation of the chat member."""
        return f"<ChatMember {self.id}: User {self.user_id} in Room {self.room_id} ({self.role})>"


class MessageType(str, Enum):
    """
    Types of messages supported by the chat system.

    Defines the possible message types:
    - TEXT: Regular text message
    - IMAGE: Image attachment
    - FILE: File attachment
    - SYSTEM: System-generated message
    - ACTION: User action notification
    """

    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"
    ACTION = "action"


class ChatMessage(Base):
    """
    Chat message model.

    This model represents individual messages in chat rooms:
    - Messages support various types (text, image, etc.)
    - Content is encrypted for security
    - Tracks message status (sent, delivered, read)

    Attributes:
        id: Primary key UUID
        room_id: Reference to chat room
        sender_id: Reference to sender user
        message_type: Type of message (text, image, file, system, action)
        content_encrypted: Encrypted message content
        metadata: Additional message metadata as JSON
        is_deleted: Whether the message has been deleted
        deleted_at: When the message was deleted
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __tablename__ = "chat_message"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chat_room.id"), nullable=False, index=True
    )
    sender_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=True, index=True
    )
    message_type: Mapped[MessageType] = mapped_column(
        String(20), nullable=False, default=MessageType.TEXT
    )
    content_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[Dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=expression.text("'{}'::jsonb"),
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=expression.false(), nullable=False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    room: Mapped["ChatRoom"] = relationship("ChatRoom", back_populates="messages")
    sender: Mapped[Optional["User"]] = relationship("User")
    reactions: Mapped[List["MessageReaction"]] = relationship(
        "MessageReaction", back_populates="message", cascade="all, delete-orphan"
    )

    @property
    def content(self) -> str:
        """Decrypt and return the message content."""
        return decrypt_message(self.content_encrypted)

    @content.setter
    def content(self, value: str) -> None:
        """Encrypt and store the message content."""
        self.content_encrypted = encrypt_message(value)

    def __repr__(self) -> str:
        """String representation of the chat message."""
        return f"<ChatMessage {self.id}: {self.message_type} in Room {self.room_id}>"


class MessageReaction(Base):
    """
    Message reaction model.

    This model tracks reactions to messages (like emoji reactions):
    - Each reaction is associated with a specific message
    - Users can react with emoji or predefined reactions
    - Multiple users can add the same reaction

    Attributes:
        id: Primary key UUID
        message_id: Reference to chat message
        user_id: Reference to user who reacted
        reaction: Reaction content (emoji or predefined reaction)
        created_at: Creation timestamp
    """

    __tablename__ = "message_reaction"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chat_message.id"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True
    )
    reaction: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    message: Mapped["ChatMessage"] = relationship(
        "ChatMessage", back_populates="reactions"
    )
    user: Mapped["User"] = relationship("User")

    # Ensure a user can only react once with the same reaction to a message
    __table_args__ = (
        Index(
            "idx_unique_message_user_reaction",
            "message_id",
            "user_id",
            "reaction",
            unique=True,
        ),
    )

    def __repr__(self) -> str:
        """String representation of the message reaction."""
        return f"<MessageReaction {self.id}: {self.reaction} from User {self.user_id}>"


class RateLimitLog(Base):
    """
    Rate limiting log model.

    This model tracks rate limiting for users to prevent spam:
    - Records user's message sending attempts
    - Used to enforce rate limits on messaging
    - Supports both global and room-specific limits

    Attributes:
        id: Primary key UUID
        user_id: Reference to user
        room_id: Reference to chat room (optional)
        event_type: Type of event being rate limited
        timestamp: When the event occurred
        count: Number of events in the current period
    """

    __tablename__ = "rate_limit_log"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True
    )
    room_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chat_room.id"), nullable=True, index=True
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Relationships
    user: Mapped["User"] = relationship("User")
    room: Mapped[Optional["ChatRoom"]] = relationship("ChatRoom")

    def __repr__(self) -> str:
        """String representation of the rate limit log."""
        return f"<RateLimitLog {self.id}: User {self.user_id} - {self.event_type} ({self.count})>"
