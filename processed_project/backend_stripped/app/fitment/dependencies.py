from __future__ import annotations
import os
from functools import lru_cache
from app.core.config import settings as app_settings
from .db import FitmentDBService
from .exceptions import ConfigurationError
from .mapper import FitmentMappingEngine
@lru_cache(maxsize=1)
def get_fitment_db_service() -> FitmentDBService:
    vcdb_path = app_settings.VCDB_PATH
    pcdb_path = app_settings.PCDB_PATH
    sqlalchemy_url = getattr(app_settings, 'FITMENT_DB_URL', None) or str(app_settings.SQLALCHEMY_DATABASE_URI)
    if not vcdb_path or not pcdb_path:
        raise ConfigurationError('VCDB_PATH and PCDB_PATH environment variables must be set')
    vcdb_path = _resolve_file_path(vcdb_path)
    pcdb_path = _resolve_file_path(pcdb_path)
    return FitmentDBService(vcdb_path, pcdb_path, sqlalchemy_url)
def _resolve_file_path(file_path: str) -> str:
    if os.path.isabs(file_path) and os.path.isfile(file_path):
        return file_path
    if os.path.isfile(file_path):
        return os.path.abspath(file_path)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    abs_path = os.path.join(project_root, file_path)
    if os.path.isfile(abs_path):
        return abs_path
    data_path = os.path.join(project_root, 'data', os.path.basename(file_path))
    if os.path.isfile(data_path):
        return data_path
    raise ConfigurationError(f'Could not find file: {file_path}')
@lru_cache(maxsize=1)
def get_fitment_mapping_engine() -> FitmentMappingEngine:
    db_service = get_fitment_db_service()
    engine = FitmentMappingEngine(db_service)
    return engine
async def initialize_mapping_engine() -> None:
    engine = get_fitment_mapping_engine()
    try:
        await engine.configure_from_database()
        return
    except Exception as e:
        from app.logging import get_logger
        logger = get_logger('app.fitment.dependencies')
        logger.warning(f'Failed to load model mappings from database: {str(e)}')
    mapping_file = getattr(app_settings, 'MODEL_MAPPINGS_PATH', None)
    if mapping_file and os.path.isfile(_resolve_file_path(mapping_file)):
        try:
            resolved_path = _resolve_file_path(mapping_file)
            engine.configure_from_file(resolved_path)
            try:
                await engine.db_service.import_mappings_from_json(engine.model_mappings)
                from app.logging import get_logger
                logger = get_logger('app.fitment.dependencies')
                logger.info('Successfully imported mappings from file to database')
            except Exception as e:
                from app.logging import get_logger
                logger = get_logger('app.fitment.dependencies')
                logger.warning(f'Failed to import mappings to database: {str(e)}')
        except Exception as e:
            from app.logging import get_logger
            logger = get_logger('app.fitment.dependencies')
            logger.error(f'Failed to load model mappings from file: {str(e)}')
            raise ConfigurationError(f'Failed to configure mapping engine: {str(e)}') from e