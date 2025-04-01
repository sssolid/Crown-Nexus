# Developer Guide: Core Systems Architecture

## Table of Contents

1. [Introduction](#1-introduction)
2. [Core System Structure](#2-core-system-structure)
3. [File Purposes and Contents](#3-file-purposes-and-contents)
    - [3.1 `__init__.py`](#31-__init__py)
    - [3.2 `base.py`](#32-basepy)
    - [3.3 `exceptions.py`](#33-exceptionspy)
    - [3.4 `service.py`](#34-servicepy)
    - [3.5 `manager.py`](#35-managerpy)
    - [3.6 `utils.py`](#36-utilspy)
    - [3.7 `backends/init.py`](#37-backends__init__py)
    - [3.8 `backends/{backend_name}.py`](#38-backendsbackend_namepy)
    - [3.9 `models.py`](#39-modelspy)
    - [3.10 `schemas.py`](#310-schemaspy)
4. [Lifecyle Managements](#4-lifecycle-management)
    - [4.1 `Initialization`](#41-initialization)
    - [4.2 `Shutdown`](#42-shutdown)
    - [4.3 `Context Manager`](#43-context-manager)
5. [Service Configuration](#5-service-configuration)
6. [Health Checking](#6-health-checking)
7. [Error Handling](#7-error-handling)
8. [Adding a New Core System](#8-adding-a-new-core-system)
9. [Accessing Core Services](#9-accessing-core-services)
10. [Testing Core Systems](#10-testing-core-systems)
    - [10.1 `Unit Testing`](#101-unit-testing)
    - [10.2 `Integration Testing`](#102-integration-testing)
    - [10.3 `Example Test`](#103-example-test)
11. [Best Practices](#11-best-practices)
    - [11.1 `Design Principles`](#111-design-principles)
    - [11.2 `Implementation Guidelines`](#112-implementation-guidelines)
    - [11.3 `Performance Considerations`](#113-performance-considerations)
12. [Application Integration](#12-application-integration)
    - [12.1 `Service Registration`](#121-service-registration)
    - [12.2 `FastAPI Dependency`](#122-fastapi-dependency)
    - [12.3 `API Route Usage`](#123-api-route-usage)
13. [Example Core Systems](#13-example-core-systems)

## 1. Introduction

This guide outlines the standardized architecture for all core systems in our application. Following this architecture ensures consistency, maintainability, and proper integration with the wider application framework.

Each core system follows the same file structure and implements the same core interfaces, making it easy for developers to understand any core system once they're familiar with the pattern.

## 2. Core System Structure

Every core system follows this exact file structure:

```
app/core/{system_name}/
├── __init__.py                  # Public API exports
├── base.py                      # Base interfaces and types
├── exceptions.py                # System-specific exceptions
├── models.py                    # Database models (if needed)
├── schemas.py                   # Pydantic schemas (if needed)
├── service.py                   # Service implementation
├── manager.py                   # Component manager
├── utils.py                     # Utility functions
└── backends/                    # Implementation backends
    ├── __init__.py              # Backend registry and factory
    └── {backend_name}.py        # Backend implementations (one file per backend)
```

## 3. File Purposes and Contents

### 3.1 __init__.py

**Purpose**: Exports the public API and provides a service factory function.

**Contents**:
- Import and re-export public types and interfaces
- Singleton service instance management
- `get_{system}_service()` factory function

**Example**:
```python
from __future__ import annotations

"""
{System} package for {purpose}.

This package provides functionality for {description}.
"""

from typing import Optional

# Import base types and interfaces
from app.core.{system}.base import (
    {System}Backend,
    {System}Context,
    # Other key types...
)

# Import service
from app.core.{system}.service import {System}Service

# Import exceptions
from app.core.{system}.exceptions import (
    {System}Exception,
    {System}BackendException,
    # Other exceptions...
)

# Singleton service instance
_{system}_service_instance: Optional[{System}Service] = None

def get_{system}_service(**kwargs) -> {System}Service:
    """Get the {system} service instance.

    Args:
        **kwargs: Service configuration options.

    Returns:
        The {system} service instance.
    """
    global _{system}_service_instance

    # Create new instance if none exists or if config is provided
    if _{system}_service_instance is None or kwargs:
        _{system}_service_instance = {System}Service(**kwargs)

    return _{system}_service_instance

# Export public API
__all__ = [
    # Service
    "{System}Service",
    "get_{system}_service",

    # Base types
    "{System}Backend",
    "{System}Context",
    # Other exports...
]
```

### 3.2 base.py

**Purpose**: Defines core interfaces, protocols, enums and types.

**Contents**:
- System-specific enums (e.g., event types, log levels)
- Protocol interfaces
- Pydantic models for configuration and data structures
- Type definitions

**Example**:
```python
from __future__ import annotations

"""
Base interfaces and types for the {system} system.

This module defines common types, protocols, and interfaces
used throughout the {system} service components.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, TypeVar

from pydantic import BaseModel, Field

from app.core.base import CoreBackend

# Core enums
class {System}EventType(str, Enum):
    """Types of events in the {system} system."""
    EVENT_1 = "event_1"
    EVENT_2 = "event_2"
    # ...

# Core models
class {System}Context(BaseModel):
    """Context information for {system} operations."""
    field1: str = Field(..., description="Description of field1")
    field2: Optional[int] = Field(None, description="Description of field2")
    # ...

# Backend protocol
class {System}Backend(CoreBackend, Protocol):
    """Protocol for {system} backends."""

    async def operation_name(
        self,
        param1: str,
        param2: Optional[int] = None,
    ) -> Any:
        """Description of the operation.

        Args:
            param1: Description of param1.
            param2: Description of param2.

        Returns:
            Description of the return value.
        """
        ...
```

### 3.3 exceptions.py

**Purpose**: Defines system-specific exceptions that extend core exceptions.

**Contents**:
- Base exception for the system
- Specialized exceptions for different error scenarios
- Error mapping and utility functions

**Example**:
```python
from __future__ import annotations

"""
{System}-specific exceptions for the application.

This module defines exceptions related to {system} operations that integrate
with the application's exception system.
"""

from typing import Any, Dict, List, Optional, Union

from app.core.exceptions.base import ErrorCode
from app.core.exceptions.service import BackendError, CoreServiceException, ManagerError

class {System}Exception(CoreServiceException):
    """Base exception for all {system}-related errors."""
    # Implementation...

class {System}BackendException(BackendError):
    """Exception raised when a {system} backend operation fails."""
    # Implementation...

class {System}ManagerException(ManagerError):
    """Exception raised when a {system} manager operation fails."""
    # Implementation...

class {System}ConfigurationException({System}Exception):
    """Exception raised when {system} configuration is invalid."""
    # Implementation...
```

### 3.4 service.py

**Purpose**: Main service implementation that provides the public API.

**Contents**:
- `{System}Service` class extending `CoreService`
- Public methods for system functionality
- Delegation to the manager for implementation details

**Example**:
```python
from __future__ import annotations

"""
Main {system} service implementation.

This module provides the primary {System}Service that coordinates {system}
operations.
"""

from typing import Any, Dict, Optional

from app.core.{system}.base import {System}Context
from app.core.{system}.manager import {System}Manager
from app.core.base import CoreService, HealthCheckable
from app.logging import get_logger

logger = get_logger("app.core.{system}.service")

class {System}Service(CoreService, HealthCheckable):
    """Service for {system} operations.

    This service coordinates {system} operations across different backends.
    """

    @property
    def service_name(self) -> str:
        """Get the service name.

        Returns:
            The service name.
        """
        return "{system}"

    def __init__(self, **kwargs) -> None:
        """Initialize the {system} service."""
        super().__init__()
        self.manager = {System}Manager(**kwargs)
        self.register_component(self.manager)

        logger.debug("{System} service created")

    async def operation_name(self, param1: str, param2: Optional[int] = None) -> Any:
        """Description of the operation.

        Args:
            param1: Description of param1.
            param2: Description of param2.

        Returns:
            Description of the return value.
        """
        # Delegate to manager
        return await self.manager.operation_name(param1, param2)

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check.

        Returns:
            Dict containing health status information.
        """
        return await self.manager.health_check()
```

### 3.5 manager.py

**Purpose**: Coordinates backends and implements core functionality.

**Contents**:
- `{System}Manager` class extending `CoreManager`
- Backend coordination
- Implementation details of system operations
- Query and management functionality

**Example**:
```python
from __future__ import annotations

"""
{System} manager for the application.

This module provides a central manager for {system} backends,
handling initialization, configuration, and access to backends.
"""

from typing import Any, Dict, List, Optional

from app.core.{system}.backends import create_default_backends, get_backend
from app.core.{system}.base import {System}Backend
from app.core.{system}.exceptions import {System}ManagerException
from app.core.base import CoreManager
from app.core.config import settings
from app.logging import get_logger

logger = get_logger("app.core.{system}.manager")

class {System}Manager(CoreManager):
    """Manager for {system} backends.

    Provides a central point for accessing and managing different {system} backends.
    """

    @property
    def component_name(self) -> str:
        """Get the component name.

        Returns:
            The component name.
        """
        return "{system}"

    def __init__(self, **kwargs) -> None:
        """Initialize the {system} manager."""
        super().__init__()
        self.backends: List[{System}Backend] = []
        self.enabled = getattr(settings, "{SYSTEM}_ENABLED", True)
        # Initialize other properties...

    async def _initialize_manager(self) -> None:
        """Initialize manager-specific logic."""
        if not self.enabled:
            self.logger.info("{System} is disabled")
            return

        # Initialize backends
        try:
            self.backends = create_default_backends()

            for backend in self.backends:
                self.register_component(backend)

            self.logger.info(
                f"Initialized {len(self.backends)} {system} backends: "
                f"{', '.join([b.__class__.__name__ for b in self.backends])}"
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize {system} backends: {str(e)}", exc_info=True)
            raise {System}ManagerException(
                operation="initialize",
                message="Failed to initialize {system} backends",
                original_exception=e,
            )

    async def operation_name(self, param1: str, param2: Optional[int] = None) -> Any:
        """Implementation of the operation.

        Args:
            param1: Description of param1.
            param2: Description of param2.

        Returns:
            Description of the return value.
        """
        if not self.enabled:
            return "disabled"

        if not self.backends:
            self.logger.warning("No {system} backends configured")
            return "no-backends"

        # Implementation...
```

### 3.6 utils.py

**Purpose**: Utility functions for the core system.

**Contents**:
- Helper functions
- Data transformation utilities
- Common operations

**Example**:
```python
from __future__ import annotations

"""
Utility functions for the {system} system.

This module provides utility functions for {system} operations.
"""

from typing import Any, Dict, List, Optional

from app.logging import get_logger

logger = get_logger("app.core.{system}.utils")

def utility_function(param1: str, param2: int) -> Dict[str, Any]:
    """Description of the utility function.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of the return value.
    """
    # Implementation...
    return {}
```

### 3.7 backends/__init__.py

**Purpose**: Factory for creating and accessing backends.

**Contents**:
- Backend registry
- Factory functions for creating backends
- Default backend configuration

**Example**:
```python
from __future__ import annotations

"""
Factory for creating {system} backends.

This module provides a factory for creating different {system} backend instances
based on configuration settings.
"""

from typing import Any, Dict, List, Optional, Type

from app.core.{system}.base import {System}Backend
from app.core.config import settings
from app.logging import get_logger

logger = get_logger("app.core.{system}.backends")

# Backend registry
_backends: Dict[str, Type[{System}Backend]] = {}

def register_backend(name: str, backend_class: Type[{System}Backend]) -> None:
    """Register a {system} backend.

    Args:
        name: Name of the backend.
        backend_class: Backend class to register.

    Raises:
        ValueError: If a backend with the given name is already registered.
    """
    if name in _backends:
        raise ValueError(f"{System} backend '{name}' is already registered")

    _backends[name] = backend_class
    logger.debug(f"Registered {system} backend: {name}")

def get_backend(name: str, **kwargs: Any) -> {System}Backend:
    """Get a {system} backend by name.

    Args:
        name: Name of the backend to get.
        **kwargs: Additional arguments for the backend.

    Returns:
        The backend instance.

    Raises:
        ValueError: If the backend is not registered.
    """
    if name not in _backends:
        valid_backends = ", ".join(_backends.keys())
        raise ValueError(
            f"Unknown {system} backend: {name}. Valid backends: {valid_backends}"
        )

    backend_class = _backends[name]
    return backend_class(**kwargs)

def create_default_backends(**kwargs) -> List[{System}Backend]:
    """Create the default set of {system} backends based on configuration.

    Args:
        **kwargs: Additional arguments for the backends.

    Returns:
        List of created backend instances.
    """
    backends: List[{System}Backend] = []

    # Create backends based on configuration
    backend_names = getattr(settings, "{SYSTEM}_BACKENDS", ["default"])

    for name in backend_names:
        backends.append(get_backend(name, **kwargs))

    return backends

# Import backend implementations after defining the factory functions
# to avoid circular imports
from app.core.{system}.backends.backend1 import Backend1
from app.core.{system}.backends.backend2 import Backend2

# Register backend implementations
register_backend("backend1", Backend1)
register_backend("backend2", Backend2)

__all__ = [
    "get_backend",
    "create_default_backends",
    "register_backend",
    "Backend1",
    "Backend2",
]
```

### 3.8 backends/{backend_name}.py

**Purpose**: Specific backend implementation.

**Contents**:
- Backend class implementing the backend protocol
- Integration with external systems or storage
- Implementation of backend operations

**Example**:
```python
from __future__ import annotations

"""
{Backend} implementation for {system}.

This module provides a backend that implements {system} functionality using {backend}.
"""

from typing import Any, Dict, Optional

from app.core.{system}.base import {System}Backend
from app.logging import get_logger

logger = get_logger("app.core.{system}.backends.{backend}")

class {Backend}Backend({System}Backend):
    """{System} backend implementation using {backend}."""

    __backend_name__ = "{backend}"

    def __init__(self, **kwargs) -> None:
        """Initialize the {backend} backend."""
        # Initialize backend-specific properties

    async def initialize(self) -> None:
        """Initialize the backend."""
        logger.info("{Backend} backend initialized")

    async def shutdown(self) -> None:
        """Shut down the backend."""
        logger.info("{Backend} backend shut down")

    async def operation_name(self, param1: str, param2: Optional[int] = None) -> Any:
        """Implement the operation using {backend}.

        Args:
            param1: Description of param1.
            param2: Description of param2.

        Returns:
            Description of the return value.
        """
        # Implementation using this backend

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check.

        Returns:
            Dict containing health status information.
        """
        return {
            "status": "healthy",
            "component": "{backend}_backend",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
```

### 3.9 models.py

**Purpose**: Defines SQLAlchemy models for database storage.

**Contents**:
- ORM models with table definitions
- Relationships between models
- Indexes and constraints
- Utility methods for model instances

**Example**:
```python
from __future__ import annotations

"""
{System} model definitions.

This module defines SQLAlchemy models for {system} data storage.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING

from sqlalchemy import DateTime, String, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.domains.users.models import User

class {System}Model(Base):
    """Database model for {system} data."""

    __tablename__ = "{system}_data"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True,
        default=datetime.now, onupdate=datetime.now
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True, index=True
    )
    # Other fields specific to this model

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="{system}_data")

    # Indexes
    __table_args__ = (
        Index("ix_{system}_data_user_id", user_id),
        # Additional indexes
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation.
        """
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_id": str(self.user_id) if self.user_id else None,
            # Other fields
        }
```

### 3.10 schemas.py

**Purpose**: Defines Pydantic models for validation and serialization.

**Contents**:
- Input validation schemas
- Response schemas
- Internal data schemas
- Schema utilities and converters

**Example**:
```python
from __future__ import annotations

"""
{System} schema definitions.

This module defines Pydantic schemas for {system} data validation and serialization.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

class {System}StatusEnum(str, Enum):
    """Status options for {system}."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

class {System}Base(BaseModel):
    """Base schema for {system} data."""

    name: str = Field(..., description="Name")
    description: Optional[str] = Field(None, description="Description")
    status: {System}StatusEnum = Field(
        {System}StatusEnum.PENDING, description="Status"
    )
    # Other fields common to all schemas

class {System}Create(BaseModel):
    """Schema for creating {system} data."""

    name: str = Field(..., description="Name")
    description: Optional[str] = Field(None, description="Description")
    # Fields needed for creation

class {System}Update(BaseModel):
    """Schema for updating {system} data."""

    name: Optional[str] = Field(None, description="Name")
    description: Optional[str] = Field(None, description="Description")
    # Fields that can be updated

class {System}InDB({System}Base):
    """Schema for {system} data as stored in the database."""

    id: uuid.UUID = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    user_id: Optional[uuid.UUID] = Field(None, description="Owner user ID")

    model_config = ConfigDict(from_attributes=True)

class {System}Response({System}InDB):
    """Schema for {system} data in API responses."""

    # Additional fields for responses
    user: Optional[Dict[str, Any]] = Field(None, description="User details")
```

## Integration Guidelines

1. **Only include when needed**: Not all core systems require database models or schemas. Include them only when needed.

2. **Consistent naming**: Use the singular form for model classes (e.g., `AuditLog`, not `AuditLogs`) and clear, descriptive names for schemas (e.g., `AuditLogCreate`, `AuditLogResponse`).

3. **Consistent imports**: Follow the project's import patterns and ordering conventions.

4. **Export in __init__.py**: Export model and schema classes from the package's `__init__.py` file.

5. **Relationships**: Define proper relationships between models, especially if they span across different core systems.

6. **Type safety**: Use comprehensive type hints throughout models and schemas.

7. **Documentation**: Include descriptive docstrings and field descriptions.

## 4. Lifecycle Management

All core systems follow a consistent initialization and shutdown pattern:

### 4.1 Initialization

1. Service is created with `get_{system}_service()`
2. Service is initialized with `await service.initialize()`
3. Service initializes its manager
4. Manager initializes its backends
5. Backends establish connections or resources

**Flow**:
```
Service.initialize()
  ↓
Manager.initialize()
  ↓
Backend1.initialize() + Backend2.initialize() + ...
```

### 4.2 Shutdown

1. Service shutdown is triggered with `await service.shutdown()`
2. Service shuts down its manager
3. Manager shuts down its backends
4. Backends release connections or resources

**Flow**:
```
Service.shutdown()
  ↓
Manager.shutdown()
  ↓
Backend2.shutdown() + Backend1.shutdown() + ... (reverse order)
```

### 4.3 Context Manager

All services support the async context manager protocol:

```python
async with get_audit_service() as audit:
    await audit.log_event(...)
# Service is automatically shut down after the block
```

## 5. Service Configuration

Configure services through:

1. **Environment variables** - Prefixed with the system name (e.g., `AUDIT_ENABLED`)
2. **Settings module** - Properties in `app.core.config.settings`
3. **Constructor parameters** - Passed to `get_{system}_service()`

Configuration cascades in that order (constructor parameters override environment variables).

## 6. Health Checking

All components implement health checking with the `health_check()` method:

```python
# Check the health of a service and all its components
health_info = await service.health_check()

# Health info structure
{
    "status": "healthy", # or "degraded" or "unhealthy"
    "service": "service_name",
    "components": [
        {
            "status": "healthy",
            "component": "manager_name",
            "components": [
                {
                    "status": "healthy",
                    "component": "backend_name",
                    "timestamp": "2023-01-01T00:00:00Z"
                }
            ],
            "timestamp": "2023-01-01T00:00:00Z"
        }
    ],
    "timestamp": "2023-01-01T00:00:00Z"
}
```

## 7. Error Handling

Each core system defines its own exception hierarchy:

```
CoreServiceException
  ↓
{System}Exception
  ↓
{System}BackendException, {System}ManagerException, {System}ConfigurationException
```

Error handling follows these patterns:

1. **Catch and wrap** - Catch lower-level exceptions and wrap them in system-specific exceptions
2. **Context in exceptions** - Include operation name, component name, and other context
3. **Error logging** - Log errors with appropriate severity and context
4. **Clean failure** - Fail gracefully and provide meaningful error messages

## 8. Adding a New Core System

To add a new core system:

1. Create the directory structure: `app/core/{system_name}/`
2. Create the required files following the patterns above
3. Define the base interfaces in `base.py`
4. Implement backends in `backends/{backend_name}.py`
5. Implement the manager in `manager.py`
6. Implement the service in `service.py`
7. Define exceptions in `exceptions.py`
8. Export the public API in `__init__.py`
9. Register the service with the dependency manager

## 9. Accessing Core Services

Core services can be accessed:

1. **Directly** - Using `get_{system}_service()`
2. **Dependency injection** - Using the dependency manager
3. **Service Registry** - Using `ServiceRegistry.get("system_name")`

**Example**:
```python
# Direct access
from app.core.audit import get_audit_service

async def function():
    audit = get_audit_service()
    await audit.log_event(...)

# Dependency injection
from app.core.dependency_manager import inject_dependency

@inject_dependency("audit_service")
async def function(audit_service):
    await audit_service.log_event(...)

# Service Registry
from app.core.base import ServiceRegistry

async def function():
    audit = ServiceRegistry.get("audit")
    await audit.log_event(...)
```

## 10. Testing Core Systems

### 10.1 Unit Testing

For unit testing individual components:

1. Create mock backends using the Backend Protocol
2. Inject mocks into the manager
3. Test manager functionality
4. Test service delegation

### 10.2 Integration Testing

For integration testing:

1. Use the `NullBackend` pattern for harmless backends
2. Use in-memory implementations where possible
3. Configure test-specific settings
4. Test end-to-end functionality

### 10.3 Example Test

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.core.audit import get_audit_service
from app.core.audit.base import AuditBackend

class MockAuditBackend(AuditBackend):
    """Mock audit backend for testing."""

    __backend_name__ = "mock"

    def __init__(self):
        self.log_event = AsyncMock(return_value="mock-event-id")
        self.initialize = AsyncMock()
        self.shutdown = AsyncMock()
        self.health_check = AsyncMock(return_value={"status": "healthy"})

@pytest.fixture
async def audit_service():
    """Fixture for an audit service with a mock backend."""
    service = get_audit_service()

    # Replace backends with mock
    mock_backend = MockAuditBackend()
    service.manager.backends = [mock_backend]

    # Initialize service
    await service.initialize()

    yield service

    # Clean up
    await service.shutdown()

async def test_log_event(audit_service):
    """Test logging an event."""
    # Act
    event_id = await audit_service.log_event(
        event_type="test_event",
        user_id="test-user"
    )

    # Assert
    assert event_id == "mock-event-id"

    # Verify backend was called
    backend = audit_service.manager.backends[0]
    backend.log_event.assert_called_once()

    # Verify args
    args, kwargs = backend.log_event.call_args
    assert kwargs["event_type"] == "test_event"
    assert kwargs["context"].user_id == "test-user"
```

## 11. Best Practices

### 11.1 Design Principles

1. **Single Responsibility** - Each component has one primary responsibility
2. **Interface Segregation** - Define specific interfaces for different functionalities
3. **Dependency Inversion** - Depend on abstractions, not implementations
4. **Open-Closed** - Open for extension, closed for modification
5. **KISS** - Keep implementations simple and focused

### 11.2 Implementation Guidelines

1. **Type Safety** - Use comprehensive type hints and protocols
2. **Error Handling** - Catch specific exceptions and provide context
3. **Logging** - Log key events and operations with appropriate level
4. **Documentation** - Document all public APIs with docstrings
5. **Testing** - Write unit and integration tests

### 11.3 Performance Considerations

1. **Lazy Initialization** - Initialize resources only when needed
2. **Connection Pooling** - Reuse connections and resources
3. **Batching** - Batch operations when possible
4. **Caching** - Cache expensive operations or frequently accessed data
5. **Async** - Use asynchronous operations for I/O-bound tasks

## 12. Application Integration

### 12.1 Service Registration

Register your service with the dependency manager:

```python
# In app/core/dependency_manager.py
def register_services() -> None:
    # ...

    # Register your service
    dependency_manager.register_service(
        lambda **kwargs: get_your_service(**kwargs),
        "your_service"
    )
```

### 12.2 FastAPI Dependency

Create a FastAPI dependency:

```python
# In app/api/deps.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.core.your_system import get_your_service

async def get_your_service_from_db(
    db: AsyncSession = Depends(get_async_session),
) -> YourService:
    """Get the your service with database session."""
    return get_your_service(db=db)
```

### 12.3 API Route Usage

Use in API routes:

```python
# In app/api/v1/endpoints/your_endpoints.py
from fastapi import APIRouter, Depends

from app.api.deps import get_your_service_from_db
from app.core.your_system import YourService

router = APIRouter()

@router.post("/your-endpoint")
async def your_endpoint(
    your_service: YourService = Depends(get_your_service_from_db),
):
    result = await your_service.your_operation()
    return {"result": result}
```

## 13. Example Core Systems

Our application includes the following core systems:

1. **Audit** - Logging of system events and user actions
2. **Cache** - Caching of data and computations
3. **Error** - Error handling and reporting
4. **Events** - Pub/sub event system
5. **Metrics** - Collection and reporting of metrics
6. **Validation** - Data validation and normalization
7. **Rate Limiting** - Controlling access rates to resources

Refer to their implementations for examples.
