# backend/app/api/v1/endpoints/currency.py
"""
Currency API endpoints.

This module provides API endpoints for:
- Retrieving currency information
- Getting exchange rates
- Converting between currencies
- Managing currency settings
"""

from __future__ import annotations

import datetime
from typing import Annotated, Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_admin_user, get_current_active_user, get_db
from app.models.currency import Currency, ExchangeRate
from app.models.user import User
from app.schemas.currency import (
    ConversionRequest,
    ConversionResponse,
    CurrencyCreate,
    CurrencyRead,
    CurrencyUpdate,
    ExchangeRateRead,
)
from app.services.currency_service import ExchangeRateService
from app.tasks.currency_tasks import update_exchange_rates

router = APIRouter()


@router.get("/", response_model=List[CurrencyRead])
async def read_currencies(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    active_only: bool = True,
) -> Any:
    """
    Get list of available currencies.

    Args:
        db: Database session
        current_user: Current authenticated user
        active_only: Whether to return only active currencies (default: True)

    Returns:
        List[CurrencyRead]: List of currencies
    """
    query = select(Currency)

    if active_only:
        query = query.where(Currency.is_active == True)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/rates", response_model=List[ExchangeRateRead])
async def read_exchange_rates(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    source_code: Optional[str] = None,
    target_code: Optional[str] = None,
    limit: int = 10,
) -> Any:
    """
    Get exchange rates with optional filtering.

    Args:
        db: Database session
        current_user: Current authenticated user
        source_code: Source currency code
        target_code: Target currency code
        limit: Maximum number of rates to return (default: 10)

    Returns:
        List[ExchangeRateRead]: List of exchange rates
    """
    # Build query
    query = (
        select(ExchangeRate)
        .join(Currency, ExchangeRate.source_currency_id == Currency.id)
        .join(Currency, ExchangeRate.target_currency_id == Currency.id)
        .order_by(desc(ExchangeRate.effective_date))
    )

    # Apply filters
    if source_code:
        subquery = select(Currency.id).where(Currency.code == source_code)
        query = query.where(ExchangeRate.source_currency_id.in_(subquery))

    if target_code:
        subquery = select(Currency.id).where(Currency.code == target_code)
        query = query.where(ExchangeRate.target_currency_id.in_(subquery))

    # Apply limit
    query = query.limit(limit)

    # Execute query
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/convert", response_model=ConversionResponse)
async def convert_currency(
    conversion: ConversionRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Any:
    """
    Convert an amount between currencies.

    Args:
        conversion: Conversion request parameters
        db: Database session
        current_user: Current authenticated user

    Returns:
        ConversionResponse: Conversion result

    Raises:
        HTTPException: If currencies not found or conversion fails
    """
    # Check if currencies exist
    query = select(Currency).where(
        Currency.code.in_([conversion.source_currency, conversion.target_currency])
    )
    result = await db.execute(query)
    found_currencies = result.scalars().all()

    if len(found_currencies) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or both specified currencies not found",
        )

    # Perform conversion
    converted_amount = await ExchangeRateService.convert_amount(
        db, conversion.amount, conversion.source_currency, conversion.target_currency
    )

    if converted_amount is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exchange rate not found for specified currencies",
        )

    # Get rate for reference
    rate = await ExchangeRateService.get_latest_exchange_rate(
        db, conversion.source_currency, conversion.target_currency
    )

    # Return response
    return {
        "source_currency": conversion.source_currency,
        "target_currency": conversion.target_currency,
        "source_amount": conversion.amount,
        "converted_amount": converted_amount,
        "exchange_rate": rate,
        "timestamp": datetime.datetime.now(datetime.UTC),
    }


@router.post("/update", status_code=status.HTTP_202_ACCEPTED)
async def trigger_exchange_rate_update(
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
    async_update: bool = Query(
        True, description="Whether to update rates asynchronously"
    ),
) -> Dict[str, Any]:
    """
    Trigger an update of exchange rates.

    Args:
        background_tasks: Background tasks
        db: Database session
        current_user: Current authenticated admin user
        async_update: Whether to update asynchronously or wait for completion

    Returns:
        Dict[str, Any]: Result of the operation

    Raises:
        HTTPException: If update fails
    """
    if async_update:
        # Trigger Celery task
        task = update_exchange_rates.delay()
        return {
            "message": "Exchange rate update triggered",
            "task_id": task.id,
        }
    else:
        try:
            # Run update synchronously
            count = await ExchangeRateService.update_exchange_rates(db, force=True)
            return {
                "message": "Exchange rates updated successfully",
                "updated_count": count,
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update exchange rates: {str(e)}",
            )
