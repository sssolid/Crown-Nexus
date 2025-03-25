from __future__ import annotations

"""User model definition.

This module defines the User model, user roles, authentication utilities,
and related functionality for user management within the application.
"""

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
    """Enumeration of user roles in the system.

    Attributes:
        ADMIN: Administrator role with full system access.
        MANAGER: Manager role with elevated permissions.
        CLIENT: Standard client user.
        DISTRIBUTOR: Distributor with specific permissions.
        READ_ONLY: User with read-only access.
    """

    ADMIN = "admin"
    MANAGER = "manager"
    CLIENT = "client"
    DISTRIBUTOR = "distributor"
    READ_ONLY = "read_only"


class User(Base):
    """User entity representing a system user.

    Attributes:
        id: Unique identifier.
        email: User's email address (unique).
        hashed_password: Securely hashed password.
        full_name: User's full name.
        role: User's role in the system.
        is_active: Whether the user account is active.
        company_id: ID of the associated company.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        sa.Enum(
            UserRole,
            values_callable=lambda enum: [e.value for e in enum],
            name="userrole",
        ),
        default=UserRole.CLIENT,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true(), nullable=False
    )
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id"), nullable=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    company: Mapped[Optional["Company"]] = relationship(
        "Company", back_populates="users"
    )
    chat_memberships: Mapped[List["ChatMember"]] = relationship(
        "ChatMember", back_populates="user"
    )
    api_keys: Mapped[List["ApiKey"]] = relationship("ApiKey", back_populates="user")
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog", back_populates="user"
    )
    uploaded_media = relationship(
        "Media", foreign_keys="[Media.uploaded_by_id]", back_populates="uploaded_by"
    )
    approved_media = relationship(
        "Media", foreign_keys="[Media.approved_by_id]", back_populates="approved_by"
    )

    def __repr__(self) -> str:
        """Return string representation of User instance.

        Returns:
            String representation including email and role.
        """
        return f"<User {self.email} ({self.role})>"


# Password handling utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a plain password matches a hash.

    Args:
        plain_password: The plain-text password to verify.
        hashed_password: The hashed password to compare against.

    Returns:
        True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a hash from a plain-text password.

    Args:
        password: The plain-text password to hash.

    Returns:
        The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, uuid.UUID],
    role: UserRole,
    expires_delta: Optional[datetime.timedelta] = None,
) -> str:
    """Create a JWT access token for a user.

    Args:
        subject: The subject (user ID) for the token.
        role: The user's role.
        expires_delta: Optional custom expiration time delta.

    Returns:
        The encoded JWT token string.
    """
    if isinstance(subject, uuid.UUID):
        subject = str(subject)

    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode: Dict[str, Any] = {
        "sub": subject,
        "jti": str(uuid.uuid4()),
        "type": "access",
        "exp": expire,
        "role": role,
        "iat": datetime.datetime.now(datetime.UTC),
    }

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
