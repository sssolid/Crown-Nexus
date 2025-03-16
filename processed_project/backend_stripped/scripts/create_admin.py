import asyncio
import sys
from pathlib import Path
import asyncpg
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.config import settings
from app.db.session import async_session
from app.models.user import User, UserRole, get_password_hash
async def create_admin_user(email: str, password: str, full_name: str) -> None:
    try:
        engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            if user:
                print(f'User with email {email} already exists.')
                return
            hashed_password = get_password_hash(password)
            user = User(email=email, hashed_password=hashed_password, full_name=full_name, role=UserRole.ADMIN, is_active=True)
            session.add(user)
            await session.commit()
            print(f'Admin user {email} created successfully.')
    except Exception as e:
        print(f'Error creating admin user: {e}')
def print_usage() -> None:
    print('Usage: python create_admin.py email password full_name')
    print("Example: python create_admin.py admin@example.com password123 'Admin User'")
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)
    email = sys.argv[1]
    password = sys.argv[2]
    full_name = sys.argv[3]
    asyncio.run(create_admin_user(email, password, full_name))