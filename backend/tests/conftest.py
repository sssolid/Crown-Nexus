# /backend/tests/conftest.py
from __future__ import annotations

import asyncio
import uuid
from typing import (
    AsyncGenerator,
    Dict,
    Generator,
)

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

# Constants
TEST_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI).replace(
    settings.POSTGRES_DB, f"{settings.POSTGRES_DB}_test"
)

# Create test engine with echo=False to reduce log noise during tests
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

# Session factory for tests
TestingSessionLocal = sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case.

    This fixture is required for pytest-asyncio to work properly.

    Yields:
        asyncio.AbstractEventLoop: Event loop for async tests
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def setup_db() -> AsyncGenerator[None, None]:
    """Set up test database tables.

    This fixture creates all tables for testing and drops them after all tests are complete.
    It runs only once per test session.

    Yields:
        None
    """
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop all tables after tests
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db(setup_db) -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for a test.

    This fixture provides an isolated database session for each test with proper
    transaction management and cleanup.

    Args:
        setup_db: Ensures database tables are created

    Yields:
        AsyncSession: Database session
    """
    async with TestingSessionLocal() as session:
        # Start a nested transaction
        async with session.begin():
            # Use session for the test
            yield session
            # Rollback the transaction after test
            await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with the database session.

    This fixture overrides the database dependency to use the test database session
    and provides an async HTTP client for testing API endpoints.

    Args:
        db: Database session fixture

    Yields:
        AsyncClient: Test client for async API requests
    """

    # Override the get_db dependency
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    # Create async client for testing
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    # Clear dependency overrides
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def normal_user(db) -> User:
    """Create a test normal user.

    This fixture provides a regular user for testing endpoints that require
    authentication but not admin privileges.

    Args:
        db: Database session fixture

    Returns:
        User: Normal user model instance
    """
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        full_name="Test User",
        role=UserRole.CLIENT,
        hashed_password=get_password_hash("password"),
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def admin_user(db) -> User:
    """Create a test admin user.

    This fixture provides an admin user for testing endpoints that require
    admin privileges.

    Args:
        db: Database session fixture

    Returns:
        User: Admin user model instance
    """
    user = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        full_name="Admin User",
        role=UserRole.ADMIN,
        hashed_password=get_password_hash("password"),
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def user_token(normal_user) -> str:
    """Create an authentication token for normal user.

    This fixture generates a valid JWT token for the normal user to use
    in authenticated API requests.

    Args:
        normal_user: Normal user fixture

    Returns:
        str: JWT token for normal user
    """
    return create_token(
        str(normal_user.id),
        "access",
        expires_delta=None,
        role=normal_user.role.value,
        user_data={"email": normal_user.email},
    )


@pytest_asyncio.fixture(scope="function")
async def admin_token(admin_user) -> str:
    """Create an authentication token for admin user.

    This fixture generates a valid JWT token for the admin user to use
    in authenticated API requests.

    Args:
        admin_user: Admin user fixture

    Returns:
        str: JWT token for admin user
    """
    return create_token(
        str(admin_user.id),
        "access",
        expires_delta=None,
        role=admin_user.role.value,
        user_data={"email": admin_user.email},
    )


@pytest_asyncio.fixture(scope="function")
async def auth_headers(user_token: str) -> Dict[str, str]:
    """Create headers with authentication token.

    This fixture creates headers with the JWT token for authenticated requests.

    Args:
        user_token: User JWT token

    Returns:
        Dict[str, str]: Headers with authentication token
    """
    return {"Authorization": f"Bearer {user_token}"}


@pytest_asyncio.fixture(scope="function")
async def admin_headers(admin_token: str) -> Dict[str, str]:
    """Create headers with admin authentication token.

    This fixture creates headers with the admin JWT token for authenticated requests.

    Args:
        admin_token: Admin JWT token

    Returns:
        Dict[str, str]: Headers with admin authentication token
    """
    return {"Authorization": f"Bearer {admin_token}"}


@pytest_asyncio.fixture(scope="function")
async def test_company(db) -> Company:
    """Create a test company.

    This fixture provides a company for testing company-related functionality.

    Args:
        db: Database session fixture

    Returns:
        Company: Company model instance
    """
    company = Company(
        id=uuid.uuid4(),
        name="Test Company",
        account_number="TEST123",
        account_type="client",
        is_active=True,
    )
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company


@pytest_asyncio.fixture(scope="function")
async def test_brand(db) -> Brand:
    """Create a test brand.

    This fixture provides a brand for testing brand-related functionality.

    Args:
        db: Database session fixture

    Returns:
        Brand: Brand model instance
    """
    brand = Brand(
        id=uuid.uuid4(),
        name="Test Brand",
    )
    db.add(brand)
    await db.commit()
    await db.refresh(brand)
    return brand


@pytest_asyncio.fixture(scope="function")
async def test_product(db, test_brand) -> Product:
    """Create a test product.

    This fixture provides a product for testing product-related functionality.

    Args:
        db: Database session fixture
        test_brand: Brand fixture

    Returns:
        Product: Product model instance
    """
    product = Product(
        id=uuid.uuid4(),
        part_number="TP123",
        part_number_stripped="TP123",
        application="Test application",
        vintage=False,
        late_model=True,
        soft=False,
        universal=False,
        is_active=True,
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@pytest_asyncio.fixture(scope="function")
async def test_fitment(db) -> Fitment:
    """Create a test fitment.

    This fixture provides a fitment for testing fitment-related functionality.

    Args:
        db: Database session fixture

    Returns:
        Fitment: Fitment model instance
    """
    fitment = Fitment(
        id=uuid.uuid4(),
        year=2020,
        make="Test Make",
        model="Test Model",
        engine="V6",
        transmission="Automatic",
    )
    db.add(fitment)
    await db.commit()
    await db.refresh(fitment)
    return fitment
