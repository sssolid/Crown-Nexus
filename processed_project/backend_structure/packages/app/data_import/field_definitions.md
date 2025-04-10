# Module: app.data_import.field_definitions

**Path:** `app/data_import/field_definitions.py`

[Back to Project Index](../../../index.md)

## Imports
```python
from __future__ import annotations
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union, Set
from datetime import date, datetime, time
from functools import lru_cache
from pydantic import BaseModel, Field, ValidationError, create_model
```

## Global Variables
```python
PRODUCT_FIELDS = PRODUCT_FIELDS = EntityFieldDefinitions(
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
PRODUCT_DESCRIPTION_MAPPINGS = PRODUCT_DESCRIPTION_MAPPINGS = {
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
PRODUCT_MARKETING_MAPPINGS = PRODUCT_MARKETING_MAPPINGS = {
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
PRICING_FIELDS = PRICING_FIELDS = EntityFieldDefinitions(
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
INVENTORY_FIELDS = INVENTORY_FIELDS = EntityFieldDefinitions(
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
ENTITY_FIELD_DEFINITIONS = ENTITY_FIELD_DEFINITIONS = {
    "product": PRODUCT_FIELDS,
    "product_pricing": PRICING_FIELDS,
    "product_stock": INVENTORY_FIELDS,
}
COMPLEX_FIELD_MAPPINGS = COMPLEX_FIELD_MAPPINGS = {
    "product": {
        "descriptions": PRODUCT_DESCRIPTION_MAPPINGS,
        # "marketing": PRODUCT_MARKETING_MAPPINGS,
    },
}
```

## Functions

| Function | Description |
| --- | --- |
| `boolean_transformation` |  |
| `clean_part_number` |  |
| `generate_query_for_entity` |  |
| `normalize_part_number` |  |
| `strip_whitespace` |  |

### `boolean_transformation`
```python
def boolean_transformation(value) -> bool:
```

### `clean_part_number`
```python
def clean_part_number(value) -> str:
```

### `generate_query_for_entity`
```python
def generate_query_for_entity(entity_name, source_type, fields) -> str:
```

### `normalize_part_number`
```python
def normalize_part_number(value) -> str:
```

### `strip_whitespace`
```python
def strip_whitespace(value) -> str:
```

## Classes

| Class | Description |
| --- | --- |
| `ComplexFieldMapping` |  |
| `ComplexFieldMappingEntry` |  |
| `Config` |  |
| `EntityFieldDefinitions` |  |
| `ExternalFieldInfo` |  |
| `FieldDefinition` |  |
| `FieldTransformation` |  |
| `FieldType` |  |
| `TableInfo` |  |
| `TransformationDirection` |  |

### Class: `ComplexFieldMapping`
**Inherits from:** BaseModel

### Class: `ComplexFieldMappingEntry`
**Inherits from:** BaseModel

### Class: `Config`

#### Attributes

| Name | Value |
| --- | --- |
| `arbitrary_types_allowed` | `True` |

### Class: `EntityFieldDefinitions`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `create_pydantic_model` |  |
| `get_external_field_mapping` |  |
| `get_field_by_name` |  |
| `get_tables_for_source` |  |

##### `create_pydantic_model`
```python
@lru_cache
def create_pydantic_model(self, model_name) -> Type[BaseModel]:
```

##### `get_external_field_mapping`
```python
def get_external_field_mapping(self, source_type) -> Dict[(str, str)]:
```

##### `get_field_by_name`
```python
def get_field_by_name(self, name) -> Optional[FieldDefinition]:
```

##### `get_tables_for_source`
```python
def get_tables_for_source(self, source_type) -> Dict[(str, List[str])]:
```

### Class: `ExternalFieldInfo`
**Inherits from:** BaseModel

### Class: `FieldDefinition`
**Inherits from:** BaseModel

#### Methods

| Method | Description |
| --- | --- |
| `get_external_names` |  |
| `validate_value` |  |

##### `get_external_names`
```python
def get_external_names(self) -> Dict[(str, str)]:
```

##### `validate_value`
```python
def validate_value(self, value) -> bool:
```

### Class: `FieldTransformation`
**Inherits from:** BaseModel

### Class: `FieldType`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `STRING` | `'string'` |
| `INTEGER` | `'integer'` |
| `FLOAT` | `'float'` |
| `BOOLEAN` | `'boolean'` |
| `DATE` | `'date'` |
| `TIME` | `'time'` |
| `DATETIME` | `'datetime'` |
| `ARRAY` | `'array'` |
| `OBJECT` | `'object'` |

### Class: `TableInfo`
**Inherits from:** BaseModel

### Class: `TransformationDirection`
**Inherits from:** str, Enum

#### Attributes

| Name | Value |
| --- | --- |
| `IMPORT` | `'import'` |
| `EXPORT` | `'export'` |
