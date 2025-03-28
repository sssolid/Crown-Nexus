from __future__ import annotations
import asyncio
from pathlib import Path
from typing import Tuple
from app.domains.media.service.base import FileNotFoundError, MediaStorageError
from app.logging import get_logger
logger = get_logger('app.domains.media.service.thumbnails')
class ThumbnailGenerator:
    @staticmethod
    async def generate_thumbnail(file_path: Path, output_path: Path, width: int=200, height: int=200, quality: int=90) -> None:
        if not file_path.exists():
            raise FileNotFoundError(f'Original image not found: {file_path}')
        await asyncio.to_thread(ThumbnailGenerator._generate_thumbnail_sync, file_path, output_path, width, height, quality)
    @staticmethod
    def _generate_thumbnail_sync(file_path: Path, output_path: Path, width: int, height: int, quality: int) -> None:
        try:
            from PIL import Image, UnidentifiedImageError
        except ImportError:
            raise MediaStorageError("Pillow library not installed. Please install with 'pip install Pillow'")
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(file_path) as img:
                if img.mode in ['RGBA', 'LA']:
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else img.split()[1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail((width, height), Image.LANCZOS)
                img.save(output_path, format='JPEG', quality=quality, optimize=True)
            logger.info('thumbnail_generated', original=str(file_path), thumbnail=str(output_path), width=width, height=height)
        except UnidentifiedImageError:
            raise MediaStorageError(f'Not a valid image file: {file_path}')
        except Exception as e:
            raise MediaStorageError(f'Error generating thumbnail: {str(e)}') from e
    @staticmethod
    def get_supported_formats() -> Tuple[str, ...]:
        return ('.jpg', '.jpeg', '.png', '.gif', '.webp')
    @staticmethod
    def can_generate_thumbnail(file_path: str) -> bool:
        return any((file_path.lower().endswith(ext) for ext in ThumbnailGenerator.get_supported_formats()))
    @staticmethod
    def get_thumbnail_path(original_path: str, width: int=200, height: int=200, thumbnails_dir: str='thumbnails') -> str:
        filename = Path(original_path).name
        thumbnail_name = f'thumb_{width}x{height}_{filename}'
        return f'{thumbnails_dir}/{thumbnail_name}'