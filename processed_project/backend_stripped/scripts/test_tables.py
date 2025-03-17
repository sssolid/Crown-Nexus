import asyncio
import asyncpg
async def create_test_table():
    print('Creating test table in crown_nexus database...')
    conn = await asyncpg.connect(user='postgres', password='postgres', host='localhost', database='crown_nexus')
    try:
        await conn.execute('\n            CREATE TABLE IF NOT EXISTS test_table (\n                id SERIAL PRIMARY KEY,\n                name TEXT NOT NULL,\n                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n            );\n        ')
        print('Test table created successfully.')
        await conn.execute("\n            INSERT INTO test_table (name) VALUES ('Test Entry');\n        ")
        print('Test row inserted successfully.')
        exists = await conn.fetchval("\n            SELECT EXISTS (\n                SELECT FROM information_schema.tables\n                WHERE table_schema = 'public'\n                AND table_name = 'test_table'\n            );\n        ")
        if exists:
            print('✅ Confirmed test_table exists in the database.')
        else:
            print('❌ Could not find test_table in the database!')
    finally:
        await conn.close()
if __name__ == '__main__':
    asyncio.run(create_test_table())