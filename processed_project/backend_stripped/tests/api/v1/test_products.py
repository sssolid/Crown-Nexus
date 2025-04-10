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
async def test_read_products(client: AsyncClient, normal_user: User, user_token: str, test_product: Product) -> None:
    response = await make_authenticated_request(client, 'get', '/api/v1/products/', token=user_token)
    assert response.status_code == 200
    data = response.json()
    assert 'items' in data
    assert 'total' in data
    assert 'page' in data
    assert 'page_size' in data
    assert 'pages' in data
    product_ids = [product['id'] for product in data['items']]
    assert str(test_product.id) in product_ids
@pytest.mark.asyncio
async def test_read_products_with_filters(client: AsyncClient, admin_token: str, test_product: Product) -> None:
    response = await make_authenticated_request(client, 'get', f'/api/v1/products/?search={test_product.name}', token=admin_token)
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) > 0
    assert data['items'][0]['name'] == test_product.name
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) > 0
@pytest.mark.asyncio
async def test_create_product_admin(client: AsyncClient, admin_token: str) -> None:
    product_data = {'sku': f'TEST-{create_random_string(5)}', 'name': f'Test Product {create_random_string(5)}', 'description': 'A test product for unit testing', 'part_number': f'TP-{create_random_string(5)}', 'attributes': {'material': 'steel', 'weight': 1.5}, 'is_active': True}
    response = await make_authenticated_request(client, 'post', '/api/v1/products/', token=admin_token, json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data['sku'] == product_data['sku']
    assert data['name'] == product_data['name']
    assert data['description'] == product_data['description']
    assert data['part_number'] == product_data['part_number']
    assert data['attributes'] == product_data['attributes']
    assert data['is_active'] == product_data['is_active']
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data
@pytest.mark.asyncio
async def test_create_product_non_admin(client: AsyncClient, user_token: str) -> None:
    product_data = {'sku': f'TEST-{create_random_string(5)}', 'name': f'Test Product {create_random_string(5)}', 'description': 'A test product for unit testing', 'part_number': f'TP-{create_random_string(5)}', 'attributes': {'material': 'steel', 'weight': 1.5}, 'is_active': True}
    response = await make_authenticated_request(client, 'post', '/api/v1/products/', token=user_token, json=product_data)
    assert response.status_code == 403
@pytest.mark.asyncio
async def test_create_product_duplicate_sku(client: AsyncClient, admin_token: str, test_product: Product) -> None:
    product_data = {'sku': test_product.sku, 'name': f'Test Product {create_random_string(5)}', 'description': 'A test product for unit testing', 'part_number': f'TP-{create_random_string(5)}', 'attributes': {'material': 'aluminum', 'weight': 2.0}, 'is_active': True}
    response = await make_authenticated_request(client, 'post', '/api/v1/products/', token=admin_token, json=product_data)
    assert response.status_code == 400
    data = response.json()
    assert 'detail' in data
    assert 'already exists' in data['detail']
@pytest.mark.asyncio
async def test_read_product(client: AsyncClient, user_token: str, test_product: Product) -> None:
    response = await make_authenticated_request(client, 'get', f'/api/v1/products/{test_product.id}', token=user_token)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(test_product.id)
    assert data['sku'] == test_product.sku
    assert data['name'] == test_product.name
@pytest.mark.asyncio
async def test_read_product_not_found(client: AsyncClient, user_token: str) -> None:
    random_id = str(uuid.uuid4())
    response = await make_authenticated_request(client, 'get', f'/api/v1/products/{random_id}', token=user_token)
    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert 'not found' in data['detail']
@pytest.mark.asyncio
async def test_update_product_admin(client: AsyncClient, admin_token: str, test_product: Product) -> None:
    update_data = {'name': f'Updated Product {create_random_string(5)}', 'description': 'Updated description for testing', 'attributes': {'material': 'aluminum', 'color': 'red'}}
    response = await make_authenticated_request(client, 'put', f'/api/v1/products/{test_product.id}', token=admin_token, json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(test_product.id)
    assert data['name'] == update_data['name']
    assert data['description'] == update_data['description']
    assert data['attributes'] == update_data['attributes']
    assert data['sku'] == test_product.sku
@pytest.mark.asyncio
async def test_update_product_non_admin(client: AsyncClient, user_token: str, test_product: Product) -> None:
    update_data = {'name': f'Updated Product {create_random_string(5)}'}
    response = await make_authenticated_request(client, 'put', f'/api/v1/products/{test_product.id}', token=user_token, json=update_data)
    assert response.status_code == 403
@pytest.mark.asyncio
async def test_delete_product_admin(client: AsyncClient, admin_token: str, db: AsyncSession) -> None:
    product = Product(sku=f'DELETE-{create_random_string(5)}', name=f'Product to Delete {create_random_string(5)}', description='A product that will be deleted', is_active=True)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    response = await make_authenticated_request(client, 'delete', f'/api/v1/products/{product.id}', token=admin_token)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'deleted' in data['message']
    result = await db.execute(select(Product).where(Product.id == product.id))
    assert result.scalar_one_or_none() is None
@pytest.mark.asyncio
async def test_delete_product_non_admin(client: AsyncClient, user_token: str, test_product: Product) -> None:
    response = await make_authenticated_request(client, 'delete', f'/api/v1/products/{test_product.id}', token=user_token)
    assert response.status_code == 403