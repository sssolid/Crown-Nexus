### Reset the database
```bash
python .\manage.py reset
```

### Generate the migration file
alembic revision --autogenerate -m "initial"


### Fix the migration:
```python
from app.core.config import settings

for schema in settings.DB_SCHEMAS:
    op.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
```
#### Add unique restraints in migration file
- sa.UniqueConstraints('region_id')
- sa.UniqueConstraints('qualifier_id')


### Execute the migration
alembic upgrade head


### Bootstrap the database
python .\scripts\database_bootstrap.py
python -m app.data_import.commands.import_all --source filemaker --verbosity normal --notify -v quiet
