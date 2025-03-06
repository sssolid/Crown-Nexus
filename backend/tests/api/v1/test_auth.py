# backend/tests/api/v1/test_auth.py
"""
Tests for authentication endpoints.

This module tests:
- User login with valid credentials
- Handling of invalid credentials
- Token validation
- User profile retrieval
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.models.user import User
from tests.utils import make_authenticated_request


async def test_login_success(client: AsyncClient, normal_user: User) -> None:
    """
    Test successful login with valid credentials.

    Args:
        client: Test client
        normal_user: Test user fixture
    """
    # Login with valid credentials
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": normal_user.email,
            "password": "user_password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_invalid_credentials(client: AsyncClient, normal_user: User) -> None:
    """
    Test login with invalid credentials.

    Args:
        client: Test client
        normal_user: Test user fixture
    """
    # Login with invalid password
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": normal_user.email,
            "password": "wrong_password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    # Check response
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "Incorrect email or password" in data["detail"]


async def test_get_current_user(
    client: AsyncClient, normal_user: User, user_token: str
) -> None:
    """
    Test retrieving the current user profile.

    Args:
        client: Test client
        normal_user: Test user fixture
        user_token: User authentication token
    """
    # Get user profile
    response = await make_authenticated_request(
        client,
        "get",
        "/api/v1/auth/me",
        token=user_token,
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == normal_user.email
    assert data["full_name"] == normal_user.full_name
    assert data["role"] == normal_user.role.value
    assert "id" in data


async def test_get_current_user_unauthorized(client: AsyncClient) -> None:
    """
    Test retrieving user profile without authentication.

    Args:
        client: Test client
    """
    # Attempt to get user profile without token
    response = await client.get("/api/v1/auth/me")

    # Check response
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "Not authenticated" in data["detail"]
