from __future__ import annotations
'Audit logger implementations.\n\nThis module provides different implementations of the AuditLogger protocol\nfor logging audit events to various destinations.\n'
import json
import uuid
import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
from app.domains.audit.service.base import AuditContext, AuditEventType, AuditLogLevel, AuditLogger, AuditOptions
logger = get_logger('app.domains.audit.service.loggers')
class BaseAuditLogger:
    def __init__(self) -> None:
        self.logger = logger
        self.sensitive_fields: List[str] = ['password', 'token', 'secret', 'credit_card', 'ssn', 'social_security', 'api_key']
        self.anonymize_events: List[AuditEventType] = [AuditEventType.GDPR_DATA_EXPORT, AuditEventType.GDPR_DATA_DELETED]
        self.event_level_mapping: Dict[AuditEventType, AuditLogLevel] = {AuditEventType.ACCESS_DENIED: AuditLogLevel.WARNING, AuditEventType.LOGIN_FAILED: AuditLogLevel.WARNING, AuditEventType.USER_DELETED: AuditLogLevel.WARNING, AuditEventType.API_KEY_REVOKED: AuditLogLevel.WARNING, AuditEventType.PAYMENT_REFUNDED: AuditLogLevel.WARNING, AuditEventType.DATA_DELETED: AuditLogLevel.WARNING, AuditEventType.CHAT_MESSAGE_DELETED: AuditLogLevel.INFO, AuditEventType.GDPR_DATA_DELETED: AuditLogLevel.WARNING, AuditEventType.SYSTEM_STOPPED: AuditLogLevel.WARNING, AuditEventType.MAINTENANCE_MODE_ENABLED: AuditLogLevel.WARNING}
    def _get_log_level(self, event_type: AuditEventType, level: Optional[AuditLogLevel]=None) -> AuditLogLevel:
        if level is not None:
            return level
        return self.event_level_mapping.get(event_type, AuditLogLevel.INFO)
    def _anonymize_data(self, data: Dict[str, Any], sensitive_fields: List[str]) -> Dict[str, Any]:
        if not data:
            return {}
        anonymized = {}
        for key, value in data.items():
            is_sensitive = any((sensitive in key.lower() for sensitive in sensitive_fields))
            if is_sensitive:
                if isinstance(value, str):
                    if len(value) <= 4:
                        anonymized[key] = '****'
                    else:
                        anonymized[key] = value[0] + '*' * (len(value) - 2) + value[-1]
                else:
                    anonymized[key] = '[REDACTED]'
            elif isinstance(value, dict):
                anonymized[key] = self._anonymize_data(value, sensitive_fields)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                anonymized[key] = [self._anonymize_data(item, sensitive_fields) if isinstance(item, dict) else item for item in value]
            else:
                anonymized[key] = value
        return anonymized
    def _prepare_log_entry(self, event_id: str, event_type: AuditEventType, level: AuditLogLevel, user_id: Optional[str], ip_address: Optional[str], resource_id: Optional[str], resource_type: Optional[str], details: Optional[Dict[str, Any]], context: Optional[AuditContext], options: Optional[AuditOptions]) -> Dict[str, Any]:
        timestamp = datetime.datetime.now(datetime.UTC).isoformat() + 'Z'
        ctx = context or AuditContext()
        ctx_user_id = ctx.user_id or user_id
        ctx_ip = ctx.ip_address or ip_address
        ctx_resource_id = ctx.resource_id or resource_id
        ctx_resource_type = ctx.resource_type or resource_type
        audit_details = details or {}
        opts = options or AuditOptions()
        should_anonymize = opts.anonymize_data or event_type in self.anonymize_events
        sensitive_fields = opts.sensitive_fields or self.sensitive_fields
        if should_anonymize and audit_details:
            audit_details = self._anonymize_data(audit_details, sensitive_fields)
        log_entry: Dict[str, Any] = {'id': event_id, 'timestamp': timestamp, 'event_type': event_type, 'level': level, 'user_id': ctx_user_id, 'ip_address': ctx_ip, 'resource_id': ctx_resource_id, 'resource_type': ctx_resource_type, 'details': audit_details}
        if context:
            for key, value in context.model_dump(exclude_none=True).items():
                if key not in log_entry and key not in ['user_id', 'ip_address', 'resource_id', 'resource_type']:
                    log_entry[key] = value
        return log_entry
