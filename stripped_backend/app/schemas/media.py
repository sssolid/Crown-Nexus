from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.config import settings
from app.models.media import MediaType, MediaVisibility
class MediaBase(BaseModel):
    filename: str
    media_type: MediaType = MediaType.IMAGE
    visibility: MediaVisibility = MediaVisibility.PRIVATE
    file_metadata: Dict[str, Any] = Field(default_factory=dict)
class MediaCreate(BaseModel):
    media_type: MediaType = MediaType.IMAGE
    visibility: MediaVisibility = MediaVisibility.PRIVATE
    file_metadata: Dict[str, Any] = Field(default_factory=dict)
class MediaUpdate(BaseModel):
    filename: Optional[str] = None
    media_type: Optional[MediaType] = None
    visibility: Optional[MediaVisibility] = None
    file_metadata: Optional[Dict[str, Any]] = None
    is_approved: Optional[bool] = None
class MediaInDB(MediaBase):
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
    url: str = ''
    thumbnail_url: Optional[str] = None
    def model_post_init(self, __context: Any) -> None:
        api_base = f'{settings.API_V1_STR}/media'
        if not self.url:
            self.url = f'{api_base}/file/{self.id}'
        if self.thumbnail_url is None and self.media_type == MediaType.IMAGE:
            self.thumbnail_url = f'{api_base}/thumbnail/{self.id}'
class MediaListResponse(BaseModel):
    items: List[Media]
    total: int
    page: int
    page_size: int
    pages: int
class FileUploadResponse(BaseModel):
    media: Media
    message: str = 'File uploaded successfully'
class FileUploadError(BaseModel):
    error: str
    detail: Optional[str] = None