from __future__ import annotations
import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, AsyncGenerator, BinaryIO, Dict, List, Literal, Optional, Protocol, Set, Tuple, TypedDict, Union
import aiofiles
import aioboto3
from fastapi import HTTPException, UploadFile, status
from pydantic import BaseModel, Field, ValidationError
from app.core.config import Environment, settings
from app.models.media import MediaType, MediaVisibility
import structlog
logger = structlog.get_logger(__name__)
class StorageBackendType(str, Enum):
    LOCAL = 'local'
    S3 = 's3'
    AZURE = 'azure'
class FileMetadata(TypedDict, total=False):
    width: Optional[int]
    height: Optional[int]
    content_type: str
    file_size: int
    original_filename: str
    created_at: str
class MediaStorageError(Exception):
    pass
class FileNotFoundError(MediaStorageError):
    pass
class StorageConnectionError(MediaStorageError):
    pass
class MediaStorageBackend(Protocol):
    async def initialize(self) -> None:
        ...
    async def save_file(self, file: Union[UploadFile, BinaryIO, bytes], destination: str, media_type: MediaType, content_type: Optional[str]=None) -> str:
        ...
    async def get_file_url(self, file_path: str) -> str:
        ...
    async def delete_file(self, file_path: str) -> bool:
        ...
    async def file_exists(self, file_path: str) -> bool:
        ...
    async def generate_thumbnail(self, file_path: str, width: int=200, height: int=200) -> Optional[str]:
        ...
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
        try:
            return await asyncio.to_thread(self._generate_thumbnail_sync, file_path, width, height)
        except Exception as e:
            logger.error('thumbnail_generation_failed', original_path=file_path, width=width, height=height, error=str(e), exc_info=True)
            if isinstance(e, FileNotFoundError):
                raise
            raise MediaStorageError(f'Thumbnail generation failed: {str(e)}') from e
    def _generate_thumbnail_sync(self, file_path: str, width: int=200, height: int=200) -> str:
        try:
            from PIL import Image, UnidentifiedImageError
        except ImportError:
            raise MediaStorageError("Pillow library not installed. Please install with 'pip install Pillow'")
        if file_path.startswith('/'):
            file_path = file_path[1:]
        original_path = self.media_root / file_path
        if not original_path.exists():
            logger.warning('original_image_not_found', path=str(original_path))
            raise FileNotFoundError(f'Original image not found: {original_path}')
        try:
            filename = original_path.name
            thumbnail_name = f'thumb_{width}x{height}_{filename}'
            thumbnail_rel_path = f'thumbnails/{thumbnail_name}'
            thumbnail_path = self.media_root / 'thumbnails' / thumbnail_name
            thumbnail_path.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(original_path) as img:
                if img.mode in ['RGBA', 'LA']:
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else img.split()[1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail((width, height), Image.LANCZOS)
                img.save(thumbnail_path, format='JPEG', quality=90, optimize=True)
            logger.info('thumbnail_generated', original=str(original_path), thumbnail=str(thumbnail_path), width=width, height=height)
            return thumbnail_rel_path
        except UnidentifiedImageError:
            raise MediaStorageError(f'Not a valid image file: {original_path}')
        except Exception as e:
            raise MediaStorageError(f'Error generating thumbnail: {str(e)}') from e
@dataclass
class S3MediaStorage:
    bucket_name: str = field(default_factory=lambda: settings.AWS_STORAGE_BUCKET_NAME)
    region_name: str = field(default_factory=lambda: settings.AWS_REGION)
    access_key_id: Optional[str] = field(default_factory=lambda: settings.AWS_ACCESS_KEY_ID)
    secret_access_key: Optional[str] = field(default_factory=lambda: settings.AWS_SECRET_ACCESS_KEY)
    endpoint_url: Optional[str] = field(default_factory=lambda: settings.AWS_S3_ENDPOINT_URL)
    cdn_url: Optional[str] = field(default_factory=lambda: settings.MEDIA_CDN_URL)
    _session: Optional[Any] = None
    _client: Optional[Any] = None
    _resource: Optional[Any] = None
    ALLOWED_MIME_TYPES: Dict[MediaType, Set[str]] = field(default_factory=lambda: {MediaType.IMAGE: {'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'}, MediaType.DOCUMENT: {'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/plain', 'text/csv'}, MediaType.VIDEO: {'video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/x-ms-wmv'}, MediaType.OTHER: {'application/zip', 'application/x-zip-compressed', 'application/octet-stream'}})
    MAX_FILE_SIZES: Dict[MediaType, int] = field(default_factory=lambda: {MediaType.IMAGE: 10 * 1024 * 1024, MediaType.DOCUMENT: 50 * 1024 * 1024, MediaType.VIDEO: 500 * 1024 * 1024, MediaType.OTHER: 100 * 1024 * 1024})
    async def initialize(self) -> None:
        try:
            self._session = aioboto3.Session(aws_access_key_id=self.access_key_id, aws_secret_access_key=self.secret_access_key, region_name=self.region_name)
            self._client = self._session.client('s3', endpoint_url=self.endpoint_url)
            self._resource = self._session.resource('s3', endpoint_url=self.endpoint_url)
            async with self._client as client:
                try:
                    await client.head_bucket(Bucket=self.bucket_name)
                    logger.info('s3_bucket_exists', bucket=self.bucket_name)
                except Exception:
                    await client.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={'LocationConstraint': self.region_name})
                    logger.info('s3_bucket_created', bucket=self.bucket_name)
            logger.info('s3_storage_initialized', bucket=self.bucket_name, region=self.region_name)
        except Exception as e:
            logger.error('s3_initialization_failed', bucket=self.bucket_name, error=str(e), exc_info=True)
            raise StorageConnectionError(f'Failed to initialize S3 storage: {str(e)}') from e
    async def save_file(self, file: Union[UploadFile, BinaryIO, bytes], destination: str, media_type: MediaType, content_type: Optional[str]=None) -> str:
        if not self._client:
            await self.initialize()
        if media_type not in MediaType:
            raise ValueError(f'Invalid media type: {media_type}')
        s3_key = f'{media_type.value}/{destination}'
        file_content_type = content_type
        if isinstance(file, UploadFile):
            file_content_type = file_content_type or file.content_type
        if file_content_type and media_type != MediaType.OTHER:
            if file_content_type not in self.ALLOWED_MIME_TYPES.get(media_type, set()):
                allowed_types = ', '.join(self.ALLOWED_MIME_TYPES.get(media_type, set()))
                raise ValueError(f"Content type '{file_content_type}' not allowed for {media_type.value}. Allowed types: {allowed_types}")
        try:
            if isinstance(file, UploadFile):
                content = await file.read()
            elif isinstance(file, bytes):
                content = file
            else:
                content = file.read()
                if not isinstance(content, bytes):
                    content = content.encode('utf-8')
            extra_args = {}
            if file_content_type:
                extra_args['ContentType'] = file_content_type
            async with self._client as client:
                await client.put_object(Bucket=self.bucket_name, Key=s3_key, Body=content, **extra_args)
            logger.info('s3_file_saved', bucket=self.bucket_name, key=s3_key, size=len(content), content_type=file_content_type, media_type=media_type.value)
            return await self.get_file_url(s3_key)
        except Exception as e:
            logger.error('s3_file_save_failed', bucket=self.bucket_name, key=s3_key, error=str(e), exc_info=True)
            raise MediaStorageError(f'Failed to save file to S3: {str(e)}') from e
    async def get_file_url(self, file_path: str) -> str:
        if file_path.startswith('/'):
            file_path = file_path[1:]
        if self.cdn_url:
            return f"{self.cdn_url.rstrip('/')}/{file_path}"
        region_url = f'.{self.region_name}' if self.region_name else ''
        return f'https://{self.bucket_name}.s3{region_url}.amazonaws.com/{file_path}'
    async def delete_file(self, file_path: str) -> bool:
        if not self._client:
            await self.initialize()
        if file_path.startswith('/'):
            file_path = file_path[1:]
        try:
            if not await self.file_exists(file_path):
                logger.warning('s3_file_not_found', bucket=self.bucket_name, key=file_path)
                raise FileNotFoundError(f'File not found in S3: {file_path}')
            async with self._client as client:
                await client.delete_object(Bucket=self.bucket_name, Key=file_path)
            logger.info('s3_file_deleted', bucket=self.bucket_name, key=file_path)
            return True
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                raise
            logger.error('s3_file_delete_failed', bucket=self.bucket_name, key=file_path, error=str(e), exc_info=True)
            raise MediaStorageError(f'Failed to delete file from S3: {str(e)}') from e
    async def file_exists(self, file_path: str) -> bool:
        if not self._client:
            await self.initialize()
        if file_path.startswith('/'):
            file_path = file_path[1:]
        try:
            async with self._client as client:
                await client.head_object(Bucket=self.bucket_name, Key=file_path)
            return True
        except Exception:
            return False
    async def generate_thumbnail(self, file_path: str, width: int=200, height: int=200) -> Optional[str]:
        if not self._client:
            await self.initialize()
        if file_path.startswith('/'):
            file_path = file_path[1:]
        if not file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            return None
        try:
            from PIL import Image, UnidentifiedImageError
        except ImportError:
            raise MediaStorageError("Pillow library not installed. Please install with 'pip install Pillow'")
        filename = Path(file_path).name
        thumbnail_name = f'thumb_{width}x{height}_{filename}'
        thumbnail_key = f'thumbnails/{thumbnail_name}'
        try:
            if await self.file_exists(thumbnail_key):
                return thumbnail_key
            import tempfile
            from contextlib import asynccontextmanager
            @asynccontextmanager
            async def temp_file() -> AsyncGenerator[Path, None]:
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp_path = Path(tmp.name)
                try:
                    yield tmp_path
                finally:
                    if tmp_path.exists():
                        tmp_path.unlink()
            async with self._client as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=file_path)
                body = await response['Body'].read()
            async with temp_file() as original_path, temp_file() as thumbnail_path:
                async with aiofiles.open(original_path, 'wb') as f:
                    await f.write(body)
                await asyncio.to_thread(self._generate_thumbnail_sync, original_path, thumbnail_path, width, height)
                async with aiofiles.open(thumbnail_path, 'rb') as f:
                    thumbnail_data = await f.read()
                async with self._client as client:
                    await client.put_object(Bucket=self.bucket_name, Key=thumbnail_key, Body=thumbnail_data, ContentType='image/jpeg')
            logger.info('s3_thumbnail_generated', bucket=self.bucket_name, original_key=file_path, thumbnail_key=thumbnail_key, width=width, height=height)
            return thumbnail_key
        except Exception as e:
            logger.error('s3_thumbnail_generation_failed', bucket=self.bucket_name, original_key=file_path, thumbnail_key=thumbnail_key, error=str(e), exc_info=True)
            if isinstance(e, (FileNotFoundError, MediaStorageError)):
                raise
            raise MediaStorageError(f'Failed to generate S3 thumbnail: {str(e)}') from e
    def _generate_thumbnail_sync(self, original_path: Path, thumbnail_path: Path, width: int, height: int) -> None:
        try:
            from PIL import Image
            with Image.open(original_path) as img:
                if img.mode in ['RGBA', 'LA']:
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else img.split()[1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail((width, height), Image.LANCZOS)
                img.save(thumbnail_path, format='JPEG', quality=90, optimize=True)
        except Exception as e:
            raise MediaStorageError(f'Error generating thumbnail: {str(e)}') from e
@dataclass
class MediaService:
    storage_type: StorageBackendType = field(default_factory=lambda: StorageBackendType(settings.MEDIA_STORAGE_TYPE.lower()))
    storage: Optional[MediaStorageBackend] = None
    initialized: bool = False
    async def initialize(self) -> None:
        if self.initialized:
            return
        logger.info('media_service_initializing', storage_type=self.storage_type)
        if self.storage_type == StorageBackendType.S3:
            self.storage = S3MediaStorage()
        else:
            self.storage = LocalMediaStorage()
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
media_service = MediaService()