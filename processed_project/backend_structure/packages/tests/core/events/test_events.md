# Module: tests.core.events.test_events

**Path:** `tests/core/events/test_events.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import pytest
from typing import Dict, Any, List
from app.core.events import EventBackendType, publish_event, get_event_service
from app.core.events.domain_events import DomainEvent, UserData, TypedUserCreatedEvent
```

## Global Variables
```python
TEST_EVENT = 'test.event'
FILTERED_EVENT = 'test.filtered_event'
event_received = False
```

## Functions

| Function | Description |
| --- | --- |
| `event_system` |  |
| `handle_filtered_event` |  |
| `handle_test_event` |  |
| `test_domain_event_class` |  |
| `test_event_error_handling` |  |
| `test_filtered_events` |  |
| `test_publish_and_handle_event` |  |

### `event_system`
```python
@pytest.fixture
async def event_system():
```

### `handle_filtered_event`
```python
@get_event_service().event_handler(FILTERED_EVENT, filter_func=Lambda)
async def handle_filtered_event(event) -> None:
```

### `handle_test_event`
```python
@get_event_service().event_handler(TEST_EVENT)
async def handle_test_event(event) -> None:
```

### `test_domain_event_class`
```python
@pytest.mark.asyncio
async def test_domain_event_class(event_system):
```

### `test_event_error_handling`
```python
@pytest.mark.asyncio
async def test_event_error_handling(event_system):
```

### `test_filtered_events`
```python
@pytest.mark.asyncio
async def test_filtered_events(event_system):
```

### `test_publish_and_handle_event`
```python
@pytest.mark.asyncio
async def test_publish_and_handle_event(event_system):
```
