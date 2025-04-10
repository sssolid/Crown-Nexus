from __future__ import annotations
'\nAS400-specific data importers.\n\nThis module provides data importers for AS400 synchronization operations,\nimplementing the logic to create or update records in the application database.\n'
from datetime import datetime
from typing import Any, Dict, List, TypeVar
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DatabaseException
from app.logging import get_logger
from app.domains.products.models import Product, ProductMeasurement, ProductPricing, ProductStock, Manufacturer, PriceType
from app.domains.currency.models import Currency
from app.domains.reference.models import Warehouse
from app.domains.products.schemas import ProductCreate, ProductMeasurementCreate, ProductStock as ProductStockSchema
from app.data_import.importers.base import Importer
logger = get_logger('app.data_import.importers.as400_importers')
T = TypeVar('T')
class AS400BaseImporter(Importer[T]):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        logger.debug(f'Initialized {self.__class__.__name__}')
    async def get_existing_entities(self, id_field: str, id_values: List[Any], model: Any) -> Dict[Any, Any]:
        if not id_values:
            return {}
        try:
            query = select(model).where(getattr(model, id_field).in_(id_values), model.is_deleted == False)
            result = await self.db.execute(query)
            entities = result.scalars().all()
            return {getattr(entity, id_field): entity for entity in entities}
        except Exception as e:
            logger.error(f'Error fetching existing {model.__name__} entities: {str(e)}')
            raise DatabaseException(message=f'Failed to fetch existing {model.__name__} entities: {str(e)}', original_exception=e) from e
    async def track_sync(self, entity_type: str, created: int, updated: int, errors: int) -> None:
        logger.info(f'AS400 Sync: {entity_type} - created={created}, updated={updated}, errors={errors}')
class ProductAS400Importer(AS400BaseImporter[ProductCreate]):
    async def import_data(self, data: List[ProductCreate]) -> Dict[str, Any]:
        if not data:
            return {'success': True, 'created': 0, 'updated': 0, 'errors': 0, 'total': 0}
        try:
            part_numbers = [p.part_number for p in data]
            existing_products = await self.get_existing_entities(id_field='part_number', id_values=part_numbers, model=Product)
            stats = {'created': 0, 'updated': 0, 'errors': 0, 'error_details': []}
            for product_data in data:
                try:
                    existing_product = existing_products.get(product_data.part_number)
                    if existing_product:
                        await self._update_product(existing_product, product_data)
                        stats['updated'] += 1
                    else:
                        await self._create_product(product_data)
                        stats['created'] += 1
                except Exception as e:
                    logger.error(f'Error importing product {product_data.part_number}: {str(e)}')
                    stats['errors'] += 1
                    stats['error_details'].append({'part_number': product_data.part_number, 'error': str(e)})
            await self.db.commit()
            await self.track_sync(entity_type='Product', created=stats['created'], updated=stats['updated'], errors=stats['errors'])
            return {'success': stats['errors'] == 0, 'created': stats['created'], 'updated': stats['updated'], 'errors': stats['errors'], 'error_details': stats['error_details'] if stats['errors'] > 0 else [], 'total': len(data)}
        except Exception as e:
            await self.db.rollback()
            logger.error(f'Transaction failed in product import: {str(e)}')
            raise DatabaseException(message=f'Product import transaction failed: {str(e)}', original_exception=e) from e
    async def _create_product(self, product_data: ProductCreate) -> Product:
        product = Product(part_number=product_data.part_number, part_number_stripped=product_data.part_number_stripped, application=product_data.application, vintage=product_data.vintage, late_model=product_data.late_model, soft=product_data.soft, universal=product_data.universal, is_active=product_data.is_active)
        self.db.add(product)
        await self.db.flush()
        if hasattr(product_data, 'descriptions') and product_data.descriptions:
            for desc_data in product_data.descriptions:
                from app.domains.products.models import ProductDescription
                description = ProductDescription(product_id=product.id, description_type=desc_data.description_type, description=desc_data.description)
                self.db.add(description)
        if hasattr(product_data, 'marketing') and product_data.marketing:
            for mkt_data in product_data.marketing:
                from app.domains.products.models import ProductMarketing
                marketing = ProductMarketing(product_id=product.id, marketing_type=mkt_data.marketing_type, content=mkt_data.content, position=mkt_data.position)
                self.db.add(marketing)
        await self.db.flush()
        await self.db.refresh(product)
        logger.debug(f'Created new product: {product.part_number}')
        return product
    async def _update_product(self, existing_product: Product, product_data: ProductCreate) -> Product:
        existing_product.application = product_data.application
        existing_product.vintage = product_data.vintage
        existing_product.late_model = product_data.late_model
        existing_product.soft = product_data.soft
        existing_product.universal = product_data.universal
        existing_product.is_active = product_data.is_active
        self.db.add(existing_product)
        if hasattr(product_data, 'descriptions') and product_data.descriptions:
            from app.domains.products.models import ProductDescription
            await self.db.execute(delete(ProductDescription).where(ProductDescription.product_id == existing_product.id))
            for desc_data in product_data.descriptions:
                description = ProductDescription(product_id=existing_product.id, description_type=desc_data.description_type, description=desc_data.description)
                self.db.add(description)
        if hasattr(product_data, 'marketing') and product_data.marketing:
            from app.domains.products.models import ProductMarketing
            await self.db.execute(delete(ProductMarketing).where(ProductMarketing.product_id == existing_product.id))
            for mkt_data in product_data.marketing:
                marketing = ProductMarketing(product_id=existing_product.id, marketing_type=mkt_data.marketing_type, content=mkt_data.content, position=mkt_data.position)
                self.db.add(marketing)
        await self.db.flush()
        await self.db.refresh(existing_product)
        logger.debug(f'Updated product: {existing_product.part_number}')
        return existing_product
