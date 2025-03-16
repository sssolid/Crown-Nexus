# app/db/utils.py
from __future__ import annotations

import contextlib
import functools
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Sequence, Type, TypeVar, Union, cast, overload

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import Delete, Insert, Update

from app.core.exceptions import DatabaseException
from app.core.logging import get_logger
from app.db.base_class import Base

logger = get_logger("app.db.utils")

T = TypeVar("T", bound=Base)
F = TypeVar("F", bound=Callable[..., Any])


@contextlib.asynccontextmanager
async def transaction(db: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """Context manager for database transactions.
    
    This ensures that operations within the context are committed together
    or rolled back on error, simplifying transaction management.
    
    Args:
        db: Database session
        
    Yields:
        AsyncSession: Database session with transaction
        
    Raises:
        DatabaseException: If a database error occurs
    """
    if db.in_transaction():
        # Already in a transaction, just yield
        yield db
        return
    
    # Start a new transaction
    async with db.begin():
        try:
            yield db
        except SQLAlchemyError as e:
            # Log the error and re-raise as DatabaseException
            logger.error(f"Transaction error: {str(e)}")
            raise DatabaseException(
                message=f"Database transaction failed: {str(e)}",
            ) from e


def transactional(func: F) -> F:
    """Decorator for managing transactions in service methods.
    
    Ensures the method runs within a transaction and properly handles errors.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function with transaction management
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Find the db session in the arguments
        db = None
        for arg in args:
            if isinstance(arg, AsyncSession):
                db = arg
                break
        
        if db is None:
            db = kwargs.get("db")
            
        if db is None:
            raise ValueError("No database session provided to transactional method")
            
        async with transaction(db):
            return await func(*args, **kwargs)
            
    return cast(F, wrapper)


async def execute_query(db: AsyncSession, query: Union[Select, Insert, Update, Delete]) -> Any:
    """Execute a SQLAlchemy query with error handling.
    
    Args:
        db: Database session
        query: SQLAlchemy query to execute
        
    Returns:
        Any: Query result
        
    Raises:
        DatabaseException: If a database error occurs
    """
    try:
        result = await db.execute(query)
        return result
    except SQLAlchemyError as e:
        logger.error(f"Query execution error: {str(e)}")
        raise DatabaseException(
            message=f"Query execution failed: {str(e)}",
        ) from e


async def get_by_id(db: AsyncSession, model: Type[T], id_value: Any) -> Optional[T]:
    """Get a model instance by ID with proper error handling.
    
    Args:
        db: Database session
        model: Model class
        id_value: ID value to look up
        
    Returns:
        Optional[T]: Found instance or None
        
    Raises:
        DatabaseException: If a database error occurs
    """
    try:
        query = model.filter_by_id(id_value)
        result = await db.execute(query)
        return result.scalars().first()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching {model.__name__} by ID: {str(e)}")
        raise DatabaseException(
            message=f"Failed to fetch {model.__name__} by ID: {str(e)}",
        ) from e


async def get_by_ids(db: AsyncSession, model: Type[T], ids: List[Any]) -> List[T]:
    """Get multiple model instances by their IDs.
    
    Args:
        db: Database session
        model: Model class
        ids: List of IDs to look up
        
    Returns:
        List[T]: List of found instances
        
    Raises:
        DatabaseException: If a database error occurs
    """
    if not ids:
        return []
        
    try:
        query = select(model).where(
            model.id.in_(ids),
            model.is_deleted == False
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    except SQLAlchemyError as e:
        logger.error(f"Error fetching {model.__name__} by IDs: {str(e)}")
        raise DatabaseException(
            message=f"Failed to fetch {model.__name__} by IDs: {str(e)}",
        ) from e


async def create_object(db: AsyncSession, model: Type[T], obj_in: Dict[str, Any]) -> T:
    """Create a new model instance.
    
    Args:
        db: Database session
        model: Model class
        obj_in: Object data
        
    Returns:
        T: Created instance
        
    Raises:
        DatabaseException: If a database error occurs
    """
    try:
        db_obj = model(**obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError as e:
        logger.error(f"Error creating {model.__name__}: {str(e)}")
        raise DatabaseException(
            message=f"Failed to create {model.__name__}: {str(e)}",
        ) from e


async def update_object(
    db: AsyncSession, 
    model: Type[T], 
    id_value: Any, 
    obj_in: Dict[str, Any],
    user_id: Optional[Any] = None,
) -> Optional[T]:
    """Update a model instance by ID.
    
    Args:
        db: Database session
        model: Model class
        id_value: ID value to look up
        obj_in: New data to update
        user_id: ID of the user making the update
        
    Returns:
        Optional[T]: Updated instance or None if not found
        
    Raises:
        DatabaseException: If a database error occurs
    """
    try:
        db_obj = await get_by_id(db, model, id_value)
        if not db_obj:
            return None
            
        # Add audit info
        if user_id is not None:
            obj_in["updated_by_id"] = user_id
            
        db_obj.update_from_dict(obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError as e:
        logger.error(f"Error updating {model.__name__}: {str(e)}")
        raise DatabaseException(
            message=f"Failed to update {model.__name__}: {str(e)}",
        ) from e


async def delete_object(
    db: AsyncSession, 
    model: Type[T], 
    id_value: Any,
    user_id: Optional[Any] = None,
    hard_delete: bool = False,
) -> bool:
    """Delete a model instance by ID.
    
    By default, performs a soft delete unless hard_delete is True.
    
    Args:
        db: Database session
        model: Model class
        id_value: ID value to look up
        user_id: ID of the user performing the deletion
        hard_delete: Whether to permanently delete the record
        
    Returns:
        bool: True if deleted, False if not found
        
    Raises:
        DatabaseException: If a database error occurs
    """
    try:
        db_obj = await get_by_id(db, model, id_value)
        if not db_obj:
            return False
            
        if hard_delete:
            await db.delete(db_obj)
        else:
            db_obj.soft_delete(user_id)
            db.add(db_obj)
            
        await db.flush()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error deleting {model.__name__}: {str(e)}")
        raise DatabaseException(
            message=f"Failed to delete {model.__name__}: {str(e)}",
        ) from e


async def count_query(db: AsyncSession, query: Select) -> int:
    """Count results of a query.
    
    Args:
        db: Database session
        query: Base query
        
    Returns:
        int: Count of matching records
        
    Raises:
        DatabaseException: If a database error occurs
    """
    try:
        # Create a count query by selecting count() from the original query
        count_query = select(func.count()).select_from(query.subquery())
        result = await db.execute(count_query)
        return result.scalar() or 0
    except SQLAlchemyError as e:
        logger.error(f"Error counting query results: {str(e)}")
        raise DatabaseException(
            message=f"Failed to count query results: {str(e)}",
        ) from e


async def paginate(
    db: AsyncSession, 
    query: Select, 
    page: int = 1, 
    page_size: int = 20,
    load_items: bool = True,
) -> Dict[str, Any]:
    """Paginate a query.
    
    Args:
        db: Database session
        query: Base query
        page: Page number (1-indexed)
        page_size: Number of items per page
        load_items: Whether to load the items or just return metadata
        
    Returns:
        Dict[str, Any]: Pagination result with items, total, page, page_size, and pages
        
    Raises:
        DatabaseException: If a database error occurs
    """
    # Validate pagination parameters
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 20
    if page_size > 100:
        page_size = 100
        
    # Calculate total count
    total = await count_query(db, query)
    
    # Calculate pagination metadata
    pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    if page > pages and pages > 0:
        page = pages
        
    # Apply pagination to query
    offset = (page - 1) * page_size
    paginated_query = query.offset(offset).limit(page_size)
    
    # Load items if requested
    items = []
    if load_items and total > 0:
        try:
            result = await db.execute(paginated_query)
            items = list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error loading paginated items: {str(e)}")
            raise DatabaseException(
                message=f"Failed to load paginated items: {str(e)}",
            ) from e
    
    # Return pagination result
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }


async def bulk_create(
    db: AsyncSession,
    model: Type[T],
    objects: List[Dict[str, Any]],
) -> List[T]:
    """Create multiple model instances in a single transaction.
    
    Args:
        db: Database session
        model: Model class
        objects: List of object data
        
    Returns:
        List[T]: List of created instances
        
    Raises:
        DatabaseException: If a database error occurs
    """
    if not objects:
        return []
        
    try:
        # Create instances
        instances = [model(**obj) for obj in objects]
        
        # Add all instances to the session
        db.add_all(instances)
        await db.flush()
        
        # Refresh all instances
        for instance in instances:
            await db.refresh(instance)
            
        return instances
    except SQLAlchemyError as e:
        logger.error(f"Error bulk creating {model.__name__}: {str(e)}")
        raise DatabaseException(
            message=f"Failed to bulk create {model.__name__}: {str(e)}",
        ) from e


async def bulk_update(
    db: AsyncSession,
    model: Type[T],
    id_field: str,
    objects: List[Dict[str, Any]],
) -> int:
    """Update multiple model instances in a single transaction.
    
    Args:
        db: Database session
        model: Model class
        id_field: Field name to use for identifying records (usually 'id')
        objects: List of object data (must include id_field)
        
    Returns:
        int: Number of updated instances
        
    Raises:
        DatabaseException: If a database error occurs
    """
    if not objects:
        return 0
        
    try:
        # Get all IDs to update
        ids = [obj[id_field] for obj in objects if id_field in obj]
        
        # Get existing instances
        query = select(model).where(getattr(model, id_field).in_(ids))
        result = await db.execute(query)
        instances = {getattr(obj, id_field): obj for obj in result.scalars().all()}
        
        # Update instances
        updated_count = 0
        for obj_data in objects:
            if id_field not in obj_data:
                continue
                
            obj_id = obj_data[id_field]
            if obj_id in instances:
                instance = instances[obj_id]
                instance.update_from_dict(obj_data)
                db.add(instance)
                updated_count += 1
                
        await db.flush()
        return updated_count
    except SQLAlchemyError as e:
        logger.error(f"Error bulk updating {model.__name__}: {str(e)}")
        raise DatabaseException(
            message=f"Failed to bulk update {model.__name__}: {str(e)}",
        ) from e


async def upsert(
    db: AsyncSession,
    model: Type[T],
    data: Dict[str, Any],
    unique_fields: List[str],
) -> T:
    """Insert a record or update it if it already exists.
    
    Args:
        db: Database session
        model: Model class
        data: Object data
        unique_fields: Fields to use for uniqueness check
        
    Returns:
        T: Created or updated instance
        
    Raises:
        DatabaseException: If a database error occurs
    """
    try:
        # Build query to check for existing record
        conditions = []
        for field in unique_fields:
            if field in data:
                conditions.append(getattr(model, field) == data[field])
        
        if not conditions:
            # No unique fields provided in data, just create
            return await create_object(db, model, data)
        
        # Check for existing record
        query = select(model).where(*conditions)
        result = await db.execute(query)
        existing = result.scalars().first()
        
        if existing:
            # Update existing record
            existing.update_from_dict(data)
            db.add(existing)
            await db.flush()
            await db.refresh(existing)
            return existing
        else:
            # Create new record
            return await create_object(db, model, data)
    except SQLAlchemyError as e:
        logger.error(f"Error upserting {model.__name__}: {str(e)}")
        raise DatabaseException(
            message=f"Failed to upsert {model.__name__}: {str(e)}",
        ) from e
