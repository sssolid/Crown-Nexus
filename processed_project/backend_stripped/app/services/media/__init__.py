from __future__ import annotations
from app.services.media.service import MediaService
def get_media_service():
    return MediaService()
__all__ = ['get_media_service', 'MediaService']