from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Annotated, Any, List, Optional, Set

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination, get_optional_user
from app.core.config import settings
from app.models.media import Media, MediaType, MediaVisibility
from app.models.product import Product, product_media_association
from app.models.user import User
from app.schemas.media import (
    FileUploadResponse,
    Media as MediaSchema,
    MediaCreate,
    MediaListResponse,
    MediaUpdate,
)
from app.utils.file import (
    get_file_path,
    get_thumbnail_path,
    save_upload_file,
    validate_file,
)

router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    file: UploadFile = File(...),
    media_type: MediaType = Form(MediaType.IMAGE),
    visibility: MediaVisibility = Form(MediaVisibility.PRIVATE),
    metadata: str = Form("{}"),
    product_id: Optional[str] = Form(None),
) -> Any:
    """
    Upload a new file.

    Args:
        background_tasks: Background tasks
        db: Database session
        current_user: Current authenticated user
        file: Uploaded file
        media_type: Type of media
        visibility: Visibility level
        metadata: Additional metadata as JSON string
        product_id: ID of product to associate with the media

    Returns:
        FileUploadResponse: Response with the created media
    """
    try:
        # Validate the file
        determined_media_type, is_image = validate_file(file, {media_type})

        # Parse metadata JSON
        try:
            parsed_metadata = json.loads(metadata)
            if not isinstance(parsed_metadata, dict):
                parsed_metadata = {}
        except (json.JSONDecodeError, TypeError):
            parsed_metadata = {}

        # Create initial media record
        media = Media(
            filename=file.filename or "unknown",
            file_path="pending",  # Temporary path, will be updated
            file_size=0,  # Temporary size, will be updated
            media_type=determined_media_type,
            mime_type=file.content_type or "application/octet-stream",
            visibility=visibility,
            file_metadata=parsed_metadata,  # Using renamed field
            uploaded_by_id=current_user.id,
            is_approved=current_user.role in ["admin", "manager"],  # Auto-approve for admins/managers
        )

        if media.is_approved:
            media.approved_by_id = current_user.id
            media.approved_at = datetime.now()

        db.add(media)
        await db.commit()
        await db.refresh(media)

        # Now save the file with the media ID
        file_path, file_size, _ = save_upload_file(
            file,
            media.id,
            determined_media_type,
            is_image
        )

        # Update the media record with the actual file path and size
        media.file_path = file_path
        media.file_size = file_size

        # Associate with product if provided
        if product_id:
            stmt = select(Product).where(Product.id == product_id)
            result = await db.execute(stmt)
            product = result.scalar_one_or_none()

            if product:
                # Create association
                stmt = product_media_association.insert().values(
                    product_id=product_id,
                    media_id=media.id
                )
                await db.execute(stmt)

        await db.commit()
        await db.refresh(media)

        # Create response object with explicit URLs
        response_media = MediaSchema.model_validate(media)

        # Ensure URLs are set correctly
        response_media.url = f"/api/v1/media/file/{media.id}"
        if media.media_type == MediaType.IMAGE:
            response_media.thumbnail_url = f"/api/v1/media/thumbnail/{media.id}"

        return {
            "media": response_media,
            "message": "File uploaded successfully"
        }
    except HTTPException as e:
        # If we've already created the media record but encounter an error, delete it
        if 'media' in locals() and hasattr(media, 'id'):
            await db.delete(media)
            await db.commit()
        raise e
    except Exception as e:
        # For any other exception, roll back and re-raise
        if 'media' in locals() and hasattr(media, 'id'):
            await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}",
        )


