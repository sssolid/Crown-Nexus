# backend/scripts/init_db.py
#!/usr/bin/env python
"""
Database initialization script.

This script initializes the application database by creating it if it doesn't
exist and ensuring the database server is accessible. It serves as a utility
for first-time setup of the application's database environment.

The script:
1. Creates the database if it doesn't exist
2. Tests connectivity to the database server
3. Provides detailed error reporting

Usage:
    python scripts/init_db.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Optional, Tuple

import asyncpg
from asyncpg import Connection
from asyncpg.exceptions import PostgresError

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings


async def connect_to_postgres() -> Tuple[Connection, bool]:
    """
    Connect to the PostgreSQL server and check if our database exists.

    Returns:
        Tuple[Connection, bool]: Connection to postgres database and whether our DB exists

    Raises:
        PostgresError: If connection to PostgreSQL server fails
    """
    # Create connection string to postgres database (for creating our db)
    postgres_url = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/postgres"

    try:
        # Connect to postgres database
        conn = await asyncpg.connect(postgres_url)

        # Check if our database exists
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", settings.POSTGRES_DB
        )

        return conn, bool(exists)
    except PostgresError as e:
        print(f"❌ Failed to connect to PostgreSQL server: {e}")
        raise from e


async def create_database_if_not_exists(conn: Connection, db_exists: bool) -> None:
    """
    Create the application database if it doesn't exist.

    Args:
        conn: Connection to postgres database
        db_exists: Whether the database already exists

    Raises:
        PostgresError: If database creation fails
    """
    db_name = settings.POSTGRES_DB

    if not db_exists:
        print(f"Creating database {db_name}...")
        try:
            # Create database
            await conn.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ Database {db_name} created successfully.")
        except PostgresError as e:
            print(f"❌ Failed to create database: {e}")
            raise
    else:
        print(f"✅ Database {db_name} already exists.")


async def test_application_database_connection() -> bool:
    """
    Test connection to the application database.

    Returns:
        bool: True if connection succeeded, False otherwise
    """
    connection_string = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"

    try:
        # Try to connect to the application database
        conn = await asyncpg.connect(connection_string)
        await conn.execute("SELECT 1")
        await conn.close()
        print(f"✅ Successfully connected to {settings.POSTGRES_DB} database!")
        return True
    except PostgresError as e:
        print(f"❌ Failed to connect to application database: {e}")
        return False


async def init_db() -> bool:
    """
    Initialize the database by creating it if it doesn't exist.

    Returns:
        bool: True if initialization succeeded, False otherwise
    """
    print("Initializing database...")
    conn: Optional[Connection] = None

    try:
        # Connect to postgres database and check if our DB exists
        conn, db_exists = await connect_to_postgres()

        # Create database if it doesn't exist
        await create_database_if_not_exists(conn, db_exists)

        # Test connection to the application database
        connection_success = await test_application_database_connection()

        print("Database initialization complete.")
        return connection_success
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        # Ensure connection is closed
        if conn:
            await conn.close()


if __name__ == "__main__":
    success = asyncio.run(init_db())
    sys.exit(0 if success else 1)
