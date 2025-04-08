# backend/manage_db.py
"""
Database management tool that actually works.
ONE command to rule them all.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, cast

from sqlalchemy import MetaData, create_engine, inspect, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.schema import Column, CreateTable, ForeignKey, Table

# Ensure we can import app modules
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import settings and models
from app.core.config import settings
from app.db.base import Base

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def get_engine() -> Engine:
    """Get synchronous database engine.

    Returns:
        Engine: SQLAlchemy engine for database operations
    """
    url = str(settings.SQLALCHEMY_DATABASE_URI).replace(
        "postgresql+asyncpg://", "postgresql://"
    )
    return create_engine(url, isolation_level="AUTOCOMMIT", echo=False)


def execute_sql(sql: str, description: Optional[str] = None) -> bool:
    """Execute SQL with better error handling.

    Args:
        sql: SQL statement to execute
        description: Optional description of the operation

    Returns:
        bool: True if successful, False otherwise
    """
    engine = get_engine()

    try:
        with engine.connect() as conn:
            if description:
                logger.info(f"SQL: {description}")
            conn.execute(text(sql))
            return True
    except Exception as e:
        logger.error(f"SQL Error: {e}")
        return False


def sort_tables_by_dependency() -> List[str]:
    """Sort tables based on their foreign key dependencies.

    Returns:
        List[str]: List of table names in order of creation
    """
    dependency_graph: Dict[str, Set[str]] = {}

    # Build dependency graph
    for table_name, table in Base.metadata.tables.items():
        dependencies = set()

        for column in table.columns:
            if not hasattr(column, "foreign_keys"):
                continue

            for fk in column.foreign_keys:
                # Skip self-references
                if fk.column.table.name != table_name:
                    dependencies.add(fk.column.table.name)

        dependency_graph[table_name] = dependencies

    # Topological sort
    result: List[str] = []
    temporary_mark: Set[str] = set()
    permanent_mark: Set[str] = set()

    def visit(node: str) -> None:
        if node in permanent_mark:
            return
        if node in temporary_mark:
            # Circular dependency - will be handled separately
            return

        temporary_mark.add(node)

        for dependency in dependency_graph.get(node, set()):
            if dependency in dependency_graph:  # Only visit nodes in our graph
                visit(dependency)

        temporary_mark.remove(node)
        permanent_mark.add(node)
        result.append(node)

    # Visit all nodes
    for node in list(dependency_graph.keys()):
        if node not in permanent_mark:
            visit(node)

    # Reverse to get correct order
    return list(reversed(result))


def find_problematic_tables() -> Dict[str, List[Tuple[str, str]]]:
    """Find all tables with self-referential foreign keys.

    Returns:
        Dict[str, List[Tuple[str, str]]]: Dictionary mapping table names to
            lists of (source_column, reference_column) tuples
    """
    problematic_tables: Dict[str, List[Tuple[str, str]]] = {}

    for table_name, table in Base.metadata.tables.items():
        self_refs: List[Tuple[str, str]] = []

        for column in table.columns:
            if not hasattr(column, "foreign_keys"):
                continue

            for fk in column.foreign_keys:
                # Check if this is a self-reference
                if fk.column.table.name == table_name:
                    # Found a self-reference
                    ref_column = fk.column.name
                    source_column = column.name
                    self_refs.append((source_column, ref_column))

        if self_refs:
            problematic_tables[table_name] = self_refs

    return problematic_tables


def initialize_alembic() -> bool:
    """Ensure Alembic is properly initialized and stamped.

    Returns:
        bool: True if successful, False otherwise
    """
    # Check if alembic directory exists
    alembic_dir = Path("alembic")

    if not alembic_dir.exists():
        logger.info("Alembic not initialized. Running 'alembic init alembic'...")
        result = subprocess.run(
            ["alembic", "init", "alembic"], capture_output=True, text=True
        )
        if result.returncode != 0:
            logger.error(f"Failed to initialize Alembic: {result.stderr}")
            return False
        logger.info("✅ Alembic initialized")

    # Stamp the current state
    logger.info("Stamping current database state...")
    result = subprocess.run(
        ["alembic", "stamp", "head"], capture_output=True, text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to stamp database: {result.stderr}")
        return False

    logger.info("✅ Database stamped successfully")
    return True


def reset_database() -> bool:
    """Reset the database using Alembic only."""
    logger.info("Resetting database...")

    # Drop all data — cleanest approach
    result = subprocess.run(
        ["alembic", "downgrade", "base"], capture_output=True, text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to downgrade: {result.stderr}")
        return False

    result = subprocess.run(
        ["alembic", "upgrade", "head"], capture_output=True, text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to upgrade: {result.stderr}")
        return False

    logger.info("✅ Database reset and upgraded via Alembic")
    return True


def run_alembic_command(command: str, *args: str) -> bool:
    """Run an alembic command.

    Args:
        command: Alembic command to run
        *args: Additional arguments to pass to the command

    Returns:
        bool: True if successful, False otherwise
    """
    cmd = ["alembic", command] + list(args)
    logger.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        logger.info(f"✅ Command completed successfully")
        if result.stdout:
            logger.info(result.stdout)
        return True
    else:
        logger.error(f"❌ Command failed: {result.stderr}")
        return False


def handle_create(message: str) -> bool:
    """Create a new migration.

    Args:
        message: Migration message

    Returns:
        bool: True if successful, False otherwise
    """
    # Make sure database is stamped first
    logger.info("Ensuring database is stamped...")
    subprocess.run(["alembic", "stamp", "head"], capture_output=True, text=True)

    return run_alembic_command("revision", "--autogenerate", "-m", message)


def handle_upgrade(revision: str = "head") -> bool:
    """Upgrade the database to a revision.

    Args:
        revision: Revision to upgrade to, defaults to "head"

    Returns:
        bool: True if successful, False otherwise
    """
    return run_alembic_command("upgrade", revision)


def handle_downgrade(revision: str = "-1") -> bool:
    """Downgrade the database to a revision.

    Args:
        revision: Revision to downgrade to, defaults to "-1"

    Returns:
        bool: True if successful, False otherwise
    """
    return run_alembic_command("downgrade", revision)


def handle_stamp(revision: str = "head") -> bool:
    """Stamp the database with a specific revision without running migrations.

    Args:
        revision: Revision to stamp with, defaults to "head"

    Returns:
        bool: True if successful, False otherwise
    """
    return run_alembic_command("stamp", revision)


def main() -> None:
    """Main function to parse arguments and execute commands."""
    parser = argparse.ArgumentParser(
        description="Database management tool that actually works"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Reset command (THE ONE COMMAND TO RULE THEM ALL)
    subparsers.add_parser("reset", help="Reset the database completely")

    # Still include the usual commands for convenience
    create_parser = subparsers.add_parser("create", help="Create a new migration")
    create_parser.add_argument("message", help="Migration message")

    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade database")
    upgrade_parser.add_argument(
        "revision", nargs="?", default="head", help="Revision to upgrade to"
    )

    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade database")
    downgrade_parser.add_argument(
        "revision", nargs="?", default="-1", help="Revision to downgrade to"
    )

    # Add stamp command
    stamp_parser = subparsers.add_parser(
        "stamp", help="Stamp database without running migrations"
    )
    stamp_parser.add_argument(
        "revision", nargs="?", default="head", help="Revision to stamp with"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Execute the command
    if args.command == "reset":
        reset_database()
    elif args.command == "create":
        handle_create(args.message)
    elif args.command == "upgrade":
        handle_upgrade(args.revision)
    elif args.command == "downgrade":
        handle_downgrade(args.revision)
    elif args.command == "stamp":
        handle_stamp(args.revision)


if __name__ == "__main__":
    main()
