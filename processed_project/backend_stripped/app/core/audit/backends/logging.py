from __future__ import annotations
'\nLogging backend for audit events.\n\nThis module provides a backend that logs audit events to the application logger.\n'
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from app.core.audit.base import AuditBackend, AuditContext, AuditEventType, AuditLogLevel, AuditOptions
from app.core.audit.utils import anonymize_data
from app.logging import get_logger
logger = get_logger('app.core.audit.backends.logging')
class LoggingAuditBackend(AuditBackend):
    __backend_name__ = 'logging'
    def __init__(self) -> None:
        self.logger = get_logger('app.audit')
    async def initialize(self) -> None:
        logger.info('Logging audit backend initialized')
    async def shutdown(self) -> None:
        logger.info('Logging audit backend shut down')
    async def log_event(self, event_type: AuditEventType, level: AuditLogLevel, context: AuditContext, details: Optional[Dict[str, Any]]=None, options: Optional[AuditOptions]=None) -> str:
        options = options or AuditOptions()
        event_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        log_entry = {'id': event_id, 'timestamp': timestamp, 'event_type': event_type, 'level': level, **context.model_dump(exclude_none=True)}
        if details:
            if options.anonymize_data:
                details = anonymize_data(details, options.sensitive_fields)
            log_entry['details'] = details
        user_id = context.user_id or 'system'
        ip_address = context.ip_address or 'internal'
        log_message = f'AUDIT: {event_type} by {user_id} from {ip_address}'
        if level == AuditLogLevel.INFO:
            self.logger.info(log_message, extra={'audit': log_entry})
        elif level == AuditLogLevel.WARNING:
            self.logger.warning(log_message, extra={'audit': log_entry})
        elif level == AuditLogLevel.ERROR:
            self.logger.error(log_message, extra={'audit': log_entry})
        elif level == AuditLogLevel.CRITICAL:
            self.logger.critical(log_message, extra={'audit': log_entry})
        return event_id
    async def health_check(self) -> Dict[str, Any]:
        return {'status': 'healthy', 'component': 'logging_backend', 'timestamp': datetime.now(timezone.utc).isoformat()}