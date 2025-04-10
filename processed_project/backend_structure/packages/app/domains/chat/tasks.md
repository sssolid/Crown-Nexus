# Module: app.domains.chat.tasks

**Path:** `app/domains/chat/tasks.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
from typing import Any, Dict, List
from celery import Celery
from app.core.config import settings
from app.logging import get_logger
```

## Global Variables
```python
logger = logger = get_logger("app.tasks.chat_tasks")
celery_app = celery_app = Celery(
    "worker",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/2",
)
```

## Functions

| Function | Description |
| --- | --- |
| `analyze_chat_activity` |  |
| `moderate_message_content` |  |
| `process_message_notifications` |  |
| `update_user_presence` |  |

### `analyze_chat_activity`
```python
@celery_app.task(bind=True, name='analyze_chat_activity')
def analyze_chat_activity(self, room_id, time_period) -> Dict[(str, Any)]:
```

### `moderate_message_content`
```python
@celery_app.task(bind=True, name='moderate_message_content')
def moderate_message_content(self, message_id, content, sender_id, room_id) -> Dict[(str, Any)]:
```

### `process_message_notifications`
```python
@celery_app.task(bind=True, name='process_message_notifications')
def process_message_notifications(self, message_id, room_id, sender_id, recipients, message_preview) -> Dict[(str, Any)]:
```

### `update_user_presence`
```python
@celery_app.task(bind=True, name='update_user_presence')
def update_user_presence(self) -> Dict[(str, Any)]:
```
