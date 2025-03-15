from __future__ import annotations
import contextlib
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Sequence, Type, TypeVar
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Delete, Insert, Select, Update
from app.db.base_class import Base
T = TypeVar('T', bound=Base)
async def get_by_id(db: AsyncSession, model: Type[T], id: Any) -> Optional[T]:
    result = await db.execute(select(model).where(model.id == id))
    return result.scalar_one_or_none()
async def create_object(db: AsyncSession, model: Type[T], obj_in: Dict[str, Any]) -> T:
    db_obj = model(**obj_in)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
async def update_object(db: AsyncSession, model: Type[T], id: Any, obj_in: Dict[str, Any]) -> Optional[T]:
    db_obj = await get_by_id(db, model, id)
    if db_obj is None:
        return None
    for field, value in obj_in.items():
        setattr(db_obj, field, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
async def delete_object(db: AsyncSession, model: Type[T], id: Any) -> bool:
    db_obj = await get_by_id(db, model, id)
    if db_obj is None:
        return False
    await db.delete(db_obj)
    await db.commit()
    return True
async def bulk_create(db: AsyncSession, model: Type[T], objects: List[Dict[str, Any]]) -> List[T]:
    instances = [model(**obj) for obj in objects]
    db.add_all(instances)
    await db.commit()
    for instance in instances:
        await db.refresh(instance)
    return instances
async def execute_query(db: AsyncSession, query: Select | Update | Delete | Insert) -> Any:
    result = await db.execute(query)
    return result
@contextlib.asynccontextmanager
async def transaction(db: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    try:
        yield db
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise
async def paginate(db: AsyncSession, query: Select, page: int=1, page_size: int=20) -> Dict[str, Any]:
    page = max(1, page)
    page_size = max(1, min(100, page_size))
    skip = (page - 1) * page_size
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0
    paginated_query = query.offset(skip).limit(page_size)
    result = await db.execute(paginated_query)
    items = result.scalars().all()
    pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return {'items': items, 'total': total, 'page': page, 'page_size': page_size, 'pages': pages}