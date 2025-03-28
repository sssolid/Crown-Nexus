# backend/app/tasks/tasks.py
"""
Celery tasks for currency operations.

This module defines Celery tasks for:
- Fetching and updating exchange rates
- Monitoring API usage
- Handling currency-related background operations
"""

from __future__ import annotations

from typing import Dict, Optional

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from sqlalchemy.exc import SQLAlchemyError

from app.logging import get_logger
from app.db.session import get_db_context
from app.domains.currency.service import ExchangeRateService

logger = get_logger("app.tasks.currency_tasks")


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
    autoretry_for=(Exception,),
    retry_backoff=True,
)
def update_exchange_rates(self) -> Dict[str, Optional[int]]:
    """
    Update exchange rates from the API.

    Returns:
        Dict[str, Optional[int]]: Result of the operation
    """
    try:
        # Create context for database operations
        async def _update_rates():
            async with get_db_context() as db:
                count = await ExchangeRateService.update_exchange_rates(db)
                return count

        # Use asyncio.run in a synchronous task
        import asyncio

        count = asyncio.run(_update_rates())

        return {"status": "success", "updated_count": count}
    except SQLAlchemyError as e:
        logger.error(f"Database error during exchange rate update: {str(e)}")
        raise self.retry(exc=e)
    except Exception as e:
        logger.error(f"Error updating exchange rates: {str(e)}")
        raise self.retry(exc=e)


@shared_task
def init_currencies() -> Dict[str, Optional[int]]:
    """
    Initialize currencies in the database.

    Returns:
        Dict[str, Optional[int]]: Result of the operation
    """
    # Common currencies to initialize
    currencies = [
        {"code": "USD", "name": "US Dollar", "symbol": "$", "is_base": True},
        {"code": "EUR", "name": "Euro", "symbol": "€", "is_base": False},
        {"code": "GBP", "name": "British Pound", "symbol": "£", "is_base": False},
        {"code": "JPY", "name": "Japanese Yen", "symbol": "¥", "is_base": False},
        {"code": "CAD", "name": "Canadian Dollar", "symbol": "C$", "is_base": False},
        {"code": "AUD", "name": "Australian Dollar", "symbol": "A$", "is_base": False},
        {"code": "CHF", "name": "Swiss Franc", "symbol": "CHF", "is_base": False},
        {"code": "CNY", "name": "Chinese Yuan", "symbol": "¥", "is_base": False},
    ]

    async def _init_currencies():
        from app.domains.currency.models import Currency
        from sqlalchemy import select

        async with get_db_context() as db:
            # Check existing currencies
            stmt = select(Currency.code)
            result = await db.execute(stmt)
            existing_codes = {code for code, in result}

            # Add missing currencies
            count = 0
            for currency_data in currencies:
                if currency_data["code"] not in existing_codes:
                    currency = Currency(**currency_data)
                    db.add(currency)
                    count += 1

            if count > 0:
                await db.commit()

            return count

    try:
        import asyncio

        count = asyncio.run(_init_currencies())
        return {"status": "success", "added_count": count}
    except Exception as e:
        logger.error(f"Error initializing currencies: {str(e)}")
        return {"status": "error", "message": str(e)}
