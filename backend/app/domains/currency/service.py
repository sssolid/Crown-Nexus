# backend/app/services/service.py
"""
Currency service for fetching and managing exchange rates.

This module provides service functions for:
- Fetching exchange rates from external APIs
- Storing rates in the database
- Converting between currencies
- Managing the rate update schedule
"""

from __future__ import annotations

import datetime
from typing import Dict, Optional

import httpx
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache.decorators import cached
from app.core.config import settings
from app.domains.currency.models import Currency, ExchangeRate

from app.core.logging import get_logger

logger = get_logger("app.services.currency_service")


class ExchangeRateService:
    """Service for fetching and managing currency exchange rates."""

    API_URL = "https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    DATA_SOURCE = "exchangerate-api.com"

    @classmethod
    async def fetch_latest_rates(
        cls, db: AsyncSession, base_currency: str = "USD"
    ) -> Dict[str, float]:
        """
        Fetch the latest exchange rates from the API.

        Args:
            db: Database session
            base_currency: Base currency code (default: USD)

        Returns:
            Dict[str, float]: Dictionary of currency codes to rates

        Raises:
            ValueError: If API key is missing or invalid
            httpx.RequestError: If request fails
            httpx.HTTPStatusError: If API returns error status
        """
        # Validate API key
        api_key = settings.EXCHANGE_RATE_API_KEY
        if not api_key:
            raise ValueError("Exchange rate API key is not configured")

        # Format URL
        url = cls.API_URL.format(api_key=api_key, base_currency=base_currency)

        # Fetch data from API
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()

        # Check API response
        if data.get("result") != "success":
            error_msg = data.get("error", "Unknown error")
            raise ValueError(f"API error: {error_msg}")

        # Extract rates
        rates = data.get("conversion_rates", {})
        if not rates:
            raise ValueError("No exchange rates found in API response")

        return rates

    @classmethod
    async def update_exchange_rates(cls, db: AsyncSession, force: bool = False) -> int:
        """
        Update exchange rates in the database.

        Args:
            db: Database session
            force: Force update even if not due yet

        Returns:
            int: Number of rates updated

        Raises:
            ValueError: If API returns invalid data
            SQLAlchemyError: If database operations fail
        """
        # Check if update is needed
        if not force and not await cls._is_update_due(db):
            logger.info("Exchange rate update not due yet, skipping")
            return 0

        # Get base currency from database, default to USD if not found
        base_currency = await cls._get_base_currency_code(db)

        # Fetch latest rates
        try:
            rates = await cls.fetch_latest_rates(db, base_currency)
        except (ValueError, httpx.RequestError) as e:
            logger.error(f"Failed to fetch exchange rates: {str(e)}")
            raise

        # Get currency records from database
        stmt = select(Currency).where(Currency.is_active == True)
        result = await db.execute(stmt)
        currencies = {c.code: c for c in result.scalars().all()}

        # Get base currency ID
        base_currency_id = currencies.get(base_currency)
        if not base_currency_id:
            raise ValueError(f"Base currency {base_currency} not found in database")
        base_currency_id = base_currency_id.id

        # Prepare rate records
        now = datetime.datetime.now(datetime.UTC)
        count = 0

        # Insert new rates
        for currency_code, rate in rates.items():
            # Skip if currency not in our database
            if currency_code not in currencies:
                continue

            # Skip base currency (rate is always 1)
            if currency_code == base_currency:
                continue

            target_currency_id = currencies[currency_code].id

            # Create new exchange rate record
            exchange_rate = ExchangeRate(
                source_currency_id=base_currency_id,
                target_currency_id=target_currency_id,
                rate=rate,
                effective_date=now,
                fetched_at=now,
                data_source=cls.DATA_SOURCE,
            )

            db.add(exchange_rate)
            count += 1

        # Create inverse rates if needed
        if settings.STORE_INVERSE_RATES:
            for currency_code, rate in rates.items():
                # Skip if currency not in our database
                if currency_code not in currencies:
                    continue

                # Skip base currency (rate is always 1)
                if currency_code == base_currency:
                    continue

                target_currency_id = currencies[currency_code].id

                # Create inverse rate record (1/rate)
                inverse_rate = ExchangeRate(
                    source_currency_id=target_currency_id,
                    target_currency_id=base_currency_id,
                    rate=1.0 / rate,
                    effective_date=now,
                    fetched_at=now,
                    data_source=cls.DATA_SOURCE,
                )

                db.add(inverse_rate)
                count += 1

        # Commit changes
        await db.commit()
        logger.info(f"Updated {count} exchange rates")

        return count

    @classmethod
    async def _is_update_due(cls, db: AsyncSession) -> bool:
        """
        Check if an update is due based on the last update time.

        Args:
            db: Database session

        Returns:
            bool: True if update is due, False otherwise
        """
        # Get update frequency from settings (in hours)
        update_frequency = settings.EXCHANGE_RATE_UPDATE_FREQUENCY

        # Get the most recent exchange rate
        stmt = select(ExchangeRate).order_by(desc(ExchangeRate.fetched_at)).limit(1)
        result = await db.execute(stmt)
        latest_rate = result.scalar_one_or_none()

        # If no rates exist, update is due
        if not latest_rate:
            return True

        # Check if enough time has passed since last update
        time_since_update = datetime.datetime.now(datetime.UTC) - latest_rate.fetched_at
        return time_since_update > datetime.timedelta(hours=update_frequency)

    @classmethod
    async def _get_base_currency_code(cls, db: AsyncSession) -> str:
        """
        Get the base currency code from the database.

        Args:
            db: Database session

        Returns:
            str: Base currency code (defaults to USD if not found)
        """
        # Try to find currency marked as base
        stmt = select(Currency).where(Currency.is_base == True)
        result = await db.execute(stmt)
        base_currency = result.scalar_one_or_none()

        if base_currency:
            return base_currency.code

        # Default to USD if no base currency is set
        return "USD"

    @classmethod
    @cached(prefix="currency", ttl=3600, backend="redis")  # Cache for 1 hour
    async def get_latest_exchange_rate(
        cls, db: AsyncSession, source_code: str, target_code: str
    ) -> Optional[float]:
        """
        Get the latest exchange rate between two currencies.

        Args:
            db: Database session
            source_code: Source currency code
            target_code: Target currency code

        Returns:
            Optional[float]: Exchange rate or None if not found
        """
        # Get currency IDs
        stmt = select(Currency).where(Currency.code.in_([source_code, target_code]))
        result = await db.execute(stmt)
        currencies = {c.code: c.id for c in result.scalars().all()}

        # Check if both currencies exist
        if source_code not in currencies or target_code not in currencies:
            return None

        # Get the latest exchange rate
        stmt = (
            select(ExchangeRate)
            .where(
                ExchangeRate.source_currency_id == currencies[source_code],
                ExchangeRate.target_currency_id == currencies[target_code],
            )
            .order_by(desc(ExchangeRate.effective_date))
            .limit(1)
        )

        result = await db.execute(stmt)
        rate = result.scalar_one_or_none()

        if rate:
            return rate.rate

        # Try to find inverse rate and calculate
        stmt = (
            select(ExchangeRate)
            .where(
                ExchangeRate.source_currency_id == currencies[target_code],
                ExchangeRate.target_currency_id == currencies[source_code],
            )
            .order_by(desc(ExchangeRate.effective_date))
            .limit(1)
        )

        result = await db.execute(stmt)
        inverse_rate = result.scalar_one_or_none()

        if inverse_rate and inverse_rate.rate != 0:
            return 1.0 / inverse_rate.rate

        return None

    @classmethod
    async def convert_amount(
        cls, db: AsyncSession, amount: float, source_code: str, target_code: str
    ) -> Optional[float]:
        """
        Convert an amount from one currency to another.

        Args:
            db: Database session
            amount: Amount to convert
            source_code: Source currency code
            target_code: Target currency code

        Returns:
            Optional[float]: Converted amount or None if rate not found
        """
        # Same currency, no conversion needed
        if source_code == target_code:
            return amount

        # Get the latest exchange rate
        rate = await cls.get_latest_exchange_rate(db, source_code, target_code)

        if rate is None:
            return None

        # Perform conversion
        return amount * rate
