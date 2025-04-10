from __future__ import annotations
"Database utilities for SQLAlchemy operations.\n\nThis module provides a comprehensive set of utilities for working with database\noperations in an async SQLAlchemy environment. It includes:\n- Transaction management\n- Common CRUD operations\n- Pagination\n- Bulk operations\n- Query execution and error handling\n- Performance metrics collection\n\nThe utilities are designed to work with the application's custom Base model class\nand provide consistent error handling and logging.\n"
import asyncio
import contextlib
import functools
import time
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Type, TypeVar, Union, cast
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import Delete, Insert, Update
from app.core.dependency_manager import get_dependency
from app.core.exceptions import DataIntegrityException, DatabaseException, ErrorCode, TransactionException
from app.logging import get_logger
from app.db.base_class import Base
logger = get_logger('app.db.utils')
T = TypeVar('T', bound=Base)
F = TypeVar('F', bound=Callable[..., Any])
@contextlib.asynccontextmanager
async def transaction(db: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    if db.in_transaction():
        yield db
        return
    try:
        async with db.begin():
            logger.debug('Transaction started')
            yield db
            logger.debug('Transaction committed')
    except SQLAlchemyError as e:
        logger.error(f'Transaction error: {str(e)}', exc_info=True)
        raise TransactionException(message=f'Database transaction failed: {str(e)}', original_exception=e) from e
    except Exception as e:
        logger.error(f'Unexpected error in transaction: {str(e)}', exc_info=True)
        raise TransactionException(message=f'Unexpected error in transaction: {str(e)}', original_exception=e) from e
def transactional(func: F) -> F:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        db = None
        for arg in args:
            if isinstance(arg, AsyncSession):
                db = arg
                break
        if db is None:
            db = kwargs.get('db')
        if db is None:
            logger.error('No database session provided to transactional method')
            raise ValueError('No database session provided to transactional method')
        async with transaction(db):
            return await func(*args, **kwargs)
    return cast(F, wrapper)
async def execute_query(db: AsyncSession, query: Union[Select, Insert, Update, Delete]) -> Any:
    try:
        logger.debug(f'Executing query: {query}')
        start_time = time.time()
        result = await db.execute(query)
        duration = time.time() - start_time
        if duration > 1.0:
            logger.warning(f'Slow query took {duration:.2f}s: {query}')
        elif duration > 0.1:
            logger.info(f'Query took {duration:.2f}s: {query}')
        else:
            logger.debug(f'Query completed in {duration:.4f}s')
        return result
    except SQLAlchemyError as e:
        logger.error(f'Query execution error: {str(e)}', exc_info=True)
        raise DatabaseException(message=f'Query execution failed: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def get_by_id(db: AsyncSession, model: Type[T], id_value: Any) -> Optional[T]:
    try:
        logger.debug(f'Getting {model.__name__} by ID: {id_value}')
        query = model.filter_by_id(id_value)
        result = await db.execute(query)
        instance = result.scalars().first()
        if instance:
            logger.debug(f'Found {model.__name__} with ID: {id_value}')
        else:
            logger.debug(f'No {model.__name__} found with ID: {id_value}')
        return instance
    except SQLAlchemyError as e:
        logger.error(f'Error fetching {model.__name__} by ID: {str(e)}', exc_info=True)
        raise DatabaseException(message=f'Failed to fetch {model.__name__} by ID: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def get_by_ids(db: AsyncSession, model: Type[T], ids: List[Any]) -> List[T]:
    if not ids:
        logger.debug(f'Empty ID list for {model.__name__}, returning empty result')
        return []
    try:
        logger.debug(f'Getting {model.__name__} by IDs: {ids}')
        query = select(model).where(model.id.in_(ids), model.is_deleted == False)
        result = await db.execute(query)
        instances = list(result.scalars().all())
        logger.debug(f'Found {len(instances)} {model.__name__} instances')
        return instances
    except SQLAlchemyError as e:
        logger.error(f'Error fetching {model.__name__} by IDs: {str(e)}', exc_info=True)
        raise DatabaseException(message=f'Failed to fetch {model.__name__} by IDs: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def create_object(db: AsyncSession, model: Type[T], obj_in: Dict[str, Any]) -> T:
    try:
        logger.debug(f'Creating {model.__name__}: {obj_in}')
        db_obj = model(**obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        logger.info(f"Created {model.__name__} with ID: {getattr(db_obj, 'id', None)}")
        return db_obj
    except SQLAlchemyError as e:
        logger.error(f'Error creating {model.__name__}: {str(e)}', exc_info=True)
        error_text = str(e).lower()
        if 'unique constraint' in error_text or 'unique violation' in error_text:
            raise DataIntegrityException(message=f'Failed to create {model.__name__}: A record with these attributes already exists', original_exception=e) from e
        raise DatabaseException(message=f'Failed to create {model.__name__}: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def update_object(db: AsyncSession, model: Type[T], id_value: Any, obj_in: Dict[str, Any], user_id: Optional[Any]=None) -> Optional[T]:
    try:
        logger.debug(f'Updating {model.__name__} with ID: {id_value}')
        db_obj = await get_by_id(db, model, id_value)
        if not db_obj:
            logger.warning(f'Update failed: No {model.__name__} found with ID: {id_value}')
            return None
        if user_id is not None:
            obj_in['updated_by_id'] = user_id
        db_obj.update_from_dict(obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        logger.info(f'Updated {model.__name__} with ID: {id_value}')
        return db_obj
    except SQLAlchemyError as e:
        logger.error(f'Error updating {model.__name__}: {str(e)}', exc_info=True)
        error_text = str(e).lower()
        if 'unique constraint' in error_text or 'unique violation' in error_text:
            raise DataIntegrityException(message=f'Cannot update {model.__name__}: A record with these attributes already exists', original_exception=e) from e
        raise DatabaseException(message=f'Failed to update {model.__name__}: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def delete_object(db: AsyncSession, model: Type[T], id_value: Any, user_id: Optional[Any]=None, hard_delete: bool=False) -> bool:
    try:
        logger.debug(f'Deleting {model.__name__} with ID: {id_value} (hard_delete={hard_delete})')
        db_obj = await get_by_id(db, model, id_value)
        if not db_obj:
            logger.warning(f'Delete failed: No {model.__name__} found with ID: {id_value}')
            return False
        if hard_delete:
            await db.delete(db_obj)
            logger.info(f'Hard deleted {model.__name__} with ID: {id_value}')
        else:
            db_obj.soft_delete(user_id)
            db.add(db_obj)
            logger.info(f'Soft deleted {model.__name__} with ID: {id_value}')
        await db.flush()
        return True
    except SQLAlchemyError as e:
        logger.error(f'Error deleting {model.__name__}: {str(e)}', exc_info=True)
        error_text = str(e).lower()
        if 'foreign key constraint' in error_text:
            raise DataIntegrityException(message=f'Cannot delete {model.__name__}: It is referenced by other records', original_exception=e) from e
        raise DatabaseException(message=f'Failed to delete {model.__name__}: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def count_query(db: AsyncSession, query: Select) -> int:
    try:
        count_query = select(func.count()).select_from(query.subquery())
        result = await db.execute(count_query)
        count = result.scalar() or 0
        logger.debug(f'Query count result: {count}')
        return count
    except SQLAlchemyError as e:
        logger.error(f'Error counting query results: {str(e)}', exc_info=True)
        raise DatabaseException(message=f'Failed to count query results: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def paginate(db: AsyncSession, query: Select, page: int=1, page_size: int=20, load_items: bool=True) -> Dict[str, Any]:
    if page < 1:
        logger.warning(f'Invalid page number: {page}, using page 1')
        page = 1
    if page_size < 1:
        logger.warning(f'Invalid page size: {page_size}, using page size 20')
        page_size = 20
    if page_size > 100:
        logger.warning(f'Page size too large: {page_size}, using maximum 100')
        page_size = 100
    try:
        total = await count_query(db, query)
        pages = (total + page_size - 1) // page_size if total > 0 else 0
        if page > pages and pages > 0:
            logger.warning(f'Page {page} out of range, using page {pages}')
            page = pages
        offset = (page - 1) * page_size
        items = []
        if load_items and total > 0:
            try:
                paginated_query = query.offset(offset).limit(page_size)
                result = await db.execute(paginated_query)
                items = list(result.scalars().all())
                logger.debug(f'Loaded {len(items)} items for page {page}')
            except SQLAlchemyError as e:
                logger.error(f'Error loading paginated items: {str(e)}', exc_info=True)
                raise DatabaseException(message=f'Failed to load paginated items: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
        logger.debug(f'Pagination results: page={page}, page_size={page_size}, total={total}, pages={pages}, items_loaded={len(items)}')
        return {'items': items, 'total': total, 'page': page, 'page_size': page_size, 'pages': pages}
    except DatabaseException:
        raise
    except Exception as e:
        logger.error(f'Unexpected error in pagination: {str(e)}', exc_info=True)
        raise DatabaseException(message=f'Pagination failed: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def bulk_create(db: AsyncSession, model: Type[T], objects: List[Dict[str, Any]]) -> List[T]:
    if not objects:
        logger.debug(f'Empty object list for {model.__name__}, returning empty result')
        return []
    try:
        logger.debug(f'Bulk creating {len(objects)} {model.__name__} instances')
        instances = [model(**obj) for obj in objects]
        db.add_all(instances)
        await db.flush()
        for instance in instances:
            await db.refresh(instance)
        logger.info(f'Bulk created {len(instances)} {model.__name__} instances')
        return instances
    except SQLAlchemyError as e:
        logger.error(f'Error bulk creating {model.__name__}: {str(e)}', exc_info=True)
        error_text = str(e).lower()
        if 'unique constraint' in error_text or 'unique violation' in error_text:
            raise DataIntegrityException(message=f'Bulk create failed: One or more {model.__name__} instances violate uniqueness constraints', original_exception=e) from e
        raise DatabaseException(message=f'Failed to bulk create {model.__name__}: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def bulk_update(db: AsyncSession, model: Type[T], id_field: str, objects: List[Dict[str, Any]]) -> int:
    if not objects:
        logger.debug(f'Empty object list for {model.__name__}, nothing to update')
        return 0
    try:
        logger.debug(f'Bulk updating {len(objects)} {model.__name__} instances')
        ids = [obj[id_field] for obj in objects if id_field in obj]
        query = select(model).where(getattr(model, id_field).in_(ids))
        result = await db.execute(query)
        instances = {getattr(obj, id_field): obj for obj in result.scalars().all()}
        updated_count = 0
        for obj_data in objects:
            if id_field not in obj_data:
                logger.warning(f'Skipping update: {id_field} not found in object data')
                continue
            obj_id = obj_data[id_field]
            if obj_id in instances:
                instance = instances[obj_id]
                instance.update_from_dict(obj_data)
                db.add(instance)
                updated_count += 1
            else:
                logger.warning(f'Skipping update: No {model.__name__} found with {id_field}={obj_id}')
        await db.flush()
        logger.info(f'Bulk updated {updated_count} {model.__name__} instances')
        return updated_count
    except SQLAlchemyError as e:
        logger.error(f'Error bulk updating {model.__name__}: {str(e)}', exc_info=True)
        error_text = str(e).lower()
        if 'unique constraint' in error_text or 'unique violation' in error_text:
            raise DataIntegrityException(message=f'Bulk update failed: One or more {model.__name__} updates violate uniqueness constraints', original_exception=e) from e
        raise DatabaseException(message=f'Failed to bulk update {model.__name__}: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
async def upsert(db: AsyncSession, model: Type[T], data: Dict[str, Any], unique_fields: List[str]) -> T:
    try:
        logger.debug(f'Upserting {model.__name__} with data: {data}')
        if not unique_fields:
            logger.warning(f'No unique fields provided for {model.__name__}, creating new instance')
            return await create_object(db, model, data)
        conditions = []
        for field in unique_fields:
            if field in data:
                conditions.append(getattr(model, field) == data[field])
            else:
                logger.warning(f'Unique field {field} not in data, skipping condition')
        if not conditions:
            logger.warning(f'No valid unique field values found, creating new instance')
            return await create_object(db, model, data)
        query = select(model).where(*conditions)
        result = await db.execute(query)
        existing = result.scalars().first()
        if existing:
            logger.debug(f'Found existing {model.__name__}, updating')
            existing.update_from_dict(data)
            db.add(existing)
            await db.flush()
            await db.refresh(existing)
            logger.info(f"Updated existing {model.__name__} with ID: {getattr(existing, 'id', None)}")
            return existing
        else:
            logger.debug(f'No existing {model.__name__} found, creating new')
            return await create_object(db, model, data)
    except SQLAlchemyError as e:
        logger.error(f'Error upserting {model.__name__}: {str(e)}', exc_info=True)
        raise DatabaseException(message=f'Failed to upsert {model.__name__}: {str(e)}', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
def track_db_query(operation: str, entity: Optional[str]=None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        is_async = asyncio.iscoroutinefunction(func)
        if is_async:
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service: Optional[Any] = None
                try:
                    metrics_service = get_dependency('metrics_service')
                except Exception as e:
                    logger.debug(f'Could not get metrics service: {str(e)}')
                entity_name = entity
                if not entity_name:
                    for arg in args:
                        if hasattr(arg, '__tablename__'):
                            entity_name = getattr(arg, '__tablename__')
                            break
                    if not entity_name:
                        for _, val in kwargs.items():
                            if hasattr(val, '__tablename__'):
                                entity_name = getattr(val, '__tablename__')
                                break
                entity_name = entity_name or 'unknown'
                start_time = time.monotonic()
                error = None
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    error = type(e).__name__
                    raise
                finally:
                    duration = time.monotonic() - start_time
                    if metrics_service:
                        metrics_service.track_db_query(operation=operation, entity=entity_name, duration=duration, error=error)
            return cast(F, async_wrapper)
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                metrics_service: Optional[Any] = None
                try:
                    metrics_service = get_dependency('metrics_service')
                except Exception as e:
                    logger.debug(f'Could not get metrics service: {str(e)}')
                entity_name = entity
                if not entity_name:
                    for arg in args:
                        if hasattr(arg, '__tablename__'):
                            entity_name = getattr(arg, '__tablename__')
                            break
                    if not entity_name:
                        for _, val in kwargs.items():
                            if hasattr(val, '__tablename__'):
                                entity_name = getattr(val, '__tablename__')
                                break
                entity_name = entity_name or 'unknown'
                start_time = time.monotonic()
                error = None
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error = type(e).__name__
                    raise
                finally:
                    duration = time.monotonic() - start_time
                    if metrics_service:
                        metrics_service.track_db_query(operation=operation, entity=entity_name, duration=duration, error=error)
            return cast(F, sync_wrapper)
    return decorator
def track_db_transaction() -> Callable[[F], F]:
    return track_db_query(operation='TRANSACTION', entity='transaction')
def track_db_select(entity: Optional[str]=None) -> Callable[[F], F]:
    return track_db_query(operation='SELECT', entity=entity)
def track_db_insert(entity: Optional[str]=None) -> Callable[[F], F]:
    return track_db_query(operation='INSERT', entity=entity)
def track_db_update(entity: Optional[str]=None) -> Callable[[F], F]:
    return track_db_query(operation='UPDATE', entity=entity)
def track_db_delete(entity: Optional[str]=None) -> Callable[[F], F]:
    return track_db_query(operation='DELETE', entity=entity)