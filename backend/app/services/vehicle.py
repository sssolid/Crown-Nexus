# backend/app/services/vehicle.py
"""
Vehicle data lookup service.

This module provides:
- Year/Make/Model lookup capabilities
- Vehicle identification number (VIN) decoding
- Engine and transmission data
- Vehicle attribute validation

These services support product fitment functionality by providing
standardized vehicle data and validation.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Set, Tuple

from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.product import Fitment
from app.utils.cache import memory_cache, redis_cache


class VehicleDataService:
    """
    Service for vehicle data lookups and validation.

    This service provides methods for working with vehicle data,
    including lookups, validation, and standardization.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the vehicle data service.

        Args:
            db: Database session
        """
        self.db = db

    @redis_cache(prefix="vehicle:years", ttl=3600)
    async def get_years(self) -> List[int]:
        """
        Get all available years from fitment data.

        Returns:
            List[int]: Sorted list of years
        """
        result = await self.db.execute(
            select(Fitment.year)
            .distinct()
            .order_by(Fitment.year.desc())
        )
        years = [row[0] for row in result.all()]
        return years

    @redis_cache(prefix="vehicle:makes", ttl=3600)
    async def get_makes(self, year: Optional[int] = None) -> List[str]:
        """
        Get all available makes, optionally filtered by year.

        Args:
            year: Filter by year

        Returns:
            List[str]: Sorted list of makes
        """
        query = select(Fitment.make).distinct().order_by(Fitment.make)

        if year is not None:
            query = query.where(Fitment.year == year)

        result = await self.db.execute(query)
        makes = [row[0] for row in result.all()]
        return makes

    @redis_cache(prefix="vehicle:models", ttl=3600)
    async def get_models(
        self, make: Optional[str] = None, year: Optional[int] = None
    ) -> List[str]:
        """
        Get all available models, optionally filtered by make and year.

        Args:
            make: Filter by make
            year: Filter by year

        Returns:
            List[str]: Sorted list of models
        """
        query = select(Fitment.model).distinct().order_by(Fitment.model)

        if make is not None:
            query = query.where(func.lower(Fitment.make) == make.lower())

        if year is not None:
            query = query.where(Fitment.year == year)

        result = await self.db.execute(query)
        models = [row[0] for row in result.all()]
        return models

    @redis_cache(prefix="vehicle:engines", ttl=3600)
    async def get_engines(
        self,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[int] = None
    ) -> List[str]:
        """
        Get all available engines, optionally filtered by make, model, and year.

        Args:
            make: Filter by make
            model: Filter by model
            year: Filter by year

        Returns:
            List[str]: Sorted list of engines
        """
        query = select(Fitment.engine).distinct().where(
            Fitment.engine.is_not(None)
        ).order_by(Fitment.engine)

        if make is not None:
            query = query.where(func.lower(Fitment.make) == make.lower())

        if model is not None:
            query = query.where(func.lower(Fitment.model) == model.lower())

        if year is not None:
            query = query.where(Fitment.year == year)

        result = await self.db.execute(query)
        engines = [row[0] for row in result.all() if row[0]]
        return engines

    @redis_cache(prefix="vehicle:transmissions", ttl=3600)
    async def get_transmissions(
        self,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[int] = None,
        engine: Optional[str] = None
    ) -> List[str]:
        """
        Get all available transmissions, optionally filtered.

        Args:
            make: Filter by make
            model: Filter by model
            year: Filter by year
            engine: Filter by engine

        Returns:
            List[str]: Sorted list of transmissions
        """
        query = select(Fitment.transmission).distinct().where(
            Fitment.transmission.is_not(None)
        ).order_by(Fitment.transmission)

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
        return transmissions

    @memory_cache(maxsize=100, ttl=3600)
    async def validate_fitment(
        self, year: int, make: str, model: str,
        engine: Optional[str] = None, transmission: Optional[str] = None
    ) -> bool:
        """
        Validate if a fitment combination exists.

        Args:
            year: Vehicle year
            make: Vehicle make
            model: Vehicle model
            engine: Vehicle engine
            transmission: Vehicle transmission

        Returns:
            bool: True if fitment exists
        """
        query = select(Fitment).where(
            (Fitment.year == year) &
            (func.lower(Fitment.make) == make.lower()) &
            (func.lower(Fitment.model) == model.lower())
        )

        if engine is not None:
            query = query.where(func.lower(Fitment.engine) == engine.lower())

        if transmission is not None:
            query = query.where(func.lower(Fitment.transmission) == transmission.lower())

        result = await self.db.execute(query.limit(1))
        return result.scalar_one_or_none() is not None

    @memory_cache(maxsize=1000, ttl=86400)  # Cache for 24 hours
    async def decode_vin(self, vin: str) -> Optional[Dict[str, Any]]:
        """
        Decode a Vehicle Identification Number (VIN).

        This method could integrate with an external VIN decoding service
        or use internal logic to parse VIN information.

        Args:
            vin: Vehicle Identification Number

        Returns:
            Optional[Dict[str, Any]]: Decoded vehicle data or None if invalid
        """
        # Basic VIN validation (should be 17 characters for modern vehicles)
        if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
            return None

        # In a real implementation, this would call an external service
        # or use a local database of VIN patterns
        # For now, we'll return a placeholder
        return {
            "vin": vin,
            "year": 2020,  # Placeholder
            "make": "Example",  # Placeholder
            "model": "Model",  # Placeholder
            "engine": "2.0L",  # Placeholder
            "transmission": "Automatic",  # Placeholder
        }

    @memory_cache(maxsize=100, ttl=3600)
    async def standardize_make(self, make: str) -> str:
        """
        Standardize vehicle make to ensure consistent naming.

        Args:
            make: Vehicle make

        Returns:
            str: Standardized make name
        """
        # Common make name mappings (lowercase to standard form)
        make_mappings = {
            "chevy": "Chevrolet",
            "vw": "Volkswagen",
            "mercedes": "Mercedes-Benz",
            "gm": "General Motors",
            "mazada": "Mazda",  # Common misspelling
        }

        # Convert to lowercase for lookup
        make_lower = make.lower()

        # Return standardized name if available, otherwise capitalize
        if make_lower in make_mappings:
            return make_mappings[make_lower]

        # Capitalize each word (e.g., "land rover" -> "Land Rover")
        return " ".join(word.capitalize() for word in make_lower.split())


# Dependency for the vehicle data service
async def get_vehicle_service(db: AsyncSession = Depends(get_db)) -> VehicleDataService:
    """
    Get vehicle data service instance.

    Args:
        db: Database session

    Returns:
        VehicleDataService: Vehicle data service
    """
    return VehicleDataService(db)
