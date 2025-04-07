# app/cli/autocare.py
from __future__ import annotations

"""
Command-line interface for AutoCare data management.

This module provides the main CLI for AutoCare data management,
including import, export, and database operations.
"""

import sys
import typer
from typing import List, Optional

# Import directly instead of adding the app
from app.domains.autocare.commands.import_autocare import import_autocare

app = typer.Typer(help="Manage AutoCare standard data (VCdb, PCdb, PAdb, Qdb)")

# Register the command directly to avoid subcommand nesting issues
app.command(name="import")(import_autocare)


# Add a callback to print version information
@app.callback()
def callback(
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Print verbose output"
    ),
    version: bool = typer.Option(
        False, "--version", help="Print version and exit"
    ),
) -> None:
    """
    AutoCare data management tool.
    """
    if version:
        typer.echo("AutoCare CLI v0.1.0")
        raise typer.Exit()


# Make sure CLI entry point works correctly
def main() -> None:
    """Command line entry point."""
    try:
        # Print a clear header to indicate the command is running
        print("=" * 80)
        print(" AUTOCARE DATA MANAGEMENT TOOL ")
        print("=" * 80)

        app()
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
