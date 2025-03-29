from __future__ import annotations
import tempfile
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncGenerator, BinaryIO, Dict, Optional, Set, Union
import aioboto3
import aiofiles
from app.domains.media.service.base import FileNotFoundError, MediaStorageError, StorageConnectionError
from app.domains.media.service.thumbnails import ThumbnailGenerator
from fastapi import UploadFile
from app.core.config import settings
from app.logging import get_logger
from app.domains.media.models import MediaType
logger = get_logger('app.domains.media.service.s3')
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
        if not ThumbnailGenerator.can_generate_thumbnail(file_path):
            return None
        try:
            thumbnail_key = ThumbnailGenerator.get_thumbnail_path(file_path, width, height)
            if await self.file_exists(thumbnail_key):
                return thumbnail_key
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
                await ThumbnailGenerator.generate_thumbnail(original_path, thumbnail_path, width, height)
                async with aiofiles.open(thumbnail_path, 'rb') as f:
                    thumbnail_data = await f.read()
                async with self._client as client:
                    await client.put_object(Bucket=self.bucket_name, Key=thumbnail_key, Body=thumbnail_data, ContentType='image/jpeg')
            logger.info('s3_thumbnail_generated', bucket=self.bucket_name, original_key=file_path, thumbnail_key=thumbnail_key, width=width, height=height)
            return thumbnail_key
        except Exception as e:
            logger.error('s3_thumbnail_generation_failed', bucket=self.bucket_name, original_key=file_path, error=str(e), exc_info=True)
            if isinstance(e, (FileNotFoundError, MediaStorageError)):
                raise
            raise MediaStorageError(f'Failed to generate S3 thumbnail: {str(e)}') from e