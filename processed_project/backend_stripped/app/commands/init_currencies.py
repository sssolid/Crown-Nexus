import asyncio
import typer
from sqlalchemy import select
from app.db.session import get_db_context
from app.domains.currency.models import Currency
from app.domains.currency.tasks import init_currencies as init_currencies_task
app = typer.Typer()
@app.command()
def init_currencies(force: bool=typer.Option(False, '--force', '-f', help='Force re-initialization even if currencies exist'), sync: bool=typer.Option(True, '--sync', help='Run synchronously instead of using Celery'), base_currency: str=typer.Option('USD', '--base', '-b', help='Set base currency code')):
    if sync:
        typer.echo('Initializing currencies synchronously...')
        asyncio.run(_init_currencies_sync(force, base_currency))
    else:
        typer.echo('Triggering currency initialization task...')
        task = init_currencies_task.delay()
        typer.echo(f'Task ID: {task.id}')
async def _init_currencies_sync(force: bool, base_currency: str) -> None:
    currencies = [{'code': 'USD', 'name': 'US Dollar', 'symbol': '$'}, {'code': 'EUR', 'name': 'Euro', 'symbol': '€'}, {'code': 'GBP', 'name': 'British Pound', 'symbol': '£'}, {'code': 'JPY', 'name': 'Japanese Yen', 'symbol': '¥'}, {'code': 'CAD', 'name': 'Canadian Dollar', 'symbol': 'C$'}, {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': 'A$'}, {'code': 'CHF', 'name': 'Swiss Franc', 'symbol': 'CHF'}, {'code': 'CNY', 'name': 'Chinese Yuan', 'symbol': '¥'}]
    for currency in currencies:
        currency['is_base'] = currency['code'] == base_currency
    async with get_db_context() as db:
        if not force:
            stmt = select(Currency)
            result = await db.execute(stmt)
            existing = list(result.scalars().all())
            if existing:
                typer.echo(f'Found {len(existing)} existing currencies. Use --force to reinitialize.')
                return
        if force:
            await db.execute('DELETE FROM exchange_rate')
            await db.execute('DELETE FROM currency')
            await db.commit()
        for currency_data in currencies:
            currency = Currency(**currency_data)
            db.add(currency)
        await db.commit()
        typer.echo(f'Added {len(currencies)} currencies to the database.')
        from app.domains.currency.service import ExchangeRateService
        try:
            count = await ExchangeRateService.update_exchange_rates(db, force=True)
            typer.echo(f'Updated {count} exchange rates.')
        except Exception as e:
            typer.echo(f'Failed to update exchange rates: {str(e)}', err=True)
if __name__ == '__main__':
    app()