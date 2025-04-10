from __future__ import annotations
import datetime
from typing import Dict, Optional
import httpx
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.cache.decorators import cached
from app.core.config import settings
from app.logging import get_logger
from app.domains.currency.models import Currency, ExchangeRate
logger = get_logger('app.services.currency_service')
class ExchangeRateService:
    API_URL = 'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
    DATA_SOURCE = 'exchangerate-api.com'
    @classmethod
    async def fetch_latest_rates(cls, db: AsyncSession, base_currency: str='USD') -> Dict[str, float]:
        api_key = settings.EXCHANGE_RATE_API_KEY
        if not api_key:
            raise ValueError('Exchange rate API key is not configured')
        url = cls.API_URL.format(api_key=api_key, base_currency=base_currency)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        if data.get('result') != 'success':
            error_msg = data.get('error', 'Unknown error')
            raise ValueError(f'API error: {error_msg}')
        rates = data.get('conversion_rates', {})
        if not rates:
            raise ValueError('No exchange rates found in API response')
        return rates
    @classmethod
    async def update_exchange_rates(cls, db: AsyncSession, force: bool=False) -> int:
        if not force and (not await cls._is_update_due(db)):
            logger.info('Exchange rate update not due yet, skipping')
            return 0
        base_currency = await cls._get_base_currency_code(db)
        try:
            rates = await cls.fetch_latest_rates(db, base_currency)
        except (ValueError, httpx.RequestError) as e:
            logger.error(f'Failed to fetch exchange rates: {str(e)}')
            raise
        stmt = select(Currency).where(Currency.is_active == True)
        result = await db.execute(stmt)
        currencies = {c.code: c for c in result.scalars().all()}
        base_currency_id = currencies.get(base_currency)
        if not base_currency_id:
            raise ValueError(f'Base currency {base_currency} not found in database')
        base_currency_id = base_currency_id.id
        now = datetime.datetime.now(datetime.UTC)
        count = 0
        for currency_code, rate in rates.items():
            if currency_code not in currencies:
                continue
            if currency_code == base_currency:
                continue
            target_currency_id = currencies[currency_code].id
            exchange_rate = ExchangeRate(source_currency_id=base_currency_id, target_currency_id=target_currency_id, rate=rate, effective_date=now, fetched_at=now, data_source=cls.DATA_SOURCE)
            db.add(exchange_rate)
            count += 1
        if settings.STORE_INVERSE_RATES:
            for currency_code, rate in rates.items():
                if currency_code not in currencies:
                    continue
                if currency_code == base_currency:
                    continue
                target_currency_id = currencies[currency_code].id
                inverse_rate = ExchangeRate(source_currency_id=target_currency_id, target_currency_id=base_currency_id, rate=1.0 / rate, effective_date=now, fetched_at=now, data_source=cls.DATA_SOURCE)
                db.add(inverse_rate)
                count += 1
        await db.commit()
        logger.info(f'Updated {count} exchange rates')
        return count
    @classmethod
    async def _is_update_due(cls, db: AsyncSession) -> bool:
        update_frequency = settings.EXCHANGE_RATE_UPDATE_FREQUENCY
        stmt = select(ExchangeRate).order_by(desc(ExchangeRate.fetched_at)).limit(1)
        result = await db.execute(stmt)
        latest_rate = result.scalar_one_or_none()
        if not latest_rate:
            return True
        time_since_update = datetime.datetime.now(datetime.UTC) - latest_rate.fetched_at
        return time_since_update > datetime.timedelta(hours=update_frequency)
    @classmethod
    async def _get_base_currency_code(cls, db: AsyncSession) -> str:
        stmt = select(Currency).where(Currency.is_base == True)
        result = await db.execute(stmt)
        base_currency = result.scalar_one_or_none()
        if base_currency:
            return base_currency.code
        return 'USD'
    @classmethod
    @cached(prefix='currency', ttl=3600, backend='redis')
    async def get_latest_exchange_rate(cls, db: AsyncSession, source_code: str, target_code: str) -> Optional[float]:
        stmt = select(Currency).where(Currency.code.in_([source_code, target_code]))
        result = await db.execute(stmt)
        currencies = {c.code: c.id for c in result.scalars().all()}
        if source_code not in currencies or target_code not in currencies:
            return None
        stmt = select(ExchangeRate).where(ExchangeRate.source_currency_id == currencies[source_code], ExchangeRate.target_currency_id == currencies[target_code]).order_by(desc(ExchangeRate.effective_date)).limit(1)
        result = await db.execute(stmt)
        rate = result.scalar_one_or_none()
        if rate:
            return rate.rate
        stmt = select(ExchangeRate).where(ExchangeRate.source_currency_id == currencies[target_code], ExchangeRate.target_currency_id == currencies[source_code]).order_by(desc(ExchangeRate.effective_date)).limit(1)
        result = await db.execute(stmt)
        inverse_rate = result.scalar_one_or_none()
        if inverse_rate and inverse_rate.rate != 0:
            return 1.0 / inverse_rate.rate
        return None
    @classmethod
    async def convert_amount(cls, db: AsyncSession, amount: float, source_code: str, target_code: str) -> Optional[float]:
        if source_code == target_code:
            return amount
        rate = await cls.get_latest_exchange_rate(db, source_code, target_code)
        if rate is None:
            return None
        return amount * rate