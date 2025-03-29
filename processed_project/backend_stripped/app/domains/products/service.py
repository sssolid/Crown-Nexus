from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency_manager import get_dependency
from app.domains.products.models import Product
from app.domains.products.schemas import ProductCreate
class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_product(self, product_id: UUID) -> Product:
        query = select(Product).where(Product.id == product_id)
        result = await self.db.execute(query)
        product = result.scalars().first()
        error_service = get_dependency('error_service')
        return error_service.ensure_not_none(product, resource_type='Product', resource_id=str(product_id))
    async def create_product(self, data: ProductCreate) -> Product:
        query = select(Product).where(Product.part_number == data.part_number)
        result = await self.db.execute(query)
        existing = result.scalars().first()
        if existing is not None:
            error_service = get_dependency('error_service')
            raise error_service.resource_already_exists(resource_type='Product', identifier=data.part_number, field='part_number')
        product = Product(**data.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product