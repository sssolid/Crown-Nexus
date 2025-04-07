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


def fix_postgresql_data_types(sql: str) -> str:
    """Fix PostgreSQL data type incompatibilities in SQL strings.

    Args:
        sql: SQL statement that might contain incompatible data types

    Returns:
        str: SQL statement with PostgreSQL compatible data types
    """
    # Replace DATETIME with TIMESTAMP
    return sql.replace(" DATETIME ", " TIMESTAMP ")


def drop_all_tables() -> bool:
    """Drop all tables with CASCADE.

    Returns:
        bool: True if successful or if no tables to drop, False otherwise
    """
    engine = get_engine()

    with engine.connect() as conn:
        # Disable foreign key constraints
        conn.execute(text("SET session_replication_role = 'replica'"))

        # Get all tables
        result = conn.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        )
        tables = [row[0] for row in result]

        if not tables:
            logger.info("No tables to drop.")
            return True  # Return True if there are no tables - this is successful!

        # Drop all tables
        for table in tables:
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
            logger.info(f"Dropped table: {table}")

        # Drop all schemas
        for schema in settings.DB_SCHEMAS:
            conn.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
            logger.info(f"Dropped schema: {schema}")

        # Re-enable constraints
        conn.execute(text("SET session_replication_role = 'origin'"))

    logger.info("✅ All tables dropped successfully")
    return True


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


def create_all_tables() -> bool:
    """Create all tables in the correct order with dependency handling.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        engine = get_engine()

        # Find problematic tables (self-references)
        problem_tables = find_problematic_tables()
        if problem_tables:
            logger.info(
                f"Found {len(problem_tables)} tables with self-referential foreign keys"
            )

        # Get list of tables in correct creation order
        table_order = sort_tables_by_dependency()
        logger.info(f"Creating tables in dependency order: {', '.join(table_order)}")

        # First phase: Create all tables without foreign key constraints
        for table_name in table_order:
            if table_name not in Base.metadata.tables:
                continue

            table = Base.metadata.tables[table_name]

            # Generate CREATE TABLE SQL without foreign keys
            column_defs = []
            primary_key_columns = []

            for column in table.columns:
                # Get column type with PostgreSQL compatibility fix
                column_type = str(column.type)
                # Convert DATETIME to TIMESTAMP for PostgreSQL
                if column_type.upper() == "DATETIME":
                    column_type = "TIMESTAMP"

                # Basic column definition
                col_def = f'"{column.name}" {column_type}'

                # Add constraints (except foreign keys and primary keys)
                if column.primary_key:
                    primary_key_columns.append(column.name)
                    # Don't add PRIMARY KEY here - we'll handle it separately
                if not column.nullable:
                    col_def += " NOT NULL"
                if column.server_default:
                    # Special handling for default values
                    default_value = str(column.server_default.arg)

                    # Fix 'NONE' as a string literal
                    if default_value == "NONE":
                        default_value = "'NONE'"

                    # Quote other non-numeric, non-function literals that aren't already quoted
                    if (
                        not default_value.startswith("'")
                        and not default_value.startswith('"')
                        and not default_value.lower() == "null"
                        and not default_value.lower() == "true"
                        and not default_value.lower() == "false"
                        and not "(" in default_value  # Skip functions like now()
                        and not default_value.replace(".", "", 1).isdigit()
                    ):  # Skip numbers
                        default_value = f"'{default_value}'"

                    col_def += f" DEFAULT {default_value}"

                column_defs.append(col_def)

                # Add composite primary key if needed
            if primary_key_columns:
                if len(primary_key_columns) == 1:
                    # Single primary key - add directly to column
                    for i, col_def in enumerate(column_defs):
                        if col_def.startswith(f'"{primary_key_columns[0]}"'):
                            column_defs[i] = col_def + " PRIMARY KEY"
                            break
                else:
                    # Composite primary key - add as separate constraint
                    quoted_cols = []
                    for col in primary_key_columns:
                        quoted_cols.append(f'"{col}"')
                    pk_constraint = f'PRIMARY KEY ({", ".join(quoted_cols)})'
                    column_defs.append(pk_constraint)

            # Create the table
            create_sql = (
                f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(column_defs) + "\n)"
            )

            with engine.connect() as conn:
                try:
                    # Skip if table already exists
                    inspector = inspect(engine)
                    if table_name in inspector.get_table_names():
                        logger.info(
                            f"Table {table_name} already exists, skipping creation"
                        )
                        continue

                    conn.execute(text(create_sql))
                    logger.info(f"Created table: {table_name}")
                except Exception as e:
                    logger.error(f"Failed to create table {table_name}: {e}")
                    return False

        # Second phase: Add foreign key constraints
        for table_name in table_order:
            if table_name not in Base.metadata.tables:
                continue

            table = Base.metadata.tables[table_name]
            is_problematic = table_name in problem_tables

            # If table is problematic, add unique constraints first
            if is_problematic:
                with engine.connect() as conn:
                    for source_col, ref_col in problem_tables[table_name]:
                        constraint_name = f"uq_{table_name}_{ref_col}"
                        try:
                            conn.execute(
                                text(
                                    f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} "
                                    f"UNIQUE ({ref_col})"
                                )
                            )
                            logger.info(
                                f"  Added unique constraint on {ref_col} in {table_name}"
                            )
                        except Exception as e:
                            if "already exists" not in str(e):
                                logger.error(f"Failed to add unique constraint: {e}")

            # Add foreign key constraints
            for column in table.columns:
                if not hasattr(column, "foreign_keys") or not column.foreign_keys:
                    continue

                for fk in column.foreign_keys:
                    target_table = fk.column.table.name
                    target_column = fk.column.name
                    source_column = column.name

                    # Skip if this is a self-reference and table is problematic
                    if is_problematic and target_table == table_name:
                        continue  # Will be handled separately

                    constraint_name = f"fk_{table_name}_{source_column}_{target_table}_{target_column}"

                    with engine.connect() as conn:
                        try:
                            conn.execute(
                                text(
                                    f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} "
                                    f"FOREIGN KEY ({source_column}) REFERENCES {target_table}({target_column})"
                                )
                            )
                            logger.info(
                                f"  Added foreign key: {table_name}.{source_column} -> {target_table}.{target_column}"
                            )
                        except Exception as e:
                            if "already exists" not in str(e):
                                logger.error(
                                    f"Failed to add foreign key constraint: {e}"
                                )

            # Add self-referential foreign keys last (for problematic tables)
            if is_problematic:
                with engine.connect() as conn:
                    for src_col, ref_col in problem_tables[table_name]:
                        constraint_name = f"fk_{table_name}_{src_col}_{ref_col}"
                        try:
                            conn.execute(
                                text(
                                    f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} "
                                    f"FOREIGN KEY ({src_col}) REFERENCES {table_name}({ref_col})"
                                )
                            )
                            logger.info(
                                f"  Added self-referential foreign key: {src_col} -> {ref_col} in {table_name}"
                            )
                        except Exception as e:
                            if "already exists" not in str(e):
                                logger.error(
                                    f"Failed to add self-referential foreign key: {e}"
                                )

        return True

    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False


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
    """Complete database reset that actually works.

    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Resetting database...")

    # Drop all tables
    if not drop_all_tables():
        logger.error("Failed to drop tables.")
        return False

    logger.info("✅ Database reset completed successfully!")
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
