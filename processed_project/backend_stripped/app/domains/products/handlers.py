from __future__ import annotations
'Product domain event handlers.\n\nThis module contains event handlers for the products domain.\n'
from app.logging import get_logger
from typing import Any, Dict
from uuid import UUID
from app.core.events import subscribe_to_event
from app.db.session import get_db
from app.domains.products.repository import ProductRepository
logger = get_logger('app.domains.products.handlers')
@subscribe_to_event('inventory.stock_level_critical')
async def handle_critical_stock_level(payload: Dict[str, Any]) -> None:
    product_id = payload['product_id']
    stock_level = payload['stock_level']
    threshold = payload['threshold']
    logger.info(f'Product {product_id} has critical stock level {stock_level} (below threshold {threshold})')
    async with get_db() as db:
        repository = ProductRepository(db)
        try:
            product = await repository.get_by_id(UUID(product_id))
            if product and product.is_active:
                await repository.update_status(product_id=UUID(product_id), status='out_of_stock', reason=f'Stock level ({stock_level}) below threshold ({threshold})')
                logger.info(f'Updated product {product_id} status to out_of_stock')
        except Exception as e:
            logger.error(f'Error updating product status for {product_id}: {e}')
@subscribe_to_event('pricing.price_update')
async def handle_price_update(payload: Dict[str, Any]) -> None:
    updates = payload.get('updates', [])
    if not updates:
        logger.warning('Received pricing.price_update event with no updates')
        return
    async with get_db() as db:
        repository = ProductRepository(db)
        for update in updates:
            product_id = update.get('product_id')
            new_price = update.get('new_price')
            if not product_id or new_price is None:
                logger.warning(f'Invalid price update data: {update}')
                continue
            try:
                logger.info(f'Updating price for product {product_id} to {new_price}')
            except Exception as e:
                logger.error(f'Error updating product price for {product_id}: {e}')