from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision: str = 'cca5aa1d9538'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade() -> None:
    op.create_table('category', sa.Column('id', sa.UUID(), nullable=False), sa.Column('name', sa.String(length=100), nullable=False), sa.Column('slug', sa.String(length=100), nullable=False), sa.Column('parent_id', sa.UUID(), nullable=True), sa.Column('description', sa.String(length=500), nullable=True), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.ForeignKeyConstraint(['parent_id'], ['category.id']), sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_category_slug'), 'category', ['slug'], unique=True)
    op.create_table('company', sa.Column('id', sa.UUID(), nullable=False), sa.Column('name', sa.String(length=255), nullable=False), sa.Column('account_number', sa.String(length=50), nullable=True), sa.Column('account_type', sa.String(length=50), nullable=False), sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_company_account_number'), 'company', ['account_number'], unique=True)
    op.create_table('fitment', sa.Column('id', sa.UUID(), nullable=False), sa.Column('year', sa.Integer(), nullable=False), sa.Column('make', sa.String(length=100), nullable=False), sa.Column('model', sa.String(length=100), nullable=False), sa.Column('engine', sa.String(length=100), nullable=True), sa.Column('transmission', sa.String(length=100), nullable=True), sa.Column('attributes', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_fitment_engine'), 'fitment', ['engine'], unique=False)
    op.create_index(op.f('ix_fitment_make'), 'fitment', ['make'], unique=False)
    op.create_index(op.f('ix_fitment_model'), 'fitment', ['model'], unique=False)
    op.create_index(op.f('ix_fitment_transmission'), 'fitment', ['transmission'], unique=False)
    op.create_index(op.f('ix_fitment_year'), 'fitment', ['year'], unique=False)
    op.create_table('product', sa.Column('id', sa.UUID(), nullable=False), sa.Column('sku', sa.String(length=50), nullable=False), sa.Column('name', sa.String(length=255), nullable=False), sa.Column('description', sa.String(length=2000), nullable=True), sa.Column('part_number', sa.String(length=100), nullable=True), sa.Column('category_id', sa.UUID(), nullable=True), sa.Column('attributes', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False), sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.ForeignKeyConstraint(['category_id'], ['category.id']), sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_product_part_number'), 'product', ['part_number'], unique=False)
    op.create_index(op.f('ix_product_sku'), 'product', ['sku'], unique=True)
    op.create_table('user', sa.Column('id', sa.UUID(), nullable=False), sa.Column('email', sa.String(length=255), nullable=False), sa.Column('hashed_password', sa.String(length=255), nullable=False), sa.Column('full_name', sa.String(length=255), nullable=False), sa.Column('role', sa.Enum('ADMIN', 'MANAGER', 'CLIENT', 'DISTRIBUTOR', 'READ_ONLY', name='userrole'), nullable=False), sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False), sa.Column('company_id', sa.UUID(), nullable=True), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.ForeignKeyConstraint(['company_id'], ['company.id']), sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('media', sa.Column('id', sa.UUID(), nullable=False), sa.Column('filename', sa.String(length=255), nullable=False), sa.Column('file_path', sa.String(length=512), nullable=False), sa.Column('file_size', sa.Integer(), nullable=False), sa.Column('media_type', sa.Enum('IMAGE', 'DOCUMENT', 'VIDEO', 'OTHER', name='mediatype'), nullable=False), sa.Column('mime_type', sa.String(length=127), nullable=False), sa.Column('visibility', sa.Enum('PUBLIC', 'PRIVATE', 'RESTRICTED', name='mediavisibility'), nullable=False), sa.Column('file_metadata', postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False), sa.Column('uploaded_by_id', sa.UUID(), nullable=False), sa.Column('is_approved', sa.Boolean(), server_default=sa.text('false'), nullable=False), sa.Column('approved_by_id', sa.UUID(), nullable=True), sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True), sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False), sa.ForeignKeyConstraint(['approved_by_id'], ['user.id']), sa.ForeignKeyConstraint(['uploaded_by_id'], ['user.id']), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('file_path'))
    op.create_table('product_fitment', sa.Column('product_id', sa.UUID(), nullable=False), sa.Column('fitment_id', sa.UUID(), nullable=False), sa.ForeignKeyConstraint(['fitment_id'], ['fitment.id'], ondelete='CASCADE'), sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'), sa.PrimaryKeyConstraint('product_id', 'fitment_id'))
    op.create_table('product_media', sa.Column('product_id', sa.UUID(), nullable=False), sa.Column('media_id', sa.UUID(), nullable=False), sa.ForeignKeyConstraint(['media_id'], ['media.id'], ondelete='CASCADE'), sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'), sa.PrimaryKeyConstraint('product_id', 'media_id'))
def downgrade() -> None:
    op.drop_table('product_media')
    op.drop_table('product_fitment')
    op.drop_table('media')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_product_sku'), table_name='product')
    op.drop_index(op.f('ix_product_part_number'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_fitment_year'), table_name='fitment')
    op.drop_index(op.f('ix_fitment_transmission'), table_name='fitment')
    op.drop_index(op.f('ix_fitment_model'), table_name='fitment')
    op.drop_index(op.f('ix_fitment_make'), table_name='fitment')
    op.drop_index(op.f('ix_fitment_engine'), table_name='fitment')
    op.drop_table('fitment')
    op.drop_index(op.f('ix_company_account_number'), table_name='company')
    op.drop_table('company')
    op.drop_index(op.f('ix_category_slug'), table_name='category')
    op.drop_table('category')