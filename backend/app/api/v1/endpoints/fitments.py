from __future__ import annotations

from typing import Annotated, Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.domains.products.models import Fitment, Product, product_fitment_association
from app.domains.users.models import User
from app.domains.products.schemas import (
    Fitment as FitmentSchema,
    FitmentCreate,
    FitmentListResponse,
    FitmentUpdate,
    Product as ProductSchema,
)

router = APIRouter()


@router.get("/", response_model=FitmentListResponse)
async def read_fitments(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    year: Optional[int] = None,
    make: Optional[str] = None,
    model: Optional[str] = None,
    engine: Optional[str] = None,
    transmission: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Any:
    """
    Retrieve fitments with filtering options.

    Args:
        db: Database session
        current_user: Current authenticated user
        year: Filter by year
        make: Filter by make
        model: Filter by model
        engine: Filter by engine
        transmission: Filter by transmission
        page: Page number
        page_size: Number of items per page

    Returns:
        FitmentListResponse: Paginated list of fitments
    """
    # Pagination parameters
    pagination = get_pagination(page, page_size)
    skip = pagination["skip"]
    limit = pagination["limit"]

    # Base query
    query = select(Fitment)

    # Apply filters
    if year:
        query = query.where(Fitment.year == year)
    if make:
        query = query.where(Fitment.make.ilike(f"%{make}%"))
    if model:
        query = query.where(Fitment.model.ilike(f"%{model}%"))
    if engine:
        query = query.where(Fitment.engine.ilike(f"%{engine}%"))
    if transmission:
        query = query.where(Fitment.transmission.ilike(f"%{transmission}%"))

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Apply pagination and load products relationship
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    fitments = result.scalars().all()

    # Calculate total pages
    pages = (total + limit - 1) // limit if limit > 0 else 0

    return {
        "items": fitments,
        "total": total,
        "page": pagination["page"],
        "page_size": pagination["page_size"],
        "pages": pages,
    }


@router.post("/", response_model=FitmentSchema, status_code=status.HTTP_201_CREATED)
async def create_fitment(
    db: Annotated[AsyncSession, Depends(get_db)],
    fitment_in: FitmentCreate,
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Create new fitment.

    Args:
        db: Database session
        fitment_in: Fitment data
        current_user: Current authenticated admin user

    Returns:
        Fitment: Created fitment
    """
    # Check if identical fitment already exists
    stmt = select(Fitment).where(
        (Fitment.year == fitment_in.year)
        & (Fitment.make == fitment_in.make)
        & (Fitment.model == fitment_in.model)
    )

    if fitment_in.engine:
        stmt = stmt.where(Fitment.engine == fitment_in.engine)
    if fitment_in.transmission:
        stmt = stmt.where(Fitment.transmission == fitment_in.transmission)

    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Identical fitment already exists",
        )

    # Create new fitment
    fitment = Fitment(**fitment_in.model_dump())
    db.add(fitment)
    await db.commit()
    await db.refresh(fitment)

    return fitment


@router.get("/{fitment_id}", response_model=FitmentSchema)
async def read_fitment(
    fitment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Any:
    """
    Get fitment by ID.

    Args:
        fitment_id: Fitment ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Fitment: Fitment with specified ID
    """
    stmt = select(Fitment).where(Fitment.id == fitment_id)
    result = await db.execute(stmt)
    fitment = result.scalar_one_or_none()

    if not fitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitment not found",
        )

    return fitment


@router.put("/{fitment_id}", response_model=FitmentSchema)
async def update_fitment(
    fitment_id: str,
    fitment_in: FitmentUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Update a fitment.

    Args:
        fitment_id: Fitment ID
        fitment_in: Updated fitment data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Fitment: Updated fitment
    """
    # Get existing fitment
    stmt = select(Fitment).where(Fitment.id == fitment_id)
    result = await db.execute(stmt)
    fitment = result.scalar_one_or_none()

    if not fitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitment not found",
        )

    # Check if update would create a duplicate
    if any(
        field is not None
        for field in [
            fitment_in.year,
            fitment_in.make,
            fitment_in.model,
            fitment_in.engine,
            fitment_in.transmission,
        ]
    ):
        # Build query to check for duplicates
        stmt = select(Fitment).where(
            (Fitment.id != fitment_id)
            & (
                Fitment.year
                == (fitment_in.year if fitment_in.year is not None else fitment.year)
            )
            & (
                Fitment.make
                == (fitment_in.make if fitment_in.make is not None else fitment.make)
            )
            & (
                Fitment.model
                == (fitment_in.model if fitment_in.model is not None else fitment.model)
            )
        )

        engine_value = (
            fitment_in.engine if fitment_in.engine is not None else fitment.engine
        )
        if engine_value:
            stmt = stmt.where(Fitment.engine == engine_value)

        transmission_value = (
            fitment_in.transmission
            if fitment_in.transmission is not None
            else fitment.transmission
        )
        if transmission_value:
            stmt = stmt.where(Fitment.transmission == transmission_value)

        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Identical fitment already exists",
            )

    # Update fitment attributes
    update_data = fitment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fitment, field, value)

    # Save changes
    await db.commit()
    await db.refresh(fitment)

    return fitment


