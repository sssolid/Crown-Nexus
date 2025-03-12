from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, validator
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
    url: str
    thumbnail_url: Optional[str] = None
    @validator('url', 'thumbnail_url', pre=True, always=True)
    def set_urls(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        if v is not None:
            return v
        if 'file_path' not in values or 'id' not in values:
            return None
        is_thumbnail = False
        if values.get('id') and values.get('media_type') == MediaType.IMAGE:
            try:
                current_field = next(iter(set(cls.__fields__.keys()) - set(values.keys())))
                is_thumbnail = current_field == 'thumbnail_url'
            except (StopIteration, KeyError):
                pass
        base_url = '/api/v1/media'
        if is_thumbnail:
            return f"{base_url}/thumbnail/{values.get('id')}"
        else:
            return f"{base_url}/file/{values.get('id')}"
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