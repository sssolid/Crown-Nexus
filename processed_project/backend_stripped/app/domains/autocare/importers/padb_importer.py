from __future__ import annotations
'\nPAdb (Part Attribute Database) data importer.\n\nThis module provides a specialized importer for PAdb data from various formats,\nmapping external data to the correct database models with proper transformations.\n'
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.autocare.importers.flexible_importer import FlexibleImporter, SourceFormat, detect_source_format
from app.domains.autocare.padb.models import PartAttribute, MetaData, MeasurementGroup, MetaUOMCode, PartAttributeAssignment, MetaUomCodeAssignment, ValidValue, ValidValueAssignment, Style, PartAttributeStyle, PartTypeStyle, PAdbVersion
from app.logging import get_logger
logger = get_logger('app.domains.autocare.importers.padb_importer')
class PAdbImporter(FlexibleImporter):
    def __init__(self, db: AsyncSession, source_path: Path, source_format: Optional[SourceFormat]=None, batch_size: int=1000):
        if source_format is None:
            source_format = detect_source_format(source_path)
            logger.info(f'Auto-detected source format: {source_format.value}')
        file_ext = '.json' if source_format == SourceFormat.JSON else '.txt'
        required_sources = [f'Version{file_ext}', f'PartAttributes{file_ext}', f'MetaData{file_ext}', f'MeasurementGroup{file_ext}', f'MetaUOMCodes{file_ext}', f'PartAttributeAssignment{file_ext}']
        super().__init__(db=db, source_path=source_path, schema_name='padb', required_sources=required_sources, version_class=PAdbVersion, source_format=source_format, version_date_field='version_date', batch_size=batch_size)
        self._register_mappings()
        self.set_import_order([f'PartAttributes{file_ext}', f'MetaData{file_ext}', f'MeasurementGroup{file_ext}', f'MetaUOMCodes{file_ext}', f'PartAttributeAssignment{file_ext}', f'MetaUOMCodeAssignment{file_ext}', f'ValidValues{file_ext}', f'ValidValueAssignment{file_ext}', f'Style{file_ext}', f'PartAttributeStyle{file_ext}', f'PartTypeStyle{file_ext}'])
    def _register_mappings(self) -> None:
        file_ext = '.json' if self.source_format == SourceFormat.JSON else '.txt'
        self.register_table_mapping(source_name=f'PartAttributes{file_ext}', model_class=PartAttribute, field_mapping={'pa_id': 'PAID', 'pa_name': 'PAName', 'pa_descr': 'PADescr'}, primary_key='pa_id', transformers={'pa_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'MetaData{file_ext}', model_class=MetaData, field_mapping={'meta_id': 'MetaID', 'meta_name': 'MetaName', 'meta_descr': 'MetaDescr', 'meta_format': 'MetaFormat', 'data_type': 'DataType', 'min_length': 'MinLength', 'max_length': 'MaxLength'}, primary_key='meta_id', transformers={'meta_id': lambda x: int(x) if x else None, 'min_length': lambda x: int(x) if x else None, 'max_length': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'MeasurementGroup{file_ext}', model_class=MeasurementGroup, field_mapping={'measurement_group_id': 'MeasurementGroupID', 'measurement_group_name': 'MeasurementGroupName'}, primary_key='measurement_group_id', transformers={'measurement_group_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'MetaUOMCodes{file_ext}', model_class=MetaUOMCode, field_mapping={'meta_uom_id': 'MetaUOMID', 'uom_code': 'UOMCode', 'uom_description': 'UOMDescription', 'uom_label': 'UOMLabel', 'measurement_group_id': 'MeasurementGroupId'}, primary_key='meta_uom_id', transformers={'meta_uom_id': lambda x: int(x) if x else None, 'measurement_group_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'PartAttributeAssignment{file_ext}', model_class=PartAttributeAssignment, field_mapping={'papt_id': 'PAPTID', 'part_terminology_id': 'PartTerminologyID', 'pa_id': 'PAID', 'meta_id': 'MetaID'}, primary_key='papt_id', transformers={'papt_id': lambda x: int(x) if x else None, 'part_terminology_id': lambda x: int(x) if x else None, 'pa_id': lambda x: int(x) if x else None, 'meta_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'MetaUOMCodeAssignment{file_ext}', model_class=MetaUomCodeAssignment, field_mapping={'meta_uom_code_assignment_id': 'MetaUomCodeAssignmentID', 'papt_id': 'PAPTID', 'meta_uom_id': 'MetaUomID'}, primary_key='meta_uom_code_assignment_id', transformers={'meta_uom_code_assignment_id': lambda x: int(x) if x else None, 'papt_id': lambda x: int(x) if x else None, 'meta_uom_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'ValidValues{file_ext}', model_class=ValidValue, field_mapping={'valid_value_id': 'ValidValueID', 'valid_value': 'ValidValue'}, primary_key='valid_value_id', transformers={'valid_value_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'ValidValueAssignment{file_ext}', model_class=ValidValueAssignment, field_mapping={'valid_value_assignment_id': 'ValidValueAssignmentID', 'papt_id': 'PAPTID', 'valid_value_id': 'ValidValueID'}, primary_key='valid_value_assignment_id', transformers={'valid_value_assignment_id': lambda x: int(x) if x else None, 'papt_id': lambda x: int(x) if x else None, 'valid_value_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'Style{file_ext}', model_class=Style, field_mapping={'style_id': 'StyleID', 'style_name': 'StyleName'}, primary_key='style_id', transformers={'style_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'PartAttributeStyle{file_ext}', model_class=PartAttributeStyle, field_mapping={'style_id': 'StyleID', 'papt_id': 'PAPTID'}, primary_key='id', transformers={'style_id': lambda x: int(x) if x else None, 'papt_id': lambda x: int(x) if x else None})
        self.register_table_mapping(source_name=f'PartTypeStyle{file_ext}', model_class=PartTypeStyle, field_mapping={'style_id': 'StyleID', 'part_terminology_id': 'PartTerminologyID'}, primary_key='id', transformers={'style_id': lambda x: int(x) if x else None, 'part_terminology_id': lambda x: int(x) if x else None})