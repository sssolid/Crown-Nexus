from __future__ import annotations
'\nGeneric data processor.\n\nThis module provides a generic processor base class that can process\ndata based on field definitions from the central source of truth.\n'
from typing import Any, Dict, Generic, List, Optional, Set, Type, TypeVar, cast
from pydantic import BaseModel, ValidationError
from app.core.exceptions import ValidationException
from app.logging import get_logger
from app.data_import.field_definitions import EntityFieldDefinitions, FieldDefinition, TransformationDirection, COMPLEX_FIELD_MAPPINGS, ExternalFieldInfo
logger = get_logger('app.data_import.processors.generic_processor')
T = TypeVar('T', bound=BaseModel)
class GenericProcessor(Generic[T]):
    def __init__(self, field_definitions: EntityFieldDefinitions, model_type: Type[T], source_type: str) -> None:
        self.field_definitions = field_definitions
        self.model_type = model_type
        self.source_type = source_type
        self.field_mapping = field_definitions.get_external_field_mapping(source_type)
        self.processed_keys: Set[str] = set()
        self.complex_mappings = COMPLEX_FIELD_MAPPINGS.get(field_definitions.entity_name, {})
        logger.debug(f'Initialized GenericProcessor for {field_definitions.entity_name} from {source_type} source')
    def _get_reverse_field_mapping(self) -> Dict[str, str]:
        reverse = {}
        for k, v in self.field_mapping.items():
            if isinstance(v, str):
                reverse[v] = k
            else:
                logger.error(f'Non-hashable field mapping value: {v} for key: {k}')
        return reverse
    def _apply_field_transformations(self, field_def: FieldDefinition, value: Any, direction: TransformationDirection) -> Any:
        if not field_def.transformations:
            return value
        transformed_value = value
        for transform in field_def.transformations:
            if transform.direction == direction:
                if transform.transformation:
                    transformed_value = transform.transformation(transformed_value)
        return transformed_value
    def _process_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        processed_record: Dict[str, Any] = {}
        for field_def in self.field_definitions.fields:
            if field_def.field_type in ['ARRAY', 'OBJECT'] and (not field_def.get_external_names()):
                continue
            external_field = self.field_mapping.get(field_def.name)
            if not external_field and field_def.get_external_names():
                continue
            value = None
            if external_field and external_field in record:
                value = record[external_field]
            elif field_def.name in record:
                value = record[field_def.name]
            if value is None and field_def.default is not None:
                value = field_def.default
            if field_def.required and value is None:
                raise ValueError(f'Missing required field: {field_def.name}')
            if value is not None:
                value = self._apply_field_transformations(field_def, value, TransformationDirection.IMPORT)
            processed_record[field_def.name] = value
        processed_record = self._process_complex_fields(processed_record, record)
        return processed_record
    def _process_complex_fields(self, processed_record: Dict[str, Any], original_record: Dict[str, Any]) -> Dict[str, Any]:
        for complex_field, mappings in self.complex_mappings.items():
            source_mappings = mappings.get(self.source_type, {})
            if not source_mappings:
                continue
            self._process_complex_field(processed_record, original_record, complex_field, source_mappings)
        return processed_record
    def _process_complex_field(self, processed_record: Dict[str, Any], original_record: Dict[str, Any], complex_field: str, mappings: Dict[str, ExternalFieldInfo]) -> None:
        items = []
        for item_type, field_info in mappings.items():
            try:
                if not isinstance(field_info, ExternalFieldInfo):
                    logger.error(f"Invalid field_info for '{item_type}': {field_info}")
                    continue
                field_name = field_info.field_name
                if field_name in original_record and original_record[field_name]:
                    items.append({f'{complex_field[:-1]}_type': item_type, 'content': str(original_record[field_name])})
            except Exception as e:
                logger.error(f"Error processing complex field '{complex_field}' item '{item_type}': {e}")
        if items:
            processed_record[complex_field] = items
    async def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        processed_data = []
        errors = []
        self.processed_keys.clear()
        for i, record in enumerate(data):
            try:
                processed_record = self._process_record(record)
                processed_record = self._process_complex_fields(processed_record, record)
                primary_key_field = self.field_definitions.primary_key_field
                if primary_key_field in processed_record and processed_record[primary_key_field]:
                    key_value = processed_record[primary_key_field]
                    if key_value in self.processed_keys:
                        logger.warning(f'Duplicate key: {key_value}')
                        errors.append({'index': i, 'key': key_value, 'error': f'Duplicate {primary_key_field}'})
                        continue
                    self.processed_keys.add(key_value)
                processed_data.append(processed_record)
            except ValueError as e:
                logger.warning(f'Error processing record at index {i}: {str(e)}')
                errors.append({'index': i, 'error': str(e), 'record': record})
            except Exception as e:
                logger.error(f'Unexpected error processing record at index {i}: {str(e)}')
                errors.append({'index': i, 'error': f'Unexpected error: {str(e)}', 'record': record})
        if errors:
            logger.warning(f'Processed {len(processed_data)} records with {len(errors)} errors')
        else:
            logger.info(f'Processed {len(processed_data)} records successfully')
        return processed_data
    async def validate(self, data: List[Dict[str, Any]]) -> List[T]:
        validated_data = []
        validation_errors = []
        for i, item in enumerate(data):
            try:
                validated_item = self.model_type(**item)
                validated_data.append(validated_item)
            except ValidationError as e:
                logger.warning(f'Validation error at index {i}: {str(e)}')
                key_value = item.get(self.field_definitions.primary_key_field, f'index_{i}')
                validation_errors.append({'index': i, 'key': key_value, 'error': str(e)})
            except Exception as e:
                logger.error(f'Unexpected error validating record at index {i}: {str(e)}')
                key_value = item.get(self.field_definitions.primary_key_field, f'index_{i}')
                validation_errors.append({'index': i, 'key': key_value, 'error': f'Unexpected error: {str(e)}'})
        if validation_errors:
            logger.warning(f'Validated {len(validated_data)} records with {len(validation_errors)} validation errors')
            if len(validation_errors) >= len(data):
                raise ValidationException(message='All records failed validation', errors=validation_errors)
        else:
            logger.info(f'Validated {len(validated_data)} records successfully')
        return validated_data