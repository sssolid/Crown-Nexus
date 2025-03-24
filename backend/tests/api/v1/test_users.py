# backend/tests/api/v1/test_users.py
"""
Tests for user management endpoints.

This module tests:
- User listing with filtering
- User creation, retrieval, update, and deletion
- Permission checks for different user roles
- Error handling for invalid operations
"""

from __future__ import annotations

from httpx import AsyncClient

from app.domains.users.models import User, UserRole
from tests.utils import (
    create_random_email,
    make_authenticated_request,
)


async def test_read_users_admin(
    client: AsyncClient, admin_user: User, admin_token: str, normal_user: User
) -> None:
    """
    Test that admin users can list all users.

    Args:
        client: Test client
        admin_user: Admin user fixture
        admin_token: Admin authentication token
        normal_user: Regular user fixture
    """
    # Get users list as admin
    response = await make_authenticated_request(
        client,
        "get",
        "/api/v1/users/",
        token=admin_token,
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # At least admin_user and normal_user

    # Check that both users are in the response
    user_ids = [user["id"] for user in data]
    assert str(admin_user.id) in user_ids
    assert str(normal_user.id) in user_ids


async def test_read_users_non_admin(
    client: AsyncClient, normal_user: User, user_token: str
) -> None:
    """
    Test that non-admin users cannot list all users.

    Args:
        client: Test client
        normal_user: Regular user fixture
        user_token: User authentication token
    """
    # Attempt to get users list as non-admin
    response = await make_authenticated_request(
        client,
        "get",
        "/api/v1/users/",
        token=user_token,
    )

    # Check response
    assert response.status_code == 403
    data = response.json()
    assert "detail" in data
    assert "Insufficient permissions" in data["detail"]


async def test_create_user_admin(client: AsyncClient, admin_token: str) -> None:
    """
    Test user creation by admin.

    Args:
        client: Test client
        admin_token: Admin authentication token
    """
    # User data
    user_data = {
        "email": create_random_email(),
        "password": "testpassword123",
        "full_name": "Test User",
        "role": UserRole.CLIENT.value,
        "is_active": True,
    }

    # Create user as admin
    response = await make_authenticated_request(
        client,
        "post",
        "/api/v1/users/",
        token=admin_token,
        json=user_data,
    )

    # Check response
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["role"] == user_data["role"]
    assert "id" in data
    assert "password" not in data  # Password should not be in response


async def test_read_user_by_id_admin(
    client: AsyncClient, admin_token: str, normal_user: User
) -> None:
    """
    Test retrieving a user by ID as admin.

    Args:
        client: Test client
        admin_token: Admin authentication token
        normal_user: User to retrieve
    """
    # Get user by ID as admin
    response = await make_authenticated_request(
        client,
        "get",
        f"/api/v1/users/{normal_user.id}",
        token=admin_token,
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == normal_user.email
    assert data["full_name"] == normal_user.full_name
    assert data["role"] == normal_user.role.value
    assert data["id"] == str(normal_user.id)


async def test_update_user_admin(
    client: AsyncClient, admin_token: str, normal_user: User
) -> None:
    """
    Test updating a user as admin.

    Args:
        client: Test client
        admin_token: Admin authentication token
        normal_user: User to update
    """
    # Updated data
    update_data = {
        "full_name": "Updated Name",
        "role": UserRole.MANAGER.value,
    }

    # Update user as admin
    response = await make_authenticated_request(
        client,
        "put",
        f"/api/v1/users/{normal_user.id}",
        token=admin_token,
        json=update_data,
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["role"] == update_data["role"]
    assert data["id"] == str(normal_user.id)
    assert data["email"] == normal_user.email  # Email should not change


async def test_delete_user_admin(
    client: AsyncClient, admin_token: str, normal_user: User
) -> None:
    """
    Test deleting a user as admin.

    Args:
        client: Test client
        admin_token: Admin authentication token
        normal_user: User to delete
    """
    # Create a user to delete
    new_user_data = {
        "email": create_random_email(),
        "password": "testpassword123",
        "full_name": "Test Delete User",
        "role": UserRole.CLIENT.value,
        "is_active": True,
    }

    # Create user
    create_response = await make_authenticated_request(
        client,
        "post",
        "/api/v1/users/",
        token=admin_token,
        json=new_user_data,
    )
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Delete user as admin
    delete_response = await make_authenticated_request(
        client,
        "delete",
        f"/api/v1/users/{user_id}",
        token=admin_token,
    )

    # Check response
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert "message" in data
    assert "deleted" in data["message"]

    # Verify user is deleted
    get_response = await make_authenticated_request(
        client,
        "get",
        f"/api/v1/users/{user_id}",
        token=admin_token,
    )
    assert get_response.status_code == 404
