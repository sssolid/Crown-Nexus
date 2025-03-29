# Module: app.domains.chat.connection

**Path:** `app/domains/chat/connection.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import asyncio
import json
from typing import Dict, Optional, Set
from app.domains.chat.schemas import WebSocketCommand
from fastapi import WebSocket
from app.logging import get_logger
from app.utils.redis_manager import get_redis_pool
```

## Global Variables
```python
logger = logger = get_logger("app.chat.connection")
manager = manager = ConnectionManager()
redis_manager = redis_manager = RedisConnectionManager(manager)
```

## Classes

| Class | Description |
| --- | --- |
| `ConnectionManager` |  |
| `RedisConnectionManager` |  |

### Class: `ConnectionManager`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `broadcast_to_room` `async` |  |
| `broadcast_to_user` `async` |  |
| `connect` `async` |  |
| `disconnect` |  |
| `get_connection_count` |  |
| `get_room_connection_count` |  |
| `get_user_connection_count` |  |
| `join_room` |  |
| `leave_room` |  |
| `send_personal_message` `async` |  |

##### `__init__`
```python
def __init__(self) -> None:
```

##### `broadcast_to_room`
```python
async def broadcast_to_room(self, message, room_id, exclude) -> None:
```

##### `broadcast_to_user`
```python
async def broadcast_to_user(self, message, user_id) -> None:
```

##### `connect`
```python
async def connect(self, websocket, connection_id, user_id) -> None:
```

##### `disconnect`
```python
def disconnect(self, connection_id) -> None:
```

##### `get_connection_count`
```python
def get_connection_count(self) -> int:
```

##### `get_room_connection_count`
```python
def get_room_connection_count(self, room_id) -> int:
```

##### `get_user_connection_count`
```python
def get_user_connection_count(self, user_id) -> int:
```

##### `join_room`
```python
def join_room(self, connection_id, room_id) -> None:
```

##### `leave_room`
```python
def leave_room(self, connection_id, room_id) -> None:
```

##### `send_personal_message`
```python
async def send_personal_message(self, message, connection_id) -> None:
```

### Class: `RedisConnectionManager`

#### Methods

| Method | Description |
| --- | --- |
| `__init__` |  |
| `broadcast_to_room` `async` |  |
| `broadcast_to_user` `async` |  |
| `start_pubsub_listener` `async` |  |

##### `__init__`
```python
def __init__(self, local_manager) -> None:
```

##### `broadcast_to_room`
```python
async def broadcast_to_room(self, message, room_id, exclude) -> None:
```

##### `broadcast_to_user`
```python
async def broadcast_to_user(self, message, user_id) -> None:
```

##### `start_pubsub_listener`
```python
async def start_pubsub_listener(self) -> None:
```
