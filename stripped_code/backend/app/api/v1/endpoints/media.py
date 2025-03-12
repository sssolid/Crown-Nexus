from __future__ import annotations
import json
import os
from datetime import datetime
from typing import Annotated, Any, List, Optional, Set
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, Response, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.core.config import settings
from app.models.media import Media, MediaType, MediaVisibility
from app.models.product import Product, product_media_association
from app.models.user import User
from app.schemas.media import FileUploadResponse, Media as MediaSchema, MediaCreate, MediaListResponse, MediaUpdate
from app.utils.file import get_file_path, get_thumbnail_path, save_upload_file, validate_file
router = APIRouter()
@router.post('/upload', response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(background_tasks: BackgroundTasks, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], file: UploadFile=File(...), media_type: MediaType=Form(MediaType.IMAGE), visibility: MediaVisibility=Form(MediaVisibility.PRIVATE), metadata: str=Form('{}'), product_id: Optional[str]=Form(None)) -> Any:
    try:
        determined_media_type, is_image = validate_file(file, {media_type})
        try:
            parsed_metadata = json.loads(metadata)
            if not isinstance(parsed_metadata, dict):
                parsed_metadata = {}
        except (json.JSONDecodeError, TypeError):
            parsed_metadata = {}
        media = Media(filename=file.filename or 'unknown', file_path='pending', file_size=0, media_type=determined_media_type, mime_type=file.content_type or 'application/octet-stream', visibility=visibility, file_metadata=parsed_metadata, uploaded_by_id=current_user.id, is_approved=current_user.role in ['admin', 'manager'])
        if media.is_approved:
            media.approved_by_id = current_user.id
            media.approved_at = datetime.now()
        db.add(media)
        await db.commit()
        await db.refresh(media)
        file_path, file_size, _ = save_upload_file(file, media.id, determined_media_type, is_image)
        media.file_path = file_path
        media.file_size = file_size
        if product_id:
            stmt = select(Product).where(Product.id == product_id)
            result = await db.execute(stmt)
            product = result.scalar_one_or_none()
            if product:
                stmt = product_media_association.insert().values(product_id=product_id, media_id=media.id)
                await db.execute(stmt)
        await db.commit()
        await db.refresh(media)
        response_media = MediaSchema.model_validate(media)
        return {'media': response_media, 'message': 'File uploaded successfully'}
    except HTTPException as e:
        if 'media' in locals() and hasattr(media, 'id'):
            await db.delete(media)
            await db.commit()
        raise e
    except Exception as e:
        if 'media' in locals() and hasattr(media, 'id'):
            await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error uploading file: {str(e)}')
@router.get('/', response_model=MediaListResponse)
async def read_media(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], media_type: Optional[MediaType]=None, visibility: Optional[MediaVisibility]=None, is_approved: Optional[bool]=None, product_id: Optional[str]=None, page: int=1, page_size: int=20) -> Any:
    pagination = get_pagination(page, page_size)
    skip = pagination['skip']
    limit = pagination['limit']
    query = select(Media)
    if media_type:
        query = query.where(Media.media_type == media_type)
    if visibility:
        query = query.where(Media.visibility == visibility)
    if is_approved is not None:
        query = query.where(Media.is_approved == is_approved)
    if product_id:
        query = query.join(product_media_association).where(product_media_association.c.product_id == product_id)
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    media_items = result.scalars().all()
    pages = (total + limit - 1) // limit if limit > 0 else 0
    media_schemas = [MediaSchema.model_validate(media) for media in media_items]
    return {'items': media_schemas, 'total': total, 'page': pagination['page'], 'page_size': pagination['page_size'], 'pages': pages}
