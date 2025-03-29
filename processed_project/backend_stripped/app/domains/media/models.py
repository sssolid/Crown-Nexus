from __future__ import annotations
'Media model definition.\n\nThis module defines the Media model and related enums for\nhandling media files within the application.\n'
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import DateTime, Enum as SQLAEnum, ForeignKey, Integer, String, func, text, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
if TYPE_CHECKING:
    from app.domains.products.models import Product
else:
    from app.models.associations import product_media_association
class MediaType(str, Enum):
    IMAGE = 'image'
    DOCUMENT = 'document'
    VIDEO = 'video'
    MSDS = 'msds'
    DOT_APPROVAL = 'dot_approval'
    OTHER = 'other'
class MediaVisibility(str, Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'
    RESTRICTED = 'restricted'
class Media(Base):
    __tablename__ = 'media'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    media_type: Mapped[MediaType] = mapped_column(SQLAEnum(MediaType), default=MediaType.IMAGE, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(127), nullable=False)
    visibility: Mapped[MediaVisibility] = mapped_column(SQLAEnum(MediaVisibility), default=MediaVisibility.PRIVATE, nullable=False)
    file_metadata: Mapped[Dict] = mapped_column(JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb"))
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, server_default=expression.false(), nullable=False)
    approved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    products: Mapped[List['Product']] = relationship('Product', secondary=product_media_association, back_populates='media')
    uploaded_by: Mapped['User'] = relationship('User', foreign_keys=[uploaded_by_id], back_populates='uploaded_media')
    approved_by: Mapped[Optional['User']] = relationship('User', foreign_keys=[approved_by_id], back_populates='approved_media')
    def __repr__(self) -> str:
        return f'<Media {self.filename} ({self.media_type})>'
    @property
    def extension(self) -> str:
        if not self.filename or '.' not in self.filename:
            return ''
        return self.filename.rsplit('.', 1)[1].lower()
    @property
    def is_image(self) -> bool:
        return self.media_type == MediaType.IMAGE
    @property
    def has_thumbnail(self) -> bool:
        return self.is_image