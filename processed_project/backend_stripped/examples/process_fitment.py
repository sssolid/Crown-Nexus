import asyncio
import json
import os
import sys
from typing import Dict, List
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.fitment.config import FitmentSettings, configure_logging
from app.fitment.db import FitmentDBService
from app.fitment.mapper import FitmentMappingEngine
from app.fitment.models import ValidationStatus
async def main():
    configure_logging()
    os.environ['FITMENT_VCDB_PATH'] = 'data/vcdb.mdb'
    os.environ['FITMENT_PCDB_PATH'] = 'data/pcdb.mdb'
    os.environ['FITMENT_MODEL_MAPPINGS_PATH'] = 'path/to/mappings.xlsx'
    settings = FitmentSettings()
    db_service = FitmentDBService(settings.vcdb_path, settings.pcdb_path, settings.db_url)
    mapping_engine = FitmentMappingEngine(db_service)
    if settings.model_mappings_path:
        mapping_engine.configure(settings.model_mappings_path)
    application_texts = ['2005-2010 WK Grand Cherokee (Left or Right Front Upper Ball Joint);', '2007-2013 JK Wrangler (Front Lower Control Arm);']
    part_terminology_id = 58869
    results = mapping_engine.batch_process_applications(application_texts, part_terminology_id)
    for app_text, validation_results in results.items():
        print(f'\nApplication: {app_text}')
        for i, result in enumerate(validation_results):
            status_str = '✅' if result.status == ValidationStatus.VALID else '⚠️' if result.status == ValidationStatus.WARNING else '❌'
            print(f'  Result {i + 1}: {status_str} {result.message}')
            if result.fitment:
                vehicle = result.fitment.vehicle
                positions = result.fitment.positions
                print(f'    Vehicle: {vehicle.year} {vehicle.make} {vehicle.model}')
                print(f'    Positions: FR={positions.front_rear.value}, LR={positions.left_right.value}, UL={positions.upper_lower.value}, IO={positions.inner_outer.value}')
                print(f'    VCDB Vehicle ID: {result.fitment.vcdb_vehicle_id}')
                print(f'    PCDB Position IDs: {result.fitment.pcdb_position_ids}')
    product_id = 'EXAMPLE-PRODUCT-123'
    all_results = []
    for app_results in results.values():
        all_results.extend(app_results)
    try:
        success = await mapping_engine.save_mapping_results(product_id, all_results)
        if success:
            print(f'\nSuccessfully saved fitment results for product {product_id}')
        else:
            print(f'\nFailed to save fitment results for product {product_id}')
    except Exception as e:
        print(f'\nError saving fitment results: {str(e)}')
if __name__ == '__main__':
    asyncio.run(main())