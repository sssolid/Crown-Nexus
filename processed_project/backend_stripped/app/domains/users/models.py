from __future__ import annotations
'User model definition.\n\nThis module defines the User model, user roles, authentication utilities,\nand related functionality for user management within the application.\n'
import uuid
import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from jose import jwt
from passlib.context import CryptContext
import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.core.config import settings
from app.db.base_class import Base
if TYPE_CHECKING:
    from app.domains.company.models import Company
    from app.domains.api_key.models import ApiKey
    from app.domains.media.models import Media
    from app.domains.chat.models import ChatMember
class UserRole(str, Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    CLIENT = 'client'
    DISTRIBUTOR = 'distributor'
    READ_ONLY = 'read_only'
class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'user'}
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(sa.Enum(UserRole, values_callable=lambda enum: [e.value for e in enum], name='userrole'), default=UserRole.CLIENT, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=expression.true(), nullable=False)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('company.company.id'), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    company: Mapped[Optional['Company']] = relationship('Company', back_populates='users')
    chat_memberships: Mapped[List['ChatMember']] = relationship('ChatMember', back_populates='user')
    api_keys: Mapped[List['ApiKey']] = relationship('ApiKey', back_populates='user')
    audit_logs: Mapped[List['AuditLog']] = relationship('AuditLog', back_populates='user')
    uploaded_media: Mapped[List['Media']] = relationship('Media', foreign_keys='Media.uploaded_by_id', back_populates='uploaded_by')
    approved_media: Mapped[List['Media']] = relationship('Media', foreign_keys='Media.approved_by_id', back_populates='approved_by')
    def __repr__(self) -> str:
        return f'<User {self.email} ({self.role})>'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
def create_access_token(subject: Union[str, uuid.UUID], role: UserRole, expires_delta: Optional[datetime.timedelta]=None) -> str:
    if isinstance(subject, uuid.UUID):
        subject = str(subject)
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: Dict[str, Any] = {'sub': subject, 'jti': str(uuid.uuid4()), 'type': 'access', 'exp': expire, 'role': role, 'iat': datetime.datetime.now(datetime.UTC)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')