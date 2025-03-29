from __future__ import annotations
'\nTests for the event system.\n\nThis module contains unit tests for the event system, ensuring that\nevents are properly published and handled.\n'
import asyncio
import pytest
from typing import Dict, Any, List
from app.core.events import EventBackendType, publish_event, get_event_service
from app.core.events.domain_events import DomainEvent, UserData, TypedUserCreatedEvent
TEST_EVENT = 'test.event'
FILTERED_EVENT = 'test.filtered_event'
event_received = False
event_data: Dict[str, Any] = {}
received_events: List[Dict[str, Any]] = []
@get_event_service().event_handler(TEST_EVENT)
async def handle_test_event(event: Dict[str, Any]) -> None:
    global event_received, event_data
    event_received = True
    event_data = event
    received_events.append(event)
@get_event_service().event_handler(FILTERED_EVENT, filter_func=lambda event: event['data'].get('value', 0) > 10)
async def handle_filtered_event(event: Dict[str, Any]) -> None:
    global received_events
    received_events.append(event)
@pytest.fixture
async def event_system():
    event_service = get_event_service()
    await event_service.initialize(EventBackendType.MEMORY)
    global event_received, event_data, received_events
    event_received = False
    event_data = {}
    received_events = []
    yield event_service
    await event_service.shutdown()
@pytest.mark.asyncio
async def test_publish_and_handle_event(event_system):
    await publish_event(TEST_EVENT, payload={'message': 'test', 'value': 42}, context={'request_id': 'test-123'})
    await asyncio.sleep(0.1)
    assert event_received is True
    assert 'data' in event_data
    assert event_data['data']['message'] == 'test'
    assert event_data['data']['value'] == 42
    assert event_data.get('request_id') == 'test-123'
@pytest.mark.asyncio
async def test_filtered_events(event_system):
    received_events.clear()
    await publish_event(FILTERED_EVENT, payload={'message': 'below threshold', 'value': 5})
    await publish_event(FILTERED_EVENT, payload={'message': 'above threshold', 'value': 15})
    await asyncio.sleep(0.1)
    assert len(received_events) == 1
    assert received_events[0]['data']['message'] == 'above threshold'
    assert received_events[0]['data']['value'] == 15
@pytest.mark.asyncio
async def test_domain_event_class(event_system):
    user_data = UserData(user_id='user-123', username='testuser', email='test@example.com')
    event = TypedUserCreatedEvent.create(data=user_data, request_id='test-req-123', user_id='admin-user')
    await publish_event(event.event_name, event.to_dict())
    received_typed_event = None
    @event_system.event_handler(TypedUserCreatedEvent.event_name)
    async def handle_typed_event(event_dict: Dict[str, Any]):
        nonlocal received_typed_event
        received_typed_event = TypedUserCreatedEvent.from_dict(event_dict)
    await asyncio.sleep(0.1)
    assert received_typed_event is not None
    assert received_typed_event.data.user_id == 'user-123'
    assert received_typed_event.data.username == 'testuser'
    assert received_typed_event.data.email == 'test@example.com'
    assert received_typed_event.request_id == 'test-req-123'
    assert received_typed_event.user_id == 'admin-user'
@pytest.mark.asyncio
async def test_event_error_handling(event_system):
    error_event = 'test.error_event'
    error_received = False
    @event_system.event_handler(error_event)
    async def handle_error_event(event: Dict[str, Any]):
        nonlocal error_received
        error_received = True
        raise ValueError('Test error in event handler')
    second_handler_called = False
    @event_system.event_handler(error_event)
    async def second_handler(event: Dict[str, Any]):
        nonlocal second_handler_called
        second_handler_called = True
    await publish_event(error_event, {'test': 'data'})
    await asyncio.sleep(0.1)
    assert error_received is True
    assert second_handler_called is True