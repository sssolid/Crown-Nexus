from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = '9fc1a9affe33'
down_revision: Union[str, None] = 'ef389cd9aa2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.alter_column('address', 'latitude', existing_type=sa.REAL(), type_=sa.Float(precision=10, decimal_return_scale=7), existing_nullable=True, schema='location')
    op.alter_column('address', 'longitude', existing_type=sa.REAL(), type_=sa.Float(precision=10, decimal_return_scale=7), existing_nullable=True, schema='location')
def downgrade() -> None:
    op.alter_column('address', 'longitude', existing_type=sa.Float(precision=10, decimal_return_scale=7), type_=sa.REAL(), existing_nullable=True, schema='location')
    op.alter_column('address', 'latitude', existing_type=sa.Float(precision=10, decimal_return_scale=7), type_=sa.REAL(), existing_nullable=True, schema='location')