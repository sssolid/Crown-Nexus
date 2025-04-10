from __future__ import annotations
import asyncio
import os
import sys
from logging.config import fileConfig
from pathlib import Path
from alembic import context
from sqlalchemy import engine_from_config, pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.config import settings
from app.db import base
config = context.config
db_url = str(settings.SQLALCHEMY_DATABASE_URI).replace('postgresql+asyncpg://', 'postgresql://')
config.set_section_option(config.config_ini_section, 'sqlalchemy.url', db_url)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
target_metadata = base.Base.metadata
def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, include_schemas=True, dialect_opts={'paramstyle': 'named'}, version_table_schema='public')
    with context.begin_transaction():
        context.run_migrations()
def do_run_migrations(connection: Connection) -> None:
    print(f'Number of tables in metadata: {len(target_metadata.tables)}')
    context.configure(connection=connection, target_metadata=target_metadata, include_schemas=True, compare_type=True, version_table_schema='public')
    with context.begin_transaction():
        context.run_migrations()
        print('Migrations executed successfully within transaction')
def run_migrations_online() -> None:
    print('Attempting to connect to database...')
    print(f'Database URL: {db_url}')
    table_names = [table.name for table in target_metadata.tables.values()]
    print(f'Models to migrate: {table_names[:10]}...')
    engine_config = config.get_section(config.config_ini_section)
    if not engine_config:
        raise ValueError('Could not find SQLAlchemy configuration section')
    connectable = engine_from_config(engine_config, prefix='sqlalchemy.', poolclass=pool.NullPool)
    with connectable.connect() as connection:
        from app.core.config import settings
        for schema in settings.DB_SCHEMAS:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        context.configure(connection=connection, target_metadata=target_metadata, include_schemas=True, compare_type=True, version_table_schema='public')
        result = connection.execute(text('SELECT 1'))
        print('Database connection successful!')
        result = connection.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        existing_tables = [row[0] for row in result]
        print(f'Existing tables before migration: {len(existing_tables)}')
        do_run_migrations(connection)
        result = connection.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        tables_after = [row[0] for row in result]
        print(f'Tables after migration: {len(tables_after)}')
        new_tables = set(tables_after) - set(existing_tables)
        print(f'Newly created tables: {len(new_tables)}')
        connection.commit()
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()