@router.get('/{media_id}', response_model=MediaSchema)
async def read_media_item(media_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)]) -> Any:
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Media not found')
    if media.visibility == MediaVisibility.PRIVATE and media.uploaded_by_id != current_user.id and (current_user.role not in ['admin', 'manager']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to access this media")
    return MediaSchema.model_validate(media)
@router.put('/{media_id}', response_model=MediaSchema)
async def update_media(media_id: str, media_in: MediaUpdate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)]) -> Any:
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Media not found')
    if media.uploaded_by_id != current_user.id and current_user.role not in ['admin', 'manager']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this media")
    was_approved = media.is_approved
    update_data = media_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(media, field, value)
    if not was_approved and media.is_approved and (current_user.role in ['admin', 'manager']):
        media.approved_by_id = current_user.id
        media.approved_at = datetime.now()
    await db.commit()
    await db.refresh(media)
    return MediaSchema.model_validate(media)
@router.delete('/{media_id}')
async def delete_media(media_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)]) -> dict:
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Media not found')
    if media.uploaded_by_id != current_user.id and current_user.role not in ['admin', 'manager']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this media")
    file_path = get_file_path(media.file_path)
    thumbnail_path = get_thumbnail_path(media.file_path)
    await db.delete(media)
    await db.commit()
    try:
        if file_path.exists():
            os.remove(file_path)
        if thumbnail_path and thumbnail_path.exists():
            os.remove(thumbnail_path)
    except Exception as e:
        print(f'Error deleting files for media {media_id}: {str(e)}')
    return {'message': 'Media deleted successfully'}
@router.get('/file/{media_id}')
async def get_media_file(media_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Optional[User]=Depends(get_current_active_user)) -> Any:
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Media not found')
    if media.visibility == MediaVisibility.PRIVATE:
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication required to access this file')
        if media.uploaded_by_id != current_user.id and current_user.role not in ['admin', 'manager']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to access this file")
    file_path = get_file_path(media.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found on server')
    return FileResponse(path=str(file_path), filename=media.filename, media_type=media.mime_type)
@router.get('/thumbnail/{media_id}')
async def get_media_thumbnail(media_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Optional[User]=Depends(get_current_active_user)) -> Any:
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Media not found')
    if media.media_type != MediaType.IMAGE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Thumbnails are only available for images')
    if media.visibility == MediaVisibility.PRIVATE:
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication required to access this file')
        if media.uploaded_by_id != current_user.id and current_user.role not in ['admin', 'manager']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to access this file")
    thumbnail_path = get_thumbnail_path(media.file_path)
    if not thumbnail_path or not thumbnail_path.exists():
        file_path = get_file_path(media.file_path)
        if not file_path.exists():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found on server')
        return FileResponse(path=str(file_path), filename=media.filename, media_type=media.mime_type)
    return FileResponse(path=str(thumbnail_path), filename=f'thumb_{media.filename}', media_type=media.mime_type)
@router.post('/{media_id}/products/{product_id}')
async def associate_media_with_product(media_id: str, product_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Media not found')
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    stmt = select(product_media_association).where((product_media_association.c.product_id == product_id) & (product_media_association.c.media_id == media_id))
    result = await db.execute(stmt)
    if result.first():
        return {'message': 'Media already associated with product'}
    stmt = product_media_association.insert().values(product_id=product_id, media_id=media_id)
    await db.execute(stmt)
    await db.commit()
    return {'message': 'Media associated with product successfully'}
@router.delete('/{media_id}/products/{product_id}')
async def remove_media_from_product(media_id: str, product_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    stmt = select(product_media_association).where((product_media_association.c.product_id == product_id) & (product_media_association.c.media_id == media_id))
    result = await db.execute(stmt)
    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Association between media and product not found')
    stmt = product_media_association.delete().where((product_media_association.c.product_id == product_id) & (product_media_association.c.media_id == media_id))
    await db.execute(stmt)
    await db.commit()
    return {'message': 'Media disassociated from product successfully'}
@router.get('/products/{product_id}', response_model=List[MediaSchema])
async def get_product_media(product_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], media_type: Optional[MediaType]=None) -> Any:
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    query = select(Media).join(product_media_association).where(product_media_association.c.product_id == product_id)
    if media_type:
        query = query.where(Media.media_type == media_type)
    result = await db.execute(query)
    media_items = result.scalars().all()
    return [MediaSchema.model_validate(media) for media in media_items]