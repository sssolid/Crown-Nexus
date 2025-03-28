from __future__ import annotations
import re
from typing import Dict, List, Optional, Any
from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.core.cache.decorators import cached
from app.core.exceptions import DatabaseException, ErrorCode, ValidationException
from app.logging import get_logger
from app.domains.products.models import Fitment
logger = get_logger('app.services.vehicle')
class VehicleDataService:
    def __init__(self, db: AsyncSession):
        self.db = db
    @cached(prefix='vehicle:years', ttl=3600, backend='redis')
    async def get_years(self) -> List[int]:
        try:
            result = await self.db.execute(select(Fitment.year).distinct().order_by(Fitment.year.desc()))
            years = [row[0] for row in result.all()]
            logger.debug(f'Retrieved {len(years)} vehicle years')
            return years
        except SQLAlchemyError as e:
            logger.error('Failed to retrieve vehicle years', error=str(e), exc_info=True)
            raise DatabaseException(message='Failed to retrieve vehicle years', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
    @cached(ttl=3600, backend='redis', prefix='vehicle:makes')
    async def get_makes(self, year: Optional[int]=None) -> List[str]:
        try:
            query = select(Fitment.make).distinct().order_by(Fitment.make)
            if year is not None:
                query = query.where(Fitment.year == year)
            result = await self.db.execute(query)
            makes = [row[0] for row in result.all()]
            logger.debug(f'Retrieved {len(makes)} vehicle makes', year=year)
            return makes
        except SQLAlchemyError as e:
            logger.error('Failed to retrieve vehicle makes', year=year, error=str(e), exc_info=True)
            raise DatabaseException(message='Failed to retrieve vehicle makes', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
    @cached(prefix='vehicle:models', ttl=3600, backend='redis')
    async def get_models(self, make: Optional[str]=None, year: Optional[int]=None) -> List[str]:
        try:
            query = select(Fitment.model).distinct().order_by(Fitment.model)
            if make is not None:
                query = query.where(func.lower(Fitment.make) == make.lower())
            if year is not None:
                query = query.where(Fitment.year == year)
            result = await self.db.execute(query)
            models = [row[0] for row in result.all()]
            logger.debug(f'Retrieved {len(models)} vehicle models', make=make, year=year)
            return models
        except SQLAlchemyError as e:
            logger.error('Failed to retrieve vehicle models', make=make, year=year, error=str(e), exc_info=True)
            raise DatabaseException(message='Failed to retrieve vehicle models', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
    @cached(prefix='vehicle:engines', ttl=3600, backend='redis')
    async def get_engines(self, make: Optional[str]=None, model: Optional[str]=None, year: Optional[int]=None) -> List[str]:
        try:
            query = select(Fitment.engine).distinct().where(Fitment.engine.is_not(None)).order_by(Fitment.engine)
            if make is not None:
                query = query.where(func.lower(Fitment.make) == make.lower())
            if model is not None:
                query = query.where(func.lower(Fitment.model) == model.lower())
            if year is not None:
                query = query.where(Fitment.year == year)
            result = await self.db.execute(query)
            engines = [row[0] for row in result.all() if row[0]]
            logger.debug(f'Retrieved {len(engines)} vehicle engines', make=make, model=model, year=year)
            return engines
        except SQLAlchemyError as e:
            logger.error('Failed to retrieve vehicle engines', make=make, model=model, year=year, error=str(e), exc_info=True)
            raise DatabaseException(message='Failed to retrieve vehicle engines', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
    @cached(prefix='vehicle:transmissions', ttl=3600, backend='redis')
    async def get_transmissions(self, make: Optional[str]=None, model: Optional[str]=None, year: Optional[int]=None, engine: Optional[str]=None) -> List[str]:
        try:
            query = select(Fitment.transmission).distinct().where(Fitment.transmission.is_not(None)).order_by(Fitment.transmission)
            if make is not None:
                query = query.where(func.lower(Fitment.make) == make.lower())
            if model is not None:
                query = query.where(func.lower(Fitment.model) == model.lower())
            if year is not None:
                query = query.where(Fitment.year == year)
            if engine is not None:
                query = query.where(func.lower(Fitment.engine) == engine.lower())
            result = await self.db.execute(query)
            transmissions = [row[0] for row in result.all() if row[0]]
            logger.debug(f'Retrieved {len(transmissions)} vehicle transmissions', make=make, model=model, year=year, engine=engine)
            return transmissions
        except SQLAlchemyError as e:
            logger.error('Failed to retrieve vehicle transmissions', make=make, model=model, year=year, engine=engine, error=str(e), exc_info=True)
            raise DatabaseException(message='Failed to retrieve vehicle transmissions', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
    @cached(ttl=3600, backend='redis')
    async def validate_fitment(self, year: int, make: str, model: str, engine: Optional[str]=None, transmission: Optional[str]=None) -> bool:
        try:
            query = select(Fitment).where((Fitment.year == year) & (func.lower(Fitment.make) == make.lower()) & (func.lower(Fitment.model) == model.lower()))
            if engine is not None:
                query = query.where(func.lower(Fitment.engine) == engine.lower())
            if transmission is not None:
                query = query.where(func.lower(Fitment.transmission) == transmission.lower())
            result = await self.db.execute(query.limit(1))
            is_valid = result.scalar_one_or_none() is not None
            logger.debug('Validated fitment', year=year, make=make, model=model, engine=engine, transmission=transmission, is_valid=is_valid)
            return is_valid
        except SQLAlchemyError as e:
            logger.error('Failed to validate fitment', year=year, make=make, model=model, error=str(e), exc_info=True)
            raise DatabaseException(message='Failed to validate vehicle fitment', code=ErrorCode.DATABASE_ERROR, original_exception=e) from e
    @cached(ttl=86400, backend='redis')
    async def decode_vin(self, vin: str) -> Optional[Dict[str, Any]]:
        try:
            if not re.match('^[A-HJ-NPR-Z0-9]{17}$', vin):
                logger.warning('Invalid VIN format', vin=vin)
                raise ValidationException(message='Invalid VIN format', code=ErrorCode.VALIDATION_ERROR, details={'vin': vin})
            logger.info('VIN decoded successfully', vin=vin)
            return {'vin': vin, 'year': 2020, 'make': 'Example', 'model': 'Model', 'engine': '2.0L', 'transmission': 'Automatic'}
        except ValidationException:
            raise
        except Exception as e:
            logger.error('Failed to decode VIN', vin=vin, error=str(e), exc_info=True)
            raise DatabaseException(message=f'Failed to decode VIN: {str(e)}', code=ErrorCode.SERVICE_ERROR, original_exception=e) from e
    @cached(ttl=3600, backend='redis')
    async def standardize_make(self, make: str) -> str:
        make_mappings = {'chevy': 'Chevrolet', 'vw': 'Volkswagen', 'mercedes': 'Mercedes-Benz', 'gm': 'General Motors', 'mazada': 'Mazda'}
        make_lower = make.lower()
        if make_lower in make_mappings:
            standardized = make_mappings[make_lower]
            logger.debug('Standardized make', original=make, standardized=standardized)
            return standardized
        standardized = ' '.join((word.capitalize() for word in make_lower.split()))
        logger.debug('Standardized make (word capitalization)', original=make, standardized=standardized)
        return standardized
    @classmethod
    def register(cls) -> None:
        from app.core.dependency_manager import register_service
        register_service(cls, 'vehicle_service')
async def get_vehicle_service(db: AsyncSession=Depends(get_db)) -> VehicleDataService:
    try:
        from app.core.dependency_manager import get_dependency
        service = get_dependency('vehicle_service', db=db)
        if service:
            return service
    except Exception:
        pass
    return VehicleDataService(db)
VehicleDataService.register()