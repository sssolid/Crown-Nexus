from __future__ import annotations
'Qdb service implementation.\n\nThis module provides service methods for working with Qdb data, including\nimport, export, and query operations.\n'
from app.logging import get_logger
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.domains.autocare.exceptions import QdbException
from app.domains.autocare.qdb.repository import QdbRepository
logger = get_logger('app.domains.autocare.qdb.service')
class QdbService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repository = QdbRepository(db)
    async def get_version(self) -> str:
        version = await self.repository.get_version()
        return version or 'No version information available'
    async def get_stats(self) -> Dict[str, Any]:
        total_qualifiers = await self.repository.qualifier_repo.count()
        qualifier_type_count = await self.repository.qualifier_type_repo.count()
        language_count = await self.repository.language_repo.count()
        group_count = await self.repository.group_repo.count()
        return {'totalQualifiers': total_qualifiers, 'qualifierTypeCount': qualifier_type_count, 'languageCount': language_count, 'groupCount': group_count}
    async def update_database(self, file_path: str) -> Dict[str, Any]:
        try:
            logger.info(f'Starting Qdb database update from {file_path}')
            version = await self.repository.update_version(datetime.now())
            logger.info(f'Qdb database updated to {version.version_date}')
            return {'status': 'success', 'version': version.version_date.strftime('%Y-%m-%d'), 'message': 'Qdb database updated successfully'}
        except Exception as e:
            logger.error(f'Error updating Qdb database: {str(e)}', exc_info=True)
            raise QdbException(f'Failed to update Qdb database: {str(e)}') from e
    async def get_qualifier_types(self) -> List[Dict[str, Any]]:
        types = await self.repository.qualifier_type_repo.get_all_types()
        return [{'id': qt.qualifier_type_id, 'name': qt.qualifier_type} for qt in types]
    async def get_languages(self) -> List[Dict[str, Any]]:
        languages = await self.repository.language_repo.get_all_languages()
        return [{'id': lang.language_id, 'name': lang.language_name, 'dialect': lang.dialect_name} for lang in languages]
    async def search_qualifiers(self, search_term: str, qualifier_type_id: Optional[int]=None, language_id: Optional[int]=None, page: int=1, page_size: int=20) -> Dict[str, Any]:
        result = await self.repository.search_qualifiers(search_term=search_term, qualifier_type_id=qualifier_type_id, language_id=language_id, page=page, page_size=page_size)
        qualifiers = []
        for qualifier in result['items']:
            qualifiers.append({'id': str(qualifier.id), 'qualifier_id': qualifier.qualifier_id, 'text': qualifier.qualifier_text, 'example': qualifier.example_text, 'type_id': qualifier.qualifier_type_id, 'superseded_by': qualifier.new_qualifier_id})
        return {'items': qualifiers, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
    async def get_qualifier_details(self, qualifier_id: int) -> Dict[str, Any]:
        qualifier = await self.repository.qualifier_repo.get_by_qualifier_id(qualifier_id)
        if not qualifier:
            raise ResourceNotFoundException(resource_type='Qualifier', resource_id=str(qualifier_id))
        qualifier_type = await self.repository.qualifier_type_repo.get_by_qualifier_type_id(qualifier.qualifier_type_id)
        translations = await self.repository.qualifier_repo.get_translations(qualifier_id)
        translations_list = []
        for translation in translations:
            language = await self.repository.language_repo.get_by_language_id(translation.language_id)
            translations_list.append({'id': translation.qualifier_translation_id, 'language': {'id': language.language_id, 'name': language.language_name, 'dialect': language.dialect_name}, 'text': translation.translation_text})
        groups = await self.repository.qualifier_repo.get_groups(qualifier_id)
        groups_list = []
        for group_data in groups:
            groups_list.append({'id': group_data['group'].qualifier_group_id, 'number': {'id': group_data['group_number'].group_number_id, 'description': group_data['group_number'].group_description}})
        superseded_info = None
        if qualifier.new_qualifier_id:
            superseding_qualifier = await self.repository.qualifier_repo.get_by_qualifier_id(qualifier.new_qualifier_id)
            if superseding_qualifier:
                superseded_info = {'id': superseding_qualifier.qualifier_id, 'text': superseding_qualifier.qualifier_text}
        return {'id': str(qualifier.id), 'qualifier_id': qualifier.qualifier_id, 'text': qualifier.qualifier_text, 'example': qualifier.example_text, 'type': {'id': qualifier_type.qualifier_type_id, 'name': qualifier_type.qualifier_type}, 'translations': translations_list, 'groups': groups_list, 'superseded_by': superseded_info, 'when_modified': qualifier.when_modified.isoformat()}