@router.get("/", response_model=MediaListResponse)
async def read_media(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    media_type: Optional[MediaType] = None,
    visibility: Optional[MediaVisibility] = None,
    is_approved: Optional[bool] = None,
    product_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Any:
    """
    Retrieve media with filtering options.

    Args:
        db: Database session
        current_user: Current authenticated user
        media_type: Filter by media type
        visibility: Filter by visibility
        is_approved: Filter by approval status
        product_id: Filter by associated product
        page: Page number
        page_size: Number of items per page

    Returns:
        MediaListResponse: Paginated list of media
    """
    # Pagination parameters
    pagination = get_pagination(page, page_size)
    skip = pagination["skip"]
    limit = pagination["limit"]

    # Base query
    query = select(Media)

    # Apply filters
    if media_type:
        query = query.where(Media.media_type == media_type)

    if visibility:
        query = query.where(Media.visibility == visibility)

    if is_approved is not None:
        query = query.where(Media.is_approved == is_approved)

    # Filter by product if provided
    if product_id:
        query = (
            query
            .join(product_media_association)
            .where(product_media_association.c.product_id == product_id)
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Apply pagination and load relationships
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    media_items = result.scalars().all()

    # Calculate total pages
    pages = (total + limit - 1) // limit if limit > 0 else 0

    # Convert models to schemas with URLs
    media_schemas = [MediaSchema.model_validate(media) for media in media_items]

    return {
        "items": media_schemas,
        "total": total,
        "page": pagination["page"],
        "page_size": pagination["page_size"],
        "pages": pages,
    }


@router.get("/{media_id}", response_model=MediaSchema)
async def read_media_item(
    media_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Any:
    """
    Get media by ID.

    Args:
        media_id: Media ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Media: Media with specified ID
    """
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )

    # Check if user has access
    if media.visibility == MediaVisibility.PRIVATE and media.uploaded_by_id != current_user.id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this media",
        )

    # Convert to response schema with URLs
    return MediaSchema.model_validate(media)


@router.put("/{media_id}", response_model=MediaSchema)
async def update_media(
    media_id: str,
    media_in: MediaUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Any:
    """
    Update media metadata.

    Args:
        media_id: Media ID
        media_in: Updated media data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Media: Updated media
    """
    # Get existing media
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )

    # Check if user has permission to update
    if media.uploaded_by_id != current_user.id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this media",
        )

    # Track approval changes
    was_approved = media.is_approved

    # Update media attributes
    update_data = media_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(media, field, value)

    # Handle approval status change
    if not was_approved and media.is_approved and current_user.role in ["admin", "manager"]:
        media.approved_by_id = current_user.id
        media.approved_at = datetime.now()

    # Save changes
    await db.commit()
    await db.refresh(media)

    # Convert to response schema with URLs
    return MediaSchema.model_validate(media)


@router.delete("/{media_id}")
async def delete_media(
    media_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> dict:
    """
    Delete media.

    Args:
        media_id: Media ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Success message
    """
    # Get existing media
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )

    # Check if user has permission to delete
    if media.uploaded_by_id != current_user.id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this media",
        )

    # Get file paths to delete after database record is removed
    file_path = get_file_path(media.file_path)
    thumbnail_path = get_thumbnail_path(media.file_path)

    # Delete the media record
    await db.delete(media)
    await db.commit()

    # Delete the files from disk
    try:
        if file_path.exists():
            os.remove(file_path)
        if thumbnail_path and thumbnail_path.exists():
            os.remove(thumbnail_path)
    except Exception as e:
        # Log but don't fail if file deletion fails
        print(f"Error deleting files for media {media_id}: {str(e)}")

    return {"message": "Media deleted successfully"}


@router.get("/file/{media_id}")
async def get_media_file(
    media_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Optional[User] = Depends(get_optional_user),
) -> Any:
    """
    Get the file for media.

    Args:
        media_id: Media ID
        db: Database session
        current_user: Current authenticated user (optional for public files)

    Returns:
        FileResponse: Media file
    """
    # Get existing media
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )

    # Check if user has access
    if media.visibility == MediaVisibility.PRIVATE:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required to access this file",
            )
        if media.uploaded_by_id != current_user.id and current_user.role not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this file",
            )

    # Get file path
    file_path = get_file_path(media.file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on server",
        )

    return FileResponse(
        path=str(file_path),
        filename=media.filename,
        media_type=media.mime_type,
    )


