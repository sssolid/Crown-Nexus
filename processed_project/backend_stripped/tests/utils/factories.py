from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Company, User, UserRole, get_password_hash
from app.models.product import Brand, Fitment, Product, ProductDescription, ProductStatus
from app.models.media import Media, MediaType, MediaVisibility
from tests.utils import create_random_email, create_random_string
class BaseFactory:
    @classmethod
    async def create_batch(cls, db_session: AsyncSession, count: int=3, **kwargs: Any) -> List[Any]:
        return [await cls.create(db_session, **kwargs) for _ in range(count)]
class UserFactory(BaseFactory):
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> User:
        defaults = {'id': uuid.uuid4(), 'email': create_random_email(), 'full_name': f'{create_random_string(6)} {create_random_string(8)}', 'hashed_password': get_password_hash('password'), 'role': UserRole.CLIENT, 'is_active': True}
        defaults.update(kwargs)
        user = User(**defaults)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user
class CompanyFactory(BaseFactory):
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Company:
        defaults = {'id': uuid.uuid4(), 'name': f'Company {create_random_string(8)}', 'account_number': f'ACC{create_random_string(6, digits_only=True)}', 'account_type': 'client', 'is_active': True}
        defaults.update(kwargs)
        company = Company(**defaults)
        db_session.add(company)
        await db_session.commit()
        await db_session.refresh(company)
        return company
class BrandFactory(BaseFactory):
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Brand:
        defaults = {'id': uuid.uuid4(), 'name': f'Brand {create_random_string(8)}'}
        defaults.update(kwargs)
        brand = Brand(**defaults)
        db_session.add(brand)
        await db_session.commit()
        await db_session.refresh(brand)
        return brand
class ProductFactory(BaseFactory):
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Product:
        part_number = f'P{create_random_string(5, digits_only=True)}'
        defaults = {'id': uuid.uuid4(), 'part_number': part_number, 'part_number_stripped': part_number, 'application': f'Application for {part_number}', 'vintage': False, 'late_model': True, 'soft': False, 'universal': False, 'is_active': True}
        defaults.update(kwargs)
        product = Product(**defaults)
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
        return product
class FitmentFactory(BaseFactory):
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Fitment:
        current_year = datetime.now().year
        defaults = {'id': uuid.uuid4(), 'year': random.randint(current_year - 10, current_year), 'make': f'Make {create_random_string(6)}', 'model': f'Model {create_random_string(6)}', 'engine': random.choice(['V6', 'V8', 'I4', 'I6', 'H4']), 'transmission': random.choice(['Manual', 'Automatic', 'CVT', 'DCT'])}
        defaults.update(kwargs)
        fitment = Fitment(**defaults)
        db_session.add(fitment)
        await db_session.commit()
        await db_session.refresh(fitment)
        return fitment
class MediaFactory(BaseFactory):
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Media:
        defaults = {'id': uuid.uuid4(), 'filename': f'file-{create_random_string(8)}.jpg', 'file_path': f'/media/test/file-{create_random_string(8)}.jpg', 'file_size': random.randint(10000, 1000000), 'media_type': MediaType.IMAGE, 'mime_type': 'image/jpeg', 'visibility': MediaVisibility.PUBLIC, 'uploaded_by_id': None, 'is_approved': True}
        defaults.update(kwargs)
        media = Media(**defaults)
        db_session.add(media)
        await db_session.commit()
        await db_session.refresh(media)
        return media