#!/usr/bin/env python
"""
Reset database script.
This will drop and recreate the crown_nexus database, then create the initial tables.
"""

import asyncio
import subprocess
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.base import Base

DATABASE_NAME = "crown_nexus"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"


async def reset_database():
    """Drop and recreate the database, then create tables."""
    print(f"Resetting database '{DATABASE_NAME}'...")

    # Connect to postgres database to manage crown_nexus database
    conn = await asyncpg.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        database="postgres"  # Connect to default postgres database
    )

    try:
        # Drop database if it exists
        await conn.execute(f"""
            DROP DATABASE IF EXISTS {DATABASE_NAME};
        """)
        print(f"Dropped database '{DATABASE_NAME}' if it existed.")

        # Create fresh database
        await conn.execute(f"""
            CREATE DATABASE {DATABASE_NAME};
        """)
        print(f"Created fresh database '{DATABASE_NAME}'.")
    finally:
        await conn.close()

    print("Database reset complete.")


async def test_connection():
    """Test database connection."""
    print("\nTesting database connection...")
    try:
        # Try direct asyncpg connection
        conn = await asyncpg.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DATABASE_NAME
        )
        await conn.execute("SELECT 1")
        await conn.close()
        print("✅ Direct asyncpg connection successful!")

        # Try SQLAlchemy connection
        engine = create_async_engine(f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}")
        async with engine.begin() as conn:
            # Use text() for raw SQL
            await conn.execute(text("SELECT 1"))
        await engine.dispose()
        print("✅ SQLAlchemy connection successful!")

        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def run_alembic_migrations():
    """Run Alembic migrations to create tables."""
    print("\nRunning Alembic migrations...")
    try:
        # Generate migration
        subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", "Initial migration"],
            check=True
        )
        print("✅ Migration generated successfully!")

        # Apply migration
        subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True
        )
        print("✅ Migration applied successfully!")

        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return False


async def main():
    """Main function to reset and initialize the database."""
    # Reset database
    await reset_database()

    # Test connection
    connection_success = await test_connection()
    if not connection_success:
        print("Database connection failed. Exiting.")
        return False

    # Run migrations
    migration_success = run_alembic_migrations()
    if not migration_success:
        print("Database migration failed. Exiting.")
        return False

    print("\n✅ Database successfully reset and initialized!")
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
