from __future__ import annotations
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.api.deps import get_admin_user, get_current_active_user, get_db, get_pagination
from app.models.product import Brand, Fitment, Product, ProductActivity, ProductBrandHistory, ProductDescription, ProductMarketing, ProductMeasurement, ProductStock, ProductSupersession
from app.models.reference import Warehouse
from app.models.user import User
from app.schemas.product import Brand as BrandSchema, BrandCreate, BrandUpdate, Fitment as FitmentSchema, FitmentCreate, FitmentUpdate, Product as ProductSchema, ProductCreate, ProductDescription as ProductDescriptionSchema, ProductDescriptionCreate, ProductDescriptionUpdate, ProductListResponse, ProductMarketing as ProductMarketingSchema, ProductMarketingCreate, ProductMarketingUpdate, ProductMeasurement as ProductMeasurementSchema, ProductMeasurementCreate, ProductMeasurementUpdate, ProductStatus, ProductStock as ProductStockSchema, ProductStockCreate, ProductStockUpdate, ProductSupersession as ProductSupersessionSchema, ProductSupersessionCreate, ProductUpdate
router = APIRouter()
@router.get('/', response_model=ProductListResponse)
async def read_products(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], search: Optional[str]=None, vintage: Optional[bool]=None, late_model: Optional[bool]=None, soft: Optional[bool]=None, universal: Optional[bool]=None, is_active: Optional[bool]=None, skip: int=0, limit: int=100, page: int=1, page_size: int=20) -> Any:
    pagination = get_pagination(page, page_size)
    skip = pagination['skip']
    limit = pagination['limit']
    query = select(Product)
    if search:
        search_term = f'%{search}%'
        query = query.where(Product.part_number.ilike(search_term) | Product.part_number_stripped.ilike(search_term) | Product.application.ilike(search_term))
    if vintage is not None:
        query = query.where(Product.vintage == vintage)
    if late_model is not None:
        query = query.where(Product.late_model == late_model)
    if soft is not None:
        query = query.where(Product.soft == soft)
    if universal is not None:
        query = query.where(Product.universal == universal)
    if is_active is not None:
        query = query.where(Product.is_active == is_active)
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0
    query = query.offset(skip).limit(limit)
    query = query.options(selectinload(Product.descriptions), selectinload(Product.marketing), selectinload(Product.activities).selectinload(ProductActivity.changed_by), selectinload(Product.superseded_by).selectinload(ProductSupersession.new_product), selectinload(Product.supersedes).selectinload(ProductSupersession.old_product), selectinload(Product.measurements), selectinload(Product.stock))
    result = await db.execute(query)
    products = result.scalars().all()
    pages = (total + limit - 1) // limit if limit > 0 else 0
    return {'items': products, 'total': total, 'page': pagination['page'], 'page_size': pagination['page_size'], 'pages': pages}
@router.post('/', response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[AsyncSession, Depends(get_db)], product_in: ProductCreate, current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(Product).where(Product.part_number == product_in.part_number)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Product with this part number already exists')
    product_data = product_in.model_dump(exclude={'descriptions', 'marketing'}, exclude_unset=True)
    product = Product(**product_data)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    if product_in.descriptions:
        for desc_data in product_in.descriptions:
            description = ProductDescription(product_id=product.id, **desc_data.model_dump())
            db.add(description)
        await db.commit()
    if product_in.marketing:
        for marketing_data in product_in.marketing:
            marketing = ProductMarketing(product_id=product.id, **marketing_data.model_dump())
            db.add(marketing)
        await db.commit()
    activity = ProductActivity(product_id=product.id, status=ProductStatus.ACTIVE, reason='Product created', changed_by_id=current_user.id)
    db.add(activity)
    await db.commit()
    await db.refresh(product, ['descriptions', 'marketing', 'activities', 'superseded_by', 'supersedes', 'measurements', 'stock'])
    return product
@router.get('/{product_id}', response_model=ProductSchema)
async def read_product(product_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)]) -> Any:
    stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.descriptions), selectinload(Product.marketing), selectinload(Product.activities).selectinload(ProductActivity.changed_by), selectinload(Product.superseded_by).selectinload(ProductSupersession.new_product), selectinload(Product.supersedes).selectinload(ProductSupersession.old_product), selectinload(Product.measurements), selectinload(Product.stock))
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    return product
@router.put('/{product_id}', response_model=ProductSchema)
async def update_product(product_id: str, product_in: ProductUpdate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.descriptions), selectinload(Product.marketing), selectinload(Product.activities), selectinload(Product.superseded_by), selectinload(Product.supersedes), selectinload(Product.measurements), selectinload(Product.stock))
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    if product_in.part_number is not None and product_in.part_number != product.part_number:
        stmt = select(Product).where(Product.part_number == product_in.part_number)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Product with this part number already exists')
    was_active = product.is_active
    will_be_active = product_in.is_active if product_in.is_active is not None else was_active
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    if 'part_number' in update_data:
        product.part_number_stripped = ''.join((c for c in product.part_number if c.isalnum())).upper()
    await db.commit()
    await db.refresh(product)
    if was_active != will_be_active:
        activity = ProductActivity(product_id=product.id, status=ProductStatus.ACTIVE if will_be_active else ProductStatus.INACTIVE, reason=f"Product {('activated' if will_be_active else 'deactivated')}", changed_by_id=current_user.id)
        db.add(activity)
        await db.commit()
    await db.refresh(product, ['activities', 'descriptions', 'marketing', 'superseded_by', 'supersedes', 'measurements', 'stock'])
    return product
