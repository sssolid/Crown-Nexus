import asyncio
import asyncpg
async def print_database_info():
    print('Connecting to database to get info...')
    conn = await asyncpg.connect(user='postgres', password='postgres', host='localhost', database='crown_nexus')
    try:
        version = await conn.fetchval('SELECT version();')
        print(f'PostgreSQL version: {version}')
        db_name = await conn.fetchval('SELECT current_database();')
        print(f'Connected to database: {db_name}')
        search_path = await conn.fetchval('SHOW search_path;')
        print(f'Schema search path: {search_path}')
        schemas = await conn.fetch("\n            SELECT schema_name\n            FROM information_schema.schemata\n            WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')\n            ORDER BY schema_name;\n        ")
        print(f'\nAvailable schemas ({len(schemas)}):')
        for schema in schemas:
            schema_name = schema['schema_name']
            table_count = await conn.fetchval(f"\n                SELECT COUNT(*)\n                FROM information_schema.tables\n                WHERE table_schema = '{schema_name}';\n            ")
            print(f'  - {schema_name} ({table_count} tables)')
        user = await conn.fetchval('SELECT current_user;')
        print(f'\nConnected as user: {user}')
        tables = await conn.fetch("\n            SELECT table_schema, table_name\n            FROM information_schema.tables\n            WHERE table_type = 'BASE TABLE'\n            AND table_schema NOT IN ('pg_catalog', 'information_schema')\n            ORDER BY table_schema, table_name;\n        ")
        print(f'\nAll tables accessible by current user ({len(tables)}):')
        current_schema = None
        for table in tables:
            schema = table['table_schema']
            if schema != current_schema:
                current_schema = schema
                print(f'\n  Schema: {schema}')
            print(f'    - {table['table_name']}')
    finally:
        await conn.close()
if __name__ == '__main__':
    asyncio.run(print_database_info())