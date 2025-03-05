import asyncio
import asyncpg

async def create_test_table():
    """Create a test table directly in the database."""
    print("Creating test table in crown_nexus database...")

    conn = await asyncpg.connect(
        user="postgres",
        password="postgres",
        host="localhost",
        database="crown_nexus"
    )

    try:
        # Create a simple test table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Test table created successfully.")

        # Insert a test row
        await conn.execute("""
            INSERT INTO test_table (name) VALUES ('Test Entry');
        """)
        print("Test row inserted successfully.")

        # Verify the table exists
        exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'test_table'
            );
        """)

        if exists:
            print("✅ Confirmed test_table exists in the database.")
        else:
            print("❌ Could not find test_table in the database!")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_test_table())
