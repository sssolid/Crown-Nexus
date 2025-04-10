from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = '660598405145'
down_revision: Union[str, None] = '9fc1a9affe33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.drop_index('ix_vcdb_year_year', table_name='year', schema='vcdb')
    op.drop_column('year', 'year', schema='vcdb')
def downgrade() -> None:
    op.add_column('year', sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=False), schema='vcdb')
    op.create_index('ix_vcdb_year_year', 'year', ['year'], unique=False, schema='vcdb')