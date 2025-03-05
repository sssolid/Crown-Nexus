# Crown Nexus

A B2B platform for the automotive aftermarket industry, providing a centralized hub for product data, fitment information, pricing, media, and customer support.

## Project Structure

- **backend/**: FastAPI backend API
- **frontend/**: Vue.js frontend application
- **infrastructure/**: Infrastructure as Code and Docker configurations
- **docs/**: Project documentation

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL 15
- Elasticsearch 8
- Redis 7

### Development Setup

1. Clone the repository
2. Start the development environment with Docker Compose:

```bash
cd infrastructure/docker
docker-compose up -d
```

Alternatively, you can run the backend and frontend separately:

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### API Documentation

When the backend is running, API documentation is available at:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### Frontend Application

The frontend development server runs at http://localhost:3000

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## License

Proprietary - All rights reserved
