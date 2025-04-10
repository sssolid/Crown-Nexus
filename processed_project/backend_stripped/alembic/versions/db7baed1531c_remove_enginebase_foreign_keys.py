from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = 'db7baed1531c'
down_revision: Union[str, None] = '0f07e2b6660a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.drop_constraint('engine_base_engine_bore_stroke_id_fkey', 'engine_base', schema='vcdb', type_='foreignkey')
    op.drop_constraint('engine_base_engine_block_id_fkey', 'engine_base', schema='vcdb', type_='foreignkey')
    op.drop_column('engine_base', 'engine_bore_stroke_id', schema='vcdb')
    op.drop_column('engine_base', 'engine_block_id', schema='vcdb')
def downgrade() -> None:
    op.add_column('engine_base', sa.Column('engine_block_id', sa.INTEGER(), autoincrement=False, nullable=False), schema='vcdb')
    op.add_column('engine_base', sa.Column('engine_bore_stroke_id', sa.INTEGER(), autoincrement=False, nullable=False), schema='vcdb')
    op.create_foreign_key('engine_base_engine_block_id_fkey', 'engine_base', 'engine_block', ['engine_block_id'], ['engine_block_id'], source_schema='vcdb', referent_schema='vcdb')
    op.create_foreign_key('engine_base_engine_bore_stroke_id_fkey', 'engine_base', 'engine_bore_stroke', ['engine_bore_stroke_id'], ['engine_bore_stroke_id'], source_schema='vcdb', referent_schema='vcdb')