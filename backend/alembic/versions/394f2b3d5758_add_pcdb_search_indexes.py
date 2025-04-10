# migrations/versions/xxxx_add_pcdb_search_indexes.py
"""Add PCDB full-text search indexes for names and descriptions

Revision ID: xxxx
Revises: <previous_revision_id>
Create Date: 2025-04-10

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = "394f2b3d5758"  # You'll get a unique ID when generating with alembic
down_revision = "4ae566f159b4"  # The previous migration in your chain
branch_labels = None
depends_on = None


def upgrade():
    # Create the pg_trgm extension if it doesn't exist
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # --- Indexes for part_terminology_name ---

    # Create a GIN index for full-text search on part names
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_parts_name_fts ON pcdb.parts "
        "USING gin(to_tsvector('english', part_terminology_name))"
    )

    # Create a GIN index for trigram similarity searches on part names
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_parts_name_trgm ON pcdb.parts "
        "USING gin(part_terminology_name gin_trgm_ops)"
    )

    # For case-insensitive searches on part names
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_parts_name_lower ON pcdb.parts "
        "USING btree(lower(part_terminology_name))"
    )

    # --- Indexes for parts_description ---

    # Create a GIN index for full-text search on descriptions
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_parts_description_fts ON pcdb.parts_description "
        "USING gin(to_tsvector('english', parts_description))"
    )

    # Create a GIN index for trigram similarity searches on descriptions
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_parts_description_trgm ON pcdb.parts_description "
        "USING gin(parts_description gin_trgm_ops)"
    )

    # For case-insensitive searches on descriptions
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_parts_description_lower ON pcdb.parts_description "
        "USING btree(lower(parts_description))"
    )

    # Run ANALYZE to update statistics
    op.execute("ANALYZE pcdb.parts")
    op.execute("ANALYZE pcdb.parts_description")


def downgrade():
    # Drop part name indexes
    op.execute("DROP INDEX IF EXISTS pcdb.idx_parts_name_fts")
    op.execute("DROP INDEX IF EXISTS pcdb.idx_parts_name_trgm")
    op.execute("DROP INDEX IF EXISTS pcdb.idx_parts_name_lower")

    # Drop description indexes
    op.execute("DROP INDEX IF EXISTS pcdb.idx_parts_description_fts")
    op.execute("DROP INDEX IF EXISTS pcdb.idx_parts_description_trgm")
    op.execute("DROP INDEX IF EXISTS pcdb.idx_parts_description_lower")

    # Note: We typically don't drop the pg_trgm extension in downgrade
    # as other parts of the system might be using it
