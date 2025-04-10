from __future__ import annotations
import asyncio
import uuid
from typing import AsyncGenerator, Dict, Generator
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_token
from app.db.base_class import Base
from app.domains.products.models import Brand, Fitment, Product
from app.domains.users.models import Company, User, UserRole, get_password_hash
from app.main import app
TEST_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI).replace(settings.POSTGRES_DB, f'{settings.POSTGRES_DB}_test')
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession, autoflush=False)
@pytest.fixture(scope='session')
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
@pytest_asyncio.fixture(scope='session')
async def setup_db() -> AsyncGenerator[None, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
@pytest_asyncio.fixture(scope='function')
async def db(setup_db) -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        async with session.begin():
            yield session
            await session.rollback()
@pytest_asyncio.fixture(scope='function')
async def client(db) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
    app.dependency_overrides.clear()
@pytest_asyncio.fixture(scope='function')
async def normal_user(db) -> User:
    user = User(id=uuid.uuid4(), email='test@example.com', full_name='Test User', role=UserRole.CLIENT, hashed_password=get_password_hash('password'), is_active=True)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
@pytest_asyncio.fixture(scope='function')
async def admin_user(db) -> User:
    user = User(id=uuid.uuid4(), email='admin@example.com', full_name='Admin User', role=UserRole.ADMIN, hashed_password=get_password_hash('password'), is_active=True)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
@pytest_asyncio.fixture(scope='function')
async def user_token(normal_user) -> str:
    return create_token(str(normal_user.id), 'access', expires_delta=None, role=normal_user.role.value, user_data={'email': normal_user.email})
@pytest_asyncio.fixture(scope='function')
async def admin_token(admin_user) -> str:
    return create_token(str(admin_user.id), 'access', expires_delta=None, role=admin_user.role.value, user_data={'email': admin_user.email})
@pytest_asyncio.fixture(scope='function')
async def auth_headers(user_token: str) -> Dict[str, str]:
    return {'Authorization': f'Bearer {user_token}'}
@pytest_asyncio.fixture(scope='function')
async def admin_headers(admin_token: str) -> Dict[str, str]:
    return {'Authorization': f'Bearer {admin_token}'}
@pytest_asyncio.fixture(scope='function')
async def test_company(db) -> Company:
    company = Company(id=uuid.uuid4(), name='Test Company', account_number='TEST123', account_type='client', is_active=True)
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company
@pytest_asyncio.fixture(scope='function')
async def test_brand(db) -> Brand:
    brand = Brand(id=uuid.uuid4(), name='Test Brand')
    db.add(brand)
    await db.commit()
    await db.refresh(brand)
    return brand
@pytest_asyncio.fixture(scope='function')
async def test_product(db, test_brand) -> Product:
    product = Product(id=uuid.uuid4(), part_number='TP123', part_number_stripped='TP123', application='Test application', vintage=False, late_model=True, soft=False, universal=False, is_active=True)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product
@pytest_asyncio.fixture(scope='function')
async def test_fitment(db) -> Fitment:
    fitment = Fitment(id=uuid.uuid4(), year=2020, make='Test Make', model='Test Model', engine='V6', transmission='Automatic')
    db.add(fitment)
    await db.commit()
    await db.refresh(fitment)
    return fitment