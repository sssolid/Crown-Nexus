# backend/tests/conftest.py
"""
Test configuration and fixtures for pytest.

This module provides test fixtures for:
- Database session setup and teardown
- Test client configuration
- Authentication helpers
- Mock data factories

These fixtures ensure that tests run in a controlled environment
with consistent data and proper isolation between test cases.
"""

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
from app.models.product import Category, Fitment, Product

# Test database URL
TEST_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI).replace(
    settings.POSTGRES_DB, f"{settings.POSTGRES_DB}_test"
)

# Create async engine for tests
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an instance of the default event loop for each test case.

    This fixture is required for pytest-asyncio to work properly.

    Yields:
        asyncio.AbstractEventLoop: Event loop for async tests
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def setup_db() -> AsyncGenerator[None, None]:
    """
    Set up test database tables.

    This fixture creates all tables for testing and drops them after
    all tests are complete. It runs only once per test session.

    Yields:
        None
    """
    # Create all tables
    async with test_engine.begin() as conn:
        # Drop tables if they exist
        await conn.run_sync(Base.metadata.drop_all)
        # Create new tables
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Clean up after all tests
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db(setup_db) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database session for a test.

    This fixture provides an isolated database session for each test
    with proper transaction management and cleanup.

    Args:
        setup_db: Ensures database tables are created

    Yields:
        AsyncSession: Database session
    """
    # Create a new session for each test
    async with TestingSessionLocal() as session:
        # Start a nested transaction
        async with session.begin():
            # Use the session for the test
            yield session
            # Rollback the transaction to clean up
            await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with the database session.

    This fixture overrides the database dependency to use the test database
    session and provides an async HTTP client for testing API endpoints.

    Args:
        db: Database session fixture

    Yields:
        AsyncClient: Test client for async API requests
    """
    # Override the get_db dependency
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db

    # Create async client for testing
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    # Clean up
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def admin_user(db: AsyncSession) -> User:
    """
    Create a test admin user.

    This fixture provides an admin user for testing endpoints
    that require admin privileges.

    Args:
        db: Database session fixture

    Returns:
        User: Admin user model instance
    """
    # Create admin user
    hashed_password = get_password_hash("admin_password")
    admin = User(
        email="admin@example.com",
        hashed_password=hashed_password,
        full_name="Test Admin",
        role=UserRole.ADMIN,
        is_active=True,
    )

    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    return admin


@pytest_asyncio.fixture(scope="function")
async def normal_user(db: AsyncSession) -> User:
    """
    Create a test normal user.

    This fixture provides a regular user for testing endpoints
    that require authentication but not admin privileges.

    Args:
        db: Database session fixture

    Returns:
        User: Normal user model instance
    """
    # Create normal user
    hashed_password = get_password_hash("user_password")
    user = User(
        email="user@example.com",
        hashed_password=hashed_password,
        full_name="Test User",
        role=UserRole.CLIENT,
        is_active=True,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def admin_token(admin_user: User) -> str:
    """
    Create an authentication token for admin user.

    This fixture generates a valid JWT token for the admin user
    to use in authenticated API requests.

    Args:
        admin_user: Admin user fixture

    Returns:
        str: JWT token for admin user
    """
    from app.models.user import create_access_token

    return create_access_token(
        subject=str(admin_user.id),
        role=admin_user.role,
    )


@pytest_asyncio.fixture(scope="function")
async def user_token(normal_user: User) -> str:
    """
    Create an authentication token for normal user.

    This fixture generates a valid JWT token for the normal user
    to use in authenticated API requests.

    Args:
        normal_user: Normal user fixture

    Returns:
        str: JWT token for normal user
    """
    from app.models.user import create_access_token

    return create_access_token(
        subject=str(normal_user.id),
        role=normal_user.role,
    )


@pytest_asyncio.fixture(scope="function")
async def test_category(db: AsyncSession) -> Category:
    """
    Create a test product category.

    This fixture provides a product category for testing
    product-related functionality.

    Args:
        db: Database session fixture

    Returns:
        Category: Category model instance
    """
    # Create test category
    category = Category(
        name="Test Category",
        slug="test-category",
        description="A test category for unit testing",
    )

    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@pytest_asyncio.fixture(scope="function")
async def test_product(db: AsyncSession, test_category: Category) -> Product:
    """
    Create a test product.

    This fixture provides a product for testing product-related
    functionality.

    Args:
        db: Database session fixture
        test_category: Category fixture

    Returns:
        Product: Product model instance
    """
    # Create test product
    product = Product(
        sku="TEST-001",
        name="Test Product",
        description="A test product for unit testing",
        part_number="TP001",
        category_id=test_category.id,
        attributes={"material": "steel", "weight": 1.5},
        is_active=True,
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@pytest_asyncio.fixture(scope="function")
async def test_fitment(db: AsyncSession) -> Fitment:
    """
    Create a test fitment.

    This fixture provides a fitment for testing fitment-related
    functionality.

    Args:
        db: Database session fixture

    Returns:
        Fitment: Fitment model instance
    """
    # Create test fitment
    fitment = Fitment(
        year=2022,
        make="Toyota",
        model="Camry",
        engine="2.5L I4",
        transmission="Automatic",
        attributes={"trim": "SE", "body_style": "Sedan"},
    )

    db.add(fitment)
    await db.commit()
    await db.refresh(fitment)
    return fitment
