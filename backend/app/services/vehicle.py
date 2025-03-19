"""
Vehicle data service for managing vehicle information and fitment data.

This module provides the VehicleDataService for retrieving vehicle details like years,
makes, models, etc., validating fitments, and decoding VINs.
"""

from __future__ import annotations
import re
from typing import Dict, List, Optional, Set, Tuple, Any

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.cache.decorators import cached
from app.core.exceptions import DatabaseException, ErrorCode, ValidationException
from app.core.logging import get_logger
from app.models.product import Fitment

logger = get_logger("app.services.vehicle")


class VehicleDataService:
    """Service for managing vehicle data and fitment information."""

    def __init__(self, db: AsyncSession):
        """Initialize the vehicle data service.

        Args:
            db: Database session for database operations.
        """
        self.db = db

    @cached(prefix="vehicle:years", ttl=3600, backend="redis")
    async def get_years(self) -> List[int]:
        """Get all available vehicle years.

        Returns:
            List[int]: A list of years in descending order.

        Raises:
            DatabaseException: If there's an error executing the database query.
        """
        try:
            result = await self.db.execute(
                select(Fitment.year).distinct().order_by(Fitment.year.desc())
            )
            years = [row[0] for row in result.all()]
            logger.debug(f"Retrieved {len(years)} vehicle years")
            return years
        except SQLAlchemyError as e:
            logger.error(
                "Failed to retrieve vehicle years", error=str(e), exc_info=True
            )
            raise DatabaseException(
                message="Failed to retrieve vehicle years",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    @cached(ttl=3600, backend="redis", prefix="vehicle:makes")
    async def get_makes(self, year: Optional[int] = None) -> List[str]:
        """Get vehicle makes, optionally filtered by year.

        Args:
            year: Optional year filter.

        Returns:
            List[str]: A list of makes in alphabetical order.

        Raises:
            DatabaseException: If there's an error executing the database query.
        """
        try:
            query = select(Fitment.make).distinct().order_by(Fitment.make)
            if year is not None:
                query = query.where(Fitment.year == year)
            result = await self.db.execute(query)
            makes = [row[0] for row in result.all()]
            logger.debug(f"Retrieved {len(makes)} vehicle makes", year=year)
            return makes
        except SQLAlchemyError as e:
            logger.error(
                "Failed to retrieve vehicle makes",
                year=year,
                error=str(e),
                exc_info=True,
            )
            raise DatabaseException(
                message="Failed to retrieve vehicle makes",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    @cached(prefix="vehicle:models", ttl=3600, backend="redis")
    async def get_models(
        self, make: Optional[str] = None, year: Optional[int] = None
    ) -> List[str]:
        """Get vehicle models, optionally filtered by make and/or year.

        Args:
            make: Optional make filter.
            year: Optional year filter.

        Returns:
            List[str]: A list of models in alphabetical order.

        Raises:
            DatabaseException: If there's an error executing the database query.
        """
        try:
            query = select(Fitment.model).distinct().order_by(Fitment.model)
            if make is not None:
                query = query.where(func.lower(Fitment.make) == make.lower())
            if year is not None:
                query = query.where(Fitment.year == year)
            result = await self.db.execute(query)
            models = [row[0] for row in result.all()]
            logger.debug(
                f"Retrieved {len(models)} vehicle models", make=make, year=year
            )
            return models
        except SQLAlchemyError as e:
            logger.error(
                "Failed to retrieve vehicle models",
                make=make,
                year=year,
                error=str(e),
                exc_info=True,
            )
            raise DatabaseException(
                message="Failed to retrieve vehicle models",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    @cached(prefix="vehicle:engines", ttl=3600, backend="redis")
    async def get_engines(
        self,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[str]:
        """Get vehicle engines, optionally filtered by make, model, and/or year.

        Args:
            make: Optional make filter.
            model: Optional model filter.
            year: Optional year filter.

        Returns:
            List[str]: A list of engines in alphabetical order.

        Raises:
            DatabaseException: If there's an error executing the database query.
        """
        try:
            query = (
                select(Fitment.engine)
                .distinct()
                .where(Fitment.engine.is_not(None))
                .order_by(Fitment.engine)
            )
            if make is not None:
                query = query.where(func.lower(Fitment.make) == make.lower())
            if model is not None:
                query = query.where(func.lower(Fitment.model) == model.lower())
            if year is not None:
                query = query.where(Fitment.year == year)
            result = await self.db.execute(query)
            engines = [row[0] for row in result.all() if row[0]]
            logger.debug(
                f"Retrieved {len(engines)} vehicle engines",
                make=make,
                model=model,
                year=year,
            )
            return engines
        except SQLAlchemyError as e:
            logger.error(
                "Failed to retrieve vehicle engines",
                make=make,
                model=model,
                year=year,
                error=str(e),
                exc_info=True,
            )
            raise DatabaseException(
                message="Failed to retrieve vehicle engines",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    @cached(prefix="vehicle:transmissions", ttl=3600, backend="redis")
    async def get_transmissions(
        self,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[int] = None,
        engine: Optional[str] = None,
    ) -> List[str]:
        """Get vehicle transmissions, optionally filtered by make, model, year, and/or engine.

        Args:
            make: Optional make filter.
            model: Optional model filter.
            year: Optional year filter.
            engine: Optional engine filter.

        Returns:
            List[str]: A list of transmissions in alphabetical order.

        Raises:
            DatabaseException: If there's an error executing the database query.
        """
        try:
            query = (
                select(Fitment.transmission)
                .distinct()
                .where(Fitment.transmission.is_not(None))
                .order_by(Fitment.transmission)
            )
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
            logger.debug(
                f"Retrieved {len(transmissions)} vehicle transmissions",
                make=make,
                model=model,
                year=year,
                engine=engine,
            )
            return transmissions
        except SQLAlchemyError as e:
            logger.error(
                "Failed to retrieve vehicle transmissions",
                make=make,
                model=model,
                year=year,
                engine=engine,
                error=str(e),
                exc_info=True,
            )
            raise DatabaseException(
                message="Failed to retrieve vehicle transmissions",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    @cached(maxsize=100, ttl=3600, backend="redis")
    async def validate_fitment(
        self,
        year: int,
        make: str,
        model: str,
        engine: Optional[str] = None,
        transmission: Optional[str] = None,
    ) -> bool:
        """Validate if a specific vehicle fitment exists.

        Args:
            year: Vehicle year.
            make: Vehicle make.
            model: Vehicle model.
            engine: Optional engine type.
            transmission: Optional transmission type.

        Returns:
            bool: True if the fitment exists, False otherwise.

        Raises:
            DatabaseException: If there's an error executing the database query.
        """
        try:
            query = select(Fitment).where(
                (Fitment.year == year)
                & (func.lower(Fitment.make) == make.lower())
                & (func.lower(Fitment.model) == model.lower())
            )
            if engine is not None:
                query = query.where(func.lower(Fitment.engine) == engine.lower())
            if transmission is not None:
                query = query.where(
                    func.lower(Fitment.transmission) == transmission.lower()
                )
            result = await self.db.execute(query.limit(1))
            is_valid = result.scalar_one_or_none() is not None
            logger.debug(
                "Validated fitment",
                year=year,
                make=make,
                model=model,
                engine=engine,
                transmission=transmission,
                is_valid=is_valid,
            )
            return is_valid
        except SQLAlchemyError as e:
            logger.error(
                "Failed to validate fitment",
                year=year,
                make=make,
                model=model,
                error=str(e),
                exc_info=True,
            )
            raise DatabaseException(
                message="Failed to validate vehicle fitment",
                code=ErrorCode.DATABASE_ERROR,
                original_exception=e,
            ) from e

    @cached(maxsize=1000, ttl=86400, backend="redis")
    async def decode_vin(self, vin: str) -> Optional[Dict[str, Any]]:
        """Decode a Vehicle Identification Number (VIN).

        Args:
            vin: The 17-character VIN to decode.

        Returns:
            Dict containing vehicle information, or None if invalid VIN.

        Raises:
            ValidationException: If the VIN format is invalid.
            ExternalServiceException: If an external VIN decoding service fails.
        """
        try:
            if not re.match("^[A-HJ-NPR-Z0-9]{17}$", vin):
                logger.warning("Invalid VIN format", vin=vin)
                raise ValidationException(
                    message="Invalid VIN format",
                    code=ErrorCode.VALIDATION_ERROR,
                    details={"vin": vin},
                )

            # In a real implementation, you'd call a VIN decoding service
            # This is a placeholder implementation
            logger.info("VIN decoded successfully", vin=vin)
            return {
                "vin": vin,
                "year": 2020,
                "make": "Example",
                "model": "Model",
                "engine": "2.0L",
                "transmission": "Automatic",
            }
        except ValidationException:
            raise
        except Exception as e:
            logger.error("Failed to decode VIN", vin=vin, error=str(e), exc_info=True)
            raise DatabaseException(
                message=f"Failed to decode VIN: {str(e)}",
                code=ErrorCode.EXTERNAL_SERVICE_ERROR,
                original_exception=e,
            ) from e

    @cached(ttl=3600, backend="redis")
    async def standardize_make(self, make: str) -> str:
        """Standardize a vehicle make name.

        Args:
            make: The make name to standardize.

        Returns:
            Standardized make name.
        """
        make_mappings = {
            "chevy": "Chevrolet",
            "vw": "Volkswagen",
            "mercedes": "Mercedes-Benz",
            "gm": "General Motors",
            "mazada": "Mazda",
        }

        make_lower = make.lower()
        if make_lower in make_mappings:
            standardized = make_mappings[make_lower]
            logger.debug("Standardized make", original=make, standardized=standardized)
            return standardized

        # Capitalize each word
        standardized = " ".join(word.capitalize() for word in make_lower.split())
        logger.debug(
            "Standardized make (word capitalization)",
            original=make,
            standardized=standardized,
        )
        return standardized

    @classmethod
    def register(cls) -> None:
        """Register this service with the service registry."""
        from app.services import service_registry

        service_registry.register(cls, "vehicle_service")


async def get_vehicle_service(db: AsyncSession = Depends(get_db)) -> VehicleDataService:
    """Dependency for getting the vehicle service.

    Args:
        db: Database session.

    Returns:
        VehicleDataService instance.
    """
    try:
        # Try to get from dependency manager first
        from app.core.dependency_manager import get_dependency

        service = get_dependency("vehicle_service", db=db)
        if service:
            return service
    except Exception:
        # Fall back to direct instantiation
        pass

    return VehicleDataService(db)


# Register the service
VehicleDataService.register()
