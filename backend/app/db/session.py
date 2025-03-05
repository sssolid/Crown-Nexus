from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=False)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
