"""Enhanced product model schema

Revision ID: 5f6c26d3a2c1
Revises: # You should fill in the parent revision ID
Create Date: 2025-03-14T12:00:00.000Z

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5f6c26d3a2c1'
down_revision: Union[str, None] = None  # Fill in the parent revision ID
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop old tables if they exist
    # (we'll handle this carefully in a real scenario)
    # op.drop_table('product')
    # op.drop_table('category')

    # Create new tables first
    op.create_table(
        'brand',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('parent_company_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['parent_company_id'], ['company.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_brand_name', 'brand', ['name'])

    # Create enhanced product table
    op.create_table(
        'product',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('part_number', sa.String(50), nullable=False),
        sa.Column('part_number_stripped', sa.String(50), nullable=False),
        sa.Column('application', sa.Text(), nullable=True),
        sa.Column('vintage', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('late_model', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('soft', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('universal', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['category.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_product_part_number', 'product', ['part_number'], unique=True)
    op.create_index('idx_product_part_number_stripped', 'product', ['part_number_stripped'])
    op.create_index('products_search_idx', 'product', ['search_vector'], postgresql_using='gin')

    # Create product description table
    op.create_table(
        'product_description',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('description_type', sa.String(20), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_product_description_product_id', 'product_description', ['product_id'])
    op.create_index('idx_product_description_type', 'product_description', ['description_type'])

    # Create product marketing table
    op.create_table(
        'product_marketing',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('marketing_type', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_product_marketing_product_id', 'product_marketing', ['product_id'])
    op.create_index('idx_product_marketing_position', 'product_marketing', ['position'])

    # Create product activity table
    op.create_table(
        'product_activity',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('changed_by_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['changed_by_id'], ['user.id']),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_product_activity_product_id', 'product_activity', ['product_id'])
    op.create_index('idx_product_activity_status', 'product_activity', ['status'])
    op.create_index('idx_product_activity_changed_at', 'product_activity', ['changed_at'])

    # Create product supersession table
    op.create_table(
        'product_supersession',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('old_product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('new_product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['old_product_id'], ['product.id']),
        sa.ForeignKeyConstraint(['new_product_id'], ['product.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_product_supersession_old_product_id', 'product_supersession', ['old_product_id'])
    op.create_index('idx_product_supersession_new_product_id', 'product_supersession', ['new_product_id'])

    # Create product brand history table
    op.create_table(
        'product_brand_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('old_brand_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('new_brand_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('changed_by_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['changed_by_id'], ['user.id']),
        sa.ForeignKeyConstraint(['product_id'], ['product.id']),
        sa.ForeignKeyConstraint(['old_brand_id'], ['brand.id']),
        sa.ForeignKeyConstraint(['new_brand_id'], ['brand.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_product_brand_history_product_id', 'product_brand_history', ['product_id'])
    op.create_index('idx_product_brand_history_changed_at', 'product_brand_history', ['changed_at'])

    # Create manufacturer table
    op.create_table(
        'manufacturer',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('address_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('billing_address_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('shipping_address_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('country_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['company_id'], ['company.id']),
        sa.ForeignKeyConstraint(['address_id'], ['address.id']),
        sa.ForeignKeyConstraint(['billing_address_id'], ['address.id']),
        sa.ForeignKeyConstraint(['shipping_address_id'], ['address.id']),
        sa.ForeignKeyConstraint(['country_id'], ['country.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_manufacturers_name', 'manufacturer', ['name'])
    op.create_index('idx_manufacturers_company_id', 'manufacturer', ['company_id'])
    op.create_index('idx_manufacturers_country_id', 'manufacturer', ['country_id'])

    # Create price type table
    op.create_table(
        'price_type',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_price_types_name', 'price_type', ['name'], unique=True)

    # Create product pricing table
    op.create_table(
        'product_pricing',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pricing_type_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('manufacturer_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('currency', sa.String(3), server_default=sa.text("'USD'"), nullable=False),
        sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pricing_type_id'], ['price_type.id']),
        sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturer.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_product_pricing_product_id', 'product_pricing', ['product_id'])
    op.create_index('idx_product_pricing_pricing_type_id', 'product_pricing', ['pricing_type_id'])
    op.create_index('idx_product_pricing_manufacturer_id', 'product_pricing', ['manufacturer_id'])

    # Create product measurement table
    op.create_table(
        'product_measurement',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('manufacturer_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('length', sa.Numeric(10, 3), nullable=True),
        sa.Column('width', sa.Numeric(10, 3), nullable=True),
        sa.Column('height', sa.Numeric(10, 3), nullable=True),
        sa.Column('weight', sa.Numeric(10, 3), nullable=True),
        sa.Column('volume', sa.Numeric(10, 3), nullable=True),
        sa.Column('dimensional_weight', sa.Numeric(10, 3), nullable=True),
        sa.Column('effective_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturer.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_product_measurements_product_id', 'product_measurement', ['product_id'])
    op.create_index('idx_product_measurements_manufacturer_id', 'product_measurement', ['manufacturer_id'])
    op.create_index('idx_product_measurements_effective_date', 'product_measurement', ['effective_date'])

    # Create warehouse table
    op.create_table(
        'warehouse',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('address_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['address_id'], ['address.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_warehouses_name', 'warehouse', ['name'])
    op.create_index('idx_warehouses_is_active', 'warehouse', ['is_active'])

    # Create product stock table
    op.create_table(
        'product_stock',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('warehouse_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('quantity', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouse.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('idx_product_stock_product_id', 'product_stock', ['product_id'])
    op.create_index('idx_product_stock_warehouse_id', 'product_stock', ['warehouse_id'])
    op.create_index('idx_product_stock_quantity', 'product_stock', ['quantity'])

    # Create attribute definition table
    op.create_table(
        'attribute_definition',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('code', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('data_type', sa.String(20), nullable=False),
        sa.Column('is_required', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('default_value', sa.Text(), nullable=True),
        sa.Column('validation_regex', sa.Text(), nullable=True),
        sa.Column('min_value', sa.Numeric(), nullable=True),
        sa.Column('max_value', sa.Numeric(), nullable=True),
        sa.Column('options', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('display_order', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )

    op.create_index('idx_attribute_definitions_code', 'attribute_definition', ['code'])
    op.create_index('idx_attribute_definitions_data_type', 'attribute_definition', ['data_type'])
    op.create_index('idx_attribute_definitions_display_order', 'attribute_definition', ['display_order'])

    # Create product attribute table
    op.create_table(
        'product_attribute',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('attribute_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('value_string', sa.Text(), nullable=True),
        sa.Column('value_number', sa.Numeric(), nullable=True),
        sa.Column('value_boolean', sa.Boolean(), nullable=True),
        sa.Column('value_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('value_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['attribute_id'], ['attribute_definition.id']),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('product_id', 'attribute_id')
    )

    op.create_index('idx_product_attributes_product_id', 'product_attribute', ['product_id'])
    op.create_index('idx_product_attributes_attribute_id', 'product_attribute', ['attribute_id'])
    op.create_index('idx_product_attributes_value_string', 'product_attribute', ['value_string'])
    op.create_index('idx_product_attributes_value_number', 'product_attribute', ['value_number'])
    op.create_index('idx_product_attributes_value_boolean', 'product_attribute', ['value_boolean'])
    op.create_index('idx_product_attributes_value_date', 'product_attribute', ['value_date'])

    # Create function to update product search vectors
    op.execute('''
    CREATE OR REPLACE FUNCTION products_search_vector_update() RETURNS trigger AS $$
    BEGIN
      NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.part_number, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.part_number_stripped, '')), 'A');
      RETURN NEW;
    END
    $$ LANGUAGE plpgsql;
    ''')

    # Create trigger to update product search vectors
    op.execute('''
    CREATE TRIGGER products_search_vector_update
    BEFORE INSERT OR UPDATE ON product
    FOR EACH ROW EXECUTE FUNCTION products_search_vector_update();
    ''')


def downgrade() -> None:
    # Drop triggers first
    op.execute('DROP TRIGGER IF EXISTS products_search_vector_update ON product;')
    op.execute('DROP FUNCTION IF EXISTS products_search_vector_update();')

    # Drop tables in reverse order of creation (respecting foreign key constraints)
    op.drop_table('product_attribute')
    op.drop_table('attribute_definition')
    op.drop_table('product_stock')
    op.drop_table('warehouse')
    op.drop_table('product_measurement')
    op.drop_table('product_pricing')
    op.drop_table('price_type')
    op.drop_table('manufacturer')
    op.drop_table('product_brand_history')
    op.drop_table('product_supersession')
    op.drop_table('product_activity')
    op.drop_table('product_marketing')
    op.drop_table('product_description')
    op.drop_table('product')
    op.drop_table('brand')
