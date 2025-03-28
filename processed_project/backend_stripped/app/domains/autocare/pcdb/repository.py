from __future__ import annotations
'PCdb repository implementation.\n\nThis module provides data access and persistence operations for PCdb entities.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.pcdb.models import Parts, Category, SubCategory, Position, PartCategory, PartPosition, PartsSupersession, PCdbVersion
class PCdbRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.parts_repo = PartsRepository(db)
        self.category_repo = CategoryRepository(db)
        self.subcategory_repo = SubCategoryRepository(db)
        self.position_repo = PositionRepository(db)
    async def get_version(self) -> Optional[str]:
        query = select(PCdbVersion).where(PCdbVersion.is_current == True)
        result = await self.db.execute(query)
        version = result.scalars().first()
        if version:
            return version.version_date.strftime('%Y-%m-%d')
        return None
    async def update_version(self, version_date: datetime) -> PCdbVersion:
        await self.db.execute(select(PCdbVersion).where(PCdbVersion.is_current == True).update({PCdbVersion.is_current: False}))
        version = PCdbVersion(version_date=version_date, is_current=True)
        self.db.add(version)
        await self.db.flush()
        return version
    async def search_parts(self, search_term: str, categories: Optional[List[int]]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        return await self.parts_repo.search(search_term, categories, page, page_size)
class PartsRepository(BaseRepository[Parts, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Parts, db=db)
    async def get_by_terminology_id(self, part_terminology_id: int) -> Optional[Parts]:
        query = select(Parts).where(Parts.part_terminology_id == part_terminology_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search(self, search_term: str, categories: Optional[List[int]]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        conditions = [Parts.part_terminology_name.ilike(f'%{search_term}%')]
        if categories:
            query = select(Parts).join(PartCategory, Parts.part_terminology_id == PartCategory.part_terminology_id).where(and_(*conditions, PartCategory.category_id.in_(categories))).order_by(Parts.part_terminology_name)
        else:
            query = select(Parts).where(and_(*conditions)).order_by(Parts.part_terminology_name)
        return await self.paginate(query, page, page_size)
    async def get_by_category(self, category_id: int, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Parts).join(PartCategory, Parts.part_terminology_id == PartCategory.part_terminology_id).where(PartCategory.category_id == category_id).order_by(Parts.part_terminology_name)
        return await self.paginate(query, page, page_size)
    async def get_supersessions(self, part_terminology_id: int) -> Dict[str, List[Parts]]:
        superseded_by_query = select(Parts).join(PartsSupersession, and_(Parts.part_terminology_id == PartsSupersession.new_part_terminology_id, PartsSupersession.old_part_terminology_id == part_terminology_id))
        supersedes_query = select(Parts).join(PartsSupersession, and_(Parts.part_terminology_id == PartsSupersession.old_part_terminology_id, PartsSupersession.new_part_terminology_id == part_terminology_id))
        superseded_by_result = await self.db.execute(superseded_by_query)
        supersedes_result = await self.db.execute(supersedes_query)
        return {'superseded_by': list(superseded_by_result.scalars().all()), 'supersedes': list(supersedes_result.scalars().all())}
class CategoryRepository(BaseRepository[Category, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Category, db=db)
    async def get_by_category_id(self, category_id: int) -> Optional[Category]:
        query = select(Category).where(Category.category_id == category_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_all_categories(self) -> List[Category]:
        query = select(Category).order_by(Category.category_name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def search(self, search_term: str) -> List[Category]:
        query = select(Category).where(Category.category_name.ilike(f'%{search_term}%')).order_by(Category.category_name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class SubCategoryRepository(BaseRepository[SubCategory, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=SubCategory, db=db)
    async def get_by_subcategory_id(self, subcategory_id: int) -> Optional[SubCategory]:
        query = select(SubCategory).where(SubCategory.subcategory_id == subcategory_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_category(self, category_id: int) -> List[SubCategory]:
        query = select(SubCategory).join(PartCategory, SubCategory.subcategory_id == PartCategory.subcategory_id).where(PartCategory.category_id == category_id).distinct().order_by(SubCategory.subcategory_name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class PositionRepository(BaseRepository[Position, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Position, db=db)
    async def get_by_position_id(self, position_id: int) -> Optional[Position]:
        query = select(Position).where(Position.position_id == position_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_all_positions(self) -> List[Position]:
        query = select(Position).order_by(Position.position)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_part(self, part_terminology_id: int) -> List[Position]:
        query = select(Position).join(PartPosition, Position.position_id == PartPosition.position_id).where(PartPosition.part_terminology_id == part_terminology_id).order_by(Position.position)
        result = await self.db.execute(query)
        return list(result.scalars().all())