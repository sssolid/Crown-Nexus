from typing import Optional
from app.domains.media.service.service import MediaService
_media_service_instance: Optional[MediaService] = None
def get_media_service_factory(storage_type: Optional[str]=None) -> MediaService:
    global _media_service_instance
    if _media_service_instance is None or storage_type is not None:
        _media_service_instance = MediaService(storage_type=storage_type)
    return _media_service_instance
async def get_media_service(storage_type: Optional[str]=None) -> MediaService:
    service = get_media_service_factory(storage_type)
    await service.ensure_initialized()
    return service