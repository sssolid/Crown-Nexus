# app/data_import/commands/__init__.py
from __future__ import annotations

"""
CLI commands for data import.

This package provides CLI commands for importing data from external sources
into the application database.
"""

import typer

from app.data_import.commands.import_products import app as import_products_app

app = typer.Typer()
app.add_typer(import_products_app, name="products", help="Import product data")

__all__ = ["app"]
