# backend/alembic/env.py
"""
Alembic environment configuration.

This module configures the Alembic environment for database migrations.
It handles both online and offline migration modes, and integrates with
the application's models and configuration.
"""

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

# Explicitly add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import settings from app config
from app.core.config import settings

# Import the Base class directly - don't import all models here
from app.db import base

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Use settings from app config instead of hardcoding
# Convert asyncpg URL to psycopg for migrations
db_url = str(settings.SQLALCHEMY_DATABASE_URI).replace(
    "postgresql+asyncpg://", "postgresql://"
)
config.set_section_option(config.config_ini_section, "sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata is the Base.metadata
target_metadata = base.Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema="public",
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the given connection."""
    print(f"Number of tables in metadata: {len(target_metadata.tables)}")
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,  # <-- required
        compare_type=True,
        version_table_schema="public",  # <-- required
    )

    with context.begin_transaction():
        context.run_migrations()
        print("Migrations executed successfully within transaction")


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using synchronous engine."""
    print("Attempting to connect to database...")
    print(f"Database URL: {db_url}")

    # List tables in metadata
    table_names = [table.name for table in target_metadata.tables.values()]
    print(f"Models to migrate: {table_names[:10]}...")  # Show first 10

    # Create a standard synchronous engine
    engine_config = config.get_section(config.config_ini_section)
    if not engine_config:
        raise ValueError("Could not find SQLAlchemy configuration section")

    connectable = engine_from_config(
        engine_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Run migrations with the synchronous engine
    with connectable.connect() as connection:
        from app.core.config import settings

        for schema in settings.DB_SCHEMAS:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            compare_type=True,
            version_table_schema="public",
        )
        # Test connection
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful!")

        # Check existing tables
        result = connection.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        )
        existing_tables = [row[0] for row in result]
        print(f"Existing tables before migration: {len(existing_tables)}")

        # Run migrations
        do_run_migrations(connection)

        # Check tables after migration
        result = connection.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        )
        tables_after = [row[0] for row in result]
        print(f"Tables after migration: {len(tables_after)}")
        new_tables = set(tables_after) - set(existing_tables)
        print(f"Newly created tables: {len(new_tables)}")

        # Commit explicitly
        connection.commit()


# This is the entrypoint that gets invoked when executing the env.py file
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
