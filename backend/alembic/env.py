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
from typing import Optional

from alembic import context
from sqlalchemy import engine_from_config, pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

# Explicitly add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import settings from app config
from app.core.config import settings

# Import the Base class directly - don't import all models here
from app.db.base_class import Base

# Import models individually to register them with SQLAlchemy
# This avoids the circular imports caused by importing base.py
# This section is crucial for Alembic to detect model changes
import app.models.user  # noqa
import app.models.associations  # noqa
import app.models.location  # noqa
import app.models.reference  # noqa
import app.models.product  # noqa
import app.models.media  # noqa
import app.models.compliance  # noqa

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Use settings from app config instead of hardcoding
db_url = str(settings.SQLALCHEMY_DATABASE_URI)
config.set_section_option(config.config_ini_section, "sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata is the Base.metadata that all models are registered with
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url: str = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Run migrations with the given connection.

    Args:
        connection: SQLAlchemy connection
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Print diagnostic information
    print("Attempting to connect to database...")
    print(f"Database URL: {db_url}")

    # List all tables in the metadata for verification
    table_names = [table.name for table in target_metadata.tables.values()]
    print(f"Models to migrate: {table_names}")

    # Create the engine with explicit configuration
    engine_config = config.get_section(config.config_ini_section)
    if not engine_config:
        raise ValueError("Could not find SQLAlchemy configuration section")

    connectable = AsyncEngine(
        engine_from_config(
            engine_config,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    # Test connection before proceeding
    try:
        async with connectable.connect() as connection:
            # Test the connection
            await connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")

            # Run migrations
            await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        # Show more detailed error information
        import traceback
        traceback.print_exc()
        raise from e
    finally:
        await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
