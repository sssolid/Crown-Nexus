import asyncio
import asyncpg
async def check_alembic_version():
    print('Checking alembic_version table...')
    conn = await asyncpg.connect(user='postgres', password='postgres', host='localhost', database='crown_nexus')
    try:
        table_exists = await conn.fetchval("\n            SELECT EXISTS (\n                SELECT FROM information_schema.tables\n                WHERE table_schema = 'public'\n                AND table_name = 'alembic_version'\n            );\n        ")
        if not table_exists:
            print('❌ alembic_version table does not exist!')
            print('This suggests Alembic migrations are not being properly applied.')
            return
        version_num = await conn.fetchval('SELECT version_num FROM alembic_version;')
        print(f'✅ alembic_version table exists with version: {version_num}')
        tables = await conn.fetch("\n            SELECT table_name\n            FROM information_schema.tables\n            WHERE table_schema = 'public'\n            ORDER BY table_name;\n        ")
        print(f'\nFound {len(tables)} tables in the public schema:')
        for table in tables:
            print(f'  - {table['table_name']}')
    finally:
        await conn.close()
if __name__ == '__main__':
    asyncio.run(check_alembic_version())