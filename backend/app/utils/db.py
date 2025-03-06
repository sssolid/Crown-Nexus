# backend/app/utils/db.py
"""
Database utility functions.

This module provides helper functions for common database operations:
- Optimized bulk operations
- Transaction management
- Query optimization
- Connection pooling utilities

These utilities improve performance and maintainability of database
operations throughout the application.
"""

from __future__ import annotations

import contextlib
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Sequence, Type, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Delete, Insert, Select, Update

from app.db.base_class import Base

# Type variable for model classes
T = TypeVar('T', bound=Base)


async def get_by_id(db: AsyncSession, model: Type[T], id: Any) -> Optional[T]:
    """
    Get a model instance by ID.

    Args:
        db: Database session
        model: Model class
        id: Instance ID

    Returns:
        Optional[T]: Model instance or None if not found
    """
    result = await db.execute(select(model).where(model.id == id))
    return result.scalar_one_or_none()


async def create_object(db: AsyncSession, model: Type[T], obj_in: Dict[str, Any]) -> T:
    """
    Create a model instance.

    Args:
        db: Database session
        model: Model class
        obj_in: Object data

    Returns:
        T: Created model instance
    """
    db_obj = model(**obj_in)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_object(
    db: AsyncSession, model: Type[T], id: Any, obj_in: Dict[str, Any]
) -> Optional[T]:
    """
    Update a model instance by ID.

    Args:
        db: Database session
        model: Model class
        id: Instance ID
        obj_in: Object data

    Returns:
        Optional[T]: Updated model instance or None if not found
    """
    db_obj = await get_by_id(db, model, id)
    if db_obj is None:
        return None

    # Update fields
    for field, value in obj_in.items():
        setattr(db_obj, field, value)

    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def delete_object(db: AsyncSession, model: Type[T], id: Any) -> bool:
    """
    Delete a model instance by ID.

    Args:
        db: Database session
        model: Model class
        id: Instance ID

    Returns:
        bool: True if deleted, False if not found
    """
    db_obj = await get_by_id(db, model, id)
    if db_obj is None:
        return False

    await db.delete(db_obj)
    await db.commit()
    return True


async def bulk_create(
    db: AsyncSession, model: Type[T], objects: List[Dict[str, Any]]
) -> List[T]:
    """
    Create multiple model instances in a single transaction.

    This is more efficient than creating objects one at a time.

    Args:
        db: Database session
        model: Model class
        objects: List of object data

    Returns:
        List[T]: List of created model instances
    """
    # Create instances
    instances = [model(**obj) for obj in objects]

    # Add all instances
    db.add_all(instances)

    # Commit in a single transaction
    await db.commit()

    # Refresh all instances
    for instance in instances:
        await db.refresh(instance)

    return instances


async def execute_query(
    db: AsyncSession, query: Select | Update | Delete | Insert
) -> Any:
    """
    Execute a SQLAlchemy query.

    Args:
        db: Database session
        query: SQLAlchemy query

    Returns:
        Any: Query result
    """
    result = await db.execute(query)
    return result


@contextlib.asynccontextmanager
async def transaction(db: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database transactions.

    This ensures that all operations within the context are committed
    together or rolled back on error.

    Args:
        db: Database session

    Yields:
        AsyncSession: Database session
    """
    try:
        yield db
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise


async def paginate(
    db: AsyncSession,
    query: Select,
    page: int = 1,
    page_size: int = 20,
) -> Dict[str, Any]:
    """
    Paginate a query.

    Args:
        db: Database session
        query: Base query
        page: Page number (starting from 1)
        page_size: Number of items per page

    Returns:
        Dict[str, Any]: Pagination result with items, total, page, page_size, and pages
    """
    # Ensure valid pagination parameters
    page = max(1, page)
    page_size = max(1, min(100, page_size))

    # Calculate skip
    skip = (page - 1) * page_size

    # Get total count (create a subquery to count efficiently)
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Apply pagination to the original query
    paginated_query = query.offset(skip).limit(page_size)
    result = await db.execute(paginated_query)
    items = result.scalars().all()

    # Calculate total pages
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }
