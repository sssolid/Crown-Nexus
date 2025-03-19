from uuid import UUID
from typing import Optional

from app.repositories.base import BaseRepository
from app.models.product import Product


class ProductRepository(BaseRepository[Product, UUID]):
    async def find_by_sku(self, sku: str) -> Optional[Product]: ...
