from __future__ import annotations
'Media schema definitions.\n\nThis module defines Pydantic schemas for Media objects,\nincluding creation, update, and response models.\n'
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domains.media.models import MediaType, MediaVisibility
from app.core.config import settings
class MediaBase(BaseModel):
    filename: str = Field(..., description='Original filename')
    media_type: MediaType = Field(MediaType.IMAGE, description='Type of media content')
    visibility: MediaVisibility = Field(MediaVisibility.PRIVATE, description='Visibility setting')
    file_metadata: Dict[str, Any] = Field(default_factory=dict, description='Additional file metadata')
class MediaCreate(BaseModel):
    media_type: MediaType = Field(MediaType.IMAGE, description='Type of media content')
    visibility: MediaVisibility = Field(MediaVisibility.PRIVATE, description='Visibility setting')
    file_metadata: Dict[str, Any] = Field(default_factory=dict, description='Additional file metadata')
class MediaUpdate(BaseModel):
    filename: Optional[str] = Field(None, description='Original filename')
    media_type: Optional[MediaType] = Field(None, description='Type of media content')
    visibility: Optional[MediaVisibility] = Field(None, description='Visibility setting')
    file_metadata: Optional[Dict[str, Any]] = Field(None, description='Additional file metadata')
    is_approved: Optional[bool] = Field(None, description='Approval status')
class MediaInDB(MediaBase):
    id: uuid.UUID = Field(..., description='Unique identifier')
    file_path: str = Field(..., description='Path to the stored file')
    file_size: int = Field(..., description='File size in bytes')
    mime_type: str = Field(..., description='MIME type of the file')
    uploaded_by_id: uuid.UUID = Field(..., description='ID of the user who uploaded the file')
    is_approved: bool = Field(..., description='Whether the media has been approved')
    approved_by_id: Optional[uuid.UUID] = Field(None, description='ID of the user who approved the media')
    approved_at: Optional[datetime] = Field(None, description='When the media was approved')
    created_at: datetime = Field(..., description='Creation timestamp')
    updated_at: datetime = Field(..., description='Last update timestamp')
    model_config = ConfigDict(from_attributes=True)
class Media(MediaInDB):
    url: str = Field('', description='URL to access the file')
    thumbnail_url: Optional[str] = Field(None, description='URL to access the thumbnail')
    def model_post_init(self, __context: Any) -> None:
        api_base = f'{settings.API_V1_STR}/media'
        if not self.url:
            self.url = f'{api_base}/file/{self.id}'
        if self.thumbnail_url is None and self.media_type == MediaType.IMAGE:
            self.thumbnail_url = f'{api_base}/thumbnail/{self.id}'
class MediaListResponse(BaseModel):
    items: List[Media] = Field(..., description='List of media items')
    total: int = Field(..., description='Total number of items')
    page: int = Field(..., description='Current page number')
    page_size: int = Field(..., description='Number of items per page')
    pages: int = Field(..., description='Total number of pages')
class FileUploadResponse(BaseModel):
    media: Media = Field(..., description='Uploaded media details')
    message: str = Field('File uploaded successfully', description='Response message')
class FileUploadError(BaseModel):
    error: str = Field(..., description='Error message')
    detail: Optional[str] = Field(None, description='Detailed error information')