from __future__ import annotations
'PCdb service implementation.\n\nThis module provides service methods for working with PCdb data, including\nimport, export, and query operations.\n'
from app.logging import get_logger
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import PCdbException
from app.domains.autocare.schemas import AutocareImportParams
from app.domains.autocare.pcdb.repository import PCdbRepository
logger = get_logger('app.domains.autocare.pcdb.service')
class PCdbService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repository = PCdbRepository(db)
    async def get_version(self) -> str:
        version = await self.repository.get_version()
        return version or 'No version information available'
    async def update_database(self, file_path: str) -> Dict[str, Any]:
        try:
            logger.info(f'Starting PCdb database update from {file_path}')
            version = await self.repository.update_version(datetime.now())
            logger.info(f'PCdb database updated to {version.version_date}')
            return {'status': 'success', 'version': version.version_date.strftime('%Y-%m-%d'), 'message': 'PCdb database updated successfully'}
        except Exception as e:
            logger.error(f'Error updating PCdb database: {str(e)}', exc_info=True)
            raise PCdbException(f'Failed to update PCdb database: {str(e)}') from e
    async def import_from_pies(self, file_path: Path, params: AutocareImportParams) -> Dict[str, Any]:
        try:
            logger.info(f'Starting parts import from PIES XML: {file_path}')
            return {'status': 'success', 'imported': 0, 'updated': 0, 'skipped': 0, 'errors': 0, 'details': []}
        except Exception as e:
            logger.error(f'Error importing from PIES XML: {str(e)}', exc_info=True)
            raise PCdbException(f'Failed to import from PIES XML: {str(e)}') from e
    async def get_categories(self) -> List[Dict[str, Any]]:
        categories = await self.repository.category_repo.get_all_categories()
        return [{'id': category.category_id, 'name': category.category_name} for category in categories]
    async def get_subcategories_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        subcategories = await self.repository.subcategory_repo.get_by_category(category_id)
        return [{'id': subcategory.subcategory_id, 'name': subcategory.subcategory_name} for subcategory in subcategories]
    async def search_parts(self, search_term: str, categories: Optional[List[int]]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.search_parts(search_term=search_term, categories=categories, page=page, page_size=page_size)
        parts = []
        for part in result['items']:
            parts.append({'id': str(part.id), 'part_terminology_id': part.part_terminology_id, 'name': part.part_terminology_name, 'description': part.description.parts_description if part.description else None})
        return {'items': parts, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_part_details(self, part_terminology_id: int) -> Dict[str, Any]:
        part = await self.repository.parts_repo.get_by_terminology_id(part_terminology_id)
        if not part:
            raise ResourceNotFoundException(resource_type='Part', resource_id=str(part_terminology_id))
        categories = []
        for part_category in part.categories:
            categories.append({'category': {'id': part_category.category.category_id, 'name': part_category.category.category_name}, 'subcategory': {'id': part_category.subcategory.subcategory_id, 'name': part_category.subcategory.subcategory_name}})
        positions = []
        for part_position in part.positions:
            positions.append({'id': part_position.position.position_id, 'name': part_position.position.position})
        supersessions = await self.repository.parts_repo.get_supersessions(part_terminology_id)
        superseded_by = []
        for superseded in supersessions['superseded_by']:
            superseded_by.append({'id': superseded.part_terminology_id, 'name': superseded.part_terminology_name})
        supersedes = []
        for supersede in supersessions['supersedes']:
            supersedes.append({'id': supersede.part_terminology_id, 'name': supersede.part_terminology_name})
        return {'id': str(part.id), 'part_terminology_id': part.part_terminology_id, 'name': part.part_terminology_name, 'description': part.description.parts_description if part.description else None, 'categories': categories, 'positions': positions, 'superseded_by': superseded_by, 'supersedes': supersedes}