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
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app.core.config import settings
from app.db.base import Base
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
def get_engine() -> Engine:
    url = str(settings.SQLALCHEMY_DATABASE_URI).replace('postgresql+asyncpg://', 'postgresql://')
    return create_engine(url, isolation_level='AUTOCOMMIT', echo=False)
def execute_sql(sql: str, description: Optional[str]=None) -> bool:
    engine = get_engine()
    try:
        with engine.connect() as conn:
            if description:
                logger.info(f'SQL: {description}')
            conn.execute(text(sql))
            return True
    except Exception as e:
        logger.error(f'SQL Error: {e}')
        return False
def fix_postgresql_data_types(sql: str) -> str:
    return sql.replace(' DATETIME ', ' TIMESTAMP ')
def drop_all_tables() -> bool:
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SET session_replication_role = 'replica'"))
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
        tables = [row[0] for row in result]
        if not tables:
            logger.info('No tables to drop.')
            return True
        for table in tables:
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
            logger.info(f'Dropped table: {table}')
        for schema in settings.DB_SCHEMAS:
            conn.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
            logger.info(f'Dropped schema: {schema}')
        conn.execute(text("SET session_replication_role = 'origin'"))
    logger.info('✅ All tables dropped successfully')
    return True
def sort_tables_by_dependency() -> List[str]:
    dependency_graph: Dict[str, Set[str]] = {}
    for table_name, table in Base.metadata.tables.items():
        dependencies = set()
        for column in table.columns:
            if not hasattr(column, 'foreign_keys'):
                continue
            for fk in column.foreign_keys:
                if fk.column.table.name != table_name:
                    dependencies.add(fk.column.table.name)
        dependency_graph[table_name] = dependencies
    result: List[str] = []
    temporary_mark: Set[str] = set()
    permanent_mark: Set[str] = set()
    def visit(node: str) -> None:
        if node in permanent_mark:
            return
        if node in temporary_mark:
            return
        temporary_mark.add(node)
        for dependency in dependency_graph.get(node, set()):
            if dependency in dependency_graph:
                visit(dependency)
        temporary_mark.remove(node)
        permanent_mark.add(node)
        result.append(node)
    for node in list(dependency_graph.keys()):
        if node not in permanent_mark:
            visit(node)
    return list(reversed(result))
def find_problematic_tables() -> Dict[str, List[Tuple[str, str]]]:
    problematic_tables: Dict[str, List[Tuple[str, str]]] = {}
    for table_name, table in Base.metadata.tables.items():
        self_refs: List[Tuple[str, str]] = []
        for column in table.columns:
            if not hasattr(column, 'foreign_keys'):
                continue
            for fk in column.foreign_keys:
                if fk.column.table.name == table_name:
                    ref_column = fk.column.name
                    source_column = column.name
                    self_refs.append((source_column, ref_column))
        if self_refs:
            problematic_tables[table_name] = self_refs
    return problematic_tables
