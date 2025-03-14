from __future__ import annotations
import os
import secrets
import uuid
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Dict, List, Optional, Set, Tuple, Union
from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from app.core.config import settings
from app.models.media import MediaType
ALLOWED_MIME_TYPES: Dict[MediaType, Set[str]] = {MediaType.IMAGE: {'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'}, MediaType.DOCUMENT: {'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'text/plain', 'text/csv'}, MediaType.VIDEO: {'video/mp4', 'video/mpeg', 'video/webm', 'video/quicktime'}, MediaType.OTHER: {'application/zip', 'application/x-zip-compressed', 'application/octet-stream'}}
MAX_FILE_SIZES: Dict[MediaType, int] = {MediaType.IMAGE: 5 * 1024 * 1024, MediaType.DOCUMENT: 20 * 1024 * 1024, MediaType.VIDEO: 100 * 1024 * 1024, MediaType.OTHER: 50 * 1024 * 1024}
THUMBNAIL_SIZE: Tuple[int, int] = (300, 300)
def get_media_type_from_mime(mime_type: str) -> MediaType:
    for media_type, mime_types in ALLOWED_MIME_TYPES.items():
        if mime_type in mime_types:
            return media_type
    return MediaType.OTHER
def validate_file(file: UploadFile, allowed_types: Optional[Set[MediaType]]=None) -> Tuple[MediaType, bool]:
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No filename provided')
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    mime_type = file.content_type or 'application/octet-stream'
    media_type = get_media_type_from_mime(mime_type)
    if allowed_types and media_type not in allowed_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File type not allowed. Allowed types: {', '.join((t.value for t in allowed_types))}")
    if mime_type not in ALLOWED_MIME_TYPES[media_type]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'MIME type {mime_type} not allowed for {media_type.value}')
    max_size = MAX_FILE_SIZES[media_type]
    if file_size > max_size:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'File too large. Maximum size for {media_type.value} is {max_size // (1024 * 1024)}MB')
    is_image = media_type == MediaType.IMAGE
    if is_image:
        try:
            file.file.seek(0)
            img = Image.open(file.file)
            img.verify()
            file.file.seek(0)
        except UnidentifiedImageError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid image file')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error validating image: {str(e)}')
    return (media_type, is_image)
def save_upload_file(file: UploadFile, media_id: uuid.UUID, media_type: MediaType, is_image: bool) -> Tuple[str, int, str]:
    upload_dir = Path(settings.MEDIA_ROOT) / str(media_type.value) / datetime.now().strftime('%Y/%m/%d')
    os.makedirs(upload_dir, exist_ok=True)
    original_ext = os.path.splitext(file.filename or 'unknown')[1].lower()
    secure_filename = f'{media_id}{original_ext}'
    file_path = upload_dir / secure_filename
    file.file.seek(0)
    try:
        with open(file_path, 'wb') as f:
            file_content = file.file.read()
            f.write(file_content)
            file_size = len(file_content)
    except IOError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error saving file: {str(e)}')
    media_hash = secrets.token_hex(16)
    if is_image:
        thumbnail_dir = Path(settings.MEDIA_ROOT) / 'thumbnails' / datetime.now().strftime('%Y/%m/%d')
        os.makedirs(thumbnail_dir, exist_ok=True)
        try:
            with Image.open(file_path) as img:
                if img.mode in ['RGBA', 'LA']:
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else img.split()[1])
                    img = rgb_img
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail(THUMBNAIL_SIZE)
                thumbnail_path = thumbnail_dir / secure_filename
                img.save(thumbnail_path, quality=85, optimize=True)
        except Exception as e:
            print(f'Error creating thumbnail: {str(e)}')
    relative_path = str(file_path.relative_to(settings.MEDIA_ROOT))
    return (relative_path, file_size, media_hash)
def get_file_path(file_path: str) -> Path:
    return Path(settings.MEDIA_ROOT) / file_path
def get_thumbnail_path(file_path: str) -> Optional[Path]:
    parts = Path(file_path).parts
    if len(parts) > 1:
        thumbnail_path = Path(settings.MEDIA_ROOT) / 'thumbnails' / '/'.join(parts[1:])
        if thumbnail_path.exists():
            return thumbnail_path
    return None
def get_file_extension(filename: str) -> str:
    if not filename or '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[1].lower()
def is_safe_filename(filename: str) -> bool:
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    if filename.startswith('.'):
        return False
    if len(filename) > 255:
        return False
    return True
def sanitize_filename(filename: str) -> str:
    safe_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.'
    name, ext = os.path.splitext(filename)
    safe_name = ''.join((c for c in name if c in safe_chars))
    if not safe_name:
        safe_name = 'file'
    return safe_name + ext.lower()