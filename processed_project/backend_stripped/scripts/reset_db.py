import argparse
import os
import shutil
import sys
from pathlib import Path
from sqlalchemy import create_engine, text, MetaData, inspect
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.config import settings
def drop_all_tables():
    sync_url = str(settings.SQLALCHEMY_DATABASE_URI).replace('postgresql+asyncpg://', 'postgresql://')
    engine = create_engine(sync_url)
    with engine.connect() as conn:
        conn.execute(text('COMMIT'))
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        tables = [row[0] for row in result]
        print(f'Found {len(tables)} tables to drop')
        conn.execute(text("SET session_replication_role = 'replica'"))
        for table in tables:
            print(f'Dropping table: {table}')
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
        conn.execute(text("SET session_replication_role = 'origin'"))
        conn.execute(text('COMMIT'))
    print('✅ All tables dropped successfully')
def clear_migrations(versions_dir):
    if not versions_dir.exists():
        print(f'Versions directory not found: {versions_dir}')
        return
    backup_dir = versions_dir.parent / 'versions_backup'
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    os.makedirs(backup_dir, exist_ok=True)
    for migration_file in versions_dir.glob('*.py'):
        if migration_file.name != '__init__.py':
            shutil.copy2(migration_file, backup_dir)
            print(f'Backed up: {migration_file.name}')
    for migration_file in versions_dir.glob('*.py'):
        if migration_file.name != '__init__.py':
            migration_file.unlink()
            print(f'Deleted: {migration_file.name}')
    print("✅ All migration files cleared (backup created in 'versions_backup')")
def create_initial_migration(message='initial'):
    cmd = f'alembic revision --autogenerate -m "{message}"'
    print(f'Creating new initial migration: {cmd}')
    result = os.system(cmd)
    if result != 0:
        print(f'⚠️ Failed to create initial migration (exit code: {result})')
    else:
        print('✅ New initial migration created successfully')
    return result
def main():
    parser = argparse.ArgumentParser(description='Complete database reset (drops all tables and optionally resets migrations)')
    parser.add_argument('--keep-migrations', action='store_true', help="Don't delete existing migration files")
    parser.add_argument('--message', default='initial', help='Message for the new initial migration')
    parser.add_argument('--skip-create', action='store_true', help='Skip creating new migration')
    args = parser.parse_args()
    print('⚠️ WARNING: This will drop ALL tables in your database and reset migrations!')
    confirm = input('Are you sure you want to continue? (y/N): ')
    if confirm.lower() != 'y':
        print('Operation cancelled.')
        return
    drop_all_tables()
    if not args.keep_migrations:
        versions_dir = Path('alembic/versions')
        clear_migrations(versions_dir)
    if not args.skip_create:
        create_initial_migration(args.message)
    print('\nTrue reset completed.')
    if not args.skip_create:
        print('You can now run: alembic upgrade head')
if __name__ == '__main__':
    main()