class ProductMeasurementImporter(AS400BaseImporter[ProductMeasurementCreate]):
    async def import_data(self, data: List[ProductMeasurementCreate]) -> Dict[str, Any]:
        if not data:
            return {'success': True, 'created': 0, 'updated': 0, 'errors': 0, 'total': 0}
        try:
            product_ids = [m.product_id for m in data]
            existing_products = await self.get_existing_entities(id_field='id', id_values=product_ids, model=Product)
            manufacturer_ids = [m.manufacturer_id for m in data if m.manufacturer_id is not None]
            existing_manufacturers = {}
            if manufacturer_ids:
                existing_manufacturers = await self.get_existing_entities(id_field='id', id_values=manufacturer_ids, model=Manufacturer)
            stats = {'created': 0, 'updated': 0, 'errors': 0, 'error_details': []}
            for measurement_data in data:
                try:
                    if measurement_data.product_id not in existing_products:
                        stats['errors'] += 1
                        stats['error_details'].append({'product_id': str(measurement_data.product_id), 'error': 'Product does not exist'})
                        continue
                    if measurement_data.manufacturer_id is not None and measurement_data.manufacturer_id not in existing_manufacturers:
                        stats['errors'] += 1
                        stats['error_details'].append({'product_id': str(measurement_data.product_id), 'manufacturer_id': str(measurement_data.manufacturer_id), 'error': 'Manufacturer does not exist'})
                        continue
                    query = select(ProductMeasurement).where(ProductMeasurement.product_id == measurement_data.product_id, ProductMeasurement.manufacturer_id == measurement_data.manufacturer_id, ProductMeasurement.is_deleted == False)
                    result = await self.db.execute(query)
                    existing_measurement = result.scalars().first()
                    if existing_measurement:
                        existing_measurement.length = measurement_data.length
                        existing_measurement.width = measurement_data.width
                        existing_measurement.height = measurement_data.height
                        existing_measurement.weight = measurement_data.weight
                        existing_measurement.volume = measurement_data.volume
                        existing_measurement.dimensional_weight = measurement_data.dimensional_weight
                        existing_measurement.effective_date = datetime.now()
                        self.db.add(existing_measurement)
                        stats['updated'] += 1
                    else:
                        new_measurement = ProductMeasurement(product_id=measurement_data.product_id, manufacturer_id=measurement_data.manufacturer_id, length=measurement_data.length, width=measurement_data.width, height=measurement_data.height, weight=measurement_data.weight, volume=measurement_data.volume, dimensional_weight=measurement_data.dimensional_weight, effective_date=datetime.now())
                        self.db.add(new_measurement)
                        stats['created'] += 1
                except Exception as e:
                    logger.error(f'Error importing measurement for product {measurement_data.product_id}: {str(e)}')
                    stats['errors'] += 1
                    stats['error_details'].append({'product_id': str(measurement_data.product_id), 'error': str(e)})
            await self.db.flush()
            await self.db.commit()
            await self.track_sync(entity_type='ProductMeasurement', created=stats['created'], updated=stats['updated'], errors=stats['errors'])
            return {'success': stats['errors'] == 0, 'created': stats['created'], 'updated': stats['updated'], 'errors': stats['errors'], 'error_details': stats['error_details'] if stats['errors'] > 0 else [], 'total': len(data)}
        except Exception as e:
            await self.db.rollback()
            logger.error(f'Transaction failed in measurement import: {str(e)}')
            raise DatabaseException(message=f'Measurement import transaction failed: {str(e)}', original_exception=e) from e
