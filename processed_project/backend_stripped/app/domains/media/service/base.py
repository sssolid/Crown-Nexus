from __future__ import annotations
from enum import Enum
from typing import BinaryIO, Optional, Protocol, TypedDict, Union
from fastapi import UploadFile
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
    async def save_file(self, file: Union[UploadFile, BinaryIO, bytes], destination: str, media_type: str, content_type: Optional[str]=None) -> str:
        ...
    async def get_file_url(self, file_path: str) -> str:
        ...
    async def delete_file(self, file_path: str) -> bool:
        ...
    async def file_exists(self, file_path: str) -> bool:
        ...
    async def generate_thumbnail(self, file_path: str, width: int=200, height: int=200) -> Optional[str]:
        ...