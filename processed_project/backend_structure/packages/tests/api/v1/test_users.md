# Module: tests.api.v1.test_users

**Path:** `tests/api/v1/test_users.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from httpx import AsyncClient
from app.domains.users.models import User, UserRole
from tests.utils import create_random_email, make_authenticated_request
```

## Functions

| Function | Description |
| --- | --- |
| `test_create_user_admin` |  |
| `test_delete_user_admin` |  |
| `test_read_user_by_id_admin` |  |
| `test_read_users_admin` |  |
| `test_read_users_non_admin` |  |
| `test_update_user_admin` |  |

### `test_create_user_admin`
```python
async def test_create_user_admin(client, admin_token) -> None:
```

### `test_delete_user_admin`
```python
async def test_delete_user_admin(client, admin_token, normal_user) -> None:
```

### `test_read_user_by_id_admin`
```python
async def test_read_user_by_id_admin(client, admin_token, normal_user) -> None:
```

### `test_read_users_admin`
```python
async def test_read_users_admin(client, admin_user, admin_token, normal_user) -> None:
```

### `test_read_users_non_admin`
```python
async def test_read_users_non_admin(client, normal_user, user_token) -> None:
```

### `test_update_user_admin`
```python
async def test_update_user_admin(client, admin_token, normal_user) -> None:
```
