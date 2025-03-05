from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, validator

from app.models.media import MediaType, MediaVisibility


class MediaBase(BaseModel):
    """Base schema for Media data."""
    filename: str
    media_type: MediaType = MediaType.IMAGE
    visibility: MediaVisibility = MediaVisibility.PRIVATE
    file_metadata: Dict[str, Any] = Field(default_factory=dict)


class MediaCreate(BaseModel):
    """Schema for creating new Media (separate from file upload)."""
    # These fields are directly from the form, not from the base model
    # File will be handled separately
    media_type: MediaType = MediaType.IMAGE
    visibility: MediaVisibility = MediaVisibility.PRIVATE
    file_metadata: Dict[str, Any] = Field(default_factory=dict)


class MediaUpdate(BaseModel):
    """Schema for updating existing Media."""
    filename: Optional[str] = None
    media_type: Optional[MediaType] = None
    visibility: Optional[MediaVisibility] = None
    file_metadata: Optional[Dict[str, Any]] = None
    is_approved: Optional[bool] = None


class MediaInDB(MediaBase):
    """Schema for Media as stored in the database."""
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
    """Schema for Media responses."""
    # URLs for the frontend
    url: str
    thumbnail_url: Optional[str] = None

    @validator("url", "thumbnail_url", pre=True, always=True)
    def set_urls(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        """
        Set URLs based on file_path for frontend consumption.

        Args:
            v: Current value (should be None since this is a computed field)
            values: Values of other fields

        Returns:
            str: URL to the file or thumbnail
        """
        if v is not None:  # If value already set somehow
            return v

        # Only continue if we have file_path
        if "file_path" not in values:
            return None

        file_path = values.get("file_path", "")

        # For thumbnail, check if we're processing thumbnail_url
        is_thumbnail = False
        if values.get("id") and values.get("media_type") == MediaType.IMAGE:
            try:
                current_field = cls.__fields__[next(iter(set(cls.__fields__.keys()) - set(values.keys())))]
                is_thumbnail = current_field.name == "thumbnail_url"
            except (StopIteration, KeyError):
                pass

        # Base URL for media files
        base_url = "/api/v1/media"

        if is_thumbnail:
            return f"{base_url}/thumbnail/{values.get('id')}"
        else:
            return f"{base_url}/file/{values.get('id')}"


class MediaListResponse(BaseModel):
    """Paginated response for media listings."""
    items: List[Media]
    total: int
    page: int
    page_size: int
    pages: int


class FileUploadResponse(BaseModel):
    """Response after file upload."""
    media: Media
    message: str = "File uploaded successfully"


class FileUploadError(BaseModel):
    """Error response for file upload."""
    error: str
    detail: Optional[str] = None
