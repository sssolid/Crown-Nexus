from __future__ import annotations
import pytest
from httpx import AsyncClient
from app.models.user import User, UserRole
from tests.utils import create_random_email, create_random_string, make_authenticated_request
async def test_read_users_admin(client: AsyncClient, admin_user: User, admin_token: str, normal_user: User) -> None:
    response = await make_authenticated_request(client, 'get', '/api/v1/users/', token=admin_token)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    user_ids = [user['id'] for user in data]
    assert str(admin_user.id) in user_ids
    assert str(normal_user.id) in user_ids
async def test_read_users_non_admin(client: AsyncClient, normal_user: User, user_token: str) -> None:
    response = await make_authenticated_request(client, 'get', '/api/v1/users/', token=user_token)
    assert response.status_code == 403
    data = response.json()
    assert 'detail' in data
    assert 'Insufficient permissions' in data['detail']
async def test_create_user_admin(client: AsyncClient, admin_token: str) -> None:
    user_data = {'email': create_random_email(), 'password': 'testpassword123', 'full_name': 'Test User', 'role': UserRole.CLIENT.value, 'is_active': True}
    response = await make_authenticated_request(client, 'post', '/api/v1/users/', token=admin_token, json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == user_data['email']
    assert data['full_name'] == user_data['full_name']
    assert data['role'] == user_data['role']
    assert 'id' in data
    assert 'password' not in data
async def test_read_user_by_id_admin(client: AsyncClient, admin_token: str, normal_user: User) -> None:
    response = await make_authenticated_request(client, 'get', f'/api/v1/users/{normal_user.id}', token=admin_token)
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == normal_user.email
    assert data['full_name'] == normal_user.full_name
    assert data['role'] == normal_user.role.value
    assert data['id'] == str(normal_user.id)
async def test_update_user_admin(client: AsyncClient, admin_token: str, normal_user: User) -> None:
    update_data = {'full_name': 'Updated Name', 'role': UserRole.MANAGER.value}
    response = await make_authenticated_request(client, 'put', f'/api/v1/users/{normal_user.id}', token=admin_token, json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['full_name'] == update_data['full_name']
    assert data['role'] == update_data['role']
    assert data['id'] == str(normal_user.id)
    assert data['email'] == normal_user.email
async def test_delete_user_admin(client: AsyncClient, admin_token: str, normal_user: User) -> None:
    new_user_data = {'email': create_random_email(), 'password': 'testpassword123', 'full_name': 'Test Delete User', 'role': UserRole.CLIENT.value, 'is_active': True}
    create_response = await make_authenticated_request(client, 'post', '/api/v1/users/', token=admin_token, json=new_user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()['id']
    delete_response = await make_authenticated_request(client, 'delete', f'/api/v1/users/{user_id}', token=admin_token)
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert 'message' in data
    assert 'deleted' in data['message']
    get_response = await make_authenticated_request(client, 'get', f'/api/v1/users/{user_id}', token=admin_token)
    assert get_response.status_code == 404