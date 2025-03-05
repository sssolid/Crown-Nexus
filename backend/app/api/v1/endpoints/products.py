from __future__ import annotations

from typing import Annotated, Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.models.product import Category, Product
from app.models.user import User
from app.schemas.product import (
    Category as CategorySchema,
    CategoryCreate,
    CategoryUpdate,
    Product as ProductSchema,
    ProductCreate,
    ProductListResponse,
    ProductUpdate,
)

router = APIRouter()


@router.get("/", response_model=ProductListResponse)
async def read_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    category_id: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    page: int = 1,
    page_size: int = 20,
) -> Any:
    """
    Retrieve products.

    Args:
        db: Database session
        current_user: Current authenticated user
        category_id: Filter by category ID
        search: Search term for product name, description, or SKU
        skip: Number of products to skip
        limit: Maximum number of products to return
        page: Page number
        page_size: Number of items per page

    Returns:
        ProductListResponse: Paginated list of products
    """
    # Pagination parameters
    pagination = get_pagination(page, page_size)
    skip = pagination["skip"]
    limit = pagination["limit"]

    # Base query
    query = select(Product).where(Product.is_active == True)

    # Apply filters
    if category_id:
        query = query.where(Product.category_id == category_id)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Product.name.ilike(search_term)) |
            (Product.description.ilike(search_term)) |
            (Product.sku.ilike(search_term))
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Apply pagination and get items
    query = query.offset(skip).limit(limit)
    query = query.options(selectinload(Product.category))
    result = await db.execute(query)
    products = result.scalars().all()

    # Calculate total pages
    pages = (total + limit - 1) // limit if limit > 0 else 0

    return {
        "items": products,
        "total": total,
        "page": pagination["page"],
        "page_size": pagination["page_size"],
        "pages": pages,
    }


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_in: ProductCreate,
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Create new product.

    Args:
        db: Database session
        product_in: Product data
        current_user: Current authenticated admin user

    Returns:
        Product: Created product
    """
    # Check if SKU already exists
    stmt = select(Product).where(Product.sku == product_in.sku)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists",
        )

    # Check if category exists if provided
    if product_in.category_id:
        stmt = select(Category).where(Category.id == product_in.category_id)
        result = await db.execute(stmt)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found",
            )

    # Create new product
    product = Product(**product_in.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)

    # Load related category if exists
    if product.category_id:
        await db.refresh(product, ["category"])

    return product


@router.get("/{product_id}", response_model=ProductSchema)
async def read_product(
    product_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Any:
    """
    Get product by ID.

    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Product: Product with specified ID
    """
    # Query with joined load for category
    stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.category))
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: str,
    product_in: ProductUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Update a product.

    Args:
        product_id: Product ID
        product_in: Updated product data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Product: Updated product
    """
    # Get existing product
    stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.category))
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # Check if SKU is changed and already exists
    if product_in.sku is not None and product_in.sku != product.sku:
        stmt = select(Product).where(Product.sku == product_in.sku)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists",
            )

    # Check if category exists if provided
    if product_in.category_id is not None:
        if product_in.category_id:  # Not None and not empty
            stmt = select(Category).where(Category.id == product_in.category_id)
            result = await db.execute(stmt)
            if not result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category not found",
                )

    # Update product attributes
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    # Save changes
    await db.commit()
    await db.refresh(product)

    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> dict:
    """
    Delete a product.

    Args:
        product_id: Product ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        dict: Success message
    """
    # Get existing product
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    # Delete the product
    await db.delete(product)
    await db.commit()

    return {"message": "Product deleted successfully"}


# Category endpoints
@router.get("/categories/", response_model=List[CategorySchema])
async def read_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve categories.

    Args:
        db: Database session
        current_user: Current authenticated user
        skip: Number of categories to skip
        limit: Maximum number of categories to return

    Returns:
        List[Category]: List of categories
    """
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/categories/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    category_in: CategoryCreate,
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Create new category.

    Args:
        db: Database session
        category_in: Category data
        current_user: Current authenticated admin user

    Returns:
        Category: Created category
    """
    # Check if slug already exists
    stmt = select(Category).where(Category.slug == category_in.slug)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this slug already exists",
        )

    # Check if parent exists if provided
    if category_in.parent_id:
        stmt = select(Category).where(Category.id == category_in.parent_id)
        result = await db.execute(stmt)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found",
            )

    # Create new category
    category = Category(**category_in.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


@router.get("/categories/{category_id}", response_model=CategorySchema)
async def read_category(
    category_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Any:
    """
    Get category by ID.

    Args:
        category_id: Category ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Category: Category with specified ID
    """
    stmt = select(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


@router.put("/categories/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: str,
    category_in: CategoryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Update a category.

    Args:
        category_id: Category ID
        category_in: Updated category data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Category: Updated category
    """
    # Get existing category
    stmt = select(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    # Check if slug is changed and already exists
    if category_in.slug is not None and category_in.slug != category.slug:
        stmt = select(Category).where(Category.slug == category_in.slug)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this slug already exists",
            )

    # Check if parent exists if provided
    if category_in.parent_id is not None and category_in.parent_id:
        stmt = select(Category).where(Category.id == category_in.parent_id)
        result = await db.execute(stmt)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found",
            )

        # Prevent circular references
        if str(category_in.parent_id) == str(category_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category cannot be its own parent",
            )

    # Update category attributes
    update_data = category_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    # Save changes
    await db.commit()
    await db.refresh(category)

    return category


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> dict:
    """
    Delete a category.

    Args:
        category_id: Category ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        dict: Success message
    """
    # Get existing category
    stmt = select(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    # Check if category has products
    stmt = select(func.count()).select_from(Product).where(Product.category_id == category_id)
    result = await db.scalar(stmt)
    if result and result > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {result} associated products",
        )

    # Check if category has children
    stmt = select(func.count()).select_from(Category).where(Category.parent_id == category_id)
    result = await db.scalar(stmt)
    if result and result > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {result} child categories",
        )

    # Delete the category
    await db.delete(category)
    await db.commit()

    return {"message": "Category deleted successfully"}
