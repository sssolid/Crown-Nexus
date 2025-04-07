# app/domains/autocare/commands/__init__.py
from __future__ import annotations

"""
Command-line interface commands for AutoCare data management.

This package provides CLI commands for importing, exporting, and
managing AutoCare standard database data.
"""

from app.domains.autocare.commands.import_autocare import app as import_app

__all__ = ["import_app"]
