# app/domains/autocare/importers/flexible_importer.py
from __future__ import annotations

"""
Flexible data importer for AutoCare data.

This module provides a generic implementation for importing data from various formats
(pipe-delimited files, JSON, database, etc.) into database tables, with configurable
mappings, transformations, and validation.
"""

import csv
import gc
import json
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, Protocol, Set, Type, TypeVar, Union, cast

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base
from app.domains.autocare.importers.base_importer import BaseImporter
from app.logging import get_logger

logger = get_logger("app.domains.autocare.importers.flexible_importer")

T = TypeVar("T", bound=Base)


class SourceFormat(str, Enum):
    """Source data formats."""
    PIPE = "pipe"
    JSON = "json"
    # Can be extended with other formats like:
    # DATABASE = "database"
    # XML = "xml"
    # EXCEL = "excel"


class DataSourceReader(ABC):
    """Interface for reading data from different sources."""

    @abstractmethod
    def validate(self, required_sources: List[str]) -> bool:
        """
        Validate that the data source is valid.

        Args:
            required_sources: List of required source names

        Returns:
            bool: True if valid, False otherwise
        """
        pass

    @abstractmethod
    def read_version(self) -> str:
        """
        Read version information from the data source.

        Returns:
            str: Version string (typically YYYY-MM-DD)
        """
        pass

    @abstractmethod
    def read_records(self, source_name: str) -> Iterator[Dict[str, Any]]:
        """
        Read records from the specified source.

        Args:
            source_name: Name of the source (file name, table name, etc.)

        Returns:
            Iterator of record dictionaries
        """
        pass


class FileReader(DataSourceReader):
    """Base class for file-based data source readers."""

    def __init__(self, source_path: Path, encoding: str = "utf-8"):
        """
        Initialize FileReader.

        Args:
            source_path: Path to source files directory
            encoding: File encoding
        """
        self.source_path = source_path
        self.encoding = encoding

    def validate(self, required_sources: List[str]) -> bool:
        """
        Validate that the required files exist.

        Args:
            required_sources: List of required file names

        Returns:
            bool: True if all required files exist, False otherwise
        """
        # Check if source directory exists
        if not self.source_path.exists() or not self.source_path.is_dir():
            logger.error(f"Directory does not exist: {self.source_path}")
            return False

        # Check for required files
        missing_files = []
        for file_name in required_sources:
            file_path = self.source_path / file_name
            if not file_path.exists():
                missing_files.append(file_name)

        if missing_files:
            logger.error(f"Missing required files: {', '.join(missing_files)}")
            return False

        # Check version file
        if not self._get_version_file_path().exists():
            logger.error(f"Version file not found: {self._get_version_file_path()}")
            return False

        return True

    @abstractmethod
    def _get_version_file_path(self) -> Path:
        """Get the path to the version file."""
        pass


