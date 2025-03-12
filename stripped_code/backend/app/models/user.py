from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Optional, Union
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.core.config import settings
from app.db.base_class import Base
class UserRole(str, Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    CLIENT = 'client'
    DISTRIBUTOR = 'distributor'
    READ_ONLY = 'read_only'
class User(Base):
    __tablename__ = 'user'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.CLIENT, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=expression.true(), nullable=False)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('company.id'), nullable=True)
    company: Mapped[Optional['Company']] = relationship('Company')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<User {self.email} ({self.role})>'
class Company(Base):
    __tablename__ = 'company'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    account_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True, nullable=True)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=expression.true(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<Company {self.name} ({self.account_type})>'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
def create_access_token(subject: Union[str, uuid.UUID], role: UserRole, expires_delta: Optional[timedelta]=None) -> str:
    if isinstance(subject, uuid.UUID):
        subject = str(subject)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: Dict[str, Any] = {'sub': subject, 'exp': expire, 'role': role, 'iat': datetime.utcnow()}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')