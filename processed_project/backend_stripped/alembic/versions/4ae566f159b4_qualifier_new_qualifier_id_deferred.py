from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = '4ae566f159b4'
down_revision: Union[str, None] = '48a3e13baa8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.drop_constraint('qualifier_new_qualifier_id_fkey', 'qualifier', schema='qdb', type_='foreignkey')
    op.create_foreign_key(None, 'qualifier', 'qualifier', ['new_qualifier_id'], ['qualifier_id'], source_schema='qdb', referent_schema='qdb', initially='DEFERRED', deferrable=True)
def downgrade() -> None:
    op.drop_constraint(None, 'qualifier', schema='qdb', type_='foreignkey')
    op.create_foreign_key('qualifier_new_qualifier_id_fkey', 'qualifier', 'qualifier', ['new_qualifier_id'], ['qualifier_id'], source_schema='qdb', referent_schema='qdb')