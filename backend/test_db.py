import asyncio
import asyncpg
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def test_connection():
    print("Testing database connection...")
    try:
        # Try direct asyncpg connection
        conn = await asyncpg.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            database="crown_nexus"
        )
        await conn.execute("SELECT 1")
        await conn.close()
        print("✅ Direct asyncpg connection successful!")

        # Try SQLAlchemy connection
        engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/crown_nexus")
        async with engine.begin() as conn:
            # Use text() for raw SQL
            await conn.execute(text("SELECT 1"))
        print("✅ SQLAlchemy connection successful!")

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_connection())
