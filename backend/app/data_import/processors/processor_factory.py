# backend/app/data_import/processors/processor_factory.py
from __future__ import annotations

"""
Processor factory.

This module provides a factory for creating processors based on entity type
and source type, using centralized field definitions.
"""

from enum import Enum
from typing import Any, Dict, Optional, Type, Union

from pydantic import BaseModel

from app.logging import get_logger
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS
from app.data_import.processors.generic_processor import GenericProcessor
from app.data_import.processors.product_processor import ProductProcessor
from app.domains.products.schemas import (
    ProductCreate,
    ProductMeasurementCreate,
    # ProductPricingCreate,
    ProductStockCreate,
)

logger = get_logger("app.data_import.processors.processor_factory")


class EntityType(str, Enum):
    """Enum for entity types."""
    PRODUCT = "product"
    PRODUCT_PRICING = "product_pricing"
    PRODUCT_STOCK = "product_stock"
    PRODUCT_MEASUREMENT = "product_measurement"
    # Add other entity types as needed


class SourceType(str, Enum):
    """Enum for data source types."""
    FILEMAKER = "filemaker"
    AS400 = "as400"
    CSV = "csv"
    # Add other source types as needed


class ProcessorFactory:
    """Factory for creating processors based on entity and source type."""

    # Map entity types to schema models
    _entity_model_map: Dict[EntityType, Type[BaseModel]] = {
        EntityType.PRODUCT: ProductCreate,
        # EntityType.PRODUCT_PRICING: ProductPricingCreate,
        EntityType.PRODUCT_STOCK: ProductStockCreate,
        EntityType.PRODUCT_MEASUREMENT: ProductMeasurementCreate,
        # Add other mappings as needed
    }

    # Map entities to specialized processor classes
    _specialized_processors: Dict[EntityType, Dict[SourceType, Type[GenericProcessor]]] = {
        EntityType.PRODUCT: {
            SourceType.FILEMAKER: ProductProcessor,
            SourceType.AS400: ProductProcessor,
            SourceType.CSV: ProductProcessor,
        },
        # Add other specialized processor mappings as needed
    }

    @classmethod
    def create_processor(
        cls,
        entity_type: Union[EntityType, str],
        source_type: Union[SourceType, str],
        **kwargs: Any,
    ) -> GenericProcessor:
        """
        Create a processor for the specified entity and source type.

        Args:
            entity_type: Type of entity to process
            source_type: Type of data source
            **kwargs: Additional arguments for the processor

        Returns:
            Appropriate processor instance

        Raises:
            ValueError: If entity type or source type is invalid
        """
        # Convert string to enum if needed
        if isinstance(entity_type, str):
            try:
                entity_type = EntityType(entity_type)
            except ValueError:
                raise ValueError(f"Unknown entity type: {entity_type}")

        if isinstance(source_type, str):
            try:
                source_type = SourceType(source_type)
            except ValueError:
                raise ValueError(f"Unknown source type: {source_type}")

        # Get the model for this entity type
        if entity_type not in cls._entity_model_map:
            raise ValueError(f"No model defined for entity type: {entity_type}")

        model_type = cls._entity_model_map[entity_type]

        # Check if we have field definitions for this entity
        if entity_type.value not in ENTITY_FIELD_DEFINITIONS:
            raise ValueError(f"No field definitions for entity type: {entity_type}")

        field_definitions = ENTITY_FIELD_DEFINITIONS[entity_type.value]

        # Check if we have a specialized processor for this entity and source
        if (entity_type in cls._specialized_processors and
            source_type in cls._specialized_processors[entity_type]):
            processor_class = cls._specialized_processors[entity_type][source_type]
            return processor_class(source_type.value, **kwargs)

        # Fall back to generic processor
        logger.debug(
            f"Using generic processor for {entity_type.value} from {source_type.value}"
        )
        return GenericProcessor(
            field_definitions=field_definitions,
            model_type=model_type,
            source_type=source_type.value,
            **kwargs
        )


# Make it easy to import directly
create_processor = ProcessorFactory.create_processor
