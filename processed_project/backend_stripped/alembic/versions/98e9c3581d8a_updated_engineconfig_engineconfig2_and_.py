from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = '98e9c3581d8a'
down_revision: Union[str, None] = '660598405145'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.create_table('engine_base2', sa.Column('id', sa.UUID(), nullable=False), sa.Column('engine_base_id', sa.Integer(), nullable=False), sa.Column('engine_block_id', sa.Integer(), nullable=False), sa.Column('engine_bore_stroke_id', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('is_deleted', sa.Boolean(), nullable=False), sa.Column('created_by_id', sa.UUID(), nullable=True), sa.Column('updated_by_id', sa.UUID(), nullable=True), sa.ForeignKeyConstraint(['engine_block_id'], ['vcdb.engine_block.engine_block_id']), sa.ForeignKeyConstraint(['engine_bore_stroke_id'], ['vcdb.engine_bore_stroke.engine_bore_stroke_id']), sa.PrimaryKeyConstraint('id'), schema='vcdb')
    op.create_index(op.f('ix_vcdb_engine_base2_engine_base_id'), 'engine_base2', ['engine_base_id'], unique=True, schema='vcdb')
    op.create_index(op.f('ix_vcdb_engine_base2_is_deleted'), 'engine_base2', ['is_deleted'], unique=False, schema='vcdb')
    op.create_table('engine_config2', sa.Column('id', sa.UUID(), nullable=False), sa.Column('engine_config_id', sa.Integer(), nullable=False), sa.Column('engine_base_id', sa.Integer(), nullable=False), sa.Column('engine_block_id', sa.Integer(), nullable=False), sa.Column('engine_bore_stroke_id', sa.Integer(), nullable=False), sa.Column('engine_designation_id', sa.Integer(), nullable=False), sa.Column('engine_vin_id', sa.Integer(), nullable=False), sa.Column('valves_id', sa.Integer(), nullable=False), sa.Column('fuel_delivery_config_id', sa.Integer(), nullable=False), sa.Column('aspiration_id', sa.Integer(), nullable=False), sa.Column('cylinder_head_type_id', sa.Integer(), nullable=False), sa.Column('fuel_type_id', sa.Integer(), nullable=False), sa.Column('ignition_system_type_id', sa.Integer(), nullable=False), sa.Column('engine_mfr_id', sa.Integer(), nullable=False), sa.Column('engine_version_id', sa.Integer(), nullable=False), sa.Column('power_output_id', sa.Integer(), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('is_deleted', sa.Boolean(), nullable=False), sa.Column('created_by_id', sa.UUID(), nullable=True), sa.Column('updated_by_id', sa.UUID(), nullable=True), sa.ForeignKeyConstraint(['aspiration_id'], ['vcdb.aspiration.aspiration_id']), sa.ForeignKeyConstraint(['cylinder_head_type_id'], ['vcdb.cylinder_head_type.cylinder_head_type_id']), sa.ForeignKeyConstraint(['engine_base_id'], ['vcdb.engine_base2.engine_base_id']), sa.ForeignKeyConstraint(['engine_block_id'], ['vcdb.engine_block.engine_block_id']), sa.ForeignKeyConstraint(['engine_bore_stroke_id'], ['vcdb.engine_bore_stroke.engine_bore_stroke_id']), sa.ForeignKeyConstraint(['engine_designation_id'], ['vcdb.engine_designation.engine_designation_id']), sa.ForeignKeyConstraint(['engine_mfr_id'], ['vcdb.mfr.mfr_id']), sa.ForeignKeyConstraint(['engine_version_id'], ['vcdb.engine_version.engine_version_id']), sa.ForeignKeyConstraint(['engine_vin_id'], ['vcdb.engine_vin.engine_vin_id']), sa.ForeignKeyConstraint(['fuel_delivery_config_id'], ['vcdb.fuel_delivery_config.fuel_delivery_config_id']), sa.ForeignKeyConstraint(['fuel_type_id'], ['vcdb.fuel_type.fuel_type_id']), sa.ForeignKeyConstraint(['ignition_system_type_id'], ['vcdb.ignition_system_type.ignition_system_type_id']), sa.ForeignKeyConstraint(['power_output_id'], ['vcdb.power_output.power_output_id']), sa.ForeignKeyConstraint(['valves_id'], ['vcdb.valves.valves_id']), sa.PrimaryKeyConstraint('id'), schema='vcdb')
    op.create_index(op.f('ix_vcdb_engine_config2_engine_config_id'), 'engine_config2', ['engine_config_id'], unique=True, schema='vcdb')
    op.create_index(op.f('ix_vcdb_engine_config2_is_deleted'), 'engine_config2', ['is_deleted'], unique=False, schema='vcdb')
    op.add_column('engine_base', sa.Column('liter', sa.String(length=10), nullable=False), schema='vcdb')
    op.add_column('engine_base', sa.Column('cc', sa.String(length=10), nullable=False), schema='vcdb')
    op.add_column('engine_base', sa.Column('cid', sa.String(length=10), nullable=False), schema='vcdb')
    op.add_column('engine_base', sa.Column('cylinders', sa.String(length=10), nullable=False), schema='vcdb')
    op.add_column('engine_base', sa.Column('block_type', sa.String(length=10), nullable=False), schema='vcdb')
    op.add_column('engine_base', sa.Column('eng_bore_in', sa.String(length=10), nullable=False), schema='vcdb')
    op.add_column('engine_base', sa.Column('eng_bore_metric', sa.String(length=10), nullable=False), schema='vcdb')
    op.add_column('engine_base', sa.Column('eng_stroke_in', sa.String(length=10), nullable=False), schema='vcdb')
    op.add_column('engine_base', sa.Column('eng_stroke_metric', sa.String(length=10), nullable=False), schema='vcdb')
def downgrade() -> None:
    op.drop_column('engine_base', 'eng_stroke_metric', schema='vcdb')
    op.drop_column('engine_base', 'eng_stroke_in', schema='vcdb')
    op.drop_column('engine_base', 'eng_bore_metric', schema='vcdb')
    op.drop_column('engine_base', 'eng_bore_in', schema='vcdb')
    op.drop_column('engine_base', 'block_type', schema='vcdb')
    op.drop_column('engine_base', 'cylinders', schema='vcdb')
    op.drop_column('engine_base', 'cid', schema='vcdb')
    op.drop_column('engine_base', 'cc', schema='vcdb')
    op.drop_column('engine_base', 'liter', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_engine_config2_is_deleted'), table_name='engine_config2', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_engine_config2_engine_config_id'), table_name='engine_config2', schema='vcdb')
    op.drop_table('engine_config2', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_engine_base2_is_deleted'), table_name='engine_base2', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_engine_base2_engine_base_id'), table_name='engine_base2', schema='vcdb')
    op.drop_table('engine_base2', schema='vcdb')