class ProductStockImporter(AS400BaseImporter[ProductStockSchema]):
    async def import_data(self, data: List[ProductStockSchema]) -> Dict[str, Any]:
        if not data:
            return {'success': True, 'created': 0, 'updated': 0, 'errors': 0, 'total': 0}
        try:
            product_ids = [s.product_id for s in data]
            existing_products = await self.get_existing_entities(id_field='id', id_values=product_ids, model=Product)
            warehouse_ids = [s.warehouse_id for s in data]
            existing_warehouses = await self.get_existing_entities(id_field='id', id_values=warehouse_ids, model=Warehouse)
            stats = {'created': 0, 'updated': 0, 'errors': 0, 'error_details': []}
            for stock_data in data:
                try:
                    if stock_data.product_id not in existing_products:
                        stats['errors'] += 1
                        stats['error_details'].append({'product_id': str(stock_data.product_id), 'error': 'Product does not exist'})
                        continue
                    if stock_data.warehouse_id not in existing_warehouses:
                        stats['errors'] += 1
                        stats['error_details'].append({'product_id': str(stock_data.product_id), 'warehouse_id': str(stock_data.warehouse_id), 'error': 'Warehouse does not exist'})
                        continue
                    query = select(ProductStock).where(ProductStock.product_id == stock_data.product_id, ProductStock.warehouse_id == stock_data.warehouse_id, ProductStock.is_deleted == False)
                    result = await self.db.execute(query)
                    existing_stock = result.scalars().first()
                    if existing_stock:
                        existing_stock.quantity = stock_data.quantity
                        existing_stock.last_updated = datetime.now()
                        self.db.add(existing_stock)
                        stats['updated'] += 1
                    else:
                        new_stock = ProductStock(product_id=stock_data.product_id, warehouse_id=stock_data.warehouse_id, quantity=stock_data.quantity, last_updated=datetime.now())
                        self.db.add(new_stock)
                        stats['created'] += 1
                except Exception as e:
                    logger.error(f'Error importing stock for product {stock_data.product_id}: {str(e)}')
                    stats['errors'] += 1
                    stats['error_details'].append({'product_id': str(stock_data.product_id), 'error': str(e)})
            await self.db.flush()
            await self.db.commit()
            await self.track_sync(entity_type='ProductStock', created=stats['created'], updated=stats['updated'], errors=stats['errors'])
            return {'success': stats['errors'] == 0, 'created': stats['created'], 'updated': stats['updated'], 'errors': stats['errors'], 'error_details': stats['error_details'] if stats['errors'] > 0 else [], 'total': len(data)}
        except Exception as e:
            await self.db.rollback()
            logger.error(f'Transaction failed in stock import: {str(e)}')
            raise DatabaseException(message=f'Stock import transaction failed: {str(e)}', original_exception=e) from e
