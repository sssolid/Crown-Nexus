from __future__ import annotations

"""Currency repository implementation.

This module provides data access and persistence operations for Currency entities.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.currency.models import Currency, ExchangeRate
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, BusinessException


class CurrencyRepository(BaseRepository[Currency, uuid.UUID]):
    """Repository for Currency entity operations.

    Provides methods for querying, creating, updating, and deleting
    Currency entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the currency repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Currency, db=db)

    async def find_by_code(self, code: str) -> Optional[Currency]:
        """Find a currency by its ISO code.

        Args:
            code: The ISO 4217 currency code.

        Returns:
            The currency if found, None otherwise.
        """
        code = code.upper()
        query = select(Currency).where(
            Currency.code == code, Currency.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_base_currency(self) -> Optional[Currency]:
        """Get the base currency of the system.

        Returns:
            The base currency if found, None otherwise.
        """
        query = select(Currency).where(
            Currency.is_base == True,
            Currency.is_active == True,
            Currency.is_deleted == False,
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_active_currencies(self) -> List[Currency]:
        """Get all active currencies.

        Returns:
            List of active currencies sorted by code.
        """
        query = (
            select(Currency)
            .where(Currency.is_active == True, Currency.is_deleted == False)
            .order_by(Currency.code)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def set_as_base(self, currency_id: uuid.UUID) -> Currency:
        """Set a currency as the base currency.

        This will unset any existing base currency.

        Args:
            currency_id: The ID of the currency to set as base.

        Returns:
            The updated currency.

        Raises:
            ResourceNotFoundException: If the currency is not found.
            BusinessException: If the currency is not active.
        """
        # First ensure the currency exists and is active
        currency = await self.get_by_id(currency_id)
        if not currency:
            raise ResourceNotFoundException(
                resource_type="Currency", resource_id=str(currency_id)
            )

        if not currency.is_active:
            raise BusinessException(
                message="Cannot set inactive currency as base currency",
                details={"currency_id": str(currency_id)},
            )

        # Unset any existing base currency
        current_base = await self.get_base_currency()
        if current_base and current_base.id != currency_id:
            current_base.is_base = False
            self.db.add(current_base)

        # Set the new base currency
        currency.is_base = True
        self.db.add(currency)
        await self.db.flush()
        await self.db.refresh(currency)

        return currency

    async def ensure_exists(self, currency_id: uuid.UUID) -> Currency:
        """Ensure a currency exists by ID, raising an exception if not found.

        Args:
            currency_id: The currency ID to check.

        Returns:
            The currency if found.

        Raises:
            ResourceNotFoundException: If the currency is not found.
        """
        currency = await self.get_by_id(currency_id)
        if not currency:
            raise ResourceNotFoundException(
                resource_type="Currency", resource_id=str(currency_id)
            )
        return currency


class ExchangeRateRepository(BaseRepository[ExchangeRate, uuid.UUID]):
    """Repository for ExchangeRate entity operations.

    Provides methods for querying, creating, updating, and deleting
    ExchangeRate entities, extending the generic BaseRepository.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the exchange rate repository.

        Args:
            db: The database session.
        """
        super().__init__(model=ExchangeRate, db=db)

    async def find_latest_rate(
        self, source_currency_id: uuid.UUID, target_currency_id: uuid.UUID
    ) -> Optional[ExchangeRate]:
        """Find the latest exchange rate between two currencies.

        Args:
            source_currency_id: The source currency ID.
            target_currency_id: The target currency ID.

        Returns:
            The latest exchange rate if found, None otherwise.
        """
        query = (
            select(ExchangeRate)
            .where(
                ExchangeRate.source_currency_id == source_currency_id,
                ExchangeRate.target_currency_id == target_currency_id,
                ExchangeRate.is_deleted == False,
            )
            .order_by(desc(ExchangeRate.effective_date))
            .limit(1)
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_rate_at_date(
        self,
        source_currency_id: uuid.UUID,
        target_currency_id: uuid.UUID,
        date: datetime,
    ) -> Optional[ExchangeRate]:
        """Find the exchange rate between two currencies at a specific date.

        Args:
            source_currency_id: The source currency ID.
            target_currency_id: The target currency ID.
            date: The date to find the rate for.

        Returns:
            The exchange rate if found, None otherwise.
        """
        query = (
            select(ExchangeRate)
            .where(
                ExchangeRate.source_currency_id == source_currency_id,
                ExchangeRate.target_currency_id == target_currency_id,
                ExchangeRate.effective_date <= date,
                ExchangeRate.is_deleted == False,
            )
            .order_by(desc(ExchangeRate.effective_date))
            .limit(1)
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def convert(
        self, source_currency_code: str, target_currency_code: str, amount: float
    ) -> Tuple[float, float, datetime]:
        """Convert an amount between two currencies using the latest exchange rate.

        Args:
            source_currency_code: The source currency code.
            target_currency_code: The target currency code.
            amount: The amount to convert.

        Returns:
            Tuple containing (converted amount, exchange rate, timestamp).

        Raises:
            ResourceNotFoundException: If either currency is not found.
            BusinessException: If no exchange rate is found.
        """
        # Look up the currencies
        currency_repo = CurrencyRepository(self.db)
        source_currency = await currency_repo.find_by_code(source_currency_code)
        target_currency = await currency_repo.find_by_code(target_currency_code)

        if not source_currency:
            raise ResourceNotFoundException(
                resource_type="Currency", resource_id=source_currency_code
            )

        if not target_currency:
            raise ResourceNotFoundException(
                resource_type="Currency", resource_id=target_currency_code
            )

        # If same currency, no conversion needed
        if source_currency.id == target_currency.id:
            return amount, 1.0, datetime.now()

        # Find the latest exchange rate
        rate = await self.find_latest_rate(source_currency.id, target_currency.id)

        if not rate:
            # Try inverse rate if direct rate not available
            inverse_rate = await self.find_latest_rate(
                target_currency.id, source_currency.id
            )

            if inverse_rate:
                rate_value = 1.0 / inverse_rate.rate
                return amount * rate_value, rate_value, inverse_rate.effective_date

            # Try triangulation through base currency
            base_currency = await currency_repo.get_base_currency()
            if not base_currency:
                raise BusinessException(
                    message="No base currency defined for triangulation"
                )

            if source_currency.id == base_currency.id:
                # From base to target
                to_target = await self.find_latest_rate(
                    base_currency.id, target_currency.id
                )

                if not to_target:
                    raise BusinessException(
                        message=f"No exchange rate found between {source_currency_code} and {target_currency_code}"
                    )

                return amount * to_target.rate, to_target.rate, to_target.effective_date

            if target_currency.id == base_currency.id:
                # From source to base
                from_source = await self.find_latest_rate(
                    source_currency.id, base_currency.id
                )

                if not from_source:
                    raise BusinessException(
                        message=f"No exchange rate found between {source_currency_code} and {target_currency_code}"
                    )

                return (
                    amount * from_source.rate,
                    from_source.rate,
                    from_source.effective_date,
                )

            # Try source -> base -> target
            from_source = await self.find_latest_rate(
                source_currency.id, base_currency.id
            )

            to_target = await self.find_latest_rate(
                base_currency.id, target_currency.id
            )

            if not from_source or not to_target:
                raise BusinessException(
                    message=f"No exchange rate found between {source_currency_code} and {target_currency_code}"
                )

            # Triangulate the rate
            rate_value = from_source.rate * to_target.rate
            timestamp = max(from_source.effective_date, to_target.effective_date)

            return amount * rate_value, rate_value, timestamp

        return amount * rate.rate, rate.rate, rate.effective_date
