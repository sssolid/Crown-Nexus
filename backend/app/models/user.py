# backend/app/models/user.py
"""
User model and authentication utilities.

This module defines the User and Company models for authentication
and authorization. It also provides utility functions for password
hashing and token creation.

The models support:
- User roles with different permission levels
- Company associations for B2B functionality
- Secure password handling
- JWT token generation for authentication
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, Optional, Union

from jose import jwt
from passlib.context import CryptContext
import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.core.config import settings
from app.db.base_class import Base


class UserRole(str, Enum):
    """
    User role enumeration for authorization.

    These roles define different permission levels in the system:
    - ADMIN: Full system access and management capabilities
    - MANAGER: Product and user management, approvals
    - CLIENT: Regular customer access
    - DISTRIBUTOR: B2B partner access
    - READ_ONLY: Limited view-only access
    """
    ADMIN = "admin"
    MANAGER = "manager"
    CLIENT = "client"
    DISTRIBUTOR = "distributor"
    READ_ONLY = "read_only"


class User(Base):
    """
    User model for authentication and authorization.

    This model stores user information, credentials, and permissions.
    It supports:
    - Email-based authentication
    - Role-based access control
    - Company association for B2B users
    - Account status tracking

    Attributes:
        id: Primary key UUID
        email: User's email address (used for login)
        hashed_password: Bcrypt-hashed password
        full_name: User's full name
        role: User's role in the system
        is_active: Whether the user account is active
        company_id: Reference to associated company (optional)
        company: Relationship to Company model
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    full_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        sa.Enum(UserRole, values_callable=lambda enum: [e.value for e in enum], name="userrole"),
        default=UserRole.CLIENT, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true(), nullable=False
    )

    # Company relationship (if applicable)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.id"), nullable=True
    )
    company: Mapped[Optional["Company"]] = relationship("Company")

    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        """
        String representation of the user.

        Returns:
            str: User representation with email and role
        """
        return f"<User {self.email} ({self.role})>"


class Company(Base):
    """
    Company model for B2B customers and distributors.

    This model stores information about client companies and distributors.
    It supports:
    - Account number tracking for integration with external systems
    - Different account types (distributor, jobber, etc.)
    - Address information for headquarters, billing, and shipping
    - Industry classification
    - Status tracking

    Attributes:
        id: Primary key UUID
        name: Company name
        headquarters_address_id: Reference to headquarters address
        billing_address_id: Reference to billing address
        shipping_address_id: Reference to shipping address
        account_number: External account number (e.g., from iSeries)
        account_type: Type of account (distributor, jobber, etc.)
        industry: Industry sector (Automotive, Electronics, etc.)
        is_active: Whether the company account is active
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "company"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    # Address relationships
    headquarters_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("address.id"), nullable=True
    )
    billing_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("address.id"), nullable=True
    )
    shipping_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("address.id"), nullable=True
    )
    # Existing fields
    account_number: Mapped[Optional[str]] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    account_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    # New industry field
    industry: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=expression.true(), nullable=False
    )

    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    headquarters_address = relationship("Address", foreign_keys=[headquarters_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])

    def __repr__(self) -> str:
        """
        String representation of the company.

        Returns:
            str: Company representation with name and account type
        """
        return f"<Company {self.name} ({self.account_type})>"


# Password handling utilities with Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password: Plain text password
        hashed_password: Bcrypt hashed password

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using Bcrypt.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, uuid.UUID],
    role: UserRole,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        subject: Subject (usually user ID) to include in the token
        role: User role to include in the token
        expires_delta: Token expiration time delta (optional)

    Returns:
        str: JWT token string
    """
    # Convert subject to string if it's a UUID
    if isinstance(subject, uuid.UUID):
        subject = str(subject)

    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Create JWT payload
    to_encode: Dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "role": role,
        "iat": datetime.utcnow(),  # Issued at time
    }

    # Encode and return token
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
