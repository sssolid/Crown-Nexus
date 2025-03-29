from __future__ import annotations
'\nAS400 data processor.\n\nThis module provides base and specific processors for transforming data from\nAS400 databases into the format required by the application.\n'
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Set, Type, TypeVar, Union
from pydantic import BaseModel
from app.core.exceptions import ValidationException
from app.logging import get_logger
logger = get_logger('app.data_import.processors.as400_processor')
T = TypeVar('T', bound=BaseModel)
class AS400ProcessorConfig(BaseModel):
    field_mapping: Dict[str, str] = {}
    boolean_true_values: List[str] = ['1', 'Y', 'YES', 'TRUE', 'T']
    boolean_false_values: List[str] = ['0', 'N', 'NO', 'FALSE', 'F']
    default_values: Dict[str, Any] = {}
    skip_fields: List[str] = []
    required_fields: List[str] = []
    date_format: str = '%Y-%m-%d'
    time_format: str = '%H:%M:%S'
    timestamp_format: str = '%Y-%m-%d %H:%M:%S'
    unique_key_field: Optional[str] = None
class AS400BaseProcessor(Generic[T], ABC):
    def __init__(self, config: AS400ProcessorConfig, destination_model: Type[T]) -> None:
        self.config = config
        self.destination_model = destination_model
        self.processed_keys: Set[str] = set()
        self.field_mapping = {as400_field: model_field for model_field, as400_field in config.field_mapping.items()}
        logger.debug(f'Initialized {self.__class__.__name__} for model {destination_model.__name__}')
    async def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        processed_data = []
        errors = []
        self.processed_keys.clear()
        for i, record in enumerate(data):
            try:
                processed_record = self._process_record(record)
                if self.config.unique_key_field and processed_record.get(self.config.unique_key_field):
                    key = processed_record[self.config.unique_key_field]
                    if key in self.processed_keys:
                        logger.warning(f'Duplicate key: {key}')
                        errors.append({'index': i, 'key': key, 'error': 'Duplicate key'})
                        continue
                    self.processed_keys.add(key)
                processed_data.append(processed_record)
            except Exception as e:
                logger.warning(f'Error processing record at index {i}: {str(e)}')
                errors.append({'index': i, 'error': str(e), 'record': record})
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
                validated_item = self.destination_model(**item)
                validated_data.append(validated_item)
            except Exception as e:
                logger.warning(f'Validation error at index {i}: {str(e)}')
                key_value = item.get(self.config.unique_key_field, f'index_{i}')
                validation_errors.append({'index': i, 'key': key_value, 'error': str(e)})
        if validation_errors:
            logger.warning(f'Validated {len(validated_data)} records with {len(validation_errors)} validation errors')
            if len(validation_errors) >= len(data):
                raise ValidationException(message='All records failed validation', errors=validation_errors)
        else:
            logger.info(f'Validated {len(validated_data)} records successfully')
        return validated_data
    def _process_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        processed_record = self.config.default_values.copy()
        for as400_field, value in record.items():
            if as400_field in self.config.skip_fields:
                continue
            model_field = self.field_mapping.get(as400_field, as400_field)
            processed_value = self._process_field_value(as400_field, value)
            processed_record[model_field] = processed_value
        processed_record = self._process_record_custom(processed_record, record)
        for field in self.config.required_fields:
            if field not in processed_record or processed_record[field] is None:
                raise ValueError(f'Missing required field: {field}')
        return processed_record
    def _process_field_value(self, field_name: str, value: Any) -> Any:
        if value is None:
            return None
        if field_name.startswith(('IS_', 'HAS_')) or field_name.endswith(('_FLAG', '_YN', '_INDICATOR')):
            return self._convert_to_boolean(value)
        if field_name.endswith(('_DATE', '_DT')):
            return self._convert_to_date(value)
        if field_name.endswith(('_TIME', '_TM')):
            return self._convert_to_time(value)
        if field_name.endswith(('_TIMESTAMP', '_TS')):
            return self._convert_to_timestamp(value)
        if field_name.endswith(('_QTY', '_AMOUNT', '_AMT', '_NUM', '_PRICE')) and isinstance(value, (str, int, float)):
            return self._convert_to_numeric(value)
        if isinstance(value, str):
            return value.strip()
        return value
    def _convert_to_boolean(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return value != 0
        str_value = str(value).strip().upper()
        if str_value in self.config.boolean_true_values:
            return True
        if str_value in self.config.boolean_false_values:
            return False
        return False
    def _convert_to_date(self, value: Any) -> Optional[datetime]:
        if not value or value in ['0000-00-00', '00/00/0000']:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            value = value.strip()
            try:
                return datetime.strptime(value, self.config.date_format)
            except ValueError:
                for fmt in ['%Y%m%d', '%m/%d/%Y', '%d/%m/%Y']:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
        logger.warning(f'Could not parse date value: {value}')
        return None
    def _convert_to_time(self, value: Any) -> Optional[datetime]:
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            value = value.strip()
            try:
                time_obj = datetime.strptime(value, self.config.time_format)
                today = datetime.today()
                return datetime(today.year, today.month, today.day, time_obj.hour, time_obj.minute, time_obj.second)
            except ValueError:
                for fmt in ['%H%M%S', '%I:%M:%S %p', '%H:%M']:
                    try:
                        time_obj = datetime.strptime(value, fmt)
                        today = datetime.today()
                        return datetime(today.year, today.month, today.day, time_obj.hour, time_obj.minute, time_obj.second)
                    except ValueError:
                        continue
        logger.warning(f'Could not parse time value: {value}')
        return None
    def _convert_to_timestamp(self, value: Any) -> Optional[datetime]:
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            value = value.strip()
            try:
                return datetime.strptime(value, self.config.timestamp_format)
            except ValueError:
                for fmt in ['%Y%m%d%H%M%S', '%Y-%m-%dT%H:%M:%S', '%m/%d/%Y %I:%M:%S %p']:
                    try:
                        return datetime.strptime(value, fmt)
                    except ValueError:
                        continue
        logger.warning(f'Could not parse timestamp value: {value}')
        return None
    def _convert_to_numeric(self, value: Any) -> Optional[Union[int, float]]:
        if value is None or value == '':
            return None
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            cleaned_value = re.sub('[^\\d.-]', '', value)
            if not cleaned_value or cleaned_value in ['.', '-', '.-', '-.']:
                return None
            try:
                numeric_value = float(cleaned_value)
                if numeric_value.is_integer():
                    return int(numeric_value)
                return numeric_value
            except ValueError:
                logger.warning(f'Could not convert to numeric: {value}')
                return None
        return None
    @abstractmethod
    def _process_record_custom(self, processed_record: Dict[str, Any], original_record: Dict[str, Any]) -> Dict[str, Any]:
        pass
class ProductAS400Processor(AS400BaseProcessor[T]):
    def _process_record_custom(self, processed_record: Dict[str, Any], original_record: Dict[str, Any]) -> Dict[str, Any]:
        if 'part_number' in processed_record and 'part_number_stripped' not in processed_record:
            part_number = processed_record['part_number']
            if part_number:
                processed_record['part_number_stripped'] = self._normalize_part_number(part_number)
        return processed_record
    def _normalize_part_number(self, part_number: str) -> str:
        return ''.join((c for c in part_number if c.isalnum())).upper()
class PricingAS400Processor(AS400BaseProcessor[T]):
    def _process_record_custom(self, processed_record: Dict[str, Any], original_record: Dict[str, Any]) -> Dict[str, Any]:
        if 'price' in processed_record and processed_record['price'] is not None:
            try:
                processed_record['price'] = float(processed_record['price'])
            except (ValueError, TypeError):
                processed_record['price'] = 0.0
        if 'currency' not in processed_record or not processed_record['currency']:
            processed_record['currency'] = 'USD'
        return processed_record
class InventoryAS400Processor(AS400BaseProcessor[T]):
    def _process_record_custom(self, processed_record: Dict[str, Any], original_record: Dict[str, Any]) -> Dict[str, Any]:
        if 'quantity' in processed_record:
            try:
                processed_record['quantity'] = int(float(processed_record['quantity']))
            except (ValueError, TypeError):
                processed_record['quantity'] = 0
        if 'quantity' in processed_record and processed_record['quantity'] < 0:
            processed_record['quantity'] = 0
        if 'last_updated' not in processed_record:
            processed_record['last_updated'] = datetime.now()
        return processed_record