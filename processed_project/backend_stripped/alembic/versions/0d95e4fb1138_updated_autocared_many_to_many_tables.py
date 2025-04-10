from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = '0d95e4fb1138'
down_revision: Union[str, None] = 'db7baed1531c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.add_column('vehicle_to_bed_config', sa.Column('vehicle_to_bed_config_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_bed_config_vehicle_to_bed_config_id'), 'vehicle_to_bed_config', ['vehicle_to_bed_config_id'], unique=True, schema='vcdb')
    op.add_column('vehicle_to_body_style_config', sa.Column('vehicle_to_body_style_config_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_body_style_config_vehicle_to_body_style_config_id'), 'vehicle_to_body_style_config', ['vehicle_to_body_style_config_id'], unique=True, schema='vcdb')
    op.add_column('vehicle_to_brake_config', sa.Column('vehicle_to_brake_config_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_brake_config_vehicle_to_brake_config_id'), 'vehicle_to_brake_config', ['vehicle_to_brake_config_id'], unique=True, schema='vcdb')
    op.add_column('vehicle_to_drive_type', sa.Column('vehicle_to_drive_type_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_drive_type_vehicle_to_drive_type_id'), 'vehicle_to_drive_type', ['vehicle_to_drive_type_id'], unique=True, schema='vcdb')
    op.add_column('vehicle_to_engine_config', sa.Column('vehicle_to_engine_config_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_engine_config_vehicle_to_engine_config_id'), 'vehicle_to_engine_config', ['vehicle_to_engine_config_id'], unique=True, schema='vcdb')
    op.add_column('vehicle_to_mfr_body_code', sa.Column('vehicle_to_mfr_body_code_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_mfr_body_code_vehicle_to_mfr_body_code_id'), 'vehicle_to_mfr_body_code', ['vehicle_to_mfr_body_code_id'], unique=True, schema='vcdb')
    op.add_column('vehicle_to_spring_type_config', sa.Column('vehicle_to_spring_type_config_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_spring_type_config_vehicle_to_spring_type_config_id'), 'vehicle_to_spring_type_config', ['vehicle_to_spring_type_config_id'], unique=True, schema='vcdb')
    op.add_column('vehicle_to_steering_config', sa.Column('vehicle_to_steering_config_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_steering_config_vehicle_to_steering_config_id'), 'vehicle_to_steering_config', ['vehicle_to_steering_config_id'], unique=True, schema='vcdb')
    op.add_column('vehicle_to_transmission', sa.Column('vehicle_to_transmission_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_transmission_vehicle_to_transmission_id'), 'vehicle_to_transmission', ['vehicle_to_transmission_id'], unique=True, schema='vcdb')
    op.add_column('vehicle_to_wheel_base', sa.Column('vehicle_to_wheel_base_id', sa.Integer(), nullable=False), schema='vcdb')
    op.create_index(op.f('ix_vcdb_vehicle_to_wheel_base_vehicle_to_wheel_base_id'), 'vehicle_to_wheel_base', ['vehicle_to_wheel_base_id'], unique=True, schema='vcdb')
def downgrade() -> None:
    op.drop_index(op.f('ix_vcdb_vehicle_to_wheel_base_vehicle_to_wheel_base_id'), table_name='vehicle_to_wheel_base', schema='vcdb')
    op.drop_column('vehicle_to_wheel_base', 'vehicle_to_wheel_base_id', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_vehicle_to_transmission_vehicle_to_transmission_id'), table_name='vehicle_to_transmission', schema='vcdb')
    op.drop_column('vehicle_to_transmission', 'vehicle_to_transmission_id', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_vehicle_to_steering_config_vehicle_to_steering_config_id'), table_name='vehicle_to_steering_config', schema='vcdb')
    op.drop_column('vehicle_to_steering_config', 'vehicle_to_steering_config_id', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_vehicle_to_spring_type_config_vehicle_to_spring_type_config_id'), table_name='vehicle_to_spring_type_config', schema='vcdb')
    op.drop_column('vehicle_to_spring_type_config', 'vehicle_to_spring_type_config_id', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_vehicle_to_mfr_body_code_vehicle_to_mfr_body_code_id'), table_name='vehicle_to_mfr_body_code', schema='vcdb')
    op.drop_column('vehicle_to_mfr_body_code', 'vehicle_to_mfr_body_code_id', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_vehicle_to_engine_config_vehicle_to_engine_config_id'), table_name='vehicle_to_engine_config', schema='vcdb')
    op.drop_column('vehicle_to_engine_config', 'vehicle_to_engine_config_id', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_vehicle_to_drive_type_vehicle_to_drive_type_id'), table_name='vehicle_to_drive_type', schema='vcdb')
    op.drop_column('vehicle_to_drive_type', 'vehicle_to_drive_type_id', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_vehicle_to_brake_config_vehicle_to_brake_config_id'), table_name='vehicle_to_brake_config', schema='vcdb')
    op.drop_column('vehicle_to_brake_config', 'vehicle_to_brake_config_id', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_vehicle_to_body_style_config_vehicle_to_body_style_config_id'), table_name='vehicle_to_body_style_config', schema='vcdb')
    op.drop_column('vehicle_to_body_style_config', 'vehicle_to_body_style_config_id', schema='vcdb')
    op.drop_index(op.f('ix_vcdb_vehicle_to_bed_config_vehicle_to_bed_config_id'), table_name='vehicle_to_bed_config', schema='vcdb')
    op.drop_column('vehicle_to_bed_config', 'vehicle_to_bed_config_id', schema='vcdb')