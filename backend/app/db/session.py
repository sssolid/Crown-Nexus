# backend/app/db/session.py
"""
Database session management module.

This module provides utilities for creating and managing database sessions
using SQLAlchemy's async functionality. It configures the engine with
appropriate connection pooling and provides session factory functions.

The module exports:
- An async engine instance configured from application settings
- A session maker configured for async operations
- A dependency provider for FastAPI route functions
- A context manager for use in scripts and background tasks

Usage:
    For FastAPI route dependencies:
    ```python
    from fastapi import Depends
    from app.db.session import get_db

    @router.get("/items")
    async def get_items(db: AsyncSession = Depends(get_db)):
        # Use db session here
        ...
    ```

    For scripts and context managers:
    ```python
    from app.db.session import get_db_context

    async def some_task():
        async with get_db_context() as db:
            # Use db session here
            ...
    ```
"""

from __future__ import annotations

import contextlib
from typing import AsyncGenerator, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# Create an async engine with proper configuration
# NullPool is safer for web applications to prevent
# connection leaks in case of unexpected errors
engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,
    future=True,
    pool_pre_ping=True,  # Check connection validity before using from pool
)

# Create sessionmaker with reasonable defaults
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session.

    This dependency provides an async database session that automatically
    rolls back any failed transactions and closes the session when done.

    Yields:
        AsyncSession: Database session
    """
    session: Optional[AsyncSession] = None
    try:
        session = async_session_maker()
        yield session
        await session.commit()
    except SQLAlchemyError as e:
        if session:
            await session.rollback()
        raise
    finally:
        if session:
            await session.close()


@contextlib.asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions.

    This is useful for scripts that need to handle their own transactions
    and session lifecycle outside of FastAPI's dependency injection.

    Yields:
        AsyncSession: Database session
    """
    session: Optional[AsyncSession] = None
    try:
        session = async_session_maker()
        yield session
        await session.commit()
    except SQLAlchemyError:
        if session:
            await session.rollback()
        raise
    finally:
        if session:
            await session.close()
