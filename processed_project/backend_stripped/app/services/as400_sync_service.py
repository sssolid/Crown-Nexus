from __future__ import annotations
'\nAS400 synchronization service.\n\nThis module provides a service to manage and schedule AS400 data synchronization\noperations, ensuring secure and consistent data flow.\n'
import asyncio
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config.integrations.as400 import as400_settings, get_as400_connector_config
from app.core.exceptions import ConfigurationException
from app.logging import get_logger
from app.data_import.connectors.as400_connector import AS400Connector, AS400ConnectionConfig
from app.data_import.pipeline.as400_pipeline import AS400Pipeline
from app.db.session import get_db_context
from app.domains.products.models import Product
from app.domains.reference.models import Warehouse
from app.domains.products.schemas import ProductCreate, ProductMeasurementCreate, ProductStock as ProductStockSchema
from app.data_import.processors.as400_processor import AS400ProcessorConfig, ProductAS400Processor
from app.data_import.importers.as400_importers import ProductAS400Importer, ProductMeasurementImporter, ProductStockImporter
logger = get_logger('app.services.as400_sync_service')
class SyncEntityType(str, Enum):
    PRODUCT = 'product'
    MEASUREMENT = 'measurement'
    STOCK = 'stock'
    PRICING = 'pricing'
    MANUFACTURER = 'manufacturer'
    CUSTOMER = 'customer'
    ORDER = 'order'
