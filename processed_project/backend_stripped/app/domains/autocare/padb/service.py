from __future__ import annotations
'PAdb service implementation.\n\nThis module provides service methods for working with PAdb data, including\nimport, export, and query operations.\n'
from app.logging import get_logger
from datetime import datetime
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import PAdbException
from app.domains.autocare.padb.repository import PAdbRepository
logger = get_logger('app.domains.autocare.padb.service')
class PAdbService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repository = PAdbRepository(db)
    async def get_version(self) -> str:
        version = await self.repository.get_version()
        return version or 'No version information available'
    async def update_database(self, file_path: str) -> Dict[str, Any]:
        try:
            logger.info(f'Starting PAdb database update from {file_path}')
            version = await self.repository.update_version(datetime.now())
            logger.info(f'PAdb database updated to {version.version_date}')
            return {'status': 'success', 'version': version.version_date.strftime('%Y-%m-%d'), 'message': 'PAdb database updated successfully'}
        except Exception as e:
            logger.error(f'Error updating PAdb database: {str(e)}', exc_info=True)
            raise PAdbException(f'Failed to update PAdb database: {str(e)}') from e
    async def search_attributes(self, search_term: str, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.attribute_repo.search(search_term=search_term, page=page, page_size=page_size)
        attributes = []
        for attribute in result['items']:
            attributes.append({'id': str(attribute.id), 'pa_id': attribute.pa_id, 'name': attribute.pa_name, 'description': attribute.pa_descr})
        return {'items': attributes, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_attribute_details(self, pa_id: int) -> Dict[str, Any]:
        attribute = await self.repository.attribute_repo.get_by_pa_id(pa_id)
        if not attribute:
            raise ResourceNotFoundException(resource_type='PartAttribute', resource_id=str(pa_id))
        assignments = await self.db.execute('\n            SELECT\n                paa.papt_id,\n                paa.part_terminology_id,\n                md.meta_id,\n                md.meta_name,\n                md.meta_descr,\n                md.data_type\n            FROM\n                autocare_part_attribute_assignment paa\n            JOIN\n                autocare_metadata md ON paa.meta_id = md.meta_id\n            WHERE\n                paa.pa_id = :pa_id\n            ', {'pa_id': pa_id})
        metadata_list = []
        for row in assignments:
            metadata_list.append({'assignment_id': row.papt_id, 'part_terminology_id': row.part_terminology_id, 'meta_id': row.meta_id, 'name': row.meta_name, 'description': row.meta_descr, 'data_type': row.data_type})
        return {'id': str(attribute.id), 'pa_id': attribute.pa_id, 'name': attribute.pa_name, 'description': attribute.pa_descr, 'metadata_assignments': metadata_list}
    async def get_part_attributes(self, part_terminology_id: int) -> Dict[str, Any]:
        attributes = await self.repository.get_attributes_for_part(part_terminology_id)
        result = []
        for attr_data in attributes:
            assignment = attr_data['assignment']
            attribute = attr_data['attribute']
            metadata = attr_data['metadata']
            valid_values = []
            for vv in attr_data['valid_values']:
                valid_values.append({'id': vv.valid_value_id, 'value': vv.valid_value})
            uom_codes = []
            for uom in attr_data['uom_codes']:
                uom_codes.append({'id': uom.meta_uom_id, 'code': uom.uom_code, 'description': uom.uom_description, 'label': uom.uom_label})
            result.append({'assignment_id': assignment.papt_id, 'attribute': {'id': attribute.pa_id, 'name': attribute.pa_name, 'description': attribute.pa_descr}, 'metadata': {'id': metadata.meta_id, 'name': metadata.meta_name, 'description': metadata.meta_descr, 'format': metadata.meta_format, 'data_type': metadata.data_type}, 'valid_values': valid_values, 'uom_codes': uom_codes})
        return {'part_terminology_id': part_terminology_id, 'attributes': result}