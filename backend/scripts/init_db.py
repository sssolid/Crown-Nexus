#!/usr/bin/env python
"""
Initialize database and create initial tables.
"""

import asyncio
import sys
from pathlib import Path

import asyncpg

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings


async def init_db() -> None:
    """
    Create database if it doesn't exist and initialize tables.
    """
    # Extract database name from connection string
    db_name = settings.POSTGRES_DB

    # Create connection string to postgres database (for creating our db)
    postgres_url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/postgres"

    try:
        # Connect to postgres database
        conn = await asyncpg.connect(postgres_url)

        # Check if our database exists
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db_name
        )

        if not exists:
            print(f"Creating database {db_name}...")
            # Create database
            await conn.execute(f"CREATE DATABASE {db_name}")
            print(f"Database {db_name} created successfully.")
        else:
            print(f"Database {db_name} already exists.")

        await conn.close()
        print("Database initialization complete.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_db())
