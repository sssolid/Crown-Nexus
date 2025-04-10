from __future__ import annotations
'\nQdb (Qualifier Database) data importer.\n\nThis module provides a specialized importer for Qdb data from various formats,\nmapping external data to the correct database models with proper transformations.\n'
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.autocare.importers.flexible_importer import FlexibleImporter, SourceFormat, detect_source_format
from app.domains.autocare.qdb.models import QualifierType, Qualifier, Language, QualifierTranslation, GroupNumber, QualifierGroup, QdbVersion
from app.logging import get_logger
logger = get_logger('app.domains.autocare.importers.qdb_importer')
class QdbImporter(FlexibleImporter):
    def __init__(self, db: AsyncSession, source_path: Path, source_format: Optional[SourceFormat]=None, batch_size: int=1000):
        if source_format is None:
            source_format = detect_source_format(source_path)
            logger.info(f'Auto-detected source format: {source_format.value}')
        file_ext = '.json' if source_format == SourceFormat.JSON else '.txt'
        required_sources = [f'Version{file_ext}', f'QualifierType{file_ext}', f'Qualifier{file_ext}']
        super().__init__(db=db, source_path=source_path, schema_name='qdb', required_sources=required_sources, version_class=QdbVersion, source_format=source_format, version_date_field='version_date', batch_size=batch_size)
        self._register_mappings()
        self.set_import_order([f'QualifierType{file_ext}', f'Qualifier{file_ext}', f'GroupNumber{file_ext}', f'QualifierGroup{file_ext}'])
    def _register_mappings(self) -> None:
        file_ext = '.json' if self.source_format == SourceFormat.JSON else '.txt'
        self.register_table_mapping(source_name=f'QualifierType{file_ext}', model_class=QualifierType, field_mapping={'qualifier_type_id': 'QualifierTypeID', 'qualifier_type': 'QualifierType'}, primary_key='qualifier_type_id', transformers={'qualifier_type_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'Qualifier{file_ext}', model_class=Qualifier, field_mapping={'qualifier_id': 'QualifierID', 'qualifier_text': 'QualifierText', 'example_text': 'ExampleText', 'qualifier_type_id': 'QualifierTypeID', 'new_qualifier_id': 'NewQualifierID', 'when_modified': 'WhenModified'}, primary_key='qualifier_id', transformers={'qualifier_id': lambda x: int(x) if x else None, 'qualifier_type_id': lambda x: int(x) if x else None, 'new_qualifier_id': lambda x: int(x) if x else None, 'when_modified': lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S') if x and x.strip() else datetime.now()})
        self.register_table_mapping(source_name=f'GroupNumber{file_ext}', model_class=GroupNumber, field_mapping={'group_number_id': 'GroupNumberId', 'group_description': 'GroupNumberDescription'}, primary_key='group_number_id', transformers={'group_number_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'QualifierGroup{file_ext}', model_class=QualifierGroup, field_mapping={'qualifier_group_id': 'QualifierGroupId', 'group_number_id': 'GroupNumberId', 'qualifier_id': 'QualifierId'}, primary_key='qualifier_group_id', transformers={'qualifier_group_id': lambda x: int(x) if x else None, 'group_number_id': lambda x: int(x) if x else None, 'qualifier_id': lambda x: int(x) if x else None})