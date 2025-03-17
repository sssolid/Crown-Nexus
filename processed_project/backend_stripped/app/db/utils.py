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
logger = get_logger('app.db.utils')
T = TypeVar('T', bound=Base)
F = TypeVar('F', bound=Callable[..., Any])
@contextlib.asynccontextmanager
async def transaction(db: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    if db.in_transaction():
        yield db
        return
    async with db.begin():
        try:
            yield db
        except SQLAlchemyError as e:
            logger.error(f'Transaction error: {str(e)}')
            raise DatabaseException(message=f'Database transaction failed: {str(e)}') from e
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
            raise ValueError('No database session provided to transactional method')
        async with transaction(db):
            return await func(*args, **kwargs)
    return cast(F, wrapper)
async def execute_query(db: AsyncSession, query: Union[Select, Insert, Update, Delete]) -> Any:
    try:
        result = await db.execute(query)
        return result
    except SQLAlchemyError as e:
        logger.error(f'Query execution error: {str(e)}')
        raise DatabaseException(message=f'Query execution failed: {str(e)}') from e
async def get_by_id(db: AsyncSession, model: Type[T], id_value: Any) -> Optional[T]:
    try:
        query = model.filter_by_id(id_value)
        result = await db.execute(query)
        return result.scalars().first()
    except SQLAlchemyError as e:
        logger.error(f'Error fetching {model.__name__} by ID: {str(e)}')
        raise DatabaseException(message=f'Failed to fetch {model.__name__} by ID: {str(e)}') from e
async def get_by_ids(db: AsyncSession, model: Type[T], ids: List[Any]) -> List[T]:
    if not ids:
        return []
    try:
        query = select(model).where(model.id.in_(ids), model.is_deleted == False)
        result = await db.execute(query)
        return list(result.scalars().all())
    except SQLAlchemyError as e:
        logger.error(f'Error fetching {model.__name__} by IDs: {str(e)}')
        raise DatabaseException(message=f'Failed to fetch {model.__name__} by IDs: {str(e)}') from e
async def create_object(db: AsyncSession, model: Type[T], obj_in: Dict[str, Any]) -> T:
    try:
        db_obj = model(**obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError as e:
        logger.error(f'Error creating {model.__name__}: {str(e)}')
        raise DatabaseException(message=f'Failed to create {model.__name__}: {str(e)}') from e
async def update_object(db: AsyncSession, model: Type[T], id_value: Any, obj_in: Dict[str, Any], user_id: Optional[Any]=None) -> Optional[T]:
    try:
        db_obj = await get_by_id(db, model, id_value)
        if not db_obj:
            return None
        if user_id is not None:
            obj_in['updated_by_id'] = user_id
        db_obj.update_from_dict(obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError as e:
        logger.error(f'Error updating {model.__name__}: {str(e)}')
        raise DatabaseException(message=f'Failed to update {model.__name__}: {str(e)}') from e
async def delete_object(db: AsyncSession, model: Type[T], id_value: Any, user_id: Optional[Any]=None, hard_delete: bool=False) -> bool:
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
        logger.error(f'Error deleting {model.__name__}: {str(e)}')
        raise DatabaseException(message=f'Failed to delete {model.__name__}: {str(e)}') from e
async def count_query(db: AsyncSession, query: Select) -> int:
    try:
        count_query = select(func.count()).select_from(query.subquery())
        result = await db.execute(count_query)
        return result.scalar() or 0
    except SQLAlchemyError as e:
        logger.error(f'Error counting query results: {str(e)}')
        raise DatabaseException(message=f'Failed to count query results: {str(e)}') from e
async def paginate(db: AsyncSession, query: Select, page: int=1, page_size: int=20, load_items: bool=True) -> Dict[str, Any]:
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 20
    if page_size > 100:
        page_size = 100
    total = await count_query(db, query)
    pages = (total + page_size - 1) // page_size if total > 0 else 0
    if page > pages and pages > 0:
        page = pages
    offset = (page - 1) * page_size
    paginated_query = query.offset(offset).limit(page_size)
    items = []
    if load_items and total > 0:
        try:
            result = await db.execute(paginated_query)
            items = list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f'Error loading paginated items: {str(e)}')
            raise DatabaseException(message=f'Failed to load paginated items: {str(e)}') from e
    return {'items': items, 'total': total, 'page': page, 'page_size': page_size, 'pages': pages}
async def bulk_create(db: AsyncSession, model: Type[T], objects: List[Dict[str, Any]]) -> List[T]:
    if not objects:
        return []
    try:
        instances = [model(**obj) for obj in objects]
        db.add_all(instances)
        await db.flush()
        for instance in instances:
            await db.refresh(instance)
        return instances
    except SQLAlchemyError as e:
        logger.error(f'Error bulk creating {model.__name__}: {str(e)}')
        raise DatabaseException(message=f'Failed to bulk create {model.__name__}: {str(e)}') from e
async def bulk_update(db: AsyncSession, model: Type[T], id_field: str, objects: List[Dict[str, Any]]) -> int:
    if not objects:
        return 0
    try:
        ids = [obj[id_field] for obj in objects if id_field in obj]
        query = select(model).where(getattr(model, id_field).in_(ids))
        result = await db.execute(query)
        instances = {getattr(obj, id_field): obj for obj in result.scalars().all()}
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
        logger.error(f'Error bulk updating {model.__name__}: {str(e)}')
        raise DatabaseException(message=f'Failed to bulk update {model.__name__}: {str(e)}') from e
async def upsert(db: AsyncSession, model: Type[T], data: Dict[str, Any], unique_fields: List[str]) -> T:
    try:
        conditions = []
        for field in unique_fields:
            if field in data:
                conditions.append(getattr(model, field) == data[field])
        if not conditions:
            return await create_object(db, model, data)
        query = select(model).where(*conditions)
        result = await db.execute(query)
        existing = result.scalars().first()
        if existing:
            existing.update_from_dict(data)
            db.add(existing)
            await db.flush()
            await db.refresh(existing)
            return existing
        else:
            return await create_object(db, model, data)
    except SQLAlchemyError as e:
        logger.error(f'Error upserting {model.__name__}: {str(e)}')
        raise DatabaseException(message=f'Failed to upsert {model.__name__}: {str(e)}') from e