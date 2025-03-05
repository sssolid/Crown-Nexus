crown-nexus/
├── .github/                      # GitHub specific files
│   └── workflows/                # GitHub Actions CI/CD workflows
├── backend/                      # FastAPI backend
│   ├── alembic/                  # Database migration scripts
│   ├── app/                      # Main application code
│   │   ├── api/                  # API routes/endpoints
│   │   │   ├── v1/               # API version 1
│   │   │   │   ├── endpoints/    # API endpoint modules by resource
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── products.py
│   │   │   │   │   ├── fitments.py
│   │   │   │   │   └── users.py
│   │   │   │   └── router.py     # API router for v1
│   │   │   └── deps.py           # API dependencies (auth, db, etc.)
│   │   ├── core/                 # Core application modules
│   │   │   ├── config.py         # Application configuration
│   │   │   ├── security.py       # Security utilities
│   │   │   └── events.py         # Event handlers
│   │   ├── db/                   # Database related code
│   │   │   ├── base.py           # Base model
│   │   │   ├── session.py        # Database session
│   │   │   └── init_db.py        # Database initialization
│   │   ├── models/               # SQLAlchemy models
│   │   │   ├── product.py
│   │   │   ├── fitment.py
│   │   │   ├── user.py
│   │   │   └── ...
│   │   ├── schemas/              # Pydantic schemas for validation
│   │   │   ├── product.py
│   │   │   ├── fitment.py
│   │   │   ├── user.py
│   │   │   └── ...
│   │   ├── services/             # Business logic
│   │   │   ├── product.py
│   │   │   ├── fitment.py
│   │   │   ├── search.py
│   │   │   └── ...
│   │   ├── utils/                # Utility functions
│   │   │   ├── logging.py
│   │   │   ├── dependencies.py
│   │   │   └── ...
│   │   └── main.py               # Application entry point
│   ├── tests/                    # Test directory
│   │   ├── conftest.py           # Test configuration
│   │   ├── api/                  # API tests
│   │   │   └── v1/
│   │   │       ├── test_products.py
│   │   │       ├── test_fitments.py
│   │   │       └── ...
│   │   └── services/             # Service tests
│   │       ├── test_product.py
│   │       ├── test_fitment.py
│   │       └── ...
│   ├── .env                      # Environment variables (not in git)
│   ├── .env.example              # Example environment variables
│   ├── pyproject.toml            # Python project configuration
│   ├── requirements.in           # Top-level dependencies
│   ├── requirements.txt          # Pinned dependencies (generated)
│   ├── requirements-dev.in       # Development dependencies
│   ├── requirements-dev.txt      # Pinned dev dependencies (generated)
│   └── README.md                 # Backend documentation
├── frontend/                     # Vue.js frontend
│   ├── public/                   # Static public files
│   ├── src/                      # Source code
│   │   ├── assets/               # Static assets
│   │   ├── components/           # Vue components
│   │   │   ├── common/           # Shared components
│   │   │   ├── layout/           # Layout components
│   │   │   ├── products/         # Product-related components
│   │   │   ├── fitments/         # Fitment-related components
│   │   │   └── ...
│   │   ├── composables/          # Vue composables (reusable logic)
│   │   ├── router/               # Vue Router configuration
│   │   │   ├── index.ts
│   │   │   └── routes/           # Route definitions
│   │   ├── services/             # API services
│   │   │   ├── api.ts            # Base API setup
│   │   │   ├── product.ts
│   │   │   ├── fitment.ts
│   │   │   └── ...
│   │   ├── stores/               # Pinia stores
│   │   │   ├── product.ts
│   │   │   ├── fitment.ts
│   │   │   ├── auth.ts
│   │   │   └── ...
│   │   ├── types/                # TypeScript types
│   │   │   ├── product.ts
│   │   │   ├── fitment.ts
│   │   │   └── ...
│   │   ├── utils/                # Utility functions
│   │   ├── views/                # Vue views/pages
│   │   │   ├── Dashboard.vue
│   │   │   ├── ProductCatalog.vue
│   │   │   └── ...
│   │   ├── App.vue               # Root component
│   │   ├── main.ts               # Application entry point
│   │   └── env.d.ts              # Environment variables type definitions
│   ├── tests/                    # Test directory
│   │   ├── unit/                 # Unit tests
│   │   └── e2e/                  # End-to-end tests
│   ├── .eslintrc.js              # ESLint configuration
│   ├── index.html                # HTML entry point
│   ├── package.json              # npm dependencies
│   ├── tsconfig.json             # TypeScript configuration
│   ├── vite.config.ts            # Vite configuration
│   └── README.md                 # Frontend documentation
├── docs/                         # Project documentation
│   ├── architecture/             # Architecture documentation
│   ├── api/                      # API documentation
│   ├── deployment/               # Deployment guides
│   └── development/              # Development guides
├── infrastructure/               # Infrastructure as Code
│   ├── pulumi/                   # Pulumi configurations
│   │   ├── __main__.py           # Main Pulumi program
│   │   ├── database.py           # Database infrastructure
│   │   └── ...
│   └── docker/                   # Docker configurations
│       ├── docker-compose.yml    # Docker Compose for local dev
│       ├── Dockerfile.backend    # Backend Dockerfile
│       ├── Dockerfile.frontend   # Frontend Dockerfile
│       └── ...
├── scripts/                      # Utility scripts
│   ├── setup.sh                  # Initial setup script
│   ├── seed_data.py              # Data seeding script
│   └── ...
├── .gitignore                    # Git ignore file
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── .editorconfig                 # Editor configuration
├── README.md                     # Project overview
└── CHANGELOG.md                  # Version history