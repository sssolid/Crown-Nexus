from __future__ import annotations

"""User repository implementation.

This module provides data access and persistence operations for User entities.
"""

import uuid
from typing import List, Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, AuthenticationException


class UserRepository(BaseRepository[User, uuid.UUID]):
    """Repository for User entity operations.

    Provides methods for querying, creating, updating, and deleting
    User entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the user repository.

        Args:
            db: The database session.
        """
        super().__init__(model=User, db=db)

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email address.

        Args:
            email: The email address to search for.

        Returns:
            The user if found, None otherwise.
        """
        query = select(User).where(User.email == email, User.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_role(self, role: UserRole) -> List[User]:
        """Get all users with a specific role.

        Args:
            role: The role to filter by.

        Returns:
            List of users with the specified role.
        """
        query = select(User).where(User.role == role, User.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_company(
        self, company_id: uuid.UUID, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated list of users for a specific company.

        Args:
            company_id: The company ID to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(User)
            .where(User.company_id == company_id, User.is_deleted == False)
            .order_by(User.full_name)
        )

        return await self.paginate(query, page, page_size)

    async def authenticate(self, email: str, password: str) -> User:
        """Authenticate a user by email and password.

        Args:
            email: The user's email.
            password: The plaintext password.

        Returns:
            The authenticated user.

        Raises:
            AuthenticationException: If authentication fails.
        """
        from app.models.user import verify_password

        user = await self.find_by_email(email)
        if not user:
            raise AuthenticationException(message="Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise AuthenticationException(message="Invalid email or password")

        if not user.is_active:
            raise AuthenticationException(message="User account is inactive")

        return user

    async def ensure_exists(self, user_id: uuid.UUID) -> User:
        """Ensure a user exists by ID, raising an exception if not found.

        Args:
            user_id: The user ID to check.

        Returns:
            The user if found.

        Raises:
            ResourceNotFoundException: If the user is not found.
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(
                resource_type="User", resource_id=str(user_id)
            )
        return user
