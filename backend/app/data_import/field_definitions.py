# backend/app/data_import/field_definitions.py
from __future__ import annotations

"""
Field definitions for data import.

This module provides a central source of truth for field definitions
used in data import operations, enabling consistent field handling
across connectors, processors, and importers.
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union, Set
from datetime import date, datetime, time
from functools import lru_cache

from pydantic import BaseModel, Field, ValidationError, create_model


class FieldType(str, Enum):
    """Enum for field data types."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    ARRAY = "array"
    OBJECT = "object"


class TransformationDirection(str, Enum):
    """Enum for transformation directions."""

    IMPORT = "import"  # External data to application format
    EXPORT = "export"  # Application format to external data


class TableInfo(BaseModel):
    """Information about a database table."""

    table_name: str
    is_primary: bool = False
    join_condition: Optional[str] = None


class ExternalFieldInfo(BaseModel):
    """Information about an external field."""

    field_name: str
    table_name: str
    description: Optional[str] = None


class FieldTransformation(BaseModel):
    """Configuration for field transformations."""

    direction: TransformationDirection
    source_field: str
    target_field: str
    transformation: Optional[Callable[[Any], Any]] = None

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True


class FieldDefinition(BaseModel):
    """Definition for a data field."""

    name: str
    field_type: FieldType
    required: bool = False
    description: Optional[str] = None
    default: Any = None
    validation: Optional[Callable[[Any], bool]] = None
    transformations: Optional[List[FieldTransformation]] = None
    nested_fields: Optional[List["FieldDefinition"]] = None
    enum_values: Optional[List[Any]] = None

    # Source-specific field information with table names
    external_fields: Dict[str, ExternalFieldInfo] = Field(
        default_factory=dict,
        description="Mapping of source type to external field information",
    )

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def validate_value(self, value: Any) -> bool:
        """
        Validate a value against this field definition.

        Args:
            value: Value to validate

        Returns:
            Whether the value is valid
        """
        if self.validation:
            return self.validation(value)
        return True

    def get_external_names(self) -> Dict[str, str]:
        """
        Get a map of source types to external field names.

        Returns:
            Dictionary mapping source types to external field names
        """
        return {
            source: info.field_name for source, info in self.external_fields.items()
        }


class EntityFieldDefinitions(BaseModel):
    """Field definitions for an entity type."""

    entity_name: str
    fields: List[FieldDefinition]
    primary_key_field: str
    unique_fields: List[str] = Field(default_factory=list)
    source_tables: Dict[str, List[TableInfo]] = Field(
        default_factory=dict, description="Mapping of source type to table information"
    )

    def get_field_by_name(self, name: str) -> Optional[FieldDefinition]:
        """
        Get a field definition by name.

        Args:
            name: Field name

        Returns:
            Field definition or None if not found
        """
        for field in self.fields:
            if field.name == name:
                return field
        return None

    def get_external_field_mapping(self, source_type: str) -> Dict[str, str]:
        """
        Get mapping of internal field names to external field names for a source type.

        Args:
            source_type: Source type identifier (e.g., 'filemaker', 'as400', 'csv')

        Returns:
            Dictionary mapping internal field names to external field names
        """
        mapping = {}
        for field in self.fields:
            if source_type in field.external_fields:
                mapping[field.name] = field.external_fields[source_type].field_name
        return mapping

    def get_tables_for_source(self, source_type: str) -> Dict[str, List[str]]:
        """
        Get all tables used for a given source type.

        Args:
            source_type: Source type identifier

        Returns:
            Dictionary mapping table names to lists of field names from that table
        """
        tables: Dict[str, List[str]] = {}

        for field in self.fields:
            if source_type in field.external_fields:
                table = field.external_fields[source_type].table_name
                if table not in tables:
                    tables[table] = []
                tables[table].append(field.external_fields[source_type].field_name)

        return tables

    @lru_cache
    def create_pydantic_model(self, model_name: str) -> Type[BaseModel]:
        """
        Create a Pydantic model based on these field definitions.

        Args:
            model_name: Name for the generated model

        Returns:
            Pydantic model class
        """
        field_definitions = {}

        for field in self.fields:
            # Convert field type to Python type
            python_type: Any = str

            if field.field_type == FieldType.INTEGER:
                python_type = int
            elif field.field_type == FieldType.FLOAT:
                python_type = float
            elif field.field_type == FieldType.BOOLEAN:
                python_type = bool
            elif field.field_type == FieldType.DATE:
                python_type = date
            elif field.field_type == FieldType.TIME:
                python_type = time
            elif field.field_type == FieldType.DATETIME:
                python_type = datetime
            elif field.field_type == FieldType.ARRAY:
                python_type = List[Any]
            elif field.field_type == FieldType.OBJECT:
                if field.nested_fields:
                    nested_model = create_model(
                        f"{model_name}_{field.name.capitalize()}",
                        **{
                            nested_field.name: (Any, ...)
                            for nested_field in field.nested_fields
                        },
                    )
                    python_type = nested_model
                else:
                    python_type = Dict[str, Any]

            # Handle optional fields
            if not field.required:
                python_type = Optional[python_type]

            # Create field definition
            field_definitions[field.name] = (
                python_type,
                Field(
                    default=field.default,
                    description=field.description,
                ),
            )

        # Create and return model
        return create_model(model_name, **field_definitions)


