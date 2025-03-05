# Crown Nexus Backend

Backend API for the Crown Nexus B2B platform for automotive aftermarket industry.

## Technology Stack

- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Pydantic
- Alembic
- Elasticsearch
- Redis

## Development Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements-dev.txt`
4. Copy `.env.example` to `.env` and update the values
5. Run the server: `uvicorn app.main:app --reload`

## API Documentation

When the server is running, API documentation is available at:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Testing

Run tests with pytest:

```bash
pytest
```

For coverage report:

```bash
pytest --cov=app
```
