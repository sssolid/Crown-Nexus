from __future__ import annotations
'\nCommand-line interface commands for AutoCare data management.\n\nThis package provides CLI commands for importing, exporting, and\nmanaging AutoCare standard database data.\n'
from app.domains.autocare.commands.import_autocare import app as import_app
__all__ = ['import_app']