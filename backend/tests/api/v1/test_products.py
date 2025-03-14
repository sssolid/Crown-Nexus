# backend/tests/api/v1/test_products.py
"""
Tests for product management endpoints.

This module tests:
- Product listing with filtering
- Product creation, retrieval, update, and deletion
- Permission checks for different user roles
- Error handling for invalid operations
"""

from __future__ import annotations

import uuid
from typing import Dict, Any

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.models.user import User
from tests.utils import make_authenticated_request, create_random_string


@pytest.mark.asyncio
async def test_read_products(
    client: AsyncClient, normal_user: User, user_token: str, test_product: Product
) -> None:
    """
    Test retrieving a list of products.

    Args:
        client: Test client
        normal_user: Regular user
        user_token: User token
        test_product: Test product fixture
    """
    # Get products list as normal user
    response = await make_authenticated_request(
        client,
        "get",
        "/api/v1/products/",
        token=user_token,
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "pages" in data

    # Check that test product is in the response
    product_ids = [product["id"] for product in data["items"]]
    assert str(test_product.id) in product_ids


@pytest.mark.asyncio
async def test_read_products_with_filters(
    client: AsyncClient, admin_token: str, test_product: Product
) -> None:
    """
    Test retrieving products with filters.

    Args:
        client: Test client
        admin_token: Admin token
        test_product: Test product fixture
    """
    # Search by name
    response = await make_authenticated_request(
        client,
        "get",
        f"/api/v1/products/?search={test_product.name}",
        token=admin_token,
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0
    assert data["items"][0]["name"] == test_product.name

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_create_product_admin(
    client: AsyncClient, admin_token: str
) -> None:
    """
    Test creating a product as admin.

    Args:
        client: Test client
        admin_token: Admin token
    """
    # Product data
    product_data = {
        "sku": f"TEST-{create_random_string(5)}",
        "name": f"Test Product {create_random_string(5)}",
        "description": "A test product for unit testing",
        "part_number": f"TP-{create_random_string(5)}",
        "attributes": {"material": "steel", "weight": 1.5},
        "is_active": True,
    }

    # Create product as admin
    response = await make_authenticated_request(
        client,
        "post",
        "/api/v1/products/",
        token=admin_token,
        json=product_data,
    )

    # Check response
    assert response.status_code == 201
    data = response.json()
    assert data["sku"] == product_data["sku"]
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["part_number"] == product_data["part_number"]
    assert data["attributes"] == product_data["attributes"]
    assert data["is_active"] == product_data["is_active"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_product_non_admin(
    client: AsyncClient, user_token: str
) -> None:
    """
    Test that non-admin users cannot create products.

    Args:
        client: Test client
        user_token: User token
    """
    # Product data
    product_data = {
        "sku": f"TEST-{create_random_string(5)}",
        "name": f"Test Product {create_random_string(5)}",
        "description": "A test product for unit testing",
        "part_number": f"TP-{create_random_string(5)}",
        "attributes": {"material": "steel", "weight": 1.5},
        "is_active": True,
    }

    # Attempt to create product as non-admin
    response = await make_authenticated_request(
        client,
        "post",
        "/api/v1/products/",
        token=user_token,
        json=product_data,
    )

    # Check response
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_product_duplicate_sku(
    client: AsyncClient, admin_token: str, test_product: Product
) -> None:
    """
    Test creating a product with a duplicate SKU.

    Args:
        client: Test client
        admin_token: Admin token
        test_product: Test product fixture
    """
    # Product data with duplicate SKU
    product_data = {
        "sku": test_product.sku,  # Duplicate SKU
        "name": f"Test Product {create_random_string(5)}",
        "description": "A test product for unit testing",
        "part_number": f"TP-{create_random_string(5)}",
        "attributes": {"material": "aluminum", "weight": 2.0},
        "is_active": True,
    }

    # Attempt to create product with duplicate SKU
    response = await make_authenticated_request(
        client,
        "post",
        "/api/v1/products/",
        token=admin_token,
        json=product_data,
    )

    # Check response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already exists" in data["detail"]


@pytest.mark.asyncio
async def test_read_product(
    client: AsyncClient, user_token: str, test_product: Product
) -> None:
    """
    Test retrieving a single product.

    Args:
        client: Test client
        user_token: User token
        test_product: Test product fixture
    """
    # Get product by ID
    response = await make_authenticated_request(
        client,
        "get",
        f"/api/v1/products/{test_product.id}",
        token=user_token,
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_product.id)
    assert data["sku"] == test_product.sku
    assert data["name"] == test_product.name


@pytest.mark.asyncio
async def test_read_product_not_found(
    client: AsyncClient, user_token: str
) -> None:
    """
    Test retrieving a non-existent product.

    Args:
        client: Test client
        user_token: User token
    """
    # Generate random UUID that doesn't exist
    random_id = str(uuid.uuid4())

    # Attempt to get non-existent product
    response = await make_authenticated_request(
        client,
        "get",
        f"/api/v1/products/{random_id}",
        token=user_token,
    )

    # Check response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


@pytest.mark.asyncio
async def test_update_product_admin(
    client: AsyncClient, admin_token: str, test_product: Product
) -> None:
    """
    Test updating a product as admin.

    Args:
        client: Test client
        admin_token: Admin token
        test_product: Test product fixture
    """
    # Update data
    update_data = {
        "name": f"Updated Product {create_random_string(5)}",
        "description": "Updated description for testing",
        "attributes": {"material": "aluminum", "color": "red"},
    }

    # Update product as admin
    response = await make_authenticated_request(
        client,
        "put",
        f"/api/v1/products/{test_product.id}",
        token=admin_token,
        json=update_data,
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_product.id)
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["attributes"] == update_data["attributes"]
    assert data["sku"] == test_product.sku  # Unchanged


@pytest.mark.asyncio
async def test_update_product_non_admin(
    client: AsyncClient, user_token: str, test_product: Product
) -> None:
    """
    Test that non-admin users cannot update products.

    Args:
        client: Test client
        user_token: User token
        test_product: Test product fixture
    """
    # Update data
    update_data = {
        "name": f"Updated Product {create_random_string(5)}",
    }

    # Attempt to update product as non-admin
    response = await make_authenticated_request(
        client,
        "put",
        f"/api/v1/products/{test_product.id}",
        token=user_token,
        json=update_data,
    )

    # Check response
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_product_admin(
    client: AsyncClient, admin_token: str, db: AsyncSession
) -> None:
    """
    Test deleting a product as admin.

    Args:
        client: Test client
        admin_token: Admin token
        db: Database session
    """
    # Create a product to delete
    product = Product(
        sku=f"DELETE-{create_random_string(5)}",
        name=f"Product to Delete {create_random_string(5)}",
        description="A product that will be deleted",
        is_active=True,
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)

    # Delete product as admin
    response = await make_authenticated_request(
        client,
        "delete",
        f"/api/v1/products/{product.id}",
        token=admin_token,
    )

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "deleted" in data["message"]

    # Verify product is deleted
    result = await db.execute(select(Product).where(Product.id == product.id))
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_delete_product_non_admin(
    client: AsyncClient, user_token: str, test_product: Product
) -> None:
    """
    Test that non-admin users cannot delete products.

    Args:
        client: Test client
        user_token: User token
        test_product: Test product fixture
    """
    # Attempt to delete product as non-admin
    response = await make_authenticated_request(
        client,
        "delete",
        f"/api/v1/products/{test_product.id}",
        token=user_token,
    )

    # Check response
    assert response.status_code == 403
