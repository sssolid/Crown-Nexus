from __future__ import annotations
import contextlib
from typing import AsyncGenerator, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=False, future=True, pool_pre_ping=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, autoflush=False)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
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