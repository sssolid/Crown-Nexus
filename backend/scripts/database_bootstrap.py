#!/usr/bin/env python
"""
Bootstrap database script.
This script will create all tables directly using SQLAlchemy and create an admin user.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import uuid
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.db.base import Base
from app.models.user import User, UserRole, get_password_hash


async def create_database():
    """Create the database if it doesn't exist."""
    # Connect to default postgres database
    engine = create_async_engine(
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_SERVER}/postgres"
    )

    try:
        async with engine.begin() as conn:
            # Check if database exists
            result = await conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.POSTGRES_DB}'")
            )
            exists = result.scalar() is not None

            if not exists:
                print(f"Creating database '{settings.POSTGRES_DB}'...")
                await conn.execute(text(f'CREATE DATABASE "{settings.POSTGRES_DB}"'))
                print(f"Database '{settings.POSTGRES_DB}' created.")
            else:
                print(f"Database '{settings.POSTGRES_DB}' already exists.")
    finally:
        await engine.dispose()


async def create_tables():
    """Create all tables using SQLAlchemy."""
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
            result = await conn.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            ))
            tables = result.fetchall()

            print("\nCreated the following tables:")
            for table in tables:
                print(f"  - {table[0]}")
    finally:
        await engine.dispose()


async def create_admin_user(email, password, full_name):
    """Create an admin user."""
    print(f"Creating admin user '{email}'...")

    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

    try:
        async with engine.begin() as conn:
            # Check if user already exists
            result = await conn.execute(
                text("SELECT 1 FROM \"user\" WHERE email = :email"),
                {"email": email}
            )
            exists = result.scalar() is not None

            if exists:
                print(f"User with email '{email}' already exists.")
                return

            # Hash the password
            hashed_password = get_password_hash(password)
            user_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            # Insert user
            await conn.execute(
                text(
                    'INSERT INTO "user" (id, email, hashed_password, full_name, role, is_active, created_at, updated_at) '
                    'VALUES (:id, :email, :hashed_password, :full_name, :role, :is_active, :created_at, :updated_at)'
                ),
                {
                    "id": user_id,
                    "email": email,
                    "hashed_password": hashed_password,
                    "full_name": full_name,
                    "role": UserRole.ADMIN.value,
                    "is_active": True,
                    "created_at": now,
                    "updated_at": now
                }
            )

            print(f"✅ Admin user '{email}' created successfully with ID: {user_id}")
    finally:
        await engine.dispose()


async def check_connection():
    """Verify database connection."""
    print("Testing database connection...")

    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise
    finally:
        await engine.dispose()


async def main():
    """Main function."""
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    # Create media directories
    for media_type in ["image", "document", "video", "other", "thumbnails"]:
        os.makedirs(os.path.join(settings.MEDIA_ROOT, media_type), exist_ok=True)

    # Create database if it doesn't exist
    await create_database()

    # Test connection
    await check_connection()

    # Create tables
    await create_tables()

    # Create admin user if specified
    if len(sys.argv) >= 4:
        email = sys.argv[1]
        password = sys.argv[2]
        full_name = sys.argv[3]
        await create_admin_user(email, password, full_name)
    else:
        # Default admin user
        await create_admin_user("admin@example.com", "securepassword", "Admin User")


if __name__ == "__main__":
    asyncio.run(main())
