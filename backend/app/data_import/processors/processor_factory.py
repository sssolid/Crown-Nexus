from __future__ import annotations

"""
Processor factory for data import.

This module provides a factory for creating appropriate processors based on entity type
and source type, using centralized field definitions. It implements a registry pattern
to map entity types to their corresponding Pydantic models and specialized processors.

The factory pattern enables flexible processor creation while maintaining consistent
behavior across different data types and sources.
"""
from enum import Enum
from typing import Any, Dict, Optional, Type, Union

from pydantic import BaseModel

from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS
from app.data_import.processors.generic_processor import GenericProcessor
from app.data_import.processors.integrated_processor import IntegratedProductProcessor
from app.data_import.processors.pricing_processor import PricingProcessor
from app.data_import.schemas.pricing import ProductPricingImport
from app.domains.products.schemas import (
    ProductCreate,
    ProductMeasurementCreate,
    ProductStockCreate
)
from app.logging import get_logger

logger = get_logger("app.data_import.processors.processor_factory")


class EntityType(str, Enum):
    """Enum for entity types that can be imported."""

    PRODUCT = "product"
    PRODUCT_PRICING = "product_pricing"
    PRODUCT_STOCK = "product_stock"
    PRODUCT_MEASUREMENT = "product_measurement"


class SourceType(str, Enum):
    """Enum for data source types."""

    FILEMAKER = "filemaker"
    AS400 = "as400"
    CSV = "csv"


class ProcessorFactory:
    """Factory for creating data processors."""

    # Map entity types to their corresponding model types
    _entity_model_map: Dict[EntityType, Type[BaseModel]] = {
        EntityType.PRODUCT: ProductCreate,
        EntityType.PRODUCT_STOCK: ProductStockCreate,
        EntityType.PRODUCT_MEASUREMENT: ProductMeasurementCreate,
        EntityType.PRODUCT_PRICING: ProductPricingImport
    }

    # Map entity types and source types to specialized processor classes
    _specialized_processors: Dict[EntityType, Dict[SourceType, Type[GenericProcessor]]] = {
        EntityType.PRODUCT: {
            SourceType.FILEMAKER: IntegratedProductProcessor,
            SourceType.AS400: IntegratedProductProcessor,
            SourceType.CSV: IntegratedProductProcessor
        },
        EntityType.PRODUCT_PRICING: {
            SourceType.AS400: PricingProcessor,
            SourceType.FILEMAKER: PricingProcessor,
            SourceType.CSV: PricingProcessor
        }
    }

    @classmethod
    def create_processor(
        cls,
        entity_type: Union[EntityType, str],
        source_type: Union[SourceType, str],
        **kwargs: Any
    ) -> GenericProcessor:
        """
        Create a processor for the specified entity type and source type.

        Args:
            entity_type: Type of entity to process
            source_type: Type of data source
            **kwargs: Additional arguments for the processor

        Returns:
            A processor instance

        Raises:
            ValueError: If entity type or source type is unknown
        """
        # Convert string entity type to enum if needed
        if isinstance(entity_type, str):
            try:
                entity_type = EntityType(entity_type)
            except ValueError:
                raise ValueError(f"Unknown entity type: {entity_type}")

        # Convert string source type to enum if needed
        if isinstance(source_type, str):
            try:
                source_type = SourceType(source_type)
            except ValueError:
                raise ValueError(f"Unknown source type: {source_type}")

        # Check if we have a model defined for this entity type
        if entity_type not in cls._entity_model_map:
            raise ValueError(f"No model defined for entity type: {entity_type}")

        # Get the model type
        model_type = cls._entity_model_map[entity_type]

        # Check if we have field definitions for this entity type
        if entity_type.value not in ENTITY_FIELD_DEFINITIONS:
            raise ValueError(f"No field definitions for entity type: {entity_type}")

        # Get field definitions
        field_definitions = ENTITY_FIELD_DEFINITIONS[entity_type.value]

        # If we have a specialized processor for this entity and source type, use it
        if (
            entity_type in cls._specialized_processors and
            source_type in cls._specialized_processors[entity_type]
        ):
            processor_class = cls._specialized_processors[entity_type][source_type]
            return processor_class(source_type.value, **kwargs)

        # Otherwise, use generic processor
        logger.debug(f"Using generic processor for {entity_type.value} from {source_type.value}")
        return GenericProcessor(
            field_definitions=field_definitions,
            model_type=model_type,
            source_type=source_type.value,
            **kwargs
        )


# Export the create_processor function for convenience
create_processor = ProcessorFactory.create_processor