@router.delete('/{product_id}')
async def delete_product(product_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    await db.delete(product)
    await db.commit()
    return {'message': 'Product deleted successfully'}
@router.post('/{product_id}/descriptions', response_model=ProductDescriptionSchema)
async def create_product_description(product_id: str, description_in: ProductDescriptionCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    description = ProductDescription(product_id=product_id, **description_in.model_dump())
    db.add(description)
    await db.commit()
    await db.refresh(description)
    return description
@router.put('/{product_id}/descriptions/{description_id}', response_model=ProductDescriptionSchema)
async def update_product_description(product_id: str, description_id: str, description_in: ProductDescriptionUpdate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(ProductDescription).where((ProductDescription.id == description_id) & (ProductDescription.product_id == product_id))
    result = await db.execute(stmt)
    description = result.scalar_one_or_none()
    if not description:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Description not found for this product')
    update_data = description_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(description, field, value)
    await db.commit()
    await db.refresh(description)
    return description
@router.delete('/{product_id}/descriptions/{description_id}')
async def delete_product_description(product_id: str, description_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    stmt = select(ProductDescription).where((ProductDescription.id == description_id) & (ProductDescription.product_id == product_id))
    result = await db.execute(stmt)
    description = result.scalar_one_or_none()
    if not description:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Description not found for this product')
    await db.delete(description)
    await db.commit()
    return {'message': 'Description deleted successfully'}
@router.post('/{product_id}/marketing', response_model=ProductMarketingSchema)
async def create_product_marketing(product_id: str, marketing_in: ProductMarketingCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    marketing = ProductMarketing(product_id=product_id, **marketing_in.model_dump())
    db.add(marketing)
    await db.commit()
    await db.refresh(marketing)
    return marketing
@router.put('/{product_id}/marketing/{marketing_id}', response_model=ProductMarketingSchema)
async def update_product_marketing(product_id: str, marketing_id: str, marketing_in: ProductMarketingUpdate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(ProductMarketing).where((ProductMarketing.id == marketing_id) & (ProductMarketing.product_id == product_id))
    result = await db.execute(stmt)
    marketing = result.scalar_one_or_none()
    if not marketing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Marketing content not found for this product')
    update_data = marketing_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(marketing, field, value)
    await db.commit()
    await db.refresh(marketing)
    return marketing
@router.delete('/{product_id}/marketing/{marketing_id}')
async def delete_product_marketing(product_id: str, marketing_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    stmt = select(ProductMarketing).where((ProductMarketing.id == marketing_id) & (ProductMarketing.product_id == product_id))
    result = await db.execute(stmt)
    marketing = result.scalar_one_or_none()
    if not marketing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Marketing content not found for this product')
    await db.delete(marketing)
    await db.commit()
    return {'message': 'Marketing content deleted successfully'}
@router.post('/{product_id}/measurements', response_model=ProductMeasurementSchema)
async def create_product_measurement(product_id: str, measurement_in: ProductMeasurementCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    measurement = ProductMeasurement(product_id=product_id, **measurement_in.model_dump())
    db.add(measurement)
    await db.commit()
    await db.refresh(measurement)
    return measurement
@router.post('/{product_id}/stock', response_model=ProductStockSchema)
async def create_product_stock(product_id: str, stock_in: ProductStockCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    stmt = select(Warehouse).where(Warehouse.id == stock_in.warehouse_id)
    result = await db.execute(stmt)
    warehouse = result.scalar_one_or_none()
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Warehouse not found')
    stmt = select(ProductStock).where((ProductStock.product_id == product_id) & (ProductStock.warehouse_id == stock_in.warehouse_id))
    result = await db.execute(stmt)
    existing_stock = result.scalar_one_or_none()
    if existing_stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Stock already exists for this product in this warehouse')
    stock = ProductStock(product_id=product_id, **stock_in.model_dump())
    db.add(stock)
    await db.commit()
    await db.refresh(stock)
    return stock
@router.put('/{product_id}/stock/{stock_id}', response_model=ProductStockSchema)
async def update_product_stock(product_id: str, stock_id: str, stock_in: ProductStockUpdate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(ProductStock).where((ProductStock.id == stock_id) & (ProductStock.product_id == product_id))
    result = await db.execute(stmt)
    stock = result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Stock information not found for this product')
    update_data = stock_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stock, field, value)
    stock.last_updated = func.now()
    await db.commit()
    await db.refresh(stock)
    return stock
@router.delete('/{product_id}/stock/{stock_id}')
async def delete_product_stock(product_id: str, stock_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    stmt = select(ProductStock).where((ProductStock.id == stock_id) & (ProductStock.product_id == product_id))
    result = await db.execute(stmt)
    stock = result.scalar_one_or_none()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Stock information not found for this product')
    await db.delete(stock)
    await db.commit()
    return {'message': 'Stock information deleted successfully'}
@router.post('/{product_id}/supersessions', response_model=ProductSupersessionSchema)
async def create_product_supersession(product_id: str, supersession_in: ProductSupersessionCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    if str(supersession_in.old_product_id) != product_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='old_product_id must match the product_id in the path')
    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    old_product = result.scalar_one_or_none()
    if not old_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Old product not found')
    stmt = select(Product).where(Product.id == supersession_in.new_product_id)
    result = await db.execute(stmt)
    new_product = result.scalar_one_or_none()
    if not new_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='New product not found')
    stmt = select(ProductSupersession).where((ProductSupersession.old_product_id == product_id) & (ProductSupersession.new_product_id == supersession_in.new_product_id))
    result = await db.execute(stmt)
    existing_supersession = result.scalar_one_or_none()
    if existing_supersession:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Supersession already exists for these products')
    supersession = ProductSupersession(**supersession_in.model_dump())
    db.add(supersession)
    await db.commit()
    await db.refresh(supersession)
    return supersession
@router.delete('/{product_id}/supersessions/{supersession_id}')
async def delete_product_supersession(product_id: str, supersession_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    stmt = select(ProductSupersession).where((ProductSupersession.id == supersession_id) & (ProductSupersession.old_product_id == product_id))
    result = await db.execute(stmt)
    supersession = result.scalar_one_or_none()
    if not supersession:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supersession not found for this product')
    await db.delete(supersession)
    await db.commit()
    return {'message': 'Supersession deleted successfully'}
@router.get('/brands/', response_model=List[BrandSchema])
async def read_brands(db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)], skip: int=0, limit: int=100) -> Any:
    stmt = select(Brand).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
@router.post('/brands/', response_model=BrandSchema, status_code=status.HTTP_201_CREATED)
async def create_brand(db: Annotated[AsyncSession, Depends(get_db)], brand_in: BrandCreate, current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    if brand_in.parent_company_id:
        from app.models.user import Company
        stmt = select(Company).where(Company.id == brand_in.parent_company_id)
        result = await db.execute(stmt)
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Parent company not found')
    brand = Brand(**brand_in.model_dump())
    db.add(brand)
    await db.commit()
    await db.refresh(brand)
    return brand
@router.get('/brands/{brand_id}', response_model=BrandSchema)
async def read_brand(brand_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)]) -> Any:
    stmt = select(Brand).where(Brand.id == brand_id)
    result = await db.execute(stmt)
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Brand not found')
    return brand
@router.put('/brands/{brand_id}', response_model=BrandSchema)
async def update_brand(brand_id: str, brand_in: BrandUpdate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> Any:
    stmt = select(Brand).where(Brand.id == brand_id)
    result = await db.execute(stmt)
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Brand not found')
    if brand_in.parent_company_id is not None and brand_in.parent_company_id:
        from app.models.user import Company
        stmt = select(Company).where(Company.id == brand_in.parent_company_id)
        result = await db.execute(stmt)
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Parent company not found')
    update_data = brand_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(brand, field, value)
    await db.commit()
    await db.refresh(brand)
    return brand
@router.delete('/brands/{brand_id}')
async def delete_brand(brand_id: str, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_admin_user)]) -> dict:
    stmt = select(Brand).where(Brand.id == brand_id)
    result = await db.execute(stmt)
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Brand not found')
    stmt = select(func.count()).select_from(ProductBrandHistory).where((ProductBrandHistory.old_brand_id == brand_id) | (ProductBrandHistory.new_brand_id == brand_id))
    result = await db.scalar(stmt)
    if result and result > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Cannot delete brand with {result} associated product brand records')
    await db.delete(brand)
    await db.commit()
    return {'message': 'Brand deleted successfully'}