# backend/app/schemas/media.py
"""
Media asset schemas.

This module provides Pydantic schemas for media-related data validation
and serialization. The schemas support:
- Request validation for media uploads and updates
- Response serialization with proper URLs
- File upload responses and errors
- Pagination for media listings

These schemas ensure consistent handling of media assets throughout
the application.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.config import settings
from app.models.media import MediaType, MediaVisibility


class MediaBase(BaseModel):
    """
    Base schema for Media data.

    Defines common fields used across media-related schemas.

    Attributes:
        filename: Original file name
        media_type: Type of media (image, document, video, other)
        visibility: Visibility level
        file_metadata: Additional file metadata
    """

    filename: str
    media_type: MediaType = MediaType.IMAGE
    visibility: MediaVisibility = MediaVisibility.PRIVATE
    file_metadata: Dict[str, Any] = Field(default_factory=dict)


class MediaCreate(BaseModel):
    """
    Schema for creating new Media (separate from file upload).

    This schema is used for the form data part of media uploads,
    separate from the actual file data.

    Attributes:
        media_type: Type of media
        visibility: Visibility level
        file_metadata: Additional file metadata
    """

    media_type: MediaType = MediaType.IMAGE
    visibility: MediaVisibility = MediaVisibility.PRIVATE
    file_metadata: Dict[str, Any] = Field(default_factory=dict)


class MediaUpdate(BaseModel):
    """
    Schema for updating existing Media.

    Defines fields that can be updated on a media asset, with all
    fields being optional to allow partial updates.

    Attributes:
        filename: Original file name (optional)
        media_type: Type of media (optional)
        visibility: Visibility level (optional)
        file_metadata: Additional file metadata (optional)
        is_approved: Whether the media is approved (optional)
    """

    filename: Optional[str] = None
    media_type: Optional[MediaType] = None
    visibility: Optional[MediaVisibility] = None
    file_metadata: Optional[Dict[str, Any]] = None
    is_approved: Optional[bool] = None


class MediaInDB(MediaBase):
    """
    Schema for Media as stored in the database.

    Extends the base media schema with database-specific fields.

    Attributes:
        id: Media UUID
        file_path: Path to the stored file
        file_size: Size of the file in bytes
        mime_type: MIME type of the file
        uploaded_by_id: Reference to user who uploaded the file
        is_approved: Whether the media is approved
        approved_by_id: Reference to user who approved the media (optional)
        approved_at: Approval timestamp (optional)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: uuid.UUID
    file_path: str
    file_size: int
    mime_type: str
    uploaded_by_id: uuid.UUID
    is_approved: bool
    approved_by_id: Optional[uuid.UUID] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Media(MediaInDB):
    """
    Schema for Media responses.

    This schema is used for API responses returning media data.
    It extends the database schema with URLs for frontend use.

    Attributes:
        url: URL to access the file
        thumbnail_url: URL to access the thumbnail (optional)
    """

    url: str = ""
    thumbnail_url: Optional[str] = None

    def model_post_init(self, __context: Any) -> None:
        """
        Post initialization hook to set URLs.

        This method runs after the model is initialized, allowing us to
        set the URL fields based on the media properties.

        Args:
            __context: Context information (not used)
        """
        # Base URL for media files
        api_base = f"{settings.API_V1_STR}/media"

        # Set the main file URL if not already set
        if not self.url:
            self.url = f"{api_base}/file/{self.id}"

        # Set thumbnail URL for images if not already set
        if self.thumbnail_url is None and self.media_type == MediaType.IMAGE:
            self.thumbnail_url = f"{api_base}/thumbnail/{self.id}"


class MediaListResponse(BaseModel):
    """
    Paginated response for media listings.

    This schema provides a structure for paginated media list responses.

    Attributes:
        items: List of media items
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        pages: Total number of pages
    """

    items: List[Media]
    total: int
    page: int
    page_size: int
    pages: int


class FileUploadResponse(BaseModel):
    """
    Response after file upload.

    This schema defines the structure of responses to file uploads.

    Attributes:
        media: Media information
        message: Success message
    """

    media: Media
    message: str = "File uploaded successfully"


class FileUploadError(BaseModel):
    """
    Error response for file upload.

    This schema defines the structure of error responses for file uploads.

    Attributes:
        error: Error type
        detail: Detailed error information (optional)
    """

    error: str
    detail: Optional[str] = None
