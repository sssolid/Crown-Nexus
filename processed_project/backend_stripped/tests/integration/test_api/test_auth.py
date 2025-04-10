from __future__ import annotations
import pytest
from httpx import AsyncClient
from app.domains.users.models import User
from tests.utils import make_authenticated_request
@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, normal_user: User) -> None:
    response = await client.post('/api/v1/auth/login', data={'username': normal_user.email, 'password': 'password'})
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, normal_user: User) -> None:
    response = await client.post('/api/v1/auth/login', data={'username': normal_user.email, 'password': 'wrong_password'})
    assert response.status_code == 401
    data = response.json()
    assert 'detail' in data
@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, normal_user: User, user_token: str) -> None:
    response = await make_authenticated_request(client, 'get', '/api/v1/auth/me', user_token)
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == normal_user.email
    assert data['full_name'] == normal_user.full_name
    assert data['role'] == normal_user.role.value
@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client: AsyncClient) -> None:
    response = await client.get('/api/v1/auth/me')
    assert response.status_code == 401
    data = response.json()
    assert 'detail' in data