class ComplexFieldMappingEntry(BaseModel):
    """An entry for a complex field mapping."""

    source_type: str
    mapping: Dict[str, ExternalFieldInfo]


class ComplexFieldMapping(BaseModel):
    """Mapping for a complex field across different sources."""

    entity_name: str
    field_name: str
    mappings: List[ComplexFieldMappingEntry]


# Define common transformations
def boolean_transformation(value: Any) -> bool:
    """
    Transform a value to a boolean.

    Args:
        value: Input value

    Returns:
        Boolean value
    """
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0

    str_value = str(value).lower()
    true_values = ["yes", "y", "true", "t", "1", "on"]
    false_values = ["no", "n", "false", "f", "0", "off"]

    if str_value in true_values:
        return True
    if str_value in false_values:
        return False

    # Default for unexpected values
    return False


def strip_whitespace(value: Any) -> str:
    """
    Strip whitespace from a string value.

    Args:
        value: Input value

    Returns:
        Cleaned string
    """
    if value is None:
        return ""
    return str(value).strip()


def clean_part_number(value: Any) -> str:
    """
    Clean and standardize a part number.

    Args:
        value: Part number

    Returns:
        Cleaned part number
    """
    if not value:
        return ""
    # Remove extra spaces and standardize
    return str(value).strip()


def normalize_part_number(value: Any) -> str:
    """
    Normalize a part number by removing non-alphanumeric chars and converting to uppercase.

    Args:
        value: Part number

    Returns:
        Normalized part number
    """
    if not value:
        return ""
    return "".join(c for c in str(value) if c.isalnum()).upper()


