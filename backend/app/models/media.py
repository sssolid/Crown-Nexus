from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SQLAEnum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.associations import product_media_association

# For type hints only, not runtime imports
if TYPE_CHECKING:
    from app.models.product import Product


class MediaType(str, Enum):
    """Types of media files."""
    IMAGE = "image"
    DOCUMENT = "document"
    VIDEO = "video"
    OTHER = "other"


class MediaVisibility(str, Enum):
    """Visibility levels for media files."""
    PUBLIC = "public"  # Accessible without authentication
    PRIVATE = "private"  # Requires authentication
    RESTRICTED = "restricted"  # Requires specific permissions


class Media(Base):
    """
    Media model for storing file metadata.

    Attributes:
        id: Primary key UUID
        filename: Original filename
        file_path: Path to the stored file
        file_size: Size of the file in bytes
        media_type: Type of media (image, document, video, other)
        mime_type: MIME type of the file
        visibility: Visibility level
        file_metadata: Additional metadata as JSON
        uploaded_by_id: Reference to the user who uploaded the file
        is_approved: Whether the file has been approved for use
        approved_by_id: Reference to the user who approved the file
        approved_at: When the file was approved
        products: Associated products
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "media"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    media_type: Mapped[MediaType] = mapped_column(
        SQLAEnum(MediaType), default=MediaType.IMAGE, nullable=False
    )
    mime_type: Mapped[str] = mapped_column(String(127), nullable=False)
    visibility: Mapped[MediaVisibility] = mapped_column(
        SQLAEnum(MediaVisibility), default=MediaVisibility.PRIVATE, nullable=False
    )
    # Renamed from 'metadata' to 'file_metadata' to avoid conflict with SQLAlchemy's reserved attribute
    file_metadata: Mapped[Dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Upload and approval tracking
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    is_approved: Mapped[bool] = mapped_column(default=False, nullable=False)
    approved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=True
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    products: Mapped[List["Product"]] = relationship(
        "app.models.product.Product",
        secondary=product_media_association,
        back_populates="media"
    )
    uploaded_by = relationship(
        "User",
        foreign_keys=[uploaded_by_id],
        backref="uploaded_media"
    )
    approved_by = relationship(
        "User",
        foreign_keys=[approved_by_id],
        backref="approved_media"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def __repr__(self) -> str:
        """String representation of the media."""
        return f"<Media {self.filename} ({self.media_type})>"
