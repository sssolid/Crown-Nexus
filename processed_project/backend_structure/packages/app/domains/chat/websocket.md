# Module: app.domains.chat.websocket

**Path:** `app/domains/chat/websocket.py`

[Back to Project Index](../../../../index.md)

## Imports
```python
from __future__ import annotations
import datetime
import json
import uuid
from typing import cast
from app.chat.schemas import ChatMessageSchema, CommandType, MessageType, WebSocketCommand, WebSocketResponse
from app.core.service_registry import get_service
from app.domains.audit.service_service import AuditEventType, AuditLogLevel, AuditService
from app.services.metrics_service import MetricsService
from app.services.validation_service import ValidationService
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user_ws, get_db
from app.core.exceptions import BusinessLogicException, ErrorCode, PermissionDeniedException, ValidationException
from app.logging import get_logger
from app.core.security import sanitize_input, moderate_content
from app.domains.chat.connection import manager, redis_manager
from app.domains.chat.service import ChatService
from app.domains.users.models import User
from app.utils.redis_manager import rate_limit_check
```

## Global Variables
```python
logger = logger = get_logger("app.chat.websocket")
router = router = APIRouter()
```

## Functions

| Function | Description |
| --- | --- |
| `get_audit_service` |  |
| `get_metrics_service` |  |
| `get_validation_service` |  |
| `process_command` |  |
| `websocket_endpoint` |  |

### `get_audit_service`
```python
async def get_audit_service() -> AuditService:
```

### `get_metrics_service`
```python
async def get_metrics_service() -> MetricsService:
```

### `get_validation_service`
```python
async def get_validation_service() -> ValidationService:
```

### `process_command`
```python
async def process_command(command, websocket, connection_id, user, chat_service, audit_service) -> None:
```

### `websocket_endpoint`
```python
@router.websocket('/ws/chat')
async def websocket_endpoint(websocket, db, current_user):
```
