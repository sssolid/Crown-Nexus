# backend/app/commands/init_currencies.py
"""
Command to initialize currencies in the database.

This command populates the currency table with common currencies
and can be run manually or during application setup.
"""

import asyncio
import typer

from sqlalchemy import select

from app.db.session import get_db_context
from app.domains.currency.models import Currency
from app.domains.currency.tasks import init_currencies as init_currencies_task

app = typer.Typer()


@app.command()
def init_currencies(
    force: bool = typer.Option(
        False, "--force", "-f", help="Force re-initialization even if currencies exist"
    ),
    sync: bool = typer.Option(
        True, "--sync", help="Run synchronously instead of using Celery"
    ),
    base_currency: str = typer.Option(
        "USD", "--base", "-b", help="Set base currency code"
    ),
):
    """Initialize currencies in the database."""
    if sync:
        # Run synchronously
        typer.echo("Initializing currencies synchronously...")
        asyncio.run(_init_currencies_sync(force, base_currency))
    else:
        # Use Celery task
        typer.echo("Triggering currency initialization task...")
        task = init_currencies_task.delay()
        typer.echo(f"Task ID: {task.id}")


async def _init_currencies_sync(force: bool, base_currency: str) -> None:
    """Initialize currencies synchronously."""
    # Common currencies
    currencies = [
        {"code": "USD", "name": "US Dollar", "symbol": "$"},
        {"code": "EUR", "name": "Euro", "symbol": "€"},
        {"code": "GBP", "name": "British Pound", "symbol": "£"},
        {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
        {"code": "CAD", "name": "Canadian Dollar", "symbol": "C$"},
        {"code": "AUD", "name": "Australian Dollar", "symbol": "A$"},
        {"code": "CHF", "name": "Swiss Franc", "symbol": "CHF"},
        {"code": "CNY", "name": "Chinese Yuan", "symbol": "¥"},
    ]

    # Mark the base currency
    for currency in currencies:
        currency["is_base"] = currency["code"] == base_currency

    async with get_db_context() as db:
        # Check for existing currencies if not forcing
        if not force:
            stmt = select(Currency)
            result = await db.execute(stmt)
            existing = list(result.scalars().all())

            if existing:
                typer.echo(
                    f"Found {len(existing)} existing currencies. Use --force to reinitialize."
                )
                return

        # Delete existing currencies if forcing
        if force:
            # Delete all exchange rates first (foreign key constraint)
            await db.execute("DELETE FROM exchange_rate")
            # Delete currencies
            await db.execute("DELETE FROM currency")
            await db.commit()

        # Add currencies
        for currency_data in currencies:
            currency = Currency(**currency_data)
            db.add(currency)

        await db.commit()
        typer.echo(f"Added {len(currencies)} currencies to the database.")

        # Trigger initial exchange rate update
        from app.domains.currency.service import ExchangeRateService

        try:
            count = await ExchangeRateService.update_exchange_rates(db, force=True)
            typer.echo(f"Updated {count} exchange rates.")
        except Exception as e:
            typer.echo(f"Failed to update exchange rates: {str(e)}", err=True)


if __name__ == "__main__":
    app()
