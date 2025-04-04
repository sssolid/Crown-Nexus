# backend/true_reset.py
"""
Hard database reset script that allows completely starting over with migrations.

This script:
1. Drops all tables in the database (including alembic_version)
2. Deletes all migration files (optional)
3. Creates a new initial migration
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from sqlalchemy import create_engine, text, MetaData, inspect

# Ensure we can import app modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import settings from app config
from app.core.config import settings


def drop_all_tables():
    """Drop ALL tables from the database, including alembic_version."""
    # Create a synchronous connection to the database
    sync_url = str(settings.SQLALCHEMY_DATABASE_URI).replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(sync_url)

    with engine.connect() as conn:
        conn.execute(text("COMMIT"))  # Close any existing transaction

        # Get list of all tables
        result = conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        ))
        tables = [row[0] for row in result]
        print(f"Found {len(tables)} tables to drop")

        # Disable foreign key constraints temporarily
        conn.execute(text("SET session_replication_role = 'replica'"))

        # Drop all tables
        for table in tables:
            print(f"Dropping table: {table}")
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))

        # Re-enable foreign key constraints
        conn.execute(text("SET session_replication_role = 'origin'"))

        # Commit changes
        conn.execute(text("COMMIT"))

    print("✅ All tables dropped successfully")


def clear_migrations(versions_dir):
    """Delete all migration files in the versions directory."""
    if not versions_dir.exists():
        print(f"Versions directory not found: {versions_dir}")
        return

    # Make backup of versions directory
    backup_dir = versions_dir.parent / "versions_backup"
    if backup_dir.exists():
        shutil.rmtree(backup_dir)

    os.makedirs(backup_dir, exist_ok=True)

    # Copy all migration files to backup
    for migration_file in versions_dir.glob("*.py"):
        if migration_file.name != "__init__.py":
            shutil.copy2(migration_file, backup_dir)
            print(f"Backed up: {migration_file.name}")

    # Delete all migration files except __init__.py
    for migration_file in versions_dir.glob("*.py"):
        if migration_file.name != "__init__.py":
            migration_file.unlink()
            print(f"Deleted: {migration_file.name}")

    print("✅ All migration files cleared (backup created in 'versions_backup')")


def create_initial_migration(message="initial"):
    """Create a new initial migration."""
    cmd = f'alembic revision --autogenerate -m "{message}"'
    print(f"Creating new initial migration: {cmd}")
    result = os.system(cmd)

    if result != 0:
        print(f"⚠️ Failed to create initial migration (exit code: {result})")
    else:
        print("✅ New initial migration created successfully")

    return result


def main():
    """Parse arguments and execute commands."""
    parser = argparse.ArgumentParser(
        description="Complete database reset (drops all tables and optionally resets migrations)"
    )
    parser.add_argument(
        "--keep-migrations",
        action="store_true",
        help="Don't delete existing migration files"
    )
    parser.add_argument(
        "--message",
        default="initial",
        help="Message for the new initial migration"
    )
    parser.add_argument(
        "--skip-create",
        action="store_true",
        help="Skip creating new migration"
    )

    args = parser.parse_args()

    # Ask for confirmation
    print("⚠️ WARNING: This will drop ALL tables in your database and reset migrations!")
    confirm = input("Are you sure you want to continue? (y/N): ")

    if confirm.lower() != "y":
        print("Operation cancelled.")
        return

    # Drop all tables
    drop_all_tables()

    # Clear migrations if requested
    if not args.keep_migrations:
        versions_dir = Path("alembic/versions")
        clear_migrations(versions_dir)

    # Create new initial migration if requested
    if not args.skip_create:
        create_initial_migration(args.message)

    print("\nTrue reset completed.")
    if not args.skip_create:
        print("You can now run: alembic upgrade head")


if __name__ == "__main__":
    main()
