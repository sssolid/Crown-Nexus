# Module: tests.api.v1.test_auth

**Path:** `tests/api/v1/test_auth.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from httpx import AsyncClient
from app.domains.users.models import User
from tests.utils import make_authenticated_request
```

## Functions

| Function | Description |
| --- | --- |
| `test_get_current_user` |  |
| `test_get_current_user_unauthorized` |  |
| `test_login_invalid_credentials` |  |
| `test_login_success` |  |

### `test_get_current_user`
```python
async def test_get_current_user(client, normal_user, user_token) -> None:
```

### `test_get_current_user_unauthorized`
```python
async def test_get_current_user_unauthorized(client) -> None:
```

### `test_login_invalid_credentials`
```python
async def test_login_invalid_credentials(client, normal_user) -> None:
```

### `test_login_success`
```python
async def test_login_success(client, normal_user) -> None:
```
