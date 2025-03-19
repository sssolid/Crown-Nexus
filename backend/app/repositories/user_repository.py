from uuid import UUID
from typing import Optional

from app.repositories.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository[User, UUID]):
    async def find_by_username(self, sku: str) -> Optional[User]: ...
