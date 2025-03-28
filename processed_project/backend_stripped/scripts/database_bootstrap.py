from __future__ import annotations
import asyncio
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
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
    print('Testing database connection...')
    try:
        engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
        async with engine.connect() as conn:
            result = await conn.execute(text('SELECT 1'))
            result.fetchone()
            print('✅ Database connection successful!')
            return True
    except SQLAlchemyError as e:
        print(f'❌ Database connection failed: {e}')
        return False
    finally:
        if 'engine' in locals():
            await engine.dispose()
async def create_tables() -> bool:
    print('Creating tables directly with SQLAlchemy...')
    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    try:
        async with engine.begin() as conn:
            print('Dropping existing tables...')
            await conn.run_sync(Base.metadata.drop_all)
            print('Creating tables...')
            await conn.run_sync(Base.metadata.create_all)
        print('✅ Tables created successfully!')
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = result.fetchall()
            print('\nCreated the following tables:')
            for table in tables:
                print(f'  - {table[0]}')
        return True
    except SQLAlchemyError as e:
        print(f'❌ Table creation failed: {e}')
        return False
    finally:
        await engine.dispose()
async def create_admin_user(email: str, password: str, full_name: str) -> Tuple[bool, Optional[str]]:
    print(f"Creating admin user '{email}'...")
    try:
        async with get_db_context() as db:
            result = await db.execute(text('SELECT 1 FROM "user" WHERE email = :email'), {'email': email})
            exists = result.scalar() is not None
            if exists:
                print(f"User with email '{email}' already exists.")
                return (True, None)
            hashed_password = get_password_hash(password)
            user_id = str(uuid.uuid4())
            now = datetime.now()
            await db.execute(text('INSERT INTO "user" (id, email, hashed_password, full_name, role, is_active, is_deleted, created_at, updated_at) VALUES (:id, :email, :hashed_password, :full_name, :role, :is_active, :is_deleted, :created_at, :updated_at)'), {'id': user_id, 'email': email, 'hashed_password': hashed_password, 'full_name': full_name, 'role': UserRole.ADMIN.value, 'is_active': True, 'is_deleted': False, 'created_at': now, 'updated_at': now})
            print(f"✅ Admin user '{email}' created successfully with ID: {user_id}")
            return (True, user_id)
    except SQLAlchemyError as e:
        print(f'❌ Admin user creation failed: {e}')
        return (False, None)
async def create_media_directories() -> None:
    print('Creating media directories...')
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    for media_type in ['image', 'document', 'video', 'other', 'thumbnails']:
        dir_path = os.path.join(settings.MEDIA_ROOT, media_type)
        os.makedirs(dir_path, exist_ok=True)
        print(f'  - Created {dir_path}')
async def main() -> bool:
    await create_media_directories()
    if not await check_connection():
        print('Database connection failed. Cannot continue with bootstrap.')
        return False
    if not await create_tables():
        print('Table creation failed. Cannot continue with bootstrap.')
        return False
    print('Populating country reference data...')
    try:
        async with get_db_context() as db:
            await insert_countries(db)
        print('✅ Country data populated successfully!')
    except Exception as e:
        print(f'⚠️ Country data population failed: {e}')
        print('Continuing with bootstrap process...')
    if len(sys.argv) >= 4:
        email = sys.argv[1]
        password = sys.argv[2]
        full_name = sys.argv[3]
    else:
        email = 'admin@example.com'
        password = 'securepassword'
        full_name = 'Admin User'
        print('Using default admin credentials. Change these in production!')
    user_created, _ = await create_admin_user(email, password, full_name)
    if not user_created:
        print('Warning: Failed to create admin user.')
    print('\n✅ Database bootstrap completed successfully!')
    return True
if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)