class SyncStatus(str, Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
class SyncLog:
    def __init__(self, entity_type: SyncEntityType, status: SyncStatus=SyncStatus.PENDING, records_processed: int=0, records_created: int=0, records_updated: int=0, records_failed: int=0, started_at: Optional[datetime]=None, completed_at: Optional[datetime]=None, error_message: Optional[str]=None) -> None:
        self.entity_type = entity_type
        self.status = status
        self.records_processed = records_processed
        self.records_created = records_created
        self.records_updated = records_updated
        self.records_failed = records_failed
        self.started_at = started_at or datetime.now()
        self.completed_at = completed_at
        self.error_message = error_message
    def complete(self, status: SyncStatus, records_processed: int, records_created: int, records_updated: int, records_failed: int, error_message: Optional[str]=None) -> None:
        self.status = status
        self.records_processed = records_processed
        self.records_created = records_created
        self.records_updated = records_updated
        self.records_failed = records_failed
        self.completed_at = datetime.now()
        self.error_message = error_message
class AS400SyncService:
    _instance: Optional[AS400SyncService] = None
    _lock = asyncio.Lock()
    _initialized = False
    _sync_history: List[SyncLog] = []
    _active_syncs: Set[SyncEntityType] = set()
    _last_sync_times: Dict[SyncEntityType, datetime] = {}
    _scheduled_tasks: Dict[SyncEntityType, asyncio.Task] = {}
    @classmethod
    def get_instance(cls) -> AS400SyncService:
        if cls._instance is None:
            cls._instance = AS400SyncService()
        return cls._instance
    def __init__(self) -> None:
        if AS400SyncService._instance is not None:
            raise RuntimeError('AS400SyncService is a singleton. Use get_instance() instead.')
        logger.debug('Initializing AS400SyncService')
    async def initialize(self) -> None:
        async with self._lock:
            if self._initialized:
                return
            logger.info('Initializing AS400 sync service')
            if not as400_settings.AS400_SYNC_ENABLED:
                logger.info('AS400 sync is disabled in configuration')
                return
            try:
                self._last_sync_times = {}
                for entity_type in SyncEntityType:
                    self._last_sync_times[entity_type] = datetime.now() - timedelta(days=1)
                if as400_settings.AS400_SYNC_ENABLED:
                    for entity_type in SyncEntityType:
                        await self.schedule_sync(entity_type)
                self._initialized = True
                logger.info('AS400 sync service initialized successfully')
            except Exception as e:
                logger.error(f'Failed to initialize AS400 sync service: {str(e)}')
                raise ConfigurationException(message=f'Failed to initialize AS400 sync service: {str(e)}', component='AS400SyncService', original_exception=e) from e
    async def shutdown(self) -> None:
        async with self._lock:
            if not self._initialized:
                return
            logger.info('Shutting down AS400 sync service')
            for entity_type, task in self._scheduled_tasks.items():
                if not task.done():
                    logger.info(f'Cancelling scheduled sync for {entity_type.value}')
                    task.cancel()
            self._scheduled_tasks = {}
            self._initialized = False
            logger.info('AS400 sync service shut down successfully')
    async def schedule_sync(self, entity_type: SyncEntityType, delay_seconds: Optional[int]=None) -> None:
        if entity_type in self._scheduled_tasks:
            task = self._scheduled_tasks[entity_type]
            if not task.done():
                task.cancel()
        if delay_seconds is None:
            delay_seconds = as400_settings.AS400_SYNC_INTERVAL
        task = asyncio.create_task(self._schedule_sync_task(entity_type, delay_seconds))
        self._scheduled_tasks[entity_type] = task
        logger.info(f'Scheduled sync for {entity_type.value} in {delay_seconds} seconds')
    async def run_sync(self, entity_type: SyncEntityType, force: bool=False) -> Dict[str, Any]:
        if entity_type in self._active_syncs and (not force):
            logger.warning(f'Sync for {entity_type.value} is already running, skipping')
            return {'success': False, 'message': f'Sync for {entity_type.value} is already running', 'entity_type': entity_type.value, 'status': 'skipped'}
        self._active_syncs.add(entity_type)
        sync_log = SyncLog(entity_type=entity_type, status=SyncStatus.RUNNING)
        self._sync_history.append(sync_log)
        try:
            logger.info(f'Starting sync for {entity_type.value}')
            async with get_db_context() as db:
                result = await self._run_entity_sync(entity_type, db)
                self._last_sync_times[entity_type] = datetime.now()
                status = SyncStatus.COMPLETED if result.get('success', False) else SyncStatus.FAILED
                sync_log.complete(status=status, records_processed=result.get('records_processed', 0), records_created=result.get('records_created', 0), records_updated=result.get('records_updated', 0), records_failed=result.get('records_with_errors', 0), error_message=result.get('error', None))
                await self._log_sync_audit(db=db, entity_type=entity_type, result=result)
                logger.info(f"Completed sync for {entity_type.value} - processed: {result.get('records_processed', 0)}, created: {result.get('records_created', 0)}, updated: {result.get('records_updated', 0)}, errors: {result.get('records_with_errors', 0)}")
                await self.schedule_sync(entity_type)
                return {'success': result.get('success', False), 'message': result.get('message', 'Sync completed'), 'entity_type': entity_type.value, 'status': status.value, 'records_processed': result.get('records_processed', 0), 'records_created': result.get('records_created', 0), 'records_updated': result.get('records_updated', 0), 'records_failed': result.get('records_with_errors', 0), 'sync_time': result.get('total_time', 0), 'sync_timestamp': datetime.now().isoformat()}
        except Exception as e:
            logger.error(f'Error running sync for {entity_type.value}: {str(e)}')
            sync_log.complete(status=SyncStatus.FAILED, records_processed=0, records_created=0, records_updated=0, records_failed=0, error_message=str(e))
            return {'success': False, 'message': f'Sync failed: {str(e)}', 'entity_type': entity_type.value, 'status': 'failed', 'error': str(e), 'sync_timestamp': datetime.now().isoformat()}
        finally:
            self._active_syncs.remove(entity_type)
    async def get_sync_status(self, entity_type: Optional[SyncEntityType]=None) -> Dict[str, Any]:
        result: Dict[str, Any] = {'is_initialized': self._initialized, 'active_syncs': [e.value for e in self._active_syncs]}
        last_syncs = {}
        for entity, time in self._last_sync_times.items():
            last_syncs[entity.value] = time.isoformat()
        result['last_sync_times'] = last_syncs
        if entity_type:
            entity_history = []
            for log in reversed(self._sync_history):
                if log.entity_type == entity_type:
                    entity_history.append({'status': log.status.value, 'records_processed': log.records_processed, 'records_created': log.records_created, 'records_updated': log.records_updated, 'records_failed': log.records_failed, 'started_at': log.started_at.isoformat(), 'completed_at': log.completed_at.isoformat() if log.completed_at else None, 'error_message': log.error_message})
            result['entity_history'] = entity_history
            result['current_status'] = 'running' if entity_type in self._active_syncs else 'idle'
        return result
    async def _schedule_sync_task(self, entity_type: SyncEntityType, delay_seconds: int) -> None:
        try:
            await asyncio.sleep(delay_seconds)
            await self.run_sync(entity_type)
        except asyncio.CancelledError:
            logger.info(f'Scheduled sync for {entity_type.value} was cancelled')
        except Exception as e:
            logger.error(f'Error in scheduled sync for {entity_type.value}: {str(e)}')
            await self.schedule_sync(entity_type, delay_seconds=300)
    async def _run_entity_sync(self, entity_type: SyncEntityType, db: AsyncSession) -> Dict[str, Any]:
        connector_config = AS400ConnectionConfig(**get_as400_connector_config())
        connector = AS400Connector(connector_config)
        if entity_type == SyncEntityType.PRODUCT:
            return await self._sync_products(connector, db)
        elif entity_type == SyncEntityType.MEASUREMENT:
            return await self._sync_measurements(connector, db)
        elif entity_type == SyncEntityType.STOCK:
            return await self._sync_inventory(connector, db)
        elif entity_type == SyncEntityType.PRICING:
            return await self._sync_pricing(connector, db)
        else:
            raise ValueError(f'Unsupported entity type: {entity_type.value}')
    async def _sync_products(self, connector: AS400Connector, db: AsyncSession) -> Dict[str, Any]:
        processor_config = AS400ProcessorConfig(field_mapping={'part_number': 'PRDNUM', 'application': 'PRDDESC', 'vintage': 'VINTAGE', 'late_model': 'LATEMDL', 'soft': 'SOFT', 'universal': 'UNIVRSL', 'is_active': 'ACTIVE'}, boolean_true_values=['1', 'Y', 'YES', 'TRUE', 'T'], boolean_false_values=['0', 'N', 'NO', 'FALSE', 'F'], required_fields=['part_number'], unique_key_field='part_number')
        processor = ProductAS400Processor(processor_config, ProductCreate)
        importer = ProductAS400Importer(db)
        pipeline = AS400Pipeline(connector=connector, processor=processor, importer=importer, chunk_size=as400_settings.AS400_BATCH_SIZE)
        return await pipeline.run('SELECT * FROM PRODUCTLIB.PRODUCTS')
    async def _sync_measurements(self, connector: AS400Connector, db: AsyncSession) -> Dict[str, Any]:
        product_id_map = await self._get_product_id_map(db)
        processor_config = AS400ProcessorConfig(field_mapping={'product_id': 'PRDNUM', 'length': 'LENGTH', 'width': 'WIDTH', 'height': 'HEIGHT', 'weight': 'WEIGHT', 'volume': 'VOLUME', 'dimensional_weight': 'DIMWT'}, required_fields=['product_id'], unique_key_field='product_id')
        from app.data_import.processors.as400_processor import AS400BaseProcessor
        class CustomMeasurementProcessor(AS400BaseProcessor[ProductMeasurementCreate]):
            def _process_record_custom(self, processed_record: Dict[str, Any], original_record: Dict[str, Any]) -> Dict[str, Any]:
                if 'product_id' in processed_record:
                    part_number = processed_record['product_id']
                    if part_number in product_id_map:
                        processed_record['product_id'] = product_id_map[part_number]
                    else:
                        raise ValueError(f'Product with part number {part_number} not found')
                return processed_record
        processor = CustomMeasurementProcessor(processor_config, ProductMeasurementCreate)
        importer = ProductMeasurementImporter(db)
        pipeline = AS400Pipeline(connector=connector, processor=processor, importer=importer, chunk_size=as400_settings.AS400_BATCH_SIZE)
        return await pipeline.run('SELECT * FROM PRODUCTLIB.MEASUREMENTS')
    async def _sync_inventory(self, connector: AS400Connector, db: AsyncSession) -> Dict[str, Any]:
        product_id_map = await self._get_product_id_map(db)
        warehouse_id_map = await self._get_warehouse_id_map(db)
        processor_config = AS400ProcessorConfig(field_mapping={'product_id': 'PRDNUM', 'warehouse_id': 'WRHSNUM', 'quantity': 'QUANTITY'}, required_fields=['product_id', 'warehouse_id', 'quantity'], unique_key_field='product_id')
        from app.data_import.processors.as400_processor import AS400BaseProcessor
        class CustomStockProcessor(AS400BaseProcessor[ProductStockSchema]):
            def _process_record_custom(self, processed_record: Dict[str, Any], original_record: Dict[str, Any]) -> Dict[str, Any]:
                if 'product_id' in processed_record:
                    part_number = processed_record['product_id']
                    if part_number in product_id_map:
                        processed_record['product_id'] = product_id_map[part_number]
                    else:
                        raise ValueError(f'Product with part number {part_number} not found')
                if 'warehouse_id' in processed_record:
                    warehouse_code = processed_record['warehouse_id']
                    if warehouse_code in warehouse_id_map:
                        processed_record['warehouse_id'] = warehouse_id_map[warehouse_code]
                    else:
                        raise ValueError(f'Warehouse with code {warehouse_code} not found')
                if 'quantity' in processed_record and processed_record['quantity'] < 0:
                    processed_record['quantity'] = 0
                return processed_record
        processor = CustomStockProcessor(processor_config, ProductStockSchema)
        importer = ProductStockImporter(db)
        pipeline = AS400Pipeline(connector=connector, processor=processor, importer=importer, chunk_size=as400_settings.AS400_BATCH_SIZE)
        return await pipeline.run('SELECT * FROM INVENTORYLIB.INVENTORY')
    async def _sync_pricing(self, connector: AS400Connector, db: AsyncSession) -> Dict[str, Any]:
        return {'success': True, 'message': 'Pricing sync not implemented yet', 'records_processed': 0, 'records_created': 0, 'records_updated': 0, 'records_with_errors': 0, 'total_time': 0}
    async def _get_product_id_map(self, db: AsyncSession) -> Dict[str, uuid.UUID]:
        query = select(Product.part_number, Product.id).where(Product.is_deleted == False)
        result = await db.execute(query)
        return {row[0]: row[1] for row in result}
    async def _get_warehouse_id_map(self, db: AsyncSession) -> Dict[str, uuid.UUID]:
        query = select(Warehouse.id, Warehouse.name).where(Warehouse.is_deleted == False)
        result = await db.execute(query)
        return {row[1]: row[0] for row in result}
    async def _log_sync_audit(self, db: AsyncSession, entity_type: SyncEntityType, result: Dict[str, Any]) -> None:
        from app.domains.audit.models import AuditLog
        audit_log = AuditLog(timestamp=datetime.now(), event_type=f'as400_sync_{entity_type.value}', level='info' if result.get('success', False) else 'error', details={'records_processed': result.get('records_processed', 0), 'records_created': result.get('records_created', 0), 'records_updated': result.get('records_updated', 0), 'records_with_errors': result.get('records_with_errors', 0), 'sync_time': result.get('total_time', 0), 'message': result.get('message', 'Sync completed')}, resource_type=entity_type.value)
        db.add(audit_log)
        await db.flush()
as400_sync_service = AS400SyncService.get_instance()