# Define product field definitions with table information
PRODUCT_FIELDS = EntityFieldDefinitions(
    entity_name="product",
    primary_key_field="part_number",
    unique_fields=["part_number", "part_number_stripped"],
    # Define source tables and their relationships
    source_tables={
        "filemaker": [TableInfo(table_name="Master", is_primary=True)],
        "as400": [
            TableInfo(table_name="DSTDATA.INSMFH", is_primary=True),
            TableInfo(
                table_name="DSTDATA.INSMFT",
                join_condition="INSMFT.SPART = INSMFH.SPART",
            ),
            TableInfo(
                table_name="DSTDATA.ININTER",
                join_condition="ININTER.SPART = INSMFH.SPART",
            ),
            TableInfo(
                table_name="DSTDATA.INPTNOTE",
                join_condition="INPTNOTE.SPART = INSMFH.SPART",
            ),
        ],
    },
    fields=[
        FieldDefinition(
            name="part_number",
            field_type=FieldType.STRING,
            required=True,
            description="Product part number",
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="PartNumber",
                    table_name="Master",
                    description="Part number in FileMaker",
                ),
                "as400": ExternalFieldInfo(
                    field_name="SPART",
                    table_name="DSTDATA.INSMFH",
                    description="Part number in AS400",
                ),
                "csv": ExternalFieldInfo(
                    field_name="part_number",
                    table_name="csv_file",
                    description="Part number in CSV",
                ),
            },
            transformations=[
                FieldTransformation(
                    direction=TransformationDirection.IMPORT,
                    source_field="part_number",
                    target_field="part_number",
                    transformation=clean_part_number,
                )
            ],
        ),
        FieldDefinition(
            name="part_number_stripped",
            field_type=FieldType.STRING,
            description="Normalized part number (alphanumeric only, uppercase)",
            external_fields={
                "as400": ExternalFieldInfo(
                    field_name="SNSCHR",
                    table_name="DSTDATA.INSMFH",
                    description="Non-special character part number in AS400",
                ),
            },
            transformations=[
                FieldTransformation(
                    direction=TransformationDirection.IMPORT,
                    source_field="part_number",
                    target_field="part_number_stripped",
                    transformation=normalize_part_number,
                )
            ],
        ),
        FieldDefinition(
            name="application",
            field_type=FieldType.STRING,
            description="Product application",
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="PartApplication",
                    table_name="Master",
                    description="Application in FileMaker",
                ),
                "csv": ExternalFieldInfo(
                    field_name="application",
                    table_name="csv_file",
                    description="Application in CSV",
                ),
            },
        ),
        FieldDefinition(
            name="vintage",
            field_type=FieldType.BOOLEAN,
            description="Whether the product is vintage",
            default=False,
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="PartVintage",
                    table_name="Master",
                    description="Vintage flag in FileMaker",
                ),
                "csv": ExternalFieldInfo(
                    field_name="vintage",
                    table_name="csv_file",
                    description="Vintage flag in CSV",
                ),
            },
            transformations=[
                FieldTransformation(
                    direction=TransformationDirection.IMPORT,
                    source_field="vintage",
                    target_field="vintage",
                    transformation=boolean_transformation,
                )
            ],
        ),
        FieldDefinition(
            name="late_model",
            field_type=FieldType.BOOLEAN,
            description="Whether the product is late model",
            default=False,
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="PartLateModel",
                    table_name="Master",
                    description="Late model flag in FileMaker",
                ),
                "csv": ExternalFieldInfo(
                    field_name="late_model",
                    table_name="csv_file",
                    description="Late model flag in CSV",
                ),
            },
            transformations=[
                FieldTransformation(
                    direction=TransformationDirection.IMPORT,
                    source_field="late_model",
                    target_field="late_model",
                    transformation=boolean_transformation,
                )
            ],
        ),
        FieldDefinition(
            name="soft",
            field_type=FieldType.BOOLEAN,
            description="Whether the product is soft",
            default=False,
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="PartSoft",
                    table_name="Master",
                    description="Soft flag in FileMaker",
                ),
                "csv": ExternalFieldInfo(
                    field_name="soft",
                    table_name="csv_file",
                    description="Soft flag in CSV",
                ),
            },
            transformations=[
                FieldTransformation(
                    direction=TransformationDirection.IMPORT,
                    source_field="soft",
                    target_field="soft",
                    transformation=boolean_transformation,
                )
            ],
        ),
        FieldDefinition(
            name="universal",
            field_type=FieldType.BOOLEAN,
            description="Whether the product is universal",
            default=False,
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="PartUniversal",
                    table_name="Master",
                    description="Universal flag in FileMaker",
                ),
                "csv": ExternalFieldInfo(
                    field_name="universal",
                    table_name="csv_file",
                    description="Universal flag in CSV",
                ),
            },
            transformations=[
                FieldTransformation(
                    direction=TransformationDirection.IMPORT,
                    source_field="universal",
                    target_field="universal",
                    transformation=boolean_transformation,
                )
            ],
        ),
        FieldDefinition(
            name="is_active",
            field_type=FieldType.BOOLEAN,
            description="Whether the product is active",
            default=True,
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="ToggleActive",
                    table_name="Master",
                    description="Active flag in FileMaker",
                ),
                "csv": ExternalFieldInfo(
                    field_name="is_active",
                    table_name="csv_file",
                    description="Active flag in CSV",
                ),
            },
            transformations=[
                FieldTransformation(
                    direction=TransformationDirection.IMPORT,
                    source_field="is_active",
                    target_field="is_active",
                    transformation=boolean_transformation,
                )
            ],
        ),
        FieldDefinition(
            name="last_updated",
            field_type=FieldType.DATETIME,
            description="Last updated timestamp",
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="DateModification",
                    table_name="Master",
                    description="Last modification date in FileMaker",
                ),
                "csv": ExternalFieldInfo(
                    field_name="last_updated",
                    table_name="csv_file",
                    description="Last updated date in CSV",
                ),
            },
        ),
        FieldDefinition(
            name="descriptions",
            field_type=FieldType.ARRAY,
            description="Product descriptions",
            external_fields={},  # Complex mapping handled separately
            nested_fields=[
                FieldDefinition(
                    name="description_type",
                    field_type=FieldType.STRING,
                    required=True,
                    description="Type of description",
                ),
                FieldDefinition(
                    name="description",
                    field_type=FieldType.STRING,
                    required=True,
                    description="Description text",
                ),
            ],
        ),
        FieldDefinition(
            name="marketing",
            field_type=FieldType.ARRAY,
            description="Product marketing content",
            external_fields={},  # Complex mapping handled separately
            nested_fields=[
                FieldDefinition(
                    name="marketing_type",
                    field_type=FieldType.STRING,
                    required=True,
                    description="Type of marketing content",
                ),
                FieldDefinition(
                    name="content",
                    field_type=FieldType.STRING,
                    required=True,
                    description="Marketing content text",
                ),
                FieldDefinition(
                    name="position",
                    field_type=FieldType.INTEGER,
                    description="Display position",
                ),
            ],
        ),
    ],
)

