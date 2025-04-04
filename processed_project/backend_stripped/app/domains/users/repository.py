from __future__ import annotations
'User repository implementation.\n\nThis module provides data access and persistence operations for User entities.\n'
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.users.models import User, UserRole
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, AuthenticationException
class UserRepository(BaseRepository[User, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=User, db=db)
    async def find_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email, User.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_role(self, role: UserRole) -> List[User]:
        query = select(User).where(User.role == role, User.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_company(self, company_id: uuid.UUID, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(User).where(User.company_id == company_id, User.is_deleted == False).order_by(User.full_name)
        return await self.paginate(query, page, page_size)
    async def authenticate(self, email: str, password: str) -> User:
        from app.domains.users.models import verify_password
        user = await self.find_by_email(email)
        if not user:
            raise AuthenticationException(message='Invalid email or password')
        if not verify_password(password, user.hashed_password):
            raise AuthenticationException(message='Invalid email or password')
        if not user.is_active:
            raise AuthenticationException(message='User account is inactive')
        return user
    async def ensure_exists(self, user_id: uuid.UUID) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(resource_type='User', resource_id=str(user_id))
        return user