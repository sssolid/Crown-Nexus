from __future__ import annotations

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.main import app

# Test database URL
TEST_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI.replace(
    settings.POSTGRES_DB, f"{settings.POSTGRES_DB}_test"
)

# Create async engine for tests
test_engine = create_async_engine(str(TEST_DATABASE_URL), echo=False)
TestingSessionLocal = sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database on each test case.
    
    Yields:
        AsyncSession: Database session
    """
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Run the tests
    async with TestingSessionLocal() as session:
        yield session

    # Drop all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with the database session.
    
    Args:
        db: Database session
        
    Yields:
        AsyncClient: Test client
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an instance of the default event loop for each test case.
    
    Yields:
        asyncio.AbstractEventLoop: Event loop
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
