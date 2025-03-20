from __future__ import annotations

"""Media repository implementation.

This module provides data access and persistence operations for Media entities.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.media import Media, MediaType, MediaVisibility
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException


class MediaRepository(BaseRepository[Media, uuid.UUID]):
    """Repository for Media entity operations.

    Provides methods for querying, creating, updating, and deleting
    Media entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the media repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Media, db=db)

    async def find_by_filename(self, filename: str) -> List[Media]:
        """Find media by filename.

        Args:
            filename: The filename to search for.

        Returns:
            List of media with matching filename.
        """
        query = select(Media).where(
            Media.filename.ilike(f"%{filename}%"), Media.is_deleted == False
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def find_by_media_type(self, media_type: MediaType) -> List[Media]:
        """Find media by type.

        Args:
            media_type: The media type to filter by.

        Returns:
            List of media of the specified type.
        """
        query = select(Media).where(
            Media.media_type == media_type, Media.is_deleted == False
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_visibility(
        self, visibility: MediaVisibility, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated list of media with specified visibility.

        Args:
            visibility: The visibility to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(Media)
            .where(Media.visibility == visibility, Media.is_deleted == False)
            .order_by(Media.created_at.desc())
        )

        return await self.paginate(query, page, page_size)

    async def approve(
        self, media_id: uuid.UUID, approver_id: uuid.UUID
    ) -> Optional[Media]:
        """Approve a media item.

        Args:
            media_id: ID of the media to approve.
            approver_id: ID of the user approving the media.

        Returns:
            Updated media if found, None otherwise.
        """
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

    async def get_by_product(
        self, product_id: uuid.UUID, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get paginated list of media for a specific product.

        Args:
            product_id: The product ID to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        from app.models.associations import product_media_association

        query = (
            select(Media)
            .join(
                product_media_association,
                Media.id == product_media_association.c.media_id,
            )
            .where(
                product_media_association.c.product_id == product_id,
                Media.is_deleted == False,
            )
            .order_by(product_media_association.c.display_order)
        )

        return await self.paginate(query, page, page_size)

    async def ensure_exists(self, media_id: uuid.UUID) -> Media:
        """Ensure a media exists by ID, raising an exception if not found.

        Args:
            media_id: The media ID to check.

        Returns:
            The media if found.

        Raises:
            ResourceNotFoundException: If the media is not found.
        """
        media = await self.get_by_id(media_id)
        if not media:
            raise ResourceNotFoundException(
                resource_type="Media", resource_id=str(media_id)
            )
        return media
