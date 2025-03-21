import asyncio
import os
import subprocess
import sys
from pathlib import Path
script_path = Path(__file__).resolve()
backend_dir = script_path.parent.parent
sys.path.insert(0, str(backend_dir))
import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
DATABASE_NAME = 'crown_nexus'
USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
async def reset_database():
    print(f"Resetting database '{DATABASE_NAME}'...")
    conn = await asyncpg.connect(user=USER, password=PASSWORD, host=HOST, database='postgres')
    try:
        await conn.execute(f'\n            DROP DATABASE IF EXISTS {DATABASE_NAME};\n        ')
        print(f"Dropped database '{DATABASE_NAME}' if it existed.")
        await conn.execute(f'\n            CREATE DATABASE {DATABASE_NAME};\n        ')
        print(f"Created fresh database '{DATABASE_NAME}'.")
    finally:
        await conn.close()
    print('Database reset complete.')
async def test_connection():
    print('\nTesting database connection...')
    try:
        conn = await asyncpg.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE_NAME)
        await conn.execute('SELECT 1')
        await conn.close()
        print('✅ Direct asyncpg connection successful!')
        engine = create_async_engine(f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}')
        async with engine.begin() as conn:
            await conn.execute(text('SELECT 1'))
        await engine.dispose()
        print('✅ SQLAlchemy connection successful!')
        return True
    except Exception as e:
        print(f'❌ Connection failed: {e}')
        return False
def run_alembic_migrations():
    print('\nRunning Alembic migrations...')
    try:
        original_dir = os.getcwd()
        os.chdir(str(backend_dir))
        if not Path('alembic.ini').exists():
            print(f'❌ alembic.ini not found in {os.getcwd()}')
            return False
        subprocess.run(['alembic', 'revision', '--autogenerate', '-m', 'Initial migration'], check=True)
        print('✅ Migration generated successfully!')
        subprocess.run(['alembic', 'upgrade', 'head'], check=True)
        print('✅ Migration applied successfully!')
        os.chdir(original_dir)
        return True
    except subprocess.CalledProcessError as e:
        print(f'❌ Migration failed: {e}')
        if 'original_dir' in locals():
            os.chdir(original_dir)
        return False
async def main():
    await reset_database()
    connection_success = await test_connection()
    if not connection_success:
        print('Database connection failed. Exiting.')
        return False
    migration_success = run_alembic_migrations()
    if not migration_success:
        print('Database migration failed. Exiting.')
        return False
    print('\n✅ Database successfully reset and initialized!')
    return True
if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)