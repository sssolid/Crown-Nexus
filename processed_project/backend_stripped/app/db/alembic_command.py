from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from alembic import command
from alembic.config import Config
from alembic.operations import Operations
from alembic.script import ScriptDirectory
def get_alembic_config(config_path: str='alembic.ini') -> Config:
    return Config(config_path)
def upgrade(config_path: str='alembic.ini', revision: str='head') -> None:
    alembic_cfg = get_alembic_config(config_path)
    command.upgrade(alembic_cfg, revision)
def downgrade(config_path: str='alembic.ini', revision: str='-1') -> None:
    alembic_cfg = get_alembic_config(config_path)
    command.downgrade(alembic_cfg, revision)
def revision(config_path: str='alembic.ini', message: str='auto-generated', autogenerate: bool=True) -> None:
    alembic_cfg = get_alembic_config(config_path)
    command.revision(alembic_cfg, message=message, autogenerate=autogenerate)
    post_process_migration_file(alembic_cfg)
def post_process_migration_file(alembic_cfg: Config) -> None:
    script = ScriptDirectory.from_config(alembic_cfg)
    revision = script.get_current_head()
    if not revision:
        print('No migration file found.')
        return
    revision_file = script.get_revision(revision).path
    if not revision_file:
        print(f'Revision file for {revision} not found.')
        return
    with open(revision_file, 'r') as f:
        content = f.read()
    fixed_content = fix_self_referential_tables(content)
    if fixed_content != content:
        print(f'🔄 Fixed self-referential table issues in {Path(revision_file).name}')
        with open(revision_file, 'w') as f:
            f.write(fixed_content)
def fix_self_referential_tables(content: str) -> str:
    create_table_pattern = "(op\\.create_table\\('([^']+)',.*?FOREIGN KEY\\(([^)]+)\\) REFERENCES \\2.*?sa\\.PrimaryKeyConstraint.*?\\))"
    def process_match(match: re.Match) -> str:
        full_match = match.group(1)
        table_name = match.group(2)
        fk_pattern = "sa\\.ForeignKeyConstraint\\(\\['([^']+)'\\], \\['([^']+)'\\]"
        self_refs = []
        for fk_match in re.finditer(fk_pattern, full_match):
            src_col = fk_match.group(1)
            target = fk_match.group(2)
            target_parts = target.split('.')
            if len(target_parts) >= 2 and target_parts[0] == table_name:
                target_col = target_parts[1]
                self_refs.append((src_col, target_col, fk_match.group(0)))
        if not self_refs:
            return full_match
        modified_create = full_match
        for _, _, fk_clause in self_refs:
            modified_create = modified_create.replace(fk_clause, '')
        modified_create = re.sub(',\\s*\\)', ')', modified_create)
        modified_create = re.sub(',\\s*,', ',', modified_create)
        alter_statements = []
        for src_col, target_col, _ in self_refs:
            if "sa.PrimaryKeyConstraint('" + target_col + "'" not in full_match and "sa.UniqueConstraint('" + target_col + "'" not in full_match:
                alter_statements.append(f"    op.create_unique_constraint('uq_{table_name}_{target_col}', '{table_name}', ['{target_col}'])")
            alter_statements.append(f"    op.create_foreign_key('fk_{table_name}_{src_col}_{target_col}', '{table_name}', '{table_name}', ['{src_col}'], ['{target_col}'])")
        return modified_create + '\n\n    # Add self-referential foreign keys after table creation\n' + '\n'.join(alter_statements)
    fixed_content = re.sub(create_table_pattern, process_match, content, flags=re.DOTALL)
    return fixed_content
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python alembic_command.py [upgrade|downgrade|revision] [args]')
        sys.exit(1)
    command_name = sys.argv[1]
    if command_name == 'upgrade':
        revision_arg = sys.argv[2] if len(sys.argv) > 2 else 'head'
        upgrade(revision=revision_arg)
    elif command_name == 'downgrade':
        revision_arg = sys.argv[2] if len(sys.argv) > 2 else '-1'
        downgrade(revision=revision_arg)
    elif command_name == 'revision':
        message = sys.argv[2] if len(sys.argv) > 2 else 'auto-generated'
        revision(message=message)
    else:
        print(f'Unknown command: {command_name}')
        sys.exit(1)