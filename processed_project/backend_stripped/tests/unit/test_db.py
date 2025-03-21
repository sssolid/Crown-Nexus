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
    user_data = {'id': uuid.uuid4(), 'email': 'test_create@example.com', 'full_name': 'Test Create User', 'hashed_password': 'hashed_password', 'role': UserRole.CLIENT, 'is_active': True}
    user = await create_object(db, User, user_data)
    assert user.email == user_data['email']
    assert user.full_name == user_data['full_name']
    assert user.role == UserRole.CLIENT
    result = await db.execute(select(User).where(User.id == user.id))
    db_user = result.scalars().first()
    assert db_user is not None
    assert db_user.email == user_data['email']
@pytest.mark.asyncio
async def test_get_by_id(db, normal_user) -> None:
    user = await get_by_id(db, User, normal_user.id)
    assert user is not None
    assert user.id == normal_user.id
    assert user.email == normal_user.email
    non_existent = await get_by_id(db, User, uuid.uuid4())
    assert non_existent is None
@pytest.mark.asyncio
async def test_update_object(db, normal_user) -> None:
    update_data = {'full_name': 'Updated Name', 'is_active': False}
    updated_user = await update_object(db, User, normal_user.id, update_data)
    assert updated_user is not None
    assert updated_user.id == normal_user.id
    assert updated_user.full_name == 'Updated Name'
    assert updated_user.is_active is False
    result = await db.execute(select(User).where(User.id == normal_user.id))
    db_user = result.scalars().first()
    assert db_user.full_name == 'Updated Name'
    assert db_user.is_active is False
@pytest.mark.asyncio
async def test_delete_object(db, normal_user) -> None:
    result = await delete_object(db, User, normal_user.id)
    assert result is True
    db_result = await db.execute(select(User).where(User.id == normal_user.id))
    db_user = db_result.scalars().first()
    assert db_user is None
    non_existent_result = await delete_object(db, User, uuid.uuid4())
    assert non_existent_result is False