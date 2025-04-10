from __future__ import annotations
import asyncio
import sys
from pathlib import Path
from typing import Optional, Tuple
import asyncpg
from asyncpg import Connection
from asyncpg.exceptions import PostgresError
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.config import settings
async def connect_to_postgres() -> Tuple[Connection, bool]:
    postgres_url = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/postgres'
    try:
        conn = await asyncpg.connect(postgres_url)
        exists = await conn.fetchval('SELECT 1 FROM pg_database WHERE datname = $1', settings.POSTGRES_DB)
        return (conn, bool(exists))
    except PostgresError as e:
        print(f'❌ Failed to connect to PostgreSQL server: {e}')
        raise
async def create_database_if_not_exists(conn: Connection, db_exists: bool) -> None:
    db_name = settings.POSTGRES_DB
    if not db_exists:
        print(f'Creating database {db_name}...')
        try:
            await conn.execute(f'CREATE DATABASE {db_name}')
            print(f'✅ Database {db_name} created successfully.')
        except PostgresError as e:
            print(f'❌ Failed to create database: {e}')
            raise
    else:
        print(f'✅ Database {db_name} already exists.')
async def test_application_database_connection() -> bool:
    connection_string = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}'
    try:
        conn = await asyncpg.connect(connection_string)
        await conn.execute('SELECT 1')
        await conn.close()
        print(f'✅ Successfully connected to {settings.POSTGRES_DB} database!')
        return True
    except PostgresError as e:
        print(f'❌ Failed to connect to application database: {e}')
        return False
async def init_db() -> bool:
    print('Initializing database...')
    conn: Optional[Connection] = None
    try:
        conn, db_exists = await connect_to_postgres()
        await create_database_if_not_exists(conn, db_exists)
        connection_success = await test_application_database_connection()
        print('Database initialization complete.')
        return connection_success
    except Exception as e:
        print(f'Error initializing database: {e}')
        return False
    finally:
        if conn:
            await conn.close()
if __name__ == '__main__':
    success = asyncio.run(init_db())
    sys.exit(0 if success else 1)