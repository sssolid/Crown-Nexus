# Module: tests.conftest

**Path:** `tests/conftest.py`

[Back to Project Index](../../index.md)

## Imports
```python
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
```

## Global Variables
```python
TEST_DATABASE_URL = TEST_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI).replace(
    settings.POSTGRES_DB, f"{settings.POSTGRES_DB}_test"
)
test_engine = test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)
TestingSessionLocal = TestingSessionLocal = sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)
```

## Functions

| Function | Description |
| --- | --- |
| `admin_headers` |  |
| `admin_token` |  |
| `admin_user` |  |
| `auth_headers` |  |
| `client` |  |
| `db` |  |
| `event_loop` |  |
| `normal_user` |  |
| `setup_db` |  |
| `test_brand` |  |
| `test_company` |  |
| `test_fitment` |  |
| `test_product` |  |
| `user_token` |  |

### `admin_headers`
```python
@pytest_asyncio.fixture(scope='function')
async def admin_headers(admin_token) -> Dict[(str, str)]:
```

### `admin_token`
```python
@pytest_asyncio.fixture(scope='function')
async def admin_token(admin_user) -> str:
```

### `admin_user`
```python
@pytest_asyncio.fixture(scope='function')
async def admin_user(db) -> User:
```

### `auth_headers`
```python
@pytest_asyncio.fixture(scope='function')
async def auth_headers(user_token) -> Dict[(str, str)]:
```

### `client`
```python
@pytest_asyncio.fixture(scope='function')
async def client(db) -> AsyncGenerator[(AsyncClient, None)]:
```

### `db`
```python
@pytest_asyncio.fixture(scope='function')
async def db(setup_db) -> AsyncGenerator[(AsyncSession, None)]:
```

### `event_loop`
```python
@pytest.fixture(scope='session')
def event_loop() -> Generator[(asyncio.AbstractEventLoop, None, None)]:
```

### `normal_user`
```python
@pytest_asyncio.fixture(scope='function')
async def normal_user(db) -> User:
```

### `setup_db`
```python
@pytest_asyncio.fixture(scope='session')
async def setup_db() -> AsyncGenerator[(None, None)]:
```

### `test_brand`
```python
@pytest_asyncio.fixture(scope='function')
async def test_brand(db) -> Brand:
```

### `test_company`
```python
@pytest_asyncio.fixture(scope='function')
async def test_company(db) -> Company:
```

### `test_fitment`
```python
@pytest_asyncio.fixture(scope='function')
async def test_fitment(db) -> Fitment:
```

### `test_product`
```python
@pytest_asyncio.fixture(scope='function')
async def test_product(db, test_brand) -> Product:
```

### `user_token`
```python
@pytest_asyncio.fixture(scope='function')
async def user_token(normal_user) -> str:
```
