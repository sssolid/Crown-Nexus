from __future__ import annotations
import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path
from typing import Optional
from alembic import context
from sqlalchemy import engine_from_config, pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.config import settings
from app.db.base import Base
config = context.config
db_url = str(settings.SQLALCHEMY_DATABASE_URI)
config.set_section_option(config.config_ini_section, 'sqlalchemy.url', db_url)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
target_metadata = Base.metadata
def run_migrations_offline() -> None:
    url: str = config.get_main_option('sqlalchemy.url')
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={'paramstyle': 'named'})
    with context.begin_transaction():
        context.run_migrations()
def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()
async def run_migrations_online() -> None:
    print('Attempting to connect to database...')
    print(f'Database URL: {db_url}')
    table_names = [table.name for table in target_metadata.tables.values()]
    print(f'Models to migrate: {table_names}')
    engine_config = config.get_section(config.config_ini_section)
    if not engine_config:
        raise ValueError('Could not find SQLAlchemy configuration section')
    connectable = AsyncEngine(engine_from_config(engine_config, prefix='sqlalchemy.', poolclass=pool.NullPool, future=True))
    try:
        async with connectable.connect() as connection:
            await connection.execute(text('SELECT 1'))
            print('✅ Database connection successful!')
            await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(f'❌ Migration failed: {e}')
        import traceback
        traceback.print_exc()
        raise
    finally:
        await connectable.dispose()
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())