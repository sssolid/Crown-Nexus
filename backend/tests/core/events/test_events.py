from __future__ import annotations

"""
Tests for the event system.

This module contains unit tests for the event system, ensuring that
events are properly published and handled.
"""

import asyncio
import pytest
from typing import Dict, Any, List

from app.core.events import EventBackendType, publish_event, get_event_service
from app.core.events.domain_events import DomainEvent, UserData, TypedUserCreatedEvent


# Test events
TEST_EVENT = "test.event"
FILTERED_EVENT = "test.filtered_event"


# Global variables to track event handler calls
event_received = False
event_data: Dict[str, Any] = {}
received_events: List[Dict[str, Any]] = []


# Test event handlers
@get_event_service().event_handler(TEST_EVENT)
async def handle_test_event(event: Dict[str, Any]) -> None:
    """Test handler for basic events."""
    global event_received, event_data
    event_received = True
    event_data = event
    received_events.append(event)


@get_event_service().event_handler(
    FILTERED_EVENT, filter_func=lambda event: event["data"].get("value", 0) > 10
)
async def handle_filtered_event(event: Dict[str, Any]) -> None:
    """Test handler for filtered events."""
    global received_events
    received_events.append(event)


@pytest.fixture
async def event_system():
    """Initialize and teardown the event system for tests."""
    # Initialize with memory backend
    event_service = get_event_service()
    await event_service.initialize(EventBackendType.MEMORY)

    # Reset test tracking variables
    global event_received, event_data, received_events
    event_received = False
    event_data = {}
    received_events = []

    # Return the service for tests
    yield event_service

    # Shut down after tests
    await event_service.shutdown()


@pytest.mark.asyncio
async def test_publish_and_handle_event(event_system):
    """Test that events are properly published and handled."""
    # Publish a test event
    await publish_event(
        TEST_EVENT,
        payload={"message": "test", "value": 42},
        context={"request_id": "test-123"},
    )

    # Wait a moment for the event to be processed
    await asyncio.sleep(0.1)

    # Check if the event was received
    assert event_received is True
    assert "data" in event_data
    assert event_data["data"]["message"] == "test"
    assert event_data["data"]["value"] == 42
    assert event_data.get("request_id") == "test-123"


@pytest.mark.asyncio
async def test_filtered_events(event_system):
    """Test that event filtering works correctly."""
    # Clear any previous events
    received_events.clear()

    # Publish events that should be filtered
    await publish_event(
        FILTERED_EVENT, payload={"message": "below threshold", "value": 5}
    )

    # Publish events that should pass the filter
    await publish_event(
        FILTERED_EVENT, payload={"message": "above threshold", "value": 15}
    )

    # Wait for event processing
    await asyncio.sleep(0.1)

    # Check that only the filtered event was received
    assert len(received_events) == 1
    assert received_events[0]["data"]["message"] == "above threshold"
    assert received_events[0]["data"]["value"] == 15


@pytest.mark.asyncio
async def test_domain_event_class(event_system):
    """Test using the domain event classes."""
    # Create a typed event
    user_data = UserData(
        user_id="user-123", username="testuser", email="test@example.com"
    )

    event = TypedUserCreatedEvent.create(
        data=user_data, request_id="test-req-123", user_id="admin-user"
    )

    # Publish the event
    await publish_event(event.event_name, event.to_dict())

    # Create a handler for this event type
    received_typed_event = None

    @event_system.event_handler(TypedUserCreatedEvent.event_name)
    async def handle_typed_event(event_dict: Dict[str, Any]):
        nonlocal received_typed_event
        # Convert dict back to domain event
        received_typed_event = TypedUserCreatedEvent.from_dict(event_dict)

    # Wait for event processing
    await asyncio.sleep(0.1)

    # Check the received event
    assert received_typed_event is not None
    assert received_typed_event.data.user_id == "user-123"
    assert received_typed_event.data.username == "testuser"
    assert received_typed_event.data.email == "test@example.com"
    assert received_typed_event.request_id == "test-req-123"
    assert received_typed_event.user_id == "admin-user"


@pytest.mark.asyncio
async def test_event_error_handling(event_system):
    """Test that errors in event handlers don't crash the system."""
    # Define a handler that raises an exception
    error_event = "test.error_event"
    error_received = False

    @event_system.event_handler(error_event)
    async def handle_error_event(event: Dict[str, Any]):
        nonlocal error_received
        error_received = True
        raise ValueError("Test error in event handler")

    # Also define a second handler that should still run
    second_handler_called = False

    @event_system.event_handler(error_event)
    async def second_handler(event: Dict[str, Any]):
        nonlocal second_handler_called
        second_handler_called = True

    # Publish the event
    await publish_event(error_event, {"test": "data"})

    # Wait for event processing
    await asyncio.sleep(0.1)

    # Verify both handlers were called, and the error didn't prevent execution
    assert error_received is True
    assert second_handler_called is True
