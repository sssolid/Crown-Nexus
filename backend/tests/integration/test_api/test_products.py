# /backend/tests/integration/test_api/test_products.py
from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.products.models import Product
from app.domains.users.models import User
from tests.utils import make_authenticated_request, create_random_string


@pytest.mark.asyncio
async def test_create_product_admin(client: AsyncClient, admin_token: str) -> None:
    """Test creating a product as admin."""
    product_data = {
        "part_number": f"TP-{create_random_string(6)}",
        "application": "Test application",
        "vintage": False,
        "late_model": True,
        "soft": False,
        "universal": False,
        "is_active": True,
    }

    response = await make_authenticated_request(
        client,
        "post",
        "/api/v1/products/",
        admin_token,
        json=product_data,
    )

    # Verify successful response
    assert response.status_code == 201
    data = response.json()
    assert data["part_number"] == product_data["part_number"]
    assert "id" in data


@pytest.mark.asyncio
async def test_create_product_non_admin(client: AsyncClient, user_token: str) -> None:
    """Test that non-admin users cannot create products."""
    product_data = {
        "part_number": f"TP-{create_random_string(6)}",
        "application": "Test application",
        "vintage": False,
        "late_model": True,
        "soft": False,
        "universal": False,
        "is_active": True,
    }

    response = await make_authenticated_request(
        client,
        "post",
        "/api/v1/products/",
        user_token,
        json=product_data,
    )

    # Verify permission denied response
    assert response.status_code == 403
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_read_products(
    client: AsyncClient, normal_user: User, user_token: str, test_product: Product
) -> None:
    """Test retrieving a list of products."""
    response = await make_authenticated_request(
        client,
        "get",
        "/api/v1/products/",
        user_token,
    )

    # Verify successful response
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0
    assert "total" in data


@pytest.mark.asyncio
async def test_read_product(
    client: AsyncClient, user_token: str, test_product: Product
) -> None:
    """Test retrieving a single product."""
    response = await make_authenticated_request(
        client,
        "get",
        f"/api/v1/products/{test_product.id}",
        user_token,
    )

    # Verify successful response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_product.id)
    assert data["part_number"] == test_product.part_number


@pytest.mark.asyncio
async def test_read_product_not_found(client: AsyncClient, user_token: str) -> None:
    """Test retrieving a non-existent product."""
    non_existent_id = uuid.uuid4()
    response = await make_authenticated_request(
        client,
        "get",
        f"/api/v1/products/{non_existent_id}",
        user_token,
    )

    # Verify not found response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_update_product_admin(
    client: AsyncClient, admin_token: str, test_product: Product
) -> None:
    """Test updating a product as admin."""
    update_data = {
        "part_number": f"TP-Updated-{create_random_string(6)}",
        "application": "Updated application",
        "is_active": False,
    }

    response = await make_authenticated_request(
        client,
        "put",
        f"/api/v1/products/{test_product.id}",
        admin_token,
        json=update_data,
    )

    # Verify successful response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_product.id)
    assert data["part_number"] == update_data["part_number"]
    assert data["application"] == update_data["application"]
    assert data["is_active"] == update_data["is_active"]


@pytest.mark.asyncio
async def test_delete_product_admin(
    client: AsyncClient, admin_token: str, db: AsyncSession
) -> None:
    """Test deleting a product as admin."""
    # Create a product to delete
    new_product = Product(
        id=uuid.uuid4(),
        part_number=f"TP-Delete-{create_random_string(6)}",
        part_number_stripped=f"TPDELETE{create_random_string(6)}",
        application="Test application for deletion",
        vintage=False,
        late_model=True,
        soft=False,
        universal=False,
        is_active=True,
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    response = await make_authenticated_request(
        client,
        "delete",
        f"/api/v1/products/{new_product.id}",
        admin_token,
    )

    # Verify successful response
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

    # Verify product was deleted
    result = await db.execute(select(Product).where(Product.id == new_product.id))
    db_product = result.scalars().first()
    assert db_product is None
