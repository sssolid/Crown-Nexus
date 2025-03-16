from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text, Boolean, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.utils.crypto import encrypt_message, decrypt_message
if TYPE_CHECKING:
    from app.models.user import User, Company
class ChatRoomType(str, Enum):
    DIRECT = 'direct'
    GROUP = 'group'
    COMPANY = 'company'
    SUPPORT = 'support'
class ChatRoom(Base):
    __tablename__ = 'chat_room'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    type: Mapped[ChatRoomType] = mapped_column(String(20), nullable=False, index=True)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('company.id'), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=expression.true(), nullable=False)
    metadata: Mapped[Dict] = mapped_column(JSONB, nullable=False, default=dict, server_default=expression.text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    company = relationship('Company', back_populates='chat_rooms')
    messages: Mapped[List['ChatMessage']] = relationship('ChatMessage', back_populates='room', cascade='all, delete-orphan')
    members: Mapped[List['ChatMember']] = relationship('ChatMember', back_populates='room', cascade='all, delete-orphan')
    def __repr__(self) -> str:
        return f"<ChatRoom {self.id}: {self.name or '(Direct)'} ({self.type})>"
class ChatMemberRole(str, Enum):
    OWNER = 'owner'
    ADMIN = 'admin'
    MEMBER = 'member'
    GUEST = 'guest'
class ChatMember(Base):
    __tablename__ = 'chat_member'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('chat_room.id'), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False, index=True)
    role: Mapped[ChatMemberRole] = mapped_column(String(20), nullable=False, default=ChatMemberRole.MEMBER)
    last_read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=expression.true(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    room: Mapped['ChatRoom'] = relationship('ChatRoom', back_populates='members')
    user: Mapped['User'] = relationship('User', back_populates='chat_memberships')
    __table_args__ = (Index('idx_unique_room_user', 'room_id', 'user_id', unique=True),)
    def __repr__(self) -> str:
        return f'<ChatMember {self.id}: User {self.user_id} in Room {self.room_id} ({self.role})>'
class MessageType(str, Enum):
    TEXT = 'text'
    IMAGE = 'image'
    FILE = 'file'
    SYSTEM = 'system'
    ACTION = 'action'
class ChatMessage(Base):
    __tablename__ = 'chat_message'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('chat_room.id'), nullable=False, index=True)
    sender_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True, index=True)
    message_type: Mapped[MessageType] = mapped_column(String(20), nullable=False, default=MessageType.TEXT)
    content_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[Dict] = mapped_column(JSONB, nullable=False, default=dict, server_default=expression.text("'{}'::jsonb"))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default=expression.false(), nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    room: Mapped['ChatRoom'] = relationship('ChatRoom', back_populates='messages')
    sender: Mapped[Optional['User']] = relationship('User')
    reactions: Mapped[List['MessageReaction']] = relationship('MessageReaction', back_populates='message', cascade='all, delete-orphan')
    @property
    def content(self) -> str:
        return decrypt_message(self.content_encrypted)
    @content.setter
    def content(self, value: str) -> None:
        self.content_encrypted = encrypt_message(value)
    def __repr__(self) -> str:
        return f'<ChatMessage {self.id}: {self.message_type} in Room {self.room_id}>'
class MessageReaction(Base):
    __tablename__ = 'message_reaction'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('chat_message.id'), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False, index=True)
    reaction: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    message: Mapped['ChatMessage'] = relationship('ChatMessage', back_populates='reactions')
    user: Mapped['User'] = relationship('User')
    __table_args__ = (Index('idx_unique_message_user_reaction', 'message_id', 'user_id', 'reaction', unique=True),)
    def __repr__(self) -> str:
        return f'<MessageReaction {self.id}: {self.reaction} from User {self.user_id}>'
class RateLimitLog(Base):
    __tablename__ = 'rate_limit_log'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False, index=True)
    room_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('chat_room.id'), nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    user: Mapped['User'] = relationship('User')
    room: Mapped[Optional['ChatRoom']] = relationship('ChatRoom')
    def __repr__(self) -> str:
        return f'<RateLimitLog {self.id}: User {self.user_id} - {self.event_type} ({self.count})>'