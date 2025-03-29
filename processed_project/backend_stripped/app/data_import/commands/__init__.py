from __future__ import annotations
'\nCLI commands for data import.\n\nThis package provides CLI commands for importing data from external sources\ninto the application database.\n'
import typer
from app.data_import.commands.import_products import app as import_products_app
app = typer.Typer()
app.add_typer(import_products_app, name='products', help='Import product data')
__all__ = ['app']