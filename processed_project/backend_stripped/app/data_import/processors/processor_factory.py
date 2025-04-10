from __future__ import annotations
'\nProcessor factory for data import.\n\nThis module provides a factory for creating appropriate processors based on entity type\nand source type, using centralized field definitions. It implements a registry pattern\nto map entity types to their corresponding Pydantic models and specialized processors.\n\nThe factory pattern enables flexible processor creation while maintaining consistent\nbehavior across different data types and sources.\n'
from enum import Enum
from typing import Any, Dict, Optional, Type, Union
from pydantic import BaseModel
from app.data_import.field_definitions import ENTITY_FIELD_DEFINITIONS
from app.data_import.processors.generic_processor import GenericProcessor
from app.data_import.processors.integrated_processor import IntegratedProductProcessor
from app.data_import.processors.pricing_processor import PricingProcessor
from app.data_import.schemas.pricing import ProductPricingImport
from app.domains.products.schemas import ProductCreate, ProductMeasurementCreate, ProductStockCreate
from app.logging import get_logger
logger = get_logger('app.data_import.processors.processor_factory')
class EntityType(str, Enum):
    PRODUCT = 'product'
    PRODUCT_PRICING = 'product_pricing'
    PRODUCT_STOCK = 'product_stock'
    PRODUCT_MEASUREMENT = 'product_measurement'
class SourceType(str, Enum):
    FILEMAKER = 'filemaker'
    AS400 = 'as400'
    CSV = 'csv'
class ProcessorFactory:
    _entity_model_map: Dict[EntityType, Type[BaseModel]] = {EntityType.PRODUCT: ProductCreate, EntityType.PRODUCT_STOCK: ProductStockCreate, EntityType.PRODUCT_MEASUREMENT: ProductMeasurementCreate, EntityType.PRODUCT_PRICING: ProductPricingImport}
    _specialized_processors: Dict[EntityType, Dict[SourceType, Type[GenericProcessor]]] = {EntityType.PRODUCT: {SourceType.FILEMAKER: IntegratedProductProcessor, SourceType.AS400: IntegratedProductProcessor, SourceType.CSV: IntegratedProductProcessor}, EntityType.PRODUCT_PRICING: {SourceType.AS400: PricingProcessor, SourceType.FILEMAKER: PricingProcessor, SourceType.CSV: PricingProcessor}}
    @classmethod
    def create_processor(cls, entity_type: Union[EntityType, str], source_type: Union[SourceType, str], **kwargs: Any) -> GenericProcessor:
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
        return GenericProcessor(field_definitions=field_definitions, model_type=model_type, source_type=source_type.value, **kwargs)
create_processor = ProcessorFactory.create_processor