# Define product description field mappings
PRODUCT_DESCRIPTION_MAPPINGS = {
    "filemaker": {
        "Standard": ExternalFieldInfo(
            field_name="PartDescription",
            table_name="Master",
            description="Standard description",
        ),
        "Long_AllModels": ExternalFieldInfo(
            field_name="PartDescriptionLongAllModels",
            table_name="Master",
            description="Long description for all models (80 char max)",
        ),
        "Long_JeepOnly": ExternalFieldInfo(
            field_name="PartDescriptionLongJeepOnly",
            table_name="Master",
            description="Long description for Jeep only (80 char max)",
        ),
        "Long_NonJeep": ExternalFieldInfo(
            field_name="PartDescriptionLongNonJeep",
            table_name="Master",
            description="Long description for non-Jeep (80 char max)",
        ),
        "Extended": ExternalFieldInfo(
            field_name="PartDescriptionExtended",
            table_name="Master",
            description="Extended description (240 char max)",
        ),
        "Extended_NonJeep": ExternalFieldInfo(
            field_name="PartDescriptionExtendedNonJeep",
            table_name="Master",
            description="Extended description for non-Jeep (240 char max)",
        ),
        "Extended_Unlimited": ExternalFieldInfo(
            field_name="PartDescriptionExtendedUnlimited",
            table_name="Master",
            description="Extended description with no character limit",
        ),
    },
    "as400": {
        "Short": ExternalFieldInfo(
            field_name="SDESCS",
            table_name="DSTDATA.INSMFT",
            description="Short description in AS400",
        ),
        "Long": ExternalFieldInfo(
            field_name="SDESCL",
            table_name="DSTDATA.INSMFT",
            description="Long description in AS400",
        ),
    },
    "csv": {
        "Standard": ExternalFieldInfo(
            field_name="description",
            table_name="csv_file",
            description="Standard description",
        ),
        "Long_AllModels": ExternalFieldInfo(
            field_name="description_long_all_models",
            table_name="csv_file",
            description="Long description for all models",
        ),
        "Long_JeepOnly": ExternalFieldInfo(
            field_name="description_long_jeep_only",
            table_name="csv_file",
            description="Long description for Jeep only",
        ),
        "Long_NonJeep": ExternalFieldInfo(
            field_name="description_long_non_jeep",
            table_name="csv_file",
            description="Long description for non-Jeep",
        ),
        "Extended": ExternalFieldInfo(
            field_name="description_extended",
            table_name="csv_file",
            description="Extended description",
        ),
        "Extended_NonJeep": ExternalFieldInfo(
            field_name="description_extended_non_jeep",
            table_name="csv_file",
            description="Extended description for non-Jeep",
        ),
        "Extended_Unlimited": ExternalFieldInfo(
            field_name="description_extended_unlimited",
            table_name="csv_file",
            description="Extended description with no character limit",
        ),
    },
}

