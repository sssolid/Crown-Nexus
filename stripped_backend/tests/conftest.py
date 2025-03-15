from __future__ import annotations
import asyncio
from typing import Any, AsyncGenerator, Callable, Dict, Generator, List
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.models.user import User, UserRole, get_password_hash
from app.api.deps import get_db
from app.models.product import Fitment, Product
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
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
    app.dependency_overrides.clear()
@pytest_asyncio.fixture(scope='function')
async def admin_user(db: AsyncSession) -> User:
    hashed_password = get_password_hash('admin_password')
    admin = User(email='admin@example.com', hashed_password=hashed_password, full_name='Test Admin', role=UserRole.ADMIN, is_active=True)
    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    return admin
@pytest_asyncio.fixture(scope='function')
async def normal_user(db: AsyncSession) -> User:
    hashed_password = get_password_hash('user_password')
    user = User(email='user@example.com', hashed_password=hashed_password, full_name='Test User', role=UserRole.CLIENT, is_active=True)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
@pytest_asyncio.fixture(scope='function')
async def admin_token(admin_user: User) -> str:
    from app.models.user import create_access_token
    return create_access_token(subject=str(admin_user.id), role=admin_user.role)
@pytest_asyncio.fixture(scope='function')
async def user_token(normal_user: User) -> str:
    from app.models.user import create_access_token
    return create_access_token(subject=str(normal_user.id), role=normal_user.role)
@pytest_asyncio.fixture(scope='function')
async def test_product(db: AsyncSession) -> Product:
    product = Product(sku='TEST-001', name='Test Product', description='A test product for unit testing', part_number='TP001', attributes={'material': 'steel', 'weight': 1.5}, is_active=True)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product
@pytest_asyncio.fixture(scope='function')
async def test_fitment(db: AsyncSession) -> Fitment:
    fitment = Fitment(year=2022, make='Toyota', model='Camry', engine='2.5L I4', transmission='Automatic', attributes={'trim': 'SE', 'body_style': 'Sedan'})
    db.add(fitment)
    await db.commit()
    await db.refresh(fitment)
    return fitment