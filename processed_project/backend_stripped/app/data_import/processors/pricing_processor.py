from __future__ import annotations
'Product pricing data processor.\n\nThis module provides a specialized processor for transforming AS400 product pricing data\ninto separate records for different pricing types (Jobber and Export).\n'
from typing import Any, Dict, List
from app.logging import get_logger
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS
from app.data_import.processors.generic_processor import GenericProcessor
from app.data_import.schemas.pricing import ProductPricingImport
logger = get_logger('app.data_import.processors.pricing_processor')
class PricingProcessor(GenericProcessor[ProductPricingImport]):
    def __init__(self, source_type: str) -> None:
        super().__init__(field_definitions=ENTITY_FIELD_DEFINITIONS['product_pricing'], model_type=ProductPricingImport, source_type=source_type)
        logger.debug(f'PricingProcessor initialized for {source_type} source')
    async def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self.source_type != 'as400':
            return await super().process(data)
        if data and len(data) > 0:
            logger.debug(f'First record field names: {list(data[0].keys())}')
            logger.debug(f'First record content: {data[0]}')
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