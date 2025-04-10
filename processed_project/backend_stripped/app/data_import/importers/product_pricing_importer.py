from __future__ import annotations
'Product pricing importer.\n\nThis module provides an importer that can convert part numbers and pricing type names\nto their corresponding UUIDs before importing pricing data into the database.\n'
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.exceptions import DatabaseException, ResourceNotFoundException
from app.domains.products.schemas import ProductPricingImport
from app.domains.products.models import Product, PriceType, ProductPricing
from app.logging import get_logger
from app.data_import.importers.base import Importer
logger = get_logger('app.data_import.importers.product_pricing_importer')
class ProductPricingImporter(Importer[ProductPricingImport]):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        logger.debug('ProductPricingImporter initialized')
    async def _get_product_id_by_part_number(self, part_number: str) -> Optional[UUID]:
        query = select(Product.id).where(Product.part_number == part_number, Product.is_deleted == False)
        result = await self.db.execute(query)
        product_id = result.scalar_one_or_none()
        return product_id
    async def _get_price_type_id_by_name(self, name: str) -> Optional[UUID]:
        query = select(PriceType.id).where(PriceType.name == name, PriceType.is_deleted == False)
        result = await self.db.execute(query)
        price_type_id = result.scalar_one_or_none()
        return price_type_id
    async def _get_or_create_price_type(self, name: str) -> UUID:
        price_type_id = await self._get_price_type_id_by_name(name)
        if price_type_id:
            return price_type_id
        price_type = PriceType(name=name, description=f'{name} price type')
        self.db.add(price_type)
        await self.db.flush()
        return price_type.id
    async def _get_existing_pricing(self, product_id: UUID, price_type_id: UUID) -> Optional[ProductPricing]:
        query = select(ProductPricing).where(ProductPricing.product_id == product_id, ProductPricing.pricing_type_id == price_type_id, ProductPricing.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    async def import_data(self, data: List[ProductPricingImport]) -> Dict[str, Any]:
        if not data:
            return {'success': True, 'created': 0, 'updated': 0, 'errors': 0, 'total': 0}
        try:
            stats = {'created': 0, 'updated': 0, 'errors': 0, 'error_details': []}
            for pricing_data in data:
                try:
                    product_id = await self._get_product_id_by_part_number(pricing_data.part_number)
                    if not product_id:
                        stats['errors'] += 1
                        stats['error_details'].append({'part_number': pricing_data.part_number, 'error': f'Product not found with part number: {pricing_data.part_number}'})
                        continue
                    price_type_id = await self._get_or_create_price_type(pricing_data.pricing_type)
                    existing_pricing = await self._get_existing_pricing(product_id, price_type_id)
                    if existing_pricing:
                        existing_pricing.price = pricing_data.price
                        existing_pricing.currency = pricing_data.currency
                        self.db.add(existing_pricing)
                        stats['updated'] += 1
                    else:
                        new_pricing = ProductPricing(product_id=product_id, pricing_type_id=price_type_id, price=pricing_data.price, currency=pricing_data.currency)
                        self.db.add(new_pricing)
                        stats['created'] += 1
                except Exception as e:
                    logger.error(f'Error importing pricing for {pricing_data.part_number}: {str(e)}')
                    stats['errors'] += 1
                    stats['error_details'].append({'part_number': pricing_data.part_number, 'error': str(e)})
            await self.db.commit()
            logger.info(f"Pricing import complete: created {stats['created']}, updated {stats['updated']}, errors {stats['errors']}, total {len(data)}")
            return {'success': stats['errors'] == 0, 'created': stats['created'], 'updated': stats['updated'], 'errors': stats['errors'], 'error_details': stats['error_details'] if stats['errors'] > 0 else [], 'total': len(data)}
        except Exception as e:
            await self.db.rollback()
            logger.error(f'Transaction failed in pricing import: {str(e)}')
            raise DatabaseException(message=f'Pricing import transaction failed: {str(e)}', original_exception=e) from e