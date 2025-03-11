# Developer Getting Started Guide

This guide will help you set up your development environment and understand the development workflow for Crown Nexus.

## Development Environment Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- Git
- Visual Studio Code, IntelliJ IDEA Ultimate, or your preferred IDE

### Setting Up the Environment

1. **Clone the repository**

```bash
git clone https://github.com/your-org/crown-nexus.git
cd crown-nexus
```

2. **Set up pre-commit hooks**

```bash
pip install pre-commit
pre-commit install
```

3. **Start the development environment with Docker Compose**

```bash
cd infrastructure/docker
docker compose up -d
```

This will start the PostgreSQL, Elasticsearch, and Redis services.

4. **Set up the backend**

```bash
cd ../../backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your development settings

# Run the development server
uvicorn app.main:app --reload
```

5. **Set up the frontend**

```bash
cd ../frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

## Development Workflow

### Git Workflow

We follow a feature branch workflow:

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

3. Push your branch to the remote repository:
   ```bash
   git push -u origin feature/your-feature-name
   ```

4. Create a Pull Request on GitHub for review.

### Code Quality

All code must pass the following checks:

- Type checking with mypy
- Linting with ruff or flake8
- Formatting with black and isort
- Frontend linting with ESLint

These checks are enforced by pre-commit hooks and CI/CD pipelines.

### Testing

Write tests for all new features and bug fixes:

- Backend: Use pytest for unit and integration tests
- Frontend: Use Vitest for component and unit tests

Run tests locally before submitting a PR:

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

### API Development

1. Define Pydantic schemas in `app/schemas/`
2. Implement database models in `app/models/`
3. Create business logic in `app/services/`
4. Implement API endpoints in `app/api/v1/endpoints/`
5. Document your API with proper docstrings
6. Add tests in `tests/`

### Frontend Development

1. Define TypeScript interfaces in `src/types/`
2. Implement API services in `src/services/`
3. Create Pinia stores in `src/stores/`
4. Build Vue components in `src/components/`
5. Implement views in `src/views/`
6. Add tests in `tests/`

## Documentation

- Update documentation when making significant changes
- Keep README.md and CHANGELOG.md up to date
- Add JSDoc comments for TypeScript code
- Use Google-style docstrings for Python code

## Getting Help

If you have questions or need help, you can:

- Check the existing documentation
- Ask a team member
- Submit an issue on GitHub
