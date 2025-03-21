from __future__ import annotations
from typing import Optional, Type
from app.core.config import settings
from app.core.logging import get_logger
from app.services.media.base import MediaStorageBackend, StorageBackendType
from app.services.media.local import LocalMediaStorage
from app.services.media.s3 import S3MediaStorage
logger = get_logger(__name__)
class StorageBackendFactory:
    @staticmethod
    def get_backend(backend_type: Optional[str]=None) -> MediaStorageBackend:
        if backend_type is None:
            backend_type = settings.MEDIA_STORAGE_TYPE.lower()
        try:
            backend_enum = StorageBackendType(backend_type)
            backend_type = backend_enum.value
        except ValueError:
            valid_types = [t.value for t in StorageBackendType]
            logger.error(f"Invalid storage backend type: {backend_type}. Valid types are: {', '.join(valid_types)}")
            backend_type = StorageBackendType.LOCAL.value
            logger.warning(f'Defaulting to {backend_type} storage')
        if backend_type == StorageBackendType.S3.value:
            logger.info('Creating S3 storage backend')
            return S3MediaStorage()
        elif backend_type == StorageBackendType.AZURE.value:
            logger.warning('Azure storage not implemented, using local storage instead')
            return LocalMediaStorage()
        else:
            logger.info('Creating local storage backend')
            return LocalMediaStorage()