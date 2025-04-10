from __future__ import annotations
'QDB API endpoints for accessing Qualifier Database.\n\nThis module provides HTTP endpoints for interacting with QDB data,\nincluding qualifiers, qualifier types, languages, and groups.\n'
from typing import Annotated, Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user, get_db, get_pagination
from app.api.responses import paginated_response, success_response
from app.domains.autocare.qdb.service import QdbService
from app.domains.users.models import User
router = APIRouter()
@router.get('/version')
async def get_version(db: Annotated[AsyncSession, Depends(get_db)]) -> str:
    service = QdbService(db)
    version = await service.get_version()
    return version
@router.get('/stats')
async def get_qdb_stats(db: Annotated[AsyncSession, Depends(get_db)]) -> Dict[str, Any]:
    service = QdbService(db)
    stats = await service.get_stats()
    return stats
@router.get('/qualifier-types')
async def get_qualifier_types(db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = QdbService(db)
    types = await service.get_qualifier_types()
    return types
@router.get('/languages')
async def get_languages(db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = QdbService(db)
    languages = await service.get_languages()
    return languages
@router.get('/qualifiers/search')
async def search_qualifiers(db: Annotated[AsyncSession, Depends(get_db)], search_term: str=Query(..., description='Search term for qualifiers'), qualifier_type_id: Optional[int]=Query(None, description='Filter by qualifier type ID'), language_id: Optional[int]=Query(None, description='Filter by language ID'), page: int=Query(1, ge=1, description='Page number'), page_size: int=Query(20, ge=1, le=100, description='Items per page')) -> Dict[str, Any]:
    service = QdbService(db)
    result = await service.search_qualifiers(search_term=search_term, qualifier_type_id=qualifier_type_id, language_id=language_id, page=page, page_size=page_size)
    return result
@router.get('/qualifiers/{qualifier_id}')
async def get_qualifier_details(qualifier_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> Dict[str, Any]:
    service = QdbService(db)
    details = await service.get_qualifier_details(qualifier_id)
    return details
@router.get('/groups')
async def get_group_numbers(db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = QdbService(db)
    groups = await service.repository.group_repo.get_all_groups()
    return [{'id': group.group_number_id, 'description': group.group_description} for group in groups]
@router.get('/groups/{group_number_id}/qualifiers')
async def get_qualifiers_by_group(db: Annotated[AsyncSession, Depends(get_db)], group_number_id: int, page: int=Query(1, ge=1, description='Page number'), page_size: int=Query(20, ge=1, le=100, description='Items per page')) -> Dict[str, Any]:
    service = QdbService(db)
    result = await service.repository.group_repo.get_qualifiers_by_group(group_number_id=group_number_id, page=page, page_size=page_size)
    qualifiers = []
    for qualifier in result['items']:
        qualifiers.append({'id': str(qualifier.id), 'qualifier_id': qualifier.qualifier_id, 'text': qualifier.qualifier_text, 'example': qualifier.example_text, 'type_id': qualifier.qualifier_type_id, 'superseded_by': qualifier.new_qualifier_id})
    return {'items': qualifiers, 'total': result['total'], 'page': result['page'], 'page_size': result['page_size'], 'pages': result['pages']}
@router.get('/qualifiers/{qualifier_id}/translations')
async def get_qualifier_translations(db: Annotated[AsyncSession, Depends(get_db)], qualifier_id: int, language_id: Optional[int]=Query(None, description='Filter by language ID')) -> List[Dict[str, Any]]:
    service = QdbService(db)
    translations = await service.repository.qualifier_repo.get_translations(qualifier_id=qualifier_id, language_id=language_id)
    result = []
    for translation in translations:
        language = await service.repository.language_repo.get_by_language_id(translation.language_id)
        result.append({'id': translation.qualifier_translation_id, 'language': {'id': language.language_id, 'name': language.language_name, 'dialect': language.dialect_name}, 'text': translation.translation_text})
    return result
@router.get('/qualifiers/{qualifier_id}/groups')
async def get_qualifier_groups(qualifier_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> List[Dict[str, Any]]:
    service = QdbService(db)
    groups = await service.repository.qualifier_repo.get_groups(qualifier_id=qualifier_id)
    return [{'id': group['group'].qualifier_group_id, 'number': {'id': group['group_number'].group_number_id, 'description': group['group_number'].group_description}} for group in groups]