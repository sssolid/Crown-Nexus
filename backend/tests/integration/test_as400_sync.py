from __future__ import annotations

"""
Integration tests for AS400 synchronization.

This module tests the integration between the application and AS400 database,
verifying the data synchronization logic functions correctly.
"""

import os
import uuid
from datetime import datetime
from typing import Any, Dict, Generator, List

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.as400 import AS400Settings, as400_settings
from app.data_import.connectors.as400_connector import AS400Connector
from app.data_import.importers.as400_importers import ProductAS400Importer
from app.data_import.processors.as400_processor import (
    AS400ProcessorConfig,
    ProductAS400Processor,
)
from app.data_import.pipeline.as400_pipeline import AS400Pipeline
from app.db.session import async_session_maker
from app.models.product import Product
from app.models.sync_history import SyncHistory, SyncEntityType, SyncSource, SyncStatus
from app.repositories.sync_history_repository import SyncHistoryRepository
from app.schemas.product import ProductCreate
from app.services.as400_sync_service import as400_sync_service, SyncEntityType


# Skip tests if AS400 environment variables are not set
pytestmark = pytest.mark.skipif(
    not os.environ.get("AS400_DSN") or not os.environ.get("AS400_USERNAME"),
    reason="AS400 credentials not found in environment",
)


@pytest_asyncio.fixture
async def db_session() -> Generator[AsyncSession, None, None]:
    """Provide a database session for tests."""
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def as400_connector() -> Generator[AS400Connector, None, None]:
    """Provide an AS400 connector for tests."""
    # Use test-specific connection config
    config = AS400Settings(
        dsn=os.environ.get("AS400_DSN", ""),
        username=os.environ.get("AS400_USERNAME", ""),
        password=os.environ.get("AS400_PASSWORD", ""),
        database=os.environ.get("AS400_DATABASE", ""),
        ssl=False,  # Disable SSL for testing
        connection_timeout=10,
        query_timeout=30,
    )

    connector = AS400Connector(config)
    yield connector

    # Clean up
    try:
        await connector.close()
    except Exception:
        pass


@pytest_asyncio.fixture
async def sync_history_repo(db_session: AsyncSession) -> SyncHistoryRepository:
    """Provide a sync history repository for tests."""
    return SyncHistoryRepository(db_session)


@pytest.mark.asyncio
async def test_as400_connection(as400_connector: AS400Connector) -> None:
    """Test that we can connect to the AS400 database."""
    await as400_connector.connect()
    assert as400_connector.connection is not None
    await as400_connector.close()


@pytest.mark.asyncio
async def test_as400_data_extraction(as400_connector: AS400Connector) -> None:
    """Test extracting data from AS400."""
    # Connect to AS400
    await as400_connector.connect()

    # Try to fetch some test data
    # Adjust the query to match your test environment
    results = await as400_connector.extract(
        "SELECT * FROM QIWS.QCUSTCDT FETCH FIRST 5 ROWS ONLY"
    )

    # Verify data was fetched
    assert isinstance(results, list)
    assert len(results) <= 5

    # Clean up
    await as400_connector.close()


@pytest.mark.asyncio
async def test_product_sync_pipeline(
    as400_connector: AS400Connector, db_session: AsyncSession
) -> None:
    """Test the complete product synchronization pipeline."""
    # Skip if no product table access
    if "PRODUCTLIB.PRODUCTS" not in os.environ.get("AS400_ALLOWED_TABLES", ""):
        pytest.skip("No access to PRODUCTLIB.PRODUCTS table")

    # Set up processor
    processor_config = AS400ProcessorConfig(
        field_mapping={
            "part_number": "PRDNUM",
            "application": "PRDDESC",
            "vintage": "VINTAGE",
            "late_model": "LATEMDL",
            "soft": "SOFT",
            "universal": "UNIVRSL",
            "is_active": "ACTIVE",
        },
        boolean_true_values=["1", "Y", "YES", "TRUE", "T"],
        boolean_false_values=["0", "N", "NO", "FALSE", "F"],
        required_fields=["part_number"],
        unique_key_field="part_number",
    )

    # Set up pipeline
    processor = ProductAS400Processor(processor_config, ProductCreate)
    importer = ProductAS400Importer(db_session)
    pipeline = AS400Pipeline(
        connector=as400_connector,
        processor=processor,
        importer=importer,
        dry_run=True,  # Use dry run for testing
        chunk_size=10,
    )

    # Run sync
    result = await pipeline.run(
        "SELECT * FROM PRODUCTLIB.PRODUCTS FETCH FIRST 5 ROWS ONLY"
    )

    # Verify results
    assert result["success"] is True
    assert result["records_processed"] >= 0
    assert "dry_run" in result and result["dry_run"] is True


@pytest.mark.asyncio
async def test_sync_history_tracking(
    db_session: AsyncSession, sync_history_repo: SyncHistoryRepository
) -> None:
    """Test sync history tracking functionality."""
    # Create a test sync record
    sync = await sync_history_repo.create_sync(
        entity_type=SyncEntityType.PRODUCT, source=SyncSource.AS400
    )

    # Verify record was created
    assert sync.id is not None
    assert sync.entity_type == SyncEntityType.PRODUCT.value
    assert sync.status == SyncStatus.PENDING.value

    # Update status
    updated_sync = await sync_history_repo.update_sync_status(
        sync_id=sync.id, status=SyncStatus.RUNNING, records_processed=0
    )

    # Verify update
    assert updated_sync.status == SyncStatus.RUNNING.value

    # Add an event
    event = await sync_history_repo.add_sync_event(
        sync_id=sync.id, event_type="test", message="Test event", details={"test": True}
    )

    # Verify event
    assert event.sync_id == sync.id
    assert event.event_type == "test"

    # Mark as complete
    completed_sync = await sync_history_repo.update_sync_status(
        sync_id=sync.id,
        status=SyncStatus.COMPLETED,
        records_processed=100,
        records_created=50,
        records_updated=50,
        records_failed=0,
    )

    # Verify completion
    assert completed_sync.status == SyncStatus.COMPLETED.value
    assert completed_sync.records_processed == 100
    assert completed_sync.records_created == 50
    assert completed_sync.records_updated == 50
    assert completed_sync.sync_duration is not None

    # Get events
    events = await sync_history_repo.get_sync_events(sync.id)
    assert len(events) >= 1

    # Roll back to avoid affecting other tests
    await db_session.rollback()


@pytest.mark.asyncio
async def test_as400_sync_service_initialization() -> None:
    """Test initialization of the AS400 sync service."""
    # Initialize service
    await as400_sync_service.initialize()

    # Get service status
    status = await as400_sync_service.get_sync_status()

    # Verify service is initialized
    assert status.get("is_initialized", False) is True

    # Shutdown service
    await as400_sync_service.shutdown()
