from __future__ import annotations
'Currency repository implementation.\n\nThis module provides data access and persistence operations for Currency entities.\n'
import uuid
from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.currency.models import Currency, ExchangeRate
from app.repositories.base import BaseRepository
from app.core.exceptions import ResourceNotFoundException, BusinessException
class CurrencyRepository(BaseRepository[Currency, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=Currency, db=db)
    async def find_by_code(self, code: str) -> Optional[Currency]:
        code = code.upper()
        query = select(Currency).where(Currency.code == code, Currency.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_base_currency(self) -> Optional[Currency]:
        query = select(Currency).where(Currency.is_base == True, Currency.is_active == True, Currency.is_deleted == False)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def get_active_currencies(self) -> List[Currency]:
        query = select(Currency).where(Currency.is_active == True, Currency.is_deleted == False).order_by(Currency.code)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    async def set_as_base(self, currency_id: uuid.UUID) -> Currency:
        currency = await self.get_by_id(currency_id)
        if not currency:
            raise ResourceNotFoundException(resource_type='Currency', resource_id=str(currency_id))
        if not currency.is_active:
            raise BusinessException(message='Cannot set inactive currency as base currency', details={'currency_id': str(currency_id)})
        current_base = await self.get_base_currency()
        if current_base and current_base.id != currency_id:
            current_base.is_base = False
            self.db.add(current_base)
        currency.is_base = True
        self.db.add(currency)
        await self.db.flush()
        await self.db.refresh(currency)
        return currency
    async def ensure_exists(self, currency_id: uuid.UUID) -> Currency:
        currency = await self.get_by_id(currency_id)
        if not currency:
            raise ResourceNotFoundException(resource_type='Currency', resource_id=str(currency_id))
        return currency
class ExchangeRateRepository(BaseRepository[ExchangeRate, uuid.UUID]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(model=ExchangeRate, db=db)
    async def find_latest_rate(self, source_currency_id: uuid.UUID, target_currency_id: uuid.UUID) -> Optional[ExchangeRate]:
        query = select(ExchangeRate).where(ExchangeRate.source_currency_id == source_currency_id, ExchangeRate.target_currency_id == target_currency_id, ExchangeRate.is_deleted == False).order_by(desc(ExchangeRate.effective_date)).limit(1)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def find_rate_at_date(self, source_currency_id: uuid.UUID, target_currency_id: uuid.UUID, date: datetime) -> Optional[ExchangeRate]:
        query = select(ExchangeRate).where(ExchangeRate.source_currency_id == source_currency_id, ExchangeRate.target_currency_id == target_currency_id, ExchangeRate.effective_date <= date, ExchangeRate.is_deleted == False).order_by(desc(ExchangeRate.effective_date)).limit(1)
        result = await self.db.execute(query)
        return result.scalars().first()
    async def convert(self, source_currency_code: str, target_currency_code: str, amount: float) -> Tuple[float, float, datetime]:
        currency_repo = CurrencyRepository(self.db)
        source_currency = await currency_repo.find_by_code(source_currency_code)
        target_currency = await currency_repo.find_by_code(target_currency_code)
        if not source_currency:
            raise ResourceNotFoundException(resource_type='Currency', resource_id=source_currency_code)
        if not target_currency:
            raise ResourceNotFoundException(resource_type='Currency', resource_id=target_currency_code)
        if source_currency.id == target_currency.id:
            return (amount, 1.0, datetime.now())
        rate = await self.find_latest_rate(source_currency.id, target_currency.id)
        if not rate:
            inverse_rate = await self.find_latest_rate(target_currency.id, source_currency.id)
            if inverse_rate:
                rate_value = 1.0 / inverse_rate.rate
                return (amount * rate_value, rate_value, inverse_rate.effective_date)
            base_currency = await currency_repo.get_base_currency()
            if not base_currency:
                raise BusinessException(message='No base currency defined for triangulation')
            if source_currency.id == base_currency.id:
                to_target = await self.find_latest_rate(base_currency.id, target_currency.id)
                if not to_target:
                    raise BusinessException(message=f'No exchange rate found between {source_currency_code} and {target_currency_code}')
                return (amount * to_target.rate, to_target.rate, to_target.effective_date)
            if target_currency.id == base_currency.id:
                from_source = await self.find_latest_rate(source_currency.id, base_currency.id)
                if not from_source:
                    raise BusinessException(message=f'No exchange rate found between {source_currency_code} and {target_currency_code}')
                return (amount * from_source.rate, from_source.rate, from_source.effective_date)
            from_source = await self.find_latest_rate(source_currency.id, base_currency.id)
            to_target = await self.find_latest_rate(base_currency.id, target_currency.id)
            if not from_source or not to_target:
                raise BusinessException(message=f'No exchange rate found between {source_currency_code} and {target_currency_code}')
            rate_value = from_source.rate * to_target.rate
            timestamp = max(from_source.effective_date, to_target.effective_date)
            return (amount * rate_value, rate_value, timestamp)
        return (amount * rate.rate, rate.rate, rate.effective_date)