@router.delete("/{fitment_id}")
async def delete_fitment(
    fitment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> dict:
    """
    Delete a fitment.

    Args:
        fitment_id: Fitment ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        dict: Success message
    """
    # Get existing fitment
    stmt = select(Fitment).where(Fitment.id == fitment_id)
    result = await db.execute(stmt)
    fitment = result.scalar_one_or_none()

    if not fitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitment not found",
        )

    # Check if fitment is associated with products
    stmt = (
        select(func.count())
        .select_from(product_fitment_association)
        .where(product_fitment_association.c.fitment_id == fitment_id)
    )
    count = await db.scalar(stmt)

    if count and count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete fitment with {count} associated products",
        )

    # Delete the fitment
    await db.delete(fitment)
    await db.commit()

    return {"message": "Fitment deleted successfully"}


@router.get("/{fitment_id}/products", response_model=List[ProductSchema])
async def read_fitment_products(
    fitment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get products associated with a fitment.

    Args:
        fitment_id: Fitment ID
        db: Database session
        current_user: Current authenticated user
        skip: Number of products to skip
        limit: Maximum number of products to return

    Returns:
        List[Product]: List of products associated with the fitment
    """
    # Check if fitment exists
    stmt = select(Fitment).where(Fitment.id == fitment_id)
    result = await db.execute(stmt)
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitment not found",
        )

    # Get associated products
    stmt = (
        select(Product)
        .join(product_fitment_association)
        .where(product_fitment_association.c.fitment_id == fitment_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    products = result.scalars().all()

    return products


@router.post("/{fitment_id}/products/{product_id}")
async def associate_product_with_fitment(
    fitment_id: str,
    product_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> dict:
    """
    Associate a product with a fitment.

    Args:
        fitment_id: Fitment ID
        product_id: Product ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        dict: Success message
    """
    # Check if fitment exists
    stmt = select(Fitment).where(Fitment.id == fitment_id)
    result = await db.execute(stmt)
    fitment = result.scalar_one_or_none()
    if not fitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitment not found",
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
    stmt = select(product_fitment_association).where(
        (product_fitment_association.c.product_id == product_id)
        & (product_fitment_association.c.fitment_id == fitment_id)
    )
    result = await db.execute(stmt)
    if result.first():
        return {"message": "Product already associated with fitment"}

    # Create association
    stmt = product_fitment_association.insert().values(
        product_id=product_id, fitment_id=fitment_id
    )
    await db.execute(stmt)
    await db.commit()

    return {"message": "Product associated with fitment successfully"}


@router.delete("/{fitment_id}/products/{product_id}")
async def remove_product_from_fitment(
    fitment_id: str,
    product_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> dict:
    """
    Remove association between a product and a fitment.

    Args:
        fitment_id: Fitment ID
        product_id: Product ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        dict: Success message
    """
    # Check if association exists
    stmt = select(product_fitment_association).where(
        (product_fitment_association.c.product_id == product_id)
        & (product_fitment_association.c.fitment_id == fitment_id)
    )
    result = await db.execute(stmt)
    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Association between product and fitment not found",
        )

    # Remove association
    stmt = product_fitment_association.delete().where(
        (product_fitment_association.c.product_id == product_id)
        & (product_fitment_association.c.fitment_id == fitment_id)
    )
    await db.execute(stmt)
    await db.commit()

    return {"message": "Product disassociated from fitment successfully"}
