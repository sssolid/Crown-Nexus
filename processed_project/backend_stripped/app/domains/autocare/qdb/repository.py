from __future__ import annotations
'Qdb repository implementation.\n\nThis module provides data access and persistence operations for Qdb entities.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.domains.autocare.qdb.models import QualifierType, Qualifier, Language, QualifierTranslation, GroupNumber, QualifierGroup, QdbVersion
class QdbRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.qualifier_repo = QualifierRepository(db)
        self.qualifier_type_repo = QualifierTypeRepository(db)
        self.language_repo = LanguageRepository(db)
        self.group_repo = GroupNumberRepository(db)
    async def get_version(self) -> Optional[str]:
        query = select(QdbVersion).where(QdbVersion.is_current == True)
        result = await self.db.execute(query)
        version = result.scalars().first()
        if version:
            return version.version_date.strftime('%Y-%m-%d')
        return None
    async def update_version(self, version_date: datetime) -> QdbVersion:
        await self.db.execute(select(QdbVersion).where(QdbVersion.is_current == True).update({QdbVersion.is_current: False}))
        version = QdbVersion(version_date=version_date, is_current=True)
        self.db.add(version)
        await self.db.flush()
        return version
    async def search_qualifiers(self, search_term: str, qualifier_type_id: Optional[int]=None, language_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        return await self.qualifier_repo.search(search_term, qualifier_type_id, language_id, page, page_size)
class QualifierRepository(BaseRepository[Qualifier, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Qualifier, db=db)
    async def get_by_qualifier_id(self, qualifier_id: int) -> Optional[Qualifier]:
        query = select(Qualifier).where(Qualifier.qualifier_id == qualifier_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def search(self, search_term: str, qualifier_type_id: Optional[int]=None, language_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        conditions = []
        conditions.append(Qualifier.qualifier_text.ilike(f'%{search_term}%'))
        if qualifier_type_id:
            conditions.append(Qualifier.qualifier_type_id == qualifier_type_id)
        query = select(Qualifier).where(or_(*conditions))
        if language_id:
            translation_query = select(Qualifier).join(QualifierTranslation, Qualifier.qualifier_id == QualifierTranslation.qualifier_id).where(and_(QualifierTranslation.language_id == language_id, QualifierTranslation.translation_text.ilike(f'%{search_term}%')))
            query = query.union(translation_query)
        query = query.order_by(Qualifier.qualifier_text)
        return await self.paginate(query, page, page_size)
    async def get_translations(self, qualifier_id: int, language_id: Optional[int]=None) -> List[QualifierTranslation]:
        conditions = [QualifierTranslation.qualifier_id == qualifier_id]
        if language_id:
            conditions.append(QualifierTranslation.language_id == language_id)
        query = select(QualifierTranslation).where(and_(*conditions)).order_by(QualifierTranslation.language_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_groups(self, qualifier_id: int) -> List[Dict[str, Any]]:
        query = select(QualifierGroup, GroupNumber).join(GroupNumber, QualifierGroup.group_number_id == GroupNumber.group_number_id).where(QualifierGroup.qualifier_id == qualifier_id).order_by(GroupNumber.group_number_id)
        result = await self.db.execute(query)
        groups = []
        for group, group_number in result:
            groups.append({'group': group, 'group_number': group_number})
        return groups
class QualifierTypeRepository(BaseRepository[QualifierType, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=QualifierType, db=db)
    async def get_by_qualifier_type_id(self, qualifier_type_id: int) -> Optional[QualifierType]:
        query = select(QualifierType).where(QualifierType.qualifier_type_id == qualifier_type_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_all_types(self) -> List[QualifierType]:
        query = select(QualifierType).order_by(QualifierType.qualifier_type)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class LanguageRepository(BaseRepository[Language, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Language, db=db)
    async def get_by_language_id(self, language_id: int) -> Optional[Language]:
        query = select(Language).where(Language.language_id == language_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_all_languages(self) -> List[Language]:
        query = select(Language).order_by(Language.language_name)
        result = await self.db.execute(query)
        return list(result.scalars().all())
class GroupNumberRepository(BaseRepository[GroupNumber, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=GroupNumber, db=db)
    async def get_by_group_number_id(self, group_number_id: int) -> Optional[GroupNumber]:
        query = select(GroupNumber).where(GroupNumber.group_number_id == group_number_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_all_groups(self) -> List[GroupNumber]:
        query = select(GroupNumber).order_by(GroupNumber.group_number_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_qualifiers_by_group(self, group_number_id: int, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Qualifier).join(QualifierGroup, Qualifier.qualifier_id == QualifierGroup.qualifier_id).where(QualifierGroup.group_number_id == group_number_id).order_by(Qualifier.qualifier_text)
        return await self.paginate(query, page, page_size)