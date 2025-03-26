# app/domains/media/service/__init__.py
from typing import Optional

from app.domains.media.service.service import MediaService

# Singleton instance
_media_service_instance: Optional[MediaService] = None

# Keep the original async function, but add a sync version
def get_media_service_factory(storage_type: Optional[str] = None) -> MediaService:
    """Get or create a MediaService instance without initialization.

    Args:
        storage_type: Optional storage type

    Returns:
        A non-initialized MediaService instance
    """
    global _media_service_instance

    # Create new instance if none exists or if a new storage type is provided
    if _media_service_instance is None or storage_type is not None:
        _media_service_instance = MediaService(storage_type=storage_type)

    return _media_service_instance

# Keep the original async function for full initialization
async def get_media_service(storage_type: Optional[str] = None) -> MediaService:
    """Get or create an initialized MediaService instance.

    Args:
        storage_type: Optional storage type

    Returns:
        An initialized MediaService instance
    """
    service = get_media_service_factory(storage_type)
    await service.ensure_initialized()
    return service
