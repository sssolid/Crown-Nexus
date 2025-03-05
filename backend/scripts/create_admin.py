#!/usr/bin/env python
"""
Create initial admin user.

Usage:
    python create_admin.py email password full_name
"""

import asyncio
import sys
from pathlib import Path

import asyncpg
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.db.session import async_session
from app.models.user import User, UserRole, get_password_hash


async def create_admin_user(email: str, password: str, full_name: str) -> None:
    """
    Create an admin user.

    Args:
        email: User email
        password: User password
        full_name: User full name
    """
    try:
        # Connect to database
        engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

        # Create tables if they don't exist
        # This is a backup if migrations haven't been run
        # try:
        #     async with engine.begin() as conn:
        #         from app.db.base import Base
        #         await conn.run_sync(Base.metadata.create_all)
        # except Exception as e:
        #     print(f"Error creating tables: {e}")

        # Create admin user
        async with async_session() as session:
            # Check if user already exists
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

            if user:
                print(f"User with email {email} already exists.")
                return

            # Create new user
            hashed_password = get_password_hash(password)
            user = User(
                email=email,
                hashed_password=hashed_password,
                full_name=full_name,
                role=UserRole.ADMIN,
                is_active=True,
            )

            session.add(user)
            await session.commit()

            print(f"Admin user {email} created successfully.")
    except Exception as e:
        print(f"Error creating admin user: {e}")


def print_usage() -> None:
    """Print script usage."""
    print("Usage: python create_admin.py email password full_name")
    print("Example: python create_admin.py admin@example.com password123 'Admin User'")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    full_name = sys.argv[3]

    asyncio.run(create_admin_user(email, password, full_name))