class LoggingAuditLogger(BaseAuditLogger, AuditLogger):
    async def log_event(self, event_type: AuditEventType, user_id: Optional[str]=None, ip_address: Optional[str]=None, resource_id: Optional[str]=None, resource_type: Optional[str]=None, details: Optional[Dict[str, Any]]=None, context: Optional[AuditContext]=None, level: Optional[AuditLogLevel]=None, options: Optional[AuditOptions]=None) -> str:
        event_id = str(uuid.uuid4())
        log_level = self._get_log_level(event_type, level)
        log_entry = self._prepare_log_entry(event_id, event_type, log_level, user_id, ip_address, resource_id, resource_type, details, context, options)
        log_message = f"AUDIT: {event_type} by user {log_entry['user_id']} from {log_entry['ip_address']}"
        if log_level == AuditLogLevel.INFO:
            self.logger.info(log_message, extra=log_entry)
        elif log_level == AuditLogLevel.WARNING:
            self.logger.warning(log_message, extra=log_entry)
        elif log_level == AuditLogLevel.ERROR:
            self.logger.error(log_message, extra=log_entry)
        elif log_level == AuditLogLevel.CRITICAL:
            self.logger.critical(log_message, extra=log_entry)
        return event_id
class FileAuditLogger(BaseAuditLogger, AuditLogger):
    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.file_path = file_path
        import os
        from pathlib import Path
        log_dir = Path(file_path).parent
        os.makedirs(log_dir, exist_ok=True)
    async def log_event(self, event_type: AuditEventType, user_id: Optional[str]=None, ip_address: Optional[str]=None, resource_id: Optional[str]=None, resource_type: Optional[str]=None, details: Optional[Dict[str, Any]]=None, context: Optional[AuditContext]=None, level: Optional[AuditLogLevel]=None, options: Optional[AuditOptions]=None) -> str:
        event_id = str(uuid.uuid4())
        log_level = self._get_log_level(event_type, level)
        log_entry = self._prepare_log_entry(event_id, event_type, log_level, user_id, ip_address, resource_id, resource_type, details, context, options)
        try:
            log_line = json.dumps(log_entry)
            with open(self.file_path, 'a') as f:
                f.write(log_line + '\n')
            self.logger.debug(f'Audit log saved to file: {event_id}')
        except Exception as e:
            self.logger.error(f'Failed to write audit log to file: {str(e)}')
        return event_id
class DatabaseAuditLogger(BaseAuditLogger, AuditLogger):
    def __init__(self, db: Optional[AsyncSession]=None) -> None:
        super().__init__()
        self.db = db
    async def log_event(self, event_type: AuditEventType, user_id: Optional[str]=None, ip_address: Optional[str]=None, resource_id: Optional[str]=None, resource_type: Optional[str]=None, details: Optional[Dict[str, Any]]=None, context: Optional[AuditContext]=None, level: Optional[AuditLogLevel]=None, options: Optional[AuditOptions]=None) -> str:
        if not self.db:
            self.logger.warning('No database session provided for database audit logger')
            return str(uuid.uuid4())
        event_id = str(uuid.uuid4())
        log_level = self._get_log_level(event_type, level)
        log_entry = self._prepare_log_entry(event_id, event_type, log_level, user_id, ip_address, resource_id, resource_type, details, context, options)
        try:
            from app.domains.audit.models import AuditLog
            audit_log = AuditLog(id=uuid.UUID(log_entry['id']), timestamp=datetime.fromisoformat(log_entry['timestamp'].rstrip('Z')), event_type=log_entry['event_type'], level=log_entry['level'], user_id=uuid.UUID(log_entry['user_id']) if log_entry.get('user_id') else None, ip_address=log_entry.get('ip_address'), resource_id=uuid.UUID(log_entry['resource_id']) if log_entry.get('resource_id') else None, resource_type=log_entry.get('resource_type'), details=log_entry.get('details', {}), request_id=log_entry.get('request_id'), user_agent=log_entry.get('user_agent'), session_id=log_entry.get('session_id'), company_id=uuid.UUID(log_entry['company_id']) if log_entry.get('company_id') else None)
            self.db.add(audit_log)
            await self.db.commit()
            self.logger.debug(f'Audit log saved to database: {event_id}')
        except Exception as e:
            self.logger.error(f'Failed to write audit log to database: {str(e)}')
            await self.db.rollback()
        return event_id