# app/utils/db.py
"""
Database utility functions for common database operations.

This module provides utility functions for common database operations such as:
- CRUD operations (get, create, update, delete)
- Transaction management
- Pagination
- Bulk operations

All functions include proper error handling, logging, and validation to ensure
database operations are performed safely and consistently.
"""

from __future__ import annotations

import contextlib
from functools import wraps
from typing import Any, AsyncGenerator, Callable, Dict, Generic, List, Optional, Sequence, Type, TypeVar, Union, cast

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Delete, Insert, Select, Update

from app.core.exceptions import (
    DatabaseException,
    DataIntegrityException,
    ErrorCode,
    TransactionException,
)
from app.core.logging import get_logger
from app.db.base_class import Base

# Initialize structured logger
logger = get_logger("app.utils.db")

# Type variable for models (must be subclass of Base)
T = TypeVar("T", bound=Base)
F = TypeVar("F", bound=Callable[..., Any])


@contextlib.asynccontextmanager
async def transaction(db: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """Context manager for database transactions with error handling.

    Manages database transaction lifecycle, including commit and rollback.

    Args:
        db: SQLAlchemy async session object

    Yields:
        AsyncSession: The database session

    Raises:
        TransactionException: If transaction fails
    """
    # Skip if already in transaction
    if db.in_transaction():
        yield db
        return

    # Start new transaction
    try:
        async with db.begin():
            logger.debug("Transaction started")
            yield db
            logger.debug("Transaction committed")
    except SQLAlchemyError as e:
        logger.error(f"Transaction error: {str(e)}", exc_info=True)
        raise TransactionException(
            message=f"Database transaction failed: {str(e)}",
            code=ErrorCode.TRANSACTION_FAILED,
            original_exception=e,
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error in transaction: {str(e)}", exc_info=True)
        raise TransactionException(
            message=f"Unexpected error in transaction: {str(e)}",
            code=ErrorCode.TRANSACTION_FAILED,
            original_exception=e,
        ) from e


def transactional(func: F) -> F:
    """Decorator to wrap function in a database transaction.

    Args:
        func: Async function that accepts a database session

    Returns:
        F: Wrapped function

    Raises:
        ValueError: If no database session is provided
        TransactionException: If transaction fails
    """
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Find db session in args or kwargs
        db = None
        for arg in args:
            if isinstance(arg, AsyncSession):
                db = arg
                break

        if db is None:
            db = kwargs.get("db")

        if db is None:
            logger.error("No database session provided to transactional method")
            raise ValueError("No database session provided to transactional method")

        async with transaction(db):
            return await func(*args, **kwargs)

    return cast(F, wrapper)


async def execute_query(
    db: AsyncSession,
    query: Union[Select, Insert, Update, Delete]
) -> Any:
    """Execute a SQLAlchemy query with error handling.

    Args:
        db: SQLAlchemy async session object
        query: SQLAlchemy query to execute

    Returns:
        Any: Query result

    Raises:
        DatabaseException: If query execution fails
    """
    try:
        logger.debug(f"Executing query: {query}")
        result = await db.execute(query)
        return result
    except SQLAlchemyError as e:
        logger.error(f"Query execution error: {str(e)}", exc_info=True)
        raise DatabaseException(
            message=f"Query execution failed: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def get_by_id(
    db: AsyncSession,
    model: Type[T],
    id_value: Any
) -> Optional[T]:
    """Get a model instance by ID.

    Args:
        db: SQLAlchemy async session object
        model: SQLAlchemy model class
        id_value: Primary key value

    Returns:
        Optional[T]: Model instance if found, None otherwise

    Raises:
        DatabaseException: If query fails
    """
    try:
        logger.debug(f"Getting {model.__name__} by ID: {id_value}")
        query = model.filter_by_id(id_value)
        result = await db.execute(query)
        instance = result.scalars().first()

        if instance:
            logger.debug(f"Found {model.__name__} with ID: {id_value}")
        else:
            logger.debug(f"No {model.__name__} found with ID: {id_value}")

        return instance
    except SQLAlchemyError as e:
        logger.error(f"Error fetching {model.__name__} by ID: {str(e)}", exc_info=True)
        raise DatabaseException(
            message=f"Failed to fetch {model.__name__} by ID: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def get_by_ids(
    db: AsyncSession,
    model: Type[T],
    ids: List[Any]
) -> List[T]:
    """Get multiple model instances by IDs.

    Args:
        db: SQLAlchemy async session object
        model: SQLAlchemy model class
        ids: List of primary key values

    Returns:
        List[T]: List of model instances

    Raises:
        DatabaseException: If query fails
    """
    if not ids:
        logger.debug(f"Empty ID list for {model.__name__}, returning empty result")
        return []

    try:
        logger.debug(f"Getting {model.__name__} by IDs: {ids}")
        query = select(model).where(model.id.in_(ids), model.is_deleted == False)
        result = await db.execute(query)
        instances = list(result.scalars().all())

        logger.debug(f"Found {len(instances)} {model.__name__} instances")
        return instances
    except SQLAlchemyError as e:
        logger.error(f"Error fetching {model.__name__} by IDs: {str(e)}", exc_info=True)
        raise DatabaseException(
            message=f"Failed to fetch {model.__name__} by IDs: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def create_object(
    db: AsyncSession,
    model: Type[T],
    obj_in: Dict[str, Any]
) -> T:
    """Create a new model instance.

    Args:
        db: SQLAlchemy async session object
        model: SQLAlchemy model class
        obj_in: Dictionary of model attribute values

    Returns:
        T: Created model instance

    Raises:
        DatabaseException: If creation fails
    """
    try:
        logger.debug(f"Creating {model.__name__}: {obj_in}")
        db_obj = model(**obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)

        logger.info(f"Created {model.__name__} with ID: {getattr(db_obj, 'id', None)}")
        return db_obj
    except SQLAlchemyError as e:
        logger.error(f"Error creating {model.__name__}: {str(e)}", exc_info=True)

        # Handle unique constraint violations
        if "unique constraint" in str(e).lower() or "unique violation" in str(e).lower():
            raise DataIntegrityException(
                message=f"A {model.__name__} with these attributes already exists",
                code=ErrorCode.DATA_INTEGRITY_ERROR,
                original_exception=e,
            ) from e

        raise DatabaseException(
            message=f"Failed to create {model.__name__}: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def update_object(
    db: AsyncSession,
    model: Type[T],
    id_value: Any,
    obj_in: Dict[str, Any],
    user_id: Optional[Any] = None
) -> Optional[T]:
    """Update a model instance.

    Args:
        db: SQLAlchemy async session object
        model: SQLAlchemy model class
        id_value: Primary key value
        obj_in: Dictionary of model attribute values to update
        user_id: ID of user performing the update (for audit)

    Returns:
        Optional[T]: Updated model instance if found, None otherwise

    Raises:
        DatabaseException: If update fails
    """
    try:
        logger.debug(f"Updating {model.__name__} with ID: {id_value}")
        db_obj = await get_by_id(db, model, id_value)

        if not db_obj:
            logger.warning(f"Update failed: No {model.__name__} found with ID: {id_value}")
            return None

        # Set updated_by_id if provided
        if user_id is not None:
            obj_in["updated_by_id"] = user_id

        db_obj.update_from_dict(obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)

        logger.info(f"Updated {model.__name__} with ID: {id_value}")
        return db_obj
    except SQLAlchemyError as e:
        logger.error(f"Error updating {model.__name__}: {str(e)}", exc_info=True)

        # Handle unique constraint violations
        if "unique constraint" in str(e).lower() or "unique violation" in str(e).lower():
            raise DataIntegrityException(
                message=f"Cannot update {model.__name__}: A record with these attributes already exists",
                code=ErrorCode.DATA_INTEGRITY_ERROR,
                original_exception=e,
            ) from e

        raise DatabaseException(
            message=f"Failed to update {model.__name__}: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def delete_object(
    db: AsyncSession,
    model: Type[T],
    id_value: Any,
    user_id: Optional[Any] = None,
    hard_delete: bool = False
) -> bool:
    """Delete a model instance (soft or hard delete).

    Args:
        db: SQLAlchemy async session object
        model: SQLAlchemy model class
        id_value: Primary key value
        user_id: ID of user performing the delete (for audit)
        hard_delete: If True, permanently delete the record

    Returns:
        bool: True if deleted, False if not found

    Raises:
        DatabaseException: If deletion fails
    """
    try:
        logger.debug(f"Deleting {model.__name__} with ID: {id_value} (hard_delete={hard_delete})")
        db_obj = await get_by_id(db, model, id_value)

        if not db_obj:
            logger.warning(f"Delete failed: No {model.__name__} found with ID: {id_value}")
            return False

        if hard_delete:
            await db.delete(db_obj)
            logger.info(f"Hard deleted {model.__name__} with ID: {id_value}")
        else:
            db_obj.soft_delete(user_id)
            db.add(db_obj)
            logger.info(f"Soft deleted {model.__name__} with ID: {id_value}")

        await db.flush()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error deleting {model.__name__}: {str(e)}", exc_info=True)

        # Handle foreign key constraint violations
        if "foreign key constraint" in str(e).lower():
            raise DataIntegrityException(
                message=f"Cannot delete {model.__name__}: It is referenced by other records",
                code=ErrorCode.DATA_INTEGRITY_ERROR,
                original_exception=e,
            ) from e

        raise DatabaseException(
            message=f"Failed to delete {model.__name__}: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def count_query(db: AsyncSession, query: Select) -> int:
    """Count the number of records returned by a query.

    Args:
        db: SQLAlchemy async session object
        query: SQLAlchemy query

    Returns:
        int: Count of matching records

    Raises:
        DatabaseException: If query fails
    """
    try:
        count_query = select(func.count()).select_from(query.subquery())
        result = await db.execute(count_query)
        count = result.scalar() or 0

        logger.debug(f"Query count result: {count}")
        return count
    except SQLAlchemyError as e:
        logger.error(f"Error counting query results: {str(e)}", exc_info=True)
        raise DatabaseException(
            message=f"Failed to count query results: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def paginate(
    db: AsyncSession,
    query: Select,
    page: int = 1,
    page_size: int = 20,
    load_items: bool = True
) -> Dict[str, Any]:
    """Paginate query results.

    Args:
        db: SQLAlchemy async session object
        query: SQLAlchemy query
        page: Page number (1-indexed)
        page_size: Number of items per page
        load_items: Whether to load the items or just count

    Returns:
        Dict[str, Any]: Dictionary containing:
            - items: List of items
            - total: Total number of items
            - page: Current page number
            - page_size: Number of items per page
            - pages: Total number of pages

    Raises:
        DatabaseException: If query fails
    """
    # Validate pagination parameters
    if page < 1:
        logger.warning(f"Invalid page number: {page}, using page 1")
        page = 1

    if page_size < 1:
        logger.warning(f"Invalid page size: {page_size}, using page size 20")
        page_size = 20

    if page_size > 100:
        logger.warning(f"Page size too large: {page_size}, using maximum 100")
        page_size = 100

    try:
        # Get total count
        total = await count_query(db, query)

        # Calculate number of pages
        pages = (total + page_size - 1) // page_size if total > 0 else 0

        # Adjust page if out of range
        if page > pages and pages > 0:
            logger.warning(f"Page {page} out of range, using page {pages}")
            page = pages

        # Calculate offset
        offset = (page - 1) * page_size

        # Apply pagination
        paginated_query = query.offset(offset).limit(page_size)

        # Load items if requested
        items = []
        if load_items and total > 0:
            try:
                result = await db.execute(paginated_query)
                items = list(result.scalars().all())
                logger.debug(f"Loaded {len(items)} items for page {page}")
            except SQLAlchemyError as e:
                logger.error(f"Error loading paginated items: {str(e)}", exc_info=True)
                raise DatabaseException(
                    message=f"Failed to load paginated items: {str(e)}",
                    code=ErrorCode.DATABASE_ERROR,
                    original_exception=e,
                ) from e

        logger.debug(
            f"Pagination results: page={page}, page_size={page_size}, "
            f"total={total}, pages={pages}, items_loaded={len(items)}"
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }
    except DatabaseException:
        # Re-raise database exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in pagination: {str(e)}", exc_info=True)
        raise DatabaseException(
            message=f"Pagination failed: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def bulk_create(
    db: AsyncSession,
    model: Type[T],
    objects: List[Dict[str, Any]]
) -> List[T]:
    """Create multiple model instances in a single operation.

    Args:
        db: SQLAlchemy async session object
        model: SQLAlchemy model class
        objects: List of dictionaries with model attribute values

    Returns:
        List[T]: List of created model instances

    Raises:
        DatabaseException: If bulk creation fails
    """
    if not objects:
        logger.debug(f"Empty object list for {model.__name__}, returning empty result")
        return []

    try:
        logger.debug(f"Bulk creating {len(objects)} {model.__name__} instances")
        instances = [model(**obj) for obj in objects]
        db.add_all(instances)
        await db.flush()

        # Refresh instances to get generated values
        for instance in instances:
            await db.refresh(instance)

        logger.info(f"Bulk created {len(instances)} {model.__name__} instances")
        return instances
    except SQLAlchemyError as e:
        logger.error(f"Error bulk creating {model.__name__}: {str(e)}", exc_info=True)

        # Handle unique constraint violations
        if "unique constraint" in str(e).lower() or "unique violation" in str(e).lower():
            raise DataIntegrityException(
                message=f"Bulk create failed: One or more {model.__name__} instances violate uniqueness constraints",
                code=ErrorCode.DATA_INTEGRITY_ERROR,
                original_exception=e,
            ) from e

        raise DatabaseException(
            message=f"Failed to bulk create {model.__name__}: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def bulk_update(
    db: AsyncSession,
    model: Type[T],
    id_field: str,
    objects: List[Dict[str, Any]]
) -> int:
    """Update multiple model instances in a single operation.

    Args:
        db: SQLAlchemy async session object
        model: SQLAlchemy model class
        id_field: Name of the ID field
        objects: List of dictionaries with model attribute values

    Returns:
        int: Number of updated instances

    Raises:
        DatabaseException: If bulk update fails
    """
    if not objects:
        logger.debug(f"Empty object list for {model.__name__}, nothing to update")
        return 0

    try:
        logger.debug(f"Bulk updating {len(objects)} {model.__name__} instances")

        # Extract IDs
        ids = [obj[id_field] for obj in objects if id_field in obj]

        # Load existing objects
        query = select(model).where(getattr(model, id_field).in_(ids))
        result = await db.execute(query)
        instances = {getattr(obj, id_field): obj for obj in result.scalars().all()}

        # Update objects
        updated_count = 0
        for obj_data in objects:
            if id_field not in obj_data:
                logger.warning(f"Skipping update: {id_field} not found in object data")
                continue

            obj_id = obj_data[id_field]
            if obj_id in instances:
                instance = instances[obj_id]
                instance.update_from_dict(obj_data)
                db.add(instance)
                updated_count += 1
            else:
                logger.warning(f"Skipping update: No {model.__name__} found with {id_field}={obj_id}")

        await db.flush()
        logger.info(f"Bulk updated {updated_count} {model.__name__} instances")
        return updated_count
    except SQLAlchemyError as e:
        logger.error(f"Error bulk updating {model.__name__}: {str(e)}", exc_info=True)

        # Handle unique constraint violations
        if "unique constraint" in str(e).lower() or "unique violation" in str(e).lower():
            raise DataIntegrityException(
                message=f"Bulk update failed: One or more {model.__name__} updates violate uniqueness constraints",
                code=ErrorCode.DATA_INTEGRITY_ERROR,
                original_exception=e,
            ) from e

        raise DatabaseException(
            message=f"Failed to bulk update {model.__name__}: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e


async def upsert(
    db: AsyncSession,
    model: Type[T],
    data: Dict[str, Any],
    unique_fields: List[str]
) -> T:
    """Create or update a model instance based on unique fields.

    Args:
        db: SQLAlchemy async session object
        model: SQLAlchemy model class
        data: Dictionary of model attribute values
        unique_fields: List of field names to use for uniqueness check

    Returns:
        T: Created or updated model instance

    Raises:
        DatabaseException: If upsert fails
    """
    try:
        logger.debug(f"Upserting {model.__name__} with data: {data}")

        # Skip if no unique fields
        if not unique_fields:
            logger.warning(f"No unique fields provided for {model.__name__}, creating new instance")
            return await create_object(db, model, data)

        # Build query conditions
        conditions = []
        for field in unique_fields:
            if field in data:
                conditions.append(getattr(model, field) == data[field])
            else:
                logger.warning(f"Unique field {field} not in data, skipping condition")

        if not conditions:
            logger.warning(f"No valid unique field values found, creating new instance")
            return await create_object(db, model, data)

        # Check if instance exists
        query = select(model).where(*conditions)
        result = await db.execute(query)
        existing = result.scalars().first()

        if existing:
            # Update existing
            logger.debug(f"Found existing {model.__name__}, updating")
            existing.update_from_dict(data)
            db.add(existing)
            await db.flush()
            await db.refresh(existing)
            logger.info(f"Updated existing {model.__name__} with ID: {getattr(existing, 'id', None)}")
            return existing
        else:
            # Create new
            logger.debug(f"No existing {model.__name__} found, creating new")
            return await create_object(db, model, data)
    except SQLAlchemyError as e:
        logger.error(f"Error upserting {model.__name__}: {str(e)}", exc_info=True)
        raise DatabaseException(
            message=f"Failed to upsert {model.__name__}: {str(e)}",
            code=ErrorCode.DATABASE_ERROR,
            original_exception=e,
        ) from e
