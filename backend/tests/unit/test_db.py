# /backend/tests/unit/test_db.py
from __future__ import annotations

import uuid
from typing import Any, List

import pytest
import pytest_asyncio
from sqlalchemy import select

from app.db.utils import create_object, get_by_id, update_object, delete_object
from app.models.user import User, UserRole


@pytest.mark.asyncio
async def test_create_object(db) -> None:
    """Test creating an object with the utility function."""
    user_data = {
        "id": uuid.uuid4(),
        "email": "test_create@example.com",
        "full_name": "Test Create User",
        "hashed_password": "hashed_password",
        "role": UserRole.CLIENT,
        "is_active": True,
    }

    # Create user
    user = await create_object(db, User, user_data)

    # Verify user was created
    assert user.email == user_data["email"]
    assert user.full_name == user_data["full_name"]
    assert user.role == UserRole.CLIENT

    # Verify user exists in database
    result = await db.execute(select(User).where(User.id == user.id))
    db_user = result.scalars().first()
    assert db_user is not None
    assert db_user.email == user_data["email"]


@pytest.mark.asyncio
async def test_get_by_id(db, normal_user) -> None:
    """Test getting an object by ID."""
    # Get user by ID
    user = await get_by_id(db, User, normal_user.id)

    # Verify correct user was retrieved
    assert user is not None
    assert user.id == normal_user.id
    assert user.email == normal_user.email

    # Try getting with non-existent ID
    non_existent = await get_by_id(db, User, uuid.uuid4())
    assert non_existent is None


@pytest.mark.asyncio
async def test_update_object(db, normal_user) -> None:
    """Test updating an object."""
    # Update user
    update_data = {
        "full_name": "Updated Name",
        "is_active": False,
    }

    updated_user = await update_object(db, User, normal_user.id, update_data)

    # Verify user was updated
    assert updated_user is not None
    assert updated_user.id == normal_user.id
    assert updated_user.full_name == "Updated Name"
    assert updated_user.is_active is False

    # Verify changes were saved to database
    result = await db.execute(select(User).where(User.id == normal_user.id))
    db_user = result.scalars().first()
    assert db_user.full_name == "Updated Name"
    assert db_user.is_active is False


@pytest.mark.asyncio
async def test_delete_object(db, normal_user) -> None:
    """Test deleting an object."""
    # Delete user
    result = await delete_object(db, User, normal_user.id)

    # Verify deletion was successful
    assert result is True

    # Verify user no longer exists in database
    db_result = await db.execute(select(User).where(User.id == normal_user.id))
    db_user = db_result.scalars().first()
    assert db_user is None

    # Try deleting non-existent user
    non_existent_result = await delete_object(db, User, uuid.uuid4())
    assert non_existent_result is False
