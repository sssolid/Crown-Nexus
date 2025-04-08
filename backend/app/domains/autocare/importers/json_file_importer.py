# app/domains/autocare/importers/json_file_importer.py
from __future__ import annotations

"""
JSON file importer for AutoCare data.

This module provides a generic implementation for importing JSON data files
into database tables, with configurable mappings, transformations, and validation.
"""

import json
import gc
from datetime import datetime
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    cast,
)

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base
from app.domains.autocare.importers.base_importer import BaseImporter
from app.logging import get_logger

logger = get_logger("app.domains.autocare.importers.json_file_importer")

T = TypeVar("T", bound=Base)


class JsonFileImporter(Generic[T]):
    """Generic importer for JSON files."""

    def __init__(
        self,
        db: AsyncSession,
        source_path: Path,
        schema_name: str,
        required_files: List[str],
        version_class: Type[Base],
        version_date_field: str = "version_date",
        batch_size: int = 1000,
        encoding: str = "utf-8",
    ) -> None:
        """
        Initialize JsonFileImporter.

        Args:
            db: Database session
            source_path: Path to source files directory
            schema_name: Database schema name
            required_files: List of required files
            version_class: Class for version records
            version_date_field: Field name for version date
            batch_size: Batch size for imports
            encoding: File encoding
        """
        self.db = db
        self.source_path = source_path
        self.schema_name = schema_name
        self.required_files = required_files
        self.version_class = version_class
        self.version_date_field = version_date_field
        self.batch_size = batch_size
        self.encoding = encoding

        # Mapping configurations
        self.table_mappings: Dict[str, Dict[str, Any]] = {}
        self.transformers: Dict[str, Dict[str, Callable]] = {}
        self.validators: Dict[str, Dict[str, Callable]] = {}

        # Optional settings
        self.import_order: List[str] = []
        self.many_to_many_tables: Dict[str, Dict[str, Any]] = {}
        self.imported_ids: Dict[str, Set[Any]] = {}

    async def validate_source(self) -> bool:
        """
        Validate that the source data consists of valid JSON files.

        Returns:
            bool: True if valid, False otherwise
        """
        # Print validation status to console
        print(f"\nValidating source directory: {self.source_path}")

        if not self.source_path.exists() or not self.source_path.is_dir():
            error_msg = f"Directory does not exist: {self.source_path}"
            print(f"ERROR: {error_msg}")
            logger.error(error_msg)
            return False

        # Print required files
        print(f"\nChecking required files:")
        for file_name in self.required_files:
            file_path = self.source_path / file_name
            exists = file_path.exists()
            print(f"  - {file_name}: {'✓' if exists else '✗'}")

        # Check for required files
        missing_files = []
        for file_name in self.required_files:
            file_path = self.source_path / file_name
            if not file_path.exists():
                missing_files.append(file_name)

        if missing_files:
            error_msg = f"Missing required files: {', '.join(missing_files)}"
            print(f"\nERROR: {error_msg}")
            logger.error(error_msg)
            return False

        # Check for Version.json file
        version_file = self.source_path / "Version.json"
        if not version_file.exists():
            error_msg = "Version.json file not found"
            print(f"\nERROR: {error_msg}")
            logger.error(error_msg)
            return False
        else:
            try:
                with open(version_file, "r", encoding=self.encoding) as f:
                    version_content = f.read().strip()
                    print(f"\nVersion file content: {version_content}")
                    # Validate JSON format
                    json.loads(version_content)
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON in Version.json: {str(e)}"
                print(f"\nERROR: {error_msg}")
                logger.error(error_msg)
                return False
            except Exception as e:
                print(f"\nWARNING: Could not read Version.json: {str(e)}")

        # Print mapped files status
        print(f"\nChecking mapped tables:")
        missing_mappings = []
        for file_name in self.table_mappings:
            file_path = self.source_path / file_name
            exists = file_path.exists()
            print(f"  - {file_name}: {'✓' if exists else '✗'}")
            if not exists:
                missing_mappings.append(file_name)
                logger.warning(f"Mapped file not found: {file_path}")

        # Check many-to-many mappings
        if self.many_to_many_tables:
            print(f"\nChecking many-to-many tables:")
            missing_many_to_many = []
            for file_name in self.many_to_many_tables:
                file_path = self.source_path / file_name
                exists = file_path.exists()
                print(f"  - {file_name}: {'✓' if exists else '✗'}")
                if not exists:
                    missing_many_to_many.append(file_name)
                    logger.warning(f"Mapped many-to-many file not found: {file_path}")
        else:
            missing_many_to_many = []

        # Print validation summary
        print(f"\nValidation Summary:")
        print(f"  - Source directory exists: ✓")
        print(
            f"  - Required files: {len(self.required_files) - len(missing_files)}/{len(self.required_files)} present"
        )
        print(
            f"  - Mapped tables: {len(self.table_mappings) - len(missing_mappings)}/{len(self.table_mappings)} present"
        )
        if self.many_to_many_tables:
            print(
                f"  - Many-to-many tables: {len(self.many_to_many_tables) - len(missing_many_to_many)}/{len(self.many_to_many_tables)} present"
            )
        print(f"  - Version.json present: {'✓' if version_file.exists() else '✗'}")

        # Additional JSON validation
        if not missing_files:
            print(f"\nValidating JSON format for required files:")
            invalid_files = []
            for file_name in self.required_files:
                file_path = self.source_path / file_name
                try:
                    with open(file_path, "r", encoding=self.encoding) as f:
                        json.load(f)
                    print(f"  - {file_name}: ✓")
                except json.JSONDecodeError as e:
                    print(f"  - {file_name}: ✗ (Invalid JSON: {str(e)})")
                    invalid_files.append(file_name)
                    logger.error(f"Invalid JSON in {file_path}: {str(e)}")
                except Exception as e:
                    print(f"  - {file_name}: ✗ (Error: {str(e)})")
                    invalid_files.append(file_name)
                    logger.error(f"Error reading {file_path}: {str(e)}")

            if invalid_files:
                error_msg = f"Invalid JSON format in files: {', '.join(invalid_files)}"
                print(f"\nERROR: {error_msg}")
                logger.error(error_msg)
                return False

        validation_result = (not missing_files) and version_file.exists()
        print(f"\nValidation result: {'SUCCESS' if validation_result else 'FAILED'}")

        return validation_result

    def register_table_mapping(
        self,
        file_name: str,
        model_class: Type[Base],
        field_mapping: Dict[str, str],
        primary_key: str,
        transformers: Optional[Dict[str, Callable]] = None,
        validators: Optional[Dict[str, Callable]] = None,
    ) -> None:
        """
        Register a mapping between a file and a database table.

        Args:
            file_name: Name of the file
            model_class: SQLAlchemy model class
            field_mapping: Mapping from file columns to model fields
            primary_key: Primary key field in the model
            transformers: Optional dict of transformer functions for fields
            validators: Optional dict of validator functions for fields
        """
        self.table_mappings[file_name] = {
            "model_class": model_class,
            "field_mapping": field_mapping,
            "primary_key": primary_key,
        }

        if transformers:
            self.transformers[file_name] = transformers

        if validators:
            self.validators[file_name] = validators

        # Add to import order if not already there
        if file_name not in self.import_order:
            self.import_order.append(file_name)

    def register_many_to_many_table(
        self,
        file_name: str,
        table_name: str,
        field_mapping: Dict[str, str],
        transformers: Optional[Dict[str, Callable]] = None,
    ) -> None:
        """
        Register a mapping for a many-to-many table.

        Args:
            file_name: Name of the file
            table_name: Name of the table
            field_mapping: Mapping from file columns to table fields
            transformers: Optional dict of transformer functions for fields
        """
        self.many_to_many_tables[file_name] = {
            "table_name": table_name,
            "field_mapping": field_mapping,
        }

        if transformers:
            self.transformers[file_name] = transformers

        # Add to import order if not already there
        if file_name not in self.import_order:
            self.import_order.append(file_name)

    def set_import_order(self, order: List[str]) -> None:
        """
        Set the order in which tables should be imported.

        Args:
            order: List of file names in import order
        """
        # Validate that all files in order exist in mappings
        unknown_files = []
        for file_name in order:
            if (
                file_name not in self.table_mappings
                and file_name not in self.many_to_many_tables
            ):
                unknown_files.append(file_name)

        if unknown_files:
            raise ValueError(
                f"Unknown files in import order: {', '.join(unknown_files)}"
            )

        # Make sure all mapped files are included in order
        missing_files = []
        for file_name in self.table_mappings:
            if file_name not in order:
                missing_files.append(file_name)

        for file_name in self.many_to_many_tables:
            if file_name not in order:
                missing_files.append(file_name)

        if missing_files:
            raise ValueError(
                f"Files missing from import order: {', '.join(missing_files)}"
            )

        self.import_order = order

    async def import_data(self) -> Dict[str, Any]:
        """
        Import data from JSON files to database.

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
                self.import_order = list(self.table_mappings.keys()) + list(
                    self.many_to_many_tables.keys()
                )

            for file_name in self.import_order:
                try:
                    if file_name in self.table_mappings:
                        # Regular table
                        mapping = self.table_mappings[file_name]
                        count = await self._import_table(file_name, mapping)
                        stats["processed_files"] += 1
                        stats["items_imported"][file_name] = count

                    elif file_name in self.many_to_many_tables:
                        # Many-to-many table
                        mapping = self.many_to_many_tables[file_name]
                        count = await self._import_many_to_many_table(
                            file_name, mapping
                        )
                        stats["processed_files"] += 1
                        stats["items_imported"][file_name] = count

                except Exception as e:
                    logger.error(f"Error importing {file_name}: {str(e)}")
                    stats["errors"].append(f"Error importing {file_name}: {str(e)}")
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
        version_file = self.source_path / "Version.json"
        if not version_file.exists():
            return {"success": False, "message": "Version file not found"}

        try:
            with open(version_file, "r", encoding=self.encoding) as f:
                version_data = json.load(f)
                # Expect a version field in the JSON
                version_str = version_data.get("version", None)

                if not version_str:
                    return {
                        "success": False,
                        "message": "Version file contains no version field",
                    }

                version_date = datetime.strptime(version_str, "%Y-%m-%d")

                # Update existing version records
                await self.db.execute(
                    text(
                        f"UPDATE {self.schema_name}.{self.version_class.__tablename__} SET is_current = false"
                    )
                )

                # Create new version record
                version = self.version_class(
                    **{self.version_date_field: version_date, "is_current": True}
                )
                self.db.add(version)
                await self.db.flush()

                return {"success": True, "version": version_date.strftime("%Y-%m-%d")}

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Version.json: {str(e)}")
            return {
                "success": False,
                "message": f"Error parsing Version.json: {str(e)}",
            }
        except Exception as e:
            logger.error(f"Error importing version: {str(e)}")
            return {"success": False, "message": f"Error importing version: {str(e)}"}

    async def _import_table(self, file_name: str, mapping: Dict[str, Any]) -> int:
        """
        Import data from a JSON file to a database table.

        Args:
            file_name: Name of the file
            mapping: Mapping configuration

        Returns:
            int: Number of records imported
        """
        file_path = self.source_path / file_name
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return 0

        model_class = mapping["model_class"]
        field_mapping = mapping["field_mapping"]
        primary_key = mapping["primary_key"]
        transformers = self.transformers.get(file_name, {})
        validators = self.validators.get(file_name, {})

        # Check if we need to clear existing data
        table_name = model_class.__tablename__
        count = await self.db.scalar(
            text(f"SELECT COUNT(*) FROM {self.schema_name}.{table_name}")
        )

        if count > 0:
            logger.info(f"Clearing existing data from {table_name}")
            await self.db.execute(
                text(
                    f"TRUNCATE TABLE {self.schema_name}.{table_name} RESTART IDENTITY CASCADE"
                )
            )

        # Initialize tracking
        total_count = 0
        batch = []
        imported_ids = set()
        self.imported_ids[file_name] = imported_ids

        # Get file size for progress reporting
        file_size = file_path.stat().st_size
        processed_size = 0
        last_progress = -1

        try:
            # Load the JSON file
            with open(file_path, "r", encoding=self.encoding) as f:
                data = json.load(f)

                # Ensure data is a list
                if not isinstance(data, list):
                    # If it's a dictionary with a data field, try to use that
                    if (
                        isinstance(data, dict)
                        and "data" in data
                        and isinstance(data["data"], list)
                    ):
                        data = data["data"]
                    else:
                        # Otherwise, wrap in a list
                        data = [data]

                # Process each item
                for i, item in enumerate(data):
                    # Track progress
                    item_size = len(json.dumps(item))
                    processed_size += item_size
                    progress = int(processed_size * 100 / file_size)
                    if progress > last_progress and progress % 10 == 0:
                        logger.info(f"Importing {file_name}: {progress}% complete")
                        last_progress = progress

                    # Map and transform fields
                    obj_data = {}
                    validation_errors = []

                    for model_field, file_field in field_mapping.items():
                        # Handle nested fields with dot notation
                        if "." in file_field:
                            parts = file_field.split(".")
                            value = item
                            for part in parts:
                                if isinstance(value, dict) and part in value:
                                    value = value[part]
                                else:
                                    value = None
                                    break
                        else:
                            value = item.get(file_field)

                        # Apply transformer if one exists
                        if model_field in transformers:
                            try:
                                value = transformers[model_field](value)
                            except Exception as e:
                                logger.error(
                                    f"Error transforming field {model_field} in {file_name}: {str(e)}"
                                )
                                validation_errors.append(
                                    f"Error transforming field {model_field}: {str(e)}"
                                )

                        # Apply validator if one exists
                        if model_field in validators:
                            try:
                                valid, error = validators[model_field](value)
                                if not valid:
                                    validation_errors.append(
                                        f"Validation error for {model_field}: {error}"
                                    )
                            except Exception as e:
                                logger.error(
                                    f"Error validating field {model_field} in {file_name}: {str(e)}"
                                )
                                validation_errors.append(
                                    f"Error validating field {model_field}: {str(e)}"
                                )

                        obj_data[model_field] = value

                    if validation_errors:
                        logger.warning(
                            f"Validation errors in {file_name}, skipping item: {', '.join(validation_errors)}"
                        )
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

        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in {file_name}: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e
        except Exception as e:
            logger.error(f"Error importing {file_name}: {str(e)}")
            raise

        # Commit final batch
        if batch:
            self.db.add_all(batch)
            await self.db.flush()
            total_count += len(batch)

        logger.info(f"Imported {total_count} records to {table_name}")
        return total_count

    async def _import_many_to_many_table(
        self, file_name: str, mapping: Dict[str, Any]
    ) -> int:
        """
        Import data from a JSON file to a many-to-many table.

        Args:
            file_name: Name of the file
            mapping: Mapping configuration

        Returns:
            int: Number of records imported
        """
        file_path = self.source_path / file_name
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return 0

        table_name = mapping["table_name"]
        field_mapping = mapping["field_mapping"]
        transformers = self.transformers.get(file_name, {})

        # Check if we need to clear existing data
        count = await self.db.scalar(
            text(f"SELECT COUNT(*) FROM {self.schema_name}.{table_name}")
        )

        if count > 0:
            logger.info(f"Clearing existing data from {table_name}")
            await self.db.execute(
                text(
                    f"TRUNCATE TABLE {self.schema_name}.{table_name} RESTART IDENTITY CASCADE"
                )
            )

        # Initialize tracking
        total_count = 0
        batch = []

        # Get file size for progress reporting
        file_size = file_path.stat().st_size
        processed_size = 0
        last_progress = -1

        try:
            # Load the JSON file
            with open(file_path, "r", encoding=self.encoding) as f:
                data = json.load(f)

                # Ensure data is a list
                if not isinstance(data, list):
                    # If it's a dictionary with a data field, try to use that
                    if (
                        isinstance(data, dict)
                        and "data" in data
                        and isinstance(data["data"], list)
                    ):
                        data = data["data"]
                    else:
                        # Otherwise, wrap in a list
                        data = [data]

                # Process each item
                for i, item in enumerate(data):
                    # Track progress
                    item_size = len(json.dumps(item))
                    processed_size += item_size
                    progress = int(processed_size * 100 / file_size)
                    if progress > last_progress and progress % 10 == 0:
                        logger.info(f"Importing {file_name}: {progress}% complete")
                        last_progress = progress

                    # Map and transform fields
                    row_data = {}

                    for db_field, file_field in field_mapping.items():
                        # Handle nested fields with dot notation
                        if "." in file_field:
                            parts = file_field.split(".")
                            value = item
                            for part in parts:
                                if isinstance(value, dict) and part in value:
                                    value = value[part]
                                else:
                                    value = None
                                    break
                        else:
                            value = item.get(file_field)

                        # Apply transformer if one exists
                        if db_field in transformers:
                            try:
                                value = transformers[db_field](value)
                            except Exception as e:
                                logger.error(
                                    f"Error transforming field {db_field} in {file_name}: {str(e)}"
                                )
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
                                f"INSERT INTO {self.schema_name}.{table_name} ({field_list}) VALUES ({placeholders})"
                            )

                            for data in batch:
                                await self.db.execute(query, data)

                            total_count += len(batch)
                            batch = []

                            # Force garbage collection to manage memory
                            gc.collect()

                            logger.debug(
                                f"Imported {total_count} records to {table_name}"
                            )
                        except Exception as e:
                            logger.error(
                                f"Error inserting batch into {table_name}: {str(e)}"
                            )
                            raise

        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in {file_name}: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e
        except Exception as e:
            logger.error(f"Error importing {file_name}: {str(e)}")
            raise

        # Commit final batch
        if batch:
            try:
                # Insert batch using raw SQL
                fields = list(field_mapping.keys())
                placeholders = ", ".join([f":{field}" for field in fields])
                field_list = ", ".join(fields)

                query = text(
                    f"INSERT INTO {self.schema_name}.{table_name} ({field_list}) VALUES ({placeholders})"
                )

                for data in batch:
                    await self.db.execute(query, data)

                total_count += len(batch)
            except Exception as e:
                logger.error(f"Error inserting final batch into {table_name}: {str(e)}")
                raise

        logger.info(f"Imported {total_count} records to {table_name}")
        return total_count
