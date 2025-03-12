# Fitment Processing Module

This module provides functionality for processing, validating, updating, and configuring automotive fitment data in the Crown Nexus platform. It bridges vehicle and product information between VCDB (Vehicle Component Database) and PCDB (Product Component Database) standards.

## Key Features

- Parse part application strings into structured data
- Validate fitment data against VCDB and PCDB databases
- Map vehicle model information using configurable rules
- Process position information (Front/Rear, Left/Right, etc.)
- Save and retrieve fitment data from databases
- Expose functionality through FastAPI endpoints

## Module Structure

- `models.py`: Pydantic data models for fitment data
- `parser.py`: Parser for fitment application strings
- `validator.py`: Validation logic for fitment data
- `mapper.py`: Mapping engine for connecting fitment to VCDB/PCDB
- `db.py`: Database access layer for VCDB and PCDB
- `api.py`: FastAPI endpoints for exposing functionality
- `dependencies.py`: Dependency injection for FastAPI
- `config.py`: Configuration settings and utilities
- `exceptions.py`: Custom exceptions for error handling

## Requirements

- Python 3.11+
- Access to VCDB and PCDB databases (Microsoft Access format)
- Pydantic for data validation
- SQLAlchemy for database access
- FastAPI for API endpoints
- Pandas for processing Excel/CSV files
- pyodbc for MS Access database connections

## Configuration

The module is configured through environment variables:

- `FITMENT_VCDB_PATH`: Path to the VCDB Access database
- `FITMENT_PCDB_PATH`: Path to the PCDB Access database
- `FITMENT_DB_URL`: SQLAlchemy URL for the application database (optional)
- `FITMENT_MODEL_MAPPINGS_PATH`: Path to the model mappings Excel file (optional)
- `FITMENT_LOG_LEVEL`: Logging level (default: INFO)
- `FITMENT_CACHE_SIZE`: Maximum size for LRU caches (default: 100)

## Usage

### Basic Usage

```python
from app.fitment.db import FitmentDBService
from app.fitment.mapper import FitmentMappingEngine

# Create DB service
db_service = FitmentDBService(
    "path/to/vcdb.mdb",
    "path/to/pcdb.mdb",
    "postgresql+asyncpg://user:password@localhost/dbname"
)

# Create mapping engine
mapping_engine = FitmentMappingEngine(db_service)

# Configure with model mappings
mapping_engine.configure("path/to/mappings.xlsx")

# Process part application
application_text = "2005-2010 WK Grand Cherokee (Left or Right Front Upper Ball Joint);"
part_terminology_id = 58869  # Suspension Ball Joint Nut

# Process the application
results = mapping_engine.process_application(application_text, part_terminology_id)

# Check results
for result in results:
    print(f"Status: {result.status}")
    print(f"Message: {result.message}")
    if result.fitment:
        print(f"Vehicle: {result.fitment.vehicle.year} {result.fitment.vehicle.make} {result.fitment.vehicle.model}")
        print(f"Positions: {result.fitment.positions}")
```

### API Usage

The module exposes several FastAPI endpoints:

- `POST /api/v1/fitment/process`: Process fitment application texts
- `POST /api/v1/fitment/upload-model-mappings`: Upload model mappings Excel file
- `GET /api/v1/fitment/pcdb-positions/{terminology_id}`: Get PCDB positions for a part terminology
- `POST /api/v1/fitment/parse-application`: Parse a part application text

Example API request:

```python
import requests
import json

# Process fitment
response = requests.post(
    "http://localhost:8000/api/v1/fitment/process",
    json={
        "application_texts": [
            "2005-2010 WK Grand Cherokee (Left or Right Front Upper Ball Joint);"
        ],
        "part_terminology_id": 58869,
        "product_id": "PRODUCT-123"
    }
)

# Check results
results = response.json()
print(json.dumps(results, indent=2))
```

## Model Mappings File

The model mappings file is an Excel file with the following structure:

- Column `Pattern`: The pattern to match in the vehicle text (e.g., "WK Grand Cherokee")
- Column `Mapping`: The mapping format: "Make|VehicleCode|Model" (e.g., "Jeep|WK|Grand Cherokee")

## Error Handling

The module uses custom exceptions for different error scenarios:

- `ParsingError`: Error parsing a fitment string
- `ValidationError`: Error validating a fitment
- `MappingError`: Error mapping a fitment
- `DatabaseError`: Error with database operations
- `ConfigurationError`: Error with configuration

## Integration with Crown Nexus

To integrate with the Crown Nexus platform:

1. Add the fitment module to the FastAPI application:

```python
# In app/main.py
from app.fitment.api import router as fitment_router

app.include_router(fitment_router)
```

2. Set up the required environment variables in your deployment environment.

3. Create the frontend components for interacting with the fitment API.

## Database Schema

For the application database, the following table structure is recommended:

```sql
CREATE TABLE product_fitments (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(255) NOT NULL,
    vcdb_vehicle_id INTEGER,
    pcdb_position_ids VARCHAR(255),
    year INTEGER NOT NULL,
    make VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    submodel VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_fitments_product_id ON product_fitments(product_id);
CREATE INDEX idx_product_fitments_vcdb_vehicle_id ON product_fitments(vcdb_vehicle_id);
```

## License

Proprietary - All rights reserved
