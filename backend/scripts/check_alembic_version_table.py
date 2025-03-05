import asyncio
import asyncpg

async def check_alembic_version():
    """Check if the alembic_version table exists and its contents."""
    print("Checking alembic_version table...")

    conn = await asyncpg.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        database="crown_nexus"
    )

    try:
        # Check if alembic_version table exists
        table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'alembic_version'
            );
        """)

        if not table_exists:
            print("❌ alembic_version table does not exist!")
            print("This suggests Alembic migrations are not being properly applied.")
            return

        # Get the current version
        version_num = await conn.fetchval("SELECT version_num FROM alembic_version;")
        print(f"✅ alembic_version table exists with version: {version_num}")

        # List all tables again to see if anything exists
        tables = await conn.fetch("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        print(f"\nFound {len(tables)} tables in the public schema:")
        for table in tables:
            print(f"  - {table['table_name']}")

    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_alembic_version())
