# AutoCare Data Import System

This system provides a comprehensive solution for importing AutoCare standard data (VCdb, PCdb, PAdb, Qdb) into the application database.

## Features

- Import from pipe-delimited text files (the standard format provided by Auto Care Association)
- Flexible mapping between external data files and database models
- Configurable field transformations and validations
- Batch processing for efficient memory usage with large datasets
- Detailed logging and error reporting
- Import history tracking
- Command-line interface for easy operation

## Supported Databases

- **VCdb** (Vehicle Component Database): Contains vehicle makes, models, and configuration data
- **PCdb** (Product Component Database): Contains standard parts terminology and categorization
- **PAdb** (Part Attribute Database): Contains part attribute definitions and values
- **Qdb** (Qualifier Database): Contains qualifiers used for vehicle fitment

## Using the CLI

The system provides a command-line interface for importing data:

```bash
# Import all databases from a directory
python -m app.cli.autocare import all --source-dir=/path/to/autocare/data

# Import a specific database
python -m app.cli.autocare import vcdb --source-dir=/path/to/vcdb/data

# Validate data without importing (dry run)
python -m app.cli.autocare import pcdb --source-dir=/path/to/pcdb/data --dry-run

# Set batch size for memory optimization
python -m app.cli.autocare import padb --source-dir=/path/to/padb/data --batch-size=5000

# Turn off sync history tracking
python -m app.cli.autocare import qdb --source-dir=/path/to/qdb/data --no-track-history
```

## Data Directory Structure

The importer expects a directory structure with pipe-delimited text files. The specific files required depend on the database being imported.

### Required Files

At minimum, each database directory must include:

- `Version.txt`: Contains the database version information

#### VCdb Required Files

- `Make.txt`, `Model.txt`, `Year.txt`, `VehicleType.txt`, `SubModel.txt`, `Region.txt`, `BaseVehicle.txt`

#### PCdb Required Files

- `Parts.txt`, `PartsDescription.txt`, `Categories.txt`, `Subcategories.txt`, `Positions.txt`, `PartCategory.txt`, `PartPosition.txt`

#### PAdb Required Files

- `PartAttributes.txt`, `MetaData.txt`, `MeasurementGroup.txt`, `MetaUOMCodes.txt`, `PartAttributeAssignment.txt`

#### Qdb Required Files

- `QualifierType.txt`, `Qualifier.txt`

## File Format

All files are expected to be pipe-delimited text files with a header row. For example:

```
QualifierId|QualifierText|ExampleText|QualifierTypeId|NewQualifierId|WhenModified
10|Air Conditioning|Example of air conditioning|1||20220101000000
11|Anti-lock Brakes|Example of anti-lock brakes|1||20220101000000
```

## Programmatic Usage

You can also use the importers programmatically:

```python
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_context
from app.domains.autocare.importers.vcdb_importer import VCdbImporter

async def import_vcdb(source_dir: Path):
    async with get_db_context() as db:
        importer = VCdbImporter(db=db, source_path=source_dir)
        is_valid = await importer.validate_source()
        if is_valid:
            result = await importer.import_data()
            print(f"Import completed: {result}")
        else:
            print("Source validation failed")
```

## Development

### Adding a New Database

To add support for a new AutoCare database:

1. Create a new importer class that inherits from `PipeFileImporter`
2. Register table mappings from file columns to database models
3. Define field transformers and validators as needed
4. Set the import order for referential integrity
5. Register the importer in the CLI command

### Adding a New File Format

The system is designed to be extensible to other file formats. To add support for a new format:

1. Create a new importer class that implements the `BaseImporter` protocol
2. Implement the `validate_source` and `import_data` methods
3. Extend the CLI command to support the new format
