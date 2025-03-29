from __future__ import annotations
'Media repository implementation.\n\nThis module provides data access and persistence operations for Media entities.\n'
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.media.models import Media, MediaType, MediaVisibility
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException
class MediaRepository(BaseRepository[Media, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Media, db=db)
    async def find_by_filename(self, filename: str) -> List[Media]:
        query = select(Media).where(Media.filename.ilike(f'%{filename}%'), Media.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def find_by_media_type(self, media_type: MediaType) -> List[Media]:
        query = select(Media).where(Media.media_type == media_type, Media.is_deleted == False)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def get_by_visibility(self, visibility: MediaVisibility, page: int=1, page_size: int=20) -> Dict[str, Any]:
        query = select(Media).where(Media.visibility == visibility, Media.is_deleted == False).order_by(Media.created_at.desc())
        return await self.paginate(query, page, page_size)
    async def approve(self, media_id: uuid.UUID, approver_id: uuid.UUID) -> Optional[Media]:
        media = await self.get_by_id(media_id)
        if not media:
            return None
        media.is_approved = True
        media.approved_by_id = approver_id
        media.approved_at = datetime.now()
        self.db.add(media)
        await self.db.flush()
        await self.db.refresh(media)
        return media
    async def get_by_product(self, product_id: uuid.UUID, page: int=1, page_size: int=20) -> Dict[str, Any]:
        from app.models.associations import product_media_association
        query = select(Media).join(product_media_association, Media.id == product_media_association.c.media_id).where(product_media_association.c.product_id == product_id, Media.is_deleted == False).order_by(product_media_association.c.display_order)
        return await self.paginate(query, page, page_size)
    async def ensure_exists(self, media_id: uuid.UUID) -> Media:
        media = await self.get_by_id(media_id)
        if not media:
            raise ResourceNotFoundException(resource_type='Media', resource_id=str(media_id))
        return media