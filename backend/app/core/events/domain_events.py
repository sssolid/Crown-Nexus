from __future__ import annotations

"""
Domain Events Definition System.

This module provides base classes and utilities for defining typed domain events
throughout the application. Using these base classes helps ensure type safety
and proper documentation of the domain events.
"""

import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, ClassVar, Dict, Generic, Optional, Type, TypeVar

T = TypeVar("T")


@dataclass
class DomainEvent(Generic[T]):
    """
    Base class for all domain events.

    This class provides common functionality for domain events and
    enforces a consistent structure across all event types.
    """

    # Class variable to store the event name
    event_name: ClassVar[str]

    # Metadata fields that all events should have
    timestamp: float = field(default_factory=time.time)
    version: str = field(default="1.0")

    # Optional context information
    request_id: Optional[str] = field(default=None)
    user_id: Optional[str] = field(default=None)
    correlation_id: Optional[str] = field(default=None)

    # The actual event data (provided by subclasses)
    data: T = field(default_factory=dict)  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the event to a dictionary for serialization.

        Returns:
            Dict containing all event data
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DomainEvent:
        """
        Create an event instance from a dictionary.

        Args:
            data: Dictionary containing event data

        Returns:
            DomainEvent: Instance of the event
        """
        # Extract the main data payload
        event_data = data.pop("data", {})

        # Create the event instance
        return cls(data=event_data, **data)

    @classmethod
    def create(cls, data: T, **context) -> DomainEvent[T]:
        """
        Create a new event with the given data and context.

        Args:
            data: The main event data
            **context: Additional context information

        Returns:
            DomainEvent: The created event instance
        """
        return cls(data=data, **context)


# Example event types that can be used as a reference


@dataclass
class UserCreatedEvent(DomainEvent[Dict[str, Any]]):
    """Event fired when a new user is created."""

    event_name: ClassVar[str] = "user.created"


@dataclass
class OrderCompletedEvent(DomainEvent[Dict[str, Any]]):
    """Event fired when an order is completed."""

    event_name: ClassVar[str] = "order.completed"


@dataclass
class ProductUpdatedEvent(DomainEvent[Dict[str, Any]]):
    """Event fired when a product is updated."""

    event_name: ClassVar[str] = "product.updated"


# You can create more specific event types with typed data


@dataclass
class UserData:
    """Data structure for user-related events."""

    user_id: str
    username: str
    email: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TypedUserCreatedEvent(DomainEvent[UserData]):
    """Event fired when a new user is created, with strongly typed data."""

    event_name: ClassVar[str] = "user.created.typed"
