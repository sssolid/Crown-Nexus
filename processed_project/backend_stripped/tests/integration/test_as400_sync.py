from __future__ import annotations
'\nIntegration tests for AS400 synchronization.\n\nThis module tests the integration between the application and AS400 database,\nverifying the data synchronization logic functions correctly.\n'
import os
from typing import Generator
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config.as400 import AS400Settings, as400_settings
from app.data_import.connectors.as400_connector import AS400Connector
from app.data_import.importers.as400_importers import ProductAS400Importer
from app.data_import.processors.as400_processor import AS400ProcessorConfig, ProductAS400Processor
from app.data_import.pipeline.as400_pipeline import AS400Pipeline
from app.db.session import async_session_maker
from app.domains.sync_history.models import SyncEntityType, SyncSource, SyncStatus
from app.domains.sync_history.repository import SyncHistoryRepository
from app.domains.products.schemas import ProductCreate
from app.services.as400_sync_service import as400_sync_service, SyncEntityType
pytestmark = pytest.mark.skipif(not os.environ.get('AS400_DSN') or not os.environ.get('AS400_USERNAME'), reason='AS400 credentials not found in environment')
@pytest_asyncio.fixture
async def db_session() -> Generator[AsyncSession, None, None]:
    async with async_session_maker() as session:
        yield session
        await session.rollback()
@pytest_asyncio.fixture
async def as400_connector() -> Generator[AS400Connector, None, None]:
    config = AS400Settings(dsn=os.environ.get('AS400_DSN', ''), username=os.environ.get('AS400_USERNAME', ''), password=os.environ.get('AS400_PASSWORD', ''), database=os.environ.get('AS400_DATABASE', ''), ssl=False, connection_timeout=10, query_timeout=30)
    connector = AS400Connector(config)
    yield connector
    try:
        await connector.close()
    except Exception:
        pass
@pytest_asyncio.fixture
async def sync_history_repo(db_session: AsyncSession) -> SyncHistoryRepository:
    return SyncHistoryRepository(db_session)
@pytest.mark.asyncio
async def test_as400_connection(as400_connector: AS400Connector) -> None:
    await as400_connector.connect()
    assert as400_connector.connection is not None
    await as400_connector.close()
@pytest.mark.asyncio
async def test_as400_data_extraction(as400_connector: AS400Connector) -> None:
    await as400_connector.connect()
    results = await as400_connector.extract('SELECT * FROM QIWS.QCUSTCDT FETCH FIRST 5 ROWS ONLY')
    assert isinstance(results, list)
    assert len(results) <= 5
    await as400_connector.close()
@pytest.mark.asyncio
async def test_product_sync_pipeline(as400_connector: AS400Connector, db_session: AsyncSession) -> None:
    if 'PRODUCTLIB.PRODUCTS' not in os.environ.get('AS400_ALLOWED_TABLES', ''):
        pytest.skip('No access to PRODUCTLIB.PRODUCTS table')
    processor_config = AS400ProcessorConfig(field_mapping={'part_number': 'PRDNUM', 'application': 'PRDDESC', 'vintage': 'VINTAGE', 'late_model': 'LATEMDL', 'soft': 'SOFT', 'universal': 'UNIVRSL', 'is_active': 'ACTIVE'}, boolean_true_values=['1', 'Y', 'YES', 'TRUE', 'T'], boolean_false_values=['0', 'N', 'NO', 'FALSE', 'F'], required_fields=['part_number'], unique_key_field='part_number')
    processor = ProductAS400Processor(processor_config, ProductCreate)
    importer = ProductAS400Importer(db_session)
    pipeline = AS400Pipeline(connector=as400_connector, processor=processor, importer=importer, dry_run=True, chunk_size=10)
    result = await pipeline.run('SELECT * FROM PRODUCTLIB.PRODUCTS FETCH FIRST 5 ROWS ONLY')
    assert result['success'] is True
    assert result['records_processed'] >= 0
    assert 'dry_run' in result and result['dry_run'] is True
@pytest.mark.asyncio
async def test_sync_history_tracking(db_session: AsyncSession, sync_history_repo: SyncHistoryRepository) -> None:
    sync = await sync_history_repo.create_sync(entity_type=SyncEntityType.PRODUCT, source=SyncSource.AS400)
    assert sync.id is not None
    assert sync.entity_type == SyncEntityType.PRODUCT.value
    assert sync.status == SyncStatus.PENDING.value
    updated_sync = await sync_history_repo.update_sync_status(sync_id=sync.id, status=SyncStatus.RUNNING, records_processed=0)
    assert updated_sync.status == SyncStatus.RUNNING.value
    event = await sync_history_repo.add_sync_event(sync_id=sync.id, event_type='test', message='Test event', details={'test': True})
    assert event.sync_id == sync.id
    assert event.event_type == 'test'
    completed_sync = await sync_history_repo.update_sync_status(sync_id=sync.id, status=SyncStatus.COMPLETED, records_processed=100, records_created=50, records_updated=50, records_failed=0)
    assert completed_sync.status == SyncStatus.COMPLETED.value
    assert completed_sync.records_processed == 100
    assert completed_sync.records_created == 50
    assert completed_sync.records_updated == 50
    assert completed_sync.sync_duration is not None
    events = await sync_history_repo.get_sync_events(sync.id)
    assert len(events) >= 1
    await db_session.rollback()
@pytest.mark.asyncio
async def test_as400_sync_service_initialization() -> None:
    await as400_sync_service.initialize()
    status = await as400_sync_service.get_sync_status()
    assert status.get('is_initialized', False) is True
    await as400_sync_service.shutdown()