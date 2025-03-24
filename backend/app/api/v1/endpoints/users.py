# backend/app/api/v1/endpoints/users.py
"""
User management API endpoints.

This module provides endpoints for user management operations:
- User listing with filtering
- User creation, retrieval, update, and deletion
- Company management
- User profile management

These endpoints implement proper authorization checks to ensure
users can only access and modify appropriate resources.
"""

from __future__ import annotations

from typing import Annotated, Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.domains.users.models import User, UserRole, get_password_hash
from app.domains.users.schemas import (
    Company as CompanySchema,
    User as UserSchema,
    UserCreate,
    UserUpdate,
)
from app.domains.company.schemas import CompanyCreate, CompanyUpdate

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def read_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
    skip: int = 0,
    limit: int = 100,
    role: Optional[UserRole] = None,
    company_id: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> Any:
    """
    Retrieve users with filtering options.

    Args:
        db: Database session
        current_user: Current authenticated admin user
        skip: Number of users to skip
        limit: Maximum number of users to return
        role: Filter by user role
        company_id: Filter by company ID
        is_active: Filter by active status

    Returns:
        List[User]: List of users
    """
    # Build the query with filters
    query = select(User).options(joinedload(User.company))

    if role:
        query = query.where(User.role == role)

    if company_id:
        query = query.where(User.company_id == company_id)

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute the query
    result = await db.execute(query)
    users = result.unique().scalars().all()

    return users


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Create new user.

    Args:
        user_in: User data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        User: Created user

    Raises:
        HTTPException: If email already exists or company not found
    """
    # Check if user with this email already exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check if company exists if provided
    if user_in.company_id:
        result = await db.execute(
            select(Company).where(Company.id == user_in.company_id)
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company not found",
            )

    # Create user object
    user_data = user_in.model_dump(exclude={"password"})
    hashed_password = get_password_hash(user_in.password)
    user = User(**user_data, hashed_password=hashed_password)

    # Save to database
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Load company relationship if exists
    if user.company_id:
        await db.refresh(user, ["company"])

    return user


@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Any:
    """
    Get current user.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        User: Current user with company information
    """
    # Load company if exists
    if current_user.company_id:
        await db.refresh(current_user, ["company"])

    return current_user


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Get user by ID.

    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        User: User with specified ID

    Raises:
        HTTPException: If user not found
    """
    query = select(User).where(User.id == user_id).options(joinedload(User.company))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: str,
    user_in: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Update a user.

    Args:
        user_id: User ID
        user_in: Updated user data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        User: Updated user

    Raises:
        HTTPException: If user not found or company not found
    """
    # Get existing user
    query = select(User).where(User.id == user_id).options(joinedload(User.company))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if email is taken by another user
    if user_in.email is not None and user_in.email != user.email:
        result = await db.execute(select(User).where(User.email == user_in.email))
        if result.first() is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Check if company exists if provided
    if user_in.company_id is not None and user_in.company_id:
        result = await db.execute(
            select(Company).where(Company.id == user_in.company_id)
        )
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company not found",
            )

    # Update user attributes
    update_data = user_in.model_dump(exclude={"password"}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    # Handle password update separately
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)

    # Save changes
    await db.commit()
    await db.refresh(user)

    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> dict:
    """
    Delete a user.

    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        dict: Success message

    Raises:
        HTTPException: If user not found or is the current user
    """
    # Prevent deleting self
    if str(current_user.id) == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete self",
        )

    # Get existing user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Delete the user
    await db.delete(user)
    await db.commit()

    return {"message": "User deleted successfully"}


# Company endpoints
@router.get("/companies/", response_model=List[CompanySchema])
async def read_companies(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
) -> Any:
    """
    Retrieve companies with filtering options.

    Args:
        db: Database session
        current_user: Current authenticated admin user
        skip: Number of companies to skip
        limit: Maximum number of companies to return
        is_active: Filter by active status

    Returns:
        List[Company]: List of companies
    """
    # Build the query with filters
    query = select(Company)

    if is_active is not None:
        query = query.where(Company.is_active == is_active)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute the query
    result = await db.execute(query)
    companies = result.scalars().all()

    return companies


@router.post(
    "/companies/", response_model=CompanySchema, status_code=status.HTTP_201_CREATED
)
async def create_company(
    company_in: CompanyCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Create new company.

    Args:
        company_in: Company data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Company: Created company

    Raises:
        HTTPException: If account number already exists
    """
    # Check if account number already exists
    if company_in.account_number:
        result = await db.execute(
            select(Company).where(Company.account_number == company_in.account_number)
        )
        if result.first() is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account number already registered",
            )

    # Create company object
    company = Company(**company_in.model_dump())

    # Save to database
    db.add(company)
    await db.commit()
    await db.refresh(company)

    return company


@router.get("/companies/{company_id}", response_model=CompanySchema)
async def read_company(
    company_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Get company by ID.

    Args:
        company_id: Company ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Company: Company with specified ID

    Raises:
        HTTPException: If company not found
    """
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    return company


@router.put("/companies/{company_id}", response_model=CompanySchema)
async def update_company(
    company_id: str,
    company_in: CompanyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> Any:
    """
    Update a company.

    Args:
        company_id: Company ID
        company_in: Updated company data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Company: Updated company

    Raises:
        HTTPException: If company not found or account number already exists
    """
    # Get existing company
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    # Check if account number is taken by another company
    if (
        company_in.account_number is not None
        and company_in.account_number != company.account_number
    ):
        result = await db.execute(
            select(Company).where(Company.account_number == company_in.account_number)
        )
        existing = result.scalar_one_or_none()
        if existing and str(existing.id) != company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account number already registered",
            )

    # Update company attributes
    update_data = company_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)

    # Save changes
    await db.commit()
    await db.refresh(company)

    return company


@router.delete("/companies/{company_id}")
async def delete_company(
    company_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> dict:
    """
    Delete a company.

    Args:
        company_id: Company ID
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        dict: Success message

    Raises:
        HTTPException: If company not found or has associated users
    """
    # Get existing company
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    # Check if company has users
    result = await db.execute(
        select(func.count()).select_from(User).where(User.company_id == company_id)
    )
    user_count = result.scalar_one()

    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete company with {user_count} associated users",
        )

    # Delete the company
    await db.delete(company)
    await db.commit()

    return {"message": "Company deleted successfully"}
