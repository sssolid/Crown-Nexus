import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
async def test_fixed_config():
    print(f'Database URI from settings: {settings.SQLALCHEMY_DATABASE_URI}')
    engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text('SELECT current_database()'))
            db_name = result.scalar_one()
            print(f'Connected to database: {db_name}')
            result = await conn.execute(text("\n                SELECT table_name\n                FROM information_schema.tables\n                WHERE table_schema = 'public'\n                ORDER BY table_name;\n            "))
            tables = result.fetchall()
            print(f'Tables in database ({len(tables)}):')
            for table in tables:
                print(f'  - {table[0]}')
        print('✅ Connection with fixed config successful!')
    except Exception as e:
        print(f'❌ Connection failed: {e}')
    finally:
        await engine.dispose()
if __name__ == '__main__':
    asyncio.run(test_fixed_config())