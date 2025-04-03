from __future__ import annotations

"""Processor factory for data import.

This module provides a factory for creating appropriate processors based on entity type
and source type, using centralized field definitions. It implements a registry pattern
to map entity types to their corresponding Pydantic models and specialized processors.

The factory pattern enables flexible processor creation while maintaining consistent
behavior across different data types and sources.
"""
from enum import Enum
from typing import Any, Dict, Optional, Type, Union
from pydantic import BaseModel
from app.logging import get_logger
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS
from app.data_import.processors.generic_processor import GenericProcessor
from app.data_import.processors.product_processor import ProductProcessor
from app.data_import.processors.pricing_processor import PricingProcessor
from app.domains.products.schemas import (
    ProductCreate,
    ProductMeasurementCreate,
    ProductStockCreate,
)
# Import the new schema for price imports
from app.data_import.schemas.pricing import ProductPricingImport

logger = get_logger('app.data_import.processors.processor_factory')


class EntityType(str, Enum):
    """Enumeration of supported entity types for data processing.

    This enum defines the valid entity types that can be processed by the factory.
    Each value corresponds to a specific domain entity in the application.

    Attributes:
        PRODUCT: Basic product information
        PRODUCT_PRICING: Product pricing data
        PRODUCT_STOCK: Product inventory/stock information
        PRODUCT_MEASUREMENT: Product physical dimensions and measurements
    """
    PRODUCT = 'product'
    PRODUCT_PRICING = 'product_pricing'
    PRODUCT_STOCK = 'product_stock'
    PRODUCT_MEASUREMENT = 'product_measurement'


class SourceType(str, Enum):
    """Enumeration of supported data source types.

    This enum defines the valid source types that data can be imported from.
    Each value corresponds to a specific external system or file format.

    Attributes:
        FILEMAKER: FileMaker Pro database
        AS400: IBM AS/400 (iSeries) database
        CSV: Comma-separated values file
    """
    FILEMAKER = 'filemaker'
    AS400 = 'as400'
    CSV = 'csv'


class ProcessorFactory:
    """Factory for creating data processors based on entity and source type.

    This class maps entity types to their corresponding Pydantic models and
    specialized processors. It provides a centralized way to create appropriate
    processors for different data types from various sources.

    Attributes:
        _entity_model_map: Mapping of entity types to their Pydantic model classes
        _specialized_processors: Registry of specialized processors for specific
            entity and source type combinations
    """
    _entity_model_map: Dict[EntityType, Type[BaseModel]] = {
        EntityType.PRODUCT: ProductCreate,
        EntityType.PRODUCT_STOCK: ProductStockCreate,
        EntityType.PRODUCT_MEASUREMENT: ProductMeasurementCreate,
        EntityType.PRODUCT_PRICING: ProductPricingImport,  # Use the import schema
    }

    _specialized_processors: Dict[EntityType, Dict[SourceType, Type[GenericProcessor]]] = {
        EntityType.PRODUCT: {
            SourceType.FILEMAKER: ProductProcessor,
            SourceType.AS400: ProductProcessor,
            SourceType.CSV: ProductProcessor
        },
        # Add the specialized pricing processor for AS400
        EntityType.PRODUCT_PRICING: {
            SourceType.AS400: PricingProcessor,
        }
    }

    @classmethod
    def create_processor(
        cls, entity_type: Union[EntityType, str], source_type: Union[SourceType, str], **kwargs: Any
    ) -> GenericProcessor:
        """Create an appropriate processor for the specified entity and source type.

        This method normalizes string inputs to enum values, validates that the
        requested entity type is supported, and returns either a specialized
        processor if available or falls back to a generic processor.

        Args:
            entity_type: Type of entity to process (e.g., 'product', 'product_pricing')
            source_type: Type of data source (e.g., 'filemaker', 'as400', 'csv')
            **kwargs: Additional keyword arguments to pass to the processor constructor

        Returns:
            An instance of a processor suitable for the specified entity and source

        Raises:
            ValueError: If the entity type or source type is not recognized
            ValueError: If no model is defined for the entity type
            ValueError: If no field definitions exist for the entity type
        """
        if isinstance(entity_type, str):
            try:
                entity_type = EntityType(entity_type)
            except ValueError:
                raise ValueError(f'Unknown entity type: {entity_type}')

        if isinstance(source_type, str):
            try:
                source_type = SourceType(source_type)
            except ValueError:
                raise ValueError(f'Unknown source type: {source_type}')

        if entity_type not in cls._entity_model_map:
            raise ValueError(f'No model defined for entity type: {entity_type}')

        model_type = cls._entity_model_map[entity_type]

        if entity_type.value not in ENTITY_FIELD_DEFINITIONS:
            raise ValueError(f'No field definitions for entity type: {entity_type}')

        field_definitions = ENTITY_FIELD_DEFINITIONS[entity_type.value]

        if entity_type in cls._specialized_processors and source_type in cls._specialized_processors[entity_type]:
            processor_class = cls._specialized_processors[entity_type][source_type]
            return processor_class(source_type.value, **kwargs)

        logger.debug(f'Using generic processor for {entity_type.value} from {source_type.value}')
        return GenericProcessor(
            field_definitions=field_definitions, model_type=model_type, source_type=source_type.value, **kwargs
        )


create_processor = ProcessorFactory.create_processor