def create_all_tables() -> bool:
    try:
        engine = get_engine()
        problem_tables = find_problematic_tables()
        if problem_tables:
            logger.info(f'Found {len(problem_tables)} tables with self-referential foreign keys')
        table_order = sort_tables_by_dependency()
        logger.info(f"Creating tables in dependency order: {', '.join(table_order)}")
        for table_name in table_order:
            if table_name not in Base.metadata.tables:
                continue
            table = Base.metadata.tables[table_name]
            column_defs = []
            primary_key_columns = []
            for column in table.columns:
                column_type = str(column.type)
                if column_type.upper() == 'DATETIME':
                    column_type = 'TIMESTAMP'
                col_def = f'"{column.name}" {column_type}'
                if column.primary_key:
                    primary_key_columns.append(column.name)
                if not column.nullable:
                    col_def += ' NOT NULL'
                if column.server_default:
                    default_value = str(column.server_default.arg)
                    if default_value == 'NONE':
                        default_value = "'NONE'"
                    if not default_value.startswith("'") and (not default_value.startswith('"')) and (not default_value.lower() == 'null') and (not default_value.lower() == 'true') and (not default_value.lower() == 'false') and (not '(' in default_value) and (not default_value.replace('.', '', 1).isdigit()):
                        default_value = f"'{default_value}'"
                    col_def += f' DEFAULT {default_value}'
                column_defs.append(col_def)
            if primary_key_columns:
                if len(primary_key_columns) == 1:
                    for i, col_def in enumerate(column_defs):
                        if col_def.startswith(f'"{primary_key_columns[0]}"'):
                            column_defs[i] = col_def + ' PRIMARY KEY'
                            break
                else:
                    quoted_cols = []
                    for col in primary_key_columns:
                        quoted_cols.append(f'"{col}"')
                    pk_constraint = f"PRIMARY KEY ({', '.join(quoted_cols)})"
                    column_defs.append(pk_constraint)
            create_sql = f'CREATE TABLE {table_name} (\n  ' + ',\n  '.join(column_defs) + '\n)'
            with engine.connect() as conn:
                try:
                    inspector = inspect(engine)
                    if table_name in inspector.get_table_names():
                        logger.info(f'Table {table_name} already exists, skipping creation')
                        continue
                    conn.execute(text(create_sql))
                    logger.info(f'Created table: {table_name}')
                except Exception as e:
                    logger.error(f'Failed to create table {table_name}: {e}')
                    return False
        for table_name in table_order:
            if table_name not in Base.metadata.tables:
                continue
            table = Base.metadata.tables[table_name]
            is_problematic = table_name in problem_tables
            if is_problematic:
                with engine.connect() as conn:
                    for source_col, ref_col in problem_tables[table_name]:
                        constraint_name = f'uq_{table_name}_{ref_col}'
                        try:
                            conn.execute(text(f'ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} UNIQUE ({ref_col})'))
                            logger.info(f'  Added unique constraint on {ref_col} in {table_name}')
                        except Exception as e:
                            if 'already exists' not in str(e):
                                logger.error(f'Failed to add unique constraint: {e}')
            for column in table.columns:
                if not hasattr(column, 'foreign_keys') or not column.foreign_keys:
                    continue
                for fk in column.foreign_keys:
                    target_table = fk.column.table.name
                    target_column = fk.column.name
                    source_column = column.name
                    if is_problematic and target_table == table_name:
                        continue
                    constraint_name = f'fk_{table_name}_{source_column}_{target_table}_{target_column}'
                    with engine.connect() as conn:
                        try:
                            conn.execute(text(f'ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({source_column}) REFERENCES {target_table}({target_column})'))
                            logger.info(f'  Added foreign key: {table_name}.{source_column} -> {target_table}.{target_column}')
                        except Exception as e:
                            if 'already exists' not in str(e):
                                logger.error(f'Failed to add foreign key constraint: {e}')
            if is_problematic:
                with engine.connect() as conn:
                    for src_col, ref_col in problem_tables[table_name]:
                        constraint_name = f'fk_{table_name}_{src_col}_{ref_col}'
                        try:
                            conn.execute(text(f'ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({src_col}) REFERENCES {table_name}({ref_col})'))
                            logger.info(f'  Added self-referential foreign key: {src_col} -> {ref_col} in {table_name}')
                        except Exception as e:
                            if 'already exists' not in str(e):
                                logger.error(f'Failed to add self-referential foreign key: {e}')
        return True
    except Exception as e:
        logger.error(f'Error creating tables: {e}')
        return False
def initialize_alembic() -> bool:
    alembic_dir = Path('alembic')
    if not alembic_dir.exists():
        logger.info("Alembic not initialized. Running 'alembic init alembic'...")
        result = subprocess.run(['alembic', 'init', 'alembic'], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f'Failed to initialize Alembic: {result.stderr}')
            return False
        logger.info('✅ Alembic initialized')
    logger.info('Stamping current database state...')
    result = subprocess.run(['alembic', 'stamp', 'head'], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f'Failed to stamp database: {result.stderr}')
        return False
    logger.info('✅ Database stamped successfully')
    return True
def reset_database() -> bool:
    logger.info('Resetting database...')
    if not drop_all_tables():
        logger.error('Failed to drop tables.')
        return False
    logger.info('✅ Database reset completed successfully!')
    return True
def run_alembic_command(command: str, *args: str) -> bool:
    cmd = ['alembic', command] + list(args)
    logger.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        logger.info(f'✅ Command completed successfully')
        if result.stdout:
            logger.info(result.stdout)
        return True
    else:
        logger.error(f'❌ Command failed: {result.stderr}')
        return False
def handle_create(message: str) -> bool:
    logger.info('Ensuring database is stamped...')
    subprocess.run(['alembic', 'stamp', 'head'], capture_output=True, text=True)
    return run_alembic_command('revision', '--autogenerate', '-m', message)
def handle_upgrade(revision: str='head') -> bool:
    return run_alembic_command('upgrade', revision)
def handle_downgrade(revision: str='-1') -> bool:
    return run_alembic_command('downgrade', revision)
def handle_stamp(revision: str='head') -> bool:
    return run_alembic_command('stamp', revision)
def main() -> None:
    parser = argparse.ArgumentParser(description='Database management tool that actually works')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    subparsers.add_parser('reset', help='Reset the database completely')
    create_parser = subparsers.add_parser('create', help='Create a new migration')
    create_parser.add_argument('message', help='Migration message')
    upgrade_parser = subparsers.add_parser('upgrade', help='Upgrade database')
    upgrade_parser.add_argument('revision', nargs='?', default='head', help='Revision to upgrade to')
    downgrade_parser = subparsers.add_parser('downgrade', help='Downgrade database')
    downgrade_parser.add_argument('revision', nargs='?', default='-1', help='Revision to downgrade to')
    stamp_parser = subparsers.add_parser('stamp', help='Stamp database without running migrations')
    stamp_parser.add_argument('revision', nargs='?', default='head', help='Revision to stamp with')
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    if args.command == 'reset':
        reset_database()
    elif args.command == 'create':
        handle_create(args.message)
    elif args.command == 'upgrade':
        handle_upgrade(args.revision)
    elif args.command == 'downgrade':
        handle_downgrade(args.revision)
    elif args.command == 'stamp':
        handle_stamp(args.revision)
if __name__ == '__main__':
    main()