@router.get("/thumbnail/{media_id}")
async def get_media_thumbnail(
    media_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Optional[User] = Depends(get_optional_user),  # Changed to optional user
) -> Any:
    """
    Get the thumbnail for an image.

    Args:
        media_id: Media ID
        db: Database session
        current_user: Current authenticated user (optional for public files)

    Returns:
        FileResponse: Thumbnail file or original file if thumbnail doesn't exist
    """
    # Get existing media
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )

    # Check if media is an image
    if media.media_type != MediaType.IMAGE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Thumbnails are only available for images",
        )

    # Check if user has access
    if media.visibility == MediaVisibility.PRIVATE:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required to access this file",
            )
        if media.uploaded_by_id != current_user.id and current_user.role not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this file",
            )

    # Get thumbnail path
    thumbnail_path = get_thumbnail_path(media.file_path)

    # If thumbnail doesn't exist, return the original file
    if not thumbnail_path or not thumbnail_path.exists():
        file_path = get_file_path(media.file_path)
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found on server",
            )
        return FileResponse(
            path=str(file_path),
            filename=media.filename,
            media_type=media.mime_type,
        )

    return FileResponse(
        path=str(thumbnail_path),
        filename=f"thumb_{media.filename}",
        media_type=media.mime_type,
    )


@router.post("/{media_id}/products/{product_id}")
async def associate_media_with_product(
    media_id: str,
    product_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> dict:
    """
    Associate media with a product.

    Args:
        media_id: Media ID
        product_id: Product ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        dict: Success message
    """
    # Check if media exists
    stmt = select(Media).where(Media.id == media_id)
    result = await db.execute(stmt)
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )

    # Check if product exists
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # Check if association already exists
    stmt = select(product_media_association).where(
        (product_media_association.c.product_id == product_id) &
        (product_media_association.c.media_id == media_id)
    )
    result = await db.execute(stmt)
    if result.first():
        return {"message": "Media already associated with product"}

    # Create association
    stmt = product_media_association.insert().values(
        product_id=product_id,
        media_id=media_id
    )
    await db.execute(stmt)
    await db.commit()

    return {"message": "Media associated with product successfully"}


@router.delete("/{media_id}/products/{product_id}")
async def remove_media_from_product(
    media_id: str,
    product_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> dict:
    """
    Remove association between media and a product.

    Args:
        media_id: Media ID
        product_id: Product ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        dict: Success message
    """
    # Check if association exists
    stmt = select(product_media_association).where(
        (product_media_association.c.product_id == product_id) &
        (product_media_association.c.media_id == media_id)
    )
    result = await db.execute(stmt)
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Association between media and product not found",
        )

    # Remove association
    stmt = product_media_association.delete().where(
        (product_media_association.c.product_id == product_id) &
        (product_media_association.c.media_id == media_id)
    )
    await db.execute(stmt)
    await db.commit()

    return {"message": "Media disassociated from product successfully"}


@router.get("/products/{product_id}", response_model=List[MediaSchema])
async def get_product_media(
    product_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    media_type: Optional[MediaType] = None,
) -> Any:
    """
    Get media associated with a product.

    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user
        media_type: Filter by media type

    Returns:
        List[Media]: List of media associated with the product
    """
    # Check if product exists
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # Base query
    query = (
        select(Media)
        .join(product_media_association)
        .where(product_media_association.c.product_id == product_id)
    )

    # Apply media type filter if provided
    if media_type:
        query = query.where(Media.media_type == media_type)

    # Execute query
    result = await db.execute(query)
    media_items = result.scalars().all()

    # Convert to response schemas with URLs
    return [MediaSchema.model_validate(media) for media in media_items]