class PipeFileReader(FileReader):
    """Reader for pipe-delimited files."""

    def __init__(self, source_path: Path, encoding: str = "utf-8", delimiter: str = "|"):
        """
        Initialize PipeFileReader.

        Args:
            source_path: Path to source files directory
            encoding: File encoding
            delimiter: Field delimiter in files
        """
        super().__init__(source_path, encoding)
        self.delimiter = delimiter

    def _get_version_file_path(self) -> Path:
        """Get the path to the version file."""
        return self.source_path / "Version.txt"

    def read_version(self) -> str:
        """
        Read version information from the version file.

        Returns:
            str: Version string (YYYY-MM-DD)
        """
        version_file = self._get_version_file_path()
        if not version_file.exists():
            raise FileNotFoundError(f"Version file not found: {version_file}")

        with open(version_file, "r", encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            for row in reader:
                # Just take the first row
                version_str = next((v for k, v in row.items() if v), None)
                if not version_str:
                    raise ValueError("Version file contains no data")

                return version_str

        raise ValueError("Version file is empty")

    def read_records(self, source_name: str) -> Iterator[Dict[str, Any]]:
        """
        Read records from the specified file.

        Args:
            source_name: Name of the file

        Returns:
            Iterator of record dictionaries
        """
        file_path = self.source_path / source_name
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return

        with open(file_path, "r", encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            for row in reader:
                yield row


class JsonFileReader(FileReader):
    """Reader for JSON files."""

    def _get_version_file_path(self) -> Path:
        """Get the path to the version file."""
        return self.source_path / "Version.json"

    def read_version(self) -> str:
        """
        Read version information from the version file.

        Returns:
            str: Version string (YYYY-MM-DD)
        """
        version_file = self._get_version_file_path()
        if not version_file.exists():
            raise FileNotFoundError(f"Version file not found: {version_file}")

        with open(version_file, "r", encoding=self.encoding) as f:
            try:
                version_data = json.load(f)

                # Handle different possible structures
                if isinstance(version_data, dict):
                    version_str = version_data.get("VersionDate")
                    if not version_str:
                        raise ValueError("Version file contains no 'VersionDate' field")
                elif isinstance(version_data, list):
                    version_str = version_data[0].get("VersionDate")
                    if not version_str:
                        raise ValueError("Version file contains no 'VersionDate' field")
                elif isinstance(version_data, str):
                    version_str = version_data
                else:
                    raise ValueError(f"Unexpected version data format: {type(version_data)}")

                return version_str
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in version file: {str(e)}")

    def read_records(self, source_name: str) -> Iterator[Dict[str, Any]]:
        """
        Read records from the specified file.

        Args:
            source_name: Name of the file

        Returns:
            Iterator of record dictionaries
        """
        file_path = self.source_path / source_name
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return

        with open(file_path, "r", encoding=self.encoding) as f:
            try:
                data = json.load(f)

                # Handle different JSON structures
                if isinstance(data, list):
                    # Array of objects
                    for item in data:
                        yield item
                elif isinstance(data, dict):
                    if "data" in data and isinstance(data["data"], list):
                        # Object with data array
                        for item in data["data"]:
                            yield item
                    else:
                        # Single object or other structure
                        yield data
                else:
                    logger.warning(f"Unexpected JSON data format in {source_name}: {type(data)}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in {source_name}: {str(e)}")
                raise ValueError(f"Invalid JSON in {source_name}: {str(e)}")


class FlexibleImporter(Generic[T]):
    """Flexible importer that can handle different data formats."""

    def __init__(
        self,
        db: AsyncSession,
        source_path: Path,
        schema_name: str,
        required_sources: List[str],
        version_class: Type[Base],
        source_format: SourceFormat = SourceFormat.PIPE,
        version_date_field: str = "version_date",
        batch_size: int = 1000,
        encoding: str = "utf-8",
    ) -> None:
        """
        Initialize FlexibleImporter.

        Args:
            db: Database session
            source_path: Path to source files directory
            schema_name: Database schema name
            required_sources: List of required sources
            version_class: Class for version records
            source_format: Format of the source data
            version_date_field: Field name for version date
            batch_size: Batch size for imports
            encoding: File encoding
        """
        self.db = db
        self.source_path = source_path
        self.schema_name = schema_name
        self.required_sources = required_sources
        self.version_class = version_class
        self.source_format = source_format
        self.version_date_field = version_date_field
        self.batch_size = batch_size
        self.encoding = encoding

        # Create appropriate reader based on source format
        self.reader = self._create_reader()

        # Mapping configurations
        self.table_mappings: Dict[str, Dict[str, Any]] = {}
        self.transformers: Dict[str, Dict[str, Callable]] = {}
        self.validators: Dict[str, Dict[str, Callable]] = {}

        # Optional settings
        self.import_order: List[str] = []
        self.many_to_many_tables: Dict[str, Dict[str, Any]] = {}
        self.imported_ids: Dict[str, Set[Any]] = {}

    def _create_reader(self) -> DataSourceReader:
        """
        Create the appropriate data source reader.

        Returns:
            DataSourceReader: The data source reader
        """
        if self.source_format == SourceFormat.PIPE:
            return PipeFileReader(source_path=self.source_path, encoding=self.encoding)
        elif self.source_format == SourceFormat.JSON:
            return JsonFileReader(source_path=self.source_path, encoding=self.encoding)
        else:
            raise ValueError(f"Unsupported source format: {self.source_format}")

    async def validate_source(self) -> bool:
        """
        Validate that the source data is valid.

        Returns:
            bool: True if valid, False otherwise
        """
        # Print validation status to console
        print(f"\nValidating source directory: {self.source_path}")
        print(f"Format: {self.source_format.value}")

        # Use the reader to validate the source
        result = self.reader.validate(self.required_sources)

        if result:
            print("\nRequired files are present.")
            try:
                version = self.reader.read_version()
                print(f"Version: {version}")
            except Exception as e:
                print(f"Warning: Could not read version: {str(e)}")
                result = False

        # Print validation result
        print(f"\nValidation result: {'SUCCESS' if result else 'FAILED'}")

        return result

    def register_table_mapping(
        self,
        source_name: str,
        model_class: Type[Base],
        field_mapping: Dict[str, str],
        primary_key: str,
        transformers: Optional[Dict[str, Callable]] = None,
        validators: Optional[Dict[str, Callable]] = None,
    ) -> None:
        """
        Register a mapping between a source and a database table.

        Args:
            source_name: Name of the source
            model_class: SQLAlchemy model class
            field_mapping: Mapping from source fields to model fields
            primary_key: Primary key field in the model
            transformers: Optional dict of transformer functions for fields
            validators: Optional dict of validator functions for fields
        """
        self.table_mappings[source_name] = {
            "model_class": model_class,
            "field_mapping": field_mapping,
            "primary_key": primary_key,
        }

        if transformers:
            self.transformers[source_name] = transformers

        if validators:
            self.validators[source_name] = validators

        # Add to import order if not already there
        if source_name not in self.import_order:
            self.import_order.append(source_name)

    def register_many_to_many_table(
        self,
        source_name: str,
        table_name: str,
        field_mapping: Dict[str, str],
        transformers: Optional[Dict[str, Callable]] = None,
    ) -> None:
        """
        Register a mapping for a many-to-many table.

        Args:
            source_name: Name of the source
            table_name: Name of the table
            field_mapping: Mapping from source fields to table fields
            transformers: Optional dict of transformer functions for fields
        """
        self.many_to_many_tables[source_name] = {
            "table_name": table_name,
            "field_mapping": field_mapping,
        }

        if transformers:
            self.transformers[source_name] = transformers

        # Add to import order if not already there
        if source_name not in self.import_order:
            self.import_order.append(source_name)

    def set_import_order(self, order: List[str]) -> None:
        """
        Set the order in which tables should be imported.

        Args:
            order: List of source names in import order
        """
        # Validate that all sources in order exist in mappings
        unknown_sources = []
        for source_name in order:
            if source_name not in self.table_mappings and source_name not in self.many_to_many_tables:
                unknown_sources.append(source_name)

        if unknown_sources:
            raise ValueError(f"Unknown sources in import order: {', '.join(unknown_sources)}")

        # Make sure all mapped sources are included in order
        missing_sources = []
        for source_name in self.table_mappings:
            if source_name not in order:
                missing_sources.append(source_name)

        for source_name in self.many_to_many_tables:
            if source_name not in order:
                missing_sources.append(source_name)

        if missing_sources:
            raise ValueError(f"Sources missing from import order: {', '.join(missing_sources)}")

        self.import_order = order

    async def import_data(self) -> Dict[str, Any]:
        """
        Import data from source to database.

        Returns:
            Dict[str, Any]: Dictionary with import results
        """
        if not await self.validate_source():
            return {"success": False, "message": "Invalid source data"}

        # Track statistics
        stats = {
            "total_files": len(self.table_mappings) + len(self.many_to_many_tables),
            "processed_files": 0,
            "success": True,
            "errors": [],
            "items_imported": {},
            "start_time": datetime.now().isoformat(),
        }

        try:
            # Start transaction
            transaction = await self.db.begin()

            # Create version record
            version_info = await self._import_version()
            if version_info["success"]:
                stats["version"] = version_info["version"]
            else:
                stats["success"] = False
                stats["errors"].append(version_info["message"])
                await transaction.rollback()
                return stats

            # Import tables in order
            if not self.import_order:
                # If no explicit order is set, use all mappings
                self.import_order = list(self.table_mappings.keys()) + list(self.many_to_many_tables.keys())

            for source_name in self.import_order:
                try:
                    if source_name in self.table_mappings:
                        # Regular table
                        mapping = self.table_mappings[source_name]
                        count = await self._import_table(source_name, mapping)
                        stats["processed_files"] += 1
                        stats["items_imported"][source_name] = count

                    elif source_name in self.many_to_many_tables:
                        # Many-to-many table
                        mapping = self.many_to_many_tables[source_name]
                        count = await self._import_many_to_many_table(source_name, mapping)
                        stats["processed_files"] += 1
                        stats["items_imported"][source_name] = count

                except Exception as e:
                    logger.error(f"Error importing {source_name}: {str(e)}")
                    stats["errors"].append(f"Error importing {source_name}: {str(e)}")
                    stats["success"] = False
                    await transaction.rollback()
                    return stats

            # Commit transaction
            await transaction.commit()

            stats["end_time"] = datetime.now().isoformat()
            return stats

        except Exception as e:
            # Rollback transaction on any error
            logger.error(f"Error in import process: {str(e)}")
            stats["success"] = False
            stats["errors"].append(f"Error in import process: {str(e)}")
            try:
                await transaction.rollback()
            except Exception as rollback_error:
                logger.error(f"Error rolling back transaction: {str(rollback_error)}")

            return stats

    async def _import_version(self) -> Dict[str, Any]:
        """
        Import version information.

        Returns:
            Dict[str, Any]: Dictionary with success status and version
        """
        try:
            # Read version from the reader
            version_str = self.reader.read_version()

            # Parse the version string into a date
            try:
                version_date = datetime.strptime(version_str, "%Y-%m-%d")
            except ValueError:
                # Try different date formats if the standard one fails
                try:
                    version_date = datetime.strptime(version_str, "%m/%d/%Y")
                except ValueError:
                    logger.warning(f"Unrecognized date format: {version_str}. Using current date.")
                    version_date = datetime.now()

            # Update existing version records
            await self.db.execute(
                text(f"UPDATE {self.schema_name}.{self.version_class.__tablename__} SET is_current = false")
            )

            # Create new version record
            version = self.version_class(
                **{self.version_date_field: version_date, "is_current": True}
            )
            self.db.add(version)
            await self.db.flush()

            return {"success": True, "version": version_date.strftime("%Y-%m-%d")}

        except Exception as e:
            logger.error(f"Error importing version: {str(e)}")
            return {"success": False, "message": f"Error importing version: {str(e)}"}

    async def _import_table(self, source_name: str, mapping: Dict[str, Any]) -> int:
        """
        Import data from a source to a database table.

        Args:
            source_name: Name of the source
            mapping: Mapping configuration

        Returns:
            int: Number of records imported
        """
        model_class = mapping["model_class"]
        field_mapping = mapping["field_mapping"]
        primary_key = mapping["primary_key"]
        transformers = self.transformers.get(source_name, {})
        validators = self.validators.get(source_name, {})

        # Check if we need to clear existing data
        table_name = model_class.__tablename__
        count = await self.db.scalar(
            text(f"SELECT COUNT(*) FROM {self.schema_name}.{table_name}")
        )

        if count > 0:
            logger.info(f"Clearing existing data from {table_name}")
            await self.db.execute(text(f"TRUNCATE TABLE {self.schema_name}.{table_name} RESTART IDENTITY CASCADE"))

        # Initialize tracking
        total_count = 0
        batch = []
        imported_ids = set()
        self.imported_ids[source_name] = imported_ids

        # Process records from the reader
        try:
            for row in self.reader.read_records(source_name):
                # Map and transform fields
                obj_data = {}
                validation_errors = []

                for model_field, source_field in field_mapping.items():
                    # Handle nested fields for JSON
                    if "." in source_field and self.source_format == SourceFormat.JSON:
                        parts = source_field.split(".")
                        value = row
                        for part in parts:
                            if isinstance(value, dict) and part in value:
                                value = value[part]
                            else:
                                value = None
                                break
                    else:
                        value = row.get(source_field)

                    # Apply transformer if one exists
                    if model_field in transformers:
                        try:
                            value = transformers[model_field](value)
                        except Exception as e:
                            logger.error(f"Error transforming field {model_field} in {source_name}: {str(e)}")
                            validation_errors.append(f"Error transforming field {model_field}: {str(e)}")

                    # Apply validator if one exists
                    if model_field in validators:
                        try:
                            valid, error = validators[model_field](value)
                            if not valid:
                                validation_errors.append(f"Validation error for {model_field}: {error}")
                        except Exception as e:
                            logger.error(f"Error validating field {model_field} in {source_name}: {str(e)}")
                            validation_errors.append(f"Error validating field {model_field}: {str(e)}")

                    obj_data[model_field] = value

                if validation_errors:
                    logger.warning(f"Validation errors in {source_name}, skipping row: {', '.join(validation_errors)}")
                    continue

                # Create model instance
                obj = model_class(**obj_data)
                batch.append(obj)

                # Track primary key
                pk_value = getattr(obj, primary_key)
                imported_ids.add(pk_value)

                # Commit in batches
                if len(batch) >= self.batch_size:
                    self.db.add_all(batch)
                    await self.db.flush()
                    total_count += len(batch)
                    batch = []

                    # Force garbage collection to manage memory
                    gc.collect()

                    logger.debug(f"Imported {total_count} records to {table_name}")

        except Exception as e:
            logger.error(f"Error processing {source_name}: {str(e)}")
            raise

        # Commit final batch
        if batch:
            self.db.add_all(batch)
            await self.db.flush()
            total_count += len(batch)

        logger.info(f"Imported {total_count} records to {table_name}")
        return total_count

    async def _import_many_to_many_table(self, source_name: str, mapping: Dict[str, Any]) -> int:
        """
        Import data from a source to a many-to-many table.

        Args:
            source_name: Name of the source
            mapping: Mapping configuration

        Returns:
            int: Number of records imported
        """
        table_name = mapping["table_name"]
        field_mapping = mapping["field_mapping"]
        transformers = self.transformers.get(source_name, {})

        # Check if we need to clear existing data
        count = await self.db.scalar(
            text(f"SELECT COUNT(*) FROM {self.schema_name}.{table_name}")
        )

        if count > 0:
            logger.info(f"Clearing existing data from {table_name}")
            await self.db.execute(text(f"TRUNCATE TABLE {self.schema_name}.{table_name} RESTART IDENTITY CASCADE"))

        # Initialize tracking
        total_count = 0
        batch = []

        # Process records from the reader
        try:
            for row in self.reader.read_records(source_name):
                # Map and transform fields
                row_data = {}

                for db_field, source_field in field_mapping.items():
                    # Handle nested fields for JSON
                    if "." in source_field and self.source_format == SourceFormat.JSON:
                        parts = source_field.split(".")
                        value = row
                        for part in parts:
                            if isinstance(value, dict) and part in value:
                                value = value[part]
                            else:
                                value = None
                                break
                    else:
                        value = row.get(source_field)

                    # Apply transformer if one exists
                    if db_field in transformers:
                        try:
                            value = transformers[db_field](value)
                        except Exception as e:
                            logger.error(f"Error transforming field {db_field} in {source_name}: {str(e)}")
                            continue

                    row_data[db_field] = value

                # Add to batch
                batch.append(row_data)

                # Commit in batches
                if len(batch) >= self.batch_size:
                    try:
                        # Insert batch using raw SQL
                        fields = list(field_mapping.keys())
                        placeholders = ", ".join([f":{field}" for field in fields])
                        field_list = ", ".join(fields)

                        query = text(
                            f"INSERT INTO {self.schema_name}.{table_name} ({field_list}) VALUES ({placeholders})")

                        for data in batch:
                            await self.db.execute(query, data)

                        total_count += len(batch)
                        batch = []

                        # Force garbage collection to manage memory
                        gc.collect()

                        logger.debug(f"Imported {total_count} records to {table_name}")
                    except Exception as e:
                        logger.error(f"Error inserting batch into {table_name}: {str(e)}")
                        raise

        except Exception as e:
            logger.error(f"Error processing {source_name}: {str(e)}")
            raise

        # Commit final batch
        if batch:
            try:
                # Insert batch using raw SQL
                fields = list(field_mapping.keys())
                placeholders = ", ".join([f":{field}" for field in fields])
                field_list = ", ".join(fields)

                query = text(f"INSERT INTO {self.schema_name}.{table_name} ({field_list}) VALUES ({placeholders})")

                for data in batch:
                    await self.db.execute(query, data)

                total_count += len(batch)
            except Exception as e:
                logger.error(f"Error inserting final batch into {table_name}: {str(e)}")
                raise

        logger.info(f"Imported {total_count} records to {table_name}")
        return total_count


def detect_source_format(source_path: Path) -> SourceFormat:
    """
    Automatically detect the format of the source data.

    Args:
        source_path: Path to source directory

    Returns:
        SourceFormat: Detected source format
    """
    # Look for format-specific version files
    if (source_path / "Version.json").exists():
        return SourceFormat.JSON

    # Default to pipe-delimited files if Version.txt exists
    if (source_path / "Version.txt").exists():
        return SourceFormat.PIPE

    # If we can't determine format from version file, look at other files
    json_count = len(list(source_path.glob("*.json")))
    txt_count = len(list(source_path.glob("*.txt")))

    if json_count > 0 and txt_count == 0:
        return SourceFormat.JSON
    elif txt_count > 0 and json_count == 0:
        return SourceFormat.PIPE
    elif txt_count > json_count:
        return SourceFormat.PIPE
    else:
        # Default to pipe if we can't determine
        return SourceFormat.PIPE
