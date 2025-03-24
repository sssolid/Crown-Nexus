# backend/scripts/database_bootstrap.py
#!/usr/bin/env python
"""
Database bootstrap script.

This script sets up the database with all necessary tables and creates
an initial admin user. It should be run after the database has been
created but before starting the application for the first time.

The script:
1. Creates all tables using SQLAlchemy models
2. Creates an admin user with provided credentials
3. Sets up required directories
4. Verifies database connectivity

Usage:
    python scripts/database_bootstrap.py [email] [password] [full_name]

    If credentials are not provided, defaults to:
    - Email: admin@example.com
    - Password: securepassword
    - Full name: Admin User
"""

from __future__ import annotations

import asyncio
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db_context
from app.domains.users.models import UserRole, get_password_hash

from scripts.bootstrap_countries import insert_countries


async def check_connection() -> bool:
    """
    Verify database connection.

    Returns:
        bool: True if connection succeeded, False otherwise
    """
    print("Testing database connection...")

    try:
        engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()
            print("✅ Database connection successful!")
            return True
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        return False
    finally:
        if "engine" in locals():
            await engine.dispose()


async def create_tables() -> bool:
    """
    Create all database tables using SQLAlchemy models.

    Returns:
        bool: True if tables were created successfully, False otherwise
    """
    print("Creating tables directly with SQLAlchemy...")

    # Create engine connecting to the app database
    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

    try:
        # Create all tables
        async with engine.begin() as conn:
            # Drop all tables first to ensure a clean start
            print("Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)

            print("Creating tables...")
            await conn.run_sync(Base.metadata.create_all)

        print("✅ Tables created successfully!")

        # Print the tables created
        async with engine.connect() as conn:
            result = await conn.execute(
                text(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = 'public'"
                )
            )
            tables = result.fetchall()

            print("\nCreated the following tables:")
            for table in tables:
                print(f"  - {table[0]}")

        return True
    except SQLAlchemyError as e:
        print(f"❌ Table creation failed: {e}")
        return False
    finally:
        await engine.dispose()


async def create_admin_user(
    email: str, password: str, full_name: str
) -> Tuple[bool, Optional[str]]:
    """
    Create an admin user.

    Args:
        email: User email
        password: User password
        full_name: User full name

    Returns:
        Tuple[bool, Optional[str]]: Success status and user ID if created
    """
    print(f"Creating admin user '{email}'...")

    try:
        async with get_db_context() as db:
            # Check if user already exists
            result = await db.execute(
                text('SELECT 1 FROM "user" WHERE email = :email'), {"email": email}
            )
            exists = result.scalar() is not None

            if exists:
                print(f"User with email '{email}' already exists.")
                return True, None

            # Hash the password
            hashed_password = get_password_hash(password)
            user_id = str(uuid.uuid4())
            now = datetime.now()

            # Insert user
            await db.execute(
                text(
                    'INSERT INTO "user" (id, email, hashed_password, full_name, role, is_active, is_deleted, created_at, updated_at) '
                    "VALUES (:id, :email, :hashed_password, :full_name, :role, :is_active, :is_deleted, :created_at, :updated_at)"
                ),
                {
                    "id": user_id,
                    "email": email,
                    "hashed_password": hashed_password,
                    "full_name": full_name,
                    "role": UserRole.ADMIN.value,
                    "is_active": True,
                    "is_deleted": False,
                    "created_at": now,
                    "updated_at": now,
                },
            )

            print(f"✅ Admin user '{email}' created successfully with ID: {user_id}")
            return True, user_id
    except SQLAlchemyError as e:
        print(f"❌ Admin user creation failed: {e}")
        return False, None


async def create_media_directories() -> None:
    """
    Create necessary media directories.
    """
    print("Creating media directories...")
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    # Create media subdirectories
    for media_type in ["image", "document", "video", "other", "thumbnails"]:
        dir_path = os.path.join(settings.MEDIA_ROOT, media_type)
        os.makedirs(dir_path, exist_ok=True)
        print(f"  - Created {dir_path}")


async def main() -> bool:
    """
    Main bootstrap function.

    Returns:
        bool: True if bootstrap succeeded, False otherwise
    """
    # Create media directories
    await create_media_directories()

    # Test database connection
    if not await check_connection():
        print("Database connection failed. Cannot continue with bootstrap.")
        return False

    # Create tables
    if not await create_tables():
        print("Table creation failed. Cannot continue with bootstrap.")
        return False

    # Add this section - populate country data
    print("Populating country reference data...")
    try:
        async with get_db_context() as db:
            await insert_countries(db)
        print("✅ Country data populated successfully!")
    except Exception as e:
        print(f"⚠️ Country data population failed: {e}")
        print("Continuing with bootstrap process...")

    # Create admin user
    if len(sys.argv) >= 4:
        email = sys.argv[1]
        password = sys.argv[2]
        full_name = sys.argv[3]
    else:
        # Default admin user
        email = "admin@example.com"
        password = "securepassword"
        full_name = "Admin User"
        print("Using default admin credentials. Change these in production!")

    user_created, _ = await create_admin_user(email, password, full_name)

    if not user_created:
        print("Warning: Failed to create admin user.")

    print("\n✅ Database bootstrap completed successfully!")
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
