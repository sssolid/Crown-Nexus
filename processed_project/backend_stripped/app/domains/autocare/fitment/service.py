from __future__ import annotations
'Fitment mapping service implementation.\n\nThis module provides service methods for mapping products to autocare database entities.\n'
from app.logging import get_logger
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import MappingNotFoundException, ImportException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.fitment.repository import FitmentMappingRepository
from app.domains.autocare.fitment.models import FitmentMapping
from app.domains.products.repository import ProductRepository
logger = get_logger('app.domains.autocare.fitment.service')
class FitmentMappingService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repository = FitmentMappingRepository(db)
        self.product_repository = ProductRepository(db)
    async def import_from_aces(self, file_path: Path, params: AutocareImportParams) -> Dict[str, Any]:
        try:
            logger.info(f'Starting fitment mapping import from ACES XML: {file_path}')
            return {'status': 'success', 'imported': 0, 'updated': 0, 'skipped': 0, 'errors': 0, 'details': []}
        except Exception as e:
            logger.error(f'Error importing from ACES XML: {str(e)}', exc_info=True)
            raise ImportException(f'Failed to import from ACES XML: {str(e)}') from e
    async def create_mapping(self, data: Dict[str, Any], user_id: Optional[uuid.UUID]=None) -> FitmentMapping:
        product_id = data.get('product_id')
        if product_id:
            product = await self.product_repository.get_by_id(product_id)
            if not product:
                raise ResourceNotFoundException(resource_type='Product', resource_id=str(product_id))
        return await self.repository.create_with_history(data, user_id)
    async def update_mapping(self, mapping_id: uuid.UUID, data: Dict[str, Any], user_id: Optional[uuid.UUID]=None) -> FitmentMapping:
        try:
            return await self.repository.update_with_history(mapping_id, data, user_id)
        except ResourceNotFoundException as e:
            logger.error(f'Mapping not found: {str(e)}')
            raise MappingNotFoundException(resource_id=str(mapping_id)) from e
    async def delete_mapping(self, mapping_id: uuid.UUID, user_id: Optional[uuid.UUID]=None) -> None:
        try:
            await self.repository.delete_with_history(mapping_id, user_id)
        except ResourceNotFoundException as e:
            logger.error(f'Mapping not found: {str(e)}')
            raise MappingNotFoundException(resource_id=str(mapping_id)) from e
    async def get_mapping(self, mapping_id: uuid.UUID) -> Dict[str, Any]:
        mapping = await self.repository.get_by_id(mapping_id)
        if not mapping:
            raise MappingNotFoundException(resource_id=str(mapping_id))
        product = await self.product_repository.get_by_id(mapping.product_id)
        return {'id': str(mapping.id), 'product': {'id': str(product.id), 'part_number': product.part_number, 'application': product.application}, 'vehicle_id': mapping.vehicle_id, 'base_vehicle_id': mapping.base_vehicle_id, 'part_terminology_id': mapping.part_terminology_id, 'position_id': mapping.position_id, 'attributes': mapping.attributes, 'is_validated': mapping.is_validated, 'is_manual': mapping.is_manual, 'notes': mapping.notes, 'created_at': mapping.created_at.isoformat(), 'updated_at': mapping.updated_at.isoformat()}
    async def search_mappings(self, product_query: Optional[str]=None, is_validated: Optional[bool]=None, is_manual: Optional[bool]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.search(product_query=product_query, is_validated=is_validated, is_manual=is_manual, page=page, page_size=page_size)
        mappings = []
        for mapping in result['items']:
            product = await self.product_repository.get_by_id(mapping.product_id)
            mappings.append({'id': str(mapping.id), 'product': {'id': str(product.id), 'part_number': product.part_number, 'application': product.application}, 'vehicle_id': mapping.vehicle_id, 'base_vehicle_id': mapping.base_vehicle_id, 'part_terminology_id': mapping.part_terminology_id, 'position_id': mapping.position_id, 'is_validated': mapping.is_validated, 'is_manual': mapping.is_manual, 'updated_at': mapping.updated_at.isoformat()})
        return {'items': mappings, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_mapping_history(self, mapping_id: uuid.UUID, page: int=1, page_size: int=20) -> Dict[str, Any]:
        mapping = await self.repository.get_by_id(mapping_id)
        if not mapping:
            raise MappingNotFoundException(resource_id=str(mapping_id))
        result = await self.repository.get_mapping_history(mapping_id=mapping_id, page=page, page_size=page_size)
        history_items = []
        for history in result['items']:
            history_items.append({'id': str(history.id), 'change_type': history.change_type, 'previous_values': history.previous_values, 'new_values': history.new_values, 'changed_at': history.changed_at.isoformat(), 'changed_by_id': str(history.changed_by_id) if history.changed_by_id else None})
        return {'items': history_items, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def find_mappings_by_product(self, product_id: uuid.UUID, page: int=1, page_size: int=20) -> Dict[str, Any]:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundException(resource_type='Product', resource_id=str(product_id))
        result = await self.repository.find_by_product(product_id=product_id, page=page, page_size=page_size)
        mappings = []
        for mapping in result['items']:
            mappings.append({'id': str(mapping.id), 'vehicle_id': mapping.vehicle_id, 'base_vehicle_id': mapping.base_vehicle_id, 'part_terminology_id': mapping.part_terminology_id, 'position_id': mapping.position_id, 'is_validated': mapping.is_validated, 'is_manual': mapping.is_manual, 'updated_at': mapping.updated_at.isoformat()})
        return {'product': {'id': str(product.id), 'part_number': product.part_number, 'application': product.application}, 'mappings': mappings, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}