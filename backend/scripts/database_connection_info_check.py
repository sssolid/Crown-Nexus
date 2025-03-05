import asyncio
import asyncpg

async def print_database_info():
    """Print detailed information about the database connection."""
    print("Connecting to database to get info...")

    conn = await asyncpg.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        database="crown_nexus"
    )

    try:
        # Get server version
        version = await conn.fetchval("SELECT version();")
        print(f"PostgreSQL version: {version}")

        # Get current database
        db_name = await conn.fetchval("SELECT current_database();")
        print(f"Connected to database: {db_name}")

        # Get current schema search path
        search_path = await conn.fetchval("SHOW search_path;")
        print(f"Schema search path: {search_path}")

        # List all schemas
        schemas = await conn.fetch("""
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
            ORDER BY schema_name;
        """)

        print(f"\nAvailable schemas ({len(schemas)}):")
        for schema in schemas:
            schema_name = schema['schema_name']
            # Count tables in this schema
            table_count = await conn.fetchval(f"""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = '{schema_name}';
            """)
            print(f"  - {schema_name} ({table_count} tables)")

        # Get current user and privileges
        user = await conn.fetchval("SELECT current_user;")
        print(f"\nConnected as user: {user}")

        # Get all tables for the current user
        tables = await conn.fetch("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
            AND table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name;
        """)

        print(f"\nAll tables accessible by current user ({len(tables)}):")
        current_schema = None
        for table in tables:
            schema = table['table_schema']
            if schema != current_schema:
                current_schema = schema
                print(f"\n  Schema: {schema}")
            print(f"    - {table['table_name']}")

    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(print_database_info())