class ProductPricingImporter(AS400BaseImporter[Any]):
    async def import_data(self, data: List[Any]) -> Dict[str, Any]:
        if not data:
            return {'success': True, 'created': 0, 'updated': 0, 'errors': 0, 'total': 0}
        try:
            product_ids = [p.product_id for p in data]
            existing_products = await self.get_existing_entities(id_field='id', id_values=product_ids, model=Product)
            price_type_ids = [p.pricing_type_id for p in data]
            existing_price_types = await self.get_existing_entities(id_field='id', id_values=price_type_ids, model=PriceType)
            currencies = set((p.currency for p in data))
            existing_currencies = {}
            if currencies:
                currencies_query = select(Currency).where(Currency.code.in_(currencies), Currency.is_deleted == False)
                currencies_result = await self.db.execute(currencies_query)
                existing_currencies = {c.code: c for c in currencies_result.scalars().all()}
            default_currency = None
            if 'USD' in existing_currencies:
                default_currency = existing_currencies['USD']
            else:
                default_currency_query = select(Currency).where(Currency.is_base == True, Currency.is_deleted == False)
                default_currency_result = await self.db.execute(default_currency_query)
                default_currency = default_currency_result.scalars().first()
            stats = {'created': 0, 'updated': 0, 'errors': 0, 'error_details': []}
            for pricing_data in data:
                try:
                    if pricing_data.product_id not in existing_products:
                        stats['errors'] += 1
                        stats['error_details'].append({'product_id': str(pricing_data.product_id), 'error': 'Product does not exist'})
                        continue
                    if pricing_data.pricing_type_id not in existing_price_types:
                        stats['errors'] += 1
                        stats['error_details'].append({'product_id': str(pricing_data.product_id), 'pricing_type_id': str(pricing_data.pricing_type_id), 'error': 'Price type does not exist'})
                        continue
                    currency_code = pricing_data.currency
                    if currency_code not in existing_currencies and default_currency:
                        logger.warning(f"Unknown currency '{currency_code}', using default: {default_currency.code}")
                        currency_code = default_currency.code
                    query = select(ProductPricing).where(ProductPricing.product_id == pricing_data.product_id, ProductPricing.pricing_type_id == pricing_data.pricing_type_id, ProductPricing.is_deleted == False)
                    if hasattr(pricing_data, 'manufacturer_id') and pricing_data.manufacturer_id:
                        query = query.where(ProductPricing.manufacturer_id == pricing_data.manufacturer_id)
                    result = await self.db.execute(query)
                    existing_pricing = result.scalars().first()
                    if existing_pricing:
                        existing_pricing.price = pricing_data.price
                        existing_pricing.currency = currency_code
                        existing_pricing.last_updated = datetime.now()
                        self.db.add(existing_pricing)
                        stats['updated'] += 1
                    else:
                        new_pricing = ProductPricing(product_id=pricing_data.product_id, pricing_type_id=pricing_data.pricing_type_id, price=pricing_data.price, currency=currency_code, last_updated=datetime.now())
                        if hasattr(pricing_data, 'manufacturer_id') and pricing_data.manufacturer_id:
                            new_pricing.manufacturer_id = pricing_data.manufacturer_id
                        self.db.add(new_pricing)
                        stats['created'] += 1
                except Exception as e:
                    logger.error(f'Error importing pricing for product {pricing_data.product_id}: {str(e)}')
                    stats['errors'] += 1
                    stats['error_details'].append({'product_id': str(pricing_data.product_id), 'error': str(e)})
            await self.db.flush()
            await self.db.commit()
            await self.track_sync(entity_type='ProductPricing', created=stats['created'], updated=stats['updated'], errors=stats['errors'])
            return {'success': stats['errors'] == 0, 'created': stats['created'], 'updated': stats['updated'], 'errors': stats['errors'], 'error_details': stats['error_details'] if stats['errors'] > 0 else [], 'total': len(data)}
        except Exception as e:
            await self.db.rollback()
            logger.error(f'Transaction failed in pricing import: {str(e)}')
            raise DatabaseException(message=f'Pricing import transaction failed: {str(e)}', original_exception=e) from e