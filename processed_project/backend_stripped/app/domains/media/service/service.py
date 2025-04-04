from __future__ import annotations
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from app.domains.media.service.base import FileNotFoundError, MediaStorageBackend, MediaStorageError, StorageBackendType
from app.domains.media.service.factory import StorageBackendFactory
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings
from app.logging import get_logger
from app.domains.media.models import MediaType, MediaVisibility
from app.services.interfaces import ServiceInterface
logger = get_logger('app.domains.media.service.service')
class MediaService(ServiceInterface):
    def __init__(self, storage_type: Optional[str]=None):
        self.storage_type = StorageBackendType(storage_type.lower()) if storage_type else StorageBackendType(settings.MEDIA_STORAGE_TYPE.lower())
        self.storage: Optional[MediaStorageBackend] = None
        self.initialized = False
    async def initialize(self) -> None:
        if self.initialized:
            return
        logger.info('media_service_initializing', storage_type=self.storage_type)
        self.storage = StorageBackendFactory.get_backend(self.storage_type.value)
        await self.storage.initialize()
        self.initialized = True
        logger.info('media_service_initialized', storage_type=self.storage_type)
    async def ensure_initialized(self) -> None:
        if not self.initialized or not self.storage:
            await self.initialize()
    async def upload_file(self, file: UploadFile, media_type: MediaType, product_id: Optional[str]=None, filename: Optional[str]=None, visibility: MediaVisibility=MediaVisibility.PRIVATE, generate_thumbnail: bool=True) -> Tuple[str, Dict[str, Any], Optional[str]]:
        await self.ensure_initialized()
        try:
            if not file.filename:
                raise ValueError('No filename provided')
            safe_filename = self._sanitize_filename(filename or file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            ext = Path(safe_filename).suffix
            unique_filename = f'{timestamp}_{uuid.uuid4().hex}{ext}'
            if product_id:
                destination = f'{product_id}/{unique_filename}'
            else:
                date_path = datetime.now().strftime('%Y/%m/%d')
                destination = f'{date_path}/{unique_filename}'
            content_type = file.content_type or self._guess_content_type(safe_filename)
            metadata: Dict[str, Any] = {'original_filename': safe_filename, 'content_type': content_type, 'visibility': visibility.value, 'product_id': product_id, 'uploaded_at': datetime.now().isoformat()}
            file_url = await self.storage.save_file(file, destination, media_type, content_type)
            thumbnail_url = None
            if generate_thumbnail and media_type == MediaType.IMAGE and (content_type in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']) and (not content_type.endswith('svg+xml')):
                rel_path = f'{media_type.value}/{destination}'
                thumbnail_path = await self.storage.generate_thumbnail(rel_path)
                if thumbnail_path:
                    thumbnail_url = await self.storage.get_file_url(thumbnail_path)
            return (file_url, metadata, thumbnail_url)
        except ValueError as e:
            logger.warning('file_upload_validation_failed', filename=getattr(file, 'filename', 'unknown'), error=str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
        except MediaStorageError as e:
            logger.error('file_upload_storage_failed', filename=getattr(file, 'filename', 'unknown'), error=str(e), exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Storage error: {str(e)}') from e
        except Exception as e:
            logger.error('file_upload_unexpected_error', filename=getattr(file, 'filename', 'unknown'), error=str(e), exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Unexpected error: {str(e)}') from e
    async def delete_file(self, file_url: str) -> bool:
        await self.ensure_initialized()
        try:
            media_url = settings.media_base_url
            if file_url.startswith(media_url):
                rel_path = file_url[len(media_url):]
            else:
                from urllib.parse import urlparse
                parsed_url = urlparse(file_url)
                rel_path = parsed_url.path
                if rel_path.startswith(settings.MEDIA_URL):
                    rel_path = rel_path[len(settings.MEDIA_URL):]
                if rel_path.startswith('/'):
                    rel_path = rel_path[1:]
            if not await self.storage.file_exists(rel_path):
                logger.warning('file_not_found_for_deletion', path=rel_path)
                return False
            result = await self.storage.delete_file(rel_path)
            try:
                if any((ext in rel_path.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'])):
                    filename = Path(rel_path).name
                    thumb_patterns = [f'thumbnails/thumb_{filename}', f'thumbnails/thumb_200x200_{filename}', f'thumbnails/thumb_300x300_{filename}']
                    for pattern in thumb_patterns:
                        if await self.storage.file_exists(pattern):
                            await self.storage.delete_file(pattern)
            except Exception as e:
                logger.warning('thumbnail_deletion_failed', original_path=rel_path, error=str(e))
            return result
        except FileNotFoundError:
            return False
        except MediaStorageError as e:
            logger.error('file_deletion_storage_failed', url=file_url, error=str(e), exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Storage error: {str(e)}') from e
        except Exception as e:
            logger.error('file_deletion_unexpected_error', url=file_url, error=str(e), exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Unexpected error: {str(e)}') from e
    def _sanitize_filename(self, filename: str) -> str:
        safe_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.'
        name, ext = os.path.splitext(filename)
        safe_name = ''.join((c for c in name if c in safe_chars))
        if not safe_name:
            safe_name = 'file'
        safe_ext = ext.lower() if ext and all((c in safe_chars for c in ext)) else ext
        return safe_name + safe_ext
    def _guess_content_type(self, filename: str) -> str:
        import mimetypes
        mimetypes.init()
        content_type, _ = mimetypes.guess_type(filename)
        return content_type or 'application/octet-stream'
    async def shutdown(self) -> None:
        logger.info('Shutting down media service')