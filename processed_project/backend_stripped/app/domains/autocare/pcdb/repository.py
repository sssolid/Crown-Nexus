from __future__ import annotations
'PCdb repository implementation.\n\nThis module provides data access and persistence operations for PCdb entities.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.pcdb.models import Parts, Category, SubCategory, Position, PartCategory, PartPosition, PartsSupersession, PCdbVersion, PartsDescription
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
    async def search_parts(self, search_term: str, categories: Optional[List[int]]=None, subcategories: Optional[List[int]]=None, positions: Optional[List[int]]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        return await self.parts_repo.search(search_term, categories, subcategories, positions, page, page_size)
class PartsRepository(BaseRepository[Parts, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Parts, db=db)
    async def get_by_terminology_id(self, part_terminology_id: int) -> Optional[Parts]:
        query = select(Parts).where(Parts.part_terminology_id == part_terminology_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_by_terminology_id_with_related(self, part_terminology_id: int) -> Optional[Parts]:
        from sqlalchemy.orm import selectinload
        query = select(Parts).options(selectinload(Parts.description), selectinload(Parts.categories).selectinload(PartCategory.category), selectinload(Parts.categories).selectinload(PartCategory.subcategory), selectinload(Parts.positions).selectinload(PartPosition.position)).where(Parts.part_terminology_id == part_terminology_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search(self, search_term: Optional[str], categories: Optional[List[int]]=None, subcategories: Optional[List[int]]=None, positions: Optional[List[int]]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        from sqlalchemy.orm import selectinload, joinedload
        from sqlalchemy import text, func, or_, desc, cast, Float
        query = select(Parts).options(selectinload(Parts.description))
        description_joined = False
        apply_ranking = False
        conditions = []
        if search_term and search_term.strip():
            search_term = search_term.strip()
            search_conditions = []
            config = 'english'
            tokens = search_term.split()
            clean_tokens = []
            for token in tokens:
                clean_token = ''.join((c for c in token if c.isalnum()))
                if len(clean_token) >= 3:
                    clean_tokens.append(clean_token)
            if clean_tokens:
                tsquery_expression = ' & '.join(clean_tokens)
                tsquery = func.to_tsquery(config, tsquery_expression)
                tsvector_name = func.to_tsvector(config, Parts.part_terminology_name)
                search_conditions.append(tsvector_name.op('@@')(tsquery))
                if not description_joined:
                    query = query.outerjoin(PartsDescription, Parts.parts_description_id == PartsDescription.parts_description_id)
                    description_joined = True
                tsvector_desc = func.to_tsvector(config, PartsDescription.parts_description)
                search_conditions.append(tsvector_desc.op('@@')(tsquery))
                apply_ranking = True
            search_conditions.append(Parts.part_terminology_name.ilike(f'%{search_term}%'))
            if not description_joined:
                query = query.outerjoin(PartsDescription, Parts.parts_description_id == PartsDescription.parts_description_id)
                description_joined = True
            search_conditions.append(PartsDescription.parts_description.ilike(f'%{search_term}%'))
            try:
                similarity_threshold = 0.3
                search_conditions.append(func.similarity(Parts.part_terminology_name, search_term) > similarity_threshold)
                if not description_joined:
                    query = query.outerjoin(PartsDescription, Parts.parts_description_id == PartsDescription.parts_description_id)
                    description_joined = True
                search_conditions.append(func.similarity(PartsDescription.parts_description, search_term) > similarity_threshold)
            except Exception:
                pass
            if search_conditions:
                conditions.append(or_(*search_conditions))
        if categories and all((category is not None for category in categories)):
            query = query.join(PartCategory, Parts.part_terminology_id == PartCategory.part_terminology_id)
            conditions.append(PartCategory.category_id.in_(categories))
        if subcategories and all((subcategory is not None for subcategory in subcategories)):
            if not any(('PartCategory' in str(join) for join in query._setup_joins if hasattr(query, '_setup_joins'))):
                query = query.join(PartCategory, Parts.part_terminology_id == PartCategory.part_terminology_id)
            conditions.append(PartCategory.subcategory_id.in_(subcategories))
        if positions and all((position is not None for position in positions)):
            query = query.join(PartPosition, Parts.part_terminology_id == PartPosition.part_terminology_id)
            conditions.append(PartPosition.position_id.in_(positions))
        if conditions:
            query = query.where(and_(*conditions))
        if apply_ranking and search_term and search_term.strip():
            if not description_joined:
                query = query.outerjoin(PartsDescription, Parts.parts_description_id == PartsDescription.parts_description_id)
            ts_rank_name = func.ts_rank(func.to_tsvector('english', Parts.part_terminology_name), func.to_tsquery('english', ' & '.join(clean_tokens)))
            ts_rank_desc = func.ts_rank(func.to_tsvector('english', PartsDescription.parts_description), func.to_tsquery('english', ' & '.join(clean_tokens)))
            query = query.order_by(desc(ts_rank_name * 2.0 + func.coalesce(ts_rank_desc, 0)), desc(func.similarity(Parts.part_terminology_name, search_term)), Parts.part_terminology_name)
        else:
            query = query.order_by(Parts.part_terminology_name)
        result = await self.paginate(query, page, page_size)
        return result
    async def get_by_category(self, category_id: int, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Parts).join(PartCategory, Parts.part_terminology_id == PartCategory.part_terminology_id).where(PartCategory.category_id == category_id).order_by(Parts.part_terminology_name)
        return await self.paginate(query, page, page_size)
    async def get_supersessions(self, part_terminology_id: int) -> Dict[str, List[Parts]]:
        superseded_by_query = select(Parts).join(PartsSupersession, and_(Parts.part_terminology_id == PartsSupersession.new_part_terminology_id, PartsSupersession.old_part_terminology_id == part_terminology_id))
        supersedes_query = select(Parts).join(PartsSupersession, and_(Parts.part_terminology_id == PartsSupersession.old_part_terminology_id, PartsSupersession.new_part_terminology_id == part_terminology_id))
        superseded_by_result = await self.db.execute(superseded_by_query)
        supersedes_result = await self.db.execute(supersedes_query)
        superseded_by_parts = list(superseded_by_result.scalars().all())
        supersedes_parts = list(supersedes_result.scalars().all())
        return {'superseded_by': superseded_by_parts, 'supersedes': supersedes_parts}
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