from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = '394f2b3d5758'
down_revision = '4ae566f159b4'
branch_labels = None
depends_on = None
def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
    op.execute("CREATE INDEX IF NOT EXISTS idx_parts_name_fts ON pcdb.parts USING gin(to_tsvector('english', part_terminology_name))")
    op.execute('CREATE INDEX IF NOT EXISTS idx_parts_name_trgm ON pcdb.parts USING gin(part_terminology_name gin_trgm_ops)')
    op.execute('CREATE INDEX IF NOT EXISTS idx_parts_name_lower ON pcdb.parts USING btree(lower(part_terminology_name))')
    op.execute("CREATE INDEX IF NOT EXISTS idx_parts_description_fts ON pcdb.parts_description USING gin(to_tsvector('english', parts_description))")
    op.execute('CREATE INDEX IF NOT EXISTS idx_parts_description_trgm ON pcdb.parts_description USING gin(parts_description gin_trgm_ops)')
    op.execute('CREATE INDEX IF NOT EXISTS idx_parts_description_lower ON pcdb.parts_description USING btree(lower(parts_description))')
    op.execute('ANALYZE pcdb.parts')
    op.execute('ANALYZE pcdb.parts_description')
def downgrade():
    op.execute('DROP INDEX IF EXISTS pcdb.idx_parts_name_fts')
    op.execute('DROP INDEX IF EXISTS pcdb.idx_parts_name_trgm')
    op.execute('DROP INDEX IF EXISTS pcdb.idx_parts_name_lower')
    op.execute('DROP INDEX IF EXISTS pcdb.idx_parts_description_fts')
    op.execute('DROP INDEX IF EXISTS pcdb.idx_parts_description_trgm')
    op.execute('DROP INDEX IF EXISTS pcdb.idx_parts_description_lower')