# Define product marketing field mappings
PRODUCT_MARKETING_MAPPINGS = {
    "filemaker": {
        "Ad Copy": ExternalFieldInfo(
            field_name="RTOffRoadAdCopy",
            table_name="Master",
            description="Marketing advertisement copy",
        ),
        "Bullet1": ExternalFieldInfo(
            field_name="RTOffRoadBullet1",
            table_name="Master",
            description="Marketing bullet point 1",
        ),
        "Bullet2": ExternalFieldInfo(
            field_name="RTOffRoadBullet2",
            table_name="Master",
            description="Marketing bullet point 2",
        ),
        "Bullet3": ExternalFieldInfo(
            field_name="RTOffRoadBullet3",
            table_name="Master",
            description="Marketing bullet point 3",
        ),
        "Bullet4": ExternalFieldInfo(
            field_name="RTOffRoadBullet4",
            table_name="Master",
            description="Marketing bullet point 4",
        ),
        "Bullet5": ExternalFieldInfo(
            field_name="RTOffRoadBullet5",
            table_name="Master",
            description="Marketing bullet point 5",
        ),
        "Bullet6": ExternalFieldInfo(
            field_name="RTOffRoadBullet6",
            table_name="Master",
            description="Marketing bullet point 6",
        ),
        "Bullet7": ExternalFieldInfo(
            field_name="RTOffRoadBullet7",
            table_name="Master",
            description="Marketing bullet point 7",
        ),
        "Bullet8": ExternalFieldInfo(
            field_name="RTOffRoadBullet8",
            table_name="Master",
            description="Marketing bullet point 8",
        ),
        "Bullet9": ExternalFieldInfo(
            field_name="RTOffRoadBullet9",
            table_name="Master",
            description="Marketing bullet point 9",
        ),
        "Bullet10": ExternalFieldInfo(
            field_name="RTOffRoadBullet10",
            table_name="Master",
            description="Marketing bullet point 10",
        ),
        "Bullet11": ExternalFieldInfo(
            field_name="RTOffRoadBullet11",
            table_name="Master",
            description="Marketing bullet point 11",
        ),
    },
    "csv": {
        "AdCopy": ExternalFieldInfo(
            field_name="ad_copy",
            table_name="csv_file",
            description="Marketing advertisement copy",
        ),
        "Bullet1": ExternalFieldInfo(
            field_name="bullet_point_1",
            table_name="csv_file",
            description="Marketing bullet point 1",
        ),
        "Bullet2": ExternalFieldInfo(
            field_name="bullet_point_2",
            table_name="csv_file",
            description="Marketing bullet point 2",
        ),
        "Bullet3": ExternalFieldInfo(
            field_name="bullet_point_3",
            table_name="csv_file",
            description="Marketing bullet point 3",
        ),
        "Bullet4": ExternalFieldInfo(
            field_name="bullet_point_4",
            table_name="csv_file",
            description="Marketing bullet point 4",
        ),
        "Bullet5": ExternalFieldInfo(
            field_name="bullet_point_5",
            table_name="csv_file",
            description="Marketing bullet point 5",
        ),
        "Bullet6": ExternalFieldInfo(
            field_name="bullet_point_6",
            table_name="csv_file",
            description="Marketing bullet point 6",
        ),
        "Bullet7": ExternalFieldInfo(
            field_name="bullet_point_7",
            table_name="csv_file",
            description="Marketing bullet point 7",
        ),
        "Bullet8": ExternalFieldInfo(
            field_name="bullet_point_8",
            table_name="csv_file",
            description="Marketing bullet point 8",
        ),
        "Bullet9": ExternalFieldInfo(
            field_name="bullet_point_9",
            table_name="csv_file",
            description="Marketing bullet point 9",
        ),
        "Bullet10": ExternalFieldInfo(
            field_name="bullet_point_10",
            table_name="csv_file",
            description="Marketing bullet point 10",
        ),
        "Bullet11": ExternalFieldInfo(
            field_name="bullet_point_11",
            table_name="csv_file",
            description="Marketing bullet point 11",
        ),
    },
}

