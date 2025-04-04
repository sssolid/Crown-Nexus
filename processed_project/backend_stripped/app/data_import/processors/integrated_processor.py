from __future__ import annotations
'\nIntegrated product data processor.\n\nThis module provides a comprehensive processor for product data that handles\nrelated elements like descriptions, marketing, and pricing in an integrated manner.\n'
import re
from typing import Any, Dict, List, Optional, Set, cast
from app.domains.products.schemas import ProductCreate, ProductDescriptionCreate, ProductMarketingCreate, ProductPricingImport
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS, COMPLEX_FIELD_MAPPINGS, ExternalFieldInfo
from app.data_import.processors.generic_processor import GenericProcessor
from app.logging import get_logger
logger = get_logger('app.data_import.processors.integrated_processor')
class IntegratedProductProcessor(GenericProcessor[ProductCreate]):
    def __init__(self, source_type: str) -> None:
        super().__init__(field_definitions=ENTITY_FIELD_DEFINITIONS['product'], model_type=ProductCreate, source_type=source_type)
        self.description_field_map = self._create_field_alias_map('descriptions')
        self.marketing_field_map = self._create_field_alias_map('marketing')
        logger.debug(f'IntegratedProductProcessor initialized for {source_type} source')
    def _create_field_alias_map(self, complex_field: str) -> Dict[str, str]:
        field_map = {}
        if 'product' in COMPLEX_FIELD_MAPPINGS and complex_field in COMPLEX_FIELD_MAPPINGS['product']:
            if self.source_type in COMPLEX_FIELD_MAPPINGS['product'][complex_field]:
                mappings = COMPLEX_FIELD_MAPPINGS['product'][complex_field][self.source_type]
                for field_type, field_info in mappings.items():
                    if isinstance(field_info, ExternalFieldInfo):
                        original_field = field_info.field_name
                        field_map[original_field] = field_type
                        field_map[field_type] = field_type
                        field_map[original_field.lower()] = field_type
                        field_map[field_type.lower()] = field_type
        return field_map
    def _process_complex_field(self, processed_record: Dict[str, Any], original_record: Dict[str, Any], complex_field: str, mappings: Dict[str, Any]) -> None:
        logger.debug(f"Processing complex field '{complex_field}' with {len(mappings)} mappings")
        field_names = list(original_record.keys())
        if logger.isEnabledFor(10):
            logger.debug(f'Original record has {len(field_names)} fields: {field_names[:10]}')
        items = []
        field_map = self.description_field_map if complex_field == 'descriptions' else self.marketing_field_map
        if complex_field == 'marketing':
            bullet_pattern = re.compile('bullet(\\d+)', re.IGNORECASE)
            bullet_fields = []
            for field_name in field_names:
                match = bullet_pattern.match(field_name)
                if match and field_name in field_map:
                    position = int(match.group(1))
                    value = original_record[field_name]
                    if value and (not isinstance(value, str) or value.strip()):
                        bullet_fields.append((position, field_name, value))
            bullet_fields.sort(key=lambda x: x[0])
            for position, field_name, value in bullet_fields:
                items.append(ProductMarketingCreate(marketing_type=field_map[field_name], content=str(value).strip(), position=position))
                logger.debug(f"Added marketing bullet {position} from field '{field_name}'")
            for field_name in field_names:
                if field_name in field_map and (not bullet_pattern.match(field_name)):
                    value = original_record[field_name]
                    if value and (not isinstance(value, str) or value.strip()):
                        field_type = field_map[field_name]
                        items.append(ProductMarketingCreate(marketing_type=field_type, content=str(value).strip(), position=len(items) + 1))
                        logger.debug(f"Added marketing '{field_type}' from field '{field_name}'")
        else:
            for field_name in field_names:
                if field_name in field_map:
                    field_type = field_map[field_name]
                    value = original_record[field_name]
                    if value and (not isinstance(value, str) or value.strip()):
                        items.append(ProductDescriptionCreate(description_type=field_type, description=str(value).strip()))
                        logger.debug(f"Added description '{field_type}' from field '{field_name}'")
        if items:
            processed_record[complex_field] = items
            logger.info(f"Added {len(items)} items to '{complex_field}'")
        else:
            logger.info(f"No items found for complex field '{complex_field}'")
    async def process_pricing(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        processed_data = []
        skipped_records = 0
        invalid_price_records = 0
        for i, record in enumerate(data):
            try:
                if 'SPART' in record:
                    part_number = str(record['SPART']).strip()
                elif 'part_number' in record:
                    part_number = str(record['part_number']).strip()
                else:
                    if i == 0:
                        logger.warning(f'Available fields in record: {list(record.keys())}')
                    skipped_records += 1
                    if i % 1000 == 0:
                        logger.warning(f'Record at index {i} is missing part number. Available fields: {list(record.keys())}')
                    continue
                if not part_number:
                    skipped_records += 1
                    continue
                jobber_price = None
                if 'SRET1' in record and record['SRET1'] is not None:
                    try:
                        jobber_value = record['SRET1']
                        if jobber_value == '' or jobber_value is None:
                            jobber_price = None
                        else:
                            jobber_price = float(jobber_value)
                            if jobber_price <= 0:
                                jobber_price = None
                    except (ValueError, TypeError):
                        invalid_price_records += 1
                        if i % 1000 == 0:
                            logger.warning(f"Invalid Jobber price for {part_number}: {record['SRET1']}")
                export_price = None
                if 'SRET2' in record and record['SRET2'] is not None:
                    try:
                        export_value = record['SRET2']
                        if export_value == '' or export_value is None:
                            export_price = None
                        else:
                            export_price = float(export_value)
                            if export_price <= 0:
                                export_price = None
                    except (ValueError, TypeError):
                        invalid_price_records += 1
                        if i % 1000 == 0:
                            logger.warning(f"Invalid Export price for {part_number}: {record['SRET2']}")
                if jobber_price is not None:
                    jobber_record = {'part_number': part_number, 'pricing_type': 'Jobber', 'price': jobber_price, 'currency': 'USD'}
                    processed_data.append(jobber_record)
                if export_price is not None:
                    export_record = {'part_number': part_number, 'pricing_type': 'Export', 'price': export_price, 'currency': 'USD'}
                    processed_data.append(export_record)
            except Exception as e:
                logger.warning(f'Error processing pricing record at index {i}: {str(e)}')
        logger.info(f'Processed {len(processed_data)} pricing records from {len(data)} input records. Skipped {skipped_records} records with missing part numbers. Found {invalid_price_records} records with invalid prices.')
        return processed_data
    async def validate_pricing(self, data: List[Dict[str, Any]]) -> List[ProductPricingImport]:
        validated_data = []
        validation_errors = []
        for i, item in enumerate(data):
            try:
                validated_item = ProductPricingImport(**item)
                validated_data.append(validated_item)
            except Exception as e:
                logger.warning(f'Validation error for pricing at index {i}: {str(e)}')
                validation_errors.append({'index': i, 'part_number': item.get('part_number', f'index_{i}'), 'error': str(e)})
        if validation_errors:
            logger.warning(f'Validated {len(validated_data)} pricing records with {len(validation_errors)} validation errors')
        else:
            logger.info(f'Validated {len(validated_data)} pricing records successfully')
        return validated_data