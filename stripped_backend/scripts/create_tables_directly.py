import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
async def create_tables():
    print('Creating tables directly with SQLAlchemy...')
    engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost/crown_nexus', echo=True)
    try:
        async with engine.begin() as conn:
            print('Dropping all existing tables...')
            await conn.run_sync(Base.metadata.drop_all)
            print('Creating tables from models...')
            await conn.run_sync(Base.metadata.create_all)
        print('✅ Tables created successfully!')
        print('\nCreated the following tables:')
        for table in Base.metadata.tables:
            print(f'  - {table}')
    finally:
        await engine.dispose()
if __name__ == '__main__':
    asyncio.run(create_tables())