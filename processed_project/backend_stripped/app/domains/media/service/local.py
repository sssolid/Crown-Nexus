from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO, Dict, Optional, Set, Tuple, Union
import aiofiles
from app.domains.media.service.base import FileNotFoundError, MediaStorageError
from app.domains.media.service.thumbnails import ThumbnailGenerator
from fastapi import UploadFile
from app.core.config import settings
from app.logging import get_logger
from app.domains.media.models import MediaType
logger = get_logger('app.domains.media.service.local')
@dataclass
class LocalMediaStorage:
    ALLOWED_MIME_TYPES: Dict[MediaType, Set[str]] = field(default_factory=lambda: {MediaType.IMAGE: {'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'}, MediaType.DOCUMENT: {'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/plain', 'text/csv'}, MediaType.VIDEO: {'video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/x-ms-wmv'}, MediaType.OTHER: {'application/zip', 'application/x-zip-compressed', 'application/octet-stream'}})
    MAX_FILE_SIZES: Dict[MediaType, int] = field(default_factory=lambda: {MediaType.IMAGE: 10 * 1024 * 1024, MediaType.DOCUMENT: 50 * 1024 * 1024, MediaType.VIDEO: 500 * 1024 * 1024, MediaType.OTHER: 100 * 1024 * 1024})
    DEFAULT_THUMBNAIL_SIZE: Tuple[int, int] = (300, 300)
    media_root: Path = field(default_factory=lambda: Path(settings.MEDIA_ROOT))
    def __post_init__(self) -> None:
        self.media_root.mkdir(parents=True, exist_ok=True)
        for media_type in MediaType:
            (self.media_root / media_type.value).mkdir(parents=True, exist_ok=True)
        (self.media_root / 'thumbnails').mkdir(parents=True, exist_ok=True)
    async def initialize(self) -> None:
        pass
    async def save_file(self, file: Union[UploadFile, BinaryIO, bytes], destination: str, media_type: MediaType, content_type: Optional[str]=None) -> str:
        if media_type not in MediaType:
            raise ValueError(f'Invalid media type: {media_type}')
        file_content_type = content_type
        if isinstance(file, UploadFile):
            file_content_type = file_content_type or file.content_type
        if file_content_type and media_type != MediaType.OTHER:
            if file_content_type not in self.ALLOWED_MIME_TYPES.get(media_type, set()):
                allowed_types = ', '.join(self.ALLOWED_MIME_TYPES.get(media_type, set()))
                raise ValueError(f"Content type '{file_content_type}' not allowed for {media_type.value}. Allowed types: {allowed_types}")
        file_path = self.media_root / media_type.value / destination
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            if isinstance(file, UploadFile):
                content = await file.read()
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(content)
            elif isinstance(file, bytes):
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(file)
            else:
                content = file.read()
                if not isinstance(content, bytes):
                    content = content.encode('utf-8')
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(content)
            logger.info('file_saved', path=str(file_path), size=file_path.stat().st_size, content_type=file_content_type, media_type=media_type.value)
            return f'{settings.media_base_url}{media_type.value}/{destination}'
        except Exception as e:
            logger.error('file_save_failed', path=str(file_path), error=str(e), exc_info=True)
            raise MediaStorageError(f'Failed to save file: {str(e)}') from e
    async def get_file_url(self, file_path: str) -> str:
        if file_path.startswith('/'):
            file_path = file_path[1:]
        return f'{settings.media_base_url}{file_path}'
    async def delete_file(self, file_path: str) -> bool:
        if file_path.startswith('/'):
            file_path = file_path[1:]
        full_path = self.media_root / file_path
        if not full_path.exists():
            logger.warning('file_not_found', path=str(full_path))
            raise FileNotFoundError(f'File not found: {full_path}')
        try:
            full_path.unlink()
            logger.info('file_deleted', path=str(full_path))
            return True
        except Exception as e:
            logger.error('file_delete_failed', path=str(full_path), error=str(e), exc_info=True)
            raise MediaStorageError(f'Failed to delete file: {str(e)}') from e
    async def file_exists(self, file_path: str) -> bool:
        if file_path.startswith('/'):
            file_path = file_path[1:]
        full_path = self.media_root / file_path
        return full_path.exists()
    async def generate_thumbnail(self, file_path: str, width: int=200, height: int=200) -> Optional[str]:
        if file_path.startswith('/'):
            file_path = file_path[1:]
        if not ThumbnailGenerator.can_generate_thumbnail(file_path):
            return None
        original_path = self.media_root / file_path
        thumbnail_rel_path = ThumbnailGenerator.get_thumbnail_path(file_path, width, height)
        thumbnail_path = self.media_root / thumbnail_rel_path
        try:
            await ThumbnailGenerator.generate_thumbnail(original_path, thumbnail_path, width, height)
            return thumbnail_rel_path
        except Exception as e:
            logger.error('thumbnail_generation_failed', original_path=file_path, width=width, height=height, error=str(e), exc_info=True)
            if isinstance(e, FileNotFoundError):
                raise
            raise MediaStorageError(f'Thumbnail generation failed: {str(e)}') from e