# Define pricing fields
PRICING_FIELDS = EntityFieldDefinitions(
    entity_name="product_pricing",
    primary_key_field="part_number",
    unique_fields=["part_number", "pricing_type"],
    source_tables={
        "as400": [
            TableInfo(table_name="DSTDATA.INSMFH", is_primary=True),
        ],
    },
    fields=[
        FieldDefinition(
            name="part_number",
            field_type=FieldType.STRING,
            required=True,
            description="Product part number",
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="PartNumber",
                    table_name="Master",
                    description="Part number in FileMaker",
                ),
                "as400": ExternalFieldInfo(
                    field_name="SPART",
                    table_name="DSTDATA.INSMFH",
                    description="Part number in AS400",
                ),
                "csv": ExternalFieldInfo(
                    field_name="part_number",
                    table_name="csv_file",
                    description="Part number in CSV",
                ),
            },
        ),
        # We don't need external mappings for pricing_type as it's handled by the processor
        FieldDefinition(
            name="pricing_type",
            field_type=FieldType.STRING,
            required=True,
            description="Pricing type (Jobber or Export)",
            enum_values=["Jobber", "Export"],
        ),
        # Include both price fields in the main AS400 source type
        FieldDefinition(
            name="price",
            field_type=FieldType.FLOAT,
            required=True,
            description="Price value",
            external_fields={
                "as400": ExternalFieldInfo(  # Changed to include both price fields in query
                    field_name="SRET1, SRET2",  # This will ensure both fields are in the query
                    table_name="DSTDATA.INSMFH",
                    description="Price fields in AS400 (Jobber and Export)",
                ),
                "csv": ExternalFieldInfo(
                    field_name="price",
                    table_name="csv_file",
                    description="Price in CSV",
                ),
            },
        ),
        FieldDefinition(
            name="currency",
            field_type=FieldType.STRING,
            description="Currency code",
            default="USD",
        ),
    ],
)

