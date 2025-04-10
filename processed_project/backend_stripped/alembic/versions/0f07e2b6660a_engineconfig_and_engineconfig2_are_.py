from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = '0f07e2b6660a'
down_revision: Union[str, None] = '98e9c3581d8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.drop_constraint('vehicle_to_engine_config_engine_config_id_fkey', 'vehicle_to_engine_config', schema='vcdb', type_='foreignkey')
    op.create_foreign_key(None, 'vehicle_to_engine_config', 'engine_config2', ['engine_config_id'], ['engine_config_id'], source_schema='vcdb', referent_schema='vcdb')
def downgrade() -> None:
    op.drop_constraint(None, 'vehicle_to_engine_config', schema='vcdb', type_='foreignkey')
    op.create_foreign_key('vehicle_to_engine_config_engine_config_id_fkey', 'vehicle_to_engine_config', 'engine_config', ['engine_config_id'], ['engine_config_id'], source_schema='vcdb', referent_schema='vcdb')