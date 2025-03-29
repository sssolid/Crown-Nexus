from __future__ import annotations
from typing import Optional
from app.domains.media.service.base import MediaStorageBackend, StorageBackendType
from app.domains.media.service.local import LocalMediaStorage
from app.domains.media.service.s3 import S3MediaStorage
from app.core.config import settings
from app.logging import get_logger
logger = get_logger('app.domains.media.service.factory')
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