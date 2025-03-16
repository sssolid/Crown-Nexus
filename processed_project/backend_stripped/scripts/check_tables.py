import asyncio
import asyncpg
async def check_tables():
    print('Checking tables in crown_nexus database...')
    conn = await asyncpg.connect(user='postgres', password='postgres', host='localhost', database='crown_nexus')
    try:
        tables = await conn.fetch("\n            SELECT table_name\n            FROM information_schema.tables\n            WHERE table_schema = 'public';\n        ")
        if tables:
            print(f'Found {len(tables)} tables:')
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print('No tables found in the public schema.')
        schemas = await conn.fetch("\n            SELECT DISTINCT table_schema\n            FROM information_schema.tables\n            WHERE table_schema NOT IN ('pg_catalog', 'information_schema');\n        ")
        if len(schemas) > 1 or (len(schemas) == 1 and schemas[0]['table_schema'] != 'public'):
            print('\nFound tables in other schemas:')
            for schema in schemas:
                schema_name = schema['table_schema']
                if schema_name != 'public':
                    schema_tables = await conn.fetch(f"\n                        SELECT table_name\n                        FROM information_schema.tables\n                        WHERE table_schema = '{schema_name}';\n                    ")
                    print(f"Schema '{schema_name}': {len(schema_tables)} tables")
                    for table in schema_tables:
                        print(f"  - {table['table_name']}")
    finally:
        await conn.close()
if __name__ == '__main__':
    asyncio.run(check_tables())