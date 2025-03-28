from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.domains.company.models import Company
from app.domains.company.schemas import CompanyCreate, CompanyUpdate
from app.domains.users.models import User, UserRole, get_password_hash
from app.domains.users.schemas import Company as CompanySchema, User as UserSchema, UserCreate, UserUpdate
router = APIRouter()
@router.get('/', response_model=List[UserSchema])
async def read_users(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)], skip: int=0, limit: int=100, role: Optional[UserRole]=None, company_id: Optional[str]=None, is_active: Optional[bool]=None) -> Any:
    query = select(User).options(joinedload(User.company))
    if role:
        query = query.where(User.role == role)
    if company_id:
        query = query.where(User.company_id == company_id)
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.unique().scalars().all()
    return users
@router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
    if user_in.company_id:
        result = await db.execute(select(Company).where(Company.id == user_in.company_id))
        if not result.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Company not found')
    user_data = user_in.model_dump(exclude={'password'})
    hashed_password = get_password_hash(user_in.password)
    user = User(**user_data, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    if user.company_id:
        await db.refresh(user, ['company'])
    return user
@router.get('/me', response_model=UserSchema)
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)], db: Annotated[AsyncSession, Depends(get_db)]) -> Any:
    if current_user.company_id:
        await db.refresh(current_user, ['company'])
    return current_user
@router.get('/{user_id}', response_model=UserSchema)
async def read_user(user_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    query = select(User).where(User.id == user_id).options(joinedload(User.company))
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
@router.put('/{user_id}', response_model=UserSchema)
async def update_user(user_id: str, user_in: UserUpdate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    query = select(User).where(User.id == user_id).options(joinedload(User.company))
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if user_in.email is not None and user_in.email != user.email:
        result = await db.execute(select(User).where(User.email == user_in.email))
        if result.first() is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
    if user_in.company_id is not None and user_in.company_id:
        result = await db.execute(select(Company).where(Company.id == user_in.company_id))
        if not result.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Company not found')
    update_data = user_in.model_dump(exclude={'password'}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)
    await db.commit()
    await db.refresh(user)
    return user
@router.delete('/{user_id}')
async def delete_user(user_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    if str(current_user.id) == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot delete self')
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    await db.delete(user)
    await db.commit()
    return {'message': 'User deleted successfully'}
@router.get('/companies/', response_model=List[CompanySchema])
async def read_companies(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)], skip: int=0, limit: int=100, is_active: Optional[bool]=None) -> Any:
    query = select(Company)
    if is_active is not None:
        query = query.where(Company.is_active == is_active)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    companies = result.scalars().all()
    return companies
@router.post('/companies/', response_model=CompanySchema, status_code=status.HTTP_201_CREATED)
async def create_company(company_in: CompanyCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    if company_in.account_number:
        result = await db.execute(select(Company).where(Company.account_number == company_in.account_number))
        if result.first() is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Account number already registered')
    company = Company(**company_in.model_dump())
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company
@router.get('/companies/{company_id}', response_model=CompanySchema)
async def read_company(company_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    return company
@router.put('/companies/{company_id}', response_model=CompanySchema)
async def update_company(company_id: str, company_in: CompanyUpdate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    if company_in.account_number is not None and company_in.account_number != company.account_number:
        result = await db.execute(select(Company).where(Company.account_number == company_in.account_number))
        existing = result.scalar_one_or_none()
        if existing and str(existing.id) != company_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Account number already registered')
    update_data = company_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    await db.commit()
    await db.refresh(company)
    return company
@router.delete('/companies/{company_id}')
async def delete_company(company_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    result = await db.execute(select(func.count()).select_from(User).where(User.company_id == company_id))
    user_count = result.scalar_one()
    if user_count > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Cannot delete company with {user_count} associated users')
    await db.delete(company)
    await db.commit()
    return {'message': 'Company deleted successfully'}