# Define inventory fields
INVENTORY_FIELDS = EntityFieldDefinitions(
    entity_name="product_stock",
    primary_key_field="part_number",
    unique_fields=["part_number"],
    source_tables={
        "as400": [
            TableInfo(table_name="DSTDATA.INSMFH", is_primary=True),
        ],
    },
    fields=[
        FieldDefinition(
            name="part_number",
            field_type=FieldType.STRING,
            required=True,
            description="Product part number",
            external_fields={
                "filemaker": ExternalFieldInfo(
                    field_name="PartNumber",
                    table_name="Master",
                    description="Part number in FileMaker",
                ),
                "as400": ExternalFieldInfo(
                    field_name="spart",
                    table_name="DSTDATA.INSMFH",
                    description="Part number in AS400",
                ),
                "csv": ExternalFieldInfo(
                    field_name="part_number",
                    table_name="csv_file",
                    description="Part number in CSV",
                ),
            },
        ),
        FieldDefinition(
            name="quantity",
            field_type=FieldType.INTEGER,
            required=True,
            description="Stock quantity",
            default=0,
            external_fields={
                "as400": ExternalFieldInfo(
                    field_name="SCLSK",
                    table_name="DSTDATA.INSMFH",
                    description="Stock quantity in AS400",
                ),
                "csv": ExternalFieldInfo(
                    field_name="quantity",
                    table_name="csv_file",
                    description="Quantity in CSV",
                ),
            },
            transformations=[
                FieldTransformation(
                    direction=TransformationDirection.IMPORT,
                    source_field="quantity",
                    target_field="quantity",
                    # Ensure quantity is not negative
                    transformation=lambda v: (
                        max(0, int(float(v))) if v is not None else 0
                    ),
                )
            ],
        ),
        FieldDefinition(
            name="last_updated",
            field_type=FieldType.DATETIME,
            description="Last update timestamp",
            # This will be set programmatically at import time
        ),
    ],
)

# Create a registry of all entity field definitions
ENTITY_FIELD_DEFINITIONS = {
    "product": PRODUCT_FIELDS,
    "product_pricing": PRICING_FIELDS,
    "product_stock": INVENTORY_FIELDS,
}

# Complex field mappings registry
COMPLEX_FIELD_MAPPINGS = {
    "product": {
        "descriptions": PRODUCT_DESCRIPTION_MAPPINGS,
        # "marketing": PRODUCT_MARKETING_MAPPINGS,
    },
}


# Update to query generation in field_definitions.py for better complex field handling


