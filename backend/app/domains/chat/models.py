from __future__ import annotations

"""Chat model definition.

This module defines the Chat models and related enums for
messaging functionality within the application.
"""

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

if TYPE_CHECKING:
    from app.domains.users.models import User
    from app.domains.company.schemas import Company


class ChatRoomType(str, Enum):
    """Types of chat rooms.

    Attributes:
        DIRECT: One-to-one chat between two users.
        GROUP: Group chat with multiple users.
        COMPANY: Company-wide chat.
        SUPPORT: Support chat with customer service.
    """

    DIRECT = "direct"
    GROUP = "group"
    COMPANY = "company"
    SUPPORT = "support"


class ChatRoom(Base):
    """Chat room entity representing a conversation space.

    Attributes:
        id: Unique identifier.
        name: Optional room name (might be null for direct chats).
        type: Type of chat room.
        company_id: ID of the associated company.
        is_active: Whether the room is active.
        extra_metadata: Additional metadata about the room.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
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
    extra_metadata: Mapped[Dict] = mapped_column(
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
    company: Mapped[Optional["Company"]] = relationship(
        "Company", back_populates="chat_rooms"
    )
    messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="room", cascade="all, delete-orphan"
    )
    members: Mapped[List["ChatMember"]] = relationship(
        "ChatMember", back_populates="room", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Return string representation of ChatRoom instance.

        Returns:
            String representation including id, name, and type.
        """
        return f"<ChatRoom {self.id}: {self.name or '(Direct)'} ({self.type})>"


class ChatMemberRole(str, Enum):
    """Roles of chat room members.

    Attributes:
        OWNER: Room owner with full control.
        ADMIN: Administrator with elevated permissions.
        MEMBER: Regular member.
        GUEST: Guest with limited permissions.
    """

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


class ChatMember(Base):
    """Chat member entity representing a user's membership in a chat room.

    Attributes:
        id: Unique identifier.
        room_id: ID of the chat room.
        user_id: ID of the user.
        role: Member's role in the room.
        last_read_at: When the user last read messages in the room.
        is_active: Whether the membership is active.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
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

    __table_args__ = (Index("idx_unique_room_user", "room_id", "user_id", unique=True),)

    def __repr__(self) -> str:
        """Return string representation of ChatMember instance.

        Returns:
            String representation including id, user ID, room ID, and role.
        """
        return f"<ChatMember {self.id}: User {self.user_id} in Room {self.room_id} ({self.role})>"


class MessageType(str, Enum):
    """Types of chat messages.

    Attributes:
        TEXT: Plain text message.
        IMAGE: Image message.
        FILE: File attachment message.
        SYSTEM: System notification message.
        ACTION: User action message.
    """

    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"
    ACTION = "action"


class ChatMessage(Base):
    """Chat message entity representing a message in a chat room.

    Attributes:
        id: Unique identifier.
        room_id: ID of the chat room.
        sender_id: ID of the user who sent the message.
        message_type: Type of message.
        content_encrypted: Encrypted message content.
        extra_metadata: Additional metadata about the message.
        is_deleted: Whether the message was deleted.
        deleted_at: When the message was deleted.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
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
    extra_metadata: Mapped[Dict] = mapped_column(
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
        """Get the decrypted message content.

        Returns:
            Decrypted message content.
        """
        return decrypt_message(self.content_encrypted)

    @content.setter
    def content(self, value: str) -> None:
        """Set the message content, encrypting it.

        Args:
            value: Plain text message content to encrypt.
        """
        self.content_encrypted = encrypt_message(value)

    def __repr__(self) -> str:
        """Return string representation of ChatMessage instance.

        Returns:
            String representation including id, message type, and room ID.
        """
        return f"<ChatMessage {self.id}: {self.message_type} in Room {self.room_id}>"


class MessageReaction(Base):
    """Message reaction entity representing a user's reaction to a message.

    Attributes:
        id: Unique identifier.
        message_id: ID of the message being reacted to.
        user_id: ID of the user who reacted.
        reaction: Reaction string (e.g., emoji).
        created_at: Creation timestamp.
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
        """Return string representation of MessageReaction instance.

        Returns:
            String representation including id, reaction, and user ID.
        """
        return f"<MessageReaction {self.id}: {self.reaction} from User {self.user_id}>"


class RateLimitLog(Base):
    """Rate limit log entity for tracking API rate limits.

    Attributes:
        id: Unique identifier.
        user_id: ID of the user being rate limited.
        room_id: ID of the chat room (if applicable).
        event_type: Type of event being limited.
        timestamp: When the event occurred.
        count: Event count.
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
        """Return string representation of RateLimitLog instance.

        Returns:
            String representation including id, user ID, event type, and count.
        """
        return f"<RateLimitLog {self.id}: User {self.user_id} - {self.event_type} ({self.count})>"
