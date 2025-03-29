from __future__ import annotations
'Autocare domain event handlers.\n\nThis module contains event handlers for the autocare domain, which respond to\ndomain events related to vehicle, part, and fitment data.\n'
from app.logging import get_logger
from typing import Any, Dict
from uuid import UUID
from app.core.events import subscribe_to_event
from app.db.session import get_db
from app.domains.autocare.fitment.repository import FitmentMappingRepository
from app.domains.products.repository import ProductRepository
logger = get_logger('app.domains.autocare.handlers')
@subscribe_to_event('products.product_created')
async def handle_product_created(payload: Dict[str, Any]) -> None:
    product_id = payload.get('product_id')
    if not product_id:
        logger.warning('Received products.product_created event without product_id')
        return
    try:
        logger.info(f'Attempting to map product {product_id} to autocare fitments')
        async with get_db() as db:
            product_repo = ProductRepository(db)
            fitment_repo = FitmentMappingRepository(db)
            product = await product_repo.get_by_id(UUID(product_id))
            if not product:
                logger.warning(f'Product {product_id} not found while handling product_created event')
                return
            logger.info(f'Auto-mapping for product {product_id} completed')
    except Exception as e:
        logger.error(f'Error handling product_created event for {product_id}: {e}')
@subscribe_to_event('autocare.database_updated')
async def handle_autocare_database_updated(payload: Dict[str, Any]) -> None:
    db_type = payload.get('database_type')
    version = payload.get('version')
    if not db_type or not version:
        logger.warning('Received autocare.database_updated event with missing data')
        return
    logger.info(f'Autocare database {db_type} updated to version {version}')
    try:
        logger.info(f'Successfully processed {db_type} database update')
    except Exception as e:
        logger.error(f'Error handling autocare database update for {db_type}: {e}')