def generate_query_for_entity(
    entity_name: str, source_type: str, fields: Optional[List[str]] = None
) -> str:
    """Generate a SQL query for extracting entity data from a specific source.

    Args:
        entity_name: Name of the entity to query (e.g., 'product', 'product_pricing')
        source_type: Type of data source (e.g., 'filemaker', 'as400', 'csv')
        fields: Optional list of field names to include in the query

    Returns:
        SQL query string

    Raises:
        ValueError: If the entity or source type is not supported
        ValueError: If no fields are available for the query
    """
    if entity_name not in ENTITY_FIELD_DEFINITIONS:
        raise ValueError(f"Unknown entity: {entity_name}")

    entity_def = ENTITY_FIELD_DEFINITIONS[entity_name]

    if source_type not in entity_def.source_tables:
        raise ValueError(
            f"Source type {source_type} not supported for entity {entity_name}"
        )

    tables_info = entity_def.source_tables[source_type]
    primary_table = None
    for table_info in tables_info:
        if table_info.is_primary:
            primary_table = table_info.table_name
            break

    if not primary_table:
        raise ValueError(f"No primary table defined for {entity_name} in {source_type}")

    # Special case for AS400 product pricing
    if entity_name == "product_pricing" and source_type == "as400":
        # DO NOT use column aliases (AS) for AS400 queries
        return f"""
            SELECT
                SPART,
                SRET1,
                SRET2
            FROM {primary_table}
            WHERE (SRET1 IS NOT NULL OR SRET2 IS NOT NULL)
        """

    # Special case for product with descriptions and marketing from AS400
    if entity_name == "product" and source_type == "as400":
        # Include all basic product fields
        basic_fields = ["SPART"]  # Part number is essential

        # Find other basic fields from field definitions
        for field in entity_def.fields:
            if source_type in field.external_fields and field.name not in [
                "descriptions",
                "marketing",
            ]:
                field_info = field.external_fields[source_type]
                if field_info.field_name != "SPART":  # Already added
                    basic_fields.append(field_info.field_name)

        # Add description fields
        description_fields = []
        if "descriptions" in COMPLEX_FIELD_MAPPINGS.get("product", {}):
            desc_mappings = COMPLEX_FIELD_MAPPINGS["product"]["descriptions"].get(
                source_type, {}
            )
            for desc_type, field_info in desc_mappings.items():
                if isinstance(field_info, ExternalFieldInfo):
                    description_fields.append(field_info.field_name)

        # Add marketing fields
        marketing_fields = []
        if "marketing" in COMPLEX_FIELD_MAPPINGS.get("product", {}):
            mkt_mappings = COMPLEX_FIELD_MAPPINGS["product"]["marketing"].get(
                source_type, {}
            )
            for mkt_type, field_info in mkt_mappings.items():
                if isinstance(field_info, ExternalFieldInfo):
                    marketing_fields.append(field_info.field_name)

        # Combine all fields for the query
        all_fields = basic_fields + description_fields + marketing_fields
        fields_clause = ", ".join(all_fields)

        return f"""
            SELECT {fields_clause}
            FROM {primary_table}
            WHERE SPART IS NOT NULL
        """

    # Standard field mapping for other cases
    if fields is None:
        field_mappings = []
        for field in entity_def.fields:
            if source_type in field.external_fields:
                field_info = field.external_fields[source_type]
                # Handle comma-separated field names (for multiple price fields)
                if "," in field_info.field_name:
                    for subfield in [
                        f.strip() for f in field_info.field_name.split(",")
                    ]:
                        # For AS400, don't use column aliases to avoid potential field name issues
                        if source_type == "as400":
                            field_mappings.append(f"{field_info.table_name}.{subfield}")
                        else:
                            field_mappings.append(
                                f"{field_info.table_name}.{subfield} AS {subfield}"
                            )
                else:
                    # For AS400, don't use column aliases to avoid potential field name issues
                    if source_type == "as400":
                        field_mappings.append(
                            f"{field_info.table_name}.{field_info.field_name}"
                        )
                    else:
                        # IMPORTANT: Don't use aliases here - use the field name directly
                        field_mappings.append(
                            f"{field_info.table_name}.{field_info.field_name}"
                        )

        # For complex fields, don't use aliases in the query
        if entity_name in COMPLEX_FIELD_MAPPINGS:
            for complex_field, mappings in COMPLEX_FIELD_MAPPINGS[entity_name].items():
                if source_type in mappings:
                    for type_name, field_info in mappings[source_type].items():
                        if isinstance(field_info, ExternalFieldInfo):
                            # Important: Remove the "AS type_name" alias
                            field_mappings.append(
                                f"{field_info.table_name}.{field_info.field_name}"
                            )
    else:
        field_mappings = []
        for field_name in fields:
            field = entity_def.get_field_by_name(field_name)
            if field and source_type in field.external_fields:
                field_info = field.external_fields[source_type]
                # For AS400, don't use column aliases to avoid potential field name issues
                if source_type == "as400":
                    field_mappings.append(
                        f"{field_info.table_name}.{field_info.field_name}"
                    )
                else:
                    field_mappings.append(
                        f"{field_info.table_name}.{field_info.field_name} AS {field.name}"
                    )

    if not field_mappings:
        raise ValueError(
            f"No fields available for entity {entity_name} from source {source_type}"
        )

    field_list = ", ".join(field_mappings)
    from_clause = primary_table
    joins = []
    for table_info in tables_info:
        if not table_info.is_primary and table_info.join_condition:
            joins.append(
                f"LEFT JOIN {table_info.table_name} ON {table_info.join_condition}"
            )
    join_clause = " ".join(joins)

    if source_type == "filemaker":
        return f"SELECT {field_list} FROM {from_clause} {join_clause}"
    elif source_type.startswith("as400"):
        return f"SELECT {field_list} FROM {from_clause} {join_clause}"
    else:
        return f"SELECT {field_list} FROM {from_clause} {join_clause}"
