from __future__ import annotations
'\nDomain Events Definition System.\n\nThis module provides base classes and utilities for defining typed domain events\nthroughout the application. Using these base classes helps ensure type safety\nand proper documentation of the domain events.\n'
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, ClassVar, Dict, Generic, Optional, Type, TypeVar
T = TypeVar('T')
@dataclass
class DomainEvent(Generic[T]):
    event_name: ClassVar[str]
    timestamp: float = field(default_factory=time.time)
    version: str = field(default='1.0')
    request_id: Optional[str] = field(default=None)
    user_id: Optional[str] = field(default=None)
    correlation_id: Optional[str] = field(default=None)
    data: T = field(default_factory=dict)
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainEvent:
        event_data = data.pop('data', {})
        return cls(data=event_data, **data)
    @classmethod
    def create(cls, data: T, **context) -> DomainEvent[T]:
        return cls(data=data, **context)
@dataclass
class UserCreatedEvent(DomainEvent[Dict[str, Any]]):
    event_name: ClassVar[str] = 'user.created'
@dataclass
class OrderCompletedEvent(DomainEvent[Dict[str, Any]]):
    event_name: ClassVar[str] = 'order.completed'
@dataclass
class ProductUpdatedEvent(DomainEvent[Dict[str, Any]]):
    event_name: ClassVar[str] = 'product.updated'
@dataclass
class UserData:
    user_id: str
    username: str
    email: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
@dataclass
class TypedUserCreatedEvent(DomainEvent[UserData]):
    event_name: ClassVar[str] = 'user.created.typed'