import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from app.core.config import settings
    print('== Database Connection Settings ==')
    print(f'POSTGRES_SERVER: {settings.POSTGRES_SERVER}')
    print(f'POSTGRES_USER: {settings.POSTGRES_USER}')
    print(f'POSTGRES_PASSWORD: {settings.POSTGRES_PASSWORD}')
    print(f'POSTGRES_DB: {settings.POSTGRES_DB}')
    print(f'SQLALCHEMY_DATABASE_URI: {settings.SQLALCHEMY_DATABASE_URI}')
    if settings.SQLALCHEMY_DATABASE_URI:
        uri = str(settings.SQLALCHEMY_DATABASE_URI)
        print('\n== Database URI Components ==')
        print(f'Full URI: {uri}')
        if '://' in uri:
            scheme, rest = uri.split('://', 1)
            print(f'Scheme: {scheme}')
            if '@' in rest:
                auth, location = rest.split('@', 1)
                print(f'Auth part: {auth}')
                if ':' in auth:
                    user, pwd = auth.split(':', 1)
                    print(f'Username: {user}')
                    print(f"Password: {'*' * len(pwd)}")
                if '/' in location:
                    host_port, db_path = location.split('/', 1)
                    print(f'Host/port: {host_port}')
                    print(f'Database path: {db_path}')
                    if db_path.startswith('/'):
                        print('⚠️ WARNING: Database path starts with a slash, which may cause issues')
                    if not db_path:
                        print('⚠️ WARNING: Empty database path')
except ImportError as e:
    print(f'Error importing settings: {e}')
except Exception as e:
    print(f'Error parsing settings: {e}')